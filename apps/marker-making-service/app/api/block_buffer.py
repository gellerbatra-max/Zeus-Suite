"""marker_making_production_plan.md Sec 1.6 (block / buffer / fuse-blocking, Gerber depth):
Block Buffer Rule Table CRUD (thin proxy, mirrors data-platform-api's app/api/block_buffer.py) and
Fuse Blocks -- where the real business logic lives.

The platform stores a fuse_block's x/y/width/height/piece_placement_ids faithfully but doesn't
compute them (it doesn't interpret placement_data, which is opaque to it) -- this service does:
Create/Modify both (re)compute the tight axis-aligned bounding box of the named pieces' *current*
placements and send that to the platform. **Simplification**: the bbox ignores each piece's
rotation (uses raw x/y/width/height as if unrotated), the same axis-aligned simplification already
used for bounding-box overlap detection and block-buffer per-piece assignment is a plain rule_no on
placement_data, exactly like stripe_mark_id -- no dedicated endpoint, no interpretation here either.

Scoped to rectangular fuse blocks built from a "draft" list of piece ids the frontend accumulates
(no marquee/multi-select on the canvas this slice) -- see marker-making-app's README. Create Fusing
Marker and Cut Net Parts are deferred -- both need a cutter_parameter_table, which doesn't exist
yet (Sec 1.10 / Phase 3 territory).
"""

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    BlockBufferRuleTableCreate,
    BlockBufferRuleTableOut,
    BlockBufferRuleTablePatch,
    CreateFuseBlockRequest,
    FuseBlockOut,
    ModifyFuseBlockRequest,
)

router = APIRouter(tags=["block-buffer", "fuse-blocks"])


def _shape_rule_table(raw: dict) -> BlockBufferRuleTableOut:
    return BlockBufferRuleTableOut(
        id=raw["id"], name=raw["name"], rule_no=raw["rule_no"], rule_type=raw["rule_type"], mode=raw["mode"],
        left_amt=raw["left_amt"], top_amt=raw["top_amt"], right_amt=raw["right_amt"], bottom_amt=raw["bottom_amt"],
        version=raw["version"],
    )


def _shape_fuse_block(raw: dict) -> FuseBlockOut:
    return FuseBlockOut(
        id=raw["id"], marker_id=raw["marker_id"], shape=raw["shape"], x=raw["x"], y=raw["y"],
        width=raw["width"], height=raw["height"], piece_placement_ids=raw["piece_placement_ids"],
        block_amount=raw["block_amount"], reduce_amount=raw["reduce_amount"],
        notch_depth=raw["block_amount"] - raw["reduce_amount"], version=raw["version"],
    )


# -- Block Buffer Rule Table (thin proxy) ------------------------------------------------------


@router.post("/block-buffer-rule-tables", response_model=BlockBufferRuleTableOut)
def create_block_buffer_rule_table(
    body: BlockBufferRuleTableCreate, client: PlatformClient = Depends(get_platform_client)
):
    if body.rule_type not in ("block", "buffer"):
        raise HTTPException(400, "rule_type must be 'block' or 'buffer'.")
    if body.mode not in ("static", "dynamic"):
        raise HTTPException(400, "mode must be 'static' or 'dynamic'.")
    raw = client.post("/block-buffer-rule-tables", json=body.model_dump())
    return _shape_rule_table(raw)


@router.get("/block-buffer-rule-tables")
def list_block_buffer_rule_tables(client: PlatformClient = Depends(get_platform_client)):
    raw = client.get("/block-buffer-rule-tables")
    return {**raw, "items": [_shape_rule_table(item) for item in raw["items"]]}


