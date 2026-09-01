# marker-making-service

Backend for Marker Making & Production Output, Phase 2 Slice 1 (see
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

Matching, fuse-blocking, layrules (Engine A), and a real (non-stub) nesting algorithm all need
schema that doesn't exist anywhere yet (`marker_making_production_plan.md` §2 describes a dozen
new tables it says should live "in the platform's metadata store," but the platform's own spec
deliberately keeps placement/matching/blocking data opaque or absent). That's a real
schema-ownership decision (extend the platform vs. give this service its own database) — explicitly
deferred, not decided here.

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

Matching (§1.4), fuse-blocking (§1.6), Engine A layrule replay (§1.2/§1.5), a real
placement-producing solver, bundle-management UI (§1.3 — the platform's `bundles` API already
exists but has no UI here), and the rest of §1.1's manual-nesting toolset beyond
place/move/rotate/flip/unplace (butt, align, marry, bump lines, measure, etc.).
