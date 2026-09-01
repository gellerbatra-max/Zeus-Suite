"""marker_making_production_plan.md Sec 1.4 (matching / plaid-stripe alignment) -- Slice 2's
scoped first pass: matching method selection, a reusable matching rules table, Define Stripes
geometry, Define Stripe Marks with Next/Prev step-through, basic in-canvas match guidance, and
basic bite-boundary validation.

The platform stores matching_rule_table's offsets_json/stripe_definitions_json/stripe_marks_json
as opaque JSON (see data-platform-api's app/api/matching.py docstring) -- this is where that JSON
actually gets interpreted: structural validation (offset count caps, id generation, sequence
bookkeeping) and the guidance/bite-validation math below.

Two explicit simplifications, not full parity with marker_making_production_plan.md Sec 1.4:
  - Guidance treats each stripe definition's grid as axis-aligned. h_angle_deg/v_angle_deg are
    accepted and stored (forward-compatible with a later slice) but not applied to the nearest-
    match calculation.
  - Bite-boundary validation assumes the marker's X axis is the cutter's bite/length axis (the
    same convention the Slice-1 canvas already uses), and is parameterized by a `bite_length`
    query value rather than a `cutter_parameter_table`, which doesn't exist yet.
"""

import math
import uuid

from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    ApplyMatchingRequest,
    BiteViolation,
    MatchGuidanceOut,
    MatchGuidanceRequest,
    MatchGuidanceTarget,
    MatchingRuleTableCreate,
    MatchingRuleTableOut,
    MatchingRuleTablePatch,
    OffsetsIn,
    StripeDefinitionIn,
    StripeDefinitionOut,
    StripeDefinitionPatch,
    StripeMarkIn,
    StripeMarkOut,
    StripeMarkPatch,
    StripeMarkStepRequest,
    ValidateBiteOut,
)

router = APIRouter(tags=["matching"])

MAX_OFFSETS_PER_AXIS = 3
SNAP_TOLERANCE = 1.0


def _shape(raw: dict) -> MatchingRuleTableOut:
    offsets = raw.get("offsets_json") or {}
    return MatchingRuleTableOut(
        id=raw["id"],
        name=raw["name"],
        method=raw["method"],
        plaid_repeat=raw.get("plaid_repeat"),
        stripe_repeat=raw.get("stripe_repeat"),
        offsets=OffsetsIn(horizontal=offsets.get("horizontal", []), vertical=offsets.get("vertical", [])),
        stripe_definitions=[StripeDefinitionOut(**d) for d in raw.get("stripe_definitions_json", [])],
        stripe_marks=[StripeMarkOut(**m) for m in raw.get("stripe_marks_json", [])],
        version=raw["version"],
    )


def _get_raw_table(client: PlatformClient, table_id: str) -> dict:
    return client.get(f"/matching-rule-tables/{table_id}")


# -- Matching rule table CRUD ---------------------------------------------------------------


@router.post("/matching-rule-tables", response_model=MatchingRuleTableOut)
def create_matching_rule_table(
    body: MatchingRuleTableCreate, client: PlatformClient = Depends(get_platform_client)
):
    if body.method not in ("standard", "five_star"):
        raise HTTPException(400, "method must be 'standard' or 'five_star'.")
    raw = client.post("/matching-rule-tables", json=body.model_dump())
    return _shape(raw)


@router.get("/matching-rule-tables")
def list_matching_rule_tables(client: PlatformClient = Depends(get_platform_client)):
    raw = client.get("/matching-rule-tables")
    return {**raw, "items": [_shape(item) for item in raw["items"]]}


