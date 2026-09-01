"""Section 4.5: markers."""

import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session

from app.auditing import record_audit
from app.deps import (
    Actor,
    check_if_match_version,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import conflict, not_found
from app.models import Bundle, Marker, MarkerPiece, MarkerVersion, WorkflowStatus
from app.schemas import (
    BeginVersionRequest,
    BeginVersionResponse,
    CompleteVersionRequest,
    DownloadUrlResponse,
    MarkerCreate,
    MarkerPatch,
    MarkerPieceIn,
    Page,
    StatusTransitionRequest,
)
from app.serializers import marker_out
from app.storage import generate_download_sas_url, generate_upload_sas_url
from app.workflow_engine import plan_transition

router = APIRouter(prefix="/markers", tags=["markers"])
STORAGE_CONTAINER = "dmp-markers"


def _get_marker_or_404(db: Session, marker_id: uuid.UUID) -> Marker:
    marker = db.get(Marker, marker_id)
    if marker is None or marker.deleted_at is not None:
        raise not_found("Marker")
    return marker


def _extension_for(file_format: str) -> str:
    return {"native": "native", "cut_data": "cut", "plot_file": "plt", "dxf_aama": "dxf"}.get(file_format, "bin")


@router.get("", response_model=Page)
def list_markers(
    folder_id: uuid.UUID | None = Query(None),
    order_id: uuid.UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "marker.read", request_id=request_id, entity_type="marker", action="marker.list")
    query = db.query(Marker).filter(Marker.organization_id == actor.organization_id, Marker.deleted_at.is_(None))
    if folder_id is not None:
        query = query.filter(Marker.folder_id == folder_id)
    if order_id is not None:
        query = query.filter(Marker.order_id == order_id)
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[marker_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("", status_code=201)
def create_marker(
    body: MarkerCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "marker.write", request_id=request_id, entity_type="marker", action="marker.create",
        folder_id=body.folder_id,
    )
    initial_status = db.query(WorkflowStatus).filter_by(entity_type="marker", is_initial=True).one()
    marker = Marker(
        organization_id=actor.organization_id,
        folder_id=body.folder_id,
        marker_code=body.marker_code,
        marker_name=body.marker_name,
        order_id=body.order_id,
        fabric_width=body.fabric_width,
        workflow_status_id=initial_status.id,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(marker)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="marker.create",
        entity_type="marker", entity_id=marker.id, folder_id=marker.folder_id, request_id=request_id,
        after_state={"marker_code": marker.marker_code}, result="success",
    )
    return marker_out(db, marker)


@router.get("/{marker_id}")
def get_marker(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.read", request_id=request_id, entity_type="marker", action="marker.read",
        folder_id=marker.folder_id, entity_id=marker.id,
    )
    return marker_out(db, marker)


@router.patch("/{marker_id}")
def patch_marker(
    marker_id: uuid.UUID,
    body: MarkerPatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.write", request_id=request_id, entity_type="marker", action="marker.update",
        folder_id=marker.folder_id, entity_id=marker.id,
    )
    check_if_match_version(if_match_version, marker.version)

    before = {"marker_name": marker.marker_name, "fabric_width": float(marker.fabric_width) if marker.fabric_width else None}
    for field in ("marker_name", "fabric_width", "matching_method"):
        value = getattr(body, field)
        if value is not None:
            setattr(marker, field, value)
    marker.updated_by = actor.user_id
    marker.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="marker.update",
        entity_type="marker", entity_id=marker.id, folder_id=marker.folder_id, request_id=request_id,
        before_state=before, after_state={"marker_name": marker.marker_name}, result="success",
    )
    return marker_out(db, marker)


@router.delete("/{marker_id}", status_code=204)
def delete_marker(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.delete", request_id=request_id, entity_type="marker", action="marker.delete",
        folder_id=marker.folder_id, entity_id=marker.id,
    )
    if db.query(Bundle.id).filter_by(marker_id=marker.id).first():
        raise conflict("Marker is still referenced by a bundle.")

    marker.deleted_at = datetime.now(UTC)
    marker.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="marker.delete",
        entity_type="marker", entity_id=marker.id, folder_id=marker.folder_id, request_id=request_id, result="success",
    )


@router.get("/{marker_id}/versions")
def list_marker_versions(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.read", request_id=request_id, entity_type="marker", action="marker.versions.list",
        folder_id=marker.folder_id,
    )
    rows = db.query(MarkerVersion).filter_by(marker_id=marker.id).order_by(MarkerVersion.version_number.desc()).all()
    return [
        {"id": str(r.id), "version_number": r.version_number, "file_format": r.file_format,
         "size_bytes": r.size_bytes, "created_at": r.created_at.isoformat()}
        for r in rows
    ]


