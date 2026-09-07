"""Marker Making Sec 1.5 (layrules automation): dmp.layrule_search_tables (reusable named
Yes/No criteria, same shape as block_buffer_rule_tables) and dmp.layrules (a captured snapshot of
one marker's placements, reusable on a different marker with compatible pieces).

This platform stores placements_json faithfully and does no piece-matching or area-comparison
itself -- that's marker-making-service's job (it already interprets placement_data everywhere
else), the same opaque-payload philosophy as marker_pieces.placement_data itself."""

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
from app.models import Layrule, LayruleSearchTable
from app.schemas import (
    LayruleCreate,
    LayrulePatch,
    LayruleSearchTableCreate,
    LayruleSearchTablePatch,
    Page,
)
from app.serializers import layrule_out, layrule_search_table_out

router = APIRouter(tags=["layrules"])


def _get_search_table_or_404(db: Session, table_id: uuid.UUID, org_id: uuid.UUID) -> LayruleSearchTable:
    row = db.get(LayruleSearchTable, table_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Layrule search table")
    return row


def _get_layrule_or_404(db: Session, layrule_id: uuid.UUID, org_id: uuid.UUID) -> Layrule:
    row = db.get(Layrule, layrule_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Layrule")
    return row


# -- Layrule Search Parameter Table --------------------------------------------------------------


@router.get("/layrule-search-tables", response_model=Page)
def list_layrule_search_tables(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "layrule_search_table.read", request_id=request_id,
        entity_type="layrule_search_table", action="layrule_search_table.list",
    )
    query = db.query(LayruleSearchTable).filter(
        LayruleSearchTable.organization_id == actor.organization_id, LayruleSearchTable.deleted_at.is_(None)
    )
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[layrule_search_table_out(r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("/layrule-search-tables", status_code=201)
def create_layrule_search_table(
    body: LayruleSearchTableCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "layrule_search_table.write", request_id=request_id,
        entity_type="layrule_search_table", action="layrule_search_table.create",
    )
    row = LayruleSearchTable(
        organization_id=actor.organization_id,
        name=body.name,
        area_compare=body.area_compare,
        area_deviation_pct=body.area_deviation_pct,
        copy_dynamics=body.copy_dynamics,
        allow_overrides=body.allow_overrides,
        include_marker_name=body.include_marker_name,
        include_marker_description=body.include_marker_description,
        comment=body.comment,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="layrule_search_table.create", entity_type="layrule_search_table", entity_id=row.id,
        request_id=request_id, after_state={"name": row.name}, result="success",
    )
    return layrule_search_table_out(row)


@router.get("/layrule-search-tables/{table_id}")
def get_layrule_search_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_search_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "layrule_search_table.read", request_id=request_id,
        entity_type="layrule_search_table", action="layrule_search_table.read", entity_id=row.id,
    )
    return layrule_search_table_out(row)


@router.patch("/layrule-search-tables/{table_id}")
def patch_layrule_search_table(
    table_id: uuid.UUID,
    body: LayruleSearchTablePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_search_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "layrule_search_table.write", request_id=request_id,
        entity_type="layrule_search_table", action="layrule_search_table.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    for field in (
        "name", "area_compare", "area_deviation_pct", "copy_dynamics", "allow_overrides",
        "include_marker_name", "include_marker_description", "comment",
    ):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="layrule_search_table.update", entity_type="layrule_search_table", entity_id=row.id,
        request_id=request_id, after_state={"name": row.name}, result="success",
    )
    return layrule_search_table_out(row)


@router.delete("/layrule-search-tables/{table_id}", status_code=204)
def delete_layrule_search_table(
    table_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_search_table_or_404(db, table_id, actor.organization_id)
    require_permission(
        db, actor, "layrule_search_table.delete", request_id=request_id,
        entity_type="layrule_search_table", action="layrule_search_table.delete", entity_id=row.id,
    )
    # Same class of simplification as block_buffer_rule_table's delete: a marker's
    # layrule_search_table_id reference isn't checked here, so deleting a table still referenced
    # by a marker just orphans that reference rather than being blocked.
    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id,
        action="layrule_search_table.delete", entity_type="layrule_search_table", entity_id=row.id,
        request_id=request_id, result="success",
    )


# -- Layrules -------------------------------------------------------------------------------------


@router.get("/layrules", response_model=Page)
def list_layrules(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "layrule.read", request_id=request_id, entity_type="layrule", action="layrule.list",
    )
    query = db.query(Layrule).filter(Layrule.organization_id == actor.organization_id, Layrule.deleted_at.is_(None))
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[layrule_out(r) for r in rows], page=page, page_size=page_size, total=total)


@router.post("/layrules", status_code=201)
def create_layrule(
    body: LayruleCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(
        db, actor, "layrule.write", request_id=request_id, entity_type="layrule", action="layrule.create",
    )
    row = Layrule(
        organization_id=actor.organization_id,
        name=body.name,
        source_marker_id=body.source_marker_id,
        placements_json=body.placements_json,
        piece_count=len(body.placements_json),
        comment=body.comment,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="layrule.create",
        entity_type="layrule", entity_id=row.id, request_id=request_id,
        after_state={"name": row.name, "piece_count": row.piece_count}, result="success",
    )
    return layrule_out(row)


@router.get("/layrules/{layrule_id}")
def get_layrule(
    layrule_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_layrule_or_404(db, layrule_id, actor.organization_id)
    require_permission(
        db, actor, "layrule.read", request_id=request_id, entity_type="layrule",
        action="layrule.read", entity_id=row.id,
    )
    return layrule_out(row)


@router.patch("/layrules/{layrule_id}")
def patch_layrule(
    layrule_id: uuid.UUID,
    body: LayrulePatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_layrule_or_404(db, layrule_id, actor.organization_id)
    require_permission(
        db, actor, "layrule.write", request_id=request_id, entity_type="layrule",
        action="layrule.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    for field in ("name", "comment"):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="layrule.update",
        entity_type="layrule", entity_id=row.id, request_id=request_id,
        after_state={"name": row.name}, result="success",
    )
    return layrule_out(row)


@router.delete("/layrules/{layrule_id}", status_code=204)
def delete_layrule(
    layrule_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_layrule_or_404(db, layrule_id, actor.organization_id)
    require_permission(
        db, actor, "layrule.delete", request_id=request_id, entity_type="layrule",
        action="layrule.delete", entity_id=row.id,
    )
    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="layrule.delete",
        entity_type="layrule", entity_id=row.id, request_id=request_id, result="success",
    )
