"""Marker Making Sec 1.4: weave-line tools -- add matching_rule_tables.weave_line_json.

Global reference-line settings (angle, perpendicular offset, visibility) used for matching
alignment ("Edit Weave Line of All pieces", "Show/hide weave line" per the plan doc). Opaque
jsonb, same philosophy as offsets_json/stripe_definitions_json/stripe_marks_json -- the platform
stores and returns it faithfully; marker-making-service interprets the shape.

Revision ID: 0007
Revises: 0006
Create Date: 2026-09-05
"""

from alembic import op

revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE dmp.matching_rule_tables ADD COLUMN weave_line_json jsonb;")


def downgrade() -> None:
    op.execute("ALTER TABLE dmp.matching_rule_tables DROP COLUMN weave_line_json;")
