"""Add migration_item.legacy_metadata/warning_accepted/block_note.

Step 4 of format_interchange_plan.md Sec 7 (Migration Viewer + triage-and-fix loop) needs somewhere
to persist the per-item state its resolve/block/accept-warning actions mutate:
- `legacy_metadata`: the LegacyMetadata bag last used to classify this item (Sec 2.6 #2: "resolution
  UI mutates the source-side mapping and re-runs conversion for that item only" -- see
  app/migration_checks.py's docstring for why this metadata bag is the source-side mapping in this
  slice, absent a real DXF/AAMA-ASTM parser or grade-rule-table registry).
- `warning_accepted`: Sec 2.6 #3's "explicit accept-as-is before the batch commits."
- `block_note`: Sec 5's "mark blocked with a correction note."

None of these are in Sec 4's own field list, same category of pragmatic addition as 0002's
`interchange_job.target_piece_id` and 0003's `migration_item.source_storage_key`.

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-09
"""

from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE format_interchange.migration_item
            ADD COLUMN legacy_metadata jsonb NOT NULL DEFAULT '{}',
            ADD COLUMN warning_accepted boolean NOT NULL DEFAULT false,
            ADD COLUMN block_note text;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE format_interchange.migration_item
            DROP COLUMN IF EXISTS legacy_metadata,
            DROP COLUMN IF EXISTS warning_accepted,
            DROP COLUMN IF EXISTS block_note;
        """
    )
