"""Legacy Migration batch pipeline (format_interchange_plan.md Sec 2/Sec 7 Steps 3-4):
`POST /migration/batches` (create + upload), `POST .../run` (classify), `GET .../{id}` (counts),
`GET .../{id}/items[/{item_id}]`, `GET .../{id}/report.csv|.json` (Step 3), plus the Step 4
triage-and-fix loop: `POST .../items/{item_id}/resolve|block|accept-warning` and
`POST .../{id}/commit`.

Conversion is synchronous within `/run` and `/resolve`, same deliberate deviation as export/import
(see app/api/export.py's docstring) -- a platform Job is still submitted at batch-creation time for
cross-service audit visibility. `/run` is idempotent in the narrow sense Sec 2.1 asks for ("a
re-run only reprocesses items that changed"): only items still in `pending` status are processed;
`/resolve` is what puts one item back through conversion+classification directly (Sec 2.6 #2).

`selection` has no wildcard pattern or source-system connector (Sec 2.1's "Select style(s) to
convert, with wildcard support") -- this suite has no actual predecessor-system connector to
select against, so the uploaded files themselves are the selection. `target_collection` (the
platform folder every committed item's piece lands in) is supplied once, at batch-creation time,
stored in `selection` -- matching how Step 2 locks `target_collection` in at the original request
rather than re-asking for it at commit time, and matching the practical shape of a real migration
(one legacy library maps to one destination collection).

**Commit gate** (Sec 2.6): `POST .../{id}/commit` refuses (400) unless every item is in a
commit-eligible state -- `converted`, `resolved`, `converted_with_warning` with `warning_accepted`,
or `blocked` (blocked items are explicitly allowed to coexist with a committed batch and "remain
queued" per Sec 2.6 #4, pending a future corrected re-upload). A bare `error` item blocks the
whole batch's commit until it's either `/resolve`d or `/block`ed.
"""

import csv
import io
import json
import math
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.blob_io import download_migration_source, upload_migration_source
from app.deps import get_actor, get_db, get_platform_client
from app.errors import bad_request, not_found
from app.migration_checks import Finding, LegacyMetadata, classify_item
from app.migration_diff import compute_diff
from app.migration_sources import (
    SUPPORTED_SOURCE_FORMATS,
    IgesParseError,
    ImportPipelineError,
    UnsupportedSourceFormatError,
    parse_source,
)
from app.models import MigrationBatch, MigrationFinding, MigrationItem
from app.platform_client import PlatformClient
from app.platform_commit import commit_geometry_to_platform
from app.schemas import MigrationBatchOut, MigrationFindingOut, MigrationItemOut

router = APIRouter(tags=["migration"])

CHUNK_THRESHOLD = 2000  # Sec 2.1: Gerber's own documented ~2,000-style chunking guidance
BLOCKING_CODES = {"source_grading_corrupt"}  # Sec 2.3: "does require a corrected source export"
# Sec 2.6 #4: "Only converted, converted_with_warning (accepted), and resolved items commit to the
# platform... blocked items remain queued" -- so a `blocked` item is allowed to coexist with a
# committed batch (doesn't block the gate below) but never itself gets a platform piece.
GATE_ALLOWED_STATUSES = {"converted", "resolved", "converted_with_warning", "blocked"}
PIECE_COMMIT_STATUSES = {"converted", "resolved", "converted_with_warning"}


@router.post("/migration/batches", response_model=MigrationBatchOut)
def create_migration_batch(
    files: list[UploadFile] = File(...),
    options: str = Form("{}"),
    client: PlatformClient = Depends(get_platform_client),
    actor: dict = Depends(get_actor),
    db: Session = Depends(get_db),
):
    if not files:
        raise bad_request("At least one file is required.")
    try:
        raw_options = json.loads(options) if options else {}
    except json.JSONDecodeError:
        raise bad_request("`options` must be a JSON object.") from None

    source_system = raw_options.get("source_system") or "unknown"
    source_format = raw_options.get("source_format", "iges")
    if source_format not in SUPPORTED_SOURCE_FORMATS:
        raise bad_request(f"Unsupported source_format '{source_format}'. Supported: {SUPPORTED_SOURCE_FORMATS}.")
    auto_sort_flagged = bool(raw_options.get("auto_sort_flagged", True))
    target_collection = raw_options.get("target_collection")

    job = client.post("/jobs", json={"job_type": "legacy_migration_batch", "input_ref": {"file_count": len(files)}})
    batch_id = uuid.UUID(job["id"])

    batch = MigrationBatch(
        id=batch_id,
        organization_id=uuid.UUID(actor["organization_id"]),
        source_system=source_system,
        selection={"file_count": len(files), "source_format": source_format, "target_collection": target_collection},
        auto_sort_flagged=auto_sort_flagged,
        chunk_count=math.ceil(len(files) / CHUNK_THRESHOLD),
        created_by=uuid.UUID(actor["id"]),
    )
    db.add(batch)
    db.flush()

    for f in files:
        item_id = uuid.uuid4()
        blob_key = f"{actor['organization_id']}/{batch_id}/{item_id}.src"
        upload_migration_source(blob_key, f.file.read())
        db.add(
            MigrationItem(
                id=item_id,
                batch_id=batch_id,
                source_style_ref=f.filename or str(item_id),
                source_storage_key=blob_key,
            )
        )
    db.flush()

    return _batch_out(batch, db)


