"""Marker Making Sec 1.5 (layrules automation): layrule_search_tables CRUD, layrules CRUD, and the
permission/audit/optimistic-concurrency contracts every other Section 4 resource already has to
honor."""

from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "layrule-tester", "X-Dev-Org": "LAYRULETEST"}
VIEWER_HEADERS = {"X-Dev-User": "layrule-viewer", "X-Dev-Org": "LAYRULETEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def _bootstrap_admin(db_session) -> None:
    client.get("/me", headers=HEADERS)  # JIT-provision
    _grant_admin(db_session, "LAYRULETEST", "layrule-tester")


def _seed_marker(db_session, unique_suffix: str):
    _bootstrap_admin(db_session)
    resp = client.post("/folders", json={"name": f"Layrule Folder {unique_suffix}"}, headers=HEADERS)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/markers",
        json={"folder_id": folder_id, "marker_code": f"MRK-LR-{unique_suffix}", "marker_name": "Layrule Marker"},
        headers=HEADERS,
    )
    return resp.json()


def test_create_layrule_search_table_defaults(db_session):
    _bootstrap_admin(db_session)
    resp = client.post("/layrule-search-tables", json={"name": "Standard Search"}, headers=HEADERS)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["area_compare"] is True
    assert body["area_deviation_pct"] == 5.0
    assert body["allow_overrides"] is True
    assert body["version"] == 1


def test_patch_layrule_search_table_requires_correct_version_and_audits(db_session):
    _bootstrap_admin(db_session)
    resp = client.post(
        "/layrule-search-tables",
        json={"name": "Patch Target", "area_deviation_pct": 10.0, "allow_overrides": False},
        headers=HEADERS,
    )
    table_id = resp.json()["id"]

    resp = client.patch(
        f"/layrule-search-tables/{table_id}", json={"area_deviation_pct": 8.0},
        headers={**HEADERS, "If-Match-Version": "999"},
    )
    assert resp.status_code == 409

    resp = client.patch(
        f"/layrule-search-tables/{table_id}", json={"area_deviation_pct": 8.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["area_deviation_pct"] == 8.0
    assert resp.json()["version"] == 2

    resp = client.get(
        "/audit-log", params={"entity_type": "layrule_search_table", "entity_id": table_id}, headers=HEADERS
    )
    assert resp.status_code == 200, resp.text
    actions = [row["action"] for row in resp.json()["items"]]
    assert "layrule_search_table.create" in actions
    assert "layrule_search_table.update" in actions


def test_viewer_role_read_only_for_layrule_search_table(db_session):
    client.get("/me", headers=VIEWER_HEADERS)  # JIT-provision with default 'viewer' role only

    resp = client.post("/layrule-search-tables", json={"name": "Viewer Table"}, headers=VIEWER_HEADERS)
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "permission_denied"

    resp = client.get("/layrule-search-tables", headers=VIEWER_HEADERS)
    assert resp.status_code == 200, resp.text


def test_layrule_create_get_patch_delete_lifecycle(db_session):
    marker = _seed_marker(db_session, "01")
    placements = [
        {"piece_id": "piece-a", "size_code": "M", "quantity": 1,
         "placement_data": {"x": 10, "y": 20, "width": 50, "height": 40}},
        {"piece_id": "piece-b", "size_code": "M", "quantity": 1,
         "placement_data": {"x": 80, "y": 5, "width": 30, "height": 60}},
    ]
    resp = client.post(
        "/layrules",
        json={"name": "Captured Layout", "source_marker_id": marker["id"], "placements_json": placements},
        headers=HEADERS,
    )
    assert resp.status_code == 201, resp.text
    layrule = resp.json()
    assert layrule["piece_count"] == 2
    assert layrule["placements_json"] == placements
    assert layrule["source_marker_id"] == marker["id"]

    resp = client.get(f"/layrules/{layrule['id']}", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    assert resp.json()["piece_count"] == 2

    resp = client.patch(
        f"/layrules/{layrule['id']}", json={"name": "Renamed Layout"},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["name"] == "Renamed Layout"
    assert resp.json()["version"] == 2

    resp = client.get("/layrules", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["items"]) == 1

    resp = client.delete(f"/layrules/{layrule['id']}", headers=HEADERS)
    assert resp.status_code == 204, resp.text
    resp = client.get("/layrules", headers=HEADERS)
    assert resp.json()["items"] == []


def test_marker_layrule_fields_default_null_and_patchable(db_session):
    marker = _seed_marker(db_session, "02")
    assert marker["force_layrule_name"] is None
    assert marker["layrule_search_table_id"] is None

    table = client.post("/layrule-search-tables", json={"name": "Linked Table"}, headers=HEADERS).json()

    resp = client.patch(
        f"/markers/{marker['id']}",
        json={"force_layrule_name": "REPEAT-ORDER-42", "layrule_search_table_id": table["id"]},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["force_layrule_name"] == "REPEAT-ORDER-42"
    assert body["layrule_search_table_id"] == table["id"]


def test_marker_layrule_search_table_cross_org_rejected(db_session):
    marker = _seed_marker(db_session, "03")

    other_org_headers = {"X-Dev-User": "other-user", "X-Dev-Org": "OTHERORG"}
    client.get("/me", headers=other_org_headers)
    _grant_admin(db_session, "OTHERORG", "other-user")
    other_table = client.post(
        "/layrule-search-tables", json={"name": "Other Org Table"}, headers=other_org_headers
    ).json()

    resp = client.patch(
        f"/markers/{marker['id']}", json={"layrule_search_table_id": other_table["id"]},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 400
