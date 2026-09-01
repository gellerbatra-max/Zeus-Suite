"""Engine B (§1.2/§5): thin wrappers over data-platform-api's existing generic job queue
(built in that service's Milestone 6), named to match this app's own §3 API surface. No new job
infrastructure -- `marker_nesting_solve` is already a seeded job_type on the platform, and its
worker's stub handler already proves the async plumbing end-to-end. A real placement-producing
solver is explicitly out of scope for this slice (see the plan file)."""

from fastapi import APIRouter, Depends

from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import NestingJobOut, NestingJobSubmitRequest

router = APIRouter(prefix="/nesting-jobs", tags=["nesting-jobs"])


def _job_out(job: dict) -> NestingJobOut:
    return NestingJobOut(
        id=job["id"],
        status=job["status"],
        progress_pct=job.get("progress_pct"),
        result_ref=job.get("result_ref"),
        error_detail=job.get("error_detail"),
    )


@router.post("", response_model=NestingJobOut, status_code=202)
def submit_nesting_job(body: NestingJobSubmitRequest, client: PlatformClient = Depends(get_platform_client)):
    job = client.post(
        "/jobs",
        json={
            "job_type": "marker_nesting_solve",
            "input_ref": {"marker_id": body.marker_id, "order_id": body.order_id},
        },
    )
    return _job_out(job)


@router.get("/{job_id}", response_model=NestingJobOut)
def get_nesting_job(job_id: str, client: PlatformClient = Depends(get_platform_client)):
    job = client.get(f"/jobs/{job_id}")
    return _job_out(job)


@router.post("/{job_id}/cancel", response_model=NestingJobOut)
def cancel_nesting_job(job_id: str, client: PlatformClient = Depends(get_platform_client)):
    job = client.post(f"/jobs/{job_id}/cancel")
    return _job_out(job)
