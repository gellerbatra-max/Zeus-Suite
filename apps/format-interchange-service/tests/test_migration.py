"""Step 3 exit criteria (format_interchange_plan.md Sec 7): "a real legacy-format sample batch
converts, and every error/warning code in the catalogue has been produced at least once against
real or constructed test fixtures." `self_intersection` and `multiple_grain_lines` are produced
from real geometry/parsed-source signals; every other Sec 2.3/2.4 code is produced via the
caller-supplied `legacy_metadata` extension point documented in app/migration_checks.py."""

import json

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_piece_with_geometry, unique_suffix
from test_export import RECTANGLE_GEOMETRY
from test_import import _assemble_iges

from app.iges_writer import IgesDocument
from app.main import app

client = TestClient(app)


def _seed_folder(unique: str) -> tuple[dict[str, str], dict]:
    org_code = f"FIM-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}
    with platform_client(headers) as p:
        p.get("/me")
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
    return headers, folder


def _export_rectangle_as_iges(headers: dict, folder: dict) -> bytes:
    with platform_client(headers) as p:
        piece = seed_piece_with_geometry(p, folder["id"], f"BODICE-{unique_suffix()}", RECTANGLE_GEOMETRY)
    resp = client.post(f"/pieces/{piece['id']}/export/iges", json={}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "succeeded"
    import httpx

    return httpx.get(body["download_url"]).content


def _create_batch(headers: dict, files: dict[str, bytes], **options) -> dict:
    resp = client.post(
        "/migration/batches",
        files=[("files", (name, content, "text/plain")) for name, content in files.items()],
        data={"options": json.dumps({"source_system": "test-legacy-system", **options})},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


def _run_batch(headers: dict, batch_id: str, metadata_by_filename: dict | None = None) -> dict:
    resp = client.post(
        f"/migration/batches/{batch_id}/run",
        data={"metadata_by_filename": json.dumps(metadata_by_filename or {})},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


def _bowtie_iges() -> str:
    """A self-intersecting outline (Type 110 lines wrapped in an OUTLINE Composite Curve) --
    hand-built rather than exported, since Step 1's own export validation gate rejects
    self-intersecting geometry before it could ever produce this file for real."""
    doc = IgesDocument()
    points = [(0.0, 0.0), (100.0, 100.0), (100.0, 0.0), (0.0, 100.0)]
    indices = [
        doc.add_line(points[i][0], points[i][1], points[(i + 1) % 4][0], points[(i + 1) % 4][1], label="OUTLINE")
        for i in range(4)
    ]
    doc.add_composite_curve(indices, label="OUTLINE")
    return _assemble_iges(doc)


def _two_grain_lines_iges() -> str:
    doc = IgesDocument()
    points = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    indices = [
        doc.add_line(points[i][0], points[i][1], points[(i + 1) % 4][0], points[(i + 1) % 4][1], label="OUTLINE")
        for i in range(4)
    ]
    doc.add_composite_curve(indices, label="OUTLINE")
    doc.add_line(10.0, 10.0, 10.0, 90.0, label="GRAIN")
    doc.add_line(20.0, 10.0, 20.0, 90.0, label="GRAIN")
    return _assemble_iges(doc)


def test_happy_path_batch_converts_cleanly():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder)

    batch = _create_batch(headers, {"clean.igs": iges_bytes})
    assert batch["status"] == "pending"
    assert batch["item_count"] == 1
    assert batch["chunk_count"] == 1

    result = _run_batch(headers, batch["id"])
    assert result["status"] == "completed"
    assert result["counts"] == {"converted": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    assert len(items) == 1
    assert items[0]["status"] == "converted"
    assert items[0]["needs_review"] is False
    assert items[0]["findings"] == []
    assert items[0]["converted_geometry"]["perimeter"]


def test_self_intersecting_source_produces_error_finding():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)
    batch = _create_batch(headers, {"bowtie.igs": _bowtie_iges().encode("ascii")})

    result = _run_batch(headers, batch["id"])
    assert result["counts"] == {"error": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    codes = {f["code"] for f in items[0]["findings"]}
    assert "self_intersection" in codes
    assert items[0]["status"] == "error"
    assert items[0]["needs_review"] is True


def test_multiple_grain_lines_promoted_to_error():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)
    batch = _create_batch(headers, {"two-grains.igs": _two_grain_lines_iges().encode("ascii")})

    result = _run_batch(headers, batch["id"])
    assert result["counts"] == {"error": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    finding = next(f for f in items[0]["findings"] if f["code"] == "multiple_grain_lines")
    assert finding["severity"] == "error"


def test_metadata_driven_catalogue_codes_all_produced():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder)
    filename = "trading-partner-style.igs"

    legacy_metadata = {
        "description": "A description far longer than twenty characters",
        "corner_treatments": [{"point_ref": "p2", "treatment": "notch-corner", "valid_angle_min_deg": 0, "valid_angle_max_deg": 45}],
        "match_lines": [{"point_refs": ["p1", "p3"]}],
        "grade_rule_table_ref": "MISSING-TABLE",
        "known_rule_tables": ["OTHER-TABLE"],
        "rule_references": [{"point_ref": "p1", "rule_number": 99}],
        "valid_rule_numbers": [1, 2, 3],
        "unavailable_rule_references": [{"point_ref": "p4", "rule_number": 7}],
        "tangent_rule_points": ["p3"],
        "size_synonyms": {"XL": None},
        "grade_points": [{"point_ref": "p1", "requires_axis": True}],
        "flip_applied": True,
        "old_grain_angle_deg": 90.0,
        "new_grain_angle_deg": 270.0,
        "rotation_type": "F",
        "cut_line_present": False,
    }

    batch = _create_batch(headers, {filename: iges_bytes})
    result = _run_batch(headers, batch["id"], metadata_by_filename={filename: legacy_metadata})
    assert result["counts"] == {"error": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    item = items[0]
    assert item["status"] == "error"
    assert item["needs_review"] is True

    codes = {f["code"] for f in item["findings"]}
    expected_error_codes = {
        "invalid_corner_angle",
        "invalid_match_line",
        "rule_table_missing",
        "unresolvable_size_synonym",
        "missing_grade_axis",
        "invalid_rule_reference",
    }
    expected_warning_codes = {
        "flip_grain_realigned",
        "rotation_behavior_change",
        "description_truncated",
        "cut_line_absent_used_sew_perimeter",
        "rule_unresolved_zero_growth",
        "invalid_tangent_rule_zero_growth",
    }
    assert expected_error_codes <= codes
    assert expected_warning_codes <= codes

    by_code = {f["code"]: f for f in item["findings"]}
    assert by_code["invalid_corner_angle"]["severity"] == "error"
    assert by_code["flip_grain_realigned"]["severity"] == "warning"


def test_source_grading_corrupt_blocks_item():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder)
    filename = "corrupt-grading.igs"

    batch = _create_batch(headers, {filename: iges_bytes})
    result = _run_batch(headers, batch["id"], metadata_by_filename={filename: {"grading_source_corrupt": True}})
    assert result["counts"] == {"blocked": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    assert items[0]["status"] == "blocked"
    assert any(f["code"] == "source_grading_corrupt" for f in items[0]["findings"])


def test_unsupported_source_format_rejected_at_batch_creation():
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)
    resp = client.post(
        "/migration/batches",
        files=[("files", ("style.dxf", b"not really dxf", "text/plain"))],
        data={"options": json.dumps({"source_system": "legacy", "source_format": "dxf"})},
        headers=headers,
    )
    assert resp.status_code == 400
    assert "Unsupported source_format" in resp.json()["error"]["message"]


def test_run_is_idempotent_only_reprocesses_pending_items():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder)
    batch = _create_batch(headers, {"clean.igs": iges_bytes})

    first = _run_batch(headers, batch["id"])
    assert first["counts"] == {"converted": 1}
    second = _run_batch(headers, batch["id"])
    assert second["counts"] == {"converted": 1}  # unchanged -- item was no longer "pending"

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    assert len(items[0]["findings"]) == 0  # no duplicate findings from the second run


def test_report_csv_and_json_list_every_finding():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder)
    filename = "needs-review.igs"

    batch = _create_batch(headers, {filename: iges_bytes})
    _run_batch(headers, batch["id"], metadata_by_filename={filename: {"cut_line_present": False}})

    json_resp = client.get(f"/migration/batches/{batch['id']}/report.json", headers=headers)
    assert json_resp.status_code == 200
    rows = json_resp.json()
    assert len(rows) == 1
    assert rows[0]["code"] == "cut_line_absent_used_sew_perimeter"
    assert rows[0]["source_style_ref"] == filename
    assert rows[0]["deep_link"].startswith(f"/migration/batches/{batch['id']}/items/")

    csv_resp = client.get(f"/migration/batches/{batch['id']}/report.csv", headers=headers)
    assert csv_resp.status_code == 200
    assert csv_resp.headers["content-type"].startswith("text/csv")
    lines = csv_resp.text.strip().splitlines()
    assert lines[0] == "item_id,source_style_ref,code,severity,message,deep_link"
    assert len(lines) == 2


def test_items_endpoint_filters_by_status():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    clean_bytes = _export_rectangle_as_iges(headers, folder)
    batch = _create_batch(headers, {"clean.igs": clean_bytes, "bowtie.igs": _bowtie_iges().encode("ascii")})
    _run_batch(headers, batch["id"])

    error_items = client.get(f"/migration/batches/{batch['id']}/items", params={"status": "error"}, headers=headers).json()
    assert len(error_items) == 1
    assert error_items[0]["source_style_ref"] == "bowtie.igs"

    converted_items = client.get(
        f"/migration/batches/{batch['id']}/items", params={"status": "converted"}, headers=headers
    ).json()
    assert len(converted_items) == 1
    assert converted_items[0]["source_style_ref"] == "clean.igs"
