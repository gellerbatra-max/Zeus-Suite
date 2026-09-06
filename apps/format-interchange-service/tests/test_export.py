"""Step 1 exit criteria (format_interchange_plan.md Sec 7): a real piece round-trips out of this
suite as a well-formed IGES file."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_piece_with_geometry, unique_suffix

from app.main import app

client = TestClient(app)

RECTANGLE_GEOMETRY = {
    "schema_version": 1,
    "units": "mm",
    "perimeter": [
        {"point_ref": "p1", "x": 0.0, "y": 0.0, "type": "corner"},
        {"point_ref": "p2", "x": 300.0, "y": 0.0, "type": "corner"},
        {"point_ref": "p3", "x": 300.0, "y": 400.0, "type": "corner"},
        {"point_ref": "p4", "x": 0.0, "y": 400.0, "type": "corner"},
    ],
    "internal_lines": [{"line_ref": "l1", "point_refs": ["p1", "p3"], "line_type": "internal"}],
    "seams": [],
    "darts": [],
    "notches": [{"point_ref": "p2", "notch_type": "V", "depth_mm": 5.0}],
    "grain_line": {
        "start": {"point_ref": "g1", "x": 10.0, "y": 10.0},
        "end": {"point_ref": "g2", "x": 10.0, "y": 390.0},
        "angle_deg": 90.0,
    },
    "grade_rule_table": None,
    "annotations": [],
    "measurements": [],
}

BOWTIE_GEOMETRY = {
    "schema_version": 1,
    "units": "mm",
    "perimeter": [
        {"point_ref": "p1", "x": 0.0, "y": 0.0, "type": "corner"},
        {"point_ref": "p2", "x": 100.0, "y": 100.0, "type": "corner"},
        {"point_ref": "p3", "x": 100.0, "y": 0.0, "type": "corner"},
        {"point_ref": "p4", "x": 0.0, "y": 100.0, "type": "corner"},
    ],
    "internal_lines": [],
    "seams": [],
    "darts": [],
    "notches": [],
    "grain_line": None,
    "grade_rule_table": None,
    "annotations": [],
    "measurements": [],
}


def _seed_folder(unique: str) -> tuple[dict[str, str], dict]:
    org_code = f"FI-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()

    return headers, folder


def test_export_succeeds_for_valid_piece_and_round_trips_real_geometry():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique}", RECTANGLE_GEOMETRY)

    resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "succeeded"
    assert body["download_url"] is not None
    assert body["error_detail"] is None

    import httpx

    iges_text = httpx.get(body["download_url"]).text
    lines = iges_text.rstrip("\n").split("\n")
    # Every IGES card is exactly 80 columns -- the format's own structural invariant.
    assert all(len(line) == 80 for line in lines)
    assert lines[0].endswith("S      1")
    assert lines[-1].endswith("T      1")
    # The real geometry's outline coordinates appear verbatim in the Parameter Data section.
    assert "110,0.0,0.0,0.0,300.0,0.0,0.0;" in iges_text
    assert "110,300.0,400.0,0.0,0.0,400.0,0.0;" in iges_text
    # Composite curve referencing the 4 outline Type-110 lines by DE pointer.
    assert "102,4,1,3,5,7;" in iges_text


def test_export_can_exclude_optional_geometry():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique}", RECTANGLE_GEOMETRY)

    resp = client.post(
        f"/pieces/{piece['id']}/export/iges",
        json={"include_internal_lines": False, "include_notches": False, "include_grain_line": False},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "succeeded"

    import httpx

    iges_text = httpx.get(body["download_url"]).text
    # Only the outline (4 lines + composite curve) should remain -- no Type 116 (notch point),
    # and only one internal-looking line (the outline itself, not the excluded internal diagonal).
    assert "116," not in iges_text
    assert "110,10.0,10.0,0.0,10.0,390.0,0.0;" not in iges_text  # grain line
    assert "110,0.0,0.0,0.0,300.0,400.0,0.0;" not in iges_text  # excluded internal diagonal


def test_export_fails_cleanly_for_piece_without_committed_version():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    with platform_client(headers) as p:
        piece = p.post(
            "/pieces", json={"folder_id": folder["id"], "piece_code": f"EMPTY-{unique}", "piece_name": "Empty"}
        ).json()

    resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "failed"
    assert body["download_url"] is None
    assert "no committed geometry" in body["error_detail"]


def test_export_fails_cleanly_for_self_intersecting_outline():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BOWTIE-{unique}", BOWTIE_GEOMETRY)

    resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "failed"
    assert body["download_url"] is None
    assert "self_intersection" in body["error_detail"]


def test_get_export_job_returns_persisted_status():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)

    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique}", RECTANGLE_GEOMETRY)

    submit_resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    job_id = submit_resp.json()["job_id"]

    poll_resp = client.get(f"/export/iges/jobs/{job_id}", headers=headers)
    assert poll_resp.status_code == 200, poll_resp.text
    assert poll_resp.json()["status"] == "succeeded"
    assert poll_resp.json()["download_url"] is not None