@router.post("/migration/batches/{batch_id}/run", response_model=MigrationBatchOut)
def run_migration_batch(
    batch_id: str,
    metadata_by_filename: str = Form("{}"),
    db: Session = Depends(get_db),
):
    """`metadata_by_filename`: JSON `{"<source_style_ref>": {<LegacyMetadata fields>}}` -- a real
    DXF/AAMA-ASTM parser would populate this per item automatically; see migration_checks.py's
    module docstring for why this slice takes it from the caller instead."""
    batch = db.get(MigrationBatch, uuid.UUID(batch_id))
    if batch is None:
        raise not_found("Migration batch")
    try:
        raw_metadata_by_filename = json.loads(metadata_by_filename) if metadata_by_filename else {}
    except json.JSONDecodeError:
        raise bad_request("`metadata_by_filename` must be a JSON object.") from None

    pending_items = db.query(MigrationItem).filter_by(batch_id=batch.id, status="pending").all()
    for item in pending_items:
        metadata_dict = raw_metadata_by_filename.get(item.source_style_ref, {})
        _convert_and_classify_item(db, item, batch, metadata_dict)

    batch.status = "completed"
    db.flush()
    return _batch_out(batch, db)


@router.post("/migration/batches/{batch_id}/items/{item_id}/resolve", response_model=MigrationItemOut)
def resolve_migration_item(
    batch_id: str,
    item_id: str,
    legacy_metadata: str = Form("{}"),
    file: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    """Sec 2.6 #2: "resolved in-tool (resolution UI mutates the source-side mapping and re-runs
    conversion for that item only)". `legacy_metadata` is shallow-merged into the item's
    previously-stored metadata (a partial correction, not a full replacement) -- see
    migration_checks.py's own docstring for why that metadata bag stands in for a real source
    parser's own extracted data. Passing `file` replaces the item's raw source bytes outright,
    for errors only a corrected source file can fix (e.g. `self_intersection`)."""
    batch = db.get(MigrationBatch, uuid.UUID(batch_id))
    if batch is None:
        raise not_found("Migration batch")
    item = db.get(MigrationItem, uuid.UUID(item_id))
    if item is None or str(item.batch_id) != batch_id:
        raise not_found("Migration item")

    try:
        raw_metadata_patch = json.loads(legacy_metadata) if legacy_metadata else {}
    except json.JSONDecodeError:
        raise bad_request("`legacy_metadata` must be a JSON object.") from None

    if file is not None:
        upload_migration_source(item.source_storage_key, file.file.read())

    merged_metadata = {**item.legacy_metadata, **raw_metadata_patch}
    was_error_or_blocked = item.status in ("error", "blocked")
    _convert_and_classify_item(db, item, batch, merged_metadata, mark_resolved_if_clean=was_error_or_blocked)
    db.flush()
    return _item_out(item, db)


@router.post("/migration/batches/{batch_id}/items/{item_id}/block", response_model=MigrationItemOut)
def block_migration_item(batch_id: str, item_id: str, note: str = Form(...), db: Session = Depends(get_db)):
    """Sec 5: "mark blocked with a correction note" -- for errors like `source_grading_corrupt`
    that "do require a corrected source export" (Sec 2.3) rather than an in-tool fix."""
    item = db.get(MigrationItem, uuid.UUID(item_id))
    if item is None or str(item.batch_id) != batch_id:
        raise not_found("Migration item")
    item.status = "blocked"
    item.block_note = note
    item.needs_review = True
    db.flush()
    return _item_out(item, db)


@router.post("/migration/batches/{batch_id}/items/{item_id}/accept-warning", response_model=MigrationItemOut)
def accept_migration_item_warning(batch_id: str, item_id: str, actor: dict = Depends(get_actor), db: Session = Depends(get_db)):
    """Sec 2.6 #3: "warning items ... require an explicit accept-as-is before the batch commits.\""""
    item = db.get(MigrationItem, uuid.UUID(item_id))
    if item is None or str(item.batch_id) != batch_id:
        raise not_found("Migration item")
    if item.status != "converted_with_warning":
        raise bad_request(f"Item is '{item.status}', not 'converted_with_warning' -- nothing to accept.")
    item.warning_accepted = True
    now = datetime.now(UTC)
    for finding in db.query(MigrationFinding).filter_by(item_id=item.id, severity="warning").all():
        finding.resolved_at = now
        finding.resolved_by = uuid.UUID(actor["id"])
    db.flush()
    return _item_out(item, db)


@router.post("/migration/batches/{batch_id}/commit", response_model=MigrationBatchOut)
def commit_migration_batch(
    batch_id: str,
    client: PlatformClient = Depends(get_platform_client),
    db: Session = Depends(get_db),
):
    """Sec 2.6 #4: commits every `converted`/`resolved`/accepted-`converted_with_warning` item to
    the platform in `target_collection` (Sec 4's `migration_batch commit target`); `blocked` items
    are left as-is ("remain queued"). Refuses if any item is still a bare, un-triaged `error`."""
    batch = db.get(MigrationBatch, uuid.UUID(batch_id))
    if batch is None:
        raise not_found("Migration batch")
    target_collection = batch.selection.get("target_collection")
    if not target_collection:
        raise bad_request("This batch's original request had no target_collection to commit to.")

    items = db.query(MigrationItem).filter_by(batch_id=batch.id).all()
    blockers = _commit_blockers(items)
    if blockers:
        raise bad_request(f"Cannot commit: {len(blockers)} item(s) not yet resolved/blocked/accepted: {blockers}.")

    for item in items:
        if item.status not in PIECE_COMMIT_STATUSES:
            continue
        piece_code = item.source_style_ref.rsplit(".", 1)[0]
        piece = commit_geometry_to_platform(client, target_collection, piece_code, item.converted_geometry)
        item.target_piece_id = uuid.UUID(piece["id"])

    batch.status = "committed"
    db.flush()
    return _batch_out(batch, db)


@router.get("/migration/batches/{batch_id}", response_model=MigrationBatchOut)
def get_migration_batch(batch_id: str, db: Session = Depends(get_db)):
    batch = db.get(MigrationBatch, uuid.UUID(batch_id))
    if batch is None:
        raise not_found("Migration batch")
    return _batch_out(batch, db)


@router.get("/migration/batches/{batch_id}/items", response_model=list[MigrationItemOut])
def list_migration_items(batch_id: str, status: str | None = Query(None), db: Session = Depends(get_db)):
    batch = db.get(MigrationBatch, uuid.UUID(batch_id))
    if batch is None:
        raise not_found("Migration batch")
    query = db.query(MigrationItem).filter_by(batch_id=batch.id)
    if status:
        query = query.filter_by(status=status)
    return [_item_out(item, db) for item in query.order_by(MigrationItem.created_at).all()]


@router.get("/migration/batches/{batch_id}/items/{item_id}", response_model=MigrationItemOut)
def get_migration_item(batch_id: str, item_id: str, db: Session = Depends(get_db)):
    item = db.get(MigrationItem, uuid.UUID(item_id))
    if item is None or str(item.batch_id) != batch_id:
        raise not_found("Migration item")
    return _item_out(item, db)


@router.get("/migration/batches/{batch_id}/report.json")
def get_migration_report_json(batch_id: str, db: Session = Depends(get_db)):
    return _report_rows(batch_id, db)


@router.get("/migration/batches/{batch_id}/report.csv")
def get_migration_report_csv(batch_id: str, db: Session = Depends(get_db)):
    rows = _report_rows(batch_id, db)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["item_id", "source_style_ref", "code", "severity", "message", "deep_link"])
    writer.writeheader()
    writer.writerows(rows)
    return Response(content=buffer.getvalue(), media_type="text/csv")


