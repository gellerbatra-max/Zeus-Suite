"""Marker Making Sec 1.5 (layrules automation): add dmp.layrule_search_tables,
dmp.layrules, and markers.force_layrule_name / layrule_search_table_id.

Layrules are still supporting mechanics for Engine A replay ("Layrule Replay"), which itself
remains a stub (Milestone 6's marker_nesting_solve is sleep-and-echo) -- but this slice makes the
concept concretely useful without a real nesting engine: a `layrule` is a captured *snapshot* of
one marker's placements (`placements_json`, the same shape `GET /markers/{id}/pieces` already
returns -- opaque to this platform, same philosophy as everywhere else), reusable on a *different*
marker that shares compatible pieces. That's the real value the plan describes ("best suited to
repeat orders with the same models/sizes... minor differences only") even without automatic
placement -- marker-making-service's apply step does the real work of matching pieces and running
the search-criteria checks below.

`dmp.layrule_search_tables` models "Layrule Search Parameter Table" [GOE] -- the Yes/No criteria
list (`area_compare`, `area_deviation_pct`, `copy_dynamics`, `allow_overrides`,
`include_marker_name`, `include_marker_description`) a marker can opt into via the new
`markers.layrule_search_table_id` FK. `markers.force_layrule_name` is the other half of "To order
a marker with layrules" -- the plan's two mutually-exclusive naming strategies (name-match vs.
search-criteria) are both just marker-level fields here rather than gated by a company-wide
setting; the org-wide naming-strategy/Auto-Store toggle from "Settings/Splice"'s Layrules
equivalent is deferred (see marker-making-service's README) -- there's no organizations settings
API anywhere in this platform yet to hang it on, and neither naming mode needs it to function.

Revision ID: 0013
Revises: 0012
Create Date: 2026-09-07
"""

from alembic import op

revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE dmp.layrule_search_tables (
            id                          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id             uuid NOT NULL REFERENCES dmp.organizations(id),
            name                        text NOT NULL,
            area_compare                boolean NOT NULL DEFAULT true,
            area_deviation_pct          numeric(5,2) NOT NULL DEFAULT 5.0,
            copy_dynamics               boolean NOT NULL DEFAULT true,
            allow_overrides             boolean NOT NULL DEFAULT true,
            include_marker_name         boolean NOT NULL DEFAULT true,
            include_marker_description  boolean NOT NULL DEFAULT false,
            comment                     text,
            created_by                  uuid NOT NULL REFERENCES dmp.users(id),
            created_at                  timestamptz NOT NULL DEFAULT now(),
            updated_by                  uuid NOT NULL REFERENCES dmp.users(id),
            updated_at                  timestamptz NOT NULL DEFAULT now(),
            deleted_at                  timestamptz NULL,
            version                     integer NOT NULL DEFAULT 1,
            UNIQUE (organization_id, name)
        );
        CREATE INDEX idx_layrule_search_tables_org ON dmp.layrule_search_tables(organization_id);

        CREATE TABLE dmp.layrules (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            name                text NOT NULL,
            source_marker_id    uuid NOT NULL REFERENCES dmp.markers(id),
            placements_json     jsonb NOT NULL DEFAULT '[]'::jsonb,
            piece_count         integer NOT NULL DEFAULT 0,
            comment             text,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            version             integer NOT NULL DEFAULT 1,
            UNIQUE (organization_id, name)
        );
        CREATE INDEX idx_layrules_org ON dmp.layrules(organization_id);

        ALTER TABLE dmp.markers
            ADD COLUMN force_layrule_name text NULL,
            ADD COLUMN layrule_search_table_id uuid NULL REFERENCES dmp.layrule_search_tables(id);
        CREATE INDEX idx_markers_layrule_search_table ON dmp.markers(layrule_search_table_id);
        """
    )

    # -- Permissions (ids continue from 0012's 62-64, so next free id is 65) --------------------
    op.execute(
        """
        INSERT INTO dmp.permissions (id, code, resource, action, description) VALUES
            (65, 'layrule_search_table.read',   'layrule_search_table', 'read',   'Read a layrule_search_table.'),
            (66, 'layrule_search_table.write',  'layrule_search_table', 'write',  'Write a layrule_search_table.'),
            (67, 'layrule_search_table.delete', 'layrule_search_table', 'delete', 'Delete a layrule_search_table.'),
            (68, 'layrule.read',   'layrule', 'read',   'Read a layrule.'),
            (69, 'layrule.write',  'layrule', 'write',  'Write a layrule.'),
            (70, 'layrule.delete', 'layrule', 'delete', 'Delete a layrule.');

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code = 'admin' AND p.code IN (
            'layrule_search_table.read', 'layrule_search_table.write', 'layrule_search_table.delete',
            'layrule.read', 'layrule.write', 'layrule.delete'
        );

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code = 'marker_maker' AND p.code IN (
            'layrule_search_table.read', 'layrule_search_table.write', 'layrule_search_table.delete',
            'layrule.read', 'layrule.write', 'layrule.delete'
        );

        INSERT INTO dmp.role_permissions (role_id, permission_id)
        SELECT r.id, p.id FROM dmp.roles r, dmp.permissions p
        WHERE r.code IN ('pattern_maker', 'production_planner', 'viewer', 'auditor', 'contractor_qa')
          AND p.code IN ('layrule_search_table.read', 'layrule.read');
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM dmp.role_permissions WHERE permission_id BETWEEN 65 AND 70;
        DELETE FROM dmp.permissions WHERE id BETWEEN 65 AND 70;
        ALTER TABLE dmp.markers
            DROP COLUMN layrule_search_table_id,
            DROP COLUMN force_layrule_name;
        DROP TABLE dmp.layrules;
        DROP TABLE dmp.layrule_search_tables;
        """
    )
