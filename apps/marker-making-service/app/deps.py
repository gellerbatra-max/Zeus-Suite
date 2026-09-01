from fastapi import Depends, Header

from app.platform_client import PlatformClient


def get_identity_headers(
    x_dev_user: str = Header(..., alias="X-Dev-User"),
    x_dev_org: str = Header("DEV", alias="X-Dev-Org"),
) -> dict[str, str]:
    """Same dev-stub convention as data-platform-api's own auth (see that service's app/auth.py)
    -- forwarded, not re-implemented."""
    return {"X-Dev-User": x_dev_user, "X-Dev-Org": x_dev_org}


def get_platform_client(identity_headers: dict[str, str] = Depends(get_identity_headers)) -> PlatformClient:
    return PlatformClient(identity_headers)