def _report_rows(batch_id: str, db: Session) -> list[dict]:
    batch = db.get(MigrationBatch, uuid.UUID(batch_id))
    if batch is None:
        raise not_found("Migration batch")
    rows = []
    items = db.query(MigrationItem).filter_by(batch_id=batch.id).all()
    for item in items:
        findings = db.query(MigrationFinding).filter_by(item_id=item.id).all()
        for finding in findings:
            rows.append(
                {
                    "item_id": str(item.id),
                    "source_style_ref": item.source_style_ref,
                    "code": finding.code,
                    "severity": finding.severity,
                    "message": finding.message,
                    # A real Pattern Design deep link needs Step 4's commit (target_piece_id);
                    # until then this points at this item's own detail endpoint.
                    "deep_link": f"/migration/batches/{batch_id}/items/{item.id}",
                }
            )
    return rows


def _convert_and_classify_item(
    db: Session, item: MigrationItem, batch: MigrationBatch, metadata_dict: dict, mark_resolved_if_clean: bool = False
) -> None:
    """Shared by `/run` (per-pending-item) and `/resolve` (one item, on demand): parses this
    item's stored source bytes, classifies it, and replaces its findings outright -- old findings
    may no longer even apply once the geometry or metadata behind them has changed."""
    source_format = batch.selection.get("source_format", "iges")
    db.query(MigrationFinding).filter_by(item_id=item.id).delete()
    item.legacy_metadata = metadata_dict
    item.warning_accepted = False  # any (re)classification invalidates a prior accept

    raw_bytes = download_migration_source(item.source_storage_key)
    try:
        result = parse_source(source_format, raw_bytes)
    except UnsupportedSourceFormatError as exc:
        item.status = "error"
        item.needs_review = batch.auto_sort_flagged
        item.error_detail = str(exc)
        item.converted_geometry = None
        item.source_summary = None
        _write_finding(db, item.id, Finding("unsupported_source_format", "error", str(exc)))
        return
    except (IgesParseError, ImportPipelineError) as exc:
        item.status = "error"
        item.needs_review = batch.auto_sort_flagged
        item.error_detail = str(exc)
        item.converted_geometry = None
        item.source_summary = None
        _write_finding(db, item.id, Finding(getattr(exc, "code", "parse_error"), "error", exc.message))
        return

    metadata = LegacyMetadata.model_validate(metadata_dict)
    findings = classify_item(result.geometry, metadata)
    for w in result.warnings:
        if w.code == "multiple_grain_lines":
            findings.append(Finding("multiple_grain_lines", "error", w.message, w.detail))
        else:
            findings.append(Finding(w.code, "warning", w.message, w.detail))

    item.converted_geometry = result.geometry.model_dump()
    item.source_summary = result.source_summary
    item.error_detail = None
    status = _status_for(findings)
    if mark_resolved_if_clean and status == "converted":
        status = "resolved"
    item.status = status
    item.needs_review = batch.auto_sort_flagged and item.status not in ("converted", "resolved")
    for finding in findings:
        _write_finding(db, item.id, finding)


