"""Test-only helpers: talk to the real running data-platform-api (see conftest.py), and grant
RBAC roles via a direct DB write -- the same one-time admin-bootstrap pattern every other
service's tests in this suite use."""

import hashlib
import json
import os
import uuid

import httpx
import psycopg
from azure.storage.blob import BlobClient

PLATFORM_BASE_URL = "http://127.0.0.1:8097"
PLATFORM_DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://zeus:zeus@localhost:5432/zeus_suite_format_interchange_test"
).replace("postgresql+psycopg://", "postgresql://")


def _raise_on_error(response: httpx.Response) -> None:
    if response.status_code >= 400:
        response.read()
        response.raise_for_status()


def platform_client(headers: dict[str, str]) -> httpx.Client:
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


def seed_piece_with_geometry(client: httpx.Client, folder_id: str, piece_code: str, geometry: dict) -> dict:
    piece = client.post(
        "/pieces", json={"folder_id": folder_id, "piece_code": piece_code, "piece_name": piece_code}
    ).json()

    payload = json.dumps(geometry).encode()
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
