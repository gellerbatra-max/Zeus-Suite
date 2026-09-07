"""Add the `legacy_migration_batch` job type Format Interchange's migration-batch endpoint submits
jobs under (format_interchange_plan.md Sec 7 Step 3, mirroring 0006/0007's `iges_export`/
`iges_import`).

Revision ID: 0008
Revises: 0007
Create Date: 2026-09-08
"""

import sqlalchemy as sa

from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO dmp.job_types (id, code, name, owning_app, default_timeout_seconds, description) "
            "VALUES (4, 'legacy_migration_batch', 'Legacy Migration Batch', 'format-interchange', 1800, "
            "'Converts and classifies a batch of legacy-format style files "
            "(format_interchange_plan.md Sec 2).')"
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM dmp.job_types WHERE code = 'legacy_migration_batch'"))
