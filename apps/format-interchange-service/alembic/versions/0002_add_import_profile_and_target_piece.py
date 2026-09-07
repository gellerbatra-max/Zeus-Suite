"""Add import_profile table, interchange_job.target_piece_id, and relax interchange_job.piece_id.

Step 2 of format_interchange_plan.md Sec 7 (IGES import) needs Sec 4's `import_profile` entity
(saved parameter presets) and a place to record which platform piece a staged import committed
to. `piece_id` (0001) was NOT NULL because Step 1 only had export jobs, which always have a
source piece; an import job has no source piece at all, so it must become nullable.
`migration_batch`/`migration_item`/`migration_finding` remain Step 3+ and are not stubbed here,
matching how 0001 only built what Step 1 needed.

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-07
"""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE format_interchange.interchange_job
            ADD COLUMN target_piece_id uuid,
            ALTER COLUMN piece_id DROP NOT NULL;

        CREATE TABLE format_interchange.import_profile (
            id                    uuid PRIMARY KEY,
            organization_id       uuid NOT NULL,
            name                  text NOT NULL,
            trading_partner       text,
            params                jsonb NOT NULL DEFAULT '{}',
            created_by            uuid NOT NULL,
            created_at            timestamptz NOT NULL DEFAULT now()
        );

        CREATE INDEX ix_import_profile_org ON format_interchange.import_profile (organization_id);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS format_interchange.import_profile;
        ALTER TABLE format_interchange.interchange_job DROP COLUMN IF EXISTS target_piece_id;
        """
    )
