# marker-making-service

Backend for Marker Making & Production Output, Phase 2 Slices 1-2 (see
[`docs/planning/03_marker_making_production/marker_making_production_plan.md`](../../docs/planning/03_marker_making_production/marker_making_production_plan.md)).
**This service has no database of its own** — every persistence call goes through
[`data-platform-api`](../data-platform-api)'s real REST API.

## Scope of this slice, and why

`marker_making_production_plan.md`'s own Phase 2 breaks into 6 sub-items (platform skeleton,
manual nesting, bundle management, matching, fuse-blocking, both nesting engines) — each a
substantial feature area on its own. This slice builds only the parts that map onto the platform's
*existing, already-tested* schema, with no platform changes:

- A platform **style** already *is* Gerber's "model" concept (the full piece set for one
  garment) — `style` + `style_pieces` answer "which pieces does this marker's order call for"
  without a new `model` table.
- Placement geometry goes into the platform's existing `marker_pieces.placement_data` JSONB via
  `PUT /markers/{id}/pieces` — exactly the mechanism that column was designed for.
- Engine B (auto-nest) reuses the platform's existing generic job queue
  (`jobs`/`job_types`, already seeded with `marker_nesting_solve`, built in that service's
  Milestone 6) — no new job infrastructure.

Fuse-blocking, layrules (Engine A), and a real (non-stub) nesting algorithm all still need schema
that doesn't exist anywhere yet (`marker_making_production_plan.md` §2 describes a dozen new tables
it says should live "in the platform's metadata store," but the platform's own spec deliberately
keeps placement/blocking data opaque or absent). That's the same schema-ownership question Slice 1
flagged — still deferred for those areas, not decided here.

