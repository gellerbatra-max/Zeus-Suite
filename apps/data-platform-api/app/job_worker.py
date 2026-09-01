"""Section 3.6's worker execution model, local-dev flavor: no real Celery/Service Bus/Container
Apps job -- `run_one_job` below plays the worker's role in-process. It dequeues via the local
Service-Bus substitute in app/job_service.py, then reports progress/completion through the *real*
HTTP endpoints (Section 4.12) using a service-account identity holding only `job.worker`, exactly
as a real out-of-process worker would -- so the same permission checks and audit trail apply
regardless of how the job got picked up.
"""

from typing import Any, Protocol

from sqlalchemy.orm import Session

from app.job_service import JOB_HANDLERS, dequeue_and_claim_job, job_type_code
from app.models import Job


class HttpResponse(Protocol):
    status_code: int


class HttpClient(Protocol):
    def post(self, url: str, json: dict[str, Any], headers: dict[str, str]) -> HttpResponse: ...


def _post(client: HttpClient, url: str, json: dict[str, Any], headers: dict[str, str]) -> HttpResponse:
    response = client.post(url, json=json, headers=headers)
    if response.status_code >= 400:
        raise RuntimeError(f"Worker call to {url} failed with {response.status_code}: {response.text}")
    return response


def run_one_job(session: Session, client: HttpClient, worker_headers: dict[str, str], worker_instance: str) -> Job | None:
    """Claims and fully processes exactly one queued job, or returns None if none are queued."""
    job = dequeue_and_claim_job(session, worker_instance)
    if job is None:
        return None

    job_id = job.id
    code = job_type_code(session, job)
    input_ref = job.input_ref

    _post(client, f"/jobs/{job_id}/heartbeat", {"progress_pct": 0}, worker_headers)

    handler = JOB_HANDLERS.get(code)
    try:
        if handler is None:
            raise ValueError(f"No handler registered for job type '{code}'")
        result_ref = handler(input_ref)
    except Exception as exc:  # noqa: BLE001 - a failed job is a normal outcome, not a worker crash
        _post(client, f"/jobs/{job_id}/complete", {"status": "failed", "error_detail": str(exc)}, worker_headers)
        return session.get(Job, job_id)

    _post(client, f"/jobs/{job_id}/heartbeat", {"progress_pct": 100}, worker_headers)
    _post(client, f"/jobs/{job_id}/complete", {"status": "succeeded", "result_ref": result_ref}, worker_headers)
    return session.get(Job, job_id)


def drain_queue(session: Session, client: HttpClient, worker_headers: dict[str, str], worker_instance: str, max_jobs: int = 1000) -> int:
    """Runs `run_one_job` until the queue is empty (or `max_jobs` processed) -- a single-process
    stand-in for "N worker replicas, scaled on queue depth" (Section 3.6), used by tests to drive
    a batch of submitted jobs to completion without a real worker fleet."""
    processed = 0
    while processed < max_jobs:
        job = run_one_job(session, client, worker_headers, worker_instance)
        if job is None:
            break
        processed += 1
    return processed
