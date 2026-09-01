"""Section 4.6: orders and bundles."""

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
from app.models import Bundle, Marker, Order, OrderLine, WorkflowStatus
from app.schemas import (
    BundleCreate,
    OrderCreate,
    OrderLineCreate,
    OrderLinePatch,
    OrderPatch,
    Page,
    StatusTransitionRequest,
)
from app.serializers import bundle_out, order_out
from app.workflow_engine import plan_transition

router = APIRouter(tags=["orders"])


def _get_order_or_404(db: Session, order_id: uuid.UUID, org_id: uuid.UUID) -> Order:
    order = db.get(Order, order_id)
    if order is None or order.deleted_at is not None or order.organization_id != org_id:
        raise not_found("Order")
    return order


def _get_bundle_or_404(db: Session, bundle_id: uuid.UUID, org_id: uuid.UUID) -> Bundle:
    bundle = db.get(Bundle, bundle_id)
    if bundle is None or bundle.organization_id != org_id:
        raise not_found("Bundle")
    return bundle


# -- Orders ---------------------------------------------------------------------------------


@router.get("/orders", response_model=Page)
def list_orders(
    style_id: uuid.UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "order.read", request_id=request_id, entity_type="order", action="order.list")
    query = db.query(Order).filter(Order.organization_id == actor.organization_id, Order.deleted_at.is_(None))
    if style_id is not None:
        query = query.filter(Order.style_id == style_id)
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[order_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("/orders", status_code=201)
def create_order(
    body: OrderCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "order.write", request_id=request_id, entity_type="order", action="order.create",
        folder_id=body.folder_id,
    )
    initial_status = db.query(WorkflowStatus).filter_by(entity_type="order", is_initial=True).one()
    order = Order(
        organization_id=actor.organization_id,
        folder_id=body.folder_id,
        order_number=body.order_number,
        style_id=body.style_id,
        customer=body.customer,
        due_date=body.due_date,
        workflow_status_id=initial_status.id,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(order)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="order.create",
        entity_type="order", entity_id=order.id, folder_id=order.folder_id, request_id=request_id,
        after_state={"order_number": order.order_number}, result="success",
    )
    return order_out(db, order)


@router.get("/orders/{order_id}")
def get_order(
    order_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.read", request_id=request_id, entity_type="order", action="order.read",
        folder_id=order.folder_id, entity_id=order.id,
    )
    return order_out(db, order)


@router.patch("/orders/{order_id}")
def patch_order(
    order_id: uuid.UUID,
    body: OrderPatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.write", request_id=request_id, entity_type="order", action="order.update",
        folder_id=order.folder_id, entity_id=order.id,
    )
    check_if_match_version(if_match_version, order.version)

    before = {"customer": order.customer, "due_date": str(order.due_date)}
    for field in ("customer", "due_date"):
        value = getattr(body, field)
        if value is not None:
            setattr(order, field, value)
    order.updated_by = actor.user_id
    order.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="order.update",
        entity_type="order", entity_id=order.id, folder_id=order.folder_id, request_id=request_id,
        before_state=before, after_state={"customer": order.customer}, result="success",
    )
    return order_out(db, order)


@router.delete("/orders/{order_id}", status_code=204)
def delete_order(
    order_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.delete", request_id=request_id, entity_type="order", action="order.delete",
        folder_id=order.folder_id, entity_id=order.id,
    )
    if db.query(Bundle.id).filter_by(order_id=order.id).first():
        raise conflict("Order is still referenced by a non-deleted bundle.")

    order.deleted_at = datetime.now(UTC)
    order.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="order.delete",
        entity_type="order", entity_id=order.id, folder_id=order.folder_id, request_id=request_id, result="success",
    )


@router.post("/orders/{order_id}/status")
def transition_order_status(
    order_id: uuid.UUID,
    body: StatusTransitionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    plan = plan_transition(db, "order", order.workflow_status_id, body.to_status)
    require_permission(
        db, actor, plan.required_permission, request_id=request_id, entity_type="order",
        action="order.status_change", folder_id=order.folder_id, entity_id=order.id,
    )
    before_status = plan.from_status.code
    order.workflow_status_id = plan.to_status.id
    order.updated_by = actor.user_id
    order.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="order.status_change",
        entity_type="order", entity_id=order.id, folder_id=order.folder_id, request_id=request_id,
        before_state={"workflow_status": before_status}, after_state={"workflow_status": plan.to_status.code},
        result="success",
    )
    return order_out(db, order)


@router.get("/orders/{order_id}/lines")
def list_order_lines(
    order_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.read", request_id=request_id, entity_type="order", action="order.lines.list",
        folder_id=order.folder_id,
    )
    rows = db.query(OrderLine).filter_by(order_id=order.id).all()
    return [
        {"id": str(r.id), "size_code": r.size_code, "color": r.color, "quantity": r.quantity,
         "marker_id": str(r.marker_id) if r.marker_id else None}
        for r in rows
    ]


@router.post("/orders/{order_id}/lines", status_code=201)
def add_order_line(
    order_id: uuid.UUID,
    body: OrderLineCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.write", request_id=request_id, entity_type="order", action="order.lines.add",
        folder_id=order.folder_id, entity_id=order.id,
    )
    line = OrderLine(order_id=order.id, size_code=body.size_code, color=body.color, quantity=body.quantity)
    db.add(line)
    order.total_quantity = (order.total_quantity or 0) + body.quantity
    order.updated_by = actor.user_id
    order.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="order.lines.add",
        entity_type="order", entity_id=order.id, folder_id=order.folder_id, request_id=request_id,
        after_state={"size_code": line.size_code, "quantity": line.quantity}, result="success",
    )
    return {"id": str(line.id), "size_code": line.size_code, "color": line.color, "quantity": line.quantity}


