"""Milestone 3: Section 5's identity/RBAC model. The permission-resolution function and JIT user
provisioning are built and unit-tested here, independent of any HTTP endpoint, since every
endpoint in Milestone 4 depends on them being correct first (per the plan's own Milestone 3 note).

Real Microsoft Entra ID OIDC/JWT validation is deferred until a real tenant is available (see the
"Auth for now" decision in the Milestone 1 plan). `dev_login` below is the placeholder Milestone 4's
JWT validation middleware will replace: it trusts a caller-supplied identity outright instead of
verifying a signed ID token's claims. `resolve_permissions` and `jit_provision_user`, in contrast,
are the real Section 5.2/5.4 logic -- only the "who is this" step ahead of them is stubbed.
"""

import uuid

from sqlalchemy.orm import Session

from app.models import Folder, Permission, Role, RolePermission, User, UserRole

DEFAULT_ROLE_CODE = "viewer"  # Section 5.4: the deployment-configured default role for new users.


def resolve_permissions(session: Session, user_id: uuid.UUID, folder_id: uuid.UUID | None = None) -> set[str]:
    """Section 5.2: the effective permission set for a user, optionally scoped to a resource's
    folder. Always includes org-wide role grants; when `folder_id` is given, also includes every
    folder-scoped role grant whose folder is an ancestor-or-self of that folder (walked via
    `folders.path`). Computed fresh on every call -- no caching -- so a revoked role takes effect
    on the very next call, exactly as the spec requires."""
    org_wide_rows = (
        session.query(Permission.code)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .filter(UserRole.user_id == user_id, UserRole.folder_id.is_(None))
        .all()
    )
    codes = {code for (code,) in org_wide_rows}

    if folder_id is None:
        return codes

    resource_folder = session.get(Folder, folder_id)
    if resource_folder is None:
        return codes

    scoped_rows = (
        session.query(Permission.code, Folder.path)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .join(Folder, Folder.id == UserRole.folder_id)
        .filter(UserRole.user_id == user_id, UserRole.folder_id.isnot(None))
        .all()
    )
    for code, grant_path in scoped_rows:
        is_ancestor_or_self = resource_folder.path == grant_path or resource_folder.path.startswith(
            grant_path.rstrip("/") + "/"
        )
        if is_ancestor_or_self:
            codes.add(code)

    return codes


def jit_provision_user(
    session: Session,
    organization_id: uuid.UUID,
    sso_subject: str,
    username: str,
    email: str,
    full_name: str,
) -> User:
    """Section 5.4: create a `users` row on first successful login for `(organization_id,
    sso_subject)`, granting DEFAULT_ROLE_CODE org-wide. Subsequent logins update the profile
    fields from the fresh identity claims without touching role grants."""
    user = session.query(User).filter_by(organization_id=organization_id, sso_subject=sso_subject).one_or_none()
    if user is not None:
        user.email = email
        user.full_name = full_name
        return user

    user = User(
        organization_id=organization_id,
        sso_subject=sso_subject,
        username=username,
        email=email,
        full_name=full_name,
    )
    session.add(user)
    session.flush()

    default_role = session.query(Role).filter_by(code=DEFAULT_ROLE_CODE).one()
    session.add(
        UserRole(
            user_id=user.id,
            role_id=default_role.id,
            folder_id=None,
            granted_by=user.id,  # self-granted at JIT provisioning time -- no admin involved yet
        )
    )
    return user


def dev_login(session: Session, organization_id: uuid.UUID, username: str, email: str, full_name: str) -> User:
    """Local-dev auth stub -- trusts the caller's claimed identity outright, with no signature or
    token to verify. `sso_subject` is synthesized from `username` since there's no real ID token
    to read a `sub` claim from yet. Replace with real OIDC/JWT validation once Entra ID access is
    available; `jit_provision_user` itself does not need to change."""
    return jit_provision_user(
        session,
        organization_id=organization_id,
        sso_subject=f"dev:{username}",
        username=username,
        email=email,
        full_name=full_name,
    )
