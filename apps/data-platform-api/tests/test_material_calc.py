"""Marker Making Sec 1.7 (material calculation / utilization): the new order-level
target_length/target_utilization_pct fields and marker-level fabric_weight_per_unit_area field --
this platform only stores/validates them, the actual utilization/weight math lives in
marker-making-service (it interprets placement_data, this platform doesn't)."""

from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "material-tester", "X-Dev-Org": "MATERIALTEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def _bootstrap_admin(db_session) -> None:
    client.get("/me", headers=HEADERS)  # JIT-provision
    _grant_admin(db_session, "MATERIALTEST", "material-tester")


def _seed_order(db_session, unique_suffix: str):
    _bootstrap_admin(db_session)
    folder_id = client.post("/folders", json={"name": f"Material Folder {unique_suffix}"}, headers=HEADERS).json()["id"]
    style_id = client.post(
        "/styles",
        json={"folder_id": folder_id, "style_number": f"STY-MAT-{unique_suffix}", "style_name": "Material Style"},
        headers=HEADERS,
    ).json()["id"]
    order = client.post(
        "/orders",
        json={"folder_id": folder_id, "order_number": f"ORD-MAT-{unique_suffix}", "style_id": style_id},
        headers=HEADERS,
    ).json()
    marker = client.post(
        "/markers",
        json={"folder_id": folder_id, "marker_code": f"MRK-MAT-{unique_suffix}", "marker_name": "Material Marker",
              "order_id": order["id"]},
        headers=HEADERS,
    ).json()
    return folder_id, order, marker


def test_order_target_fields_default_null_and_patchable(db_session):
    _, order, _ = _seed_order(db_session, "01")
    assert order["target_length"] is None
    assert order["target_utilization_pct"] is None

    resp = client.patch(
        f"/orders/{order['id']}", json={"target_length": 120.5, "target_utilization_pct": 85.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["target_length"] == 120.5
    assert body["target_utilization_pct"] == 85.0
    assert body["version"] == 2


def test_order_target_utilization_pct_out_of_range_rejected(db_session):
    _, order, _ = _seed_order(db_session, "02")

    resp = client.patch(
        f"/orders/{order['id']}", json={"target_utilization_pct": 150.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 400, resp.text

    resp = client.patch(
        f"/orders/{order['id']}", json={"target_utilization_pct": -5.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 400, resp.text


def test_marker_material_fields_default_null_and_patchable(db_session):
    _, _, marker = _seed_order(db_session, "03")
    assert marker["marker_length"] is None
    assert marker["ply_count"] is None
    assert marker["utilization_pct"] is None
    assert marker["fabric_weight_per_unit_area"] is None

    resp = client.patch(
        f"/markers/{marker['id']}",
        json={"marker_length": 300.0, "ply_count": 40, "utilization_pct": 78.5, "fabric_weight_per_unit_area": 0.15},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["marker_length"] == 300.0
    assert body["ply_count"] == 40
    assert body["utilization_pct"] == 78.5
    assert body["fabric_weight_per_unit_area"] == 0.15
    assert body["version"] == 2

    resp = client.get(f"/markers/{marker['id']}", headers=HEADERS)
    assert resp.json()["utilization_pct"] == 78.5


def test_marker_utilization_pct_out_of_range_rejected(db_session):
    _, _, marker = _seed_order(db_session, "04")

    resp = client.patch(
        f"/markers/{marker['id']}", json={"utilization_pct": 101.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 400, resp.text
