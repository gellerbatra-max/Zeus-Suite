# pattern-design-service

Backend for Pattern Design & Grading, Phase 2.1 (see
[`docs/planning/02_pattern_design/pattern_design_plan.md`](../../docs/planning/02_pattern_design/pattern_design_plan.md)).
**This service has no database of its own** — every persistence call goes through
[`data-platform-api`](../data-platform-api)'s real REST API, the same "thin client" pattern
[`marker-making-service`](../marker-making-service) already proves out.

## Scope of this slice, and why

The plan's own Phase 2 breaks Pattern Design into six sub-phases (§7): platform scaffolding, full
piece creation/point-editing, seams/darts/notches/grain line, grading, measurement/digitizing/
plotting, customization/automation. This is **Phase 2.1 only** — platform integration scaffolding
plus the core piece lifecycle. Its exit criteria (§7): *"a piece with just a drawn perimeter
round-trips through Blob Storage and Postgres correctly, including workflow status."*

Two things this slice deliberately reuses rather than builds:
- **Piece/folder/version/workflow lifecycle** — `data-platform-api` already has real, non-stub
  `/pieces`, `/pieces/{id}/versions`, and `/pieces/{id}/status` endpoints (Section 4.3 of the
  platform's own plan). This service proxies them rather than inventing parallel schema.
- **Geometry storage shape** — the plan's §3.3 structured-JSON-document-per-version design maps
  directly onto a piece version's existing Blob Storage payload; no new platform table was needed
  to store it.

One thing this slice is genuinely new work on: unlike `marker-making-service` (which never
uploads/downloads piece version bytes itself), this service's whole job *is* writing and reading a
piece's geometry document, so `app/blob_io.py` talks to Blob Storage directly — using the SAS URL
`data-platform-api` hands back from `begin_version`/`download-url`, never a storage credential of
this service's own.

## What's here

- `app/schemas.py` — `PieceGeometryDocument` (plan §3.3): `perimeter` is the only part any tool in
  this slice writes; `seams`/`darts`/`notches`/`grain_line`/`annotations` are already in the schema
  so Phase 2.3 doesn't need a `schema_version` bump to start using them.
- `app/api/pieces.py` — `GET/PUT /pieces/{id}/geometry` (the new part: save/load the geometry
  document as an immutable Blob Storage-backed piece version) plus thin `GET/POST /pieces` and
  `POST /pieces/{id}/status` proxies.
- `app/api/folders.py` — thin `GET/POST /folders` proxy; a piece can't be created without a
  `folder_id` and this app has no folder concept of its own.
- `app/blob_io.py` — the one piece of Blob Storage I/O this service does that
  `marker-making-service` doesn't need.

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

## Deferred (flagged, not built here)

Everything past Phase 2.1: the full draw/trace/extract point-and-line editing toolset (§4 Piece
Creation, Point/Line Editing), seams/darts/pleats/notches/grain line (Phase 2.3), the grading
engine (Phase 2.4), measurement/digitizing/plotting/annotation (Phase 2.5), and
customization/automation (Phase 2.6). The frontend's canvas (`pattern-design-app`) in this slice
only supports drawing and saving a straight-line perimeter — no curves, no point/line editing
tools, no seam allowance.
