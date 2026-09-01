"""The marker-making canvas's single load/save surface. Assembles everything the canvas needs
from data-platform-api's real, already-built endpoints -- no new platform schema, per the plan's
resolution of the marker_making_production_plan.md vs. data_management_platform_plan.md schema
mismatch (see the plan file / commit message for the full reasoning).

A style already *is* Gerber's "model" concept (the full piece set for one garment) -- so "which
pieces does this marker's order call for" is answered by walking marker -> order -> style ->
style_pieces -> pieces, all of which already exist on the platform.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_platform_client
from app.platform_client import PlatformClient, PlatformError
from app.schemas import (
    SaveWorkspaceRequest,
    WorkspaceOut,
    WorkspacePiece,
    WorkspacePlacement,
)
from app.synthetic_geometry import synthetic_dimensions

router = APIRouter(tags=["workspace"])

# The marker workflow_transitions seeded on the platform (Milestone 1) only allow
# unmade -> needs_approval -> {partial, made} -> approved -- there is no direct unmade -> made/
# partial, and no backward transition at all. This walks the shortest legal forward path;
# degrading (e.g. made -> partial because a piece got unplaced) isn't a modeled transition, so
# that case is left as a no-op rather than failing the save -- the placement data itself still
# saves regardless of what happens to the status field.
_FORWARD_PATH = {
    ("unmade", "needs_approval"): "needs_approval",
    ("unmade", "partial"): "needs_approval",
    ("unmade", "made"): "needs_approval",
    ("needs_approval", "partial"): "partial",
    ("needs_approval", "made"): "made",
    ("partial", "made"): "made",
}


def _advance_marker_status(client: PlatformClient, marker_id: str, current: str, target: str) -> None:
    if current == target:
        return
    next_hop = _FORWARD_PATH.get((current, target))
    if next_hop is None:
        return  # no legal path (e.g. asked to degrade) -- leave status as-is
    try:
        client.post(f"/markers/{marker_id}/status", json={"to_status": next_hop})
    except PlatformError:
        return
    if next_hop != target:
        _advance_marker_status(client, marker_id, next_hop, target)


def _assemble_workspace(marker_id: str, client: PlatformClient) -> WorkspaceOut:
    marker = client.get(f"/markers/{marker_id}")

    style = None
    if marker.get("order_id"):
        try:
            order = client.get(f"/orders/{marker['order_id']}")
            if order.get("style_id"):
                style = client.get(f"/styles/{order['style_id']}")
        except PlatformError:
            style = None

    available_pieces: list[WorkspacePiece] = []
    if style is not None:
        style_pieces = client.get(f"/styles/{style['id']}/pieces")
        for link in style_pieces:
            piece = client.get(f"/pieces/{link['piece_id']}")
            width, height = synthetic_dimensions(piece["piece_code"])
            available_pieces.append(
                WorkspacePiece(
                    id=piece["id"], piece_code=piece["piece_code"], piece_name=piece["piece_name"],
                    width=width, height=height,
                )
            )

    raw_placements = client.get(f"/markers/{marker_id}/pieces")
    placements = [
        WorkspacePlacement(
            piece_id=p["piece_id"],
            piece_version_id=p.get("piece_version_id"),
            size_code=p["size_code"],
            quantity=p["quantity"],
            placement_data=p.get("placement_data") or {},
        )
        for p in raw_placements
    ]

    return WorkspaceOut(
        marker_id=marker["id"],
        marker_code=marker["marker_code"],
        workflow_status=marker["workflow_status"]["code"],
        order_id=marker.get("order_id"),
        style_id=style["id"] if style else None,
        matching_method=marker.get("matching_method"),
        matching_rule_table_id=marker.get("matching_rule_table_id"),
        available_pieces=available_pieces,
        placements=placements,
    )


@router.get("/markers/{marker_id}/workspace", response_model=WorkspaceOut)
def get_workspace(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _assemble_workspace(marker_id, client)


@router.put("/markers/{marker_id}/workspace", response_model=WorkspaceOut)
def save_workspace(
    marker_id: str, body: SaveWorkspaceRequest, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")

    bulk_rows = []
    for placement in body.placements:
        piece = client.get(f"/pieces/{placement.piece_id}")
        version_id = piece.get("current_version_id")
        if version_id is None:
            raise HTTPException(
                422, f"Piece {placement.piece_id} has no committed version yet -- cannot place it on a marker."
            )
        bulk_rows.append(
            {
                "piece_id": placement.piece_id,
                "piece_version_id": version_id,
                "size_code": placement.size_code,
                "quantity": placement.quantity,
                "placement_data": placement.placement_data.model_dump(),
            }
        )

    client.put(f"/markers/{marker_id}/pieces", json=bulk_rows)

    style_piece_ids: set[str] = set()
    if marker.get("order_id"):
        try:
            order = client.get(f"/orders/{marker['order_id']}")
            if order.get("style_id"):
                style_pieces = client.get(f"/styles/{order['style_id']}/pieces")
                style_piece_ids = {p["piece_id"] for p in style_pieces}
        except PlatformError:
            pass

    placed_piece_ids = {p.piece_id for p in body.placements}
    if not placed_piece_ids:
        target_status = "unmade"
    elif style_piece_ids and placed_piece_ids >= style_piece_ids:
        target_status = "made"
    else:
        target_status = "partial"

    _advance_marker_status(client, marker_id, marker["workflow_status"]["code"], target_status)

    return _assemble_workspace(marker_id, client)
