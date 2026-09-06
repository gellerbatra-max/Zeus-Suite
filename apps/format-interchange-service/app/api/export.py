"""POST /pieces/{piece_id}/export/iges + GET /export/iges/jobs/{job_id} (format_interchange_plan.md
Sec 1.1/Sec 5, Step 1 of Sec 7's phased build plan -- "the smallest complete slice").

This slice's conversion is synchronous (small flat 2D outlines, not the kind of workload that needs
real async processing -- same reasoning pattern-design-service's own plan gives for skipping the
job-queue pattern in its own grading computation). A platform Job is still submitted via
`POST /jobs` for cross-service audit/tracking id, but this endpoint does NOT push it to a terminal
state via the platform's `heartbeat`/`complete` endpoints -- those require a `job.worker`
permission this caller's own identity doesn't hold (per data-platform-api's seed data, that
permission is "service-account-only"), and provisioning a dedicated worker identity per
organization is out of scope here. Instead, `interchange_job.status` (this service's own row) is
the authoritative status, set synchronously in this same request; the platform Job row exists for
audit/cross-service visibility and stays `queued` in this slice.
"""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.blob_io import download_bytes, download_url_for_export, upload_export
from app.deps import get_actor, get_db, get_platform_client
from app.errors import not_found
from app.geometry import (
    ExportValidationError,
    PieceGeometryDocument,
    validate_for_export,
)
from app.iges_writer import write_iges
from app.models import InterchangeJob
from app.platform_client import PlatformClient
from app.schemas import ExportIgesJobOut, ExportIgesRequest

router = APIRouter(tags=["export"])


@router.post("/pieces/{piece_id}/export/iges", response_model=ExportIgesJobOut)
def export_iges(
    piece_id: str,
    body: ExportIgesRequest,
    client: PlatformClient = Depends(get_platform_client),
    actor: dict = Depends(get_actor),
    db: Session = Depends(get_db),
):
    piece = client.get(f"/pieces/{piece_id}")
    version_id = piece.get("current_version_id")

    job = client.post(
        "/jobs", json={"job_type": "iges_export", "input_ref": {"piece_id": piece_id}}
    )
    job_id = uuid.UUID(job["id"])

    interchange_job = InterchangeJob(
        id=job_id,
        organization_id=uuid.UUID(actor["organization_id"]),
        job_type="iges_export",
        piece_id=uuid.UUID(piece_id),
        status="running",
        params=body.model_dump(),
        created_by=uuid.UUID(actor["id"]),
    )
    db.add(interchange_job)
    db.flush()

    if version_id is None:
        interchange_job.status = "failed"
        interchange_job.error_detail = "Piece has no committed geometry version yet -- nothing to export."
        return _job_out(interchange_job, piece)

    try:
        download = client.get(f"/pieces/{piece_id}/versions/{version_id}/download-url")
        geometry_bytes = download_bytes(download["download_url"])
        doc = PieceGeometryDocument.model_validate_json(geometry_bytes)

        validate_for_export(doc)

        if not body.include_internal_lines:
            doc = doc.model_copy(update={"internal_lines": []})
        if not body.include_notches:
            doc = doc.model_copy(update={"notches": []})
        if not body.include_grain_line:
            doc = doc.model_copy(update={"grain_line": None})

        file_name = f"{piece['piece_code']}.igs"
        iges_text = write_iges(doc, piece["piece_code"], file_name)

        blob_key = f"{actor['organization_id']}/{piece_id}/{job_id}.igs"
        upload_export(blob_key, iges_text.encode("ascii", errors="replace"))

        interchange_job.status = "succeeded"
        interchange_job.object_storage_key = blob_key
    except ExportValidationError as exc:
        interchange_job.status = "failed"
        interchange_job.error_detail = f"{exc.code}: {exc.message}"
    except Exception as exc:  # noqa: BLE001 - surface any conversion failure as a failed job, not a 500
        interchange_job.status = "failed"
        interchange_job.error_detail = str(exc)

    return _job_out(interchange_job, piece)


@router.get("/export/iges/jobs/{job_id}", response_model=ExportIgesJobOut)
def get_export_job(
    job_id: str,
    client: PlatformClient = Depends(get_platform_client),
    db: Session = Depends(get_db),
):
    interchange_job = db.get(InterchangeJob, uuid.UUID(job_id))
    if interchange_job is None:
        raise not_found("Export job")
    piece = client.get(f"/pieces/{interchange_job.piece_id}")
    return _job_out(interchange_job, piece)


def _job_out(job: InterchangeJob, piece: dict) -> ExportIgesJobOut:
    download_url = download_url_for_export(job.object_storage_key) if job.object_storage_key else None
    return ExportIgesJobOut(
        job_id=str(job.id),
        status=job.status,
        piece_id=str(job.piece_id),
        piece_code=piece.get("piece_code"),
        download_url=download_url,
        error_detail=job.error_detail,
    )
