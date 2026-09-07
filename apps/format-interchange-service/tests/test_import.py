"""Step 2 exit criteria (format_interchange_plan.md Sec 7): "an IGES file exported in Step 1
round-trips back in and reproduces the original piece within trim/closure tolerance; a file from a
real external system imports with correct warnings surfaced for any ambiguous geometry."""

import json

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_piece_with_geometry, unique_suffix
from test_export import RECTANGLE_GEOMETRY

from app.iges_writer import (
    IgesDocument,
    _directory_entries,
    _global_section,
    _parameter_data,
    _start_section,
    _terminate_section,
)
from app.main import app

client = TestClient(app)


def _seed_folder(unique: str) -> tuple[dict[str, str], dict]:
    org_code = f"FII-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}
    with platform_client(headers) as p:
        p.get("/me")
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
    return headers, folder


def _assemble_iges(doc: IgesDocument, unit: str = "mm") -> str:
    """Assembles a raw IGES file from a hand-built `IgesDocument` without going through
    `write_iges` (which always adds Entity Labels and wraps the outline in a Composite Curve) --
    used here to build a "genuinely external, unlabeled" file for the heuristic-chaining tests."""
    pd_lines, pd_counts = _parameter_data(doc.entities)
    de_lines = _directory_entries(doc.entities, pd_counts)
    s_lines = _start_section("TEST")
    g_lines = _global_section("test.igs", "TEST", unit)
    t_lines = _terminate_section(len(s_lines), len(g_lines), len(de_lines), len(pd_lines))
    return "\n".join(s_lines + g_lines + de_lines + pd_lines + t_lines) + "\n"


def _export_rectangle_as_iges(headers: dict, folder: dict, code_prefix: str) -> bytes:
    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"{code_prefix}-{unique_suffix()}", RECTANGLE_GEOMETRY)
    resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "succeeded"
    import httpx

    return httpx.get(body["download_url"]).content


def test_round_trip_reproduces_exported_rectangle():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder, "BODICE")

    resp = client.post(
        "/import/iges",
        files={"file": ("bodice.igs", iges_bytes, "text/plain")},
        data={"options": json.dumps({})},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "staged"
    assert body["error_detail"] is None

    perimeter = body["geometry"]["perimeter"]
    assert [(p["x"], p["y"]) for p in perimeter] == [(0.0, 0.0), (300.0, 0.0), (300.0, 400.0), (0.0, 400.0)]
    assert len(body["geometry"]["internal_lines"]) == 1
    assert len(body["geometry"]["notches"]) == 1
    assert body["geometry"]["grain_line"] is not None
    assert body["source_summary"]["declared_unit"] == "mm"
    assert body["warnings"] == []


def test_staged_import_can_be_committed_and_creates_a_real_piece():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder, "BODICE")

    resp = client.post(
        "/import/iges",
        files={"file": ("bodice.igs", iges_bytes, "text/plain")},
        data={"options": json.dumps({"target_collection": folder["id"]})},
        headers=headers,
    )
    body = resp.json()
    assert body["status"] == "staged"
    job_id = body["job_id"]

    commit_resp = client.post(f"/import/iges/jobs/{job_id}/commit", headers=headers)
    assert commit_resp.status_code == 200, commit_resp.text
    committed = commit_resp.json()
    assert committed["status"] == "committed"
    assert committed["target_piece_id"] is not None
    assert committed["geometry"] is None  # omitted once committed -- see schemas.py's docstring

    with platform_client(headers) as p:
        piece = p.get(f"/pieces/{committed['target_piece_id']}").json()
        assert piece["current_version_id"] is not None
        download = p.get(f"/pieces/{piece['id']}/versions/{piece['current_version_id']}/download-url").json()
        import httpx

        geometry = httpx.get(download["download_url"]).json()
        assert len(geometry["perimeter"]) == 4


def test_stage_only_false_commits_immediately():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder, "BODICE")

    resp = client.post(
        "/import/iges",
        files={"file": ("bodice.igs", iges_bytes, "text/plain")},
        data={"options": json.dumps({"target_collection": folder["id"], "stage_only": False})},
        headers=headers,
    )
    body = resp.json()
    assert body["status"] == "committed"
    assert body["target_piece_id"] is not None


def test_malformed_file_fails_cleanly():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)

    resp = client.post(
        "/import/iges",
        files={"file": ("garbage.igs", b"this is not an IGES file at all", "text/plain")},
        data={"options": json.dumps({})},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "failed"
    assert body["error_detail"] is not None


def test_unlabeled_external_style_file_infers_outline_via_heuristic_chaining():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)

    doc = IgesDocument()
    doc.add_line(0.0, 0.0, 100.0, 0.0)
    doc.add_line(100.0, 0.0, 100.0, 100.0)
    doc.add_line(100.0, 100.0, 0.0, 100.0)
    doc.add_line(0.0, 100.0, 0.0, 0.0)
    iges_text = _assemble_iges(doc)

    resp = client.post(
        "/import/iges",
        files={"file": ("external.igs", iges_text.encode("ascii"), "text/plain")},
        data={"options": json.dumps({})},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "staged"
    perimeter = body["geometry"]["perimeter"]
    assert len(perimeter) == 4
    assert {(p["x"], p["y"]) for p in perimeter} == {(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)}
    warning_codes = {w["code"] for w in body["warnings"]}
    assert "outline_inferred_from_unlabeled_geometry" in warning_codes


def test_gap_within_closure_amount_is_auto_closed_with_a_warning():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)

    doc = IgesDocument()
    doc.add_line(0.0, 0.0, 100.0, 0.0)
    doc.add_line(100.0, 0.0, 100.0, 100.0)
    doc.add_line(100.0, 100.0, 0.0, 100.0)
    doc.add_line(0.0, 100.0, 0.0, 0.5)  # 0.5mm short of closing exactly back onto the start point
    iges_text = _assemble_iges(doc)

    resp = client.post(
        "/import/iges",
        files={"file": ("gap.igs", iges_text.encode("ascii"), "text/plain")},
        data={"options": json.dumps({"closure_amount_mm": 2.0})},
        headers=headers,
    )
    body = resp.json()
    assert body["status"] == "staged"
    warning_codes = {w["code"] for w in body["warnings"]}
    assert "gap_auto_closed" in warning_codes


def test_gap_beyond_closure_amount_fails_cleanly():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)

    doc = IgesDocument()
    doc.add_line(0.0, 0.0, 100.0, 0.0)
    doc.add_line(100.0, 0.0, 100.0, 100.0)
    doc.add_line(100.0, 100.0, 50.0, 100.0)  # 50mm short -- well beyond any reasonable closure tolerance
    iges_text = _assemble_iges(doc)

    resp = client.post(
        "/import/iges",
        files={"file": ("gap.igs", iges_text.encode("ascii"), "text/plain")},
        data={"options": json.dumps({"closure_amount_mm": 2.0})},
        headers=headers,
    )
    body = resp.json()
    assert body["status"] == "failed"
    assert "outline_not_closed" in body["error_detail"]
