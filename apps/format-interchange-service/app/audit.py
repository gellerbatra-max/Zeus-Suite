"""Writes to this service's own `audit_log` (see app/models.py's `AuditLogEntry` docstring for why
it keeps one instead of relying on data-platform-api's). One call per completed mutating action --
reads are never audited, matching data-platform-api's own `record_audit` convention."""

import uuid

from sqlalchemy.orm import Session

from app.models import AuditLogEntry


def record_audit(
    db: Session,
    actor: dict,
    action: str,
    entity_type: str,
    entity_id: uuid.UUID | str | None = None,
    detail: dict | None = None,
    result: str = "success",
) -> None:
    db.add(
        AuditLogEntry(
            id=uuid.uuid4(),
            organization_id=uuid.UUID(actor["organization_id"]),
            actor_id=uuid.UUID(actor["id"]),
            action=action,
            entity_type=entity_type,
            entity_id=uuid.UUID(str(entity_id)) if entity_id else None,
            result=result,
            detail=detail or {},
        )
    )