Matching (§1.4) is the one area where that question **has** been resolved (Slice 2): the platform
now owns a real `matching_rule_table` entity (see `data-platform-api`'s README/migration `0006`),
reached only through its API — because §2 of this plan already listed that table living in the
platform's Postgres, and because matching genuinely needs structured, queryable schema that opaque
JSONB placement data can't provide (stripe geometry, named marks, offsets). Placement's own schema
stays untouched; a piece's assignment to a stripe mark rides along inside the existing
`marker_pieces.placement_data` JSONB as an added `stripe_mark_id` key, and the cutter stripe setup
toggle (below) the same way as a `cutter_stripe_needed` key — neither needed a platform change.

## What's here

- `app/platform_client.py` — the only way this service touches data. Forwards the caller's
  `X-Dev-User`/`X-Dev-Org` identity untouched on every call (this service never authenticates as a
  separate identity for these — it acts *as* the operator, not *instead of* them).
- `app/api/workspace.py` — `GET`/`PUT /markers/{id}/workspace`: assembles marker + order + style +
  style's pieces + current placements in one call; on save, bulk-replaces placements and walks the
  platform's real workflow-transition graph (`unmade → needs_approval → {partial, made}`) to the
  correct status — there's no direct `unmade → made` transition, so this takes two calls when
  needed.
- `app/api/nesting_jobs.py` — thin `POST/GET /nesting-jobs` wrappers over the platform's generic
  `/jobs` API, named to match this app's own spec.
- `app/api/matching.py` — matching rule table CRUD (proxy + structural validation of the platform's
  opaque JSON sub-resources: offset count caps, stripe-definition/stripe-mark id generation and
  sequence bookkeeping), plus two pieces of real business logic this service owns:
  - **In-canvas match guidance** (`POST /markers/{id}/matching/guidance`) — computes the nearest
    valid grid point for a dragged piece and returns vector-arrow targets, per §1.4's "live vector-
    arrow guides... blinking + 'Matching Location Not Found'." Applies `h_angle_deg`/`v_angle_deg`:
    each stripe family's grid lines repeat every `h_distance`/`v_distance` along the direction given
    by that angle (measured from +X, standard math convention) — `_nearest_along_family` projects
    the query point onto that direction, snaps to the nearest multiple of the distance, and returns
    the perpendicular correction vector. At the shipped defaults (`h_angle_deg=0`, `v_angle_deg=90`)
    this reduces to exactly the original pure-X/pure-Y behavior. **Remaining simplification**: no
    other angle geometry (e.g. non-orthogonal skew between the two families) beyond this.
  - **Bite-boundary validation** (`GET /markers/{id}/matching/validate-bite`) — flags pieces sharing
    a stripe mark that fall into different cutter "bites." **Simplification**: assumes the marker's
    X axis is the cutter's bite/length axis (the same convention the canvas already uses), and takes
    a `bite_length` query value directly rather than a `cutter_parameter_table`, which doesn't exist
    yet (that's `§1.10`/APSM territory, still deferred below).
  - **Cutter stripe setup** (§1.4) — no dedicated endpoint; `PlacementData.cutter_stripe_needed`
    (default `True`, "still needs auto-cutter stripe matching") rides through the normal
    `PUT /markers/{id}/workspace` save path exactly like `stripe_mark_id`, so the cut file can later
    read it straight off `placement_data` without a second lookup.
  - **Define Material / Material Pattern** — five thin proxy endpoints
    (`begin-upload`/`complete`/`visibility`/`download-url`/`DELETE .../material-pattern`) mirroring
    the platform's SAS-URL flow already used for piece/marker versions; this service never touches
    the image bytes. Scoped to "Show Marker's Pattern" (one image as a marker-wide canvas
    background) — "Show Piece's Pattern" (per-piece clipping) is deferred below, since there's no
    real piece silhouette to clip against yet.
- `app/synthetic_geometry.py` — deterministic placeholder piece dimensions (Pattern Design doesn't
  exist yet, so there's no real silhouette geometry to nest).
- `app/api/block_buffer.py` — §1.6 Fuse-blocking. Block/buffer rule tables are a thin proxy over the
  platform's `/block-buffer-rule-tables` CRUD (no interpretation needed — just L/T/R/B amounts and a
  static/dynamic mode). Fuse blocks are where this service does real work: `_compute_bounds` fetches
  a marker's current placements (`GET /markers/{id}/pieces`) and computes the tight axis-aligned
  bounding box of the member pieces' *current* `placement_data.x/y/width/height` — the platform never
  computes this itself, consistent with it not interpreting `placement_data` anywhere else.
  `POST /markers/{id}/fuse-blocks` takes a flat `piece_ids` list (not group-then-place — see the
  frontend's "draft" workaround for why) and a `block_amount`/`reduce_amount`, computes bounds once,
  and stores the result; `PATCH` re-supplies `piece_ids` to force a bounds recompute (e.g. after
  dragging a member piece) or just adjusts `block_amount`/`reduce_amount` in place. `notch_depth`
  (`block_amount - reduce_amount`, the depth of the cutter's Op-Stop notch per §1.4/1.6) is computed
  here and returned as a plain field — the platform's `fuse_blocks` table doesn't store it, since
  it's fully derived from the two amounts it does store. **Simplifications, explicit**: rectangular
  blocks only (matches the platform's `shape` CHECK constraint), no rotation support (a block is
  always axis-aligned even if a member piece is rotated on the canvas — bounds use the piece's raw
  `x/y/width/height`, not its rotated silhouette), and no Create Fusing Marker / Cut Net Parts (both
  need a `cutter_parameter_table`, which doesn't exist yet — §1.10/Phase 3 territory).
- `app/api/material.py` — §1.7 Material calculation/utilization. `GET /markers/{id}/material/
  summary` is the read side: fetches current placements the same way `_compute_bounds` does and
  sums `width*height*quantity`/`2*(width+height)*quantity` across all of them for total area/
  perimeter, plus `max(x + width)` for the marker length actually needed to fit everything —
  along X, the same length-axis convention `matching.py`'s bite-boundary validation already
  assumes. `computed_utilization_pct = total_area / (fabric_width * computed_marker_length) * 100`
  when both are available. These "live" numbers are distinct from the marker's *stored*
  `marker_length`/`utilization_pct` (which start `null` and only change when asked to) —
  `POST .../material/apply-computed` is the explicit "save this as the marker's real value" step.
  `PATCH .../material` sets the two plain inputs (`ply_count`, `fabric_weight_per_unit_area`);
  `PATCH .../material/target` reaches through the marker to its linked order and sets
  `target_length`/`target_utilization_pct` there (400 if the marker has no order — nowhere to put
  a target). Two pure-calculation endpoints, neither persists anything: `POST .../material/
  required-length` ("Calculate Efficiency and Marker Length" per the plan's own wording — given a
  target efficiency %, what length is needed) and `POST .../material/weight`
  (`fabric_width * length * plies * weight_per_unit_area`, falling back to the marker's stored
  values for any argument not supplied). **Deferred**: "Estimate Material" (cap-nesting, a
  per-mode Normal/Reverse/Interleaving breakdown) and the standalone material-calculation-file
  what-if tool — both need multiple real nesting variants to compare against each other, which
  this app's single manual/Engine-B-stub canvas doesn't produce. Piece-level area/perimeter for
  one selected piece needs no endpoint at all — the frontend already has that piece's width/height
  locally.
- `app/api/marker_transform.py` — §1.9 Marker transformations, scoped to the three capabilities
  confirmed with the user. Whole-marker **Flip X/Y/XY has no endpoint here at all** — it's
  computed entirely client-side (see [`marker-making-app`](../marker-making-app)'s README) and
  persisted through the ordinary `PUT /markers/{id}/workspace` save path, exactly like
  single-piece rotate/flip already work. **Shrink and Stretch** *is* server-backed: the plan
  frames it as an order-level setting read at cut-time, so `shrink_x_pct`/`shrink_y_pct` live on
  `dmp.orders` (platform migration `0011`) via `PATCH .../transform/shrink-stretch` (reaches
  through the marker to its linked order, 400 if there isn't one). Since no real cut-time pipeline
  exists yet (§1.10 is blocked on a `cutter_parameter_table`), `POST .../transform/
  apply-shrink-stretch` is a stand-in that scales the *current* placements right now — anchored at
  their own combined bounding-box top-left corner (not the canvas origin), so the layout doesn't
  drift if pieces don't start at `(0,0)`. **Simplification, flagged explicitly**: nothing clears
  the stored percentages after applying, so clicking Apply twice in a row double-shrinks — a real
  cut-time reader would apply the setting exactly once, at generation time, never mutating stored
  placements at all. **Change Width of Marker** just `PATCH`es the already-existing
  `markers.fabric_width` column through the normal proxy path — **"auto-rearranges pieces" is
  explicitly NOT implemented**, since there's no real nesting algorithm to call (Engine B is still
  Milestone 6's sleep-and-echo stub); pieces stay exactly where they were and may now overflow or
  leave slack, which the operator has to notice and fix by hand. `app/api/workspace.py`'s
  `WorkspaceOut` now also carries `fabric_width`, so the frontend can size its canvas from the
  marker's real value instead of a hardcoded constant.

## Local setup

Needs `data-platform-api` fully set up and its Postgres/Azurite containers running (see
[`../data-platform-api/README.md`](../data-platform-api/README.md)).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --port 8001   # run it
pytest                              # run tests (spawns a real data-platform-api subprocess --
                                     # see tests/conftest.py's docstring for why not an in-process
                                     # ASGI transport: both services' top-level package is `app`)
```

## Deferred (flagged, not built here)

Engine A layrule replay (§1.2/§1.5), a real placement-producing solver, bundle-management UI
(§1.3 — the platform's `bundles` API already exists but has no UI here), and the rest of §1.1's
manual-nesting toolset beyond place/move/rotate/flip/unplace (butt, align, marry, bump lines,
measure, etc.).

Within marker transformations (§1.9) specifically: Marker/Split, Marker/Attach (join up to 99
markers into one), Merge, Fix Marker Length/auto-continue, per-piece pre-placement shrink/scale
(distinct from the marker-wide Shrink and Stretch built here), post-hoc `zoom` scaling, Reference
Marker, and Associate (live link back to a Pattern Design source file — there's no Pattern Design
app yet to link to).

Within fuse-blocking (§1.6) specifically: manual-trace (polygon) block shape — only rectangles,
per the platform's `shape` CHECK; Create Fusing Marker and Cut Net Parts, both blocked on a
`cutter_parameter_table` that doesn't exist anywhere yet; and full Lay-Limits-Table-driven rule
assignment (rules are assigned per-piece by hand here, not derived from a lay-limits chain).

Within material calculation/utilization (§1.7) specifically: "Estimate Material" (cap-nesting,
Normal/Reverse/Interleaving per-mode breakdown) and the standalone material-calculation-file
what-if tool, both needing multiple real nesting variants this app doesn't produce; the target
line's "set from historical markers of that style" default (targets are entered by hand here, not
derived from history); and the `U` utilization annotation print code (no plot/annotation system
exists yet to carry it).

Within matching (§1.4) specifically, Slice 2 built a scoped first pass — method selection
(Standard/5-Star), the matching rules table with Standard's offset entry, Define Stripes geometry,
Define Stripe Marks with Next/Prev step-through, basic in-canvas guidance, and basic bite-boundary
validation — plus the cutter stripe setup toggle, overlapped checking (frontend-only, see
[`marker-making-app`](../marker-making-app)'s README), angled-stripe geometry in the guidance math,
the *global* weave line (angle/offset/visibility, `PUT .../weave-line`), the *per-piece* weave-
line override (`placement_data.weave_line_angle_deg`/`weave_line_offset`, riding through the same
opaque JSONB as `stripe_mark_id`/`cutter_stripe_needed` — no new endpoint), Define Material/
Material Pattern (fabric reference image, "Show Marker's Pattern" only), and Stripe-only-in-a-set
(`placement_data.stripe_independent_in_set`, another opaque-JSONB passthrough field with the
sync/opt-out logic living entirely in `marker-making-app` — this service does no interpretation of
it) added just after — and explicitly deferred the rest: APSM/cutter-code generation,
point-vs-line matching's line+label alternative (only the point/rule-table style is built), and
"Show Piece's Pattern" (per-piece image clipping — no real piece silhouette exists yet to clip
against).
