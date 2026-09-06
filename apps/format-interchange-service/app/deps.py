from fastapi import Depends, Header

from app.db import SessionLocal
from app.platform_client import PlatformClient


def get_identity_headers(
    x_dev_user: str = Header(..., alias="X-Dev-User"),
    x_dev_org: str = Header("DEV", alias="X-Dev-Org"),
) -> dict[str, str]:
    """Same dev-stub convention as every other service in the suite (see data-platform-api's own
    app/auth.py) -- forwarded, not re-implemented."""
    return {"X-Dev-User": x_dev_user, "X-Dev-Org": x_dev_org}


def get_platform_client(identity_headers: dict[str, str] = Depends(get_identity_headers)) -> PlatformClient:
    return PlatformClient(identity_headers)


def get_actor(client: PlatformClient = Depends(get_platform_client)) -> dict:
    """This service has no identity table of its own -- `organization_id`/`user_id` for its local
    `interchange_job` bookkeeping rows are resolved by asking the platform who the caller is,
    the same JIT-provisioning `/me` call every other client in the suite uses."""
    return client.get("/me")


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
