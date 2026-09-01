# data-platform-api

Foundation service of the Zeus Suite (see [`docs/planning/00_master/master_plan.md`](../../docs/planning/00_master/master_plan.md)).
This covers Milestones 1–6 of [`data_management_platform_plan.md`](../../docs/planning/01_data_management_platform/data_management_platform_plan.md#8-phased-build-plan-for-this-application):
schema/migrations, object storage (SAS URLs against Azurite), permission resolution + JIT user
provisioning, the Section 4.1–4.7 REST API (folders, pieces, styles, markers, orders/bundles,
workflow metadata, audit log) — the literal Phase 1 exit criteria: a stub client can
create/lock/version/transition a piece and read its full history back, entirely over HTTP —
Section 4.8's search/cross-reference ("Find" utility equivalent), Section 2.12/3.5-3.8/4.12's
generic async job queue, and Section 4.10's reports API (added to unblock Milestone 7's reporting
UI, which needed something to call). CORS is enabled for `localhost:5173` so
[`../data-management-app`](../data-management-app) (Milestone 7's React frontend) can call this
API directly in local dev.

Run it locally with `uvicorn app.main:app --reload` (from this directory, venv active) once the
steps below are done; interactive docs at `http://localhost:8000/docs`. Auth is a **local-dev
stub** — send `X-Dev-User: <username>` (and optionally `X-Dev-Org`, default `DEV`) on every
request instead of a real bearer token; see `app/auth.py` and `app/deps.py` for the real-Entra-ID
swap-over path once tenant access exists. A brand-new dev user gets the `viewer` role only — granting
anything more (e.g. `admin`) needs a direct DB write today, since Section 4.11's RBAC-admin
endpoints aren't built yet (see `tests/test_api_milestone4.py` for the pattern).

## Local setup

```bash
# 1. Start Postgres + Azurite from the repo root
docker compose -f ../../infra/docker-compose.yml up -d

# 2. Create a virtualenv and install this package
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 3. Copy the env file (defaults already match docker-compose.yml)
cp ../../.env.example ../../.env

# 4. Apply the schema + seed data (no manual SQL — this is the whole database)
alembic upgrade head

# 5. Run the test suite (Milestone 1-6 exit checks)
pytest
```

## What's here

- `app/models/` — SQLAlchemy models mirroring `data_management_platform_plan.md` Section 2
  table-for-table, column-for-column. These are the query-time mapping layer; the schema itself
  is defined independently in the Alembic migration below (see the note in `app/models/__init__.py`
  for why).
- `alembic/versions/0001_initial_schema.py` — the full DDL from Section 2, transcribed close to
  verbatim, in FK-safe order.
- `alembic/versions/0002_seed_reference_data.py` — workflow statuses/transitions, the generated
  permission catalogue, roles, role_permissions, and report_definitions (Appendices A & B). Two
  small extensions beyond the literal appendix tables are called out in that file's docstring.
- `app/storage.py` — Section 3.3's SAS-URL issuance (upload/download), using Azurite account-key
  SAS as the local-dev stand-in for real user-delegation SAS (see the module docstring for the
  swap-over path once real Azure/Entra ID access exists).
- `app/auth.py` — Section 5.2's permission-resolution function (org-wide + folder-scoped grants,
  ancestor-folder inheritance, no caching) and Section 5.4's JIT user provisioning. `dev_login` is
  a local-dev auth stub standing in for real Entra ID OIDC/JWT validation (see module docstring).
- `tests/test_schema_smoke.py` — inserts one row per table across a full realistic FK chain
  (org → user → folder → piece → piece_version → style → marker → order → bundle → job → …).
- `tests/test_constraints.py` — a handful of representative CHECK/UNIQUE constraint violations.
- `tests/test_storage_smoke.py` — SAS-URL upload/download round-trip against Azurite.
- `tests/test_auth.py` — JIT provisioning (create + update) and permission resolution (org-wide,
  folder-scoped, ancestor inheritance, immediate revocation).
- `alembic/versions/0003_add_optimistic_concurrency_version.py` — adds the `version` integer
  column Section 4.0's `If-Match-Version` contract needs but Section 2's DDL never defines (a gap
  between the API-conventions and schema sections of the same spec doc, flagged in the migration's
  docstring).
- `app/api/` — the Section 4 routers (folders, pieces, styles, markers, orders/bundles, workflow
  metadata, audit log), `app/deps.py` (the shared permission-check-then-audit-write path every
  handler calls into), `app/workflow_engine.py` (status-transition validation), `app/auditing.py`
  (the one place that writes `audit_log` rows), and `app/serializers.py` (ORM row → response schema).
- `tests/test_api_milestone4.py` — the literal Milestone 4 exit check end-to-end over HTTP, plus
  permission-denial and optimistic-concurrency-conflict coverage.
- `alembic/versions/0004_add_code_trgm_indexes.py` — pg_trgm GIN indexes on entity code fields
  (piece_code, style_number, etc.) for Section 4.8's "substring fallback" search behavior, which
  Section 2's DDL only ever wired up for `folders.path` — the same category of spec gap as
  migration 0003, closed the same way.
