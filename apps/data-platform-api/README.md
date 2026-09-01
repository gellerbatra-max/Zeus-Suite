# data-platform-api

Foundation service of the Zeus Suite (see [`docs/planning/00_master/master_plan.md`](../../docs/planning/00_master/master_plan.md)).
This covers Milestones 1–4 of [`data_management_platform_plan.md`](../../docs/planning/01_data_management_platform/data_management_platform_plan.md#8-phased-build-plan-for-this-application):
schema/migrations, object storage (SAS URLs against Azurite), permission resolution + JIT user
provisioning, and now the Section 4.1–4.7 REST API itself (folders, pieces, styles, markers,
orders/bundles, workflow metadata, audit log) — the literal Phase 1 exit criteria: a stub client
can create/lock/version/transition a piece and read its full history back, entirely over HTTP.

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

# 5. Run the test suite (Milestone 1-4 exit checks)
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

## Useful commands

```bash
alembic upgrade head          # apply all migrations
alembic downgrade base        # drop everything (dmp schema, cascade)
alembic revision -m "..."     # new migration (write raw SQL for schema changes to keep parity
                               # with the spec document; don't rely on --autogenerate for
                               # triggers/tsvector/gin-trgm indexes)
pytest                        # run the smoke + constraint test suite
```
