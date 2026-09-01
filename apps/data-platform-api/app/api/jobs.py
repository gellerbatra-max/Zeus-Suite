"""Section 4.12: the generic async job API. This is what Marker Making calls to submit a
nesting solve and poll for its result, and what the (stub) worker in app/job_worker.py calls to
report progress and completion."""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auditing import record_audit
from app.deps import (
    Actor,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import bad_request, not_found
from app.job_service import (
    cancel_job,
    complete_job,
    get_job_events,
    heartbeat,
    job_type_code,
    submit_job,
)
from app.models import Job, JobType
from app.schemas import (
    HeartbeatRequest,
    JobCompleteRequest,
    JobEventOut,
    JobOut,
    JobSubmitRequest,
    Page,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _get_job_or_404(db: Session, job_id: uuid.UUID, org_id: uuid.UUID) -> Job:
    job = db.get(Job, job_id)
    if job is None or job.organization_id != org_id:
        raise not_found("Job")
    return job


def _job_out(db: Session, job: Job) -> JobOut:
    return JobOut(
        id=job.id,
        job_type=job_type_code(db, job),
        status=job.status,
        progress_pct=float(job.progress_pct) if job.progress_pct is not None else None,
        result_ref=job.result_ref,
        error_detail=job.error_detail,
        submitted_at=job.submitted_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        timeout_at=job.timeout_at,
    )


@router.post("", status_code=202, response_model=JobOut)
def submit(
    body: JobSubmitRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "job.submit", request_id=request_id, entity_type="job", action="job.submit")
    job = submit_job(db, actor.organization_id, actor.user_id, body.job_type, body.input_ref, body.callback_url)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="job.submit",
        entity_type="job", entity_id=job.id, request_id=request_id,
        after_state={"job_type": body.job_type}, result="success",
    )
    return _job_out(db, job)


@router.get("", response_model=Page)
def list_jobs(
    job_type: str | None = Query(None),
    status: str | None = Query(None),
    submitted_by: uuid.UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "job.read", request_id=request_id, entity_type="job", action="job.list")
    query = db.query(Job).filter(Job.organization_id == actor.organization_id)
    if status is not None:
        query = query.filter(Job.status == status)
    if submitted_by is not None:
        query = query.filter(Job.submitted_by == submitted_by)
    if job_type is not None:
        query = query.join(JobType, JobType.id == Job.job_type_id).filter(JobType.code == job_type)
    total = query.count()
    rows = query.order_by(Job.submitted_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return Page(items=[_job_out(db, r) for r in rows], page=page, page_size=page_size, total=total)


@router.get("/{job_id}", response_model=JobOut)
def get_job(
    job_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    job = _get_job_or_404(db, job_id, actor.organization_id)
    require_permission(
        db, actor, "job.read", request_id=request_id, entity_type="job", action="job.read", entity_id=job.id,
    )
    return _job_out(db, job)


@router.get("/{job_id}/events", response_model=list[JobEventOut])
def list_job_events(
    job_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    job = _get_job_or_404(db, job_id, actor.organization_id)
    require_permission(
        db, actor, "job.read", request_id=request_id, entity_type="job", action="job.events", entity_id=job.id,
    )
    return [
        JobEventOut(id=e.id, occurred_at=e.occurred_at, event_type=e.event_type, detail=e.detail)
        for e in get_job_events(db, job.id)
    ]


@router.post("/{job_id}/cancel", response_model=JobOut)
def cancel(
    job_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    job = _get_job_or_404(db, job_id, actor.organization_id)
    require_permission(
        db, actor, "job.cancel", request_id=request_id, entity_type="job", action="job.cancel", entity_id=job.id,
    )
    cancel_job(db, job)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="job.cancel",
        entity_type="job", entity_id=job.id, request_id=request_id, result="success",
    )
    return _job_out(db, job)


@router.post("/{job_id}/heartbeat", response_model=JobOut)
def worker_heartbeat(
    job_id: uuid.UUID,
    body: HeartbeatRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    job = _get_job_or_404(db, job_id, actor.organization_id)
    require_permission(
        db, actor, "job.worker", request_id=request_id, entity_type="job", action="job.heartbeat", entity_id=job.id,
    )
    heartbeat(db, job, body.progress_pct)
    db.flush()
    return _job_out(db, job)


@router.post("/{job_id}/complete", response_model=JobOut)
def worker_complete(
    job_id: uuid.UUID,
    body: JobCompleteRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    job = _get_job_or_404(db, job_id, actor.organization_id)
    require_permission(
        db, actor, "job.worker", request_id=request_id, entity_type="job", action="job.complete", entity_id=job.id,
    )
    if body.status not in ("succeeded", "failed"):
        raise bad_request("status must be 'succeeded' or 'failed'.")
    complete_job(db, job, body.status, result_ref=body.result_ref, error_detail=body.error_detail)
    db.flush()
    record_audit(
        db, organization_id=actor.organization_id, user_id=actor.user_id, action="job.complete",
        entity_type="job", entity_id=job.id, request_id=request_id,
        after_state={"status": body.status}, result="success",
    )
    return _job_out(db, job)