@router.post("/{marker_id}/versions", response_model=BeginVersionResponse)
def begin_marker_version(
    marker_id: uuid.UUID,
    body: BeginVersionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.write", request_id=request_id, entity_type="marker", action="marker.version.begin",
        folder_id=marker.folder_id, entity_id=marker.id,
    )
    next_number = db.query(MarkerVersion).filter_by(marker_id=marker.id).count() + 1
    blob_key = f"{actor.organization_id}/{marker.id}/{next_number}.{_extension_for(body.file_format)}"
    version = MarkerVersion(
        marker_id=marker.id,
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
        version_id=version.id, upload_url=upload_url,
        expires_at=datetime.now(UTC) + timedelta(minutes=expiry_minutes),
    )


@router.post("/{marker_id}/versions/{version_id}/complete")
def complete_marker_version(
    marker_id: uuid.UUID,
    version_id: uuid.UUID,
    body: CompleteVersionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.write", request_id=request_id, entity_type="marker", action="marker.version.complete",
        folder_id=marker.folder_id, entity_id=marker.id,
    )
    version = db.get(MarkerVersion, version_id)
    if version is None or version.marker_id != marker.id:
        raise not_found("Marker version")

    version.checksum_sha256 = body.checksum_sha256
    marker.current_version_id = version.id
    marker.updated_by = actor.user_id
    marker.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="marker.version.complete",
        entity_type="marker", entity_id=marker.id, folder_id=marker.folder_id, request_id=request_id,
        after_state={"current_version_id": str(version.id)}, result="success",
    )
    return marker_out(db, marker)


@router.get("/{marker_id}/versions/{version_id}/download-url", response_model=DownloadUrlResponse)
def get_marker_download_url(
    marker_id: uuid.UUID,
    version_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.read", request_id=request_id, entity_type="marker", action="marker.version.download_url",
        folder_id=marker.folder_id,
    )
    version = db.get(MarkerVersion, version_id)
    if version is None or version.marker_id != marker.id:
        raise not_found("Marker version")
    expiry_minutes = 15
    url = generate_download_sas_url(version.storage_container, version.storage_key, expiry_minutes=expiry_minutes)
    return DownloadUrlResponse(download_url=url, expires_at=datetime.now(UTC) + timedelta(minutes=expiry_minutes))


@router.post("/{marker_id}/status")
def transition_marker_status(
    marker_id: uuid.UUID,
    body: StatusTransitionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    plan = plan_transition(db, "marker", marker.workflow_status_id, body.to_status)
    require_permission(
        db, actor, plan.required_permission, request_id=request_id, entity_type="marker",
        action="marker.status_change", folder_id=marker.folder_id, entity_id=marker.id,
    )
    before_status = plan.from_status.code
    marker.workflow_status_id = plan.to_status.id
    marker.updated_by = actor.user_id
    marker.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="marker.status_change",
        entity_type="marker", entity_id=marker.id, folder_id=marker.folder_id, request_id=request_id,
        before_state={"workflow_status": before_status}, after_state={"workflow_status": plan.to_status.code},
        result="success",
    )
    return marker_out(db, marker)


@router.get("/{marker_id}/pieces")
def list_marker_pieces(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.read", request_id=request_id, entity_type="marker", action="marker.pieces.list",
        folder_id=marker.folder_id,
    )
    rows = db.query(MarkerPiece).filter_by(marker_id=marker.id).all()
    return [
        {"piece_id": str(r.piece_id), "piece_version_id": str(r.piece_version_id), "size_code": r.size_code,
         "quantity": r.quantity, "placement_data": r.placement_data}
        for r in rows
    ]


@router.put("/{marker_id}/pieces")
def replace_marker_pieces(
    marker_id: uuid.UUID,
    body: list[MarkerPieceIn],
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    """Bulk-replaces the marker's piece placement list in one call -- the normal path after a
    nesting run completes (Section 4.5)."""
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.write", request_id=request_id, entity_type="marker", action="marker.pieces.replace",
        folder_id=marker.folder_id, entity_id=marker.id,
    )
    db.query(MarkerPiece).filter_by(marker_id=marker.id).delete()
    for row in body:
        db.add(
            MarkerPiece(
                marker_id=marker.id, piece_id=row.piece_id, piece_version_id=row.piece_version_id,
                size_code=row.size_code, quantity=row.quantity, placement_data=row.placement_data,
            )
        )
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="marker.pieces.replace",
        entity_type="marker", entity_id=marker.id, folder_id=marker.folder_id, request_id=request_id,
        after_state={"piece_count": len(body)}, result="success",
    )
    return [{"piece_id": str(r.piece_id), "size_code": r.size_code, "quantity": r.quantity} for r in body]


@router.get("/{marker_id}/bundles")
def get_marker_bundles(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id)
    require_permission(
        db, actor, "marker.read", request_id=request_id, entity_type="marker", action="marker.bundles",
        folder_id=marker.folder_id,
    )
    rows = db.query(Bundle).filter_by(marker_id=marker.id).all()
    return [{"id": str(r.id), "bundle_code": r.bundle_code} for r in rows]
