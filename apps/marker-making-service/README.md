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
    arrow guides... blinking + 'Matching Location Not Found'." **Simplification**: each stripe
    definition's grid is treated as axis-aligned — `h_angle_deg`/`v_angle_deg` are accepted and
    stored (forward-compatible with a later slice) but not applied to the nearest-match math.
  - **Bite-boundary validation** (`GET /markers/{id}/matching/validate-bite`) — flags pieces sharing
    a stripe mark that fall into different cutter "bites." **Simplification**: assumes the marker's
    X axis is the cutter's bite/length axis (the same convention the canvas already uses), and takes
    a `bite_length` query value directly rather than a `cutter_parameter_table`, which doesn't exist
    yet (that's `§1.10`/APSM territory, still deferred below).
  - **Cutter stripe setup** (§1.4) — no dedicated endpoint; `PlacementData.cutter_stripe_needed`
    (default `True`, "still needs auto-cutter stripe matching") rides through the normal
    `PUT /markers/{id}/workspace` save path exactly like `stripe_mark_id`, so the cut file can later
    read it straight off `placement_data` without a second lookup.
- `app/synthetic_geometry.py` — deterministic placeholder piece dimensions (Pattern Design doesn't
  exist yet, so there's no real silhouette geometry to nest).

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

Fuse-blocking (§1.6), Engine A layrule replay (§1.2/§1.5), a real placement-producing solver,
bundle-management UI (§1.3 — the platform's `bundles` API already exists but has no UI here), and
the rest of §1.1's manual-nesting toolset beyond place/move/rotate/flip/unplace (butt, align, marry,
bump lines, measure, etc.).

Within matching (§1.4) specifically, Slice 2 built a scoped first pass — method selection
(Standard/5-Star), the matching rules table with Standard's offset entry, Define Stripes geometry,
Define Stripe Marks with Next/Prev step-through, basic in-canvas guidance, and basic bite-boundary
validation, plus the cutter stripe setup toggle added just after — and explicitly deferred the rest:
APSM/cutter-code generation, point-vs-line matching's line+label alternative (only the
point/rule-table style is built), Define Material/Material Pattern (fabric reference image overlay
— needs blob-storage plumbing orthogonal to geometry), Stripe-only-in-a-set, Overlapped checking
(matching context), weave-line tools, and angled-stripe geometry in the guidance math (see
`app/api/matching.py`'s docstring).
