"""Milestone 3 exit check: org-wide grants, folder-scoped grants, ancestor-folder inheritance, and
revocation-takes-effect-immediately, all pass against a seeded test dataset. Plus JIT
user-provisioning (Section 5.4): create-on-first-login and update-on-repeat-login."""

import uuid

from app.auth import dev_login, resolve_permissions
from app.models import Folder, Organization, Role, UserRole


def _make_org(session, unique: str) -> Organization:
    org = Organization(name="Acme", code=f"ACME-{unique}")
    session.add(org)
    session.flush()
    return org


def test_jit_provisioning_creates_user_with_default_role(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = _make_org(session, unique)

    user = dev_login(session, org.id, username=f"jsmith-{unique}", email="jsmith@example.com", full_name="Jamie Smith")
    session.commit()

    viewer_role = session.query(Role).filter_by(code="viewer").one()
    grant = (
        session.query(UserRole)
        .filter_by(user_id=user.id, role_id=viewer_role.id, folder_id=None)
        .one_or_none()
    )
    assert grant is not None


def test_jit_provisioning_updates_profile_on_repeat_login(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = _make_org(session, unique)

    first = dev_login(session, org.id, username=f"jsmith-{unique}", email="old@example.com", full_name="Old Name")
    session.commit()

    second = dev_login(session, org.id, username=f"jsmith-{unique}", email="new@example.com", full_name="New Name")
    session.commit()

    assert first.id == second.id
    assert second.email == "new@example.com"
    assert second.full_name == "New Name"


def test_org_wide_grant_applies_with_no_folder_context(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = _make_org(session, unique)
    user = dev_login(session, org.id, username=f"u-{unique}", email="u@example.com", full_name="U")
    session.commit()

    # dev_login already grants org-wide 'viewer' via JIT provisioning.
    perms = resolve_permissions(session, user.id)
    assert "piece.read" in perms
    assert "folder.read" in perms


def test_folder_scoped_grant_and_ancestor_inheritance(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = _make_org(session, unique)
    user = dev_login(session, org.id, username=f"u-{unique}", email="u@example.com", full_name="U")
    session.flush()

    parent = Folder(
        organization_id=org.id,
        name=f"Parent-{unique}",
        path=f"/Parent-{unique}",
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(parent)
    session.flush()

    child = Folder(
        organization_id=org.id,
        parent_id=parent.id,
        name="Child",
        path=f"/Parent-{unique}/Child",
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(child)
    session.flush()

    contractor_role = session.query(Role).filter_by(code="contractor_qa").one()
    session.add(UserRole(user_id=user.id, role_id=contractor_role.id, folder_id=parent.id, granted_by=user.id))
    session.commit()

    # Granted at the parent -> applies to the parent itself and to descendant folders.
    assert "piece.status.approved" in resolve_permissions(session, user.id, folder_id=parent.id)
    assert "piece.status.approved" in resolve_permissions(session, user.id, folder_id=child.id)

    # A sibling folder outside the grant's subtree must not inherit it.
    sibling = Folder(
        organization_id=org.id,
        name=f"Sibling-{unique}",
        path=f"/Sibling-{unique}",
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(sibling)
    session.commit()
    assert "piece.status.approved" not in resolve_permissions(session, user.id, folder_id=sibling.id)


def test_revocation_takes_effect_immediately(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = _make_org(session, unique)
    user = dev_login(session, org.id, username=f"u-{unique}", email="u@example.com", full_name="U")
    session.flush()

    admin_role = session.query(Role).filter_by(code="admin").one()
    grant = UserRole(user_id=user.id, role_id=admin_role.id, folder_id=None, granted_by=user.id)
    session.add(grant)
    session.commit()

    assert "rbac.admin" in resolve_permissions(session, user.id)

    session.delete(grant)
    session.commit()

    assert "rbac.admin" not in resolve_permissions(session, user.id)