@router.get("/block-buffer-rule-tables/{table_id}", response_model=BlockBufferRuleTableOut)
def get_block_buffer_rule_table(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _shape_rule_table(client.get(f"/block-buffer-rule-tables/{table_id}"))


@router.patch("/block-buffer-rule-tables/{table_id}", response_model=BlockBufferRuleTableOut)
def patch_block_buffer_rule_table(
    table_id: str, body: BlockBufferRuleTablePatch, client: PlatformClient = Depends(get_platform_client)
):
    current = client.get(f"/block-buffer-rule-tables/{table_id}")
    raw = client.patch(
        f"/block-buffer-rule-tables/{table_id}",
        json=body.model_dump(exclude_none=True),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape_rule_table(raw)


@router.delete("/block-buffer-rule-tables/{table_id}", status_code=204)
def delete_block_buffer_rule_table(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/block-buffer-rule-tables/{table_id}")


# -- Fuse Blocks ---------------------------------------------------------------------------------


def _compute_bounds(client: PlatformClient, marker_id: str, piece_ids: list[str]) -> dict:
    if not piece_ids:
        raise HTTPException(400, "A fuse block needs at least one piece.")
    placements = client.get(f"/markers/{marker_id}/pieces")
    selected = [p for p in placements if p["piece_id"] in piece_ids]
    missing = set(piece_ids) - {p["piece_id"] for p in selected}
    if missing:
        raise HTTPException(400, f"Piece(s) not placed on this marker: {sorted(missing)}")

    xs, ys, x2s, y2s = [], [], [], []
    for p in selected:
        data = p.get("placement_data") or {}
        x, y = data.get("x", 0.0), data.get("y", 0.0)
        width, height = data.get("width", 0.0), data.get("height", 0.0)
        xs.append(x)
        ys.append(y)
        x2s.append(x + width)
        y2s.append(y + height)

    return {"x": min(xs), "y": min(ys), "width": max(x2s) - min(xs), "height": max(y2s) - min(ys)}


@router.post("/markers/{marker_id}/fuse-blocks", response_model=FuseBlockOut)
def create_fuse_block(
    marker_id: str, body: CreateFuseBlockRequest, client: PlatformClient = Depends(get_platform_client)
):
    bounds = _compute_bounds(client, marker_id, body.piece_ids)
    raw = client.post(
        f"/markers/{marker_id}/fuse-blocks",
        json={
            "piece_placement_ids": body.piece_ids, **bounds,
            "block_amount": body.block_amount, "reduce_amount": body.reduce_amount,
        },
    )
    return _shape_fuse_block(raw)


@router.get("/markers/{marker_id}/fuse-blocks")
def list_fuse_blocks(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    raw = client.get(f"/markers/{marker_id}/fuse-blocks")
    return [_shape_fuse_block(item) for item in raw]


@router.delete("/markers/{marker_id}/fuse-blocks", status_code=204)
def delete_all_fuse_blocks(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/markers/{marker_id}/fuse-blocks")


@router.patch("/markers/{marker_id}/fuse-blocks/{fuse_block_id}", response_model=FuseBlockOut)
def modify_fuse_block(
    marker_id: str, fuse_block_id: str, body: ModifyFuseBlockRequest,
    client: PlatformClient = Depends(get_platform_client),
):
    current = client.get(f"/fuse-blocks/{fuse_block_id}")
    patch: dict = {}
    if body.piece_ids is not None:
        patch["piece_placement_ids"] = body.piece_ids
        patch.update(_compute_bounds(client, marker_id, body.piece_ids))
    if body.block_amount is not None:
        patch["block_amount"] = body.block_amount
    if body.reduce_amount is not None:
        patch["reduce_amount"] = body.reduce_amount
    raw = client.patch(
        f"/fuse-blocks/{fuse_block_id}", json=patch, headers={"If-Match-Version": str(current["version"])}
    )
    return _shape_fuse_block(raw)


@router.delete("/markers/{marker_id}/fuse-blocks/{fuse_block_id}", status_code=204)
def delete_fuse_block(marker_id: str, fuse_block_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/fuse-blocks/{fuse_block_id}")
