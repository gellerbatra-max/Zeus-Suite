"""Section 4.7: the shared workflow-transition handler every per-entity `POST
/{resource}/{id}/status` endpoint uses -- look up the entity's current status, confirm a row in
`workflow_transitions` exists for `(entity_type, from_status_id, to_status_id)`, confirm the
caller holds that row's `required_permission`, then let the caller apply the update."""

from dataclasses import dataclass

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import WorkflowStatus, WorkflowTransition


class IllegalTransitionError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail={"error": {"code": "illegal_transition", "message": detail}})


@dataclass
class TransitionPlan:
    from_status: WorkflowStatus
    to_status: WorkflowStatus
    required_permission: str


def plan_transition(session: Session, entity_type: str, current_status_id: int, to_status_code: str) -> TransitionPlan:
    """Resolves and validates a requested status transition without applying it or checking
    permissions -- the caller checks `required_permission` via `require_permission_or_raise`
    (app.deps) so the same permission-check-then-audit-write path is used everywhere."""
    to_status = (
        session.query(WorkflowStatus).filter_by(entity_type=entity_type, code=to_status_code).one_or_none()
    )
    if to_status is None:
        raise IllegalTransitionError(f"'{to_status_code}' is not a known status for entity type '{entity_type}'.")

    from_status = session.get(WorkflowStatus, current_status_id)

    transition = (
        session.query(WorkflowTransition)
        .filter_by(entity_type=entity_type, from_status_id=current_status_id, to_status_id=to_status.id)
        .one_or_none()
    )
    if transition is None:
        raise IllegalTransitionError(
            f"No legal transition from '{from_status.code if from_status else current_status_id}' "
            f"to '{to_status_code}' for entity type '{entity_type}'."
        )

    return TransitionPlan(from_status=from_status, to_status=to_status, required_permission=transition.required_permission)
