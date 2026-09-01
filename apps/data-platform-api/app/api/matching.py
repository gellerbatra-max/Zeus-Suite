"""Marker Making Sec 1.4/2 (new): matching rule tables. The platform stores and returns
offsets_json / stripe_definitions_json / stripe_marks_json faithfully -- it does not validate
their internal shape (element ids, offset-count caps, etc.); that interpretation lives in
marker-making-service, per the same opaque-payload philosophy as marker_pieces.placement_data."""

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
from app.models import Marker, MatchingRuleTable
from app.schemas import (
    JsonArrayReplace,
    MatchingRuleTableCreate,
    MatchingRuleTablePatch,
    OffsetsReplace,
    Page,
)
from app.serializers import matching_rule_table_out

router = APIRouter(prefix="/matching-rule-tables", tags=["matching-rule-tables"])


def _get_table_or_404(db: Session, table_id: uuid.UUID, org_id: uuid.UUID) -> MatchingRuleTable:
    row = db.get(MatchingRuleTable, table_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Matching rule table")
    return row


@router.get("", response_model=Page)
def list_matching_rule_tables(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "matching_rule_table.read", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.list",
    )
    query = db.query(MatchingRuleTable).filter(
        MatchingRuleTable.organization_id == actor.organization_id, MatchingRuleTable.deleted_at.is_(None)
    )
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[matching_rule_table_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("", status_code=201)
def create_matching_rule_table(
    body: MatchingRuleTableCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.create",
    )
    row = MatchingRuleTable(
        organization_id=actor.organization_id,
        name=body.name,
        method=body.method,
        plaid_repeat=body.plaid_repeat,
        stripe_repeat=body.stripe_repeat,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="matching_rule_table.create",
        entity_type="matching_rule_table", entity_id=row.id, request_id=request_id,
        after_state={"name": row.name, "method": row.method}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.get("/{table_id}")
def get_matching_rule_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.read", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.read", entity_id=row.id,
    )
    return matching_rule_table_out(db, row)


@router.patch("/{table_id}")
def patch_matching_rule_table(
    table_id: uuid.UUID,
    body: MatchingRuleTablePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)

    before = {"name": row.name, "method": row.method}
    for field in ("name", "method", "plaid_repeat", "stripe_repeat"):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="matching_rule_table.update",
        entity_type="matching_rule_table", entity_id=row.id, request_id=request_id,
        before_state=before, after_state={"name": row.name, "method": row.method}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.delete("/{table_id}", status_code=204)
def delete_matching_rule_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.delete", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.delete", entity_id=row.id,
    )
    if db.query(Marker.id).filter_by(matching_rule_table_id=row.id).filter(Marker.deleted_at.is_(None)).first():
        raise conflict("Matching rule table is still referenced by a marker.")

    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="matching_rule_table.delete",
        entity_type="matching_rule_table", entity_id=row.id, request_id=request_id, result="success",
    )


@router.put("/{table_id}/offsets")
def replace_offsets(
    table_id: uuid.UUID,
    body: OffsetsReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.offsets.replace", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.offsets_json = {"horizontal": body.horizontal, "vertical": body.vertical}
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.offsets.replace", entity_type="matching_rule_table", entity_id=row.id,
        request_id=request_id, after_state=row.offsets_json, result="success",
    )
    return matching_rule_table_out(db, row)


@router.put("/{table_id}/stripe-definitions")
def replace_stripe_definitions(
    table_id: uuid.UUID,
    body: JsonArrayReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.stripe_definitions.replace",
        entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.stripe_definitions_json = body.items
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.stripe_definitions.replace", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, after_state={"count": len(body.items)}, result="success",
    )
    return matching_rule_table_out(db, row)


@router.put("/{table_id}/stripe-marks")
def replace_stripe_marks(
    table_id: uuid.UUID,
    body: JsonArrayReplace,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "matching_rule_table.write", request_id=request_id,
        entity_type="matching_rule_table", action="matching_rule_table.stripe_marks.replace", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    row.stripe_marks_json = body.items
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="matching_rule_table.stripe_marks.replace", entity_type="matching_rule_table",
        entity_id=row.id, request_id=request_id, after_state={"count": len(body.items)}, result="success",
    )
    return matching_rule_table_out(db, row)
