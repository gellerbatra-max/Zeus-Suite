"""Section 4's shared audit-write behavior: every mutating endpoint writes exactly one
`audit_log` row per call, success or denial, in the same transaction as the mutation. This module
is the one place that inserts audit_log rows, so no handler can accidentally skip it."""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models import AuditLog


def record_audit(
    session: Session,
    *,
    organization_id: uuid.UUID,
    user_id: uuid.UUID | None,
    action: str,
    entity_type: str,
    entity_id: uuid.UUID | None,
    request_id: uuid.UUID,
    result: str,
    folder_id: uuid.UUID | None = None,
    before_state: dict[str, Any] | None = None,
    after_state: dict[str, Any] | None = None,
    client_app: str | None = None,
    ip_address: str | None = None,
    detail: str | None = None,
) -> None:
    session.add(
        AuditLog(
            organization_id=organization_id,
            user_id=user_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            folder_id=folder_id,
            before_state=before_state,
            after_state=after_state,
            request_id=request_id,
            client_app=client_app,
            ip_address=ip_address,
            result=result,
            detail=detail,
        )
    )
