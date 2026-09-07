"""marker_making_production_plan.md Sec 1.7 (material calculation / utilization). The platform
only stores the marker-level fields (fabric_width, marker_length, ply_count, utilization_pct,
fabric_weight_per_unit_area) and order-level targets (target_length, target_utilization_pct) --
it never computes them (data-platform-api's own README: it stores/returns JSON faithfully and
doesn't interpret it). This service does the actual math, since it's the one that already
interprets placement_data everywhere else (matching guidance, fuse-block bounds).

**Length-axis convention**: this app's marker canvas draws the cut length along X (the same
convention `matching.py`'s bite-boundary validation already assumes -- "the marker's X axis is
the cutter's bite/length axis"), so `computed_marker_length` here is `max(x + width)` across
placements, not `max(y + height)`.

**Simplifications, explicit**: `computed_total_piece_area`/`computed_total_perimeter` sum each
placement's raw (unrotated) width*height / 2*(width+height) times its `quantity` -- the same
axis-aligned, rotation-ignoring convention already used by `block_buffer.py`'s `_compute_bounds`
and the canvas's own overlap detection. Piece-level area/perimeter for a *single* selected piece
needs no endpoint at all -- the frontend already has that piece's width/height locally and computes
it directly. "Estimate Material" (cap-nesting, per-mode breakdown across Normal/Reverse/
Interleaving) and the standalone material-calculation-file what-if tool are deferred -- both need
multiple real nesting variants to compare, which this app's single manual/Engine-B-stub canvas
doesn't produce.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_platform_client
from app.platform_client import PlatformClient, PlatformError
from app.schemas import (
    MaterialPatchRequest,
    MaterialSummaryOut,
    MaterialWeightOut,
    MaterialWeightRequest,
    OrderTargetPatchRequest,
    RequiredLengthOut,
    RequiredLengthRequest,
)

router = APIRouter(tags=["material"])


def _compute_geometry(client: PlatformClient, marker_id: str) -> dict:
    placements = client.get(f"/markers/{marker_id}/pieces")
    if not placements:
        return {"computed_marker_length": None, "computed_total_piece_area": None, "computed_total_perimeter": None}

    total_area = 0.0
    total_perimeter = 0.0
    max_x2 = 0.0
    for p in placements:
        data = p.get("placement_data") or {}
        x, width, height = data.get("x", 0.0), data.get("width", 0.0), data.get("height", 0.0)
        quantity = p.get("quantity", 1)
        total_area += width * height * quantity
        total_perimeter += 2 * (width + height) * quantity
        max_x2 = max(max_x2, x + width)

    return {
        "computed_marker_length": max_x2,
        "computed_total_piece_area": total_area,
        "computed_total_perimeter": total_perimeter,
    }


def _fetch_marker_and_order(client: PlatformClient, marker_id: str) -> tuple[dict, dict | None]:
    marker = client.get(f"/markers/{marker_id}")
    order = None
    if marker.get("order_id"):
        try:
            order = client.get(f"/orders/{marker['order_id']}")
        except PlatformError:
            order = None
    return marker, order


def _build_summary(client: PlatformClient, marker_id: str) -> MaterialSummaryOut:
    marker, order = _fetch_marker_and_order(client, marker_id)
    geometry = _compute_geometry(client, marker_id)

    computed_utilization_pct = None
    fabric_width = marker.get("fabric_width")
    if fabric_width and geometry["computed_marker_length"]:
        computed_utilization_pct = round(
            geometry["computed_total_piece_area"] / (fabric_width * geometry["computed_marker_length"]) * 100, 2
        )

    return MaterialSummaryOut(
        fabric_width=fabric_width,
        ply_count=marker.get("ply_count"),
        fabric_weight_per_unit_area=marker.get("fabric_weight_per_unit_area"),
        marker_length=marker.get("marker_length"),
        utilization_pct=marker.get("utilization_pct"),
        computed_utilization_pct=computed_utilization_pct,
        target_length=order.get("target_length") if order else None,
        target_utilization_pct=order.get("target_utilization_pct") if order else None,
        **geometry,
    )


@router.get("/markers/{marker_id}/material/summary", response_model=MaterialSummaryOut)
def get_material_summary(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _build_summary(client, marker_id)


@router.post("/markers/{marker_id}/material/apply-computed", response_model=MaterialSummaryOut)
def apply_computed_material(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    """Persists the live-computed marker_length/utilization_pct onto the platform marker record,
    so they survive as the marker's stored values instead of being recomputed from scratch every
    time (and so other tools reading MarkerOut directly, e.g. a future report, see them too)."""
    marker = client.get(f"/markers/{marker_id}")
    geometry = _compute_geometry(client, marker_id)
    if geometry["computed_marker_length"] is None:
        raise HTTPException(400, "No placed pieces yet -- nothing to compute.")

    patch: dict = {"marker_length": geometry["computed_marker_length"]}
    fabric_width = marker.get("fabric_width")
    if fabric_width:
        patch["utilization_pct"] = round(
            geometry["computed_total_piece_area"] / (fabric_width * geometry["computed_marker_length"]) * 100, 2
        )
    client.patch(f"/markers/{marker_id}", json=patch, headers={"If-Match-Version": str(marker["version"])})
    return _build_summary(client, marker_id)


@router.patch("/markers/{marker_id}/material", response_model=MaterialSummaryOut)
def patch_material(marker_id: str, body: MaterialPatchRequest, client: PlatformClient = Depends(get_platform_client)):
    marker = client.get(f"/markers/{marker_id}")
    patch = body.model_dump(exclude_none=True)
    if patch:
        client.patch(f"/markers/{marker_id}", json=patch, headers={"If-Match-Version": str(marker["version"])})
    return _build_summary(client, marker_id)


@router.patch("/markers/{marker_id}/material/target", response_model=MaterialSummaryOut)
def patch_material_target(
    marker_id: str, body: OrderTargetPatchRequest, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")
    if not marker.get("order_id"):
        raise HTTPException(400, "This marker has no linked order -- there's nowhere to store a target.")
    order = client.get(f"/orders/{marker['order_id']}")
    patch = body.model_dump(exclude_none=True)
    if patch:
        client.patch(f"/orders/{order['id']}", json=patch, headers={"If-Match-Version": str(order["version"])})
    return _build_summary(client, marker_id)


@router.post("/markers/{marker_id}/material/required-length", response_model=RequiredLengthOut)
def calculate_required_length(
    marker_id: str, body: RequiredLengthRequest, client: PlatformClient = Depends(get_platform_client)
):
    """"Calculate Efficiency and Marker Length": given a target efficiency %, computes the
    material length required to hit it -- a pure calculation, not persisted anywhere."""
    if body.target_efficiency_pct <= 0:
        raise HTTPException(400, "target_efficiency_pct must be greater than 0.")
    marker = client.get(f"/markers/{marker_id}")
    fabric_width = marker.get("fabric_width")
    if not fabric_width:
        raise HTTPException(400, "This marker has no fabric_width set yet.")
    geometry = _compute_geometry(client, marker_id)
    if geometry["computed_total_piece_area"] is None:
        raise HTTPException(400, "No placed pieces yet -- nothing to compute.")
    required_length = geometry["computed_total_piece_area"] / (fabric_width * body.target_efficiency_pct / 100)
    return RequiredLengthOut(required_length=round(required_length, 2))


@router.post("/markers/{marker_id}/material/weight", response_model=MaterialWeightOut)
def calculate_material_weight(
    marker_id: str, body: MaterialWeightRequest, client: PlatformClient = Depends(get_platform_client)
):
    """width x length x plies x weight-per-unit-area. Any of length/plies/weight-per-unit-area
    not supplied in the request body falls back to the marker's own stored values."""
    marker = client.get(f"/markers/{marker_id}")
    fabric_width = marker.get("fabric_width")
    weight_per_unit_area = body.weight_per_unit_area or marker.get("fabric_weight_per_unit_area")
    plies = body.plies or marker.get("ply_count")
    length = body.length or marker.get("marker_length")
    if length is None:
        geometry = _compute_geometry(client, marker_id)
        length = geometry["computed_marker_length"]

    missing = [
        name for name, value in (
            ("fabric_width", fabric_width), ("length", length), ("plies", plies),
            ("weight_per_unit_area", weight_per_unit_area),
        ) if not value
    ]
    if missing:
        raise HTTPException(400, f"Missing value(s) needed for weight calculation: {', '.join(missing)}.")

    weight = fabric_width * length * plies * weight_per_unit_area
    return MaterialWeightOut(weight=round(weight, 4))