@router.patch("/orders/{order_id}/lines/{line_id}")
def patch_order_line(
    order_id: uuid.UUID,
    line_id: uuid.UUID,
    body: OrderLinePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.write", request_id=request_id, entity_type="order", action="order.lines.update",
        folder_id=order.folder_id, entity_id=order.id,
    )
    line = db.query(OrderLine).filter_by(id=line_id, order_id=order.id).one_or_none()
    if line is None:
        raise not_found("Order line")

    if body.marker_id is not None:
        if db.get(Marker, body.marker_id) is None:
            raise not_found("Marker")
        line.marker_id = body.marker_id
    if body.quantity is not None:
        line.quantity = body.quantity

    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="order.lines.update",
        entity_type="order", entity_id=order.id, folder_id=order.folder_id, request_id=request_id,
        after_state={"line_id": str(line.id)}, result="success",
    )
    return {"id": str(line.id), "marker_id": str(line.marker_id) if line.marker_id else None, "quantity": line.quantity}


@router.get("/orders/{order_id}/markers")
def get_order_markers(
    order_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.read", request_id=request_id, entity_type="order", action="order.markers",
        folder_id=order.folder_id,
    )
    rows = db.query(Marker).filter_by(order_id=order.id).all()
    return [{"id": str(r.id), "marker_code": r.marker_code} for r in rows]


@router.get("/orders/{order_id}/bundles")
def get_order_bundles(
    order_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, order_id, actor.organization_id)
    require_permission(
        db, actor, "order.read", request_id=request_id, entity_type="order", action="order.bundles",
        folder_id=order.folder_id,
    )
    rows = db.query(Bundle).filter_by(order_id=order.id).all()
    return [{"id": str(r.id), "bundle_code": r.bundle_code} for r in rows]


# -- Bundles ------------------------------------------------------------------------------------


@router.get("/bundles", response_model=Page)
def list_bundles(
    rfid_tag: str | None = Query(None),
    qr_code: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "bundle.read", request_id=request_id, entity_type="bundle", action="bundle.list")
    query = db.query(Bundle).filter(Bundle.organization_id == actor.organization_id)
    if rfid_tag is not None:
        query = query.filter(Bundle.rfid_tag == rfid_tag)
    if qr_code is not None:
        query = query.filter(Bundle.qr_code == qr_code)
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[bundle_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("/bundles", status_code=201)
def create_bundle(
    body: BundleCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    order = _get_order_or_404(db, body.order_id, actor.organization_id)
    require_permission(
        db, actor, "bundle.write", request_id=request_id, entity_type="bundle", action="bundle.create",
        folder_id=order.folder_id,
    )
    initial_status = db.query(WorkflowStatus).filter_by(entity_type="bundle", is_initial=True).one()
    bundle = Bundle(
        organization_id=actor.organization_id,
        order_id=body.order_id,
        marker_id=body.marker_id,
        piece_id=body.piece_id,
        bundle_code=body.bundle_code,
        size_code=body.size_code,
        color=body.color,
        ply_range_start=body.ply_range_start,
        ply_range_end=body.ply_range_end,
        quantity=body.quantity,
        rfid_tag=body.rfid_tag,
        qr_code=body.qr_code,
        workflow_status_id=initial_status.id,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(bundle)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="bundle.create",
        entity_type="bundle", entity_id=bundle.id, folder_id=order.folder_id, request_id=request_id,
        after_state={"bundle_code": bundle.bundle_code}, result="success",
    )
    return bundle_out(db, bundle)


@router.get("/bundles/{bundle_id}")
def get_bundle(
    bundle_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    bundle = _get_bundle_or_404(db, bundle_id, actor.organization_id)
    require_permission(
        db, actor, "bundle.read", request_id=request_id, entity_type="bundle", action="bundle.read",
        entity_id=bundle.id,
    )
    return bundle_out(db, bundle)


@router.post("/bundles/{bundle_id}/status")
def transition_bundle_status(
    bundle_id: uuid.UUID,
    body: StatusTransitionRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    bundle = _get_bundle_or_404(db, bundle_id, actor.organization_id)
    plan = plan_transition(db, "bundle", bundle.workflow_status_id, body.to_status)
    require_permission(
        db, actor, plan.required_permission, request_id=request_id, entity_type="bundle",
        action="bundle.status_change", entity_id=bundle.id,
    )
    before_status = plan.from_status.code
    bundle.workflow_status_id = plan.to_status.id
    bundle.updated_by = actor.user_id
    bundle.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="bundle.status_change",
        entity_type="bundle", entity_id=bundle.id, request_id=request_id,
        before_state={"workflow_status": before_status}, after_state={"workflow_status": plan.to_status.code},
        result="success",
    )
    return bundle_out(db, bundle)


@router.post("/bundles/{bundle_id}/cut-event")
def record_cut_event(
    bundle_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    bundle = _get_bundle_or_404(db, bundle_id, actor.organization_id)
    plan = plan_transition(db, "bundle", bundle.workflow_status_id, "cut")
    require_permission(
        db, actor, "bundle.write", request_id=request_id, entity_type="bundle", action="bundle.cut_event",
        entity_id=bundle.id,
    )
    bundle.cut_at = datetime.now(UTC)
    bundle.workflow_status_id = plan.to_status.id
    bundle.updated_by = actor.user_id
    bundle.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="bundle.cut_event",
        entity_type="bundle", entity_id=bundle.id, request_id=request_id,
        after_state={"cut_at": bundle.cut_at.isoformat()}, result="success",
    )
    return bundle_out(db, bundle)
