"""Section 4.10: reports. Not a numbered milestone's own exit check -- this closes a gap (the
Reports API was never built in Milestones 4-6) needed before Milestone 7's reporting UI has
anything to call."""

import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.models import Folder, Organization, Piece, Role, User, UserRole, WorkflowStatus

client = TestClient(app)


def _grant_admin(session, org_code: str, username: str) -> None:
    org = session.query(Organization).filter_by(code=org_code).one()
    user = session.query(User).filter_by(organization_id=org.id, username=username).one()
    role = session.query(Role).filter_by(code="admin").one()
    session.add(UserRole(user_id=user.id, role_id=role.id, folder_id=None, granted_by=user.id))
    session.commit()


def test_list_definitions_and_run_single_piece_report(db_session):
    unique = uuid.uuid4().hex[:8]
    org_code = f"REPORTS-{unique}"
    headers = {"X-Dev-User": f"reporter-{unique}", "X-Dev-Org": org_code}
    client.get("/me", headers=headers)
    _grant_admin(db_session, org_code, f"reporter-{unique}")

    resp = client.get("/reports/definitions", headers=headers)
    assert resp.status_code == 200, resp.text
    codes = {r["code"] for r in resp.json()}
    assert {"single_piece", "all_piece", "all_marker"} <= codes

    org = db_session.query(Organization).filter_by(code=org_code).one()
    user = db_session.query(User).filter_by(organization_id=org.id, username=f"reporter-{unique}").one()
    folder = Folder(organization_id=org.id, name="F", path=f"/F-{unique}", created_by=user.id, updated_by=user.id)
    db_session.add(folder)
    db_session.flush()
    piece = Piece(
        organization_id=org.id, folder_id=folder.id, piece_code=f"P-{unique}", piece_name="Report Test Piece",
        workflow_status_id=db_session.query(WorkflowStatus).filter_by(entity_type="piece", code="unmade").one().id,
        created_by=user.id, updated_by=user.id,
    )
    db_session.add(piece)
    db_session.commit()

    resp = client.post(
        "/reports/run", json={"report_code": "single_piece", "entity_id": str(piece.id)}, headers=headers
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "completed"
    assert body["result_inline"]["piece_code"] == f"P-{unique}"

    resp = client.get(f"/reports/runs/{body['id']}", headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["result_inline"]["piece_code"] == f"P-{unique}"

    resp = client.post("/reports/run", json={"report_code": "all_piece"}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert any(p["piece_code"] == f"P-{unique}" for p in resp.json()["result_inline"]["pieces"])


def test_unimplemented_report_code_returns_501(db_session):
    unique = uuid.uuid4().hex[:8]
    org_code = f"REPORTS2-{unique}"
    headers = {"X-Dev-User": f"reporter-{unique}", "X-Dev-Org": org_code}
    client.get("/me", headers=headers)
    _grant_admin(db_session, org_code, f"reporter-{unique}")

    resp = client.post("/reports/run", json={"report_code": "splice"}, headers=headers)
    assert resp.status_code == 501


def test_report_run_requires_permission(db_session):
    """The default JIT-provisioned 'viewer' role has *.read but not report.run (Appendix B) --
    running a report must be denied until that's explicitly granted."""
    unique = uuid.uuid4().hex[:8]
    org_code = f"REPORTS3-{unique}"
    headers = {"X-Dev-User": f"viewer-{unique}", "X-Dev-Org": org_code}
    client.get("/me", headers=headers)

    resp = client.post("/reports/run", json={"report_code": "all_piece"}, headers=headers)
    assert resp.status_code == 403
