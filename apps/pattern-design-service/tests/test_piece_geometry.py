"""Phase 2.1 exit criteria (pattern_design_plan.md Sec 7): a piece with just a drawn perimeter
round-trips through Blob Storage and Postgres correctly, including workflow status."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_folder(unique: str) -> tuple[dict[str, str], dict]:
    org_code = f"PD-{unique}"
    username = f"designer-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()

    return headers, folder


def test_new_piece_has_empty_geometry():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    piece = client.post(
        "/pieces",
        json={"folder_id": folder["id"], "piece_code": f"BODICE-{unique}", "piece_name": "Bodice Front"},
        headers=headers,
    ).json()

    resp = client.get(f"/pieces/{piece['id']}/geometry", headers=headers)
    assert resp.status_code == 200, resp.text
    geometry = resp.json()
    assert geometry["schema_version"] == 1
    assert geometry["units"] == "mm"
    assert geometry["perimeter"] == []


def test_perimeter_round_trips_through_blob_storage_and_postgres():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    piece = client.post(
        "/pieces",
        json={"folder_id": folder["id"], "piece_code": f"SLEEVE-{unique}", "piece_name": "Sleeve"},
        headers=headers,
    ).json()
    assert piece["current_version_id"] is None
    assert piece["workflow_status"]["code"] == "unmade"

    geometry = {
        "schema_version": 1,
        "units": "mm",
        "perimeter": [
            {"point_ref": "p1", "x": 0.0, "y": 0.0, "type": "corner"},
            {"point_ref": "p2", "x": 300.0, "y": 0.0, "type": "corner"},
            {"point_ref": "p3", "x": 300.0, "y": 450.0, "type": "corner"},
            {"point_ref": "p4", "x": 0.0, "y": 450.0, "type": "corner"},
        ],
    }
    resp = client.put(f"/pieces/{piece['id']}/geometry", json=geometry, headers=headers)
    assert resp.status_code == 200, resp.text
    saved_piece = resp.json()
    assert saved_piece["current_version_id"] is not None
    # Saving geometry commits a new Blob Storage version but does not itself transition
    # workflow status -- that stays an explicit operator action (POST /pieces/{id}/status).
    assert saved_piece["workflow_status"]["code"] == "unmade"

    # Reload independently -- confirms this actually persisted through Blob Storage + Postgres,
    # not just an in-memory echo of the request.
    resp = client.get(f"/pieces/{piece['id']}/geometry", headers=headers)
    assert resp.status_code == 200, resp.text
    reloaded = resp.json()
    assert reloaded["perimeter"] == geometry["perimeter"]

    resp = client.get(f"/pieces/{piece['id']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["current_version_id"] == saved_piece["current_version_id"]


def test_internal_line_round_trips_with_perimeter():
    """Phase 2.2: an internal line (Gerber's "Create Line - 2 Point") connecting two existing
    perimeter points saves and reloads alongside the perimeter."""
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    piece = client.post(
        "/pieces",
        json={"folder_id": folder["id"], "piece_code": f"YOKE-{unique}", "piece_name": "Yoke"},
        headers=headers,
    ).json()

    geometry = {
        "schema_version": 1,
        "units": "mm",
        "perimeter": [
            {"point_ref": "p1", "x": 0.0, "y": 0.0, "type": "corner"},
            {"point_ref": "p2", "x": 200.0, "y": 0.0, "type": "corner"},
            {"point_ref": "p3", "x": 200.0, "y": 200.0, "type": "corner"},
            {"point_ref": "p4", "x": 0.0, "y": 200.0, "type": "corner"},
        ],
        "internal_lines": [
            {"line_ref": "l1", "point_refs": ["p1", "p3"], "line_type": "internal"},
        ],
    }
    resp = client.put(f"/pieces/{piece['id']}/geometry", json=geometry, headers=headers)
    assert resp.status_code == 200, resp.text

    resp = client.get(f"/pieces/{piece['id']}/geometry", headers=headers)
    assert resp.status_code == 200, resp.text
    reloaded = resp.json()
    assert reloaded["internal_lines"] == geometry["internal_lines"]


def test_status_transition_round_trips():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    piece = client.post(
        "/pieces",
        json={"folder_id": folder["id"], "piece_code": f"COLLAR-{unique}", "piece_name": "Collar"},
        headers=headers,
    ).json()

    resp = client.post(f"/pieces/{piece['id']}/status", json={"to_status": "needs_approval"}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["workflow_status"]["code"] == "needs_approval"
