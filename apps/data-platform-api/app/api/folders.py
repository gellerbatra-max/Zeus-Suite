"""Section 4.2: folders (the "Storage Area" equivalent)."""

import uuid
from datetime import UTC, datetime

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
from app.models import Bundle, Folder, Marker, Order, Piece, Style
from app.schemas import FolderCreate, FolderMove, FolderOut, FolderRename, Page
from app.serializers import folder_out

router = APIRouter(prefix="/folders", tags=["folders"])


def _get_folder_or_404(db: Session, folder_id: uuid.UUID) -> Folder:
    folder = db.get(Folder, folder_id)
    if folder is None or folder.deleted_at is not None:
        raise not_found("Folder")
    return folder


def _compute_path(db: Session, parent_id: uuid.UUID | None, name: str) -> str:
    if parent_id is None:
        return f"/{name}"
    parent = _get_folder_or_404(db, parent_id)
    return f"{parent.path.rstrip('/')}/{name}"


@router.get("", response_model=Page)
def list_folders(
    parent_id: uuid.UUID | None = Query(None),
    q: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "folder.read", request_id=request_id, entity_type="folder", action="folder.list")
    query = db.query(Folder).filter(
        Folder.organization_id == actor.organization_id,
        Folder.deleted_at.is_(None),
        Folder.parent_id == parent_id,
    )
    if q:
        query = query.filter(Folder.name.ilike(f"%{q}%"))
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[folder_out(r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("", response_model=FolderOut, status_code=201)
def create_folder(
    body: FolderCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "folder.write", request_id=request_id, entity_type="folder", action="folder.create",
        folder_id=body.parent_id,
    )
    path = _compute_path(db, body.parent_id, body.name)
    folder = Folder(
        organization_id=actor.organization_id,
        parent_id=body.parent_id,
        name=body.name,
        path=path,
        folder_type=body.folder_type,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(folder)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="folder.create",
        entity_type="folder", entity_id=folder.id, folder_id=folder.id, request_id=request_id,
        after_state={"name": folder.name, "path": folder.path}, result="success",
    )
    return folder_out(folder)


@router.get("/{folder_id}", response_model=FolderOut)
def get_folder(
    folder_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    folder = _get_folder_or_404(db, folder_id)
    require_permission(
        db, actor, "folder.read", request_id=request_id, entity_type="folder", action="folder.read",
        folder_id=folder.id, entity_id=folder.id,
    )
    return folder_out(folder)


@router.patch("/{folder_id}", response_model=FolderOut)
def rename_folder(
    folder_id: uuid.UUID,
    body: FolderRename,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    folder = _get_folder_or_404(db, folder_id)
    require_permission(
        db, actor, "folder.write", request_id=request_id, entity_type="folder", action="folder.rename",
        folder_id=folder.id, entity_id=folder.id,
    )
    check_if_match_version(if_match_version, folder.version)

    before = {"name": folder.name, "path": folder.path}
    folder.name = body.name
    folder.path = _compute_path(db, folder.parent_id, body.name)
    folder.updated_by = actor.user_id
    folder.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="folder.rename",
        entity_type="folder", entity_id=folder.id, folder_id=folder.id, request_id=request_id,
        before_state=before, after_state={"name": folder.name, "path": folder.path}, result="success",
    )
    return folder_out(folder)


@router.post("/{folder_id}/move", response_model=FolderOut)
def move_folder(
    folder_id: uuid.UUID,
    body: FolderMove,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    folder = _get_folder_or_404(db, folder_id)
    require_permission(
        db, actor, "folder.write", request_id=request_id, entity_type="folder", action="folder.move",
        folder_id=folder.id, entity_id=folder.id,
    )
    before_path = folder.path
    old_prefix = folder.path
    folder.parent_id = body.new_parent_id
    folder.path = _compute_path(db, body.new_parent_id, folder.name)
    folder.updated_by = actor.user_id
    folder.version += 1
    db.flush()

    # Recompute descendants' materialized paths in the same transaction.
    descendants = db.query(Folder).filter(Folder.path.like(f"{old_prefix}/%")).all()
    for descendant in descendants:
        descendant.path = folder.path + descendant.path[len(old_prefix):]

    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="folder.move",
        entity_type="folder", entity_id=folder.id, folder_id=folder.id, request_id=request_id,
        before_state={"path": before_path}, after_state={"path": folder.path}, result="success",
    )
    return folder_out(folder)


@router.delete("/{folder_id}", status_code=204)
def delete_folder(
    folder_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    folder = _get_folder_or_404(db, folder_id)
    require_permission(
        db, actor, "folder.delete", request_id=request_id, entity_type="folder", action="folder.delete",
        folder_id=folder.id, entity_id=folder.id,
    )

    has_children = db.query(Folder.id).filter(Folder.parent_id == folder.id, Folder.deleted_at.is_(None)).first()
    has_content = any(
        db.query(model.id).filter(model.folder_id == folder.id, model.deleted_at.is_(None)).first()
        for model in (Piece, Style, Marker, Order)
    )
    if has_children or has_content:
        raise conflict("Folder or a descendant still contains non-deleted items.")

    folder.deleted_at = datetime.now(UTC)
    folder.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="folder.delete",
        entity_type="folder", entity_id=folder.id, folder_id=folder.id, request_id=request_id, result="success",
    )


@router.get("/{folder_id}/children", response_model=Page)
def list_children(
    folder_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    folder = _get_folder_or_404(db, folder_id)
    require_permission(
        db, actor, "folder.read", request_id=request_id, entity_type="folder", action="folder.children",
        folder_id=folder.id,
    )
    rows = db.query(Folder).filter(Folder.parent_id == folder.id, Folder.deleted_at.is_(None)).all()
    return Page(items=[folder_out(r) for r in rows], page=1, page_size=len(rows) or 1, total=len(rows))


@router.get("/{folder_id}/contents", response_model=Page)
def list_contents(
    folder_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    """Immediate-child pieces + styles + markers + orders + bundles, one paginated mixed list,
    each item tagged `entity_type` -- the endpoint the folder browser calls (Section 6.1)."""
    folder = _get_folder_or_404(db, folder_id)
    require_permission(
        db, actor, "folder.read", request_id=request_id, entity_type="folder", action="folder.contents",
        folder_id=folder.id,
    )
    items: list[dict] = []
    for entity_type, model, code_field in (
        ("piece", Piece, "piece_code"),
        ("style", Style, "style_number"),
        ("marker", Marker, "marker_code"),
        ("order", Order, "order_number"),
    ):
        for row in db.query(model).filter(model.folder_id == folder.id, model.deleted_at.is_(None)).all():
            items.append(
                {
                    "entity_type": entity_type,
                    "id": str(row.id),
                    "code": getattr(row, code_field),
                    "updated_at": row.updated_at.isoformat(),
                }
            )
    for bundle in db.query(Bundle).filter(Bundle.order_id.in_(
        db.query(Order.id).filter(Order.folder_id == folder.id)
    )).all():
        items.append({"entity_type": "bundle", "id": str(bundle.id), "code": bundle.bundle_code,
                       "updated_at": bundle.updated_at.isoformat()})

    return Page(items=items, page=1, page_size=len(items) or 1, total=len(items))
