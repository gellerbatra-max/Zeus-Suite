"""Builds the Section 4 response schemas from ORM rows. Kept separate from app/schemas.py (the
shape definitions) since these functions need a session to resolve `workflow_status_id` -> the
`{code, label}` the API contract returns -- the ORM models store only the FK, no `relationship()`
mappings are declared (Milestone 1 kept the model layer intentionally plain)."""

from sqlalchemy.orm import Session

from app import schemas
from app.models import Bundle, Folder, Marker, Order, Piece, Style, WorkflowStatus


def workflow_status_out(session: Session, status_id: int) -> schemas.WorkflowStatusOut:
    status = session.get(WorkflowStatus, status_id)
    return schemas.WorkflowStatusOut(code=status.code, label=status.label)


def folder_out(folder: Folder) -> schemas.FolderOut:
    return schemas.FolderOut.model_validate(folder)


def piece_out(session: Session, piece: Piece) -> schemas.PieceOut:
    return schemas.PieceOut(
        id=piece.id,
        folder_id=piece.folder_id,
        piece_code=piece.piece_code,
        piece_name=piece.piece_name,
        piece_type=piece.piece_type,
        base_size=piece.base_size,
        description=piece.description,
        current_version_id=piece.current_version_id,
        workflow_status=workflow_status_out(session, piece.workflow_status_id),
        lock_owner_id=piece.lock_owner_id,
        version=piece.version,
        created_at=piece.created_at,
        created_by=piece.created_by,
    )


def style_out(session: Session, style: Style) -> schemas.StyleOut:
    return schemas.StyleOut(
        id=style.id,
        folder_id=style.folder_id,
        style_number=style.style_number,
        style_name=style.style_name,
        season=style.season,
        customer=style.customer,
        description=style.description,
        workflow_status=workflow_status_out(session, style.workflow_status_id),
        version=style.version,
        created_at=style.created_at,
        created_by=style.created_by,
    )


def marker_out(session: Session, marker: Marker) -> schemas.MarkerOut:
    return schemas.MarkerOut(
        id=marker.id,
        folder_id=marker.folder_id,
        marker_code=marker.marker_code,
        marker_name=marker.marker_name,
        order_id=marker.order_id,
        fabric_width=marker.fabric_width,
        marker_length=marker.marker_length,
        ply_count=marker.ply_count,
        utilization_pct=marker.utilization_pct,
        matching_method=marker.matching_method,
        current_version_id=marker.current_version_id,
        workflow_status=workflow_status_out(session, marker.workflow_status_id),
        version=marker.version,
        created_at=marker.created_at,
        created_by=marker.created_by,
    )


def order_out(session: Session, order: Order) -> schemas.OrderOut:
    return schemas.OrderOut(
        id=order.id,
        folder_id=order.folder_id,
        order_number=order.order_number,
        style_id=order.style_id,
        customer=order.customer,
        due_date=order.due_date,
        total_quantity=order.total_quantity,
        workflow_status=workflow_status_out(session, order.workflow_status_id),
        version=order.version,
        created_at=order.created_at,
        created_by=order.created_by,
    )


def bundle_out(session: Session, bundle: Bundle) -> schemas.BundleOut:
    return schemas.BundleOut(
        id=bundle.id,
        order_id=bundle.order_id,
        marker_id=bundle.marker_id,
        piece_id=bundle.piece_id,
        bundle_code=bundle.bundle_code,
        rfid_tag=bundle.rfid_tag,
        qr_code=bundle.qr_code,
        size_code=bundle.size_code,
        quantity=bundle.quantity,
        workflow_status=workflow_status_out(session, bundle.workflow_status_id),
        cut_at=bundle.cut_at,
        version=bundle.version,
        created_at=bundle.created_at,
        created_by=bundle.created_by,
    )
