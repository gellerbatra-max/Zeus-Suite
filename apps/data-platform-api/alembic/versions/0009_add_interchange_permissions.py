"""Add the `interchange.export`/`interchange.import`/`interchange.migrate`/`interchange.review`
permissions format_interchange_plan.md Sec 5 names ("enforce RBAC roles (interchange:export,
interchange:import, interchange:migrate, interchange:review) at the API layer"), for Sec 7 Step 5
hardening.

Unlike every other permission code in 0002's seed data, these aren't checked by THIS service --
format-interchange-service checks them itself (see its own app/permissions.py for why: it's the
first service in the suite with local state and endpoints that never call a platform endpoint at
all, so there's no transitive `require_permission` check to lean on the way every other thin
client gets for free). They still belong in the platform's own registry, the single source of
truth for what a role grants, exactly like every other permission code.

Granted to `admin` (all four, matching that role's existing "every permission" grant) and to
`viewer`/`auditor` (`interchange.review` only, matching their existing read-oriented grants).

Revision ID: 0009
Revises: 0008
Create Date: 2026-09-10
"""

import sqlalchemy as sa

from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None

NEW_PERMISSIONS = [
    ("interchange.export", "interchange", "export", "Submit or check status of a single-piece IGES export."),
    (
        "interchange.import", "interchange", "import",
        "Submit, check status, commit, or manage saved presets for a single-piece IGES import.",
    ),
    ("interchange.migrate", "interchange", "migrate", "Create, run, or commit a Legacy Migration batch."),
    (
        "interchange.review", "interchange", "review",
        "View and triage (resolve/block/accept-warning) Legacy Migration batch items.",
    ),
]

ROLE_GRANTS = {
    "admin": ["interchange.export", "interchange.import", "interchange.migrate", "interchange.review"],
    "viewer": ["interchange.review"],
    "auditor": ["interchange.review"],
}


def upgrade() -> None:
    conn = op.get_bind()

    next_id = conn.execute(sa.text("SELECT COALESCE(MAX(id), 0) + 1 FROM dmp.permissions")).scalar()
    permission_id_by_code = {}
    for i, (code, resource, action, description) in enumerate(NEW_PERMISSIONS):
        permission_id_by_code[code] = next_id + i
        conn.execute(
            sa.text(
                "INSERT INTO dmp.permissions (id, code, resource, action, description) "
                "VALUES (:id, :code, :resource, :action, :description)"
            ),
            {"id": next_id + i, "code": code, "resource": resource, "action": action, "description": description},
        )

    for role_code, perm_codes in ROLE_GRANTS.items():
        role_id = conn.execute(sa.text("SELECT id FROM dmp.roles WHERE code = :code"), {"code": role_code}).scalar()
        conn.execute(
            sa.text("INSERT INTO dmp.role_permissions (role_id, permission_id) VALUES (:role_id, :permission_id)"),
            [{"role_id": role_id, "permission_id": permission_id_by_code[code]} for code in perm_codes],
        )


def downgrade() -> None:
    conn = op.get_bind()
    codes = [c for c, *_ in NEW_PERMISSIONS]
    conn.execute(
        sa.text("DELETE FROM dmp.role_permissions WHERE permission_id IN (SELECT id FROM dmp.permissions WHERE code = ANY(:codes))"),
        {"codes": codes},
    )
    conn.execute(sa.text("DELETE FROM dmp.permissions WHERE code = ANY(:codes)"), {"codes": codes})
