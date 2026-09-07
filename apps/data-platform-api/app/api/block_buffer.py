"""Marker Making Sec 1.6 (block / buffer / fuse-blocking, Gerber depth): block_buffer_rule_tables
(reusable per-side L/T/R/B amount config, keyed by rule_no) and fuse_blocks (groups pieces on one
marker into a fusing block). Both stored faithfully, opaque-payload style for fuse_blocks'
piece_placement_ids -- the platform doesn't interpret which pieces those ids mean, that's
marker-making-service's job (it also computes x/y/width/height from the pieces' current placements
before calling create/patch here, since placement_data itself is opaque to this service too).

Scoped to rectangular fuse blocks only. Create Fusing Marker and Cut Net Parts are deferred -- both
need a cutter_parameter_table, which doesn't exist yet (Sec 1.10 / Phase 3 territory)."""

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
from app.errors import not_found
from app.models import BlockBufferRuleTable, FuseBlock, Marker
from app.schemas import (
    BlockBufferRuleTableCreate,
    BlockBufferRuleTablePatch,
    FuseBlockCreate,
    FuseBlockPatch,
    Page,
)
from app.serializers import block_buffer_rule_table_out, fuse_block_out

router = APIRouter(tags=["block-buffer", "fuse-blocks"])


def _get_rule_table_or_404(db: Session, table_id: uuid.UUID, org_id: uuid.UUID) -> BlockBufferRuleTable:
    row = db.get(BlockBufferRuleTable, table_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Block/buffer rule table")
    return row


def _get_marker_or_404(db: Session, marker_id: uuid.UUID, org_id: uuid.UUID) -> Marker:
    marker = db.get(Marker, marker_id)
    if marker is None or marker.deleted_at is not None or marker.organization_id != org_id:
        raise not_found("Marker")
    return marker


def _get_fuse_block_or_404(db: Session, fuse_block_id: uuid.UUID, org_id: uuid.UUID) -> FuseBlock:
    row = db.get(FuseBlock, fuse_block_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Fuse block")
    return row


# -- Block Buffer Rule Table ------------------------------------------------------------------


@router.get("/block-buffer-rule-tables", response_model=Page)
def list_block_buffer_rule_tables(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "block_buffer_rule_table.read", request_id=request_id,
        entity_type="block_buffer_rule_table", action="block_buffer_rule_table.list",
    )
    query = db.query(BlockBufferRuleTable).filter(
        BlockBufferRuleTable.organization_id == actor.organization_id, BlockBufferRuleTable.deleted_at.is_(None)
    )
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[block_buffer_rule_table_out(r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("/block-buffer-rule-tables", status_code=201)
def create_block_buffer_rule_table(
    body: BlockBufferRuleTableCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "block_buffer_rule_table.write", request_id=request_id,
        entity_type="block_buffer_rule_table", action="block_buffer_rule_table.create",
    )
    row = BlockBufferRuleTable(
        organization_id=actor.organization_id,
        name=body.name,
        rule_no=body.rule_no,
        rule_type=body.rule_type,
        mode=body.mode,
        left_amt=body.left_amt,
        top_amt=body.top_amt,
        right_amt=body.right_amt,
        bottom_amt=body.bottom_amt,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="block_buffer_rule_table.create",
        entity_type="block_buffer_rule_table", entity_id=row.id, request_id=request_id,
        after_state={"name": row.name, "rule_no": row.rule_no, "rule_type": row.rule_type}, result="success",
    )
    return block_buffer_rule_table_out(row)


@router.get("/block-buffer-rule-tables/{table_id}")
def get_block_buffer_rule_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_rule_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "block_buffer_rule_table.read", request_id=request_id,
        entity_type="block_buffer_rule_table", action="block_buffer_rule_table.read", entity_id=row.id,
    )
    return block_buffer_rule_table_out(row)


@router.patch("/block-buffer-rule-tables/{table_id}")
def patch_block_buffer_rule_table(
    table_id: uuid.UUID,
    body: BlockBufferRuleTablePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_rule_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "block_buffer_rule_table.write", request_id=request_id,
        entity_type="block_buffer_rule_table", action="block_buffer_rule_table.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)

    before = {"name": row.name, "rule_type": row.rule_type}
    for field in ("name", "rule_no", "rule_type", "mode", "left_amt", "top_amt", "right_amt", "bottom_amt"):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="block_buffer_rule_table.update",
        entity_type="block_buffer_rule_table", entity_id=row.id, request_id=request_id,
        before_state=before, after_state={"name": row.name, "rule_type": row.rule_type}, result="success",
    )
    return block_buffer_rule_table_out(row)


@router.delete("/block-buffer-rule-tables/{table_id}", status_code=204)
def delete_block_buffer_rule_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_rule_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "block_buffer_rule_table.delete", request_id=request_id,
        entity_type="block_buffer_rule_table", action="block_buffer_rule_table.delete", entity_id=row.id,
    )
    # Unlike matching_rule_table_id (a real marker FK column), a piece's block/buffer rule
    # assignment lives inside marker_pieces.placement_data -- opaque JSON this service doesn't
    # index or query -- so there's no cheap "still referenced" check to run here. Deleting a rule
    # still in use just orphans the reference (the same class of simplification as matching's
    # "no way to unset a marker's rule table" limitation).
    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="block_buffer_rule_table.delete",
        entity_type="block_buffer_rule_table", entity_id=row.id, request_id=request_id, result="success",
    )


# -- Fuse Blocks -------------------------------------------------------------------------------


@router.get("/markers/{marker_id}/fuse-blocks")
def list_fuse_blocks(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id, actor.organization_id)
    require_permission(
        db, actor, "fuse_block.read", request_id=request_id,
        entity_type="fuse_block", action="fuse_block.list", folder_id=marker.folder_id,
    )
    rows = (
        db.query(FuseBlock)
        .filter(FuseBlock.marker_id == marker.id, FuseBlock.deleted_at.is_(None))
        .order_by(FuseBlock.created_at)
        .all()
    )
    return [fuse_block_out(r) for r in rows]


@router.post("/markers/{marker_id}/fuse-blocks", status_code=201)
def create_fuse_block(
    marker_id: uuid.UUID,
    body: FuseBlockCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id, actor.organization_id)
    require_permission(
        db, actor, "fuse_block.write", request_id=request_id,
        entity_type="fuse_block", action="fuse_block.create", folder_id=marker.folder_id,
    )
    row = FuseBlock(
        organization_id=actor.organization_id,
        marker_id=marker.id,
        x=body.x, y=body.y, width=body.width, height=body.height,
        piece_placement_ids=body.piece_placement_ids,
        block_amount=body.block_amount,
        reduce_amount=body.reduce_amount,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="fuse_block.create",
        entity_type="fuse_block", entity_id=row.id, folder_id=marker.folder_id, request_id=request_id,
        after_state={"piece_count": len(body.piece_placement_ids)}, result="success",
    )
    return fuse_block_out(row)


@router.delete("/markers/{marker_id}/fuse-blocks", status_code=204)
def delete_all_fuse_blocks(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id, actor.organization_id)
    require_permission(
        db, actor, "fuse_block.delete", request_id=request_id,
        entity_type="fuse_block", action="fuse_block.delete_all", folder_id=marker.folder_id,
    )
    rows = db.query(FuseBlock).filter(FuseBlock.marker_id == marker.id, FuseBlock.deleted_at.is_(None)).all()
    now = datetime.now(UTC)
    for row in rows:
        row.deleted_at = now
        row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="fuse_block.delete_all",
        entity_type="fuse_block", entity_id=None, folder_id=marker.folder_id, request_id=request_id,
        after_state={"count": len(rows)}, result="success",
    )


