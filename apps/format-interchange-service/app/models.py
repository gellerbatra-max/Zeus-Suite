from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID
from sqlalchemy.sql import func

from app.db import Base


class InterchangeJob(Base):
    """One IGES export (or, later, import) operation -- format_interchange_plan.md Sec 4.

    `id` deliberately reuses the platform's own Job id (from `POST /jobs`) as this row's primary
    key, rather than minting a separate local id, per Sec 6's instruction that this service "should
    not invent its own" job-status state machine -- the platform's `Job` row is authoritative for
    status/progress/timeout; this row is this service's own bookkeeping *about* that job (which
    piece, what params, where the result file ended up), joined to it by sharing the same id.
    """

    __tablename__ = "interchange_job"

    id = Column(UUID(as_uuid=True), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), nullable=False)
    job_type = Column(Text, nullable=False)
    piece_id = Column(UUID(as_uuid=True), nullable=False)
    # Authoritative status for THIS service's own bookkeeping, set synchronously in the same
    # request that does the conversion -- see app/api/export.py's module docstring for why this
    # slice doesn't push status through the platform Job's own heartbeat/complete lifecycle
    # (those endpoints are gated on a `job.worker` permission this caller's identity doesn't hold,
    # and provisioning a dedicated per-org worker service-account is out of scope for Step 1).
    status = Column(Text, nullable=False, server_default="queued")
    params = Column(JSONB, nullable=False, server_default="{}")
    object_storage_key = Column(Text, nullable=True)
    error_detail = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
