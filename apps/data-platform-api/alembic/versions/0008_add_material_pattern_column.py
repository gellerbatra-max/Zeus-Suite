"""Marker Making Sec 1.4: Define Material / Material Pattern -- add
matching_rule_tables.material_pattern_json.

A fabric-pattern reference image loaded onto a matching rule table for visual matching
confirmation, distinct from the geometric stripe definition. Opaque jsonb, same philosophy as the
table's other sub-resource columns: `{name, visible, storage_container, storage_key,
checksum_sha256}` -- the platform stores and returns it faithfully; marker-making-service
interprets the shape and never exposes storage_container/storage_key to its own callers (those are
internal bookkeeping between the begin-upload and complete calls).

Revision ID: 0008
Revises: 0007
Create Date: 2026-09-07
"""

from alembic import op

revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE dmp.matching_rule_tables ADD COLUMN material_pattern_json jsonb;")


def downgrade() -> None:
    op.execute("ALTER TABLE dmp.matching_rule_tables DROP COLUMN material_pattern_json;")
