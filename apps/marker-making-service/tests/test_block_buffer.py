"""Marker Making Sec 1.6 (block / buffer / fuse-blocking): Block Buffer Rule Table CRUD (thin
proxy) and Fuse Block bounding-box computation/lifecycle -- all proxying through the real
data-platform-api subprocess (see conftest.py)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_org_and_marker(unique: str):
    org_code = f"BLOCKBUF-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
        marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Block Buffer Marker"},
        ).json()

    return headers, folder, marker


def test_block_buffer_rule_table_crud():
    unique = unique_suffix()
    headers, _folder, _marker = _seed_org_and_marker(unique)

    resp = client.post(
        "/block-buffer-rule-tables",
        json={"name": f"Rule-{unique}", "rule_no": 1, "rule_type": "block", "mode": "static", "left_amt": 0.25},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    table = resp.json()
    assert table["left_amt"] == 0.25
    assert table["version"] == 1

    resp = client.post(
        "/block-buffer-rule-tables",
        json={"name": "Bad rule type", "rule_no": 2, "rule_type": "not-real", "mode": "static"},
        headers=headers,
    )
    assert resp.status_code == 400

    resp = client.patch(
        f"/block-buffer-rule-tables/{table['id']}", json={"top_amt": 0.5}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["top_amt"] == 0.5
    assert resp.json()["version"] == 2

    resp = client.get("/block-buffer-rule-tables", headers=headers)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["items"]) == 1

    resp = client.delete(f"/block-buffer-rule-tables/{table['id']}", headers=headers)
    assert resp.status_code == 204, resp.text


def test_fuse_block_bounding_box_from_placements():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_and_marker(unique)

    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"FUSE-A-{unique}", "Fuse Piece A")
        piece_b = seed_nestable_piece(p, folder["id"], f"FUSE-B-{unique}", "Fuse Piece B")

    save_body = {
        "placements": [
            {
                "piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
                "placement_data": {"x": 10, "y": 20, "width": 50, "height": 40},
            },
            {
                "piece_id": piece_b["id"], "size_code": "M", "quantity": 1,
                "placement_data": {"x": 80, "y": 5, "width": 30, "height": 60},
            },
        ]
    }
    resp = client.put(f"/markers/{marker['id']}/workspace", json=save_body, headers=headers)
    assert resp.status_code == 200, resp.text

    # Tight bbox: x=min(10,80)=10, y=min(20,5)=5, x2=max(60,110)=110, y2=max(60,65)=65
    # -> width=100, height=60
    resp = client.post(
        f"/markers/{marker['id']}/fuse-blocks",
        json={"piece_ids": [piece_a["id"], piece_b["id"]]},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    block = resp.json()
    assert block["x"] == 10
    assert block["y"] == 5
    assert block["width"] == 100
    assert block["height"] == 60
    assert block["block_amount"] == 0.5
    assert block["reduce_amount"] == 0.0
    assert block["notch_depth"] == 0.5
    assert set(block["piece_placement_ids"]) == {piece_a["id"], piece_b["id"]}

    resp = client.post(
        f"/markers/{marker['id']}/fuse-blocks", json={"piece_ids": ["not-a-real-piece"]}, headers=headers,
    )
    assert resp.status_code == 400

    resp = client.post(f"/markers/{marker['id']}/fuse-blocks", json={"piece_ids": []}, headers=headers)
    assert resp.status_code == 400


def test_fuse_block_modify_recomputes_bounds_and_lifecycle():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_and_marker(unique)

    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"FUSE-C-{unique}", "Fuse Piece C")
        piece_b = seed_nestable_piece(p, folder["id"], f"FUSE-D-{unique}", "Fuse Piece D")

    client.put(
        f"/markers/{marker['id']}/workspace",
        json={
            "placements": [
                {"piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 0, "y": 0, "width": 20, "height": 20}},
                {"piece_id": piece_b["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 100, "y": 100, "width": 20, "height": 20}},
            ]
        },
        headers=headers,
    )

    block = client.post(
        f"/markers/{marker['id']}/fuse-blocks", json={"piece_ids": [piece_a["id"]]}, headers=headers,
    ).json()
    assert block["width"] == 20
    assert block["height"] == 20

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=headers)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 1

    # Modify to include piece_b too -> bbox should expand to cover both.
    resp = client.patch(
        f"/markers/{marker['id']}/fuse-blocks/{block['id']}",
        json={"piece_ids": [piece_a["id"], piece_b["id"]], "block_amount": 0.75, "reduce_amount": 0.1},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    modified = resp.json()
    assert modified["x"] == 0
    assert modified["y"] == 0
    assert modified["width"] == 120
    assert modified["height"] == 120
    assert modified["block_amount"] == 0.75
    assert modified["reduce_amount"] == 0.1
    assert abs(modified["notch_depth"] - 0.65) < 1e-9
    assert modified["version"] == 2

    resp = client.delete(f"/markers/{marker['id']}/fuse-blocks/{block['id']}", headers=headers)
    assert resp.status_code == 204, resp.text
    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=headers)
    assert resp.json() == []


def test_fuse_block_delete_all():
    unique = unique_suffix()
    headers, folder, marker = _seed_org_and_marker(unique)

    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"FUSE-E-{unique}", "Fuse Piece E")

    client.put(
        f"/markers/{marker['id']}/workspace",
        json={"placements": [
            {"piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
             "placement_data": {"x": 0, "y": 0, "width": 10, "height": 10}},
        ]},
        headers=headers,
    )

    for _ in range(2):
        client.post(f"/markers/{marker['id']}/fuse-blocks", json={"piece_ids": [piece_a["id"]]}, headers=headers)

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=headers)
    assert len(resp.json()) == 2

    resp = client.delete(f"/markers/{marker['id']}/fuse-blocks", headers=headers)
    assert resp.status_code == 204, resp.text

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=headers)
    assert resp.json() == []
