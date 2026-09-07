"""Marker Making Sec 1.8 (splice marks / fabric-roll handling): splice_marks CRUD and the
marker-level splice settings fields, plus the permission/audit/optimistic-concurrency contracts
every other Section 4 resource already has to honor."""

from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "splice-tester", "X-Dev-Org": "SPLICETEST"}
VIEWER_HEADERS = {"X-Dev-User": "splice-viewer", "X-Dev-Org": "SPLICETEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def _bootstrap_admin(db_session) -> None:
    client.get("/me", headers=HEADERS)  # JIT-provision
    _grant_admin(db_session, "SPLICETEST", "splice-tester")


def _seed_marker(db_session, unique_suffix: str):
    _bootstrap_admin(db_session)
    resp = client.post("/folders", json={"name": f"Splice Folder {unique_suffix}"}, headers=HEADERS)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/markers",
        json={"folder_id": folder_id, "marker_code": f"MRK-SPL-{unique_suffix}", "marker_name": "Splice Marker"},
        headers=HEADERS,
    )
    return resp.json()


def test_marker_splice_settings_default_null_and_patchable(db_session):
    marker = _seed_marker(db_session, "01")
    assert marker["splice_min_length"] is None
    assert marker["splice_max_length"] is None
    assert marker["splice_margin"] is None
    assert marker["splice_separation"] is None

    resp = client.patch(
        f"/markers/{marker['id']}",
        json={"splice_min_length": 1.0, "splice_max_length": 5.0, "splice_margin": 0.5, "splice_separation": 2.0},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["splice_min_length"] == 1.0
    assert body["splice_max_length"] == 5.0
    assert body["splice_margin"] == 0.5
    assert body["splice_separation"] == 2.0


def test_create_manual_splice_mark_defaults(db_session):
    marker = _seed_marker(db_session, "02")
    resp = client.post(
        f"/markers/{marker['id']}/splice-marks",
        json={"start_x": 10.0, "end_x": 12.0, "roll_id": "roll-1"},
        headers=HEADERS,
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["source"] == "manual"
    assert body["roll_id"] == "roll-1"
    assert body["version"] == 1


def test_patch_requires_correct_version_and_audits(db_session):
    marker = _seed_marker(db_session, "03")
    resp = client.post(
        f"/markers/{marker['id']}/splice-marks", json={"start_x": 5.0, "end_x": 7.0}, headers=HEADERS,
    )
    mark_id = resp.json()["id"]

    resp = client.patch(
        f"/splice-marks/{mark_id}", json={"end_x": 8.0}, headers={**HEADERS, "If-Match-Version": "999"},
    )
    assert resp.status_code == 409

    resp = client.patch(
        f"/splice-marks/{mark_id}", json={"end_x": 8.0}, headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["end_x"] == 8.0
    assert resp.json()["version"] == 2

    resp = client.get(
        "/audit-log", params={"entity_type": "splice_mark", "entity_id": mark_id}, headers=HEADERS
    )
    assert resp.status_code == 200, resp.text
    actions = [row["action"] for row in resp.json()["items"]]
    assert "splice_mark.create" in actions
    assert "splice_mark.update" in actions


def test_viewer_role_read_only_for_splice_mark(db_session):
    client.get("/me", headers=VIEWER_HEADERS)  # JIT-provision with default 'viewer' role only
    marker = _seed_marker(db_session, "04")

    resp = client.post(
        f"/markers/{marker['id']}/splice-marks", json={"start_x": 1.0, "end_x": 2.0}, headers=VIEWER_HEADERS,
    )
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "permission_denied"

    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=VIEWER_HEADERS)
    assert resp.status_code == 200, resp.text


def test_delete_all_splice_marks_filters_by_source(db_session):
    marker = _seed_marker(db_session, "05")
    client.post(
        f"/markers/{marker['id']}/splice-marks",
        json={"start_x": 1.0, "end_x": 2.0, "source": "auto", "roll_id": "roll-1"},
        headers=HEADERS,
    )
    client.post(
        f"/markers/{marker['id']}/splice-marks",
        json={"start_x": 3.0, "end_x": 4.0, "source": "auto", "roll_id": "roll-2"},
        headers=HEADERS,
    )
    manual = client.post(
        f"/markers/{marker['id']}/splice-marks", json={"start_x": 5.0, "end_x": 6.0}, headers=HEADERS,
    ).json()

    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=HEADERS)
    assert len(resp.json()) == 3

    resp = client.delete(f"/markers/{marker['id']}/splice-marks", params={"source": "auto"}, headers=HEADERS)
    assert resp.status_code == 204, resp.text

    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=HEADERS)
    remaining = resp.json()
    assert len(remaining) == 1
    assert remaining[0]["id"] == manual["id"]

    resp = client.delete(f"/markers/{marker['id']}/splice-marks", headers=HEADERS)
    assert resp.status_code == 204, resp.text
    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=HEADERS)
    assert resp.json() == []


def test_delete_splice_mark(db_session):
    marker = _seed_marker(db_session, "06")
    mark = client.post(
        f"/markers/{marker['id']}/splice-marks", json={"start_x": 1.0, "end_x": 2.0}, headers=HEADERS,
    ).json()

    resp = client.delete(f"/splice-marks/{mark['id']}", headers=HEADERS)
    assert resp.status_code == 204, resp.text

    resp = client.get(f"/markers/{marker['id']}/splice-marks", headers=HEADERS)
    assert resp.json() == []
