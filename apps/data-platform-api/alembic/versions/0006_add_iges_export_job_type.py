"""Add the `iges_export` job type Format Interchange's export endpoint submits jobs under
(format_interchange_plan.md Sec 6: "both single-piece conversions and batch migrations run through
the platform's standard job-queue pattern -- this service should not invent its own").

`submit_job` (app/job_service.py) resolves `job_type_code` against `dmp.job_types` with
`.filter_by(code=job_type_code).one()` -- there is no dynamic-registration path, so a new job type
needs a migration the same way `marker_nesting_solve` got one in 0002.

Revision ID: 0006
Revises: 0005
Create Date: 2026-09-07
"""

import sqlalchemy as sa

from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO dmp.job_types (id, code, name, owning_app, default_timeout_seconds, description) "
            "VALUES (2, 'iges_export', 'IGES Piece Export', 'format-interchange', 300, "
            "'Converts one pattern piece''s geometry to an IGES file for CAD-to-CAD interchange "
            "(format_interchange_plan.md Sec 1.1).')"
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM dmp.job_types WHERE code = 'iges_export'"))
