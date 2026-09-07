"""Marker Making Sec 1.6 (block / buffer / fuse-blocking, Gerber depth -- Phase 2 item 5): add
block_buffer_rule_tables and fuse_blocks.

Two new platform-owned tables, same pattern as matching_rule_tables (0006):
  - block_buffer_rule_tables: reusable config, keyed by rule_no per the plan doc ("per-side (L/T/
    R/B) amount, keyed by rule number").
  - fuse_blocks: groups pieces on one marker into a fusing block. x/y/width/height are the tight
    bounding box of the member pieces' current placements -- marker-making-service computes this
    (it interprets placement_data; the platform doesn't) and sends it here as plain numbers. The
    visual block outline (inflated by block_amount) and the block-notch depth
    (block_amount - reduce_amount) are also service/frontend computations, not stored.
  - piece_placement_ids is opaque jsonb (a list of piece_id strings), same opaque-payload
    philosophy as marker_pieces.placement_data -- the platform stores and returns it faithfully.

Scoped to rectangular fuse blocks only this slice (shape is CHECK-constrained to 'rectangle' for
now, forward-compatible with a later 'manual' polygon shape). Create Fusing Marker and Cut Net
Parts are deferred -- both need a cutter_parameter_table, which doesn't exist yet (Sec 1.10 /
Phase 3 territory).

Revision ID: 0009
Revises: 0008
Create Date: 2026-09-07
"""

from alembic import op

revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE dmp.block_buffer_rule_tables (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            name                text NOT NULL,
            rule_no             integer NOT NULL,
            rule_type           text NOT NULL CHECK (rule_type IN ('block','buffer')),
            mode                text NOT NULL CHECK (mode IN ('static','dynamic')),
            left_amt            numeric(8,3) NOT NULL DEFAULT 0,
            top_amt             numeric(8,3) NOT NULL DEFAULT 0,
            right_amt           numeric(8,3) NOT NULL DEFAULT 0,
            bottom_amt          numeric(8,3) NOT NULL DEFAULT 0,
            comment             text,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            version             integer NOT NULL DEFAULT 1,
            UNIQUE (organization_id, rule_no)
        );
        CREATE INDEX idx_block_buffer_rule_tables_org ON dmp.block_buffer_rule_tables(organization_id);

        CREATE TABLE dmp.fuse_blocks (
            id                     uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id        uuid NOT NULL REFERENCES dmp.organizations(id),
            marker_id              uuid NOT NULL REFERENCES dmp.markers(id),
            shape                  text NOT NULL DEFAULT 'rectangle' CHECK (shape IN ('rectangle')),
            x                      numeric(10,3) NOT NULL,
            y                      numeric(10,3) NOT NULL,
            width                  numeric(10,3) NOT NULL,
            height                 numeric(10,3) NOT NULL,
            piece_placement_ids    jsonb NOT NULL DEFAULT '[]'::jsonb,
            block_amount           numeric(8,3) NOT NULL DEFAULT 0.5,
            reduce_amount          numeric(8,3) NOT NULL DEFAULT 0,
            created_by             uuid NOT NULL REFERENCES dmp.users(id),
            created_at             timestamptz NOT NULL DEFAULT now(),
            updated_by             uuid NOT NULL REFERENCES dmp.users(id),
            updated_at             timestamptz NOT NULL DEFAULT now(),
            deleted_at             timestamptz NULL,
            version                integer NOT NULL DEFAULT 1
        );
        CREATE INDEX idx_fuse_blocks_marker ON dmp.fuse_blocks(marker_id);
        """
    )

    # -- Permissions (ids continue from 0006's 53-55, so next free id is 56) --------------------
    op.execute(
        """
        INSERT INTO dmp.permissions (id, code, resource, action, description) VALUES
            (56, 'block_buffer_rule_table.read',   'block_buffer_rule_table', 'read',   'Read a block_buffer_rule_table.'),
            (57, 'block_buffer_rule_table.write',  'block_buffer_rule_table', 'write',  'Write a block_buffer_rule_table.'),
            (58, 'block_buffer_rule_table.delete', 'block_buffer_rule_table', 'delete', 'Delete a block_buffer_rule_table.'),
            (59, 'fuse_block.read',   'fuse_block', 'read',   'Read a fuse_block.'),
            (60, 'fuse_block.write',  'fuse_block', 'write',  'Write a fuse_block.'),
            (61, 'fuse_block.delete', 'fuse_block', 'delete', 'Delete a fuse_block.');

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code = 'admin' AND p.code IN (
            'block_buffer_rule_table.read', 'block_buffer_rule_table.write', 'block_buffer_rule_table.delete',
            'fuse_block.read', 'fuse_block.write', 'fuse_block.delete'
        );

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code = 'marker_maker' AND p.code IN (
            'block_buffer_rule_table.read', 'block_buffer_rule_table.write', 'block_buffer_rule_table.delete',
            'fuse_block.read', 'fuse_block.write', 'fuse_block.delete'
        );

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code IN ('pattern_maker', 'production_planner', 'viewer', 'auditor', 'contractor_qa')
          AND p.code IN ('block_buffer_rule_table.read', 'fuse_block.read');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM dmp.role_permissions WHERE permission_id BETWEEN 56 AND 61;
        DELETE FROM dmp.permissions WHERE id BETWEEN 56 AND 61;
        DROP TABLE dmp.fuse_blocks;
        DROP TABLE dmp.block_buffer_rule_tables;
        """
    )
