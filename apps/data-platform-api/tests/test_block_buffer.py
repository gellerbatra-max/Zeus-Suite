"""Marker Making Sec 1.6 (block / buffer / fuse-blocking): block_buffer_rule_tables CRUD and
fuse_blocks lifecycle, plus the permission/audit/optimistic-concurrency contracts every other
Section 4 resource already has to honor."""

from fastapi.testclient import TestClient

from app.main import app
from app.models import Organization, Role, User, UserRole

client = TestClient(app)
HEADERS = {"X-Dev-User": "blockbuffer-tester", "X-Dev-Org": "BLOCKTEST"}
VIEWER_HEADERS = {"X-Dev-User": "blockbuffer-viewer", "X-Dev-Org": "BLOCKTEST"}


def _grant_admin(db_session, org_code: str, username: str) -> None:
    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=username).one()
    admin_role = db_session.query(Role).filter_by(code="admin").one()
    db_session.add(UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id))
    db_session.commit()


def _bootstrap_admin(db_session) -> None:
    client.get("/me", headers=HEADERS)  # JIT-provision
    _grant_admin(db_session, "BLOCKTEST", "blockbuffer-tester")


def test_create_block_buffer_rule_table_defaults(db_session):
    _bootstrap_admin(db_session)
    resp = client.post(
        "/block-buffer-rule-tables",
        json={"name": "Rule 1", "rule_no": 1, "rule_type": "block", "mode": "static"},
        headers=HEADERS,
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["left_amt"] == 0.0
    assert body["version"] == 1


def test_patch_requires_correct_version_and_audits(db_session):
    _bootstrap_admin(db_session)
    resp = client.post(
        "/block-buffer-rule-tables",
        json={"name": "Patch Target", "rule_no": 10, "rule_type": "buffer", "mode": "dynamic", "left_amt": 0.25},
        headers=HEADERS,
    )
    table_id = resp.json()["id"]

    resp = client.patch(
        f"/block-buffer-rule-tables/{table_id}", json={"name": "Renamed"},
        headers={**HEADERS, "If-Match-Version": "999"},
    )
    assert resp.status_code == 409

    resp = client.patch(
        f"/block-buffer-rule-tables/{table_id}", json={"name": "Renamed", "left_amt": 0.75},
        headers={**HEADERS, "If-Match-Version": "1"},
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["name"] == "Renamed"
    assert resp.json()["left_amt"] == 0.75
    assert resp.json()["version"] == 2

    resp = client.get(
        "/audit-log", params={"entity_type": "block_buffer_rule_table", "entity_id": table_id}, headers=HEADERS
    )
    assert resp.status_code == 200, resp.text
    actions = [row["action"] for row in resp.json()["items"]]
    assert "block_buffer_rule_table.create" in actions
    assert "block_buffer_rule_table.update" in actions


def test_viewer_role_read_only_for_rule_table(db_session):
    client.get("/me", headers=VIEWER_HEADERS)  # JIT-provision with default 'viewer' role only

    resp = client.post(
        "/block-buffer-rule-tables",
        json={"name": "Viewer Table", "rule_no": 20, "rule_type": "block", "mode": "static"},
        headers=VIEWER_HEADERS,
    )
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "permission_denied"

    resp = client.get("/block-buffer-rule-tables", headers=VIEWER_HEADERS)
    assert resp.status_code == 200, resp.text


def _seed_marker(db_session, unique_suffix: str):
    _bootstrap_admin(db_session)
    resp = client.post("/folders", json={"name": f"Fuse Block Folder {unique_suffix}"}, headers=HEADERS)
    folder_id = resp.json()["id"]
    resp = client.post(
        "/markers",
        json={"folder_id": folder_id, "marker_code": f"MRK-FB-{unique_suffix}", "marker_name": "Fuse Block Marker"},
        headers=HEADERS,
    )
    return resp.json()


def test_fuse_block_create_patch_delete_lifecycle(db_session):
    marker = _seed_marker(db_session, "01")

    resp = client.post(
        f"/markers/{marker['id']}/fuse-blocks",
        json={
            "piece_placement_ids": ["piece-a", "piece-b"],
            "x": 10.0, "y": 20.0, "width": 100.0, "height": 50.0,
        },
        headers=HEADERS,
    )
    assert resp.status_code == 201, resp.text
    fuse_block = resp.json()
    assert fuse_block["marker_id"] == marker["id"]
    assert fuse_block["shape"] == "rectangle"
    assert fuse_block["block_amount"] == 0.5
    assert fuse_block["reduce_amount"] == 0.0
    assert fuse_block["piece_placement_ids"] == ["piece-a", "piece-b"]

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()) == 1

    resp = client.patch(
        f"/fuse-blocks/{fuse_block['id']}",
        json={"width": 120.0, "block_amount": 0.75},
        headers={**HEADERS, "If-Match-Version": str(fuse_block["version"])},
    )
    assert resp.status_code == 200, resp.text
    updated = resp.json()
    assert updated["width"] == 120.0
    assert updated["block_amount"] == 0.75
    assert updated["version"] == 2

    resp = client.get(f"/fuse-blocks/{fuse_block['id']}", headers=HEADERS)
    assert resp.status_code == 200, resp.text
    assert resp.json()["width"] == 120.0

    resp = client.delete(f"/fuse-blocks/{fuse_block['id']}", headers=HEADERS)
    assert resp.status_code == 204, resp.text

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=HEADERS)
    assert resp.json() == []


def test_fuse_block_delete_all(db_session):
    marker = _seed_marker(db_session, "02")

    for _ in range(3):
        client.post(
            f"/markers/{marker['id']}/fuse-blocks",
            json={"piece_placement_ids": ["piece-x"], "x": 0.0, "y": 0.0, "width": 10.0, "height": 10.0},
            headers=HEADERS,
        )

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=HEADERS)
    assert len(resp.json()) == 3

    resp = client.delete(f"/markers/{marker['id']}/fuse-blocks", headers=HEADERS)
    assert resp.status_code == 204, resp.text

    resp = client.get(f"/markers/{marker['id']}/fuse-blocks", headers=HEADERS)
    assert resp.json() == []
