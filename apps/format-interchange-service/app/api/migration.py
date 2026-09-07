"""Legacy Migration batch pipeline -- classification only (format_interchange_plan.md Sec 2/Sec 7
Step 3): `POST /migration/batches` (create + upload), `POST /migration/batches/{id}/run`
(classify), `GET .../{id}` (counts), `GET .../{id}/items[/{item_id}]`, `GET .../{id}/report.csv|
.json`. The remaining Sec 5 endpoints (`resolve`/`block`/`accept-warning`/`commit`) are Step 4's
Migration Viewer triage loop -- this slice classifies and reports, it does not yet fix or commit.

Conversion is synchronous within `/run`, same deliberate deviation as export/import (see
app/api/export.py's docstring) -- a platform Job is still submitted at batch-creation time for
cross-service audit visibility. `/run` is idempotent in the narrow sense Sec 2.1 asks for ("a
re-run only reprocesses items that changed"): only items still in `pending` status are processed;
Step 4's resolve action is what would put an item back into `pending` for a genuine re-run.

`selection` has no wildcard pattern or source-system connector (Sec 2.1's "Select style(s) to
convert, with wildcard support") -- this suite has no actual predecessor-system connector to
select against, so the uploaded files themselves are the selection.
"""

import csv
import io
import json
import math
import uuid

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.blob_io import download_migration_source, upload_migration_source
from app.deps import get_actor, get_db, get_platform_client
from app.errors import bad_request, not_found
from app.migration_checks import Finding, LegacyMetadata, classify_item
from app.migration_sources import (
    SUPPORTED_SOURCE_FORMATS,
    IgesParseError,
    ImportPipelineError,
    UnsupportedSourceFormatError,
    parse_source,
)
from app.models import MigrationBatch, MigrationFinding, MigrationItem
from app.platform_client import PlatformClient
from app.schemas import MigrationBatchOut, MigrationFindingOut, MigrationItemOut

router = APIRouter(tags=["migration"])

CHUNK_THRESHOLD = 2000  # Sec 2.1: Gerber's own documented ~2,000-style chunking guidance
BLOCKING_CODES = {"source_grading_corrupt"}  # Sec 2.3: "does require a corrected source export"


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

    job = client.post("/jobs", json={"job_type": "legacy_migration_batch", "input_ref": {"file_count": len(files)}})
    batch_id = uuid.UUID(job["id"])

    batch = MigrationBatch(
        id=batch_id,
        organization_id=uuid.UUID(actor["organization_id"]),
        source_system=source_system,
        selection={"file_count": len(files), "source_format": source_format},
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

    source_format = batch.selection.get("source_format", "iges")
    pending_items = db.query(MigrationItem).filter_by(batch_id=batch.id, status="pending").all()

    for item in pending_items:
        raw_bytes = download_migration_source(item.source_storage_key)
        try:
            result = parse_source(source_format, raw_bytes)
        except UnsupportedSourceFormatError as exc:
            item.status = "error"
            item.needs_review = batch.auto_sort_flagged
            item.error_detail = str(exc)
            _write_finding(db, item.id, Finding("unsupported_source_format", "error", str(exc)))
            continue
        except (IgesParseError, ImportPipelineError) as exc:
            item.status = "error"
            item.needs_review = batch.auto_sort_flagged
            item.error_detail = str(exc)
            _write_finding(db, item.id, Finding(getattr(exc, "code", "parse_error"), "error", exc.message))
            continue

        metadata = LegacyMetadata.model_validate(raw_metadata_by_filename.get(item.source_style_ref, {}))
        findings = classify_item(result.geometry, metadata)
        for w in result.warnings:
            if w.code == "multiple_grain_lines":
                findings.append(Finding("multiple_grain_lines", "error", w.message, w.detail))
            else:
                findings.append(Finding(w.code, "warning", w.message, w.detail))

        item.converted_geometry = result.geometry.model_dump()
        item.source_summary = result.source_summary
        item.status = _status_for(findings)
        item.needs_review = batch.auto_sort_flagged and item.status != "converted"
        for finding in findings:
            _write_finding(db, item.id, finding)

    batch.status = "completed"
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
        target_piece_id=str(item.target_piece_id) if item.target_piece_id else None,
        converted_geometry=item.converted_geometry,
        source_summary=item.source_summary,
        error_detail=item.error_detail,
        findings=[
            MigrationFindingOut(id=str(f.id), code=f.code, severity=f.severity, message=f.message, geometry_ref=f.geometry_ref)
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
    )
