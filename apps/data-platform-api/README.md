# data-platform-api

Foundation service of the Zeus Suite (see [`docs/planning/00_master/master_plan.md`](../../docs/planning/00_master/master_plan.md)).
This is Milestone 1 of [`data_management_platform_plan.md`](../../docs/planning/01_data_management_platform/data_management_platform_plan.md#8-phased-build-plan-for-this-application):
schema + migrations only. No API routes yet — those land in Milestone 4 once object storage
(Milestone 2) and auth/RBAC (Milestone 3) exist.

## Local setup

```bash
# 1. Start Postgres (+ Azurite, for the upcoming Milestone 2) from the repo root
docker compose -f ../../infra/docker-compose.yml up -d

# 2. Create a virtualenv and install this package
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 3. Copy the env file (defaults already match docker-compose.yml)
cp ../../.env.example ../../.env

# 4. Apply the schema + seed data (no manual SQL — this is the whole database)
alembic upgrade head

# 5. Run the test suite (Milestone 1 exit check)
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
- `tests/test_schema_smoke.py` — inserts one row per table across a full realistic FK chain
  (org → user → folder → piece → piece_version → style → marker → order → bundle → job → …).
- `tests/test_constraints.py` — a handful of representative CHECK/UNIQUE constraint violations.

## Useful commands

```bash
alembic upgrade head          # apply all migrations
alembic downgrade base        # drop everything (dmp schema, cascade)
alembic revision -m "..."     # new migration (write raw SQL for schema changes to keep parity
                               # with the spec document; don't rely on --autogenerate for
                               # triggers/tsvector/gin-trgm indexes)
pytest                        # run the smoke + constraint test suite
```
