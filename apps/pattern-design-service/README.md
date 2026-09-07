# pattern-design-service

Backend for Pattern Design & Grading, Phases 2.1–2.6 (all six sub-phases in the plan's own
breakdown, see
[`docs/planning/02_pattern_design/pattern_design_plan.md`](../../docs/planning/02_pattern_design/pattern_design_plan.md)).
**This service has no database of its own** — every persistence call goes through
[`data-platform-api`](../data-platform-api)'s real REST API, the same "thin client" pattern
[`marker-making-service`](../marker-making-service) already proves out, held all the way through
grading (Phase 2.4) rather than giving this service its own Postgres schema.

## Scope, and why

The plan's own Phase 2 breaks Pattern Design into six sub-phases (§7): platform scaffolding (2.1),
full piece creation/point-editing (2.2), seams/darts/notches/grain line (2.3), grading (2.4),
measurement/digitizing/plotting/annotation (2.5), customization/automation (2.6). This build covers
all six. Piece Transformation (§4) — whole-piece rotate/flip — is a category §7's own phase
breakdown never assigns to a numbered sub-phase; it's folded into 2.5 as a small, self-contained
slice rather than left permanently unscheduled. Phase 2.6 is genuinely last for the reason the plan
itself gives: it's the largest category pair by raw function count but the lowest-risk to build,
since every tool it attaches preferences/automation to already exists by this point.

Phase 2.6 is also the first (and, deliberately, only) phase that lives entirely outside the
geometry document: a preference or a saved shape template is per-operator UI state, not piece data
-- see `pattern-design-app/src/preferences.ts` and `src/templates.ts` for why they're localStorage,
not something this service or the platform ever sees.

Two things Phase 2.1 established that every later phase reused rather than re-deciding:
- **Piece/folder/version/workflow lifecycle** — `data-platform-api` already has real, non-stub
  `/pieces`, `/pieces/{id}/versions`, and `/pieces/{id}/status` endpoints (Section 4.3 of the
  platform's own plan). This service proxies them rather than inventing parallel schema.
- **Geometry storage shape** — the plan's §3.3 structured-JSON-document-per-version design maps
  directly onto a piece version's existing Blob Storage payload; no new platform table was needed
  to store it. Every phase since has extended this one document (`app/schemas.py`'s
  `PieceGeometryDocument`) rather than adding new Postgres tables the plan's §3.2 proposes for
  grading — see that schema's docstrings for the specific deviations and why.

One thing Phase 2.1 was genuinely new work on, that every phase since has kept using: unlike
`marker-making-service` (which never uploads/downloads piece version bytes itself), this service's
whole job *is* writing and reading a piece's geometry document, so `app/blob_io.py` talks to Blob
Storage directly — using the SAS URL `data-platform-api` hands back from
`begin_version`/`download-url`, never a storage credential of this service's own.

## What's here

- `app/schemas.py` — `PieceGeometryDocument` (plan §3.3), now fully populated: `perimeter`,
  `internal_lines`, `seams`, `darts`, `notches`, `grain_line`, `grade_rule_table`, `annotations`,
  `measurements`. Each model's docstring names its plan section, its build-depth target (Gerber vs.
  Richpeace vs. union, per §4), and what's deliberately deferred within that category.
- `app/api/pieces.py` — `GET/PUT /pieces/{id}/geometry` (save/load the geometry document as an
  immutable Blob Storage-backed piece version) plus thin `GET/POST /pieces` and
  `POST /pieces/{id}/status` proxies.
- `app/api/folders.py` — thin `GET/POST /folders` proxy; a piece can't be created without a
  `folder_id` and this app has no folder concept of its own.
- `app/blob_io.py` — the one piece of Blob Storage I/O this service does that
  `marker-making-service` doesn't need.

The frontend (`pattern-design-app`) has a canvas tool per geometry category — draw/edit/add-line/
delete-line, seam, dart, notch, grain-line, grade, annotate, measure — plus rectangle/circle piece
creation, whole-piece rotate/flip, a grade-nest overlay, and a client-side-only trace-reference
image overlay for digitizing (loaded via the browser's File API, never uploaded/persisted — see
`PatternCanvas.tsx`'s overlay-layer comment for why real camera-capture persistence is deferred).
On top of that, Phase 2.6 adds a Preferences panel (display unit, grid spacing, snap-to-grid,
autosave interval, piece/background colors — all localStorage, all real: snap-to-grid actually
rounds Draw/Edit coordinates, autosave actually calls the same save path the Save Geometry button
does, on a timer decoupled from `geometry` so it doesn't reset on every keystroke) and a shape
Template library (save the current perimeter, centered on its own centroid, as a named reusable
shape; apply it to any piece via the same `replaceShapeCommand` rectangle/circle creation already
uses) — Richpeace's Motif Library / Custom curve save & reuse, scoped to perimeter shapes rather
than a general command-recording macro system, since `Command` objects (`commands.ts`) are
closures, not data `localStorage` can hold across a reload.

## Local setup

Needs `data-platform-api` fully set up and its Postgres/Azurite containers running (see
[`../data-platform-api/README.md`](../data-platform-api/README.md)).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --port 8002   # run it
pytest                              # run tests (spawns a real data-platform-api subprocess --
                                     # see tests/conftest.py's docstring for why not an in-process
                                     # ASGI transport: both services' top-level package is `app`)
```

If the shared dev Postgres database is stamped at a migration this service's own
`data-platform-api` checkout doesn't know about (e.g. another branch's uncommitted/in-progress
migration), point both the platform subprocess and `tests/helpers.py`'s direct DB connection at an
isolated database instead of fighting the shared one:

```bash
createdb -h localhost -U zeus zeus_suite_pattern_design   # once
DATABASE_URL="postgresql+psycopg://zeus:zeus@localhost:5432/zeus_suite_pattern_design" \
  .venv/bin/alembic -c ../data-platform-api/alembic.ini upgrade head   # or cd there first
DATABASE_URL="postgresql+psycopg://zeus:zeus@localhost:5432/zeus_suite_pattern_design" pytest
```

If another local session is also running `data-platform-api` on port 8000 (e.g. testing a
different branch against the shared `zeus_suite` database), don't fight over the port: run this
service's own manual platform instance on a different port (`--port 8010` or similar) and point
`pattern-design-service` at it with `PLATFORM_API_URL=http://localhost:8010`. The shared Postgres
*container* itself isn't immune to this either — another session restarting it (or its compose
stack) can silently drop an isolated database created this way; if a previously-working manual
setup suddenly reports "database ... does not exist", that's what happened, not a code regression
-- just recreate it.

## Deferred (flagged, not built here)

Within each built category, the deep catalogue variants named in `app/schemas.py`'s docstrings
(corner-mitering seam types, dart rotate/combine/distribute, sign/axis grading paste operations,
etc.) — §4's full catalogue is ~950 raw functions across all categories combined. Also deferred
entirely: `graded_pieces` materialization (separate platform `pieces` rows per graded size — Sec
3.2), real camera-capture calibration and server-side contour auto-detection for digitizing (Sec
6.5), single-piece DXF/AAMA-ASTM import/export, a general command-recording macro system (only
perimeter-shape templates are built — see above), toolbar/menu docking and screen-layout
persistence, and the legacy AccuMark/MicroMark menu-emulation modes the plan itself flags as
optional migration aids, not required build items.
