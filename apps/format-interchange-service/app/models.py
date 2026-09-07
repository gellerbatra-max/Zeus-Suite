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
    # Nullable as of Step 2: an export job's *source* piece; an import job has no source piece at
    # all (the piece is the output, tracked via `target_piece_id` below once committed).
    piece_id = Column(UUID(as_uuid=True), nullable=True)
    # Authoritative status for THIS service's own bookkeeping, set synchronously in the same
    # request that does the conversion -- see app/api/export.py's module docstring for why this
    # slice doesn't push status through the platform Job's own heartbeat/complete lifecycle
    # (those endpoints are gated on a `job.worker` permission this caller's identity doesn't hold,
    # and provisioning a dedicated per-org worker service-account is out of scope for Step 1).
    status = Column(Text, nullable=False, server_default="queued")
    params = Column(JSONB, nullable=False, server_default="{}")
    object_storage_key = Column(Text, nullable=True)
    # Import-only (Step 2): set once a staged import is committed to the platform -- null for
    # export jobs, and null for import jobs still staged/pending review.
    target_piece_id = Column(UUID(as_uuid=True), nullable=True)
    error_detail = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class ImportProfile(Base):
    """A saved import parameter preset per trading partner (Sec 1.3, replacing `IGES.INI`) --
    `params` holds the same option set `ImportIgesOptions` (app/import_pipeline.py) accepts on
    `POST /import/iges`, so a caller can pass `import_profile_id` instead of repeating every field."""

    __tablename__ = "import_profile"

    id = Column(UUID(as_uuid=True), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), nullable=False)
    name = Column(Text, nullable=False)
    trading_partner = Column(Text, nullable=True)
    params = Column(JSONB, nullable=False, server_default="{}")
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
