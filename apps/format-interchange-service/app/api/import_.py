"""POST /import/iges + GET /import/iges/jobs/{job_id} + GET .../log + POST .../commit
(format_interchange_plan.md Sec 1.2/Sec 1.4, Step 2 of Sec 7's phased build plan).

Conversion is synchronous, same deliberate deviation app/api/export.py documents for Step 1 (no
`job.worker` identity to push the platform Job through heartbeat/complete) -- a platform Job is
still submitted for cross-service audit visibility, and `interchange_job.status` is this service's
own authoritative status.

**Staging vs. committing** (Sec 1.2's `stage_only` + Sec 1.4's `auto_approve`, unified here): a
converted piece commits to the platform in the *same request* that submitted it only if
`stage_only=false` OR `auto_approve=true`; otherwise it is held `staged` -- geometry, the raw
source, and every warning saved to a blob bundle -- pending a caller's own explicit
`POST /import/iges/jobs/{job_id}/commit` once they've reviewed it (Sec 1.4: "commit ... is blocked
until the caller explicitly approves"). `target_collection` (a platform folder id) must be present
on the original `POST /import/iges` request for either commit path -- it is not re-askable at
commit time, matching how Sec 1.2's table scopes it as a param of the import request itself.
"""

import json
import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.audit import record_audit
from app.blob_io import download_import_bundle, upload_import_bundle
from app.deps import get_db, get_platform_client
from app.errors import bad_request, not_found
from app.iges_reader import IgesParseError, parse_iges
from app.import_pipeline import (
    ImportIgesOptions,
    ImportPipelineError,
    run_import_pipeline,
)
from app.models import ImportProfile, InterchangeJob
from app.permissions import require_import
from app.platform_client import PlatformClient
from app.platform_commit import commit_geometry_to_platform
from app.schemas import ImportIgesJobOut

router = APIRouter(tags=["import"])


def _resolve_options(raw_options: dict, actor: dict, db: Session) -> ImportIgesOptions:
    merged: dict = {}
    profile_id = raw_options.get("import_profile_id")
    if profile_id:
        profile = db.get(ImportProfile, uuid.UUID(profile_id))
        if profile is None or str(profile.organization_id) != actor["organization_id"]:
            raise not_found("Import profile")
        merged.update(profile.params)
    merged.update(raw_options)
    return ImportIgesOptions.model_validate(merged)


@router.post("/import/iges", response_model=ImportIgesJobOut)
def import_iges(
    file: UploadFile = File(...),
    options: str = Form("{}"),
    piece_code: str | None = Form(None),
    client: PlatformClient = Depends(get_platform_client),
    actor: dict = Depends(require_import),
    db: Session = Depends(get_db),
):
    try:
        raw_options = json.loads(options) if options else {}
    except json.JSONDecodeError:
        raise bad_request("`options` must be a JSON object.") from None
    parsed_options = _resolve_options(raw_options, actor, db)

    file_bytes = file.file.read()
    iges_text = file_bytes.decode("ascii", errors="replace")

    job = client.post("/jobs", json={"job_type": "iges_import", "input_ref": {"file_name": file.filename}})
    job_id = uuid.UUID(job["id"])
    resolved_piece_code = piece_code or (file.filename or f"IMPORT-{job_id}").rsplit(".", 1)[0]

    interchange_job = InterchangeJob(
        id=job_id,
        organization_id=uuid.UUID(actor["organization_id"]),
        job_type="iges_import",
        piece_id=None,  # an import has no *source* piece (unlike export) -- see models.py
        status="running",
        params={**parsed_options.model_dump(), "piece_code": resolved_piece_code},
        created_by=uuid.UUID(actor["id"]),
    )
    db.add(interchange_job)
    db.flush()

    try:
        parsed = parse_iges(iges_text)
        result = run_import_pipeline(parsed, parsed_options)

        bundle = {
            "source_iges": iges_text,
            "geometry": result.geometry.model_dump(),
            "source_summary": result.source_summary,
            "warnings": [w.as_dict() for w in result.warnings],
        }
        blob_key = f"{actor['organization_id']}/{job_id}.json"
        upload_import_bundle(blob_key, json.dumps(bundle).encode())
        interchange_job.object_storage_key = blob_key

        should_commit_now = parsed_options.auto_approve or not parsed_options.stage_only
        if should_commit_now:
            if not parsed_options.target_collection:
                interchange_job.status = "failed"
                interchange_job.error_detail = "target_collection is required to commit (stage_only=false or auto_approve=true)."
            else:
                piece = commit_geometry_to_platform(
                    client, parsed_options.target_collection, resolved_piece_code, bundle["geometry"]
                )
                interchange_job.status = "committed"
                interchange_job.target_piece_id = uuid.UUID(piece["id"])
        else:
            interchange_job.status = "staged"
    except (IgesParseError, ImportPipelineError) as exc:
        interchange_job.status = "failed"
        interchange_job.error_detail = f"{getattr(exc, 'code', 'parse_error')}: {exc.message}"
    except Exception as exc:  # noqa: BLE001 - surface any conversion failure as a failed job, not a 500
        interchange_job.status = "failed"
        interchange_job.error_detail = str(exc)

    record_audit(
        db, actor, "import.iges", "interchange_job", interchange_job.id,
        {"file_name": file.filename, "status": interchange_job.status},
    )
    return _job_out(interchange_job)


