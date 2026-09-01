"""Section 2.12 + 3.5-3.8 + 4.12: the generic async job pattern. Shared by app/api/jobs.py (the
HTTP surface a real client/worker calls) and app/job_worker.py (the local worker stand-in) so
both paths run identical logic and produce identical audit/job_events trails.

No real Azure Service Bus is available locally (see the Milestone 1 plan's "Local dev infra"
decision) -- `dequeue_and_claim_job` below is the local substitute for "Service Bus hands a
worker a queued job_id," implemented as an atomic `SELECT ... FOR UPDATE SKIP LOCKED` claim
instead. Everything downstream of that (heartbeat, complete, cancel, the timeout sweep) is the
real Section 3.7/4.12 behavior, unchanged by the substitution.
"""

import time
import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Job, JobEvent, JobType


def _stub_marker_nesting_solve(input_ref: dict[str, Any]) -> dict[str, Any]:
    """Milestone 6's own instruction: "a stub nesting function (a sleep-and-echo placeholder,
    not the real algorithm -- the real algorithm's integration is Marker Making's own build)."
    A short sleep stands in for the ~30-minute real solve."""
    time.sleep(0.05)
    return {"echo": input_ref, "cut_plan_blob_key": "stub/cut_plan.json", "marker_version_ids": []}


JOB_HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "marker_nesting_solve": _stub_marker_nesting_solve,
}


def submit_job(
    session: Session,
    organization_id: uuid.UUID,
    submitted_by: uuid.UUID,
    job_type_code: str,
    input_ref: dict[str, Any],
    callback_url: str | None,
) -> Job:
    job_type = session.query(JobType).filter_by(code=job_type_code).one()
    now = datetime.now(UTC)
    job = Job(
        organization_id=organization_id,
        job_type_id=job_type.id,
        status="queued",
        submitted_by=submitted_by,
        input_ref=input_ref,
        callback_url=callback_url,
        submitted_at=now,
    )
    job.timeout_at = now + timedelta(seconds=job_type.default_timeout_seconds)
    session.add(job)
    session.flush()
    session.add(JobEvent(job_id=job.id, event_type="queued", detail={}))
    return job


def job_type_code(session: Session, job: Job) -> str:
    return session.get(JobType, job.job_type_id).code


def get_job_events(session: Session, job_id: uuid.UUID) -> list[JobEvent]:
    return session.query(JobEvent).filter_by(job_id=job_id).order_by(JobEvent.occurred_at).all()


def heartbeat(session: Session, job: Job, progress_pct: float | None) -> None:
    job.last_heartbeat_at = datetime.now(UTC)
    if progress_pct is not None:
        job.progress_pct = progress_pct
    session.add(JobEvent(job_id=job.id, event_type="progress", detail={"progress_pct": progress_pct}))


def complete_job(
    session: Session,
    job: Job,
    status: str,
    result_ref: dict[str, Any] | None = None,
    error_detail: str | None = None,
) -> None:
    if status not in ("succeeded", "failed"):
        raise ValueError(f"complete_job status must be 'succeeded' or 'failed', got {status!r}")
    job.status = status
    job.completed_at = datetime.now(UTC)
    job.result_ref = result_ref
    job.error_detail = error_detail
    session.add(
        JobEvent(
            job_id=job.id,
            event_type=status,
            detail={"result_ref": result_ref} if status == "succeeded" else {"error_detail": error_detail},
        )
    )


def cancel_job(session: Session, job: Job) -> None:
    """Best-effort per Section 4.12: a queued job is cancelled outright (no worker has touched
    it yet, so this is safe); a running job just gets the cancel request recorded -- the spec is
    explicit this "does not guarantee an already-running... solve stops immediately," so the stub
    worker here makes no attempt at mid-flight interruption."""
    if job.status == "queued":
        job.status = "cancelled"
        job.completed_at = datetime.now(UTC)
    session.add(JobEvent(job_id=job.id, event_type="cancelled", detail={"previous_status": job.status}))


def dequeue_and_claim_job(session: Session, worker_instance: str) -> Job | None:
    """The local Service-Bus-delivery substitute: atomically claims one queued job (SELECT ...
    FOR UPDATE SKIP LOCKED, so concurrent worker pollers never claim the same row) and flips it
    straight to 'running', combining what a real deployment splits across Service Bus delivery
    and the worker's own first heartbeat call."""
    row = session.execute(
        text(
            "SELECT id FROM dmp.jobs WHERE status = 'queued' "
            "ORDER BY submitted_at FOR UPDATE SKIP LOCKED LIMIT 1"
        )
    ).first()
    if row is None:
        return None

    job = session.get(Job, row[0])
    job.status = "running"
    job.started_at = datetime.now(UTC)
    job.worker_instance = worker_instance
    job.last_heartbeat_at = job.started_at
    session.add(JobEvent(job_id=job.id, event_type="picked_up", detail={"worker_instance": worker_instance}))
    session.commit()
    return job


def sweep_timed_out_jobs(session: Session) -> int:
    """Section 3.7's timeout sweep: any job past its `timeout_at` that never reached a terminal
    state is failed with the same error_detail Service Bus dead-lettering would surface."""
    now = datetime.now(UTC)
    stale = (
        session.query(Job)
        .filter(Job.status.in_(["queued", "running"]), Job.timeout_at.isnot(None), Job.timeout_at < now)
        .all()
    )
    for job in stale:
        job.status = "failed"
        job.completed_at = now
        job.error_detail = "max_delivery_exceeded"
        session.add(JobEvent(job_id=job.id, event_type="timed_out", detail={}))
    session.commit()
    return len(stale)
