"""Marker Making Sec 1.9 (marker transformations): Shrink and Stretch (order-level settings +
the apply-to-current-placements stand-in) and Change Width of Marker, proxying through the real
data-platform-api subprocess (see conftest.py). Whole-marker Flip X/Y/XY needs no test here --
it's pure client-side geometry in marker-making-app (see src/geometry.ts's computeBoundingBox)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_org_marker(unique: str, fabric_width: float = 200.0, with_order: bool = True):
    org_code = f"TRANSFORM-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()

        order = None
        if with_order:
            style = p.post(
                "/styles", json={"folder_id": folder["id"], "style_number": f"STY-{unique}", "style_name": "Style"}
            ).json()
            order = p.post(
                "/orders", json={"folder_id": folder["id"], "order_number": f"ORD-{unique}", "style_id": style["id"]}
            ).json()

        marker_body = {"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Transform Marker",
                       "fabric_width": fabric_width}
        if order is not None:
            marker_body["order_id"] = order["id"]
        marker = p.post("/markers", json=marker_body).json()

    return headers, folder, marker, order


def _place_two_pieces(headers, folder, marker, unique):
    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"TRF-A-{unique}", "Transform Piece A")
        piece_b = seed_nestable_piece(p, folder["id"], f"TRF-B-{unique}", "Transform Piece B")

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
    return piece_a, piece_b


def test_transform_settings_reads_fabric_width_and_defaults():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)

    resp = client.get(f"/markers/{marker['id']}/transform/settings", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["fabric_width"] == 200.0
    assert body["shrink_x_pct"] is None
    assert body["shrink_y_pct"] is None


def test_shrink_stretch_patch_requires_linked_order():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique, with_order=False)

    resp = client.patch(
        f"/markers/{marker['id']}/transform/shrink-stretch", json={"shrink_x_pct": -25.0}, headers=headers,
    )
    assert resp.status_code == 400


def test_shrink_stretch_patch_persists_to_linked_order():
    unique = unique_suffix()
    headers, _folder, marker, order = _seed_org_marker(unique)

    resp = client.patch(
        f"/markers/{marker['id']}/transform/shrink-stretch",
        json={"shrink_x_pct": -25.0, "shrink_y_pct": 10.0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["shrink_x_pct"] == -25.0
    assert body["shrink_y_pct"] == 10.0

    with platform_client(headers) as p:
        order_row = p.get(f"/orders/{order['id']}").json()
    assert order_row["shrink_x_pct"] == -25.0
    assert order_row["shrink_y_pct"] == 10.0


def test_apply_shrink_stretch_requires_settings():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    resp = client.post(f"/markers/{marker['id']}/transform/apply-shrink-stretch", headers=headers)
    assert resp.status_code == 400


def test_apply_shrink_stretch_requires_placements():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)
    client.patch(f"/markers/{marker['id']}/transform/shrink-stretch", json={"shrink_x_pct": -25.0}, headers=headers)

    resp = client.post(f"/markers/{marker['id']}/transform/apply-shrink-stretch", headers=headers)
    assert resp.status_code == 400


def test_apply_shrink_stretch_scales_placements_anchored_at_bbox():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    piece_a, piece_b = _place_two_pieces(headers, folder, marker, unique)

    # shrink_x_pct=-50 -> scale_x=0.5, shrink_y_pct=+100 -> scale_y=2.0
    client.patch(
        f"/markers/{marker['id']}/transform/shrink-stretch",
        json={"shrink_x_pct": -50.0, "shrink_y_pct": 100.0}, headers=headers,
    )

    resp = client.post(f"/markers/{marker['id']}/transform/apply-shrink-stretch", headers=headers)
    assert resp.status_code == 200, resp.text
    placements = {p["piece_id"]: p["placement_data"] for p in resp.json()["placements"]}

    # bbox: min_x=10, min_y=5. Piece A (x=10,y=20,w=50,h=40):
    #   new_x = 10 + (10-10)*0.5 = 10, new_width = 25
    #   new_y = 5 + (20-5)*2.0 = 35, new_height = 80
    a = placements[piece_a["id"]]
    assert a["x"] == 10.0
    assert a["width"] == 25.0
    assert a["y"] == 35.0
    assert a["height"] == 80.0

    # Piece B (x=80,y=5,w=30,h=60):
    #   new_x = 10 + (80-10)*0.5 = 45, new_width = 15
    #   new_y = 5 + (5-5)*2.0 = 5, new_height = 120
    b = placements[piece_b["id"]]
    assert b["x"] == 45.0
    assert b["width"] == 15.0
    assert b["y"] == 5.0
    assert b["height"] == 120.0


def test_change_width_persists_fabric_width():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique, fabric_width=200.0)

    resp = client.post(
        f"/markers/{marker['id']}/transform/change-width", json={"fabric_width": 300.0}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["fabric_width"] == 300.0

    with platform_client(headers) as p:
        marker_row = p.get(f"/markers/{marker['id']}").json()
    assert marker_row["fabric_width"] == 300.0
