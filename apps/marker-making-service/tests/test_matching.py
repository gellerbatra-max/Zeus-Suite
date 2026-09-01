"""Marker Making Phase 2 Slice 2 (Sec 1.4): matching rule table CRUD/sub-resource lifecycle,
method application to a marker, in-canvas guidance math, and bite-boundary validation -- all
proxying through the real data-platform-api subprocess (see conftest.py)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_org_and_marker(unique: str):
    org_code = f"MATCH-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
        marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Matching Marker"},
        ).json()

    return headers, folder, marker


def test_stripe_definition_and_mark_lifecycle_with_sequence_bookkeeping():
    unique = unique_suffix()
    headers, _folder, _marker = _seed_org_and_marker(unique)

    resp = client.post(
        "/matching-rule-tables", json={"name": f"Table-{unique}", "method": "standard"}, headers=headers
    )
    assert resp.status_code == 200, resp.text
    table = resp.json()
    table_id = table["id"]

    resp = client.post(
        f"/matching-rule-tables/{table_id}/stripe-definitions",
        json={"name": "Def A", "origin_x": 0.0, "origin_y": 0.0, "h_distance": 10.0, "v_distance": 8.0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    resp = client.post(
        f"/matching-rule-tables/{table_id}/stripe-definitions",
        json={"name": "Def B", "h_distance": 5.0},
        headers=headers,
    )
    table = resp.json()
    assert len(table["stripe_definitions"]) == 2
    def_a_id = table["stripe_definitions"][0]["id"]
    def_b_id = table["stripe_definitions"][1]["id"]

    for name in ("Mark 1", "Mark 2", "Mark 3"):
        resp = client.post(
            f"/matching-rule-tables/{table_id}/stripe-marks",
            json={"name": name, "stripe_definition_id": def_a_id, "position": {"x": 0, "y": 0}},
            headers=headers,
        )
    table = resp.json()
    marks = table["stripe_marks"]
    assert [m["sequence"] for m in marks] == [1, 2, 3]
    mark_ids = [m["id"] for m in marks]

    resp = client.post(
        f"/matching-rule-tables/{table_id}/stripe-marks/{mark_ids[0]}/step",
        json={"direction": "next"}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["id"] == mark_ids[1]

    resp = client.post(
        f"/matching-rule-tables/{table_id}/stripe-marks/{mark_ids[0]}/step",
        json={"direction": "prev"}, headers=headers,
    )
    assert resp.status_code == 404

    resp = client.patch(
        f"/matching-rule-tables/{table_id}/stripe-marks/{mark_ids[1]}",
        json={"name": "Renamed Mark 2", "stripe_definition_id": def_b_id},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    renamed = next(m for m in resp.json()["stripe_marks"] if m["id"] == mark_ids[1])
    assert renamed["name"] == "Renamed Mark 2"
    assert renamed["stripe_definition_id"] == def_b_id

    resp = client.delete(f"/matching-rule-tables/{table_id}/stripe-marks/{mark_ids[2]}", headers=headers)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["stripe_marks"]) == 2

    # Deleting a stripe definition orphans (nulls, not deletes) any mark still pointing at it.
    resp = client.delete(f"/matching-rule-tables/{table_id}/stripe-definitions/{def_a_id}", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert len(body["stripe_definitions"]) == 1
    surviving_mark = next(m for m in body["stripe_marks"] if m["id"] == mark_ids[0])
    assert surviving_mark["stripe_definition_id"] is None


def test_offsets_replace_enforces_max_three_per_axis():
    unique = unique_suffix()
    headers, _folder, _marker = _seed_org_and_marker(unique)
    resp = client.post(
        "/matching-rule-tables", json={"name": f"OffsetsTable-{unique}", "method": "standard"}, headers=headers
    )
    table_id = resp.json()["id"]

    resp = client.put(
        f"/matching-rule-tables/{table_id}/offsets",
        json={"horizontal": [0.0, 1.0, 2.0, 3.0], "vertical": []},
        headers=headers,
    )
    assert resp.status_code == 400

    resp = client.put(
        f"/matching-rule-tables/{table_id}/offsets",
        json={"horizontal": [0.0, 5.0], "vertical": [0.0]},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["offsets"] == {"horizontal": [0.0, 5.0], "vertical": [0.0]}


def test_apply_matching_reflected_in_workspace():
    unique = unique_suffix()
    headers, _folder, marker = _seed_org_and_marker(unique)
    resp = client.post(
        "/matching-rule-tables", json={"name": f"ApplyTable-{unique}", "method": "five_star"}, headers=headers
    )
    table_id = resp.json()["id"]

    resp = client.post(
        f"/markers/{marker['id']}/matching/apply",
        json={"matching_rule_table_id": table_id, "matching_method": "five_star"},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["matching_rule_table_id"] == table_id
    assert resp.json()["matching_method"] == "five_star"

    resp = client.get(f"/markers/{marker['id']}/workspace", headers=headers)
    assert resp.status_code == 200, resp.text
    workspace = resp.json()
    assert workspace["matching_method"] == "five_star"
    assert workspace["matching_rule_table_id"] == table_id


def test_guidance_no_matching_rule_table_is_graceful():
    unique = unique_suffix()
    headers, _folder, marker = _seed_org_and_marker(unique)

    resp = client.post(
        f"/markers/{marker['id']}/matching/guidance",
        json={"piece_id": "does-not-matter", "stripe_mark_id": None, "x": 10, "y": 10},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["found"] is False
    assert body["targets"] == []
    assert body["message"]


def test_guidance_computes_nearest_grid_target_and_snaps_within_tolerance():
    unique = unique_suffix()
    headers, _folder, marker = _seed_org_and_marker(unique)

    table = client.post(
        "/matching-rule-tables", json={"name": f"GuidanceTable-{unique}", "method": "standard"}, headers=headers
    ).json()
    table = client.post(
        f"/matching-rule-tables/{table['id']}/stripe-definitions",
        json={"name": "Guide Def", "origin_x": 0.0, "origin_y": 0.0, "h_distance": 10.0, "v_distance": 0.0},
        headers=headers,
    ).json()
    def_id = table["stripe_definitions"][0]["id"]
    table = client.post(
        f"/matching-rule-tables/{table['id']}/stripe-marks",
        json={"name": "Guide Mark", "stripe_definition_id": def_id, "position": {"x": 0, "y": 0}},
        headers=headers,
    ).json()
    mark_id = table["stripe_marks"][0]["id"]

    client.post(
        f"/markers/{marker['id']}/matching/apply",
        json={"matching_rule_table_id": table["id"], "matching_method": "standard"},
        headers=headers,
    )

    resp = client.post(
        f"/markers/{marker['id']}/matching/guidance",
        json={"piece_id": "piece-x", "stripe_mark_id": mark_id, "x": 23, "y": 0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["found"] is False
    assert body["message"] == "Matching Location Not Found"
    assert len(body["targets"]) == 1
    assert body["targets"][0]["axis"] == "horizontal"
    assert body["targets"][0]["target_x"] == 20

    resp = client.post(
        f"/markers/{marker['id']}/matching/guidance",
        json={"piece_id": "piece-x", "stripe_mark_id": mark_id, "x": 20.5, "y": 0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["found"] is True
    assert resp.json()["targets"] == []


def test_validate_bite_detects_and_clears_violation():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_and_marker(unique)

    table_id = client.post(
        "/matching-rule-tables", json={"name": f"BiteTable-{unique}", "method": "standard"}, headers=headers
    ).json()["id"]
    client.post(
        f"/markers/{marker['id']}/matching/apply", json={"matching_rule_table_id": table_id}, headers=headers
    )

    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"BITE-A-{unique}", "Bite Piece A")
        piece_b = seed_nestable_piece(p, folder["id"], f"BITE-B-{unique}", "Bite Piece B")

    def _save(x_a: float, x_b: float):
        return client.put(
            f"/markers/{marker['id']}/workspace",
            json={
                "placements": [
                    {"piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
                     "placement_data": {"x": x_a, "y": 0, "width": 10, "height": 10, "stripe_mark_id": "sm-shared"}},
                    {"piece_id": piece_b["id"], "size_code": "M", "quantity": 1,
                     "placement_data": {"x": x_b, "y": 0, "width": 10, "height": 10, "stripe_mark_id": "sm-shared"}},
                ]
            },
            headers=headers,
        )

    resp = _save(5, 25)
    assert resp.status_code == 200, resp.text

    resp = client.get(f"/markers/{marker['id']}/matching/validate-bite", params={"bite_length": 20}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ok"] is False
    assert len(body["violations"]) == 1
    assert body["violations"][0]["bite_index_a"] == 0
    assert body["violations"][0]["bite_index_b"] == 1

    resp = _save(5, 15)
    assert resp.status_code == 200, resp.text
    resp = client.get(f"/markers/{marker['id']}/matching/validate-bite", params={"bite_length": 20}, headers=headers)
    assert resp.json()["ok"] is True
    assert resp.json()["violations"] == []