- `app/search_service.py` — Section 4.8's structured search, typeahead suggest, and one-hop
  cross-reference graph: Postgres FTS + trigram substring matching, cross-reference-anchor
  resolution, and permission-scoped result filtering (`resolve_read_scope`, distinct from
  `app/auth.py`'s single-resource `resolve_permissions` — this one resolves every folder a caller
  can read an entity type in, once per request, so a page of results is filtered in memory
  instead of re-querying RBAC per row).
- `tests/test_search.py` — the literal Milestone 5 exit check: a ~500-row interlinked dataset,
  free-text and cross-reference-anchored queries both correct and sub-200ms, plus cross-tenant
  isolation and folder-scoped-permission filtering.

**Note:** building Milestone 5 surfaced a real cross-tenant data leak in Milestones 1-4's by-ID
lookups (`GET /pieces/{id}` etc. never checked the entity's `organization_id` against the caller's
own) — fixed in the same pass across every entity router, not scoped to search alone.

- `alembic/versions/0005_add_job_heartbeat_column.py` — adds `jobs.last_heartbeat_at`, the clock
  Section 3.7's timeout sweep is supposed to watch but Section 2.12's DDL never gives it a column
  for — the third instance of this pattern (see migrations 0003 and 0004).
- `app/job_service.py` — the generic async job pattern (Section 2.12/3.5-3.8/4.12): submit,
  heartbeat, complete, cancel, and the timeout sweep, all as plain functions shared by the HTTP
  routes and the worker so both paths produce identical audit/`job_events` trails.
  `dequeue_and_claim_job` is the local stand-in for real Azure Service Bus (not available without
  an Azure subscription) — an atomic `SELECT ... FOR UPDATE SKIP LOCKED` claim instead of a real
  queue delivery, clearly boundaried so swapping in Service Bus later only touches this function.
- `app/job_worker.py` — the local worker: dequeues via the substitute above, then reports
  progress/completion through the *real* HTTP endpoints using a service-account identity holding
  only `job.worker`, so the same permission checks and audit trail apply as a real out-of-process
  Celery worker would produce. `JOB_HANDLERS` in `job_service.py` holds the
  `marker_nesting_solve` stub (sleep-and-echo, per Milestone 6's own instruction not to build the
  real ~30-minute algorithm here) — Marker Making's build swaps in the real one later.
- `app/api/jobs.py` — Section 4.12's REST surface: `POST /jobs`, `GET /jobs`, `GET /jobs/{id}`,
  `GET /jobs/{id}/events`, `POST /jobs/{id}/cancel`, and the worker-only
  `POST /jobs/{id}/heartbeat` / `.../complete` (gated on `job.worker`, never granted to a human role).
- `tests/test_jobs.py` — the literal Milestone 6 exit check: 20 jobs submitted, drained by 4
  concurrent worker threads with no double-processing (proving the SKIP LOCKED claim is
  concurrency-safe), a complete `job_events` trail per job, plus cancellation, a deliberately
  induced timeout, and worker-permission enforcement.
- `app/report_service.py` + `app/api/reports.py` — Section 4.10's reports API, never built in
  Milestones 4-6. Every report here runs synchronously (`result_inline`) since none of the seeded
  codes are expensive enough to need the async job path; `single_piece`, `all_piece`, and
  `all_marker` are implemented, while the geometry-dependent codes (`piece_perimeter`,
  `all_layrule`, `all_plot`, `all_cut`, `splice`) return `501` on purpose — they need piece/marker
  geometry this platform stores as an opaque blob (Pattern Design's/Marker Making's domain, not
  this platform's). `tests/test_reports.py` covers both paths plus permission enforcement.

- `alembic/versions/0006_add_matching_tables.py` + `app/api/matching.py` — Marker Making Phase 2
  Slice 2's one platform-side schema addition: `dmp.matching_rule_tables` (plaid/stripe matching
  config: method, plaid/stripe repeat, and opaque `offsets_json`/`stripe_definitions_json`/
  `stripe_marks_json`, mirroring the opaque-payload philosophy `marker_pieces.placement_data`
  already established) plus `markers.matching_rule_table_id`. This platform stores and returns
  that JSON faithfully — it does not interpret stripe/offset structure; that's
  [`marker-making-service`](../marker-making-service)'s job. `tests/test_matching.py` covers CRUD,
  the sub-resource full-replace endpoints, marker linkage (including a cross-org guard), the
  delete-while-referenced conflict, and permission enforcement; `tests/test_constraints.py` covers
  the `method` CHECK and `(organization_id, name)` UNIQUE constraints.

## Useful commands

```bash
alembic upgrade head          # apply all migrations
alembic downgrade base        # drop everything (dmp schema, cascade)
alembic revision -m "..."     # new migration (write raw SQL for schema changes to keep parity
                               # with the spec document; don't rely on --autogenerate for
                               # triggers/tsvector/gin-trgm indexes)
pytest                        # run the smoke + constraint test suite
```
