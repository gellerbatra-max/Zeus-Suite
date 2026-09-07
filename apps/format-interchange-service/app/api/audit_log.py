"""GET /audit-log -- reads this service's own audit trail (Sec 7 Step 5). Gated by
`interchange.review` (the same permission that gates viewing migration items/findings; auditing
one's own actions is a review-class concern, not named separately in Sec 5's four-code list)."""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import AuditLogEntry
from app.permissions import require_review

router = APIRouter(tags=["audit"])


@router.get("/audit-log")
def list_audit_log(
    entity_type: str | None = Query(None),
    entity_id: str | None = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    actor: dict = Depends(require_review),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLogEntry).filter(AuditLogEntry.organization_id == uuid.UUID(actor["organization_id"]))
    if entity_type:
        query = query.filter(AuditLogEntry.entity_type == entity_type)
    if entity_id:
        query = query.filter(AuditLogEntry.entity_id == uuid.UUID(entity_id))
    rows = query.order_by(AuditLogEntry.created_at.desc()).limit(limit).all()
    return [
        {
            "id": str(r.id),
            "actor_id": str(r.actor_id),
            "action": r.action,
            "entity_type": r.entity_type,
            "entity_id": str(r.entity_id) if r.entity_id else None,
            "result": r.result,
            "detail": r.detail,
            "created_at": r.created_at.isoformat(),
        }
        for r in rows
    ]
