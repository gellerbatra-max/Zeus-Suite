"""Marker Making Sec 1.8 (splice marks / fabric-roll handling): dmp.splice_marks CRUD, following
the exact shape/permission/audit conventions app/api/block_buffer.py's fuse_blocks already
established. This platform stores start_x/end_x/source/roll_id faithfully and does no auto-
placement math itself -- that's marker-making-service's job (see its README): it computes where
splice marks belong from the marker's current placements and the marker's own splice settings
(splice_min_length/splice_max_length/splice_margin/splice_separation, patched via the normal
PATCH /markers/{id} field-copy loop), then calls the create/delete endpoints here exactly like a
human adding a manual mark would."""

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
from app.models import Marker, SpliceMark
from app.schemas import SpliceMarkCreate, SpliceMarkPatch
from app.serializers import splice_mark_out

router = APIRouter(tags=["splice-marks"])


def _get_marker_or_404(db: Session, marker_id: uuid.UUID, org_id: uuid.UUID) -> Marker:
    marker = db.get(Marker, marker_id)
    if marker is None or marker.deleted_at is not None or marker.organization_id != org_id:
        raise not_found("Marker")
    return marker


def _get_splice_mark_or_404(db: Session, mark_id: uuid.UUID, org_id: uuid.UUID) -> SpliceMark:
    row = db.get(SpliceMark, mark_id)
    if row is None or row.deleted_at is not None or row.organization_id != org_id:
        raise not_found("Splice mark")
    return row


@router.get("/markers/{marker_id}/splice-marks")
def list_splice_marks(
    marker_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id, actor.organization_id)
    require_permission(
        db, actor, "splice_mark.read", request_id=request_id,
        entity_type="splice_mark", action="splice_mark.list", folder_id=marker.folder_id,
    )
    rows = (
        db.query(SpliceMark)
        .filter(SpliceMark.marker_id == marker.id, SpliceMark.deleted_at.is_(None))
        .order_by(SpliceMark.start_x)
        .all()
    )
    return [splice_mark_out(r) for r in rows]


@router.post("/markers/{marker_id}/splice-marks", status_code=201)
def create_splice_mark(
    marker_id: uuid.UUID,
    body: SpliceMarkCreate,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id, actor.organization_id)
    require_permission(
        db, actor, "splice_mark.write", request_id=request_id,
        entity_type="splice_mark", action="splice_mark.create", folder_id=marker.folder_id,
    )
    row = SpliceMark(
        organization_id=actor.organization_id,
        marker_id=marker.id,
        start_x=body.start_x, end_x=body.end_x,
        source=body.source, roll_id=body.roll_id,
        created_by=actor.user_id,
        updated_by=actor.user_id,
    )
    db.add(row)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="splice_mark.create",
        entity_type="splice_mark", entity_id=row.id, folder_id=marker.folder_id, request_id=request_id,
        after_state={"start_x": float(row.start_x), "end_x": float(row.end_x), "source": row.source},
        result="success",
    )
    return splice_mark_out(row)


@router.delete("/markers/{marker_id}/splice-marks", status_code=204)
def delete_all_splice_marks(
    marker_id: uuid.UUID,
    source: str | None = Query(None, description="Only delete marks with this source ('auto' or 'manual')."),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    marker = _get_marker_or_404(db, marker_id, actor.organization_id)
    require_permission(
        db, actor, "splice_mark.delete", request_id=request_id,
        entity_type="splice_mark", action="splice_mark.delete_all", folder_id=marker.folder_id,
    )
    query = db.query(SpliceMark).filter(SpliceMark.marker_id == marker.id, SpliceMark.deleted_at.is_(None))
    if source is not None:
        query = query.filter(SpliceMark.source == source)
    rows = query.all()
    now = datetime.now(UTC)
    for row in rows:
        row.deleted_at = now
        row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="splice_mark.delete_all",
        entity_type="splice_mark", entity_id=None, folder_id=marker.folder_id, request_id=request_id,
        after_state={"count": len(rows), "source": source}, result="success",
    )


@router.get("/splice-marks/{mark_id}")
def get_splice_mark(
    mark_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_splice_mark_or_404(db, mark_id, actor.organization_id)
    require_permission(
        db, actor, "splice_mark.read", request_id=request_id, entity_type="splice_mark",
        action="splice_mark.read", entity_id=row.id,
    )
    return splice_mark_out(row)


@router.patch("/splice-marks/{mark_id}")
def patch_splice_mark(
    mark_id: uuid.UUID,
    body: SpliceMarkPatch,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
    if_match_version: int | None = Header(None, alias="If-Match-Version"),
):
    row = _get_splice_mark_or_404(db, mark_id, actor.organization_id)
    require_permission(
        db, actor, "splice_mark.write", request_id=request_id, entity_type="splice_mark",
        action="splice_mark.update", entity_id=row.id,
    )
    check_if_match_version(if_match_version, row.version)
    for field in ("start_x", "end_x", "roll_id"):
        value = getattr(body, field)
        if value is not None:
            setattr(row, field, value)
    row.updated_by = actor.user_id
    row.version += 1
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="splice_mark.update",
        entity_type="splice_mark", entity_id=row.id, request_id=request_id,
        after_state={"start_x": float(row.start_x), "end_x": float(row.end_x)}, result="success",
    )
    return splice_mark_out(row)


@router.delete("/splice-marks/{mark_id}", status_code=204)
def delete_splice_mark(
    mark_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    row = _get_splice_mark_or_404(db, mark_id, actor.organization_id)
    require_permission(
        db, actor, "splice_mark.delete", request_id=request_id, entity_type="splice_mark",
        action="splice_mark.delete", entity_id=row.id,
    )
    row.deleted_at = datetime.now(UTC)
    row.updated_by = actor.user_id
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="splice_mark.delete",
        entity_type="splice_mark", entity_id=row.id, request_id=request_id, result="success",
    )
