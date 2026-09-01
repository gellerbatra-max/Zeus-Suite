"""Add `jobs.last_heartbeat_at` for Section 3.7's timeout sweep.

Section 3.7 says a worker's heartbeat call "resets the heartbeat-staleness clock the
Milestone-6-tested timeout sweep watches" -- but Section 2.12's `jobs` table never defines a
column to hold that clock (only `started_at`/`completed_at`/`timeout_at`, none of which are
updated on every heartbeat). Same category of gap as migrations 0003 and 0004: an API/worker
behavior section describing something the schema section doesn't back, closed the same way.

Revision ID: 0005
Revises: 0004
Create Date: 2026-09-01
"""

from alembic import op

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE dmp.jobs ADD COLUMN last_heartbeat_at timestamptz;")


def downgrade() -> None:
    op.execute("ALTER TABLE dmp.jobs DROP COLUMN last_heartbeat_at;")
