from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
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


class MigrationBatch(Base):
    """One bulk-migration run (Sec 4/Sec 7 Step 3) -- a Style-Converter-equivalent batch of
    uploaded legacy source files, classified but (Step 3) not yet committed to the platform;
    committing is Step 4's job, alongside the Migration Viewer triage loop.

    `selection` deliberately does not carry a wildcard pattern or source-system connector, per
    Sec 2.1's "Select style(s) to convert, with wildcard support" -- this suite has no actual
    predecessor-system connector to select against, so the uploaded files themselves ARE the
    selection; `selection` instead records `{"file_count": N}` for audit/report purposes.
    """

    __tablename__ = "migration_batch"

    id = Column(UUID(as_uuid=True), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), nullable=False)
    source_system = Column(Text, nullable=False)
    selection = Column(JSONB, nullable=False, server_default="{}")
    # pending (created, not yet run) -> running -> completed. Synchronous single-request
    # processing (same deviation as export/import -- see app/api/migration.py's docstring), so
    # "running" is only ever observed if a request crashes mid-batch.
    status = Column(Text, nullable=False, server_default="pending")
    auto_sort_flagged = Column(Boolean, nullable=False, server_default="true")
    chunk_count = Column(Integer, nullable=False, server_default="1")
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class MigrationItem(Base):
    """One style/piece within a migration batch (Sec 4)."""

    __tablename__ = "migration_item"

    id = Column(UUID(as_uuid=True), primary_key=True)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("format_interchange.migration_batch.id"), nullable=False)
    source_style_ref = Column(Text, nullable=False)
    target_piece_id = Column(UUID(as_uuid=True), nullable=True)
    # pending | converted | converted_with_warning | error | blocked | resolved
    status = Column(Text, nullable=False, server_default="pending")
    needs_review = Column(Boolean, nullable=False, server_default="false")
    # Raw uploaded source bytes, kept for Step 4's "resolve in-tool and re-run just this item"
    # (Sec 2.6) -- not part of Sec 4's own field list, added here since a re-run genuinely needs
    # the original bytes back, the same class of pragmatic addition Step 2 made for target_piece_id.
    source_storage_key = Column(Text, nullable=True)
    # Converted geometry + parsed-source summary are small structured JSON (a few KB per piece),
    # so they're stored directly rather than round-tripped through blob storage like the raw
    # source above -- the item-detail endpoint (Sec 5) needs to serve them on every read.
    converted_geometry = Column(JSONB, nullable=True)
    source_summary = Column(JSONB, nullable=True)
    error_detail = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class MigrationFinding(Base):
    """One error/warning/diff-highlight against a migration item (Sec 4), from the catalogues in
    Sec 2.3 (errors) / Sec 2.4 (warnings). `resolved_at`/`resolved_by` stay null until Step 4's
    resolve/accept-warning actions exist -- this table is written here but not yet mutated after
    creation."""

    __tablename__ = "migration_finding"

    id = Column(UUID(as_uuid=True), primary_key=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("format_interchange.migration_item.id"), nullable=False)
    code = Column(Text, nullable=False)
    severity = Column(Text, nullable=False)  # error | warning
    message = Column(Text, nullable=False)
    geometry_ref = Column(JSONB, nullable=False, server_default="{}")
    resolved_at = Column(TIMESTAMP(timezone=True), nullable=True)
    resolved_by = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
