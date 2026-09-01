"""Section 7.3's permission-check-then-audit-write path, and the dev-stub auth dependency
(Section 5, with real Entra ID validation deferred -- see app/auth.py). `require_permission` is
the single choke point every mutating/read handler calls into, so permission enforcement and
denial-auditing can never be silently skipped per-handler even though FastAPI's `Depends` alone
can't express folder-scoped checks whose folder_id isn't known until the request body is parsed.
"""

import uuid
from dataclasses import dataclass

from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session

from app.auditing import record_audit
from app.auth import dev_login, resolve_permissions
from app.db import SessionLocal
from app.errors import api_error
from app.models import Organization


def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_request_id(request: Request) -> uuid.UUID:
    return request.state.request_id


@dataclass(frozen=True)
class Actor:
    user_id: uuid.UUID
    organization_id: uuid.UUID
    username: str
    full_name: str


def _get_or_create_dev_org(session: Session, code: str) -> Organization:
    org = session.query(Organization).filter_by(code=code).one_or_none()
    if org is None:
        org = Organization(name=f"Dev Org ({code})", code=code)
        session.add(org)
        session.flush()
    return org


def get_current_actor(
    db: Session = Depends(get_db),
    x_dev_user: str = Header(..., alias="X-Dev-User"),
    x_dev_org: str = Header("DEV", alias="X-Dev-Org"),
    x_dev_email: str | None = Header(None, alias="X-Dev-Email"),
    x_dev_full_name: str | None = Header(None, alias="X-Dev-Full-Name"),
) -> Actor:
    """Local-dev auth: identity comes from plain request headers instead of a validated Entra ID
    JWT (see app/auth.py's `dev_login` docstring for the real-auth swap-over path). Getting or
    creating the organization by header is a dev-only convenience -- a real deployment's
    organizations are provisioned out of band, not auto-created from a request header."""
    org = _get_or_create_dev_org(db, x_dev_org)
    user = dev_login(
        db,
        organization_id=org.id,
        username=x_dev_user,
        email=x_dev_email or f"{x_dev_user}@example.invalid",
        full_name=x_dev_full_name or x_dev_user,
    )
    db.flush()
    return Actor(user_id=user.id, organization_id=org.id, username=user.username, full_name=user.full_name)


def require_permission(
    db: Session,
    actor: Actor,
    code: str,
    *,
    request_id: uuid.UUID,
    entity_type: str,
    action: str,
    folder_id: uuid.UUID | None = None,
    entity_id: uuid.UUID | None = None,
    client_app: str | None = None,
) -> None:
    """Raises 403 if `actor` lacks `code` (scoped to `folder_id` if given), first recording *and
    committing* a 'denied' audit_log row on its own -- independent of the caller's own
    transaction, so a denial is never lost even though the request goes no further. Returns
    normally if granted; the caller writes its own 'success' audit row alongside its mutation,
    in the same transaction, per Section 4's "exactly one audit_log row per call" rule."""
    granted = resolve_permissions(db, actor.user_id, folder_id=folder_id)
    if code in granted:
        return

    record_audit(
        db,
        organization_id=actor.organization_id,
        user_id=actor.user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        folder_id=folder_id,
        request_id=request_id,
        client_app=client_app,
        result="denied",
        detail=f"Missing permission '{code}'.",
    )
    db.commit()
    raise api_error(403, "permission_denied", f"Missing permission '{code}'.")


def check_if_match_version(if_match_version: int | None, current_version: int) -> None:
    """Section 4.0's optimistic-concurrency contract for PATCH endpoints."""
    if if_match_version is None:
        raise api_error(400, "missing_if_match_version", "The If-Match-Version header is required.")
    if if_match_version != current_version:
        raise api_error(
            409,
            "version_conflict",
            f"Expected version {if_match_version}, but the resource is currently at version {current_version}.",
        )
