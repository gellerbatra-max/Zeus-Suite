"""Section 4.3: pieces."""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app.auditing import record_audit
from app.auth import resolve_permissions
from app.deps import (
    Actor,
    check_if_match_version,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import api_error, conflict, not_found
from app.models import (
    Marker,
    MarkerPiece,
    Piece,
    PieceVersion,
    Style,
    StylePiece,
    WorkflowStatus,
)
from app.schemas import (
    BeginVersionRequest,
    BeginVersionResponse,
    CompleteVersionRequest,
    DownloadUrlResponse,
    Page,
    PieceCreate,
    PiecePatch,
    StatusTransitionRequest,
)
from app.serializers import piece_out
from app.storage import generate_download_sas_url, generate_upload_sas_url
from app.workflow_engine import plan_transition

router = APIRouter(prefix="/pieces", tags=["pieces"])

STORAGE_CONTAINER = "dmp-pieces"
LOCK_IDLE_TIMEOUT = timedelta(hours=4)


def _get_piece_or_404(db: Session, piece_id: uuid.UUID) -> Piece:
    piece = db.get(Piece, piece_id)
    if piece is None or piece.deleted_at is not None:
        raise not_found("Piece")
    return piece


@router.get("", response_model=Page)
def list_pieces(
    folder_id: uuid.UUID | None = Query(None),
    workflow_status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "piece.read", request_id=request_id, entity_type="piece", action="piece.list")
    query = db.query(Piece).filter(Piece.organization_id == actor.organization_id, Piece.deleted_at.is_(None))
    if folder_id is not None:
        query = query.filter(Piece.folder_id == folder_id)
    if workflow_status is not None:
        status_row = db.query(WorkflowStatus).filter_by(entity_type="piece", code=workflow_status).one_or_none()
        query = query.filter(Piece.workflow_status_id == (status_row.id if status_row else -1))
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[piece_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("", status_code=201)
def create_piece(
    body: PieceCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "piece.write", request_id=request_id, entity_type="piece", action="piece.create",
        folder_id=body.folder_id,
    )
    initial_status = (
        db.query(WorkflowStatus).filter_by(entity_type="piece", is_initial=True).one()
    )
    piece = Piece(
        organization_id=actor.organization_id,
        folder_id=body.folder_id,
        piece_code=body.piece_code,
        piece_name=body.piece_name,
        piece_type=body.piece_type,
        base_size=body.base_size,
        description=body.description,
        workflow_status_id=initial_status.id,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(piece)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.create",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id,
        after_state={"piece_code": piece.piece_code, "piece_name": piece.piece_name}, result="success",
    )
    return piece_out(db, piece)


@router.get("/{piece_id}")
def get_piece(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.read", request_id=request_id, entity_type="piece", action="piece.read",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    return piece_out(db, piece)


@router.patch("/{piece_id}")
def patch_piece(
    piece_id: uuid.UUID,
    body: PiecePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.write", request_id=request_id, entity_type="piece", action="piece.update",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    check_if_match_version(if_match_version, piece.version)

    before = {"piece_name": piece.piece_name, "description": piece.description, "folder_id": str(piece.folder_id)}
    for field in ("piece_name", "description", "base_size", "folder_id"):
        value = getattr(body, field)
        if value is not None:
            setattr(piece, field, value)
    piece.updated_by = actor.user_id
    piece.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.update",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id,
        before_state=before, after_state={"piece_name": piece.piece_name, "description": piece.description},
        result="success",
    )
    return piece_out(db, piece)


@router.delete("/{piece_id}", status_code=204)
def delete_piece(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.delete", request_id=request_id, entity_type="piece", action="piece.delete",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    referenced = (
        db.query(StylePiece.id).filter_by(piece_id=piece.id).first()
        or db.query(MarkerPiece.id).filter_by(piece_id=piece.id).first()
    )
    if referenced:
        raise conflict("Piece is still referenced by a style or marker.")

    piece.deleted_at = datetime.now(UTC)
    piece.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.delete",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id, result="success",
    )


@router.post("/{piece_id}/lock")
def lock_piece(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.write", request_id=request_id, entity_type="piece", action="piece.lock",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    now = datetime.now(UTC)
    lock_stale = piece.lock_acquired_at is not None and (now - piece.lock_acquired_at) > LOCK_IDLE_TIMEOUT
    if piece.lock_owner_id is not None and piece.lock_owner_id != actor.user_id and not lock_stale:
        raise conflict("Piece is already locked by another user.")

    piece.lock_owner_id = actor.user_id
    piece.lock_acquired_at = now
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.lock",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id, result="success",
    )
    return piece_out(db, piece)


@router.post("/{piece_id}/unlock")
def unlock_piece(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.write", request_id=request_id, entity_type="piece", action="piece.unlock",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    is_other_users_lock = piece.lock_owner_id is not None and piece.lock_owner_id != actor.user_id
    if is_other_users_lock and "piece.force_unlock" not in resolve_permissions(db, actor.user_id, folder_id=piece.folder_id):
        raise api_error(403, "permission_denied", "Only the lock owner or piece.force_unlock may unlock this piece.")

    piece.lock_owner_id = None
    piece.lock_acquired_at = None
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.unlock",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id, result="success",
    )
    return piece_out(db, piece)


@router.get("/{piece_id}/versions")
def list_versions(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.read", request_id=request_id, entity_type="piece", action="piece.versions.list",
        folder_id=piece.folder_id,
    )
    rows = (
        db.query(PieceVersion)
        .filter_by(piece_id=piece.id)
        .order_by(PieceVersion.version_number.desc())
        .all()
    )
    return [
        {"id": str(r.id), "version_number": r.version_number, "file_format": r.file_format,
         "size_bytes": r.size_bytes, "created_at": r.created_at.isoformat()}
        for r in rows
    ]


@router.post("/{piece_id}/versions", response_model=BeginVersionResponse)
def begin_version(
    piece_id: uuid.UUID,
    body: BeginVersionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.write", request_id=request_id, entity_type="piece", action="piece.version.begin",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    next_number = (
        db.query(PieceVersion).filter_by(piece_id=piece.id).count() + 1
    )
    blob_key = f"{actor.organization_id}/{piece.id}/{next_number}.{_extension_for(body.file_format)}"
    version = PieceVersion(
        piece_id=piece.id,
        version_number=next_number,
        storage_container=STORAGE_CONTAINER,
        storage_key=blob_key,
        file_format=body.file_format,
        checksum_sha256="pending",
        size_bytes=body.size_bytes,
        comment=body.comment,
        created_by=actor.user_id,
    )
    db.add(version)
    db.flush()
    expiry_minutes = 15
    upload_url = generate_upload_sas_url(STORAGE_CONTAINER, blob_key, expiry_minutes=expiry_minutes)
    return BeginVersionResponse(
        version_id=version.id,
        upload_url=upload_url,
        expires_at=datetime.now(UTC) + timedelta(minutes=expiry_minutes),
    )


def _extension_for(file_format: str) -> str:
    return {"native": "pat", "dxf_aama": "dxf", "dxf_asdf": "dxf", "iges": "igs"}.get(file_format, "bin")


@router.post("/{piece_id}/versions/{version_id}/complete")
def complete_version(
    piece_id: uuid.UUID,
    version_id: uuid.UUID,
    body: CompleteVersionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.write", request_id=request_id, entity_type="piece", action="piece.version.complete",
        folder_id=piece.folder_id, entity_id=piece.id,
    )
    version = db.get(PieceVersion, version_id)
    if version is None or version.piece_id != piece.id:
        raise not_found("Piece version")

    version.checksum_sha256 = body.checksum_sha256
    piece.current_version_id = version.id
    piece.updated_by = actor.user_id
    piece.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.version.complete",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id,
        after_state={"current_version_id": str(version.id), "version_number": version.version_number},
        result="success",
    )
    return piece_out(db, piece)


@router.get("/{piece_id}/versions/{version_id}/download-url", response_model=DownloadUrlResponse)
def get_download_url(
    piece_id: uuid.UUID,
    version_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.read", request_id=request_id, entity_type="piece", action="piece.version.download_url",
        folder_id=piece.folder_id,
    )
    version = db.get(PieceVersion, version_id)
    if version is None or version.piece_id != piece.id:
        raise not_found("Piece version")

    expiry_minutes = 15
    url = generate_download_sas_url(version.storage_container, version.storage_key, expiry_minutes=expiry_minutes)
    return DownloadUrlResponse(download_url=url, expires_at=datetime.now(UTC) + timedelta(minutes=expiry_minutes))


@router.post("/{piece_id}/status")
def transition_status(
    piece_id: uuid.UUID,
    body: StatusTransitionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    plan = plan_transition(db, "piece", piece.workflow_status_id, body.to_status)
    require_permission(
        db, actor, plan.required_permission, request_id=request_id, entity_type="piece",
        action="piece.status_change", folder_id=piece.folder_id, entity_id=piece.id,
    )

    before_status = plan.from_status.code
    piece.workflow_status_id = plan.to_status.id
    piece.updated_by = actor.user_id
    piece.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="piece.status_change",
        entity_type="piece", entity_id=piece.id, folder_id=piece.folder_id, request_id=request_id,
        before_state={"workflow_status": before_status}, after_state={"workflow_status": plan.to_status.code},
        detail=body.comment, result="success",
    )
    return piece_out(db, piece)


@router.get("/{piece_id}/styles")
def get_piece_styles(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.read", request_id=request_id, entity_type="piece", action="piece.styles",
        folder_id=piece.folder_id,
    )
    rows = (
        db.query(Style)
        .join(StylePiece, StylePiece.style_id == Style.id)
        .filter(StylePiece.piece_id == piece.id)
        .all()
    )
    return [{"id": str(r.id), "style_number": r.style_number, "style_name": r.style_name} for r in rows]


@router.get("/{piece_id}/markers")
def get_piece_markers(
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    piece = _get_piece_or_404(db, piece_id)
    require_permission(
        db, actor, "piece.read", request_id=request_id, entity_type="piece", action="piece.markers",
        folder_id=piece.folder_id,
    )
    rows = (
        db.query(Marker)
        .join(MarkerPiece, MarkerPiece.marker_id == Marker.id)
        .filter(MarkerPiece.piece_id == piece.id)
        .all()
    )
    return [{"id": str(r.id), "marker_code": r.marker_code, "marker_name": r.marker_name} for r in rows]
