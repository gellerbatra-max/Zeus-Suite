"""Test-only helpers: talk to the real running data-platform-api (see conftest.py), and grant
RBAC roles via a direct DB write -- the same one-time admin-bootstrap pattern data-platform-api's
own tests and marker-making-service's tests use (every RBAC system needs an out-of-band way to
create its first admin; there's no HTTP path for that yet on any service)."""

import os
import uuid

import httpx
import psycopg

PLATFORM_BASE_URL = "http://127.0.0.1:8098"
# The platform subprocess (conftest.py) already respects a DATABASE_URL override in its own
# environment; this direct psycopg connection has to match it or grant_role silently writes to
# (or, as happened once, reads from) the wrong database -- e.g. when a developer points the
# subprocess at an isolated test database via DATABASE_URL to avoid colliding with another
# service's migrations on the shared `zeus_suite` DB. psycopg wants a plain postgresql:// URL,
# not SQLAlchemy's postgresql+psycopg:// form, hence the strip.
PLATFORM_DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://zeus:zeus@localhost:5432/zeus_suite"
).replace("postgresql+psycopg://", "postgresql://")


def _raise_on_error(response: httpx.Response) -> None:
    if response.status_code >= 400:
        response.read()
        response.raise_for_status()


def platform_client(headers: dict[str, str]) -> httpx.Client:
    """Auto-raises on any 4xx/5xx so a broken test-setup step fails loudly at the call site,
    instead of surfacing later as a confusing KeyError on a malformed response body."""
    return httpx.Client(
        base_url=PLATFORM_BASE_URL, headers=headers, timeout=30.0,
        event_hooks={"response": [_raise_on_error]},
    )


def grant_role(org_code: str, username: str, role_code: str) -> None:
    with psycopg.connect(PLATFORM_DATABASE_URL, autocommit=True) as conn, conn.cursor() as cur:
        cur.execute("SELECT id FROM dmp.organizations WHERE code = %s", (org_code,))
        org_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM dmp.users WHERE organization_id = %s AND username = %s", (org_id, username))
        user_id = cur.fetchone()[0]
        cur.execute("SELECT id FROM dmp.roles WHERE code = %s", (role_code,))
        role_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO dmp.user_roles (user_id, role_id, folder_id, granted_by) "
            "VALUES (%s, %s, NULL, %s) ON CONFLICT DO NOTHING",
            (user_id, role_id, user_id),
        )


def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]
