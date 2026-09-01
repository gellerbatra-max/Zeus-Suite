# Zeus Suite

An enterprise apparel CAD/CAM/MES product suite, modeled on Gerber AccuMark's proven architecture
and enhanced with capabilities identified by comparing against the Richpeace DGS/GMS CAD system.
Hosted on Microsoft Azure.

## Start here

All planning and specification documents live under [`docs/planning/`](docs/planning/README.md).
Read `docs/planning/00_master/master_plan.md` first — it is the single interconnected reference
for the whole suite (architecture, build order, hosting, language/technology matrix) — then the
per-application plans under `docs/planning/01_data_management_platform/` through
`docs/planning/04_format_interchange/` for implementation-level detail.

## Applications in this suite

1. **Data Management Platform** — the foundation every other application is a thin client of
   (object storage, relational metadata DB, identity/RBAC, virtual folder browser).
2. **Pattern Design & Grading** — 2D pattern CAD.
3. **Marker Making & Production Output** — nesting (manual + automatic), cut-data generation,
   plotting/export, bundle/RFID tracking.
4. **Format Interchange & Legacy Migration Utility** — IGES import/export and bulk legacy data
   migration.

## Stack

Python 3.12+ / FastAPI backends, TypeScript / React (Vite) frontends, Azure Database for
PostgreSQL, Azure Blob Storage, Microsoft Entra ID, Azure Service Bus for async job queuing. See
the Language & Technology Matrix in `docs/planning/00_master/master_plan.md` for the full
breakdown per component.
