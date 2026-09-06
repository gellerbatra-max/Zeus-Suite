# format-interchange-service

Backend for the Format Interchange & Legacy Migration Utility, Step 1 of Phase 3 (see
[`docs/planning/04_format_interchange/format_interchange_plan.md`](../../docs/planning/04_format_interchange/format_interchange_plan.md)
Sec 7): single-piece IGES export -- "the smallest complete slice."

## How this differs from every other app built so far

`pattern-design-service` and `marker-making-service` are pure thin clients with no database of
their own. This service genuinely owns one (Sec 4: "This service's own database ... holds only
interchange-specific bookkeeping"): `interchange_job` (this slice), with `import_profile`/
`migration_batch`/`migration_item`/`migration_finding` reserved for Steps 2-4. It's the first app
in this delivery built with its own Alembic/SQLAlchemy setup alongside `data-platform-api`'s.

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
  isn't a piece version, so it never goes through the platform's `begin_version` dance).
- `alembic/` -- `format_interchange` schema, `interchange_job` table only (Step 1's needs).

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

Everything past Step 1 of Sec 7's phased plan: IGES **import** (Step 2 -- the reader, Import
Profiles, the Import Viewer with staged-commit), the Legacy Migration batch pipeline and its full
error/warning catalogue (Step 3), the Migration Viewer and triage-and-fix loop (Step 4), and
load/audit/RBAC hardening (Step 5). Within Step 1 itself: batch export (`POST /export/iges/batch`),
`entity_profile` target-system curve preferences (no curve/spline entity exists yet to have
preferences about), and a dedicated worker service-account identity for pushing the platform `Job`
through its real `heartbeat`/`complete` lifecycle (see `app/api/export.py`'s docstring).