@router.get("/fuse-blocks/{fuse_block_id}")
def get_fuse_block(
    fuse_block_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_fuse_block_or_404(db, fuse_block_id, actor.organization_id)
    require_permission(
        db, actor, "fuse_block.read", request_id=request_id, entity_type="fuse_block",
        action="fuse_block.read", entity_id=row.id,
    )
    return fuse_block_out(row)


@router.patch("/fuse-blocks/{fuse_block_id}")
def patch_fuse_block(
    fuse_block_id: uuid.UUID,
    body: FuseBlockPatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_fuse_block_or_404(db, fuse_block_id, actor.organization_id)
    require_permission(
        db, actor, "fuse_block.write", request_id=request_id, entity_type="fuse_block",
        action="fuse_block.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    for field in ("piece_placement_ids", "x", "y", "width", "height", "block_amount", "reduce_amount"):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="fuse_block.update",
        entity_type="fuse_block", entity_id=row.id, request_id=request_id,
        after_state={"piece_count": len(row.piece_placement_ids)}, result="success",
    )
    return fuse_block_out(row)


@router.delete("/fuse-blocks/{fuse_block_id}", status_code=204)
def delete_fuse_block(
    fuse_block_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_fuse_block_or_404(db, fuse_block_id, actor.organization_id)
    require_permission(
        db, actor, "fuse_block.delete", request_id=request_id, entity_type="fuse_block",
        action="fuse_block.delete", entity_id=row.id,
    )
    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="fuse_block.delete",
        entity_type="fuse_block", entity_id=row.id, request_id=request_id, result="success",
    )
