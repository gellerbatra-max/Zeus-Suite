"""Section 4.10: reports. Every report in this build runs synchronously and returns
`result_inline` -- none of the seeded report codes need the async job path Section 4.10 describes
for "slower/larger reports," since even `all_piece`/`all_marker` over a single org are cheap
queries. `piece_perimeter`, `all_layrule`, `all_plot`, `all_cut`, and `splice` are left
unimplemented on purpose: they need the piece/marker geometry and cut-data Section 2.4/2.6
explicitly store as opaque blobs this platform never parses (that's Pattern Design's and Marker
Making's domain) -- a real implementation belongs in one of those apps' builds, not here.
"""

import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models import Marker, Piece, WorkflowStatus

UNIMPLEMENTED_CODES = {"piece_perimeter", "all_layrule", "all_plot", "all_cut", "splice"}


def _piece_summary(session: Session, piece: Piece) -> dict[str, Any]:
    status = session.get(WorkflowStatus, piece.workflow_status_id)
    return {
        "id": str(piece.id),
        "piece_code": piece.piece_code,
        "piece_name": piece.piece_name,
        "piece_type": piece.piece_type,
        "workflow_status": status.code,
        "folder_id": str(piece.folder_id),
        "updated_at": piece.updated_at.isoformat(),
    }


def _marker_summary(session: Session, marker: Marker) -> dict[str, Any]:
    status = session.get(WorkflowStatus, marker.workflow_status_id)
    return {
        "id": str(marker.id),
        "marker_code": marker.marker_code,
        "marker_name": marker.marker_name,
        "workflow_status": status.code,
        "folder_id": str(marker.folder_id),
        "updated_at": marker.updated_at.isoformat(),
    }


def run_report(
    session: Session, org_id: uuid.UUID, report_code: str, entity_id: uuid.UUID | None
) -> dict[str, Any]:
    if report_code == "single_piece":
        if entity_id is None:
            raise ValueError("single_piece requires entity_id (a piece id).")
        piece = session.get(Piece, entity_id)
        if piece is None or piece.organization_id != org_id:
            raise LookupError("Piece not found.")
        return _piece_summary(session, piece)

    if report_code == "all_piece":
        query = session.query(Piece).filter(Piece.organization_id == org_id, Piece.deleted_at.is_(None))
        if entity_id is not None:
            query = query.filter(Piece.folder_id == entity_id)
        return {"pieces": [_piece_summary(session, p) for p in query.all()]}

    if report_code == "all_marker":
        query = session.query(Marker).filter(Marker.organization_id == org_id, Marker.deleted_at.is_(None))
        if entity_id is not None:
            query = query.filter(Marker.folder_id == entity_id)
        return {"markers": [_marker_summary(session, m) for m in query.all()]}

    if report_code in UNIMPLEMENTED_CODES:
        raise NotImplementedError(
            f"'{report_code}' needs piece/marker geometry or cut-data this platform stores as an "
            "opaque blob -- implement it in Pattern Design or Marker Making, not here."
        )

    raise ValueError(f"Unknown report code '{report_code}'.")
