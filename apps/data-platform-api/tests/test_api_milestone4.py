"""Milestone 4 exit check (development_roadmap.md's literal Phase 1 exit criteria): a stub/mock
client -- this test, not a real UI -- can create a piece, lock it, upload a version, commit it,
transition its status through the full legal sequence, and read back its full history from
/audit-log, all through the HTTP API with no direct database access.

The one exception: granting the test's dev user an `admin` role before the flow starts, via a
direct DB write. That's a one-time RBAC *bootstrap* step -- every RBAC system needs an
out-of-band way to create its first admin (a deployment script, a seed migration, or the
Section 4.11 RBAC-admin endpoints this pass doesn't build) -- not part of the piece/version/
status/audit-log flow itself, which runs entirely over HTTP below.
"""

import hashlib

from azure.storage.blob import BlobClient
from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "m4-tester", "X-Dev-Org": "M4TEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def test_milestone4_full_http_flow(db_session):
    # First call JIT-provisions the dev user with the default 'viewer' role (Section 5.4).
    resp = client.get("/me", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    assert "piece.read" in resp.json()["permissions"]
    assert "piece.write" not in resp.json()["permissions"]

    _grant_admin(db_session, "M4TEST", "m4-tester")

    # Revocation/grant visibility is immediate -- no caching (Milestone 3's guarantee, exercised
    # here through the HTTP layer instead of resolve_permissions() directly).
    resp = client.get("/me", headers=HEADERS)
    assert "piece.write" in resp.json()["permissions"]

    resp = client.post("/folders", json={"name": "FW26"}, headers=HEADERS)
    assert resp.status_code == 201, resp.text
    folder_id = resp.json()["id"]

    resp = client.post(
        "/pieces",
        json={"folder_id": folder_id, "piece_code": "FRONT-PANEL-01", "piece_name": "Front Panel"},
        headers=HEADERS,
    )
    assert resp.status_code == 201, resp.text
    piece = resp.json()
    piece_id = piece["id"]
    assert piece["workflow_status"]["code"] == "unmade"

    resp = client.post(f"/pieces/{piece_id}/lock", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    assert resp.json()["lock_owner_id"] is not None

    resp = client.post(
        f"/pieces/{piece_id}/versions",
        json={"file_format": "native", "size_bytes": 1024, "comment": "initial draft"},
        headers=HEADERS,
    )
    assert resp.status_code == 200, resp.text
    version = resp.json()

    # The client uploads directly to Blob Storage using the SAS URL -- the API service never
    # sees these bytes (Section 3.3).
    payload = b"fake pattern bytes"
    BlobClient.from_blob_url(version["upload_url"]).upload_blob(payload, overwrite=True)
    checksum = hashlib.sha256(payload).hexdigest()

    resp = client.post(
        f"/pieces/{piece_id}/versions/{version['version_id']}/complete",
        json={"checksum_sha256": checksum},
        headers=HEADERS,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["current_version_id"] == version["version_id"]

    for to_status in ("needs_approval", "made", "approved"):
        resp = client.post(f"/pieces/{piece_id}/status", json={"to_status": to_status}, headers=HEADERS)
        assert resp.status_code == 200, resp.text
        assert resp.json()["workflow_status"]["code"] == to_status

    # An illegal transition (approved is terminal) is rejected with 422, not silently accepted.
    resp = client.post(f"/pieces/{piece_id}/status", json={"to_status": "unmade"}, headers=HEADERS)
    assert resp.status_code == 422

    resp = client.get("/audit-log", params={"entity_type": "piece", "entity_id": piece_id}, headers=HEADERS)
    assert resp.status_code == 200, resp.text
    actions = [row["action"] for row in resp.json()["items"]]
    assert "piece.create" in actions
    assert "piece.lock" in actions
    assert "piece.version.complete" in actions
    assert actions.count("piece.status_change") == 3


def test_permission_denied_is_recorded_and_returns_403(db_session):
    headers = {"X-Dev-User": "no-perms-user", "X-Dev-Org": "M4TEST"}
    client.get("/me", headers=headers)  # JIT-provision with default 'viewer' role only

    resp = client.post("/folders", json={"name": "Should Fail"}, headers=headers)
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "permission_denied"

    resp = client.get(
        "/audit-log",
        params={"action": "folder.create", "result": "denied"},
        headers=HEADERS,  # the admin user from the other test can read the audit log
    )
    assert resp.status_code == 200
    assert any(row["result"] == "denied" for row in resp.json()["items"])


def test_optimistic_concurrency_conflict(db_session):
    resp = client.post("/folders", json={"name": "Concurrency Test"}, headers=HEADERS)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/pieces",
        json={"folder_id": folder_id, "piece_code": "CONCURRENCY-01", "piece_name": "Concurrency Piece"},
        headers=HEADERS,
    )
    piece_id = resp.json()["id"]

    resp = client.patch(
        f"/pieces/{piece_id}",
        json={"piece_name": "Renamed"},
        headers={**HEADERS, "If-Match-Version": "999"},
    )
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "version_conflict"
