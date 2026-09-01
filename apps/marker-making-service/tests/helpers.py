"""Test-only helpers: seed data directly against the real running data-platform-api (see
conftest.py), and grant RBAC roles via a direct DB write -- the same one-time admin-bootstrap
pattern data-platform-api's own tests use (every RBAC system needs an out-of-band way to create
its first admin; there's no HTTP path for that yet on either service)."""

import hashlib
import uuid

import httpx
import psycopg
from azure.storage.blob import BlobClient

PLATFORM_BASE_URL = "http://127.0.0.1:8099"
PLATFORM_DATABASE_URL = "postgresql://zeus:zeus@localhost:5432/zeus_suite"
AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)


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


def seed_nestable_piece(client: httpx.Client, folder_id: str, piece_code: str, piece_name: str) -> dict:
    """Creates a piece AND commits an initial version, since marker_pieces.piece_version_id is
    NOT NULL on the platform -- a piece can't be placed on a marker until it has one."""
    piece = client.post(
        "/pieces", json={"folder_id": folder_id, "piece_code": piece_code, "piece_name": piece_name}
    ).json()

    payload = b"synthetic piece geometry placeholder"
    begin = client.post(
        f"/pieces/{piece['id']}/versions",
        json={"file_format": "native", "size_bytes": len(payload), "comment": "test seed"},
    ).json()
    BlobClient.from_blob_url(begin["upload_url"]).upload_blob(payload, overwrite=True)
    checksum = hashlib.sha256(payload).hexdigest()
    client.post(f"/pieces/{piece['id']}/versions/{begin['version_id']}/complete", json={"checksum_sha256": checksum})

    return client.get(f"/pieces/{piece['id']}").json()


def unique_suffix() -> str:
    return uuid.uuid4().hex[:8]
