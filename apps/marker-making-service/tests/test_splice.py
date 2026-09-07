"""Marker Making Sec 1.8 (splice marks / fabric-roll handling): manual mark CRUD (thin proxy) and
the real auto-placement algorithm, proxying through the real data-platform-api subprocess (see
conftest.py)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_org_marker(unique: str):
    org_code = f"SPLICE-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
        marker = p.post(
            "/markers", json={"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Splice Marker"},
        ).json()

    return headers, folder, marker


def _place_two_pieces(headers, folder, marker, unique):
    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"SPL-A-{unique}", "Splice Piece A")
        piece_b = seed_nestable_piece(p, folder["id"], f"SPL-B-{unique}", "Splice Piece B")

    client.put(
        f"/markers/{marker['id']}/workspace",
        json={
            "placements": [
                {"piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 10, "y": 20, "width": 50, "height": 40}},
                {"piece_id": piece_b["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 80, "y": 5, "width": 30, "height": 60}},
            ]
        },
        headers=headers,
    )


def _set_settings(headers, marker):
    client.patch(
        f"/markers/{marker['id']}/splice/settings",
        json={"min_length": 1.0, "max_length": 5.0, "margin": 0.5, "separation": 2.0},
        headers=headers,
    )


def test_splice_settings_round_trip():
    unique = unique_suffix()
    headers, _folder, marker = _seed_org_marker(unique)

    resp = client.get(f"/markers/{marker['id']}/splice/settings", headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"min_length": None, "max_length": None, "margin": None, "separation": None}

    resp = client.patch(
        f"/markers/{marker['id']}/splice/settings",
        json={"min_length": 1.0, "max_length": 5.0, "margin": 0.5, "separation": 2.0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"min_length": 1.0, "max_length": 5.0, "margin": 0.5, "separation": 2.0}


def test_manual_splice_mark_crud():
    unique = unique_suffix()
    headers, _folder, marker = _seed_org_marker(unique)

    resp = client.post(
        f"/markers/{marker['id']}/splice-marks", json={"start_x": 5.0, "end_x": 6.0, "roll_id": "roll-1"},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    mark = resp.json()
    assert mark["source"] == "manual"
    assert mark["roll_id"] == "roll-1"

    resp = client.patch(f"/splice-marks/{mark['id']}", json={"end_x": 6.5}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["end_x"] == 6.5
    assert resp.json()["version"] == 2

    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=headers)
    assert len(resp.json()) == 1

    resp = client.delete(f"/splice-marks/{mark['id']}", headers=headers)
    assert resp.status_code == 204, resp.text
    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=headers)
    assert resp.json() == []


def test_auto_splice_requires_settings_and_placements():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    resp = client.post(f"/markers/{marker['id']}/splice/auto", json={"roll_length": 40}, headers=headers)
    assert resp.status_code == 400  # settings not configured

    _set_settings(headers, marker)
    resp = client.post(
        f"/markers/{marker['id']}/splice/auto", json={"roll_length": 0}, headers=headers,
    )
    assert resp.status_code == 400  # roll_length must be > 0

    unique2 = unique_suffix()
    headers2, _folder2, marker2 = _seed_org_marker(unique2)
    _set_settings(headers2, marker2)
    resp = client.post(f"/markers/{marker2['id']}/splice/auto", json={"roll_length": 40}, headers=headers2)
    assert resp.status_code == 400  # no placements


def test_auto_splice_places_marks_at_roll_length_intervals():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)
    _set_settings(headers, marker)

    # marker_length = max(10+50, 80+30) = 110. roll_length=40 -> boundaries at 40, 80 (120 excluded).
    # mark_length = clamp(margin*2=1.0, min=1.0, max=5.0) = 1.0.
    resp = client.post(f"/markers/{marker['id']}/splice/auto", json={"roll_length": 40}, headers=headers)
    assert resp.status_code == 200, resp.text
    marks = resp.json()
    assert len(marks) == 2
    marks_by_roll = {m["roll_id"]: m for m in marks}
    assert marks_by_roll["roll-2"]["start_x"] == 39.5
    assert marks_by_roll["roll-2"]["end_x"] == 40.5
    assert marks_by_roll["roll-2"]["source"] == "auto"
    assert marks_by_roll["roll-3"]["start_x"] == 79.5
    assert marks_by_roll["roll-3"]["end_x"] == 80.5


def test_auto_splice_skips_boundary_within_separation_of_edge():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)
    _set_settings(headers, marker)

    # marker_length=110, separation=2.0 -> valid boundary range is [2, 108].
    # roll_length=109 -> only boundary is 109, which exceeds 108, so it's skipped entirely.
    resp = client.post(f"/markers/{marker['id']}/splice/auto", json={"roll_length": 109}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json() == []


def test_auto_splice_regenerate_preserves_manual_marks():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)
    _set_settings(headers, marker)

    manual = client.post(
        f"/markers/{marker['id']}/splice-marks", json={"start_x": 1.0, "end_x": 1.5, "roll_id": "hand-added"},
        headers=headers,
    ).json()

    resp = client.post(f"/markers/{marker['id']}/splice/auto", json={"roll_length": 40}, headers=headers)
    marks = resp.json()
    assert len(marks) == 3  # 1 manual + 2 auto
    assert any(m["id"] == manual["id"] for m in marks)

    # Regenerating again must not duplicate the auto marks, and must still keep the manual one.
    resp = client.post(f"/markers/{marker['id']}/splice/auto", json={"roll_length": 40}, headers=headers)
    marks = resp.json()
    assert len(marks) == 3
    assert any(m["id"] == manual["id"] for m in marks)
    auto_marks = [m for m in marks if m["source"] == "auto"]
    assert len(auto_marks) == 2
