"""marker_making_production_plan.md Sec 1.9 (marker transformations). Scoped to the three
capabilities confirmed with the user: whole-marker Flip X/Y/XY, Shrink and Stretch, and Change
Width of Marker.

**Flip X/Y/XY needs no endpoint here at all** -- it's a pure transform of the already-loaded
placements (mirror each piece's position within the tight bounding box of everything currently
placed, toggle that piece's own flip flag), computed entirely client-side in
`marker-making-app/src/geometry.ts` and persisted through the existing
`PUT /markers/{id}/workspace` save path, exactly like single-piece rotate/flip already work. That
mirrors this app's existing precedent (single-piece transforms are plain local state edits, not
server round trips) more closely than inventing a new endpoint would.

**Shrink and Stretch** *is* server-backed, because the plan frames it as an order-level setting
("entered on the order... read at cut-time"), not a one-off canvas action -- `shrink_x_pct`/
`shrink_y_pct` live on `dmp.orders` (migration 0011). Since no real cut-time pipeline exists yet
(Sec 1.10 is blocked on a `cutter_parameter_table`), `apply-shrink-stretch` here is a stand-in:
it scales the *current* placements immediately, anchored at their own combined bounding-box
top-left corner (not the canvas origin) so the layout doesn't drift if pieces don't start at
(0,0). **Known simplification, flagged explicitly**: nothing clears `shrink_x_pct`/`shrink_y_pct`
after applying, so clicking Apply twice in a row double-shrinks -- there's no "already applied"
flag on this stand-in action (a real cut-time reader would apply it exactly once, at generation
time, never mutating stored placements at all).

**Change Width of Marker** just updates `markers.fabric_width` (already a platform column,
already patchable) through the normal proxy path. **"Auto-rearranges pieces" is explicitly NOT
implemented** -- there's no real nesting algorithm to call (Engine B is still Milestone 6's
sleep-and-echo stub); changing the width only changes the canvas's fabric-width axis, pieces stay
exactly where they were and may now overflow or leave more slack, which the operator has to
notice and fix by hand.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.workspace import _assemble_workspace
from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    ChangeWidthOut,
    ChangeWidthRequest,
    ShrinkStretchPatchRequest,
    TransformSettingsOut,
    WorkspaceOut,
)

router = APIRouter(tags=["marker-transform"])


def _build_settings(client: PlatformClient, marker_id: str) -> TransformSettingsOut:
    marker = client.get(f"/markers/{marker_id}")
    order = None
    if marker.get("order_id"):
        order = client.get(f"/orders/{marker['order_id']}")
    return TransformSettingsOut(
        fabric_width=marker.get("fabric_width"),
        shrink_x_pct=(order or {}).get("shrink_x_pct"),
        shrink_y_pct=(order or {}).get("shrink_y_pct"),
    )


@router.get("/markers/{marker_id}/transform/settings", response_model=TransformSettingsOut)
def get_transform_settings(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _build_settings(client, marker_id)


@router.patch("/markers/{marker_id}/transform/shrink-stretch", response_model=TransformSettingsOut)
def patch_shrink_stretch(
    marker_id: str, body: ShrinkStretchPatchRequest, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")
    if not marker.get("order_id"):
        raise HTTPException(400, "This marker has no linked order -- there's nowhere to store shrink/stretch settings.")
    order = client.get(f"/orders/{marker['order_id']}")
    patch = body.model_dump(exclude_none=True)
    if patch:
        client.patch(f"/orders/{order['id']}", json=patch, headers={"If-Match-Version": str(order["version"])})
    return _build_settings(client, marker_id)


@router.post("/markers/{marker_id}/transform/apply-shrink-stretch", response_model=WorkspaceOut)
def apply_shrink_stretch(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    marker = client.get(f"/markers/{marker_id}")
    order = client.get(f"/orders/{marker['order_id']}") if marker.get("order_id") else None
    shrink_x_pct = (order or {}).get("shrink_x_pct")
    shrink_y_pct = (order or {}).get("shrink_y_pct")
    if shrink_x_pct is None and shrink_y_pct is None:
        raise HTTPException(400, "This marker's order has no shrink_x_pct/shrink_y_pct set.")

    placements = client.get(f"/markers/{marker_id}/pieces")
    if not placements:
        raise HTTPException(400, "No placed pieces yet -- nothing to scale.")

    min_x = min(p["placement_data"].get("x", 0.0) for p in placements)
    min_y = min(p["placement_data"].get("y", 0.0) for p in placements)
    scale_x = 1 + (shrink_x_pct or 0) / 100
    scale_y = 1 + (shrink_y_pct or 0) / 100

    bulk_rows = []
    for p in placements:
        data = dict(p["placement_data"])
        x, y = data.get("x", 0.0), data.get("y", 0.0)
        width, height = data.get("width", 0.0), data.get("height", 0.0)
        data["x"] = min_x + (x - min_x) * scale_x
        data["y"] = min_y + (y - min_y) * scale_y
        data["width"] = width * scale_x
        data["height"] = height * scale_y
        bulk_rows.append(
            {
                "piece_id": p["piece_id"], "piece_version_id": p["piece_version_id"],
                "size_code": p["size_code"], "quantity": p["quantity"], "placement_data": data,
            }
        )
    client.put(f"/markers/{marker_id}/pieces", json=bulk_rows)
    return _assemble_workspace(marker_id, client)


@router.post("/markers/{marker_id}/transform/change-width", response_model=ChangeWidthOut)
def change_width(marker_id: str, body: ChangeWidthRequest, client: PlatformClient = Depends(get_platform_client)):
    marker = client.get(f"/markers/{marker_id}")
    client.patch(
        f"/markers/{marker_id}", json={"fabric_width": body.fabric_width},
        headers={"If-Match-Version": str(marker["version"])},
    )
    return ChangeWidthOut(fabric_width=body.fabric_width)
