# format-interchange-service

Backend for the Format Interchange & Legacy Migration Utility, Steps 1-3 of Phase 3 (see
[`docs/planning/04_format_interchange/format_interchange_plan.md`](../../docs/planning/04_format_interchange/format_interchange_plan.md)
Sec 7): single-piece IGES export ("the smallest complete slice"), single-piece IGES import (the
reader, the Sec 1.2 option pipeline, Import Profiles, and a staged-commit Import Viewer), and the
Legacy Migration batch pipeline's classification stage (batch upload, per-item conversion, the
full Sec 2.3/2.4 error/warning catalogue, and a CSV/JSON findings report -- no Viewer or commit
yet, that's Step 4).

## How this differs from every other app built so far

`pattern-design-service` and `marker-making-service` are pure thin clients with no database of
their own. This service genuinely owns one (Sec 4: "This service's own database ... holds only
interchange-specific bookkeeping"): `interchange_job`, `import_profile`, `migration_batch`,
`migration_item`, `migration_finding`. It's the first app in this delivery built with its own
Alembic/SQLAlchemy setup alongside `data-platform-api`'s.

It also talks **directly to `data-platform-api`**, never to `pattern-design-service` (Sec 0: "It
never talks to Pattern Design or Marker Making directly"). A piece's geometry document -- the JSON
`pattern-design-service` writes to Blob Storage -- is fetched here via the platform's own
`GET /pieces/{id}/versions/{version_id}/download-url` and parsed with this service's **own** mirror
of the document shape (`app/geometry.py`, a subset: perimeter, internal lines, notches, grain
line -- not seams/darts/grade_rule_table/annotations/measurements, out of scope for export). This
is the same cross-service-schema-mirroring pattern `pattern-design-app`'s `api/types.ts` already
uses against its own backend, just one hop further out.

## What's here

- `app/iges_writer.py` -- a purpose-built IGES 5.3 ASCII writer (Sec 6: "no full CAD kernel is
  needed -- pieces are flat 2D outlines, not solids"). Implements Type 110 (Line) assembled into
  Type 102 (Composite Curve) for the outline, Type 110 for internal lines and the grain line, and
  Type 116 (Point) for notches. Every card is verified to be exactly 80 columns; DE/PD pointer
  arithmetic is covered by `tests/test_export.py` reading its own output back.
- `app/geometry.py` -- the geometry document mirror, plus the **export validation gate** (Sec
  1.1): a self-intersection + minimum-point-count check (Shapely) that runs before entity mapping,
  so a broken outline is rejected with the offending coordinate rather than silently exported --
  "Gerber's IGESOUT has no equivalent check."
- `app/api/export.py` -- `POST /pieces/{piece_id}/export/iges` + `GET /export/iges/jobs/{job_id}`.
  See its module docstring for a real, deliberate deviation: this slice's conversion is
  synchronous and does NOT push the platform `Job` it submits to a terminal state via
  `heartbeat`/`complete` (those require a `job.worker` permission this caller doesn't hold) --
  `interchange_job.status`, this service's own row, is authoritative instead.
- `app/blob_io.py` -- downloads geometry bytes from the platform's SAS URL; uploads/serves this
  service's own export artifacts from its own `format-interchange-exports` container (an export
  isn't a piece version, so it never goes through the platform's `begin_version` dance), and (Step
  2) staged-import bundles (raw source + converted geometry + warnings) from a second
  `format-interchange-imports` container.
- `app/iges_reader.py` -- the symmetrical counterpart to `iges_writer.py`: parses IGES ASCII back
  into Type 110/116/102 entities, reading the Directory Entry's Entity Label back to recover
  "OUTLINE"/"INTERNAL"/"GRAIN"/"NOTCH" semantics on round-trip.
- `app/import_pipeline.py` -- turns a parsed IGES document into this service's geometry mirror,
  applying Sec 1.2's option table as explicit, individually-warned pipeline stages: outline
  reconstruction (Composite Curve when present, heuristic endpoint-chaining -- "largest closed
  loop = outline" -- otherwise), `closure_amount_mm` gap-bridging, `trim_tolerance` collinear-point
  removal, `paste_internal_to_notch`, `points_to_drill_holes`, and a `unit_override` plausibility
  heuristic. `infer_grade_points`/`numbering_scheme` (no grading integration exists yet) and
  `max_arc_points`/`max_spline_points`/`force_sharp_corners` (no arc/spline/curve-smoothing entity
  exists to act on) are deliberately scoped out -- requesting them produces an
  `option_not_implemented` warning rather than a silent no-op.
- `app/api/import_.py` -- `POST /import/iges` (multipart file + JSON options) and
  `GET/POST .../jobs/{job_id}` (+ `/log`, `/commit`). Conversion is synchronous, same deviation as
  export's job-queue usage (see its own module docstring). A converted piece commits to the
  platform in the same request only if `stage_only=false` or `auto_approve=true`; otherwise it's
  held `staged` (Sec 1.4's Import Viewer gate) pending an explicit `/commit` call.
- `app/api/import_profiles.py` -- `GET/POST /import-profiles`, `PUT /import-profiles/{id}` (Sec
  1.3's saved parameter presets, replacing `IGES.INI`).
- `app/migration_sources.py` -- legacy source format dispatch (Sec 6: "one parser module per
  supported source format... new source formats are added as new parser modules, not new pipeline
  logic"). Step 3 supports exactly one format, `iges`, reusing Step 2's reader/pipeline verbatim;
  DXF/AAMA-ASTM/proprietary-binary parsers are new modules for a future slice -- there's no real
  spec or sample data for either in this suite yet.
- `app/migration_checks.py` -- the Sec 2.3 (error) / Sec 2.4 (warning) catalogues as individual
  check functions, run against converted geometry plus a caller-supplied `LegacyMetadata` bag. Most
  catalogue rows need legacy-system data this geometry model has no concept of (corner-treatment
  types, plaid/stripe match lines, grade-rule-table references, size-synonym tables, grade-axis
  assignments, flip/rotation flags) and this suite has no grade-rule-table registry to resolve
  against either -- see the module's own docstring for why the caller supplies this explicitly
  instead of it being inferred, and why that's the natural extension point a future DXF/AAMA-ASTM
  parser would populate automatically. `self_intersection` and `multiple_grain_lines` are the two
  catalogue rows produced from real signals instead (the import pipeline's own validation gate and
  its own multi-grain-line detection, respectively, the latter re-emitted at `error` severity here
  since a legacy-batch item shouldn't silently auto-resolve an ambiguous grain line the way a
  manually-reviewed single-piece import can).
- `app/api/migration.py` -- `POST /migration/batches` (multipart file upload, one item per file),
  `POST .../run` (classifies every still-`pending` item -- idempotent in the sense that a re-run
  only reprocesses items Step 4's resolve action would reset back to `pending`), `GET .../{id}`
  (status counts), `GET .../{id}/items[/{item_id}]`, `GET .../{id}/report.csv|.json`. The remaining
  Sec 5 endpoints (`resolve`/`block`/`accept-warning`/`commit`) are Step 4's job -- this slice
  classifies and reports, it doesn't fix or commit anything to the platform yet.
- `alembic/` -- `format_interchange` schema: `interchange_job` (Step 1) plus (Step 2)
  `import_profile` and `interchange_job.target_piece_id`/nullable `piece_id`, plus (Step 3)
  `migration_batch`/`migration_item`/`migration_finding`.

## Local setup

Needs `data-platform-api` fully set up and its Postgres/Azurite containers running (see
[`../data-platform-api/README.md`](../data-platform-api/README.md)).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Both this service AND data-platform-api migrate against the SAME database in local dev --
# they'd fight over a shared `alembic_version` table with the default config, so this service's
# own alembic/env.py tracks its history in `alembic_version_format_interchange` instead (see that
# file's comment). Migrate both, in order:
cd ../data-platform-api && DATABASE_URL=... alembic upgrade head && cd -
DATABASE_URL=... alembic upgrade head

uvicorn app.main:app --port 8002   # pick a port not already used by another local service
pytest                              # spawns its own data-platform-api subprocess + its own
                                     # isolated test database (tests/conftest.py creates
                                     # zeus_suite_format_interchange_test on the fly)
```

**On shared local infrastructure**: this repo's other app branches (marker-making, pattern-design)
each independently learned the hard way that another session's `docker compose` restarts, own
`data-platform-api` instance on the default port, or own Alembic migrations against the shared
`zeus_suite` database can silently break yours mid-session -- not a code regression, just
contention over shared local infra. This service's own manual testing used a fully isolated
stack (`zeus_suite_format_interchange` database, ports 8033/8034) for exactly that reason; do the
same rather than assuming port 8000 / the `zeus_suite` database are yours alone.

## Deferred (flagged, not built here)

Everything past Step 3 of Sec 7's phased plan: the Migration Viewer and triage-and-fix loop (Step
4 -- side-by-side overlay, Measure, Snap-to-Geometry, the Sec 2.5 diff-highlight catalogue, and the
`resolve`/`block`/`accept-warning`/`commit` endpoints), and load/audit/RBAC hardening (Step 5).
Within Step 1: batch export (`POST /export/iges/batch`), `entity_profile` target-system curve
preferences (no curve/spline entity exists yet to have preferences about), and a dedicated worker
service-account identity for pushing the platform `Job` through its real `heartbeat`/`complete`
lifecycle (see `app/api/export.py`'s docstring). Within Step 2: `infer_grade_points`/
`numbering_scheme` grade-point inference (no grading integration exists in this service),
`max_arc_points`/`max_spline_points`/`force_sharp_corners` (no arc/spline entity or
curve-smoothing exists to act on -- these produce an `option_not_implemented` warning if
requested), and the Konva-based visual Import Viewer (this slice's viewer is a structured-JSON
summary + warnings list in `format-interchange-app`, not a canvas rendering -- that's Step 4's
Migration Viewer work, reused here per the plan's own note that it's a shared component). Within
Step 3: real chunked/async batch processing at scale (`chunk_count` is computed and stored, but
`/run` still processes every pending item synchronously in one request, same deviation as Steps
1-2 -- Step 5's own "load-test batch migration at realistic legacy-library scale" is where this
gets hardened), any legacy source format other than IGES (Sec 6's per-format parser-module
extension point is in place via `app/migration_sources.py`, but only `iges` is registered), a
frontend panel for batches (the plan scopes the Migration Viewer itself to Step 4; Step 3's own
API surface has no UI-facing endpoints beyond the JSON/CSV report), and the `resolve`/`block`/
`accept-warning`/`commit` endpoints (Sec 5's own phased split puts these under Step 4's triage
loop, not Step 3's classification pass).
