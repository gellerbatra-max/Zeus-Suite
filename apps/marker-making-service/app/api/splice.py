"""marker_making_production_plan.md Sec 1.8 (splice marks / fabric-roll handling). Manual mark
CRUD and settings are thin proxies over data-platform-api's `dmp.splice_marks` and the marker's
own `splice_min_length`/`splice_max_length`/`splice_margin`/`splice_separation` fields. The real
business logic -- "Splice/Automatic" -- lives here, since this service is the one that already
interprets `placement_data` everywhere else (material calc's marker-length math, matching
guidance, fuse-block bounds).

**No real fabric-roll entity exists anywhere in this platform** (no roll length, no roll
inventory) -- so unlike Gerber's real algorithm (which reads actual roll lengths from fabric-roll
records), auto-placement here takes a `roll_length` directly on each call: it's the honest,
explicit stand-in for "how long is one roll of fabric on the spreading table," a parameter the
operator supplies rather than a value looked up from real inventory data.

**Auto-placement algorithm** (a real but deliberately simplified interpretation of "Splice/
Automatic... start must be covered by the new roll, end by the original roll"): splice points fall
at every multiple of `roll_length` along the computed marker length (the same X-axis length
convention `material.py`'s `computed_marker_length` already uses); each mark's own length is
`clamp(margin * 2, min_length, max_length)`, centered on the boundary and clipped to stay within
the marker; boundaries within `separation` of either marker edge are skipped entirely, per
"Separation (distance from marker edge)." Each generated mark gets `roll_id=f"roll-{n+1}"` --
"roll 1" is implicitly whatever covers the marker from x=0, "roll 2" begins at the first splice,
and so on -- a natural, forward-compatible source for Sec 1.13's bundle-tag `lot/roll_id` field.
Regenerating **only replaces marks with `source='auto'`** -- manual marks are left untouched,
per "manual entries take priority over auto-generated ones," so an operator can hand-correct one
splice and re-run Auto without losing that edit.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    AutoSpliceRequest,
    SpliceMarkCreateRequest,
    SpliceMarkOut,
    SpliceMarkPatchRequest,
    SpliceSettingsOut,
    SpliceSettingsPatchRequest,
)

router = APIRouter(tags=["splice-marks"])


def _shape_mark(raw: dict) -> SpliceMarkOut:
    return SpliceMarkOut(
        id=raw["id"], marker_id=raw["marker_id"], start_x=raw["start_x"], end_x=raw["end_x"],
        source=raw["source"], roll_id=raw["roll_id"], version=raw["version"],
    )


def _computed_marker_length(client: PlatformClient, marker_id: str) -> float | None:
    placements = client.get(f"/markers/{marker_id}/pieces")
    if not placements:
        return None
    max_x2 = 0.0
    for p in placements:
        data = p.get("placement_data") or {}
        max_x2 = max(max_x2, data.get("x", 0.0) + data.get("width", 0.0))
    return max_x2


def _build_settings(marker: dict) -> SpliceSettingsOut:
    return SpliceSettingsOut(
        min_length=marker.get("splice_min_length"), max_length=marker.get("splice_max_length"),
        margin=marker.get("splice_margin"), separation=marker.get("splice_separation"),
    )


@router.get("/markers/{marker_id}/splice/settings", response_model=SpliceSettingsOut)
def get_splice_settings(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _build_settings(client.get(f"/markers/{marker_id}"))


@router.patch("/markers/{marker_id}/splice/settings", response_model=SpliceSettingsOut)
def patch_splice_settings(
    marker_id: str, body: SpliceSettingsPatchRequest, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")
    patch = {f"splice_{field}": value for field, value in body.model_dump(exclude_none=True).items()}
    if patch:
        client.patch(f"/markers/{marker_id}", json=patch, headers={"If-Match-Version": str(marker["version"])})
        marker = client.get(f"/markers/{marker_id}")
    return _build_settings(marker)


@router.get("/markers/{marker_id}/splice-marks")
def list_splice_marks(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    raw = client.get(f"/markers/{marker_id}/splice-marks")
    return [_shape_mark(item) for item in raw]


@router.post("/markers/{marker_id}/splice-marks", response_model=SpliceMarkOut)
def create_splice_mark(
    marker_id: str, body: SpliceMarkCreateRequest, client: PlatformClient = Depends(get_platform_client)
):
    raw = client.post(
        f"/markers/{marker_id}/splice-marks",
        json={"start_x": body.start_x, "end_x": body.end_x, "source": "manual", "roll_id": body.roll_id},
    )
    return _shape_mark(raw)


@router.patch("/splice-marks/{mark_id}", response_model=SpliceMarkOut)
def patch_splice_mark(
    mark_id: str, body: SpliceMarkPatchRequest, client: PlatformClient = Depends(get_platform_client)
):
    current = client.get(f"/splice-marks/{mark_id}")
    raw = client.patch(
        f"/splice-marks/{mark_id}",
        json=body.model_dump(exclude_none=True),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape_mark(raw)


@router.delete("/splice-marks/{mark_id}", status_code=204)
def delete_splice_mark(mark_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/splice-marks/{mark_id}")


@router.delete("/markers/{marker_id}/splice-marks", status_code=204)
def delete_all_splice_marks(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/markers/{marker_id}/splice-marks")


@router.post("/markers/{marker_id}/splice/auto")
def auto_splice(marker_id: str, body: AutoSpliceRequest, client: PlatformClient = Depends(get_platform_client)):
    if body.roll_length <= 0:
        raise HTTPException(400, "roll_length must be greater than 0.")

    marker = client.get(f"/markers/{marker_id}")
    settings = (
        marker.get("splice_min_length"), marker.get("splice_max_length"),
        marker.get("splice_margin"), marker.get("splice_separation"),
    )
    if any(value is None for value in settings):
        raise HTTPException(400, "Set splice_min_length/splice_max_length/splice_margin/splice_separation first.")
    min_length, max_length, margin, separation = settings

    marker_length = _computed_marker_length(client, marker_id)
    if marker_length is None:
        raise HTTPException(400, "No placed pieces yet -- nothing to splice.")

    mark_length = max(min_length, min(max_length, margin * 2))

    # Regenerating only replaces 'auto' marks -- manual ones are untouched, per "manual entries
    # take priority over auto-generated ones."
    client.delete(f"/markers/{marker_id}/splice-marks", params={"source": "auto"})

    n = 1
    while n * body.roll_length < marker_length:
        boundary = n * body.roll_length
        if separation <= boundary <= marker_length - separation:
            client.post(
                f"/markers/{marker_id}/splice-marks",
                json={
                    "start_x": max(0.0, boundary - mark_length / 2),
                    "end_x": min(marker_length, boundary + mark_length / 2),
                    "source": "auto",
                    "roll_id": f"roll-{n + 1}",
                },
            )
        n += 1

    raw = client.get(f"/markers/{marker_id}/splice-marks")
    return [_shape_mark(item) for item in raw]
