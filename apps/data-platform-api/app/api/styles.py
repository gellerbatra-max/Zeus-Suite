"""Section 4.4: styles."""

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
from app.models import Order, Piece, Style, StylePiece, WorkflowStatus
from app.schemas import (
    Page,
    StatusTransitionRequest,
    StyleCreate,
    StylePatch,
    StylePieceAdd,
)
from app.serializers import style_out
from app.workflow_engine import plan_transition

router = APIRouter(prefix="/styles", tags=["styles"])


def _get_style_or_404(db: Session, style_id: uuid.UUID, org_id: uuid.UUID) -> Style:
    style = db.get(Style, style_id)
    if style is None or style.deleted_at is not None or style.organization_id != org_id:
        raise not_found("Style")
    return style


@router.get("", response_model=Page)
def list_styles(
    folder_id: uuid.UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "style.read", request_id=request_id, entity_type="style", action="style.list")
    query = db.query(Style).filter(Style.organization_id == actor.organization_id, Style.deleted_at.is_(None))
    if folder_id is not None:
        query = query.filter(Style.folder_id == folder_id)
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[style_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("", status_code=201)
def create_style(
    body: StyleCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "style.write", request_id=request_id, entity_type="style", action="style.create",
        folder_id=body.folder_id,
    )
    initial_status = db.query(WorkflowStatus).filter_by(entity_type="style", is_initial=True).one()
    style = Style(
        organization_id=actor.organization_id,
        folder_id=body.folder_id,
        style_number=body.style_number,
        style_name=body.style_name,
        season=body.season,
        customer=body.customer,
        description=body.description,
        workflow_status_id=initial_status.id,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(style)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="style.create",
        entity_type="style", entity_id=style.id, folder_id=style.folder_id, request_id=request_id,
        after_state={"style_number": style.style_number}, result="success",
    )
    return style_out(db, style)


@router.get("/{style_id}")
def get_style(
    style_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.read", request_id=request_id, entity_type="style", action="style.read",
        folder_id=style.folder_id, entity_id=style.id,
    )
    return style_out(db, style)


@router.patch("/{style_id}")
def patch_style(
    style_id: uuid.UUID,
    body: StylePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.write", request_id=request_id, entity_type="style", action="style.update",
        folder_id=style.folder_id, entity_id=style.id,
    )
    check_if_match_version(if_match_version, style.version)

    before = {"style_name": style.style_name, "description": style.description}
    for field in ("style_name", "season", "customer", "description", "folder_id"):
        value = getattr(body, field)
        if value is not None:
            setattr(style, field, value)
    style.updated_by = actor.user_id
    style.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="style.update",
        entity_type="style", entity_id=style.id, folder_id=style.folder_id, request_id=request_id,
        before_state=before, after_state={"style_name": style.style_name}, result="success",
    )
    return style_out(db, style)


@router.delete("/{style_id}", status_code=204)
def delete_style(
    style_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.delete", request_id=request_id, entity_type="style", action="style.delete",
        folder_id=style.folder_id, entity_id=style.id,
    )
    if db.query(Order.id).filter_by(style_id=style.id).filter(Order.deleted_at.is_(None)).first():
        raise conflict("Style is still referenced by a non-deleted order.")

    style.deleted_at = datetime.now(UTC)
    style.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="style.delete",
        entity_type="style", entity_id=style.id, folder_id=style.folder_id, request_id=request_id, result="success",
    )


@router.post("/{style_id}/status")
def transition_style_status(
    style_id: uuid.UUID,
    body: StatusTransitionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    plan = plan_transition(db, "style", style.workflow_status_id, body.to_status)
    require_permission(
        db, actor, plan.required_permission, request_id=request_id, entity_type="style",
        action="style.status_change", folder_id=style.folder_id, entity_id=style.id,
    )
    before_status = plan.from_status.code
    style.workflow_status_id = plan.to_status.id
    style.updated_by = actor.user_id
    style.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="style.status_change",
        entity_type="style", entity_id=style.id, folder_id=style.folder_id, request_id=request_id,
        before_state={"workflow_status": before_status}, after_state={"workflow_status": plan.to_status.code},
        result="success",
    )
    return style_out(db, style)


@router.get("/{style_id}/pieces")
def list_style_pieces(
    style_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.read", request_id=request_id, entity_type="style", action="style.pieces.list",
        folder_id=style.folder_id,
    )
    rows = db.query(StylePiece).filter_by(style_id=style.id).order_by(StylePiece.sequence).all()
    return [{"piece_id": str(r.piece_id), "piece_role": r.piece_role, "sequence": r.sequence} for r in rows]


@router.post("/{style_id}/pieces", status_code=201)
def add_style_piece(
    style_id: uuid.UUID,
    body: StylePieceAdd,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.write", request_id=request_id, entity_type="style", action="style.pieces.add",
        folder_id=style.folder_id, entity_id=style.id,
    )
    if db.get(Piece, body.piece_id) is None:
        raise not_found("Piece")

    link = StylePiece(
        style_id=style.id, piece_id=body.piece_id, piece_role=body.piece_role,
        sequence=body.sequence, added_by=actor.user_id,
    )
    db.add(link)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="style.pieces.add",
        entity_type="style", entity_id=style.id, folder_id=style.folder_id, request_id=request_id,
        after_state={"piece_id": str(body.piece_id)}, result="success",
    )
    return {"piece_id": str(link.piece_id), "piece_role": link.piece_role, "sequence": link.sequence}


@router.delete("/{style_id}/pieces/{piece_id}", status_code=204)
def remove_style_piece(
    style_id: uuid.UUID,
    piece_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.write", request_id=request_id, entity_type="style", action="style.pieces.remove",
        folder_id=style.folder_id, entity_id=style.id,
    )
    link = db.query(StylePiece).filter_by(style_id=style.id, piece_id=piece_id).one_or_none()
    if link is None:
        raise not_found("Style/piece link")
    db.delete(link)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="style.pieces.remove",
        entity_type="style", entity_id=style.id, folder_id=style.folder_id, request_id=request_id,
        before_state={"piece_id": str(piece_id)}, result="success",
    )


@router.get("/{style_id}/orders")
def get_style_orders(
    style_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    style = _get_style_or_404(db, style_id, actor.organization_id)
    require_permission(
        db, actor, "style.read", request_id=request_id, entity_type="style", action="style.orders",
        folder_id=style.folder_id,
    )
    rows = db.query(Order).filter_by(style_id=style.id).all()
    return [{"id": str(r.id), "order_number": r.order_number} for r in rows]
