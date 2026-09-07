"""Add the `iges_import` job type Format Interchange's import endpoint submits jobs under
(format_interchange_plan.md Sec 7 Step 2, mirroring 0006's `iges_export`).

`submit_job` (app/job_service.py) resolves `job_type_code` against `dmp.job_types` with
`.filter_by(code=job_type_code).one()` -- there is no dynamic-registration path, so this job type
needs its own migration the same way `iges_export` got one in 0006.

Revision ID: 0007
Revises: 0006
Create Date: 2026-09-07
"""

import sqlalchemy as sa

from alembic import op

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO dmp.job_types (id, code, name, owning_app, default_timeout_seconds, description) "
            "VALUES (3, 'iges_import', 'IGES Piece Import', 'format-interchange', 300, "
            "'Converts one uploaded IGES file into a staged (or immediately committed) pattern "
            "piece for CAD-to-CAD interchange (format_interchange_plan.md Sec 1.2).')"
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM dmp.job_types WHERE code = 'iges_import'"))
