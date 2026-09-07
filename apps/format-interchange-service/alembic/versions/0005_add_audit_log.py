"""Add audit_log table.

Step 5 of format_interchange_plan.md Sec 7 (hardening for Phase 4): "verify audit-log completeness
for every export/import/migration action." data-platform-api's own `dmp.audit_log` has no write
endpoint an external caller can use (see app/models.py's `AuditLogEntry` docstring), so this
service keeps its own -- one row per completed mutating action.

Revision ID: 0005
Revises: 0004
Create Date: 2026-09-10
"""

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE format_interchange.audit_log (
            id                    uuid PRIMARY KEY,
            organization_id       uuid NOT NULL,
            actor_id              uuid NOT NULL,
            action                text NOT NULL,
            entity_type           text NOT NULL,
            entity_id             uuid,
            result                text NOT NULL DEFAULT 'success',
            detail                jsonb NOT NULL DEFAULT '{}',
            created_at            timestamptz NOT NULL DEFAULT now()
        );

        CREATE INDEX ix_audit_log_org ON format_interchange.audit_log (organization_id, created_at DESC);
        CREATE INDEX ix_audit_log_entity ON format_interchange.audit_log (entity_type, entity_id);
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS format_interchange.audit_log;")
