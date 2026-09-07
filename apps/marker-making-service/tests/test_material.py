"""Marker Making Sec 1.7 (material calculation / utilization): live computation from current
placements (this service interprets placement_data, the platform doesn't), persisting computed
values back onto the platform marker, and the two pure-calculation endpoints (required length /
weight) -- all proxying through the real data-platform-api subprocess (see conftest.py)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_org_marker(unique: str, fabric_width: float = 200.0, with_order: bool = False):
    org_code = f"MATERIAL-{unique}"
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

        marker_body = {"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Material Marker",
                       "fabric_width": fabric_width}
        if order is not None:
            marker_body["order_id"] = order["id"]
        marker = p.post("/markers", json=marker_body).json()

    return headers, folder, marker, order


def _place_two_pieces(headers, folder, marker, unique):
    with platform_client(headers) as p:
        piece_a = seed_nestable_piece(p, folder["id"], f"MAT-A-{unique}", "Material Piece A")
        piece_b = seed_nestable_piece(p, folder["id"], f"MAT-B-{unique}", "Material Piece B")

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


def test_material_summary_computes_from_placements():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    resp = client.get(f"/markers/{marker['id']}/material/summary", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["fabric_width"] == 200.0
    assert body["marker_length"] is None  # nothing stored on the marker yet
    assert body["computed_marker_length"] == 110.0  # max(10+50, 80+30)
    assert body["computed_total_piece_area"] == 3800.0  # 50*40 + 30*60
    assert body["computed_total_perimeter"] == 360.0  # 2*(50+40) + 2*(30+60)
    assert body["computed_utilization_pct"] == 17.27  # 3800 / (200*110) * 100, rounded


def test_material_summary_with_no_placements_has_no_computed_values():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)

    resp = client.get(f"/markers/{marker['id']}/material/summary", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["computed_marker_length"] is None
    assert body["computed_total_piece_area"] is None
    assert body["computed_utilization_pct"] is None


def test_apply_computed_persists_length_and_utilization():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    resp = client.post(f"/markers/{marker['id']}/material/apply-computed", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["marker_length"] == 110.0
    assert body["utilization_pct"] == 17.27

    with platform_client(headers) as p:
        marker_row = p.get(f"/markers/{marker['id']}").json()
    assert marker_row["marker_length"] == 110.0
    assert marker_row["utilization_pct"] == 17.27


def test_apply_computed_requires_placements():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)

    resp = client.post(f"/markers/{marker['id']}/material/apply-computed", headers=headers)
    assert resp.status_code == 400


def test_patch_material_sets_ply_count_and_weight_per_unit_area():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)

    resp = client.patch(
        f"/markers/{marker['id']}/material",
        json={"ply_count": 10, "fabric_weight_per_unit_area": 0.02},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["ply_count"] == 10
    assert body["fabric_weight_per_unit_area"] == 0.02


def test_material_target_patch_requires_linked_order():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique, with_order=False)

    resp = client.patch(
        f"/markers/{marker['id']}/material/target", json={"target_length": 100.0}, headers=headers,
    )
    assert resp.status_code == 400


def test_material_target_patch_persists_to_linked_order():
    unique = unique_suffix()
    headers, _folder, marker, order = _seed_org_marker(unique, with_order=True)

    resp = client.patch(
        f"/markers/{marker['id']}/material/target",
        json={"target_length": 150.0, "target_utilization_pct": 90.0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["target_length"] == 150.0
    assert body["target_utilization_pct"] == 90.0

    with platform_client(headers) as p:
        order_row = p.get(f"/orders/{order['id']}").json()
    assert order_row["target_length"] == 150.0
    assert order_row["target_utilization_pct"] == 90.0


def test_required_length_calculation():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    # total_piece_area=3800, fabric_width=200, target 50% efficiency -> 3800 / (200*0.5) = 38.0
    resp = client.post(
        f"/markers/{marker['id']}/material/required-length",
        json={"target_efficiency_pct": 50}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["required_length"] == 38.0


def test_required_length_rejects_non_positive_target():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    resp = client.post(
        f"/markers/{marker['id']}/material/required-length",
        json={"target_efficiency_pct": 0}, headers=headers,
    )
    assert resp.status_code == 400


def test_material_weight_calculation_with_explicit_args():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)

    # width=200 * length=38.0 * plies=10 * weight_per_unit_area=0.02 = 1520.0
    resp = client.post(
        f"/markers/{marker['id']}/material/weight",
        json={"weight_per_unit_area": 0.02, "plies": 10, "length": 38.0},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["weight"] == 1520.0


def test_material_weight_calculation_falls_back_to_stored_values():
    unique = unique_suffix()
    headers, folder, marker, _order = _seed_org_marker(unique)
    _place_two_pieces(headers, folder, marker, unique)

    client.patch(
        f"/markers/{marker['id']}/material",
        json={"ply_count": 10, "fabric_weight_per_unit_area": 0.02},
        headers=headers,
    )
    client.post(f"/markers/{marker['id']}/material/apply-computed", headers=headers)  # stores marker_length=110

    # width=200 * length=110 (stored marker_length) * plies=10 * weight_per_unit_area=0.02 = 4400.0
    resp = client.post(f"/markers/{marker['id']}/material/weight", json={}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["weight"] == 4400.0


def test_material_weight_calculation_rejects_missing_values():
    unique = unique_suffix()
    headers, _folder, marker, _order = _seed_org_marker(unique)

    resp = client.post(f"/markers/{marker['id']}/material/weight", json={}, headers=headers)
    assert resp.status_code == 400
