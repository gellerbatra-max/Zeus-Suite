"""Marker Making Sec 1.9 (marker transformations): the new order-level shrink_x_pct/shrink_y_pct
fields -- this platform only stores/validates them, the actual scaling of placement_data happens
in marker-making-service (it interprets placement_data, this platform doesn't). Whole-marker Flip
X/Y/XY needs no platform schema at all -- it's a pure client-side transform of the already-loaded
placements, persisted through the existing `PUT /markers/{id}/pieces` bulk-replace endpoint."""

from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "transform-tester", "X-Dev-Org": "TRANSFORMTEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def _bootstrap_admin(db_session) -> None:
    client.get("/me", headers=HEADERS)  # JIT-provision
    _grant_admin(db_session, "TRANSFORMTEST", "transform-tester")


def _seed_order(db_session, unique_suffix: str):
    _bootstrap_admin(db_session)
    folder_id = client.post("/folders", json={"name": f"Transform Folder {unique_suffix}"}, headers=HEADERS).json()["id"]
    style_id = client.post(
        "/styles",
        json={"folder_id": folder_id, "style_number": f"STY-TRF-{unique_suffix}", "style_name": "Transform Style"},
        headers=HEADERS,
    ).json()["id"]
    return client.post(
        "/orders",
        json={"folder_id": folder_id, "order_number": f"ORD-TRF-{unique_suffix}", "style_id": style_id},
        headers=HEADERS,
    ).json()


def test_order_shrink_fields_default_null_and_patchable(db_session):
    order = _seed_order(db_session, "01")
    assert order["shrink_x_pct"] is None
    assert order["shrink_y_pct"] is None

    resp = client.patch(
        f"/orders/{order['id']}", json={"shrink_x_pct": -25.0, "shrink_y_pct": 10.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["shrink_x_pct"] == -25.0
    assert body["shrink_y_pct"] == 10.0
    assert body["version"] == 2


def test_order_shrink_pct_at_or_below_negative_100_rejected(db_session):
    order = _seed_order(db_session, "02")

    resp = client.patch(
        f"/orders/{order['id']}", json={"shrink_x_pct": -100.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 400, resp.text

    resp = client.patch(
        f"/orders/{order['id']}", json={"shrink_y_pct": -150.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 400, resp.text
