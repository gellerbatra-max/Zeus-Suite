"""Builds the Section 4 response schemas from ORM rows. Kept separate from app/schemas.py (the
shape definitions) since these functions need a session to resolve `workflow_status_id` -> the
`{code, label}` the API contract returns -- the ORM models store only the FK, no `relationship()`
mappings are declared (Milestone 1 kept the model layer intentionally plain)."""

from sqlalchemy.orm import Session

from app import schemas
from app.models import (
    BlockBufferRuleTable,
    Bundle,
    Folder,
    FuseBlock,
    Marker,
    MatchingRuleTable,
    Order,
    Piece,
    SpliceMark,
    Style,
    WorkflowStatus,
)


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
        fabric_weight_per_unit_area=marker.fabric_weight_per_unit_area,
        splice_min_length=marker.splice_min_length,
        splice_max_length=marker.splice_max_length,
        splice_margin=marker.splice_margin,
        splice_separation=marker.splice_separation,
        matching_method=marker.matching_method,
        matching_rule_table_id=marker.matching_rule_table_id,
        current_version_id=marker.current_version_id,
        workflow_status=workflow_status_out(session, marker.workflow_status_id),
        version=marker.version,
        created_at=marker.created_at,
        created_by=marker.created_by,
    )


def matching_rule_table_out(session: Session, row: MatchingRuleTable) -> schemas.MatchingRuleTableOut:
    return schemas.MatchingRuleTableOut(
        id=row.id,
        name=row.name,
        method=row.method,
        plaid_repeat=row.plaid_repeat,
        stripe_repeat=row.stripe_repeat,
        offsets_json=row.offsets_json,
        stripe_definitions_json=row.stripe_definitions_json,
        stripe_marks_json=row.stripe_marks_json,
        weave_line_json=row.weave_line_json,
        material_pattern_json=row.material_pattern_json,
        version=row.version,
        created_at=row.created_at,
        created_by=row.created_by,
    )


def block_buffer_rule_table_out(row: BlockBufferRuleTable) -> schemas.BlockBufferRuleTableOut:
    return schemas.BlockBufferRuleTableOut(
        id=row.id,
        name=row.name,
        rule_no=row.rule_no,
        rule_type=row.rule_type,
        mode=row.mode,
        left_amt=row.left_amt,
        top_amt=row.top_amt,
        right_amt=row.right_amt,
        bottom_amt=row.bottom_amt,
        version=row.version,
        created_at=row.created_at,
        created_by=row.created_by,
    )


def fuse_block_out(row: FuseBlock) -> schemas.FuseBlockOut:
    return schemas.FuseBlockOut(
        id=row.id,
        marker_id=row.marker_id,
        shape=row.shape,
        x=row.x,
        y=row.y,
        width=row.width,
        height=row.height,
        piece_placement_ids=row.piece_placement_ids,
        block_amount=row.block_amount,
        reduce_amount=row.reduce_amount,
        version=row.version,
        created_at=row.created_at,
        created_by=row.created_by,
    )


def splice_mark_out(row: SpliceMark) -> schemas.SpliceMarkOut:
    return schemas.SpliceMarkOut(
        id=row.id,
        marker_id=row.marker_id,
        start_x=row.start_x,
        end_x=row.end_x,
        source=row.source,
        roll_id=row.roll_id,
        version=row.version,
        created_at=row.created_at,
        created_by=row.created_by,
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
        target_length=order.target_length,
        target_utilization_pct=order.target_utilization_pct,
        shrink_x_pct=order.shrink_x_pct,
        shrink_y_pct=order.shrink_y_pct,
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