@router.get("/matching-rule-tables/{table_id}", response_model=MatchingRuleTableOut)
def get_matching_rule_table(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    return _shape(_get_raw_table(client, table_id))


@router.patch("/matching-rule-tables/{table_id}", response_model=MatchingRuleTableOut)
def patch_matching_rule_table(
    table_id: str, body: MatchingRuleTablePatch, client: PlatformClient = Depends(get_platform_client)
):
    current = _get_raw_table(client, table_id)
    raw = client.patch(
        f"/matching-rule-tables/{table_id}",
        json=body.model_dump(exclude_none=True),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.delete("/matching-rule-tables/{table_id}", status_code=204)
def delete_matching_rule_table(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    client.delete(f"/matching-rule-tables/{table_id}")


# -- Standard method's offset entry -----------------------------------------------------------


@router.put("/matching-rule-tables/{table_id}/offsets", response_model=MatchingRuleTableOut)
def replace_offsets(table_id: str, body: OffsetsIn, client: PlatformClient = Depends(get_platform_client)):
    if len(body.horizontal) > MAX_OFFSETS_PER_AXIS or len(body.vertical) > MAX_OFFSETS_PER_AXIS:
        raise HTTPException(400, f"Standard matching allows at most {MAX_OFFSETS_PER_AXIS} offsets per axis.")
    current = _get_raw_table(client, table_id)
    raw = client.put(
        f"/matching-rule-tables/{table_id}/offsets",
        json=body.model_dump(),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


# -- Define Stripes -----------------------------------------------------------------------------


@router.post("/matching-rule-tables/{table_id}/stripe-definitions", response_model=MatchingRuleTableOut)
def add_stripe_definition(
    table_id: str, body: StripeDefinitionIn, client: PlatformClient = Depends(get_platform_client)
):
    current = _get_raw_table(client, table_id)
    entry = {"id": f"sd-{uuid.uuid4().hex[:8]}", **body.model_dump()}
    items = [*current.get("stripe_definitions_json", []), entry]
    raw = client.put(
        f"/matching-rule-tables/{table_id}/stripe-definitions",
        json={"items": items},
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.patch(
    "/matching-rule-tables/{table_id}/stripe-definitions/{def_id}", response_model=MatchingRuleTableOut
)
def patch_stripe_definition(
    table_id: str, def_id: str, body: StripeDefinitionPatch, client: PlatformClient = Depends(get_platform_client)
):
    current = _get_raw_table(client, table_id)
    items = current.get("stripe_definitions_json", [])
    updates = body.model_dump(exclude_none=True)
    found = False
    new_items = []
    for item in items:
        if item["id"] == def_id:
            found = True
            item = {**item, **updates}
        new_items.append(item)
    if not found:
        raise HTTPException(404, "Stripe definition not found.")
    raw = client.put(
        f"/matching-rule-tables/{table_id}/stripe-definitions",
        json={"items": new_items},
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.delete(
    "/matching-rule-tables/{table_id}/stripe-definitions/{def_id}", response_model=MatchingRuleTableOut
)
def delete_stripe_definition(table_id: str, def_id: str, client: PlatformClient = Depends(get_platform_client)):
    current = _get_raw_table(client, table_id)
    defs = current.get("stripe_definitions_json", [])
    new_defs = [d for d in defs if d["id"] != def_id]
    if len(new_defs) == len(defs):
        raise HTTPException(404, "Stripe definition not found.")

    raw = client.put(
        f"/matching-rule-tables/{table_id}/stripe-definitions",
        json={"items": new_defs},
        headers={"If-Match-Version": str(current["version"])},
    )

    marks = raw.get("stripe_marks_json", [])
    orphaned = [m for m in marks if m.get("stripe_definition_id") == def_id]
    if orphaned:
        new_marks = [
            {**m, "stripe_definition_id": None} if m.get("stripe_definition_id") == def_id else m for m in marks
        ]
        raw = client.put(
            f"/matching-rule-tables/{table_id}/stripe-marks",
            json={"items": new_marks},
            headers={"If-Match-Version": str(raw["version"])},
        )
    return _shape(raw)


# -- Define Stripe Marks --------------------------------------------------------------------


@router.post("/matching-rule-tables/{table_id}/stripe-marks", response_model=MatchingRuleTableOut)
def add_stripe_mark(table_id: str, body: StripeMarkIn, client: PlatformClient = Depends(get_platform_client)):
    current = _get_raw_table(client, table_id)
    marks = current.get("stripe_marks_json", [])
    next_sequence = max((m.get("sequence", 0) for m in marks), default=0) + 1
    entry = {"id": f"sm-{uuid.uuid4().hex[:8]}", "sequence": next_sequence, **body.model_dump()}
    raw = client.put(
        f"/matching-rule-tables/{table_id}/stripe-marks",
        json={"items": [*marks, entry]},
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.patch("/matching-rule-tables/{table_id}/stripe-marks/{mark_id}", response_model=MatchingRuleTableOut)
def patch_stripe_mark(
    table_id: str, mark_id: str, body: StripeMarkPatch, client: PlatformClient = Depends(get_platform_client)
):
    current = _get_raw_table(client, table_id)
    marks = current.get("stripe_marks_json", [])
    updates = body.model_dump(exclude_none=True)
    found = False
    new_marks = []
    for mark in marks:
        if mark["id"] == mark_id:
            found = True
            mark = {**mark, **updates}
        new_marks.append(mark)
    if not found:
        raise HTTPException(404, "Stripe mark not found.")
    raw = client.put(
        f"/matching-rule-tables/{table_id}/stripe-marks",
        json={"items": new_marks},
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.delete("/matching-rule-tables/{table_id}/stripe-marks/{mark_id}", response_model=MatchingRuleTableOut)
def delete_stripe_mark(table_id: str, mark_id: str, client: PlatformClient = Depends(get_platform_client)):
    current = _get_raw_table(client, table_id)
    marks = current.get("stripe_marks_json", [])
    new_marks = [m for m in marks if m["id"] != mark_id]
    if len(new_marks) == len(marks):
        raise HTTPException(404, "Stripe mark not found.")
    raw = client.put(
        f"/matching-rule-tables/{table_id}/stripe-marks",
        json={"items": new_marks},
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.post("/matching-rule-tables/{table_id}/stripe-marks/{mark_id}/step", response_model=StripeMarkOut)
def step_stripe_mark(
    table_id: str, mark_id: str, body: StripeMarkStepRequest, client: PlatformClient = Depends(get_platform_client)
):
    if body.direction not in ("next", "prev"):
        raise HTTPException(400, "direction must be 'next' or 'prev'.")
    current = _get_raw_table(client, table_id)
    marks = sorted(current.get("stripe_marks_json", []), key=lambda m: m["sequence"])
    index = next((i for i, m in enumerate(marks) if m["id"] == mark_id), None)
    if index is None:
        raise HTTPException(404, "Stripe mark not found.")
    target_index = index + 1 if body.direction == "next" else index - 1
    if target_index < 0 or target_index >= len(marks):
        raise HTTPException(404, f"No {body.direction} stripe mark.")
    return StripeMarkOut(**marks[target_index])


# -- Marker-scoped matching actions -----------------------------------------------------------


@router.post("/markers/{marker_id}/matching/apply")
def apply_matching(marker_id: str, body: ApplyMatchingRequest, client: PlatformClient = Depends(get_platform_client)):
    marker = client.get(f"/markers/{marker_id}")
    patch = body.model_dump(exclude_none=True)
    updated = client.patch(
        f"/markers/{marker_id}", json=patch, headers={"If-Match-Version": str(marker["version"])}
    )
    return {
        "marker_id": updated["id"],
        "matching_method": updated.get("matching_method"),
        "matching_rule_table_id": updated.get("matching_rule_table_id"),
    }


def _nearest_grid_value(actual: float, origin: float, distance: float) -> float | None:
    if not distance:
        return None
    steps = round((actual - origin) / distance)
    return origin + steps * distance


@router.post("/markers/{marker_id}/matching/guidance", response_model=MatchGuidanceOut)
def match_guidance(
    marker_id: str, body: MatchGuidanceRequest, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")
    table_id = marker.get("matching_rule_table_id")
    if not table_id or not body.stripe_mark_id:
        return MatchGuidanceOut(found=False, targets=[], message="No matching rule table assigned to this marker.")

    table = _get_raw_table(client, table_id)
    mark = next((m for m in table.get("stripe_marks_json", []) if m["id"] == body.stripe_mark_id), None)
    if mark is None or not mark.get("stripe_definition_id"):
        return MatchGuidanceOut(found=False, targets=[], message="Selected stripe mark has no stripe definition.")

    definition = next(
        (d for d in table.get("stripe_definitions_json", []) if d["id"] == mark["stripe_definition_id"]), None
    )
    if definition is None:
        return MatchGuidanceOut(found=False, targets=[], message="Selected stripe mark has no stripe definition.")

    # Simplification: h_angle_deg/v_angle_deg are stored but not applied here -- the grid is
    # treated as axis-aligned this slice (see module docstring).
    nearest_x = _nearest_grid_value(body.x, definition.get("origin_x", 0.0), definition.get("h_distance", 0.0))
    nearest_y = _nearest_grid_value(body.y, definition.get("origin_y", 0.0), definition.get("v_distance", 0.0))

    targets: list[MatchGuidanceTarget] = []
    found = True
    if nearest_x is not None:
        dx = nearest_x - body.x
        if abs(dx) > SNAP_TOLERANCE:
            found = False
            targets.append(MatchGuidanceTarget(axis="horizontal", dx=dx, dy=0.0, target_x=nearest_x, target_y=body.y))
    if nearest_y is not None:
        dy = nearest_y - body.y
        if abs(dy) > SNAP_TOLERANCE:
            found = False
            targets.append(MatchGuidanceTarget(axis="vertical", dx=0.0, dy=dy, target_x=body.x, target_y=nearest_y))

    return MatchGuidanceOut(found=found, targets=targets, message=None if found else "Matching Location Not Found")


@router.get("/markers/{marker_id}/matching/validate-bite", response_model=ValidateBiteOut)
def validate_bite(
    marker_id: str, bite_length: float, client: PlatformClient = Depends(get_platform_client)
):
    marker = client.get(f"/markers/{marker_id}")
    if not marker.get("matching_rule_table_id"):
        return ValidateBiteOut(bite_length=bite_length, ok=True, violations=[])

    placements = client.get(f"/markers/{marker_id}/pieces")
    groups: dict[str, list[dict]] = {}
    for p in placements:
        stripe_mark_id = (p.get("placement_data") or {}).get("stripe_mark_id")
        if not stripe_mark_id:
            continue
        groups.setdefault(stripe_mark_id, []).append(p)

    violations: list[BiteViolation] = []
    for stripe_mark_id, group in groups.items():
        indexed = [
            (p, math.floor((p.get("placement_data") or {}).get("x", 0.0) / bite_length)) for p in group
        ]
        for i in range(len(indexed)):
            for j in range(i + 1, len(indexed)):
                piece_a, bite_a = indexed[i]
                piece_b, bite_b = indexed[j]
                if bite_a != bite_b:
                    violations.append(
                        BiteViolation(
                            piece_id_a=piece_a["piece_id"],
                            piece_id_b=piece_b["piece_id"],
                            stripe_mark_id=stripe_mark_id,
                            bite_index_a=bite_a,
                            bite_index_b=bite_b,
                        )
                    )

    return ValidateBiteOut(bite_length=bite_length, ok=len(violations) == 0, violations=violations)
