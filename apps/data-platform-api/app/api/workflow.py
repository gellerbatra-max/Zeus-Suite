"""Section 4.7: workflow status metadata."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import Actor, get_current_actor, get_db
from app.models import WorkflowStatus, WorkflowTransition

router = APIRouter(tags=["workflow"])


@router.get("/workflow-statuses")
def list_workflow_statuses(
    entity_type: str = Query(...),
    db: Session = Depends(get_db),
    actor: Actor = Depends(get_current_actor),  # any authenticated user (Section 4.7)
):
    rows = (
        db.query(WorkflowStatus)
        .filter_by(entity_type=entity_type)
        .order_by(WorkflowStatus.sequence)
        .all()
    )
    return [
        {"code": r.code, "label": r.label, "sequence": r.sequence, "is_initial": r.is_initial, "is_terminal": r.is_terminal}
        for r in rows
    ]


@router.get("/workflow-transitions")
def list_workflow_transitions(
    entity_type: str = Query(...),
    from_status: str = Query(...),
    db: Session = Depends(get_db),
    actor: Actor = Depends(get_current_actor),  # any authenticated user (Section 4.7)
):
    from_row = db.query(WorkflowStatus).filter_by(entity_type=entity_type, code=from_status).one_or_none()
    if from_row is None:
        return []
    rows = db.query(WorkflowTransition).filter_by(entity_type=entity_type, from_status_id=from_row.id).all()
    results = []
    for r in rows:
        to_row = db.get(WorkflowStatus, r.to_status_id)
        results.append({"to_status": to_row.code, "label": to_row.label, "required_permission": r.required_permission})
    return results
