"""marker_making_production_plan.md Sec 1.4 (matching / plaid-stripe alignment) -- Slice 2's
scoped first pass: matching method selection, a reusable matching rules table, Define Stripes
geometry, Define Stripe Marks with Next/Prev step-through, basic in-canvas match guidance, and
basic bite-boundary validation.

The platform stores matching_rule_table's offsets_json/stripe_definitions_json/stripe_marks_json
as opaque JSON (see data-platform-api's app/api/matching.py docstring) -- this is where that JSON
actually gets interpreted: structural validation (offset count caps, id generation, sequence
bookkeeping) and the guidance/bite-validation math below.

One remaining explicit simplification, not full parity with marker_making_production_plan.md
Sec 1.4: bite-boundary validation assumes the marker's X axis is the cutter's bite/length axis
(the same convention the Slice-1 canvas already uses), and is parameterized by a `bite_length`
query value rather than a `cutter_parameter_table`, which doesn't exist yet.

Guidance now applies h_angle_deg/v_angle_deg (previously stored but ignored -- treated as
axis-aligned). See `_nearest_along_family` below for the angle convention: h_angle_deg/v_angle_deg
are the *spacing-direction* angle of each stripe family (measured from +X, standard math
convention), not the line direction -- e.g. h_angle_deg=0 means the h-family's repeat is measured
straight along X (so its lines run vertically), matching the pre-angle defaults exactly. This
convention was chosen because it's the one under which the already-shipped defaults
(h_angle_deg=0.0, v_angle_deg=90.0) reduce to exactly the axis-aligned behavior this slice shipped
with -- 0 deg = spacing along +X, 90 deg = spacing along +Y.

Weave-line tools: a matching_rule_table now also carries one *global* reference line
(`weave_line_json`: angle_deg + a perpendicular `offset` from the marker origin + `visible`),
covering "Edit Weave Line of All pieces" and "Show/hide weave line". The frontend computes
`offset` for "center on selected piece" itself (projecting that piece's center onto the line's
perpendicular direction) and just calls this same replace endpoint -- no separate "center" route.
"Font on Weaveline Upwards always" isn't a setting to expose -- the doc's "always" reads as fixed
behavior, so the frontend just always renders the weave-line label upright rather than rotated
with the line.

Per-piece override ("Edit Weave Line" for a single piece) rides through placement_data
(`weave_line_angle_deg`/`weave_line_offset`, both optional) exactly like stripe_mark_id and
cutter_stripe_needed -- no new endpoint here either; a piece with both fields set uses its own
line instead of the rule table's global one, and the frontend persists it via the normal
`PUT /markers/{id}/workspace` save path.

Define Material / Material Pattern: a fabric reference image on the rule table, uploaded via the
platform's SAS-URL begin-upload/complete flow (see data-platform-api's app/api/matching.py
docstring) -- this service just proxies the three-call sequence (begin-upload, complete,
download-url) plus a visibility toggle and delete, never touching the image bytes itself. Scoped
to "Show Marker's Pattern" (one image as a marker-wide canvas background) -- "Show Piece's Pattern"
(per-piece image clipping) is deferred, since there's no real piece silhouette to clip against yet
(Pattern Design doesn't exist -- see the synthetic-geometry note elsewhere in this service).
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
    MaterialPatternBeginRequest,
    MaterialPatternBeginResponse,
    MaterialPatternCompleteRequest,
    MaterialPatternDownloadUrlOut,
    MaterialPatternInfo,
    MaterialPatternVisibilityRequest,
    OffsetsIn,
    StripeDefinitionIn,
    StripeDefinitionOut,
    StripeDefinitionPatch,
    StripeMarkIn,
    StripeMarkOut,
    StripeMarkPatch,
    StripeMarkStepRequest,
    ValidateBiteOut,
    WeaveLineIn,
)

router = APIRouter(tags=["matching"])

MAX_OFFSETS_PER_AXIS = 3
SNAP_TOLERANCE = 1.0


def _shape(raw: dict) -> MatchingRuleTableOut:
    offsets = raw.get("offsets_json") or {}
    weave_line = raw.get("weave_line_json")
    material_pattern = raw.get("material_pattern_json")
    return MatchingRuleTableOut(
        id=raw["id"],
        name=raw["name"],
        method=raw["method"],
        plaid_repeat=raw.get("plaid_repeat"),
        stripe_repeat=raw.get("stripe_repeat"),
        offsets=OffsetsIn(horizontal=offsets.get("horizontal", []), vertical=offsets.get("vertical", [])),
        stripe_definitions=[StripeDefinitionOut(**d) for d in raw.get("stripe_definitions_json", [])],
        stripe_marks=[StripeMarkOut(**m) for m in raw.get("stripe_marks_json", [])],
        weave_line=WeaveLineIn(**weave_line) if weave_line else None,
        material_pattern=(
            MaterialPatternInfo(name=material_pattern.get("name"), visible=material_pattern.get("visible", True))
            if material_pattern else None
        ),
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


# -- Weave-line tools -----------------------------------------------------------------------------
# The global weave line ("Edit Weave Line of All pieces" + "Show/hide weave line"); the per-piece
# override ("Edit Weave Line" for a single piece) rides through placement_data instead -- see
# module docstring.


@router.put("/matching-rule-tables/{table_id}/weave-line", response_model=MatchingRuleTableOut)
def replace_weave_line(table_id: str, body: WeaveLineIn, client: PlatformClient = Depends(get_platform_client)):
    current = _get_raw_table(client, table_id)
    raw = client.put(
        f"/matching-rule-tables/{table_id}/weave-line",
        json=body.model_dump(),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


# -- Define Material / Material Pattern ---------------------------------------------------------


@router.post(
    "/matching-rule-tables/{table_id}/material-pattern/begin-upload", response_model=MaterialPatternBeginResponse
)
def begin_material_pattern_upload(
    table_id: str, body: MaterialPatternBeginRequest, client: PlatformClient = Depends(get_platform_client)
):
    return client.post(f"/matching-rule-tables/{table_id}/material-pattern/begin-upload", json=body.model_dump())


@router.post("/matching-rule-tables/{table_id}/material-pattern/complete", response_model=MatchingRuleTableOut)
def complete_material_pattern_upload(
    table_id: str, body: MaterialPatternCompleteRequest, client: PlatformClient = Depends(get_platform_client)
):
    current = _get_raw_table(client, table_id)
    raw = client.post(
        f"/matching-rule-tables/{table_id}/material-pattern/complete",
        json=body.model_dump(),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.put(
    "/matching-rule-tables/{table_id}/material-pattern/visibility", response_model=MatchingRuleTableOut
)
def set_material_pattern_visibility(
    table_id: str, body: MaterialPatternVisibilityRequest, client: PlatformClient = Depends(get_platform_client)
):
    current = _get_raw_table(client, table_id)
    raw = client.put(
        f"/matching-rule-tables/{table_id}/material-pattern/visibility",
        json=body.model_dump(),
        headers={"If-Match-Version": str(current["version"])},
    )
    return _shape(raw)


@router.get(
    "/matching-rule-tables/{table_id}/material-pattern/download-url", response_model=MaterialPatternDownloadUrlOut
)
def get_material_pattern_download_url(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    return client.get(f"/matching-rule-tables/{table_id}/material-pattern/download-url")


@router.delete("/matching-rule-tables/{table_id}/material-pattern", response_model=MatchingRuleTableOut)
def delete_material_pattern(table_id: str, client: PlatformClient = Depends(get_platform_client)):
    current = _get_raw_table(client, table_id)
    raw = client.delete(
        f"/matching-rule-tables/{table_id}/material-pattern", headers={"If-Match-Version": str(current["version"])}
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


def _nearest_along_family(
    x: float, y: float, origin_x: float, origin_y: float, distance: float, angle_deg: float
) -> tuple[float, float] | None:
    """The (dx, dy) world-space correction that snaps (x, y) onto the nearest line of a stripe
    family whose lines repeat every `distance` along the direction `angle_deg` (from +X, standard
    math convention) -- i.e. the perpendicular projection onto that family's nearest grid line.
    At angle_deg=0 this reduces to a pure X correction; at angle_deg=90 to a pure Y correction --
    exactly the axis-aligned behavior this slice originally shipped with."""
    if not distance:
        return None
    angle = math.radians(angle_deg)
    ux, uy = math.cos(angle), math.sin(angle)
    projection = (x - origin_x) * ux + (y - origin_y) * uy
    target_projection = round(projection / distance) * distance
    delta = target_projection - projection
    return delta * ux, delta * uy


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

    origin_x = definition.get("origin_x", 0.0)
    origin_y = definition.get("origin_y", 0.0)
    h_correction = _nearest_along_family(
        body.x, body.y, origin_x, origin_y, definition.get("h_distance", 0.0), definition.get("h_angle_deg", 0.0)
    )
    v_correction = _nearest_along_family(
        body.x, body.y, origin_x, origin_y, definition.get("v_distance", 0.0), definition.get("v_angle_deg", 90.0)
    )

    targets: list[MatchGuidanceTarget] = []
    found = True
    for axis, correction in (("horizontal", h_correction), ("vertical", v_correction)):
        if correction is None:
            continue
        dx, dy = correction
        if max(abs(dx), abs(dy)) > SNAP_TOLERANCE:
            found = False
            targets.append(
                MatchGuidanceTarget(axis=axis, dx=dx, dy=dy, target_x=body.x + dx, target_y=body.y + dy)
            )

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
