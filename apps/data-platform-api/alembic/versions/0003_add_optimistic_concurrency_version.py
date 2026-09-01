"""Add the `version` optimistic-concurrency column Section 4.0 requires on every entity
resource ("a plain integer, incremented on every update... distinct from piece_versions/
marker_versions file-version history", used with the `If-Match-Version` header for 409 Conflict
detection) but Section 2's DDL never actually defines. This is a gap between the API-conventions
section and the schema section of the same source document -- flagged here rather than silently
reinterpreted as e.g. an `updated_at` comparison, since the doc is explicit that it's a separate
integer counter.

Applied to every mutable entity resource exposed through the REST API (Section 4.2-4.6):
folders, pieces, styles, markers, orders, bundles.

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-01
"""

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

TABLES = ["folders", "pieces", "styles", "markers", "orders", "bundles"]


def upgrade() -> None:
    for table in TABLES:
        op.execute(f"ALTER TABLE dmp.{table} ADD COLUMN version integer NOT NULL DEFAULT 1;")


def downgrade() -> None:
    for table in TABLES:
        op.execute(f"ALTER TABLE dmp.{table} DROP COLUMN version;")
