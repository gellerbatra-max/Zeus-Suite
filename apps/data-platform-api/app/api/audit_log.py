"""Section 4.9: audit log ("Activity Log" equivalent). No DELETE/"clear all" endpoint exists here
by design -- destructive audit-log clearing is deliberately not carried forward (Section 2.9)."""

import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import (
    Actor,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import not_found
from app.models import AuditLog
from app.schemas import AuditLogOut, Page

router = APIRouter(prefix="/audit-log", tags=["audit-log"])


@router.get("", response_model=Page)
def list_audit_log(
    entity_type: str | None = Query(None),
    entity_id: uuid.UUID | None = Query(None),
    user_id: uuid.UUID | None = Query(None),
    action: str | None = Query(None),
    from_: datetime | None = Query(None, alias="from"),
    to: datetime | None = Query(None),
    result: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "audit.read", request_id=request_id, entity_type="audit_log", action="audit.list")
    query = db.query(AuditLog).filter(AuditLog.organization_id == actor.organization_id)
    if entity_type is not None:
        query = query.filter(AuditLog.entity_type == entity_type)
    if entity_id is not None:
        query = query.filter(AuditLog.entity_id == entity_id)
    if user_id is not None:
        query = query.filter(AuditLog.user_id == user_id)
    if action is not None:
        query = query.filter(AuditLog.action == action)
    if from_ is not None:
        query = query.filter(AuditLog.occurred_at >= from_)
    if to is not None:
        query = query.filter(AuditLog.occurred_at <= to)
    if result is not None:
        query = query.filter(AuditLog.result == result)

    query = query.order_by(AuditLog.occurred_at.desc())
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[AuditLogOut.model_validate(r, from_attributes=True) for r in rows], page=page, page_size=page_size, total=total)


@router.get("/{entry_id}", response_model=AuditLogOut)
def get_audit_entry(
    entry_id: int,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "audit.read", request_id=request_id, entity_type="audit_log", action="audit.read")
    entry = db.get(AuditLog, entry_id)
    if entry is None or entry.organization_id != actor.organization_id:
        raise not_found("Audit log entry")
    return AuditLogOut.model_validate(entry, from_attributes=True)
