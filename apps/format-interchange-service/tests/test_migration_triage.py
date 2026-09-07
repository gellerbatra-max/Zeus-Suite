"""Step 4 exit criteria (format_interchange_plan.md Sec 7): "a batch containing every error type
in the catalogue can be fully triaged end to end -- each error either resolved in-tool and
re-converted, or correctly marked blocked -- and a clean batch commits to the platform and becomes
visible in Pattern Design.\""""

import json

from fastapi.testclient import TestClient
from helpers import platform_client, unique_suffix
from test_migration import (
    _bowtie_iges,
    _create_batch,
    _export_rectangle_as_iges,
    _run_batch,
    _seed_folder,
)

from app.main import app

client = TestClient(app)


def test_resolve_fixes_a_metadata_driven_error_and_marks_item_resolved():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    iges_bytes = _export_rectangle_as_iges(headers, folder)
    filename = "needs-fix.igs"

    batch = _create_batch(headers, {filename: iges_bytes})
    run_result = _run_batch(
        headers, batch["id"], metadata_by_filename={filename: {"grade_rule_table_ref": "MISSING", "known_rule_tables": []}}
    )
    assert run_result["counts"] == {"error": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    item_id = items[0]["id"]
    assert items[0]["status"] == "error"

    resolve_resp = client.post(
        f"/migration/batches/{batch['id']}/items/{item_id}/resolve",
        data={"legacy_metadata": json.dumps({"known_rule_tables": ["MISSING"]})},
        headers=headers,
    )
    assert resolve_resp.status_code == 200, resolve_resp.text
    resolved = resolve_resp.json()
    assert resolved["status"] == "resolved"
    assert resolved["needs_review"] is False
    assert resolved["findings"] == []


def test_resolve_with_replacement_file_fixes_self_intersection():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    batch = _create_batch(headers, {"bowtie.igs": _bowtie_iges().encode("ascii")})
    run_result = _run_batch(headers, batch["id"])
    assert run_result["counts"] == {"error": 1}

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    item_id = items[0]["id"]

    good_bytes = _export_rectangle_as_iges(headers, folder)
    resolve_resp = client.post(
        f"/migration/batches/{batch['id']}/items/{item_id}/resolve",
        files={"file": ("fixed.igs", good_bytes, "text/plain")},
        data={"legacy_metadata": "{}"},
        headers=headers,
    )
    assert resolve_resp.status_code == 200, resolve_resp.text
    resolved = resolve_resp.json()
    assert resolved["status"] == "resolved"
    assert not any(f["code"] == "self_intersection" for f in resolved["findings"])


def test_block_marks_item_with_a_correction_note():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    filename = "corrupt.igs"
    batch = _create_batch(headers, {filename: _export_rectangle_as_iges(headers, folder)})
    _run_batch(headers, batch["id"], metadata_by_filename={filename: {"grading_source_corrupt": True}})

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    assert items[0]["status"] == "blocked"
    item_id = items[0]["id"]

    resp = client.post(
        f"/migration/batches/{batch['id']}/items/{item_id}/block",
        data={"note": "Waiting on a corrected grade rule table from the trading partner."},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "blocked"
    assert "corrected grade rule table" in body["block_note"]


def test_accept_warning_stamps_findings_and_rejects_wrong_status():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    filename = "has-warning.igs"
    batch = _create_batch(headers, {filename: _export_rectangle_as_iges(headers, folder)})
    _run_batch(headers, batch["id"], metadata_by_filename={filename: {"cut_line_present": False}})

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    assert items[0]["status"] == "converted_with_warning"
    item_id = items[0]["id"]

    resp = client.post(f"/migration/batches/{batch['id']}/items/{item_id}/accept-warning", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["warning_accepted"] is True
    assert body["findings"]
    assert all(f["resolved"] for f in body["findings"] if f["severity"] == "warning")

    # A second accept-warning call on an already-accepted item's ORIGINAL status ("converted")
    # after a fresh warning-free item should be rejected.
    clean_filename = "clean.igs"
    clean_batch = _create_batch(headers, {clean_filename: _export_rectangle_as_iges(headers, folder)})
    _run_batch(headers, clean_batch["id"])
    clean_items = client.get(f"/migration/batches/{clean_batch['id']}/items", headers=headers).json()
    reject_resp = client.post(
        f"/migration/batches/{clean_batch['id']}/items/{clean_items[0]['id']}/accept-warning", headers=headers
    )
    assert reject_resp.status_code == 400


def test_commit_refuses_until_every_error_is_resolved_or_blocked():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    batch = _create_batch(headers, {"bowtie.igs": _bowtie_iges().encode("ascii")}, target_collection=folder["id"])
    _run_batch(headers, batch["id"])

    commit_resp = client.post(f"/migration/batches/{batch['id']}/commit", headers=headers)
    assert commit_resp.status_code == 400
    assert "not yet resolved" in commit_resp.json()["error"]["message"]

    batch_status = client.get(f"/migration/batches/{batch['id']}", headers=headers).json()
    assert batch_status["commit_blocked_by"] == ["bowtie.igs"]


def test_commit_refuses_until_warnings_are_accepted():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    filename = "has-warning.igs"
    batch = _create_batch(headers, {filename: _export_rectangle_as_iges(headers, folder)}, target_collection=folder["id"])
    _run_batch(headers, batch["id"], metadata_by_filename={filename: {"cut_line_present": False}})

    commit_resp = client.post(f"/migration/batches/{batch['id']}/commit", headers=headers)
    assert commit_resp.status_code == 400


def test_commit_creates_real_pieces_and_skips_blocked_items():
    unique = unique_suffix()
    headers, folder = _seed_folder(unique)
    clean_bytes = _export_rectangle_as_iges(headers, folder)
    corrupt_filename = "corrupt.igs"

    batch = _create_batch(
        headers,
        {"clean.igs": clean_bytes, corrupt_filename: _export_rectangle_as_iges(headers, folder)},
        target_collection=folder["id"],
    )
    _run_batch(headers, batch["id"], metadata_by_filename={corrupt_filename: {"grading_source_corrupt": True}})

    commit_resp = client.post(f"/migration/batches/{batch['id']}/commit", headers=headers)
    assert commit_resp.status_code == 200, commit_resp.text
    committed = commit_resp.json()
    assert committed["status"] == "committed"

    items = client.get(f"/migration/batches/{batch['id']}/items", headers=headers).json()
    by_ref = {i["source_style_ref"]: i for i in items}
    assert by_ref["clean.igs"]["target_piece_id"] is not None
    assert by_ref[corrupt_filename]["status"] == "blocked"
    assert by_ref[corrupt_filename]["target_piece_id"] is None

    with platform_client(headers) as p:
        piece = p.get(f"/pieces/{by_ref['clean.igs']['target_piece_id']}").json()
        assert piece["current_version_id"] is not None
        download = p.get(f"/pieces/{piece['id']}/versions/{piece['current_version_id']}/download-url").json()
        import httpx

        geometry = httpx.get(download["download_url"]).json()
        assert len(geometry["perimeter"]) == 4
