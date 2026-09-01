"""Add pg_trgm GIN indexes on entity code fields for Section 4.8's search contract.

Section 4.8 states free-text search matches "against each entity's search_vector (Postgres FTS)
plus a pg_trgm substring fallback so partial codes still match (e.g. 'PANEL' matches
FRONT-PANEL-01)". Section 2's DDL only ever wires up a trigram index for `folders.path`
(idx_folders_path_trgm) -- no entity code field (piece_code, style_number, marker_code,
order_number, bundle_code) gets one, even though Section 4.8 explicitly describes trigram
fallback behavior for exactly this kind of substring match. This is the same category of gap as
migration 0003 (an API-conventions section promising behavior Section 2's schema doesn't back),
closed the same way: additively, flagged here rather than silently reinterpreted.

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-01
"""

from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None

INDEXES = [
    ("idx_pieces_code_trgm", "pieces", "piece_code"),
    ("idx_styles_number_trgm", "styles", "style_number"),
    ("idx_markers_code_trgm", "markers", "marker_code"),
    ("idx_orders_number_trgm", "orders", "order_number"),
    ("idx_bundles_code_trgm", "bundles", "bundle_code"),
]


def upgrade() -> None:
    for index_name, table, column in INDEXES:
        op.execute(f"CREATE INDEX {index_name} ON dmp.{table} USING gin ({column} gin_trgm_ops);")


def downgrade() -> None:
    for index_name, _table, _column in INDEXES:
        op.execute(f"DROP INDEX dmp.{index_name};")
