"""Marker Making Phase 2 Slice 2 (marker_making_production_plan.md Sec 1.4): matching_rule_tables
+ markers.matching_rule_table_id.

Confirmed architectural decision (not a schema-minimalism call like Slice 1's): the platform owns
matching_rule_table per marker_making_production_plan.md Sec 2, which explicitly lists this table
living in the platform's Postgres, reached only via its REST API. offsets_json /
stripe_definitions_json / stripe_marks_json are opaque jsonb -- this service stores and returns
them faithfully; structural validation (offset count caps, stripe-mark id generation, etc.) lives
in marker-making-service, per the same opaque-payload philosophy as marker_pieces.placement_data.

Revision ID: 0006
Revises: 0005
Create Date: 2026-09-01
"""

from alembic import op

revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE dmp.matching_rule_tables (
            id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id         uuid NOT NULL REFERENCES dmp.organizations(id),
            name                    text NOT NULL,
            method                  text NOT NULL CHECK (method IN ('standard','five_star')),
            plaid_repeat            numeric(10,4),
            stripe_repeat           numeric(10,4),
            offsets_json            jsonb,
            stripe_definitions_json jsonb NOT NULL DEFAULT '[]'::jsonb,
            stripe_marks_json       jsonb NOT NULL DEFAULT '[]'::jsonb,
            comment                 text,
            created_by              uuid NOT NULL REFERENCES dmp.users(id),
            created_at              timestamptz NOT NULL DEFAULT now(),
            updated_by              uuid NOT NULL REFERENCES dmp.users(id),
            updated_at              timestamptz NOT NULL DEFAULT now(),
            deleted_at              timestamptz NULL,
            version                 integer NOT NULL DEFAULT 1,
            UNIQUE (organization_id, name)
        );
        CREATE INDEX idx_matching_rule_tables_org ON dmp.matching_rule_tables(organization_id);

        ALTER TABLE dmp.markers ADD COLUMN matching_rule_table_id uuid NULL
            REFERENCES dmp.matching_rule_tables(id);
        CREATE INDEX idx_markers_matching_rule_table ON dmp.markers(matching_rule_table_id);
        """
    )

    # -- Permissions (ids continue from 0002's generated catalogue, whose max id is 52) ---------
    op.execute(
        """
        INSERT INTO dmp.permissions (id, code, resource, action, description) VALUES
            (53, 'matching_rule_table.read',   'matching_rule_table', 'read',   'Read a matching_rule_table.'),
            (54, 'matching_rule_table.write',  'matching_rule_table', 'write',  'Write a matching_rule_table.'),
            (55, 'matching_rule_table.delete', 'matching_rule_table', 'delete', 'Delete a matching_rule_table.');

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code = 'admin' AND p.code LIKE 'matching_rule_table.%';

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code = 'marker_maker' AND p.code LIKE 'matching_rule_table.%';

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code IN ('pattern_maker', 'production_planner', 'viewer', 'auditor', 'contractor_qa')
          AND p.code = 'matching_rule_table.read';
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM dmp.role_permissions WHERE permission_id IN (53, 54, 55);
        DELETE FROM dmp.permissions WHERE id IN (53, 54, 55);
        ALTER TABLE dmp.markers DROP COLUMN matching_rule_table_id;
        DROP TABLE dmp.matching_rule_tables;
        """
    )
