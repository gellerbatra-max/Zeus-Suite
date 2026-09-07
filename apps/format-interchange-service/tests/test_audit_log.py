"""Step 5 exit criteria (format_interchange_plan.md Sec 7): "verify audit-log completeness for
every export/import/migration action." One audit_log row per completed mutating action (not
reads) -- app/audit.py."""

import json

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_piece_with_geometry, unique_suffix
from test_export import RECTANGLE_GEOMETRY
from test_migration import _create_batch, _run_batch

from app.main import app

client = TestClient(app)


def _seed_folder(unique: str) -> tuple[dict[str, str], dict]:
    org_code = f"AUD-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}
    with platform_client(headers) as p:
        p.get("/me")
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
    return headers, folder


def _actions(headers: dict) -> list[str]:
    return [row["action"] for row in client.get("/audit-log", headers=headers).json()]


def test_export_action_is_audited():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique}", RECTANGLE_GEOMETRY)

    resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    assert resp.status_code == 200, resp.text

    actions = _actions(headers)
    assert "export.iges" in actions
    entry = next(row for row in client.get("/audit-log", headers=headers).json() if row["action"] == "export.iges")
    assert entry["entity_type"] == "interchange_job"
    assert entry["entity_id"] == resp.json()["job_id"]
    assert entry["detail"]["status"] == "succeeded"


def test_import_and_commit_actions_are_audited():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique}", RECTANGLE_GEOMETRY)
    export_resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    import httpx

    iges_bytes = httpx.get(export_resp.json()["download_url"]).content

    import_resp = client.post(
        "/import/iges",
        files={"file": ("bodice.igs", iges_bytes, "text/plain")},
        data={"options": json.dumps({"target_collection": folder["id"]})},
        headers=headers,
    )
    job_id = import_resp.json()["job_id"]
    commit_resp = client.post(f"/import/iges/jobs/{job_id}/commit", headers=headers)
    assert commit_resp.status_code == 200, commit_resp.text

    actions = _actions(headers)
    assert "import.iges" in actions
    assert "import.commit" in actions


def test_migration_batch_lifecycle_actions_are_all_audited():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique}", RECTANGLE_GEOMETRY)
    export_resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    import httpx

    iges_bytes = httpx.get(export_resp.json()["download_url"]).content

    batch = _create_batch(headers, {"clean.igs": iges_bytes}, target_collection=folder["id"])
    _run_batch(headers, batch["id"])

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    item_id = items[0]["id"]

    accept_resp_status = client.post(
        f"/migration/batches/{batch['id']}/items/{item_id}/accept-warning", headers=headers
    ).status_code
    # This item is clean ("converted"), so accept-warning correctly refuses (400) -- block it
    # instead purely to exercise that action's own audit entry.
    assert accept_resp_status == 400
    client.post(f"/migration/batches/{batch['id']}/items/{item_id}/block", data={"note": "test"}, headers=headers)
    client.post(f"/migration/batches/{batch['id']}/commit", headers=headers)

    actions = _actions(headers)
    assert "migration.batch_create" in actions
    assert "migration.batch_run" in actions
    assert "migration.item_block" in actions
    assert "migration.batch_commit" in actions


def test_audit_log_is_scoped_to_the_caller_own_organization():
    headers_a, folder_a = _seed_folder(unique_suffix())
    headers_b, _folder_b = _seed_folder(unique_suffix())
    with platform_client(headers_a) as p:
        piece = seed_piece_with_geometry(p, folder_a["id"], f"BODICE-{unique_suffix()}", RECTANGLE_GEOMETRY)
    client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers_a)

    assert "export.iges" in _actions(headers_a)
    assert "export.iges" not in _actions(headers_b)
