# Apparel CAD/CAM/MES Product Suite — Complete Delivery Package
*Everything needed to feed to Claude Code for implementation, organized by application.*

## Read in this order

1. **`00_master/master_plan.md`** — START HERE. The single interconnected reference: what each
   application is, how they connect (master flowchart), the phase-by-phase build order, the
   Azure hosting/async-job architecture update, and the suite-wide language/technology matrix.
   `00_master/master_suite_flowchart.png` is the one diagram showing every application
   interconnected. `00_master/build_order.png` shows the build-order dependency graph specifically
   (which phases are parallel vs sequential).

2. **`01_data_management_platform/data_management_platform_plan.md`** — build this first. Full
   database schema (see `erd_schema.png`), API surface, identity/RBAC, and the async job-queue
   infrastructure every other app depends on (see `flow4_async_nesting_job.png` for how the
   30-minute nesting algorithm integrates as a queued job).

3. **`02_pattern_design/pattern_design_plan.md`** and **`03_marker_making_production/
   marker_making_production_plan.md`** — build these in parallel once the platform's API is
   stubbed. Each has its own full merged function catalogue (Gerber + Richpeace) and detailed
   workflow flowcharts.

4. **`04_format_interchange/format_interchange_plan.md`** — build once Pattern Design's piece
   format and Marker Making's marker format are stable.

5. **`05_3d_digital_twin/digital_twin_3d_plan.md`** — the 5th application, 3D Virtual Sampling /
   Digital Twin. Build alongside Production Output in Phase 3, once Pattern Design's piece format
   is stable. **Caveat:** unlike every other catalogue in this package, this plan's function
   catalogue was NOT verified against CLO3D/Browzwear/Optitex/Lectra Modaris vendor documentation
   — despite an earlier claim to the contrary, no web search or document fetch occurred when it
   was authored, so treat its named vendor capabilities as unverified until checked against real
   sources. It reuses the platform's async-job pattern with a GPU-backed worker tier, and
   documents a justified C++ exception to the suite's Python-everywhere rule for the physics core.

6. **`06_ui_mockups/`** — high-fidelity visual reference for the Marker Making workspace screen.
   See that folder's own README for status (a live Figma design file exists but is currently
   blocked by a Starter-plan rate limit; this screen was rendered statically as a substitute).

7. **`05_reference_function_catalogues/`** — the raw source material every per-app plan was built
   from: the full Gerber AccuMark function definitions (Pattern Design, Marker Making, Order
   Entry, IGES, Style Converter) and the full Richpeace DGS/GMS function definitions, plus the
   Richpeace-vs-Gerber comparison findings that justified several design decisions (e.g. the
   unified Marker Making + Production Output app, both nesting automation modes, the expanded
   matching toolset). Consult these if a per-app plan references a function you want more detail
   on than the plan document itself gives.

## Key architecture decisions baked into every document
- **Enterprise scale target** — full three-layer data architecture (object storage + relational
  DB + identity/RBAC) built from day one, not a lighter starting tier.
- **Microsoft Azure hosting** — Blob Storage, Azure Database for PostgreSQL, Microsoft Entra ID,
  Container Apps/AKS, Azure Service Bus for job queuing, Azure Batch/Container Apps Jobs for the
  ~30-minute nesting compute.
- **The nesting/production-planning algorithm already exists** (Python) — it is integrated as an
  async queued job, not redesigned.
- **One backend language (Python/FastAPI), one frontend language (TypeScript/React) across the
  whole suite.**
- **Marker Making and Order Entry are unified into one application** (Marker Making & Production
  Output), following the Richpeace GMS consolidation pattern rather than Gerber's historical split.

## Folder contents

| Folder | Contents |
|---|---|
| `00_master/` | Master plan, master interconnection flowchart, suite architecture, development roadmap, enterprise data architecture spec, build-order flowchart |
| `01_data_management_platform/` | Plan, 4 workflow flowcharts, ERD schema diagram |
| `02_pattern_design/` | Plan, 4 workflow flowcharts |
| `03_marker_making_production/` | Plan, 4 workflow flowcharts |
| `04_format_interchange/` | Plan, 3 workflow flowcharts |
| `05_3d_digital_twin/` | Plan, 3 workflow flowcharts (mesh construction/drape, fit review, material/export) |
| `06_ui_mockups/` | High-fidelity Marker Making workspace mockup (static render; live Figma file in progress) |
| `05_reference_function_catalogues/` | Full Gerber + Richpeace function catalogues, comparison report |
