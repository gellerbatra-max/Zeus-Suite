"""Initial schema: dmp schema, extensions, all Section 2 tables/indexes/triggers.

Transcribed directly from docs/planning/01_data_management_platform/data_management_platform_plan.md
Section 2, reordered only where the document itself calls out a forward-reference (folders must
exist before user_roles' folder_id FK; piece_versions/marker_versions/orders must exist before the
current_version_id / order_id FKs on pieces/markers can be added).

Revision ID: 0001
Revises:
Create Date: 2026-09-01
"""

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE SCHEMA IF NOT EXISTS dmp;
        CREATE EXTENSION IF NOT EXISTS pgcrypto;
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        SET search_path TO dmp, public;
        """
    )

    # -- 2.1 Identity and organization -----------------------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.organizations (
            id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            name            text NOT NULL,
            code            text NOT NULL UNIQUE,
            is_active       boolean NOT NULL DEFAULT true,
            created_at      timestamptz NOT NULL DEFAULT now(),
            updated_at      timestamptz NOT NULL DEFAULT now()
        );

        CREATE TABLE dmp.users (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            sso_subject         text NOT NULL,
            username            text NOT NULL,
            email               text NOT NULL,
            full_name           text NOT NULL,
            status              text NOT NULL DEFAULT 'active'
                                    CHECK (status IN ('active','suspended','deprovisioned')),
            last_login_at       timestamptz,
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            UNIQUE (organization_id, sso_subject),
            UNIQUE (organization_id, username)
        );

        CREATE TABLE dmp.service_accounts (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id             uuid NOT NULL UNIQUE REFERENCES dmp.users(id),
            client_id           text NOT NULL UNIQUE,
            description         text NOT NULL,
            is_active           boolean NOT NULL DEFAULT true,
            created_at          timestamptz NOT NULL DEFAULT now()
        );

        CREATE TABLE dmp.roles (
            id              smallint PRIMARY KEY,
            code            text NOT NULL UNIQUE,
            name            text NOT NULL,
            description     text NOT NULL
        );

        CREATE TABLE dmp.permissions (
            id              smallint PRIMARY KEY,
            code            text NOT NULL UNIQUE,
            resource        text NOT NULL,
            action          text NOT NULL,
            description     text NOT NULL
        );

        CREATE TABLE dmp.role_permissions (
            role_id         smallint NOT NULL REFERENCES dmp.roles(id),
            permission_id   smallint NOT NULL REFERENCES dmp.permissions(id),
            PRIMARY KEY (role_id, permission_id)
        );
        """
    )

    # -- 2.2 Virtual folder tree (declared before user_roles, per the doc's own note) ------
    op.execute(
        """
        CREATE TABLE dmp.folders (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            parent_id           uuid NULL REFERENCES dmp.folders(id),
            name                text NOT NULL,
            path                text NOT NULL,
            folder_type         text NOT NULL DEFAULT 'general'
                                    CHECK (folder_type IN ('general','customer','season','style_group','archive')),
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            UNIQUE (organization_id, parent_id, name),
            UNIQUE (organization_id, path)
        );
        CREATE INDEX idx_folders_parent ON dmp.folders(parent_id);
        CREATE INDEX idx_folders_path_trgm ON dmp.folders USING gin (path gin_trgm_ops);

        CREATE TABLE dmp.user_roles (
            id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id         uuid NOT NULL REFERENCES dmp.users(id),
            role_id         smallint NOT NULL REFERENCES dmp.roles(id),
            folder_id       uuid NULL REFERENCES dmp.folders(id),
            granted_by      uuid NOT NULL REFERENCES dmp.users(id),
            granted_at      timestamptz NOT NULL DEFAULT now(),
            UNIQUE (user_id, role_id, folder_id)
        );
        """
    )

    # -- 2.3 Workflow status (shared state machine) ----------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.workflow_statuses (
            id              smallint PRIMARY KEY,
            entity_type     text NOT NULL
                                CHECK (entity_type IN ('piece','style','marker','order','bundle')),
            code            text NOT NULL,
            label           text NOT NULL,
            sequence        smallint NOT NULL,
            is_terminal     boolean NOT NULL DEFAULT false,
            is_initial      boolean NOT NULL DEFAULT false,
            UNIQUE (entity_type, code)
        );

        CREATE TABLE dmp.workflow_transitions (
            id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            entity_type             text NOT NULL,
            from_status_id          smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            to_status_id            smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            required_permission     text NOT NULL,
            UNIQUE (entity_type, from_status_id, to_status_id)
        );
        """
    )

    # -- 2.4 Pieces -------------------------------------------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.pieces (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            folder_id           uuid NOT NULL REFERENCES dmp.folders(id),
            piece_code          text NOT NULL,
            piece_name          text NOT NULL,
            piece_type          text NOT NULL DEFAULT 'pattern'
                                    CHECK (piece_type IN ('pattern','block','digitized_raw')),
            description         text,
            base_size           text,
            current_version_id  uuid NULL,
            workflow_status_id  smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            lock_owner_id        uuid NULL REFERENCES dmp.users(id),
            lock_acquired_at      timestamptz NULL,
            search_vector        tsvector,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            UNIQUE (organization_id, folder_id, piece_code)
        );
        CREATE INDEX idx_pieces_folder ON dmp.pieces(folder_id);
        CREATE INDEX idx_pieces_status ON dmp.pieces(workflow_status_id);
        CREATE INDEX idx_pieces_search ON dmp.pieces USING gin (search_vector);
        CREATE TRIGGER trg_pieces_search_vector
            BEFORE INSERT OR UPDATE ON dmp.pieces
            FOR EACH ROW EXECUTE FUNCTION
            tsvector_update_trigger(search_vector, 'pg_catalog.english', piece_code, piece_name, description);

        CREATE TABLE dmp.piece_versions (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            piece_id            uuid NOT NULL REFERENCES dmp.pieces(id),
            version_number      integer NOT NULL,
            storage_container   text NOT NULL,
            storage_key         text NOT NULL,
            file_format         text NOT NULL DEFAULT 'native'
                                    CHECK (file_format IN ('native','dxf_aama','dxf_asdf','iges')),
            checksum_sha256     text NOT NULL,
            size_bytes          bigint NOT NULL,
            comment             text,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            UNIQUE (piece_id, version_number)
        );
        CREATE INDEX idx_piece_versions_piece ON dmp.piece_versions(piece_id);

        ALTER TABLE dmp.pieces
            ADD CONSTRAINT fk_pieces_current_version
            FOREIGN KEY (current_version_id) REFERENCES dmp.piece_versions(id);
        """
    )

    # -- 2.5 Styles (and the piece cross-reference) -----------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.styles (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            folder_id           uuid NOT NULL REFERENCES dmp.folders(id),
            style_number        text NOT NULL,
            style_name          text NOT NULL,
            season              text,
            customer            text,
            description         text,
            workflow_status_id  smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            search_vector        tsvector,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            UNIQUE (organization_id, folder_id, style_number)
        );
        CREATE INDEX idx_styles_folder ON dmp.styles(folder_id);
        CREATE INDEX idx_styles_search ON dmp.styles USING gin (search_vector);
        CREATE TRIGGER trg_styles_search_vector
            BEFORE INSERT OR UPDATE ON dmp.styles
            FOR EACH ROW EXECUTE FUNCTION
            tsvector_update_trigger(search_vector, 'pg_catalog.english', style_number, style_name, customer, description);

        CREATE TABLE dmp.style_pieces (
            id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            style_id        uuid NOT NULL REFERENCES dmp.styles(id),
            piece_id        uuid NOT NULL REFERENCES dmp.pieces(id),
            piece_role      text NOT NULL DEFAULT 'primary'
                                CHECK (piece_role IN ('primary','paste','lining','interfacing')),
            sequence        integer NOT NULL DEFAULT 0,
            added_by        uuid NOT NULL REFERENCES dmp.users(id),
            added_at        timestamptz NOT NULL DEFAULT now(),
            UNIQUE (style_id, piece_id)
        );
        CREATE INDEX idx_style_pieces_style ON dmp.style_pieces(style_id);
        CREATE INDEX idx_style_pieces_piece ON dmp.style_pieces(piece_id);
        """
    )

    # -- 2.6 Markers (and the marker/piece cross-reference) ---------------------------------
    op.execute(
        """
        CREATE TABLE dmp.markers (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            folder_id           uuid NOT NULL REFERENCES dmp.folders(id),
            marker_code         text NOT NULL,
            marker_name         text NOT NULL,
            order_id            uuid NULL,
            fabric_width        numeric(8,2),
            marker_length        numeric(10,2),
            ply_count           integer,
            utilization_pct     numeric(5,2),
            matching_method     text CHECK (matching_method IN (NULL,'none','standard','five_star')),
            current_version_id  uuid NULL,
            workflow_status_id  smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            search_vector        tsvector,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            UNIQUE (organization_id, folder_id, marker_code)
        );
        CREATE INDEX idx_markers_folder ON dmp.markers(folder_id);
        CREATE INDEX idx_markers_order ON dmp.markers(order_id);
        CREATE INDEX idx_markers_status ON dmp.markers(workflow_status_id);
        CREATE INDEX idx_markers_search ON dmp.markers USING gin (search_vector);
        CREATE TRIGGER trg_markers_search_vector
            BEFORE INSERT OR UPDATE ON dmp.markers
            FOR EACH ROW EXECUTE FUNCTION
            tsvector_update_trigger(search_vector, 'pg_catalog.english', marker_code, marker_name);

        CREATE TABLE dmp.marker_versions (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            marker_id           uuid NOT NULL REFERENCES dmp.markers(id),
            version_number      integer NOT NULL,
            storage_container   text NOT NULL,
            storage_key         text NOT NULL,
            file_format         text NOT NULL DEFAULT 'native'
                                    CHECK (file_format IN ('native','cut_data','plot_file','dxf_aama')),
            checksum_sha256     text NOT NULL,
            size_bytes          bigint NOT NULL,
            comment             text,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            UNIQUE (marker_id, version_number)
        );
        CREATE INDEX idx_marker_versions_marker ON dmp.marker_versions(marker_id);

        ALTER TABLE dmp.markers
            ADD CONSTRAINT fk_markers_current_version
            FOREIGN KEY (current_version_id) REFERENCES dmp.marker_versions(id);

        CREATE TABLE dmp.marker_pieces (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            marker_id           uuid NOT NULL REFERENCES dmp.markers(id),
            piece_id            uuid NOT NULL REFERENCES dmp.pieces(id),
            piece_version_id    uuid NOT NULL REFERENCES dmp.piece_versions(id),
            size_code           text NOT NULL,
            quantity             integer NOT NULL CHECK (quantity > 0),
            placement_data       jsonb,
            created_at          timestamptz NOT NULL DEFAULT now()
        );
        CREATE INDEX idx_marker_pieces_marker ON dmp.marker_pieces(marker_id);
        CREATE INDEX idx_marker_pieces_piece ON dmp.marker_pieces(piece_id);
        """
    )

    # -- 2.7 Orders --------------------------------------------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.orders (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            folder_id           uuid NOT NULL REFERENCES dmp.folders(id),
            order_number        text NOT NULL,
            style_id            uuid NOT NULL REFERENCES dmp.styles(id),
            customer            text,
            due_date            date,
            total_quantity      integer NOT NULL DEFAULT 0,
            workflow_status_id  smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            search_vector        tsvector,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            deleted_at          timestamptz NULL,
            UNIQUE (organization_id, folder_id, order_number)
        );
        CREATE INDEX idx_orders_folder ON dmp.orders(folder_id);
        CREATE INDEX idx_orders_style ON dmp.orders(style_id);
        CREATE INDEX idx_orders_search ON dmp.orders USING gin (search_vector);
        CREATE TRIGGER trg_orders_search_vector
            BEFORE INSERT OR UPDATE ON dmp.orders
            FOR EACH ROW EXECUTE FUNCTION
            tsvector_update_trigger(search_vector, 'pg_catalog.english', order_number, customer);

        ALTER TABLE dmp.markers
            ADD CONSTRAINT fk_markers_order
            FOREIGN KEY (order_id) REFERENCES dmp.orders(id);

        CREATE TABLE dmp.order_lines (
            id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            order_id        uuid NOT NULL REFERENCES dmp.orders(id),
            size_code       text NOT NULL,
            color           text,
            quantity         integer NOT NULL CHECK (quantity > 0),
            marker_id       uuid NULL REFERENCES dmp.markers(id),
            created_at      timestamptz NOT NULL DEFAULT now(),
            UNIQUE (order_id, size_code, color)
        );
        CREATE INDEX idx_order_lines_order ON dmp.order_lines(order_id);
        CREATE INDEX idx_order_lines_marker ON dmp.order_lines(marker_id);
        """
    )

    # -- 2.8 Bundles ---------------------------------------------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.bundles (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            order_id            uuid NOT NULL REFERENCES dmp.orders(id),
            marker_id           uuid NOT NULL REFERENCES dmp.markers(id),
            piece_id            uuid NOT NULL REFERENCES dmp.pieces(id),
            bundle_code         text NOT NULL,
            rfid_tag            text UNIQUE,
            qr_code             text UNIQUE,
            size_code           text NOT NULL,
            color               text,
            ply_range_start     integer,
            ply_range_end       integer,
            quantity             integer NOT NULL CHECK (quantity > 0),
            workflow_status_id  smallint NOT NULL REFERENCES dmp.workflow_statuses(id),
            cut_at              timestamptz,
            created_by          uuid NOT NULL REFERENCES dmp.users(id),
            created_at          timestamptz NOT NULL DEFAULT now(),
            updated_by          uuid NOT NULL REFERENCES dmp.users(id),
            updated_at          timestamptz NOT NULL DEFAULT now(),
            UNIQUE (organization_id, bundle_code)
        );
        CREATE INDEX idx_bundles_order ON dmp.bundles(order_id);
        CREATE INDEX idx_bundles_marker ON dmp.bundles(marker_id);
        CREATE INDEX idx_bundles_piece ON dmp.bundles(piece_id);
        CREATE INDEX idx_bundles_rfid ON dmp.bundles(rfid_tag);
        CREATE INDEX idx_bundles_qr ON dmp.bundles(qr_code);
        """
    )

    # -- 2.9 Audit log -------------------------------------------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.audit_log (
            id              bigserial PRIMARY KEY,
            occurred_at     timestamptz NOT NULL DEFAULT now(),
            organization_id uuid NOT NULL REFERENCES dmp.organizations(id),
            user_id         uuid NULL REFERENCES dmp.users(id),
            action          text NOT NULL,
            entity_type     text NOT NULL,
            entity_id       uuid NULL,
            folder_id       uuid NULL REFERENCES dmp.folders(id),
            before_state    jsonb,
            after_state     jsonb,
            request_id      uuid NOT NULL,
            client_app      text,
            ip_address      inet,
            result          text NOT NULL CHECK (result IN ('success','denied','error')),
            detail          text
        );
        CREATE INDEX idx_audit_log_entity ON dmp.audit_log(entity_type, entity_id);
        CREATE INDEX idx_audit_log_user ON dmp.audit_log(user_id);
        CREATE INDEX idx_audit_log_occurred ON dmp.audit_log(occurred_at);
        CREATE INDEX idx_audit_log_org_time ON dmp.audit_log(organization_id, occurred_at);
        """
    )

    # -- 2.10 Reporting support ------------------------------------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.report_definitions (
            id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            code            text NOT NULL UNIQUE,
            name            text NOT NULL,
            entity_type     text NOT NULL,
            description     text
        );

        CREATE TABLE dmp.report_runs (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            report_definition_id uuid NOT NULL REFERENCES dmp.report_definitions(id),
            requested_by        uuid NOT NULL REFERENCES dmp.users(id),
            parameters          jsonb NOT NULL,
            status               text NOT NULL DEFAULT 'pending'
                                    CHECK (status IN ('pending','running','completed','failed')),
            result_storage_key   text,
            result_inline        jsonb,
            requested_at         timestamptz NOT NULL DEFAULT now(),
            completed_at         timestamptz
        );
        CREATE INDEX idx_report_runs_definition ON dmp.report_runs(report_definition_id);
        CREATE INDEX idx_report_runs_requested_by ON dmp.report_runs(requested_by);
        """
    )

    # -- 2.12 Long-running jobs (generic async job pattern) --------------------------------------
    op.execute(
        """
        CREATE TABLE dmp.job_types (
            id                          smallint PRIMARY KEY,
            code                        text NOT NULL UNIQUE,
            name                        text NOT NULL,
            owning_app                  text NOT NULL,
            default_timeout_seconds     integer NOT NULL DEFAULT 3600,
            description                 text
        );

        CREATE TABLE dmp.jobs (
            id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            organization_id     uuid NOT NULL REFERENCES dmp.organizations(id),
            job_type_id         smallint NOT NULL REFERENCES dmp.job_types(id),
            status              text NOT NULL DEFAULT 'queued'
                                    CHECK (status IN ('queued','running','succeeded','failed','cancelled')),
            submitted_by        uuid NOT NULL REFERENCES dmp.users(id),
            input_ref           jsonb NOT NULL,
            result_ref          jsonb,
            progress_pct        numeric(5,2),
            error_detail        text,
            queue_message_id    text,
            worker_instance     text,
            callback_url        text,
            submitted_at        timestamptz NOT NULL DEFAULT now(),
            started_at          timestamptz,
            completed_at         timestamptz,
            timeout_at            timestamptz
        );
        CREATE INDEX idx_jobs_status ON dmp.jobs(status);
        CREATE INDEX idx_jobs_type ON dmp.jobs(job_type_id);
        CREATE INDEX idx_jobs_submitted_by ON dmp.jobs(submitted_by);

        CREATE TABLE dmp.job_events (
            id          bigserial PRIMARY KEY,
            job_id      uuid NOT NULL REFERENCES dmp.jobs(id),
            occurred_at timestamptz NOT NULL DEFAULT now(),
            event_type  text NOT NULL CHECK (event_type IN
                            ('queued','picked_up','progress','succeeded','failed','retried','cancelled','timed_out')),
            detail      jsonb
        );
        CREATE INDEX idx_job_events_job ON dmp.job_events(job_id);
        """
    )


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS dmp CASCADE;")
