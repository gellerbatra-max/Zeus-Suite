"""marker_making_production_plan.md Sec 1.5 (layrules automation). Layrule Search Parameter
Table CRUD is a thin proxy over the platform's `layrule_search_tables` (mirrors
`block_buffer.py`'s rule-table pattern). The real work lives in **capture** and **apply**, since
this service is the one that interprets `placement_data` everywhere else:

- **Capture** snapshots a marker's *current* placements (`GET /markers/{id}/pieces`, the exact
  same shape the platform stores) into a new named `layrule` -- this *is* "Auto-Store Layrule"
  [GMM] made concrete: there's no background hook system anywhere in this app to fire it on every
  save automatically, so it's an explicit one-click action instead (the frontend can, and does,
  trigger it right after a normal Save to approximate "automatic").
- **Apply** takes a captured layrule and reproduces its layout on a *different* marker: it
  cross-references the layrule's piece ids against the target marker's available style pieces
  (via `workspace.py`'s `_assemble_workspace`, reused rather than duplicated), applying only the
  intersection and reporting the rest as `unmatched_piece_ids` -- the real expression of "best
  suited to repeat orders with the same models/sizes... same-or-fewer piece count." If the target
  marker has a `layrule_search_table_id` linked, its criteria get real teeth here:
  `area_compare`/`area_deviation_pct` compares the layrule's captured total piece area against the
  target marker's own available-piece area and rejects (409) an apply that deviates past the
  threshold -- the concrete form of "changing these settings can invalidate previously saved
  layrules"; `allow_overrides=false` refuses to apply onto a marker that already has any
  placements, protecting manual work from being silently clobbered.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.api.workspace import _assemble_workspace
from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    ApplyLayruleRequest,
    ApplyLayruleResult,
    CaptureLayruleRequest,
    LayruleOut,
    LayrulePatchRequest,
    LayruleSearchTableCreateRequest,
    LayruleSearchTableOut,
    LayruleSearchTablePatchRequest,
    LayruleSettingsPatchRequest,
)

router = APIRouter(tags=["layrules"])


def _shape_search_table(raw: dict) -> LayruleSearchTableOut:
    return LayruleSearchTableOut(
        id=raw["id"], name=raw["name"], area_compare=raw["area_compare"],
        area_deviation_pct=raw["area_deviation_pct"], copy_dynamics=raw["copy_dynamics"],
        allow_overrides=raw["allow_overrides"], include_marker_name=raw["include_marker_name"],
        include_marker_description=raw["include_marker_description"], comment=raw["comment"],
        version=raw["version"],
    )


def _shape_layrule(raw: dict) -> LayruleOut:
    return LayruleOut(
        id=raw["id"], name=raw["name"], source_marker_id=raw["source_marker_id"],
        piece_count=raw["piece_count"], comment=raw["comment"], version=raw["version"],
    )


# -- Layrule Search Parameter Table (thin proxy) --------------------------------------------------


@router.post("/layrule-search-tables", response_model=LayruleSearchTableOut)
def create_layrule_search_table(
    body: LayruleSearchTableCreateRequest, client: PlatformClient = Depends(get_platform_client)
):
    if body.area_deviation_pct < 0:
        raise HTTPException(400, "area_deviation_pct must be >= 0.")
    raw = client.post("/layrule-search-tables", json=body.model_dump())
    return _shape_search_table(raw)


@router.get("/layrule-search-tables")
def list_layrule_search_tables(client: PlatformClient = Depends(get_platform_client)):
    raw = client.get("/layrule-search-tables")
    return {**raw, "items": [_shape_search_table(item) for item in raw["items"]]}


@router.get("/layrule-search-tables/{table_id}", response_model=LayruleSearchTableOut)
def get_layrule_search_table(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _shape_search_table(client.get(f"/layrule-search-tables/{table_id}"))


@router.patch("/layrule-search-tables/{table_id}", response_model=LayruleSearchTableOut)
def patch_layrule_search_table(
    table_id: str, body: LayruleSearchTablePatchRequest, client: PlatformClient = Depends(get_platform_client)
):
    if body.area_deviation_pct is not None and body.area_deviation_pct < 0:
        raise HTTPException(400, "area_deviation_pct must be >= 0.")
    current = client.get(f"/layrule-search-tables/{table_id}")
    raw = client.patch(
        f"/layrule-search-tables/{table_id}",
        json=body.model_dump(exclude_none=True),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape_search_table(raw)


@router.delete("/layrule-search-tables/{table_id}", status_code=204)
def delete_layrule_search_table(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/layrule-search-tables/{table_id}")


# -- Layrules (thin proxy for list/get/patch/delete; capture/apply below are the real logic) ------


@router.get("/layrules")
def list_layrules(client: PlatformClient = Depends(get_platform_client)):
    raw = client.get("/layrules")
    return {**raw, "items": [_shape_layrule(item) for item in raw["items"]]}


@router.get("/layrules/{layrule_id}", response_model=LayruleOut)
def get_layrule(layrule_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _shape_layrule(client.get(f"/layrules/{layrule_id}"))


@router.patch("/layrules/{layrule_id}", response_model=LayruleOut)
def patch_layrule(layrule_id: str, body: LayrulePatchRequest, client: PlatformClient = Depends(get_platform_client)):
    current = client.get(f"/layrules/{layrule_id}")
    raw = client.patch(
        f"/layrules/{layrule_id}", json=body.model_dump(exclude_none=True),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape_layrule(raw)


@router.delete("/layrules/{layrule_id}", status_code=204)
def delete_layrule(layrule_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/layrules/{layrule_id}")


# -- Marker-scoped actions: capture / apply / settings ---------------------------------------------


@router.post("/markers/{marker_id}/layrules/capture", response_model=LayruleOut)
def capture_layrule(
    marker_id: str, body: CaptureLayruleRequest, client: PlatformClient = Depends(get_platform_client)
):
    placements = client.get(f"/markers/{marker_id}/pieces")
    if not placements:
        raise HTTPException(400, "No placements yet -- nothing to capture.")
    raw = client.post(
        "/layrules",
        json={"name": body.name, "source_marker_id": marker_id, "placements_json": placements, "comment": body.comment},
    )
    return _shape_layrule(raw)


@router.post("/markers/{marker_id}/layrules/apply", response_model=ApplyLayruleResult)
def apply_layrule(marker_id: str, body: ApplyLayruleRequest, client: PlatformClient = Depends(get_platform_client)):
    layrule = client.get(f"/layrules/{body.layrule_id}")
    marker = client.get(f"/markers/{marker_id}")
    workspace = _assemble_workspace(marker_id, client)
    available_by_id = {p.id: p for p in workspace.available_pieces}

    search_table = None
    if marker.get("layrule_search_table_id"):
        search_table = client.get(f"/layrule-search-tables/{marker['layrule_search_table_id']}")

    if search_table and not search_table.get("allow_overrides", True):
        existing = client.get(f"/markers/{marker_id}/pieces")
        if existing:
            raise HTTPException(
                409,
                "This marker already has placements and Allow Overrides is disabled on its "
                "linked layrule search table.",
            )

    layrule_area = sum(
        p["placement_data"].get("width", 0.0) * p["placement_data"].get("height", 0.0) * p.get("quantity", 1)
        for p in layrule["placements_json"]
    )
    marker_area = sum(p.width * p.height for p in workspace.available_pieces)
    area_deviation_pct = None
    if layrule_area or marker_area:
        area_deviation_pct = abs(layrule_area - marker_area) / max(layrule_area, marker_area, 1e-9) * 100

    if search_table and search_table.get("area_compare", True) and area_deviation_pct is not None:
        threshold = search_table["area_deviation_pct"]
        if area_deviation_pct > threshold:
            raise HTTPException(
                409,
                f"Area deviation {area_deviation_pct:.1f}% exceeds the linked search table's "
                f"{threshold}% threshold -- this layrule may not fit this marker.",
            )

    applied_piece_ids: list[str] = []
    unmatched_piece_ids: list[str] = []
    bulk_rows = []
    for p in layrule["placements_json"]:
        piece_id = p["piece_id"]
        if piece_id not in available_by_id:
            unmatched_piece_ids.append(piece_id)
            continue
        piece = client.get(f"/pieces/{piece_id}")
        version_id = piece.get("current_version_id")
        if version_id is None:
            unmatched_piece_ids.append(piece_id)
            continue
        bulk_rows.append(
            {
                "piece_id": piece_id, "piece_version_id": version_id,
                "size_code": p["size_code"], "quantity": p["quantity"], "placement_data": p["placement_data"],
            }
        )
        applied_piece_ids.append(piece_id)

    if not bulk_rows:
        raise HTTPException(400, "No compatible pieces between this layrule and this marker.")

    client.put(f"/markers/{marker_id}/pieces", json=bulk_rows)

    return ApplyLayruleResult(
        applied_piece_ids=applied_piece_ids,
        unmatched_piece_ids=unmatched_piece_ids,
        area_deviation_pct=round(area_deviation_pct, 2) if area_deviation_pct is not None else None,
        warning=(
            f"{len(unmatched_piece_ids)} piece(s) in this layrule have no match on this marker."
            if unmatched_piece_ids else None
        ),
    )


def _build_layrule_settings(marker: dict) -> dict:
    return {
        "force_layrule_name": marker.get("force_layrule_name"),
        "layrule_search_table_id": marker.get("layrule_search_table_id"),
    }


@router.get("/markers/{marker_id}/layrules/settings")
def get_layrule_settings(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _build_layrule_settings(client.get(f"/markers/{marker_id}"))


@router.patch("/markers/{marker_id}/layrules/settings")
def patch_layrule_settings(
    marker_id: str, body: LayruleSettingsPatchRequest, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")
    patch = body.model_dump(exclude_none=True)
    if patch:
        client.patch(f"/markers/{marker_id}", json=patch, headers={"If-Match-Version": str(marker["version"])})
        marker = client.get(f"/markers/{marker_id}")
    return _build_layrule_settings(marker)
