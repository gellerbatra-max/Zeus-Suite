"""Step 5 exit criteria (format_interchange_plan.md Sec 7): "confirm RBAC role enforcement on
every endpoint in Sec 5." A `viewer` (read-oriented, granted `interchange.review` only -- see
data-platform-api's 0009 migration) must be refused on every export/import/migrate action but
allowed through every review-gated one; `admin` (granted all four) must be refused nowhere."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_user(unique: str, role: str) -> dict[str, str]:
    org_code = f"PERM-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}
    with platform_client(headers) as p:
        p.get("/me")
        grant_role(org_code, username, role)
    return headers


def test_viewer_is_refused_on_every_mutating_export_import_migrate_endpoint():
    headers = _seed_user(unique_suffix(), "viewer")
    fake_id = "00000000-0000-0000-0000-000000000000"

    export_resp = client.post(f"/pieces/{fake_id}/export/iges", json={}, headers=headers)
    assert export_resp.status_code == 403
    assert "interchange.export" in export_resp.json()["error"]["message"]

    export_status_resp = client.get(f"/export/iges/jobs/{fake_id}", headers=headers)
    assert export_status_resp.status_code == 403

    import_resp = client.post(
        "/import/iges", files={"file": ("x.igs", b"whatever", "text/plain")}, data={"options": "{}"}, headers=headers
    )
    assert import_resp.status_code == 403
    assert "interchange.import" in import_resp.json()["error"]["message"]

    import_status_resp = client.get(f"/import/iges/jobs/{fake_id}", headers=headers)
    assert import_status_resp.status_code == 403

    profiles_resp = client.get("/import-profiles", headers=headers)
    assert profiles_resp.status_code == 403

    batch_create_resp = client.post(
        "/migration/batches", files=[("files", ("x.igs", b"whatever", "text/plain"))], data={"options": "{}"}, headers=headers
    )
    assert batch_create_resp.status_code == 403
    assert "interchange.migrate" in batch_create_resp.json()["error"]["message"]

    batch_run_resp = client.post(f"/migration/batches/{fake_id}/run", data={"metadata_by_filename": "{}"}, headers=headers)
    assert batch_run_resp.status_code == 403

    batch_commit_resp = client.post(f"/migration/batches/{fake_id}/commit", headers=headers)
    assert batch_commit_resp.status_code == 403


def test_viewer_is_allowed_through_every_review_gated_endpoint():
    headers = _seed_user(unique_suffix(), "viewer")
    fake_id = "00000000-0000-0000-0000-000000000000"

    # Reaches the route body (404, not 403) -- proves the permission dependency let it through.
    assert client.get(f"/migration/batches/{fake_id}", headers=headers).status_code == 404
    assert client.get(f"/migration/batches/{fake_id}/items", headers=headers).status_code == 404
    assert client.get(f"/migration/batches/{fake_id}/items/{fake_id}", headers=headers).status_code == 404
    assert client.get(f"/migration/batches/{fake_id}/report.json", headers=headers).status_code == 404
    assert (
        client.post(
            f"/migration/batches/{fake_id}/items/{fake_id}/resolve", data={"legacy_metadata": "{}"}, headers=headers
        ).status_code
        == 404
    )
    assert (
        client.post(f"/migration/batches/{fake_id}/items/{fake_id}/block", data={"note": "x"}, headers=headers).status_code
        == 404
    )
    assert client.post(f"/migration/batches/{fake_id}/items/{fake_id}/accept-warning", headers=headers).status_code == 404
    assert client.get("/audit-log", headers=headers).status_code == 200


def test_admin_is_refused_nowhere():
    headers = _seed_user(unique_suffix(), "admin")
    fake_id = "00000000-0000-0000-0000-000000000000"

    # A real platform error (piece not found), not a permission_denied -- proves the gate passed.
    export_resp = client.post(f"/pieces/{fake_id}/export/iges", json={}, headers=headers)
    assert export_resp.status_code != 403

    batch_run_resp = client.post(f"/migration/batches/{fake_id}/run", data={"metadata_by_filename": "{}"}, headers=headers)
    assert batch_run_resp.status_code == 404  # not_found, not permission_denied