def _commit_blockers(items: list[MigrationItem]) -> list[str]:
    blockers = []
    for item in items:
        if item.status not in GATE_ALLOWED_STATUSES or item.status == "converted_with_warning" and not item.warning_accepted:
            blockers.append(item.source_style_ref)
    return blockers


def _status_for(findings: list[Finding]) -> str:
    if any(f.code in BLOCKING_CODES for f in findings):
        return "blocked"
    if any(f.severity == "error" for f in findings):
        return "error"
    if any(f.severity == "warning" for f in findings):
        return "converted_with_warning"
    return "converted"


def _write_finding(db: Session, item_id: uuid.UUID, finding: Finding) -> None:
    db.add(
        MigrationFinding(
            id=uuid.uuid4(),
            item_id=item_id,
            code=finding.code,
            severity=finding.severity,
            message=finding.message,
            geometry_ref=finding.geometry_ref,
        )
    )


def _item_out(item: MigrationItem, db: Session) -> MigrationItemOut:
    findings = db.query(MigrationFinding).filter_by(item_id=item.id).all()
    return MigrationItemOut(
        id=str(item.id),
        batch_id=str(item.batch_id),
        source_style_ref=item.source_style_ref,
        status=item.status,
        needs_review=item.needs_review,
        warning_accepted=item.warning_accepted,
        block_note=item.block_note,
        target_piece_id=str(item.target_piece_id) if item.target_piece_id else None,
        converted_geometry=item.converted_geometry,
        source_summary=item.source_summary,
        diff=compute_diff(item.source_summary, item.converted_geometry),
        error_detail=item.error_detail,
        findings=[
            MigrationFindingOut(
                id=str(f.id),
                code=f.code,
                severity=f.severity,
                message=f.message,
                geometry_ref=f.geometry_ref,
                resolved=f.resolved_at is not None,
            )
            for f in findings
        ],
    )


def _batch_out(batch: MigrationBatch, db: Session) -> MigrationBatchOut:
    items = db.query(MigrationItem).filter_by(batch_id=batch.id).all()
    counts: dict[str, int] = {}
    for item in items:
        counts[item.status] = counts.get(item.status, 0) + 1
    return MigrationBatchOut(
        id=str(batch.id),
        source_system=batch.source_system,
        status=batch.status,
        auto_sort_flagged=batch.auto_sort_flagged,
        chunk_count=batch.chunk_count,
        item_count=len(items),
        counts=counts,
        commit_blocked_by=_commit_blockers(items),
    )
