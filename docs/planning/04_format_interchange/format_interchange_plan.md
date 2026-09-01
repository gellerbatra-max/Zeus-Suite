# Format Interchange & Legacy Migration Utility — Unified Implementation Plan

> **Languages & Frameworks for this app:** Backend API — Python 3.12+, FastAPI, Pydantic;
> database access via SQLAlchemy + Alembic against Azure Database for PostgreSQL Flexible Server;
> IGES parsing and Style Converter geometric checks — Python, Shapely + NumPy; frontend — TypeScript
> + React (Vite), shared Konva.js viewer component. Same suite-wide stack as every other
> application in this delivery; see the Language & Technology Matrix in `master_plan.md`.



> **Hosting update:** this suite is hosted on Microsoft Azure. Object storage references below
> mean Azure Blob Storage, "PostgreSQL" means Azure Database for PostgreSQL Flexible Server, and
> the SSO layer is Microsoft Entra ID (Azure AD) -- substituted throughout from the generic
> service names used when this document was first drafted.



*Application 4 of 4 in the suite (`suite_architecture.md`). Phase 3 of the roadmap
(`development_roadmap.md`), built in parallel with Production Output, once Pattern Design's piece
data model is real. Modeled on Gerber's IGES Translator (`IGESOUT.EXE` / `IGES.EXE`) and Style
Converter, cross-referenced against the enterprise data architecture
(`enterprise_data_architecture.md`).*

## 0. Scope and boundaries

This application owns exactly two modules, per `suite_architecture.md` §4:

