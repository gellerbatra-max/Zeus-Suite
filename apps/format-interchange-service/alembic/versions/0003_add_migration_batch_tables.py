"""Add migration_batch, migration_item, migration_finding tables.

Step 3 of format_interchange_plan.md Sec 7 (Legacy Migration batch pipeline, classification only)
needs Sec 4's remaining three entities. `migration_item` also gets a `source_storage_key` column
not in Sec 4's own field list -- a pragmatic addition for Step 4's "resolve in-tool and re-run just
this item," which needs the original uploaded bytes back (same category of addition as 0002's
`interchange_job.target_piece_id`).

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-08
"""

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE format_interchange.migration_batch (
            id                    uuid PRIMARY KEY,
            organization_id       uuid NOT NULL,
            source_system         text NOT NULL,
            selection             jsonb NOT NULL DEFAULT '{}',
            status                text NOT NULL DEFAULT 'pending',
            auto_sort_flagged     boolean NOT NULL DEFAULT true,
            chunk_count           integer NOT NULL DEFAULT 1,
            created_by            uuid NOT NULL,
            created_at            timestamptz NOT NULL DEFAULT now()
        );

        CREATE TABLE format_interchange.migration_item (
            id                    uuid PRIMARY KEY,
            batch_id              uuid NOT NULL REFERENCES format_interchange.migration_batch(id),
            source_style_ref      text NOT NULL,
            target_piece_id       uuid,
            status                text NOT NULL DEFAULT 'pending',
            needs_review          boolean NOT NULL DEFAULT false,
            source_storage_key    text,
            converted_geometry    jsonb,
            source_summary        jsonb,
            error_detail          text,
            created_at            timestamptz NOT NULL DEFAULT now()
        );

        CREATE TABLE format_interchange.migration_finding (
            id                    uuid PRIMARY KEY,
            item_id               uuid NOT NULL REFERENCES format_interchange.migration_item(id),
            code                  text NOT NULL,
            severity              text NOT NULL,
            message               text NOT NULL,
            geometry_ref          jsonb NOT NULL DEFAULT '{}',
            resolved_at           timestamptz,
            resolved_by           uuid,
            created_at            timestamptz NOT NULL DEFAULT now()
        );

        CREATE INDEX ix_migration_batch_org ON format_interchange.migration_batch (organization_id);
        CREATE INDEX ix_migration_item_batch ON format_interchange.migration_item (batch_id);
        CREATE INDEX ix_migration_item_status ON format_interchange.migration_item (batch_id, status);
        CREATE INDEX ix_migration_finding_item ON format_interchange.migration_finding (item_id);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DROP TABLE IF EXISTS format_interchange.migration_finding;
        DROP TABLE IF EXISTS format_interchange.migration_item;
        DROP TABLE IF EXISTS format_interchange.migration_batch;
        """
    )
