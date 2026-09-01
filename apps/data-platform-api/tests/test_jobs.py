"""Milestone 6 exit check: a test script submits 20 concurrent stub jobs, confirms they queue,
scale workers, run, and complete (or correctly fail/time out when deliberately induced to), with
a complete job_events trail for each -- proving the generic async-job pattern before Marker
Making's real ~30-minute nesting solve is the first thing to exercise it live.
"""

import threading
import uuid
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.auth import dev_login
from app.db import SessionLocal
from app.job_service import submit_job, sweep_timed_out_jobs
from app.job_worker import run_one_job
from app.main import app
from app.models import JobEvent, Organization, Role, User, UserRole

client = TestClient(app)


def _grant_role(session, org_code: str, username: str, role_code: str) -> None:
    org = session.query(Organization).filter_by(code=org_code).one()
    user = session.query(User).filter_by(organization_id=org.id, username=username).one()
    role = session.query(Role).filter_by(code=role_code).one()
    session.add(UserRole(user_id=user.id, role_id=role.id, folder_id=None, granted_by=user.id))
    session.commit()


def test_submit_20_concurrent_jobs_scale_workers_and_complete(db_session):
    unique = uuid.uuid4().hex[:8]
    org_code = f"JOBS-{unique}"
    submitter_headers = {"X-Dev-User": f"submitter-{unique}", "X-Dev-Org": org_code}
    worker_headers = {"X-Dev-User": f"worker-{unique}", "X-Dev-Org": org_code}

    client.get("/me", headers=submitter_headers)  # JIT-provision (default: viewer)
    client.get("/me", headers=worker_headers)
    _grant_role(db_session, org_code, f"submitter-{unique}", "marker_maker")  # job.submit/read/cancel
    _grant_role(db_session, org_code, f"worker-{unique}", "job_worker")  # job.worker only

    submitted_ids = []
    for i in range(20):
        resp = client.post(
            "/jobs",
            json={"job_type": "marker_nesting_solve", "input_ref": {"i": i}},
            headers=submitter_headers,
        )
        assert resp.status_code == 202, resp.text
        submitted_ids.append(resp.json()["id"])

    resp = client.get("/jobs", params={"status": "queued"}, headers=submitter_headers)
    assert resp.json()["total"] == 20

    # "Scale workers": several worker threads pull from the same queue concurrently. Each thread
    # gets its own DB session (SQLAlchemy sessions aren't thread-safe to share) and drains the
    # queue via app.job_worker.run_one_job until nothing is left to claim.
    processed_ids: list[str] = []
    lock = threading.Lock()

    def worker_loop(worker_instance: str):
        session = SessionLocal()
        try:
            while True:
                job = run_one_job(session, client, worker_headers, worker_instance)
                if job is None:
                    break
                with lock:
                    processed_ids.append(str(job.id))
        finally:
            session.close()

    threads = [threading.Thread(target=worker_loop, args=(f"worker-thread-{n}",)) for n in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=10)

    # Every submitted job was processed exactly once -- no double-claims across concurrent workers.
    assert sorted(processed_ids) == sorted(submitted_ids)
    assert len(set(processed_ids)) == 20

    for job_id in submitted_ids:
        resp = client.get(f"/jobs/{job_id}", headers=submitter_headers)
        assert resp.json()["status"] == "succeeded"
        assert resp.json()["result_ref"] is not None

        events = client.get(f"/jobs/{job_id}/events", headers=submitter_headers).json()
        event_types = [e["event_type"] for e in events]
        assert event_types == ["queued", "picked_up", "progress", "progress", "succeeded"]


def test_job_cancel_while_still_queued(db_session):
    unique = uuid.uuid4().hex[:8]
    org_code = f"JOBCANCEL-{unique}"
    headers = {"X-Dev-User": f"submitter-{unique}", "X-Dev-Org": org_code}
    client.get("/me", headers=headers)
    _grant_role(db_session, org_code, f"submitter-{unique}", "marker_maker")

    resp = client.post(
        "/jobs", json={"job_type": "marker_nesting_solve", "input_ref": {}}, headers=headers
    )
    job_id = resp.json()["id"]

    resp = client.post(f"/jobs/{job_id}/cancel", headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "cancelled"

    events = client.get(f"/jobs/{job_id}/events", headers=headers).json()
    assert events[-1]["event_type"] == "cancelled"


def test_timeout_sweep_fails_a_stale_job(db_session):
    unique = uuid.uuid4().hex[:8]
    org = Organization(name="Timeout Org", code=f"TIMEOUT-{unique}")
    db_session.add(org)
    db_session.flush()
    user = dev_login(db_session, org.id, username=f"u-{unique}", email="u@example.com", full_name="U")
    db_session.flush()

    job = submit_job(db_session, org.id, user.id, "marker_nesting_solve", {}, None)
    db_session.flush()

    # Deliberately induce a timeout, per the exit check's own "when deliberately induced to" --
    # backdate the job past its own timeout_at rather than waiting 40 real minutes.
    job.timeout_at = datetime.now(UTC) - timedelta(seconds=1)
    db_session.commit()

    swept = sweep_timed_out_jobs(db_session)
    assert swept == 1

    db_session.refresh(job)
    assert job.status == "failed"
    assert job.error_detail == "max_delivery_exceeded"

    events = [e.event_type for e in db_session.query(JobEvent).filter_by(job_id=job.id).all()]
    assert "timed_out" in events


def test_job_worker_endpoints_reject_non_worker_actor(db_session):
    unique = uuid.uuid4().hex[:8]
    org_code = f"WORKERPERM-{unique}"
    submitter_headers = {"X-Dev-User": f"submitter-{unique}", "X-Dev-Org": org_code}
    client.get("/me", headers=submitter_headers)
    _grant_role(db_session, org_code, f"submitter-{unique}", "marker_maker")

    resp = client.post(
        "/jobs", json={"job_type": "marker_nesting_solve", "input_ref": {}}, headers=submitter_headers
    )
    job_id = resp.json()["id"]

    # marker_maker holds job.submit/read/cancel but NOT job.worker.
    resp = client.post(f"/jobs/{job_id}/heartbeat", json={"progress_pct": 50}, headers=submitter_headers)
    assert resp.status_code == 403

    resp = client.post(
        f"/jobs/{job_id}/complete", json={"status": "succeeded"}, headers=submitter_headers
    )
    assert resp.status_code == 403
