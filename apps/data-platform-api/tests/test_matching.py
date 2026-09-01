"""Marker Making Phase 2 Slice 2 (Sec 1.4/2, new): matching_rule_tables CRUD, sub-resource
full-replace endpoints, marker linkage, and the permission/audit/optimistic-concurrency contracts
every other Section 4 resource already has to honor."""

from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "matching-tester", "X-Dev-Org": "MATCHTEST"}
VIEWER_HEADERS = {"X-Dev-User": "matching-viewer", "X-Dev-Org": "MATCHTEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def _bootstrap_admin(db_session) -> None:
    client.get("/me", headers=HEADERS)  # JIT-provision
    _grant_admin(db_session, "MATCHTEST", "matching-tester")


def test_create_matching_rule_table_defaults(db_session):
    _bootstrap_admin(db_session)
    resp = client.post(
        "/matching-rule-tables", json={"name": "Standard Plaid A", "method": "standard"}, headers=HEADERS
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["stripe_definitions_json"] == []
    assert body["stripe_marks_json"] == []
    assert body["version"] == 1


def test_patch_requires_correct_version(db_session):
    _bootstrap_admin(db_session)
    resp = client.post("/matching-rule-tables", json={"name": "Patch Target", "method": "standard"}, headers=HEADERS)
    table_id = resp.json()["id"]

    resp = client.patch(
        f"/matching-rule-tables/{table_id}", json={"name": "Renamed"},
        headers={**HEADERS, "If-Match-Version": "999"},
    )
    assert resp.status_code == 409

    resp = client.patch(
        f"/matching-rule-tables/{table_id}", json={"name": "Renamed"},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["name"] == "Renamed"
    assert resp.json()["version"] == 2


def test_offsets_and_stripe_subresources_replace_and_audit(db_session):
    _bootstrap_admin(db_session)
    resp = client.post("/matching-rule-tables", json={"name": "Sub Resource Table", "method": "standard"}, headers=HEADERS)
    table = resp.json()
    table_id = table["id"]

    resp = client.put(
        f"/matching-rule-tables/{table_id}/offsets",
        json={"horizontal": [0.0, 5.0], "vertical": [0.0]},
        headers={**HEADERS, "If-Match-Version": str(table["version"])},
    )
    assert resp.status_code == 200, resp.text
    table = resp.json()
    assert table["offsets_json"] == {"horizontal": [0.0, 5.0], "vertical": [0.0]}

    resp = client.put(
        f"/matching-rule-tables/{table_id}/stripe-definitions",
        json={"items": [{"id": "sd-1", "name": "Main", "origin_x": 0.0, "h_distance": 10.0}]},
        headers={**HEADERS, "If-Match-Version": str(table["version"])},
    )
    assert resp.status_code == 200, resp.text
    table = resp.json()
    assert len(table["stripe_definitions_json"]) == 1

    resp = client.put(
        f"/matching-rule-tables/{table_id}/stripe-marks",
        json={"items": [{"id": "sm-1", "name": "Mark 1", "sequence": 1}]},
        headers={**HEADERS, "If-Match-Version": str(table["version"])},
    )
    assert resp.status_code == 200, resp.text

    resp = client.get(
        "/audit-log", params={"entity_type": "matching_rule_table", "entity_id": table_id}, headers=HEADERS
    )
    assert resp.status_code == 200, resp.text
    actions = [row["action"] for row in resp.json()["items"]]
    assert "matching_rule_table.create" in actions
    assert "matching_rule_table.offsets.replace" in actions
    assert "matching_rule_table.stripe_definitions.replace" in actions
    assert "matching_rule_table.stripe_marks.replace" in actions


def test_marker_can_link_to_matching_rule_table(db_session):
    _bootstrap_admin(db_session)
    resp = client.post("/matching-rule-tables", json={"name": "Link Table", "method": "five_star"}, headers=HEADERS)
    table_id = resp.json()["id"]

    resp = client.post("/folders", json={"name": "Matching Link Folder"}, headers=HEADERS)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/markers", json={"folder_id": folder_id, "marker_code": "MRK-LINK-01", "marker_name": "Link Marker"},
        headers=HEADERS,
    )
    marker = resp.json()

    resp = client.patch(
        f"/markers/{marker['id']}", json={"matching_rule_table_id": table_id, "matching_method": "five_star"},
        headers={**HEADERS, "If-Match-Version": str(marker["version"])},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["matching_rule_table_id"] == table_id
    assert resp.json()["matching_method"] == "five_star"


def test_marker_cannot_link_to_matching_rule_table_from_another_org(db_session):
    _bootstrap_admin(db_session)
    resp = client.post("/matching-rule-tables", json={"name": "Cross Org Table", "method": "standard"}, headers=HEADERS)
    table_id = resp.json()["id"]

    other_headers = {"X-Dev-User": "other-org-tester", "X-Dev-Org": "OTHERORG"}
    client.get("/me", headers=other_headers)
    _grant_admin(db_session, "OTHERORG", "other-org-tester")

    resp = client.post("/folders", json={"name": "Other Org Folder"}, headers=other_headers)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/markers", json={"folder_id": folder_id, "marker_code": "MRK-OTHER-01", "marker_name": "Other Marker"},
        headers=other_headers,
    )
    marker = resp.json()

    resp = client.patch(
        f"/markers/{marker['id']}", json={"matching_rule_table_id": table_id},
        headers={**other_headers, "If-Match-Version": str(marker["version"])},
    )
    assert resp.status_code == 400


def test_delete_blocked_while_referenced_by_marker(db_session):
    _bootstrap_admin(db_session)
    resp = client.post("/matching-rule-tables", json={"name": "Delete Guard Table", "method": "standard"}, headers=HEADERS)
    table_id = resp.json()["id"]
    resp = client.post("/matching-rule-tables", json={"name": "Delete Guard Table (unreferenced)", "method": "standard"}, headers=HEADERS)
    unreferenced_table_id = resp.json()["id"]

    resp = client.post("/folders", json={"name": "Delete Guard Folder"}, headers=HEADERS)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/markers", json={"folder_id": folder_id, "marker_code": "MRK-DELGUARD-01", "marker_name": "Guard Marker"},
        headers=HEADERS,
    )
    marker = resp.json()
    client.patch(
        f"/markers/{marker['id']}", json={"matching_rule_table_id": table_id},
        headers={**HEADERS, "If-Match-Version": str(marker["version"])},
    )

    # Referenced table is blocked from deletion...
    resp = client.delete(f"/matching-rule-tables/{table_id}", headers=HEADERS)
    assert resp.status_code == 409

    # ...but an unreferenced one deletes cleanly (PATCH has no way to unset a FK field once set --
    # None means "field not provided", same as every other MarkerPatch field -- so this only
    # proves the guard fires on a real reference, not that unlinking-then-delete works).
    resp = client.delete(f"/matching-rule-tables/{unreferenced_table_id}", headers=HEADERS)
    assert resp.status_code == 204


def test_viewer_role_read_only(db_session):
    client.get("/me", headers=VIEWER_HEADERS)  # JIT-provision with default 'viewer' role only

    resp = client.post("/matching-rule-tables", json={"name": "Viewer Table", "method": "standard"}, headers=VIEWER_HEADERS)
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "permission_denied"

    resp = client.get("/matching-rule-tables", headers=VIEWER_HEADERS)
    assert resp.status_code == 200, resp.text