@router.get("/import/iges/jobs/{job_id}", response_model=ImportIgesJobOut)
def get_import_job(job_id: str, actor: dict = Depends(require_import), db: Session = Depends(get_db)):
    interchange_job = db.get(InterchangeJob, uuid.UUID(job_id))
    if interchange_job is None:
        raise not_found("Import job")
    return _job_out(interchange_job)


@router.get("/import/iges/jobs/{job_id}/log")
def get_import_job_log(job_id: str, actor: dict = Depends(require_import), db: Session = Depends(get_db)):
    interchange_job = db.get(InterchangeJob, uuid.UUID(job_id))
    if interchange_job is None:
        raise not_found("Import job")
    warnings = []
    if interchange_job.object_storage_key:
        bundle = json.loads(download_import_bundle(interchange_job.object_storage_key))
        warnings = bundle["warnings"]
    return {"job_id": str(interchange_job.id), "status": interchange_job.status, "warnings": warnings}


@router.post("/import/iges/jobs/{job_id}/commit", response_model=ImportIgesJobOut)
def commit_import_job(
    job_id: str,
    client: PlatformClient = Depends(get_platform_client),
    actor: dict = Depends(require_import),
    db: Session = Depends(get_db),
):
    interchange_job = db.get(InterchangeJob, uuid.UUID(job_id))
    if interchange_job is None:
        raise not_found("Import job")
    if interchange_job.status != "staged":
        raise bad_request(f"Import job is '{interchange_job.status}', not 'staged' -- nothing to commit.")

    target_collection = interchange_job.params.get("target_collection")
    if not target_collection:
        raise bad_request("This job's original request had no target_collection to commit to.")

    bundle = json.loads(download_import_bundle(interchange_job.object_storage_key))
    piece_code = interchange_job.params.get("piece_code") or f"IMPORT-{interchange_job.id}"
    piece = commit_geometry_to_platform(client, target_collection, piece_code, bundle["geometry"])
    interchange_job.status = "committed"
    interchange_job.target_piece_id = uuid.UUID(piece["id"])
    record_audit(db, actor, "import.commit", "interchange_job", interchange_job.id, {"target_piece_id": str(piece["id"])})
    return _job_out(interchange_job)


def _job_out(job: InterchangeJob) -> ImportIgesJobOut:
    geometry = None
    source_summary = None
    warnings: list[dict] = []
    if job.object_storage_key:
        bundle = json.loads(download_import_bundle(job.object_storage_key))
        warnings = bundle["warnings"]
        if job.status != "committed":
            geometry = bundle["geometry"]
            source_summary = bundle["source_summary"]
    return ImportIgesJobOut(
        job_id=str(job.id),
        status=job.status,
        target_piece_id=str(job.target_piece_id) if job.target_piece_id else None,
        geometry=geometry,
        source_summary=source_summary,
        warnings=warnings,
        error_detail=job.error_detail,
    )
