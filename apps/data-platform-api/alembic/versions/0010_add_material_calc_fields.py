"""Marker Making Sec 1.7 (material calculation / utilization): add orders.target_length /
orders.target_utilization_pct and markers.fabric_weight_per_unit_area.

No new tables and no new permissions this slice -- everything here rides on the existing
`order.write`/`marker.write` permissions already gating `PATCH /orders/{id}` and
`PATCH /markers/{id}`.

Column placement follows the plan doc's own sketch (Sec 2): target length/utilization are
order-level ("set from historical markers of that style", read back into every marker cut
against that order), while fabric_weight_per_unit_area sits on `markers` alongside the other
already-marker-scoped fabric fields (fabric_width, marker_length, ply_count, utilization_pct) --
a marker can use different fabric than its sibling markers on the same order, but a target
length/utilization is set once per order.

`markers.utilization_pct` and `orders.target_utilization_pct` are both percentages with no CHECK
constraint from migration 0001 -- add one now (0-100 inclusive, NULL allowed) since this is the
first time anything actually computes and writes real values into them; the other new/existing
numeric fields (marker_length, ply_count, fabric_weight_per_unit_area, target_length) stay
unconstrained at the DB level, consistent with fabric_width's own precedent of no non-negativity
check.

Revision ID: 0010
Revises: 0009
Create Date: 2026-09-07
"""

from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE dmp.orders
            ADD COLUMN target_length numeric(10,2) NULL,
            ADD COLUMN target_utilization_pct numeric(5,2) NULL,
            ADD CONSTRAINT orders_target_utilization_pct_range
                CHECK (target_utilization_pct IS NULL OR (target_utilization_pct >= 0 AND target_utilization_pct <= 100));

        ALTER TABLE dmp.markers
            ADD COLUMN fabric_weight_per_unit_area numeric(10,4) NULL,
            ADD CONSTRAINT markers_utilization_pct_range
                CHECK (utilization_pct IS NULL OR (utilization_pct >= 0 AND utilization_pct <= 100));
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE dmp.markers
            DROP CONSTRAINT markers_utilization_pct_range,
            DROP COLUMN fabric_weight_per_unit_area;

        ALTER TABLE dmp.orders
            DROP CONSTRAINT orders_target_utilization_pct_range,
            DROP COLUMN target_utilization_pct,
            DROP COLUMN target_length;
        """
    )
