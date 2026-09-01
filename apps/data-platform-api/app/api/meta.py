"""Section 4.1: auth/session."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.auth import resolve_permissions
from app.deps import Actor, get_current_actor, get_db
from app.errors import api_error
from app.schemas import MeOut
from app.storage import get_blob_service_client

router = APIRouter(tags=["meta"])


@router.get("/healthz")
def healthz(db: Session = Depends(get_db)):
    """Liveness/readiness probe: checks DB connectivity and object-storage reachability
    (Section 4.1)."""
    db.execute(text("SELECT 1"))
    try:
        get_blob_service_client().get_service_properties()
    except Exception as exc:
        raise api_error(503, "storage_unreachable", "Object storage is not reachable.") from exc
    return {"status": "ok"}


@router.get("/me", response_model=MeOut)
def me(actor: Actor = Depends(get_current_actor), db: Session = Depends(get_db)):
    permissions = sorted(resolve_permissions(db, actor.user_id))
    return MeOut(
        id=actor.user_id,
        username=actor.username,
        full_name=actor.full_name,
        organization_id=actor.organization_id,
        permissions=permissions,
    )
