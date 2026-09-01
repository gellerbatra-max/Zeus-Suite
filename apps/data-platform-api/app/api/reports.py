"""Section 4.10: reports."""

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import (
    Actor,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import api_error, not_found
from app.models import ReportDefinition, ReportRun, User
from app.report_service import run_report
from app.schemas import ReportDefinitionOut, ReportRunOut, ReportRunRequest

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/definitions", response_model=list[ReportDefinitionOut])
def list_definitions(
    actor: Actor = Depends(get_current_actor),  # any authenticated user (Section 4.10)
    db: Session = Depends(get_db),
):
    rows = db.query(ReportDefinition).order_by(ReportDefinition.code).all()
    return [
        ReportDefinitionOut(code=r.code, name=r.name, entity_type=r.entity_type, description=r.description)
        for r in rows
    ]


def _run_out(run: ReportRun, report_code: str) -> ReportRunOut:
    return ReportRunOut(
        id=run.id,
        report_code=report_code,
        status=run.status,
        result_inline=run.result_inline,
        requested_at=run.requested_at,
        completed_at=run.completed_at,
    )


@router.post("/run", response_model=ReportRunOut)
def run(
    body: ReportRunRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "report.run", request_id=request_id, entity_type="report", action="report.run")

    definition = db.query(ReportDefinition).filter_by(code=body.report_code).one_or_none()
    if definition is None:
        raise not_found("Report definition")

    report_run = ReportRun(
        report_definition_id=definition.id,
        requested_by=actor.user_id,
        parameters={"entity_id": str(body.entity_id) if body.entity_id else None, "format": body.format},
        status="running",
    )
    db.add(report_run)
    db.flush()

    try:
        result = run_report(db, actor.organization_id, body.report_code, body.entity_id)
    except LookupError as exc:
        report_run.status = "failed"
        report_run.completed_at = datetime.now(UTC)
        db.flush()
        raise not_found("Report target") from exc
    except NotImplementedError as exc:
        report_run.status = "failed"
        report_run.completed_at = datetime.now(UTC)
        db.flush()
        raise api_error(501, "report_not_implemented", str(exc)) from exc
    except ValueError as exc:
        report_run.status = "failed"
        report_run.completed_at = datetime.now(UTC)
        db.flush()
        raise api_error(400, "bad_request", str(exc)) from exc

    report_run.status = "completed"
    report_run.result_inline = result
    report_run.completed_at = datetime.now(UTC)
    db.flush()
    return _run_out(report_run, body.report_code)


@router.get("/runs/{run_id}", response_model=ReportRunOut)
def get_run(
    run_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "report.run", request_id=request_id, entity_type="report", action="report.read")
    report_run = db.get(ReportRun, run_id)
    if report_run is None:
        raise not_found("Report run")
    # report_runs has no organization_id of its own (Section 2.10) -- scope through the
    # requesting user's organization, same pattern as bundle cross-referencing through orders.
    requester = db.get(User, report_run.requested_by)
    if requester is None or requester.organization_id != actor.organization_id:
        raise not_found("Report run")
    definition = db.get(ReportDefinition, report_run.report_definition_id)
    return _run_out(report_run, definition.code)
