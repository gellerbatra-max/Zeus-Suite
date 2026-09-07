"""Initial schema: format_interchange schema, interchange_job table.

Step 1 of format_interchange_plan.md Sec 7 (single-piece IGES export) only needs
`interchange_job` from Sec 4's data model -- import_profile/migration_batch/migration_item/
migration_finding are Step 2+ and are added by later migrations, not stubbed here.

Revision ID: 0001
Revises:
Create Date: 2026-09-07
"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE SCHEMA IF NOT EXISTS format_interchange;
        CREATE EXTENSION IF NOT EXISTS pgcrypto;

        CREATE TABLE format_interchange.interchange_job (
            id                    uuid PRIMARY KEY,
            organization_id       uuid NOT NULL,
            job_type              text NOT NULL,
            piece_id              uuid NOT NULL,
            status                text NOT NULL DEFAULT 'queued',
            params                jsonb NOT NULL DEFAULT '{}',
            object_storage_key    text,
            error_detail          text,
            created_by            uuid NOT NULL,
            created_at            timestamptz NOT NULL DEFAULT now()
        );

        CREATE INDEX ix_interchange_job_org ON format_interchange.interchange_job (organization_id);
        CREATE INDEX ix_interchange_job_piece ON format_interchange.interchange_job (piece_id);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS format_interchange.interchange_job;
        DROP SCHEMA IF EXISTS format_interchange;
        """
    )