1. **Piece Interchange module** — IGES-equivalent import/export for moving individual pattern
   pieces between this suite and other CAD systems (competitor apparel CAD, mechanical CAD, or a
   customer's own system).
2. **Legacy Migration module** — a Style-Converter-equivalent bulk utility for converting an
   incoming customer's or predecessor system's pattern library (potentially thousands of styles)
   into this suite's native format, including the viewer-based error/warning triage workflow
   Gerber's Style Converter uses.

**Out of scope, by suite design:**
- This app is a thin client against the Data Management Platform (per the Integration Model in
  `suite_architecture.md`): it has no local database, and reads/writes pieces, grade rule tables,
  and size charts exclusively through that platform's API. It never talks to Pattern Design or
  Marker Making directly.
- Nesting, marker geometry, and cut-data formats belong to Marker Making & Production Output —
  this app deals only in piece-level geometry.
- Bulk *native* format converters (e.g. a generic DXF/AAMA-ASTM import path used for day-to-day
  data browsing) were tentatively scoped under the Data Management Platform's "AccuMark Explorer
  equivalent" in `enterprise_data_architecture.md` before the final app boundaries were fixed. Per
  the now-authoritative `suite_architecture.md`, all CAD-to-CAD piece interchange — including any
  future DXF/AAMA-ASTM piece-level path — belongs in this app's Piece Interchange module, built on
  the same import/export pipeline described in §1. It is not built in Phase 3; noted here only so
  a future extension has a documented home instead of being bolted onto the platform app.

## 1. Function catalogue — Piece Interchange module (IGES-equivalent)

Gerber splits this into two command-line executables (`IGESOUT.EXE`, `IGES.EXE`) plus a static INI
file. The modern equivalent is a set of REST endpoints on a `format-interchange-service`
FastAPI microservice, backed by an async job queue (conversions are not guaranteed sub-second), a
saved-parameter-preset entity replacing the INI file, and a web-based Import Viewer replacing the
manual "open in Pattern Design and eyeball it" verification step.

### 1.1 Export (replaces `IGESOUT.EXE`)

| Gerber function | Modern equivalent | Notes |
|---|---|---|
| `IGESOUT <storage_area> <piece_name> <IGES_filename>` | `POST /pieces/{piece_id}/export/iges` | `piece_id` resolves via the platform API; no local storage-area path. Returns an async `job_id`. |
| `/?` / `/h` help screen | OpenAPI schema / interactive API docs | Standard FastAPI `/docs`; no bespoke help command needed. |
| `/U<u>` unit override | `unit` request param (`in` \| `mm` \| `cm`) | Applied as a coordinate transform before entity mapping if it differs from the piece's native unit. |
| *(implicit: full piece geometry)* | `include_grading`, `include_internal_lines`, `include_notches`, `include_grain_line`, `include_drill_holes` boolean params | Gerber exports whatever the piece has; the modern version makes each geometry class an explicit opt-in/out so a caller can request a bare outline. |
| *(new — not in Gerber)* | `entity_profile` param: `generic` \| `target_system:<name>` | Some receiving CAD systems expect specific IGES entity types (e.g. Type 126 rational B-spline vs. Type 112 parametric spline) for the same curve; profiles let the export map curve types to the target system's known preferences instead of one fixed mapping. |
| *(new)* | Batch export: `POST /export/iges/batch {piece_ids: [...]}` | Returns a zip of individual IGES files (one piece per file, matching how receiving systems expect one-piece-per-file) plus a manifest. |
| *(new)* | `GET /export/iges/jobs/{job_id}` | Job status/result polling: `queued` \| `running` \| `succeeded` \| `failed`, with a download URL or structured error on completion. |

**Internal geometry → IGES entity mapping** (used by the export pipeline):

| Piece geometry | IGES entity type |
|---|---|
| Outline (straight segments) | Type 110 (Line), assembled into a Type 102 Composite Curve |
| Outline (curved segments) | Type 100 (Circular Arc) or Type 126 (Rational B-Spline Curve), in the same composite curve |
| Internal lines (pocket lines, style lines) | Type 106 (Copious Data) or Type 110/126 as above |
| Notches | Type 106 (Copious Data, form 11 — point sequence) tagged as a notch via a Type 406 property entity |
| Grain line | Type 110 (Line) + Type 406 property entity marking it as the grain-line reference |
| Drill holes | Type 116 (Point) |
| Grade rule references | Type 406 (Property) entities carrying rule-table name and rule number per grade point — not a standard IGES convention, but necessary for round-tripping to another instance of this suite or to a system with a compatible extension |

**Export validation gate:** before entity mapping, the pipeline re-runs the same self-intersection
and closure checks used by Pattern Design's save validation (§3 of the flowchart). A piece that
fails either check is rejected with the offending segment's coordinates rather than silently
exporting broken geometry — Gerber's IGESOUT has no equivalent check and will happily export a
self-intersecting outline.

### 1.2 Import (replaces `IGES.EXE`)

| Gerber option | Modern equivalent | Notes |
|---|---|---|
| `IGES <in> <out> [options]` | `POST /import/iges` (multipart file upload + JSON params) | Returns an async `job_id`. |
| `-A<n>` closure amount | `closure_amount_mm` (float, converted from Gerber's hundredths-of-an-inch) | Auto-bridges gaps ≤ this distance so the outline closes. |
| `-T<d>` trimming | `trim_tolerance` (float) | Douglas–Peucker-style collinear-point removal; `d` controls sensitivity. |
| `-G` grade points | `infer_grade_points` (bool) | Maps the incoming file's point-numbering convention to grade-point tags. Requires a `numbering_scheme` in the Import Profile (see §1.3) telling the parser which numbering convention is in use, since this is not a fixed IGES standard. |
| `-MA<n>` max arc points | `max_arc_points` (int) | Tessellation cap for arcs, to bound render/processing cost on pathological input. |
| `-MB<n>` max spline points | `max_spline_points` (int) | Same, for splines. |
| `-I` paste internals | `paste_internal_to_notch` (bool) | If an internal line's endpoint lies on the outline within tolerance, convert that endpoint into a notch instead of leaving a dangling internal line. |
| `-L` / `-P` logging | Structured job log returned via `GET /import/iges/jobs/{job_id}/log` | No separate print-vs-screen distinction; the log is always captured and queryable. |
| `-D` point → drill hole | `points_to_drill_holes` (bool) | Converts bare Type 116 point entities into drill-hole markings. |
| `-U<u>` unit correction | `unit_override` (`in` \| `mm` \| `cm` \| `null`=auto-detect) | If the file's declared unit produces an implausible piece size (heuristic: bounding box outside a configurable plausible range for a garment piece), the pipeline flags a warning rather than silently guessing. |
| `-S` force sharp corners | `force_sharp_corners` (bool) | Disables curve-smoothing/blending at vertices. |
| `-O<storage_area>` online import | `target_collection` (string) + `stage_only` (bool) | If `stage_only=false`, the converted piece is committed straight to the named platform collection; if `true`, it is held in a staging area pending a separate `POST /import/iges/jobs/{job_id}/commit` call after visual review. |

### 1.3 Saved parameter presets (replaces `IGES.INI`)

Gerber's INI file is a static, single-machine config. The modern equivalent is an **Import
Profile** entity, owned by this service and reusable per trading partner:

- `StorageAreaName=` → `target_collection` field on the Import Profile.
- `PieceNameAtLine=` / `DescriptionAtLine=` / `CategoryAtLine=` → a `field_extraction` map on the
  profile, generalized beyond "fixed line number" to also support: a named IGES Type 406 property
  slot, a regex against the filename, or a fixed line number (kept for parity with legacy
  exporters that still emit metadata as leading comment lines).
- `numbering_scheme` (new, needed for `-G`/`infer_grade_points` above): identifies which
  point-numbering convention the trading partner's system uses, so grade-point inference is
  deterministic instead of guessed per file.

A caller passes `import_profile_id` on `POST /import/iges` instead of repeating every parameter;
this is the direct replacement for "not having to type the same options every time."

### 1.4 Post-import verification (replaces the manual "open in Pattern Design and look at it" step)

Gerber's manual step (open the IMPORT DATA editor, press F1, then open the piece in Pattern Design
to eyeball it) becomes the **Import Viewer**, a required stop in the pipeline before commit:

- Renders the converted piece geometry (outline, internals, notches, grain line, drill holes)
  immediately after conversion, without a save round-trip through Pattern Design.
- Overlays a rendering of the raw IGES source geometry underneath, so smoothing/trimming/closure
  changes made by the pipeline are visible, not just the final result.
- Surfaces every warning generated during conversion (unit-mismatch heuristic triggered, points
  trimmed, gaps auto-closed, etc.) as an annotated marker on the geometry it affects.
- Gate: commit to `target_collection` is blocked until the caller explicitly approves (or the job
  was submitted with an `auto_approve=true` flag for trusted, previously-validated trading
  partners running unattended batch feeds).

## 2. Function catalogue — Legacy Migration module (Style-Converter-equivalent)

This is a batch pipeline plus a comparison viewer, backed by the same `format-interchange-service`
but operating on **batches of styles** rather than single pieces, and reading source data in
whatever legacy format the predecessor system used (proprietary binary, DXF/AAMA-ASTM, or a
structured export the customer provides) rather than IGES specifically.

### 2.1 Batch workflow functions

| Gerber Style Converter function | Modern equivalent |
|---|---|
| Select style(s) to convert, with wildcard support above ~2,000 styles | `POST /migration/batches {selection: {pattern: "ABC*", source: "<uploaded folder / connector>"}}`. The service auto-chunks any batch above a configurable threshold (default 2,000, matching Gerber's documented recommendation) into sequential sub-jobs rather than requiring the user to chunk manually. |
| Inspection Options (auto-sort flagged styles into a problem folder) | `auto_sort_flagged` (bool) on the batch request. When true, any item classified `warning` or `error` is automatically added to a **Needs Review** collection (the modern equivalent of the `C:\ads` problem folder) instead of a filesystem move. |
| Convert / Run | `POST /migration/batches/{batch_id}/run` — submits the batch to the async job queue; runs are idempotent per item so a re-run only reprocesses items that changed. |
| Results dialog (counts + offer to sort flagged items) | `GET /migration/batches/{batch_id}` returns `{converted, converted_with_warning, error, blocked}` counts; sorting into Needs Review already happened per-item if `auto_sort_flagged=true`. |
| Report Results (CSV export of every warning/error) | `GET /migration/batches/{batch_id}/report.csv` (and `.json`) — one row per finding, with `item_id`, `source_style_ref`, `code`, `severity`, `message`, and a deep link to that item in the Migration Viewer. |

### 2.2 Migration Viewer (replaces the Style Converter Viewer)

| Gerber function | Modern equivalent |
|---|---|
| Side-by-side / overlaid old vs. new piece comparison | Canvas-based overlay of source-system geometry (parsed read-only) against converted geometry, using the same Konva.js/canvas renderer as Pattern Design, in a distinct "diff" render mode (old in one color/line style, new in another, both semi-transparent). |
| Measure function | Click-two-points distance readout, reusing Pattern Design's measurement tool component. |
| Snap to Geometry | An "align" toggle that translates/rotates the old overlay onto the new one by a shared reference point (e.g. matched grade-point-zero or notch), so only true shape differences remain visible instead of a incidental origin offset. |

### 2.3 Error catalogue — condition → modern check → fix path

Each row is a direct translation of one Gerber Style Converter **error** (blocks migration of that
item until resolved) into a concrete, implementable check against this suite's data model.

| Gerber error | Modern check | Modern fix path |
|---|---|---|
| Intersection error while grading piece | Run a polygon self-intersection test (e.g. Shapely `is_valid` / `is_simple`) against the base-size outline **and every graded size** produced by applying the piece's grade rules. | Flag item `error: self_intersection`, record the offending size and segment coordinates. Fix path: deep link opens the piece in Pattern Design's outline/grade-rule editor pre-scrolled to the offending point. |
| Piece modification has invalidated a corner angle | Recompute the actual angle at every point carrying an assigned corner-treatment type (e.g. notch corner, blunt corner) and check it against that treatment's valid angle range. | Flag `error: invalid_corner_angle` with computed vs. expected range. Fix path: resolution UI offers the closest valid corner type as a one-click reassignment, or opens the point in Pattern Design for manual correction. |
| Unable to store, 2 F points required (two grain lines) | Count grain-line entities per piece during parse; flag if > 1 (the platform's piece schema, like AccuMark's, holds exactly one grain line per piece). | Flag `error: multiple_grain_lines`. Fix path: resolution UI lists both source grain lines and lets the user pick which one becomes canonical before re-running conversion for that item — no need to go back to the source system. |
| Failed MicroMark grading (missing update / damaged grade rule) | Before attempting the geometry transform, validate that every grade rule table referenced by the source style parses cleanly (checksum/structure check appropriate to the source format). | Flag `error: source_grading_corrupt`. Fix path: this one *does* require a corrected source export — mark `blocked`, emit a correction note naming the damaged table, and hold the item for a corrected re-upload (see §2.5). |
| Invalid matching lines (plaid/stripe match line not parallel/perpendicular to grain) | Compute the angle between each declared match line and the piece's grain-line vector; flag if it is not within tolerance of 0° or 90°. | Flag `error: invalid_match_line` with the measured angle. Fix path: deep link to Pattern Design's match-line editor with the offending line pre-selected. |
| Rule Table missing | Resolve every grade-rule-table reference against the platform's grade rule table registry at parse time. | Flag `error: rule_table_missing` naming the unresolved reference. Fix path: resolution UI offers (a) map to an existing platform grade rule table by name, or (b) upload the correct source table and re-run just this item. |
| MicroMark sizes missing (synonym table not processable) | Detect a source-format size-synonym/rename table that does not reduce to a 1:1 mapping onto the platform's size-chart model. | Flag `error: unresolvable_size_synonym`. Fix path: resolution UI shows the synonym table and lets the user collapse it to direct size codes (drop the synonym layer) or map it onto an existing platform size chart. |
| Missing OPP Grade Axis | For every grade point whose rule type requires a directional reference axis, verify one is defined. | Flag `error: missing_grade_axis`. Fix path: deep link to Pattern Design's point editor to define the reference direction; item re-queued for re-conversion once saved. |
| Cannot find rule –1 (placeholder/invalid rule number) | Resolve every point's assigned grade-rule number against the rule table at parse time; flag any that don't resolve (not just the literal sentinel `-1` — any unresolvable reference). | Flag `error: invalid_rule_reference` naming the point and the unresolved number. Fix path: resolution UI lets the user assign a valid rule number directly, or opens the point in Pattern Design. |

### 2.4 Warning catalogue — condition → modern log entry

These do **not** block migration; the item still converts, but the finding is recorded against it
for review, matching Gerber's "informational" framing.

| Gerber warning | Modern log entry |
|---|---|
| Piece was flipped, grain line realigned to maintain flip state | `warning: flip_grain_realigned` — logged with old/new grain-line orientation. |
| Piece with grain line converted to F Rotation will not rotate the same way in marking | `warning: rotation_behavior_change` — logged so Marker Making QA can spot-check nesting behavior for this piece. |
| Piece message has been truncated (32→20-char field) | `warning: description_truncated` — logged with full original text preserved in the finding record even though the piece's `description` field is truncated to the platform's field length. |
| Cut lines not present — sew perimeter used for comparison | `warning: cut_line_absent_used_sew_perimeter` — logged; piece stored with sew-line perimeter only, matching source. |
| Unavailable rules converted to 0 growth | `warning: rule_unresolved_zero_growth` — logged with point/line reference so grading can be manually corrected later without waiting on this migration. |
| Tangent rule not valid on points, replaced with 0 growth | `warning: invalid_tangent_rule_zero_growth` — logged with point reference. |

### 2.5 Viewer diff-highlight catalogue

| Gerber Viewer diff type | Modern Migration Viewer feature |
|---|---|
| Intersection Moved | Highlight the corner point; Measure tool pre-anchored to old/new position, distance shown numerically. |
| Curves Different | Per-size curve-deviation highlight; report max and RMS deviation between old and new curve samples for the size currently displayed. |
| Changes in Notches | List of added/removed/moved notches with before/after coordinates; each entry highlights its notch on the canvas when clicked. |
| Overall Perimeter Changes | Whole-outline highlight plus an offset vector (magnitude + direction) when only the reference origin moved, not the shape. |
| Sizes has variations and cannot be converted | Item flagged `error: unresolvable_size_synonym` (§2.3) with a direct link from the Viewer into the size-chart resolution UI — the Viewer surfaces it, the migration-batch error path fixes it. |

### 2.6 Triage-and-fix loop (batch-level behavior)

This is the workflow Gerber's Style Converter implies (Inspection Options → problem folder →
manual review in the Viewer → re-run) made explicit as a stateful loop, detailed in the flowchart
in §3.3:

1. Every `error` item is auto-sorted into Needs Review if Inspection Options is on.
2. Each Needs Review item is either resolved in-tool (resolution UI mutates the source-side mapping
   and re-runs conversion for that item only) or marked `blocked` pending a corrected source
   re-upload.
3. `warning` items do not block the batch but require an explicit accept-as-is before the batch
   commits, so warnings cannot silently slip past review on a large batch.
4. Only `converted`, `converted_with_warning` (accepted), and `resolved` items commit to the
   platform in one batch-commit call; `blocked` items remain queued.

## 3. Workflow flowcharts

### 3.1 Single-piece IGES export

![IGES export flowchart]({{artifact:49c1b4dc-def2-4e33-b278-70bce737b639}})

Piece geometry is fetched from the platform, validated for export-readiness (unit consistency,
grading completeness if requested, self-intersection/closure), mapped to IGES entities per the
table in §1.1, written to object storage, and delivered either as a download or a direct push to a
configured external endpoint. Both validation failure paths return actionable errors rather than
emitting broken geometry.

### 3.2 Single-piece IGES import with error handling

![IGES import flowchart]({{artifact:283bb3c3-4a74-4bea-9815-37347f38883a}})

Every `IGES.EXE` command-line option becomes an explicit decision branch: parse validity, closure
tolerance (with auto-close retry), point-numbering-based grade-point inference, internal-to-notch
conversion, point-to-drill-hole conversion, unit-mismatch handling, and forced sharp corners. The
pipeline always stops at the Import Viewer for visual approval before commit, and supports staging
(hold without committing) as a first-class outcome, not just success/failure.

### 3.3 Bulk legacy migration with triage-and-fix loop

![Legacy migration flowchart]({{artifact:cf06f743-2cdb-4a6f-8108-4057a213421e}})

Batch selection and chunking, per-item classification into clean/warning/error, auto-sort into
Needs Review, and the Migration Viewer triage loop (resolve in-tool and re-run vs. block for
source-system correction) are all explicit, matching the error/warning/diff catalogues in §2.3–2.5.
The batch only commits once every open error is resolved or blocked, and every warning is
explicitly accepted.

## 4. Data model mapping to the platform

This service holds **no piece/style/grade-rule/size-chart data of its own** — those records live
in the Data Management Platform (Azure Database for PostgreSQL metadata + Azure Blob Storage) and are
reached only through its API, per the Integration Model in `suite_architecture.md`. This service's
own database (a small schema in the same Azure Database for PostgreSQL Flexible Server instance, or a dedicated schema/namespace, per
the platform's multi-tenancy convention) holds only interchange-specific bookkeeping:

| Entity | Purpose | Key fields |
|---|---|---|
| `interchange_job` | One IGES export or import operation | `job_id`, `type` (`iges_export`\|`iges_import`), `piece_id` (platform reference), `status`, `params` (JSON), `created_by`, `created_at`, `object_storage_key` (result file) |
| `import_profile` | Saved parameter preset (replaces `IGES.INI`) | `profile_id`, `name`, `trading_partner`, `params` (JSON: closure_amount, trim_tolerance, numbering_scheme, field_extraction map, target_collection, …) |
| `migration_batch` | One bulk-migration run | `batch_id`, `source_system`, `selection` (JSON: pattern/list/connector ref), `status`, `auto_sort_flagged` (bool), `created_by`, `created_at`, `chunk_count` |
| `migration_item` | One style/piece within a batch | `item_id`, `batch_id`, `source_style_ref`, `target_piece_id` (platform reference, null until committed), `status` (`pending`\|`converted`\|`converted_with_warning`\|`error`\|`blocked`\|`resolved`), `needs_review` (bool) |
| `migration_finding` | One error/warning/diff-highlight against an item | `finding_id`, `item_id`, `code` (from §2.3/§2.4 catalogues), `severity` (`error`\|`warning`), `message`, `geometry_ref` (point/line/segment locator within the item), `resolved_at`, `resolved_by` |

**Cross-references into platform-owned data** (read via platform API, never a direct foreign key
into another service's tables):
- `interchange_job.piece_id` → Pattern Design piece record.
- `migration_item.target_piece_id` → the piece record created on successful commit.
- `import_profile.params.target_collection` / `migration_batch` commit target → a platform
  storage-area/collection identifier.
- Grade rule table and size chart references inside `migration_finding.message`/`geometry_ref` are
  platform entity identifiers (grade rule table ID, size chart ID), resolved through the platform's
  grade-rule and size-chart lookup endpoints during the resolution UI flow in §2.6.

All binary artifacts this service produces or consumes — IGES files, migration batch CSV/JSON
reports, staged (not-yet-committed) piece geometry — are written to the same Azure Blob Storage account as every other application, under a service-specific prefix, with the object key recorded on
the owning `interchange_job`/`migration_batch` row for audit-log traceability.

## 5. API surface (FastAPI service: `format-interchange-service`)

```
POST   /pieces/{piece_id}/export/iges          — single-piece export, returns job_id
POST   /export/iges/batch                      — multi-piece export, returns job_id
GET    /export/iges/jobs/{job_id}              — job status + result download URL

POST   /import/iges                            — single-file import, returns job_id
GET    /import/iges/jobs/{job_id}               — job status + Import Viewer payload
GET    /import/iges/jobs/{job_id}/log           — structured conversion log
POST   /import/iges/jobs/{job_id}/commit        — commit a staged import to target_collection

GET    /import-profiles                        — list saved presets
POST   /import-profiles                        — create a preset
PUT    /import-profiles/{profile_id}           — update a preset

POST   /migration/batches                      — create a batch (selection + options)
POST   /migration/batches/{batch_id}/run        — start/resume conversion
GET    /migration/batches/{batch_id}           — status + counts
GET    /migration/batches/{batch_id}/report.csv | .json  — findings export
GET    /migration/batches/{batch_id}/items      — list items, filterable by status
GET    /migration/batches/{batch_id}/items/{item_id}     — item detail incl. findings
POST   /migration/batches/{batch_id}/items/{item_id}/resolve — apply a fix, re-run this item
POST   /migration/batches/{batch_id}/items/{item_id}/block   — mark blocked with a correction note
POST   /migration/batches/{batch_id}/items/{item_id}/accept-warning
POST   /migration/batches/{batch_id}/commit     — commit all resolved/accepted items to the platform
```

All endpoints authenticate via the shared Microsoft Entra ID (Azure AD) layer and enforce RBAC roles
(`interchange:export`, `interchange:import`, `interchange:migrate`, `interchange:review`) at the
API layer, consistent with every other application in the suite.

## 6. Tech stack specifics for this app

- **IGES parsing/writing**: no full CAD kernel is needed — pieces are flat 2D outlines, not solids.
  A purpose-built IGES reader/writer (Python) handling the entity subset in §1.1 (Types 100, 102,
  106, 110, 116, 126, 406) is sufficient and keeps the dependency footprint small; a general CAD
  kernel (e.g. OpenCascade/pythonocc) would be justified only if 3D solid entities are ever added
  to scope, which they are not per the suite architecture.
- **Geometry validation** (self-intersection, closure, angle computation): Shapely, consistent with
  the "computational-geometry libraries as needed" stack note; the same library Pattern Design and
  Marker Making use for outline/nesting validation, so results are consistent across apps.
- **Legacy format parsers**: one parser module per supported source format (proprietary binary,
  DXF/AAMA-ASTM, structured customer export), each normalizing to the same internal piece-geometry
  representation before the shared validation/classification pipeline in §2 runs — new source
  formats are added as new parser modules, not new pipeline logic.
- **Async jobs**: both single-piece conversions and batch migrations run through the platform's
  standard job-queue pattern (this service should not invent its own); large batches chunk into
  sub-jobs per §2.1.
- **Migration Viewer rendering**: same Konva.js/canvas renderer as Pattern Design, reused as a
  package/component rather than reimplemented, so overlay/measure/snap-to-geometry behave
  identically to any other canvas surface in the suite.

## 7. Phased build plan

This app is entirely Phase 3 of the suite roadmap (parallel with Production Output), but Phase 3
work for this app should itself be sequenced as follows:

**Step 1 — Piece Interchange core (single-piece export)**
Build the IGES writer against the entity mapping in §1.1, the export validation gate, and the
`POST /pieces/{piece_id}/export/iges` + job-status endpoints. This is the smallest complete slice
and exercises the platform API read path (fetch piece geometry) without needing any new write path
back to the platform.
*Exit criteria:* a real piece round-trips out of this suite and opens correctly in at least one
external CAD viewer used for validation.

**Step 2 — Piece Interchange import**
Build the IGES reader, the full option set in §1.2 as explicit pipeline stages, Import Profiles
(§1.3), and the Import Viewer (§1.4) with staged-commit support.
*Exit criteria:* an IGES file exported in Step 1 round-trips back in and reproduces the original
piece within trim/closure tolerance; a file from a real external system imports with correct
warnings surfaced for any ambiguous geometry.

**Step 3 — Legacy Migration batch pipeline (classification only)**
Build batch selection/chunking, the per-item conversion pipeline reusing Step 2's geometry-handling
code where the source format allows, and the full error/warning classification catalogue from
§2.3–2.4 — without the Viewer yet. Results report (CSV/JSON) ships here.
*Exit criteria:* a real legacy-format sample batch converts, and every error/warning code in the
catalogue has been produced at least once against real or constructed test fixtures.

**Step 4 — Migration Viewer and triage-and-fix loop**
Build the side-by-side overlay, Measure, Snap-to-Geometry, the diff-highlight catalogue (§2.5), and
the full resolve/block/accept-warning/commit workflow (§2.6, flowchart §3.3).
*Exit criteria:* a batch containing every error type in the catalogue can be fully triaged end to
end — each error either resolved in-tool and re-converted, or correctly marked blocked — and a
clean batch commits to the platform and becomes visible in Pattern Design.

**Step 5 — Hardening for Phase 4**
Load-test batch migration at realistic legacy-library scale (thousands of styles, per Gerber's own
~2,000-style chunking guidance as a floor, not a ceiling), verify audit-log completeness for every
export/import/migration action, and confirm RBAC role enforcement on every endpoint in §5 ahead of
the suite-wide Phase 4 integration and hardening pass.
