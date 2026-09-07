"""Marker Making Sec 1.9 (marker transformations): add orders.shrink_x_pct / shrink_y_pct.

Per the plan doc's own schema sketch (Sec 2, same row that already had target_length/
target_utilization -- see migration 0010's docstring), Shrink and Stretch is "entered on the
order" ("e.g. -25.0 for 25% shrink, +10.0 for 10% stretch on the order; system scales every
placed piece accordingly before cutting") -- an order-level setting, not a one-off marker action,
since the plan intends it to be read at cut-time by the (not-yet-built) cut-data generation step
(Sec 1.10). marker-making-service's app/api/marker_transform.py lets an operator apply it to the
*current* canvas placements today as a stand-in for that not-yet-built cut-time application.

No upper bound CHECK (the doc gives no ceiling on stretch %) -- only a lower bound: -100% would
scale a dimension to exactly zero, which is nonsensical, so reject anything at or below that.

Revision ID: 0011
Revises: 0010
Create Date: 2026-09-07
"""

from alembic import op

revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE dmp.orders
            ADD COLUMN shrink_x_pct numeric(6,2) NULL,
            ADD COLUMN shrink_y_pct numeric(6,2) NULL,
            ADD CONSTRAINT orders_shrink_x_pct_range CHECK (shrink_x_pct IS NULL OR shrink_x_pct > -100),
            ADD CONSTRAINT orders_shrink_y_pct_range CHECK (shrink_y_pct IS NULL OR shrink_y_pct > -100);
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE dmp.orders
            DROP CONSTRAINT orders_shrink_y_pct_range,
            DROP CONSTRAINT orders_shrink_x_pct_range,
            DROP COLUMN shrink_y_pct,
            DROP COLUMN shrink_x_pct;
        """
    )
