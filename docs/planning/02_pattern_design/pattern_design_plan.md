# Pattern Design & Grading — Unified Implementation Plan

*Implementation-ready specification for the **Pattern Design & Grading** application defined in
`suite_architecture.md`. This document merges Gerber PDS2000's documented function set (552
functions/sections) with Richpeace DGS's documented function set (437 functions) into one
de-duplicated implementation catalogue, adds the workflow diagrams, data-model mapping, UI
approach, and phased build plan needed to hand this to an implementation team.*

## 0. Scope recap (from `suite_architecture.md`)

This is the 2D CAD application for creating, editing, and grading pattern pieces: piece creation,
point/line editing, seams, darts/pleats, notches, grain lines, grading, measurement, digitizing
input, and plotting. It is a **thin client** against the Data Management Platform — no local
database, no direct calls to Marker Making or Format Interchange. A piece created here becomes
visible to Marker Making and the Format Interchange utility only through the platform's shared
object storage + PostgreSQL metadata layer. Bulk format translation (DXF/IGES/AAMA-ASTM legacy
migration) is explicitly **out of scope** for this app — that is the Format Interchange & Legacy
Migration Utility's job; this app's import/export surface is limited to native piece open/save
through the platform API and single-piece interchange for interop with Marker Making.

## 1. Languages & Frameworks

This app follows the suite-wide technology matrix exactly. Nothing below is left to be decided at
implementation time.

| Layer | Technology |
|---|---|
| Web frontend | TypeScript + React, built with Vite |
| 2D CAD drawing canvas (piece perimeter, points/lines, seams, darts, grade nest overlay) | Konva.js (HTML5 Canvas/WebGL wrapper) |
| Backend API service (`pattern-design-service`) | Python 3.12+, FastAPI, Pydantic for request/response schema validation |
| Database access / migrations | Python, SQLAlchemy ORM + Alembic, against Azure Database for PostgreSQL Flexible Server (the platform's shared metadata store — this app owns no database of its own) |
| Object storage client (piece geometry files, digitized source images) | Python, `azure-storage-blob` SDK, against Azure Blob Storage (via the platform's storage API — this app does not talk to Blob Storage directly; see §3) |
| Computational geometry (grading transforms, seam-allowance offset curves, dart/pleat geometry, digitized-outline cleanup, DXF piece export) | Python, Shapely + NumPy |
| Backend hosting | Azure Container Apps (the `pattern-design-service` is a stateless FastAPI container; no long-running/CPU-bound compute lives in this app, so Azure Batch/Container Apps Jobs are not needed here — see §6.4 for the one place this could change) |
| Identity / RBAC | Microsoft Entra ID for authentication (OIDC), app-level RBAC enforced in FastAPI middleware against roles supplied by the platform |
| Infrastructure as code | Bicep |
| CI/CD | YAML pipelines, GitHub Actions or Azure DevOps Pipelines |
| Testing | Python: pytest (API + geometry unit tests). TypeScript: Vitest (component/unit), Playwright (end-to-end canvas interaction tests) |

This app has **no CPU-bound long-running compute** of the kind the nesting algorithm requires in
Marker Making — piece creation, editing, and grading-across-a-size-range are all sub-second-to-
low-second operations performed synchronously in the request/response cycle. Grading computation
(applying deltas to a base piece across N sizes) is O(points × sizes), not an optimization solve;
it does not need the async job-queue pattern. §6.4 flags the one scenario (bulk re-grading of an
entire style's piece set in one operation) where adopting the platform's generic job-status/queue
pattern would be the right call if it is ever added.

## 2. Methodology

Source material: `function_definitions_pattern_design.md` (Gerber PDS2000/Silhouette 2000,
552 documented functions/sections) and `richpeace_dgs_functions.md` (Richpeace DGS, 437
documented functions), read against the audited category-depth findings in
`richpeace_vs_gerber_comparison.md`.

Processing pipeline used to build §4's catalogue:
1. Parsed both source manuals into discrete function records (name + description). 531 named
   functions were extracted from Gerber's 21 top-level manual sections (the sections themselves —
   e.g. "Getting Started," "Glossary of Terms" — are overview/orientation text, not invokable
   functions, and are excluded from the catalogue below; 21 such sections + 531 named functions
   reconciles to the manual's own stated count of 552 "functions/sections"). All 437 Richpeace DGS
   entries are named functions (no section-header overhead in that source).
2. Classified every named function into one of the fifteen categories in the task brief (piece
   creation, point/line editing, seams, darts/pleats/fullness, notches/internal markings, grain
   line, grading, measurement, piece transformation, text/annotation, digitizing input,
   import/export, plotting, customization/preferences, automation) via an LLM classification pass,
   with a second pass to force-resolve ambiguous items and a manual pass for the residual handful
   of items that pass could not place. 16 Gerber items (pure overview/hints text with no distinct
   invokable function — e.g. "About Pieces," "Practical Application Examples") were excluded as
   non-functional. This yields 512 real Gerber functions and 437 real Richpeace functions
   classified into the taxonomy — a total of 949 raw named functions.
3. Per category, merged the two vendors' function lists into one de-duplicated table: functions
   describing the same capability under different vendor names collapsed into a single row citing
   both source names; functions unique to one vendor kept as their own row; each row tagged with a
   **Build target** (which vendor's documented depth to implement to, per the audited comparison
   findings) and, where applicable, flagged as a **novel** capability worth keeping even though the
   other vendor has no equivalent.

**Caveat on this document's own classification pass (declared deviation):** the category counts
used to organize §4 come from an independent LLM-based classification of the raw function text,
not from re-running the original audited comparison's classification labels (those per-function
labels were not preserved as an artifact — only the aggregate counts in
`richpeace_vs_gerber_comparison.md` were). The two classification passes agree closely on most
categories (typically within 5–15 items) but are not identical, and a few categories drift more —
notably Gerber piece-creation (34 in this pass vs. 57 documented in the audited comparison; some
piece-creation sub-tools describing point/line operations were classified as point/line editing in
this pass) and Gerber measurement (16 vs. 26 documented). The **depth-target guidance per
category** in §4 is taken directly from the audited comparison document's qualitative findings, not
from this pass's own counts, so which vendor's depth to build to is not affected by this
discrepancy — only the exact bucketing of a handful of borderline functions is. Every merged catalogue
row traces back to a specific named source function from one or both manuals; none are invented.

## 3. Data model: how this app maps onto the Data Management Platform's schema

Per `enterprise_data_architecture.md`, the platform provides Azure Blob Storage for binary
pattern/marker/grading files and Azure Database for PostgreSQL Flexible Server for
metadata/workflow-status/cross-references/audit log, reached only through the platform's own API
— this app has **no direct Blob Storage or Postgres connection of its own**; `pattern-design-
service` calls the platform's API for every read/write, and the platform's API client wraps
`azure-storage-blob` and SQLAlchemy/Alembic-managed tables on the platform's side. The tables below
are grouped by who owns them.

### 3.1 Platform-owned tables (already specified in the Data Management Platform's own plan; consumed here, not redefined here)
- `pieces` — generic piece header: `id`, `name`, `style_id`, `workflow_status` (Draft / Unapproved
  / Approved / Obsolete, mirroring the AccuMark Made/Unmade/Approved status-field pattern),
  `current_version_id`, `created_by`, `created_at`, `updated_at`.
  Pattern Design owns the *content* of a piece; the platform owns the *record* and its lifecycle
  status.
- `styles` — style/model grouping a piece belongs to.
- `object_versions` — Blob Storage key + version for every binary payload (this app's piece
  geometry documents included), content-addressed and immutable per version.
  ↳ Azure Blob Storage soft-delete + versioning is enabled at the container level so a piece
  geometry blob is never overwritten in place — every save creates a new blob version, and
  `pieces.current_version_id` is repointed.
- `cross_references` — link table connecting a piece to the markers that consume it, to its base
  piece (for a graded size), and to its digitized source (if any).
- `audit_log` — every create/update/delete/approve action logged here via the platform API, not by
  this app writing its own log table.
- `users` / `roles` — synced from Microsoft Entra ID; this app checks role claims on the incoming
  request (via the platform's auth middleware) rather than maintaining its own user table.

### 3.2 Pattern-Design-owned tables (this app's own schema in the same Postgres instance, namespaced e.g. `pattern_design.*`, migrated with Alembic)

| Table | Purpose | Key columns |
|---|---|---|
| `piece_geometry_ref` | Points a platform `pieces` row at this app's structured geometry document | `piece_id` (FK to platform `pieces.id`), `blob_version_id` (FK to platform `object_versions.id`), `geometry_schema_version` |
| `grade_rule_tables` | A reusable named grade-rule set (e.g. "Misses Dress Sizes 2–18") | `id`, `name`, `size_range` (ordered list of size labels), `base_size` |
| `grade_rules` | One row per graded point per size-step: the delta that produces that size from the adjacent size | `id`, `grade_rule_table_id`, `point_ref` (identifier into the piece geometry document, not a separate points table — see §3.3), `size_step`, `delta_x`, `delta_y`, `axis_sign_flags` |
| `graded_pieces` | One row per (base piece × size) — the materialized graded outline, itself a `pieces` row referencing a geometry blob, plus grading provenance | `piece_id` (FK to platform `pieces.id`, this size's own piece record), `base_piece_id` (FK to platform `pieces.id`), `grade_rule_table_id`, `size_label` |
| `measurement_charts` | A named spec/measurement chart | `id`, `name`, `piece_id` or `style_id` |
| `measurement_points` | One measured point-to-point spec entry within a chart | `id`, `chart_id`, `label`, `point_ref_a`, `point_ref_b`, `target_value`, `tolerance` |
| `digitized_sources` | Provenance for a piece created via digitizing/camera/scan | `id`, `piece_id`, `source_type` (digitizer_table / camera / scan), `source_image_blob_version_id`, `calibration_scale`, `captured_by`, `captured_at` |
| `piece_templates` | Saved reusable sewing-template / motif definitions (Richpeace's template-reuse feature, §4 Automation) | `id`, `name`, `template_geometry_blob_version_id`, `category` |

### 3.3 The piece geometry document (Blob Storage payload, not a Postgres table)
A single pattern piece's actual CAD content — perimeter, internal lines, points, seam allowances,
darts/pleats, notches, grain line, text annotations — is stored as **one structured JSON document
per piece per version** in Azure Blob Storage, not normalized into per-point/per-line Postgres
rows. This mirrors the platform's own stated design (object storage for the binary/structured
pattern files, Postgres for metadata/cross-references/workflow) and avoids a row-per-point schema
that would not scale to enterprise piece complexity (a single complex piece can carry hundreds of
points). Grade rules and measurement points reference a point by a stable `point_ref` identifier
(a UUID assigned to the point at creation time and preserved across edits) embedded in this
document, not by a Postgres foreign key to a points table — Postgres only needs to store the
*rule*, not the point's coordinates.

Document shape (illustrative, not exhaustive):
```json
{
  "schema_version": 1,
  "units": "mm",
  "perimeter": [{"point_ref": "uuid", "x":  0.0, "y":  0.0, "type": "corner"}, ...],
  "internal_lines": [...],
  "seams": [{"edge_ref": ["uuid","uuid"], "allowance_mm": 10, "corner_type": "2_length_fix"}],
  "darts": [{"leg_a": "uuid", "leg_b": "uuid", "apex": "uuid", "intake_mm": 25}],
  "notches": [{"point_ref": "uuid", "notch_type": "V", "depth_mm": 5}],
  "grain_line": {"start": "uuid", "end": "uuid", "angle_deg": 90},
  "annotations": [{"point_ref": "uuid", "text": "Cut 2"}]
}
```

### 3.4 Async job pattern — not needed for this app's core workflows, but namespaced consistently
Piece creation, editing, and grading-across-a-size-range are synchronous, sub-second-to-low-second
operations (§1) and do not use the platform's async-job queue (Azure Service Bus + Celery workers,
as specified for Marker Making's nesting solver). If a future requirement adds a genuinely
long-running bulk operation to this app — e.g., re-grading every piece in a style's entire piece
set in one batch, or a bulk digitize-and-vectorize pass over hundreds of scanned images — it
should reuse the platform's generic long-running-job table and queue rather than this app
inventing its own: submit to Azure Service Bus, a Celery worker on Azure Container Apps Jobs picks
it up, writes progress/result back through the platform API, and the frontend polls (or receives a
webhook/notification on) the shared job-status entity. No such operation is in this app's Phase-2
scope (§7); this is a forward-compatibility note, not a build item.

## 4. Merged function catalogue

*713 merged, de-duplicated catalogue entries across 15 categories, drawn from 949 raw named
functions (512 real Gerber PDS2000 functions + 437 real Richpeace DGS functions — see §2 for the
extraction/classification methodology). Every row states which vendor's documented depth to build
to, or flags a novel capability unique to one vendor.*

### Piece Creation

This category merges Gerber's 57-deep piece-creation toolset with Richpeace's 21 functions, revealing substantial overlap in core creation methods (rectangle/circle primitives, trace-to-create, mirroring, extraction from enclosed lines) alongside distinct workflow scaffolding unique to each system. Gerber's depth dominates due to its granular breakdown of conic sub-tools (circle/oval by center, tangent, 3-point) and trace variants (Normal/Mirrored/Scored × Sew/Cut), which Richpeace collapses into single commands (CR ARC, Fold out pattern, Forfex) — build target follows Gerber depth for these families while folding in Richpeace's genuinely novel notch/interlining/geometric-shape tools. A few Richpeace functions (Make Interlining, Parallel quadrangle, Trapezia, Count and gap, Continue) have no Gerber equivalent and are preserved as novel additions.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Place Pieces into Work Area | Gerber: Placing Pieces into the Work Area | Novel — Gerber | Select one or more piece icons from the piece menu (click, shift-range, ctrl-multi, or drag) and click/drop into the main work area to begin editing. |
| Add/Delete Standard Piece & Descriptions | Gerber: Adding or Deleting Pieces and Descriptions | Novel — Gerber | On the Piece Description page, add a named standard piece with a material group or delete an existing piece, plus attach/remove free-text descriptions per piece. |
| Redo | Gerber: Redo | Novel — Gerber | Re-applies the last undone action, restoring state to before the Undo; standard linear redo stack. |
| Set Selected / Current Piece | Gerber: Set Selected · Gerber: Current Pieces | Novel — Gerber | Designate one or multiple pieces as "current/active" so subsequent commands and clicks target only those, avoiding mis-selection on overlapping pieces. |
| Add Pieces to Model | Gerber: Add Pieces | Novel — Gerber | Create a new named model (piece group) or append additional pieces to an existing active model, validated against current storage-area/model context. |
| Create Lines (menu) | Gerber: Create Lines | Novel — Gerber | Top-level menu grouping tools for drawing straight, curved, offset, copied, or mirrored construction/design lines on a piece. |
| Circle by 2 Points + Center | Gerber: Conics - Circle 2 Pt Center | Gerber depth | Click two points on the circle's circumference, then drag/type to place the approximate center; system computes and draws the circle. |
| Circle by 3 Points | Gerber: Conics - Circle 3 Pt | Gerber depth | Click three points the circle must pass through; system auto-fits the circle and marks the center with a drill hole or draft point. |
| Circle Tangent to 1 Line | Gerber: Conics - Circle Tang 1 Line | Gerber depth | Pick a tangent point on one line, then drag/type a radius to draw a circle tangent to that single line — used for rounding a point. |
| Circle Tangent to 2 Lines | Gerber: Conics - Circle Tang 2 Line | Gerber depth | Select two lines meeting at a corner, then drag/type a radius to fit a circle tangent to both, rounding the corner. |
| CR ARC / Circle by Center + Length | Richpeace: CR ARC | Both (union) | Click a center point, then enter an arc length (or shift-toggle to three-point circle/arc mode) to draw an arc or circle as a design/assistant line. |
| Oval by Orientation (Center + Axes) | Gerber: Conics - Oval Orient | Gerber depth | Pick a center point, set the short axis length and tilt angle, then set the long axis length to draw an oriented oval. |
| Oval by Focus Point | Gerber: Conics - Oval Focus | Gerber depth | Pick a center point and a focus point (sets long-axis direction), then enter the long-axis length to draw the oval. |
| Circle/Oval Creation Overview | Gerber: Creating Circles and Ovals | Gerber depth | Reference/overview grouping of all circle and oval creation methods (center+size, 2/3-point, tangent, edge-conversion). |
| Create Piece (menu/section overview) | Gerber: Create Pieces · Gerber: Creating Pieces | Gerber depth | Top-level menu/section for building brand-new pieces from scratch (typed measurements or drawn shapes) or derived from existing pieces; enforces unique piece naming. |
| Create Piece – Rectangle | Gerber: Create Piece - Rectangle · Richpeace: Rectangle · Richpeace: Make pattern (rectangle option) | Both (union) | Draw a rectangular piece/design line by cursor drag or typed length/width values; supports both full new-piece creation and rectangle-as-assistant-line use inside a pattern. |
| Create Piece – Circle | Gerber: Create Piece - Circle · Richpeace: Make pattern (circle option) | Both (union) | Create a circular pattern piece by dragging or entering exact radius/circumference, with optional center-point marking; can generate as a real separate piece. |
| Create Piece – Skirt | Gerber: Create Piece - Skirt | Novel — Gerber | Auto-generate a quarter-circle skirt piece from typed waist and length measurements, including boundary and grain/grade line, no manual drawing required. |
| Create Piece – Oval | Gerber: Create Piece - Oval | Gerber depth | Generate an oval piece from typed horizontal/vertical dimensions, auto-adding outline and grain/grade line, with optional center marking. |
| Create Piece – Collar | Gerber: Create Piece - Collar | Novel — Gerber | Auto-draft a basic collar from typed measurements (width, center-back-to-shoulder, shoulder-to-center-front), with optional notch placement. |
| Create Piece – Facing | Gerber: Create Piece - Facing | Novel — Gerber | Generate a facing piece automatically from a selected existing edge line (e.g., neckline/armhole), optionally including seam allowance, instead of manual tracing. |
| Create Piece – Copy | Gerber: Create Piece - Copy | Novel — Gerber | Duplicate an existing piece exactly, including internal lines (darts, markings), and drag the copy to a new location, preserving the original untouched. |
| Extract Piece from Enclosed Area | Gerber: -Create Piece - Extract Piece · Richpeace: Forfex | Both (union) | Mark off a sub-area within an existing piece using drawn design/assistant lines (or shift-click to fill enclosed regions), then auto-generate a new piece from that enclosed outline. |
| Trace Pieces (menu/overview) | Gerber: Trace Pieces · Gerber: Tracing to Create Pieces | Gerber depth | Menu/instructional grouping for all trace commands that build new pieces by selecting and combining lines from existing pieces, generally in clockwise order. |
| Trace Normal – Sew Outline | Gerber: Create Piece - Trace Normal - Sew | Gerber depth | Select and combine lines from one or more existing pieces (clockwise) to build a new piece whose outline is the sew line (excludes seam allowance). |
| Trace Normal – Cut Outline | Gerber: Create Piece - Trace Normal - Cut | Gerber depth | Same as Trace Normal but the resulting outline is the cut line, including seam allowance. |
| Trace Mirrored – Sew Outline | Gerber: Create Piece - Trace Mirrored - Sew · Richpeace: Fold out pattern | Both (union) | Select a mirror/center line, then trace and combine lines from existing piece(s), flipping across the mirror line to build a symmetrical new piece with a sew-line outline. |
| Trace Mirrored – Cut Outline | Gerber: Create Piece - Trace Mirrored - Cut | Gerber depth | Same as Trace Mirrored – Sew but the resulting mirrored outline is the cut line, including seam allowance. |
| Trace Scored – Sew Outline | Gerber: Create Piece - Trace Scored - Sew | Gerber depth | Select a fold (score) line and unfold part of an existing piece across it to build a non-symmetrical piece (e.g., turnback hem) with a sew-line outline. |
| Trace Scored – Cut Outline | Gerber: Create Piece - Trace Scored - Cut | Gerber depth | Same as Trace Scored – Sew but the resulting outline is the cut line, including seam allowance. |
| Split Piece Along Line | Gerber: Creating Pieces using Split Lines | Novel — Gerber | Divide a piece along a line via existing internal line, digitized new line, two-point connection, or horizontal/vertical/diagonal cut from a point — used to break one piece into two. |
| Finalize Draft into Working Piece | Gerber: Create Piece · Gerber: Create Draft Pieces and Save Working Pieces | Gerber depth | Convert a rough sketched draft into a valid piece by closing the perimeter and adding a grain/grade reference line, then save it as a stored working piece. |
| Draft Trace (Selective Perimeter Trace) | Gerber: Draft Trace | Gerber depth | Build a valid piece from a sketch by selectively picking only the lines that form the outer edge (clockwise from lower-left), ignoring extraneous sketch lines. |
| Trim/Extend Piece (Kerf) | Gerber: Trim/Extend Piece | Novel — Gerber | Removes a thin sliver equal to half the trace-pen tip width from a piece's edge after Create Piece/Draft Trace, correcting for digitizing pen thickness. |
| Add Design Line to Pattern | Richpeace: Creat design line to pattern | Novel — Richpeace | Click a pattern to add a new design line directly onto it, with an option to apply the same design line to all patterns simultaneously. |
| Inside Border / Cut-out Shape | Richpeace: Inside border | Novel — Richpeace | Create a hollow cut-out inside a pattern by selecting the pattern outline plus an inside border line, or by enclosing an area with assistant lines, then confirming to punch the hole. |
| Make Interlining | Richpeace: Make Interlining | Novel — Richpeace | Generate interlining pieces from a pattern: add an equal-width interlining strip along selected border/slope lines, or apply interlining to the entire pattern boundary. |
| Parallel Quadrangle Shape | Richpeace: Parallel quadrangle | Novel — Richpeace | Draw a parallelogram-shaped piece (e.g., for bags/toys) by clicking placement, then entering dimension values in a dialog to finalize. |
| Trapezoid Shape | Richpeace: Trapezia | Novel — Richpeace | Draw a trapezoid-shaped piece (e.g., for bags/toys) by clicking placement, then entering dimension values in a dialog to finalize. |
| Continue Adding Elements to Returned Pattern | Richpeace: Continue | Novel — Richpeace | Reopen a pattern already returned to the packing list so additional elements (notches, assistant lines) can continue to be read/added into it. |
| Set Notch Count and Gap | Richpeace: Count and gap | Novel — Richpeace | Configure a distinct notch number and the spacing gap between multiple notches placed on a piece edge. |



### Point / Line Editing

**Part 1 of 2:**

Both manuals were scanned for overlapping point/line editing capabilities. Gerber's list dominates this part with fine-grained point/line modification, selection, and view/verification tools, so most rows build to Gerber depth. Richpeace contributes several genuinely novel geometric-construction tools (angle bisector, arc corner, ARC cutline, equidistant/parallel curve variants, compasses, fix length, corner connection, etc.) not represented in this Gerber excerpt, which are retained as Novel — Richpeace; one clear conceptual overlap (Corner vs. Gerber's line-intersection style editing, and Delete Line/Eraser) is merged where the capability is truly equivalent.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Select and move points/lines/pieces | Gerber: Select and Move Points, Lines, and Pieces (incl. duplicate listing) | Gerber depth | Click-drag any point, line, or whole piece to reposition it in the work area; base interaction for all editing. |
| Multi-select points/lines/pieces | Gerber: Selecting Multiple Points, Lines, or Pieces | Gerber depth | Supports sequential click, click-inside-piece for whole outline, Shift range select, Ctrl discontiguous select, and marquee drag box. |
| Range selection via thumbtacks | Gerber: Selecting a Range with Thumbtacks | Gerber depth | Two draggable end markers define a variable-length span of points on a line for range-limited commands (e.g., Move Range); lock in with a click. |
| Cross-line/piece point selection via cursor proximity + arrow keys | Gerber: Selecting Points/Locations on Multiple Lines/Pieces | Gerber depth | Highlights all points on the nearby line; holding mouse button and pressing arrow keys jumps selection across lines/pieces (left/right = around edge, up/down = across pieces). |
| Line context options menu | Gerber: Options for Lines | Gerber depth | Right-click menu offering precision options for selecting/handling lines during active commands. |
| Work-area context options menu | Gerber: Using Options Pop-up Menu for Work Area Tasks | Gerber depth | Right-click in blank canvas (no active tool) for Undo/Redo, Edit Piece/Line/Point Info dialogs, and sending pieces to the Piece/Icon menu. |
| Select All | Gerber: Select All | Gerber depth | Ctrl+A selects every point/line/detail of the active type in one action, e.g. for bulk grade-rule assignment. |
| Clear/deselect all | Gerber: Clear All | Gerber depth | Ctrl+D (or right-click) instantly deselects all current selections to allow a fresh pick. |
| Edit point/line/piece info (category) | Gerber: Edit Point, Line, and Piece Info | Gerber depth | Menu grouping for commands that edit stored attributes of points, lines, and pieces (numbers, grade rules, line types, seam, names). |
| Edit point info | Gerber: Edit Point Info | Gerber depth | Modify a point's notch type, grade rule, or point number; navigate points via Track or auto-tracking. |
| Live point info tooltip | Gerber: Showing Point Info | Gerber depth | While in Edit Point Info, dragging along a line pops up a live-updating box showing attribute, type, ID, and grade rule of the nearest point (toggle in Preferences). |
| Edit line info | Gerber: Edit Line Info | Gerber depth | Change a line's type, label, or seam allowance by tracking to it and editing fields directly. |
| View point ID numbers | Gerber: Point - Point Numbers | Gerber depth | Displays each point's assigned ID number on selected pieces for reference before editing. |
| View point types/attributes | Gerber: Point - Point Types/Attributes; Point Types and Modifiers | Gerber depth | Displays Point Modifiers/Attributes (grading, cutting, shaping settings) for one point or all points on a piece, and lets values be adjusted from the same view. |
| Point attribute settings | Gerber: Attributes | Gerber depth | Underlying settings (Turn, Curve, X-free, Alternate Start, Curve Length Reference, Lift and Plunge, Grade Like Intersection, etc.) controlling grading/plotting/cutting behavior per point. |
| View line numbers | Gerber: Line - Numbers | Gerber depth | Displays identifying numbers of lines on selected pieces (F5 shortcut) for reference during editing. |
| View line names | Gerber: Line - Names | Gerber depth | Shows up to 10-character alphanumeric names already assigned to lines. |
| View line types/labels | Gerber: Line - Types/Labels | Gerber depth | Displays each line's type/label (AccuMark "line labels" vs. MicroMark "types and labels") prior to editing. |
| Line type/label reference list | Gerber: Line Modifiers - Types and Labels | Gerber depth | Standard catalogue of MicroMark line type/label names (Style, Draft, Stripe/Plaid, etc.) defining each line's purpose. |
| Verify line by label | Gerber: Line - Verify by Label | Gerber depth | Highlights only internal lines matching a typed label value, for locating a specific line on a busy piece. |
| Hide/ignore lines (category) | Gerber: Hide/Ignore Lines | Gerber depth | Grouping of commands to temporarily hide perimeter/internal/cut/sew lines from view without deleting data, plus name/label checks. |
| Hide/ignore perimeter lines | Gerber: Line - Hide/Ignore Perimeter | Gerber depth | Temporarily removes selected outer boundary lines from screen display without deleting underlying data. |
| Hide/ignore internal lines | Gerber: Line - Hide/Ignore Internal | Gerber depth | Temporarily removes selected internal lines (darts, notches, seam details) from view to reduce clutter. |
| Reset hidden lines | Gerber: Line - Hide/Ignore Reset | Gerber depth | Restores all previously hidden perimeter/internal lines on selected piece(s) back to visible. |
| Add point / drill point | Gerber: Add Point | Gerber depth | Places a new point onto an existing line or a drill point inside a piece, via on-screen click (Cursor mode) or exact coordinate entry. |
| Add multiple points | Gerber: Adding Multiple Points | Gerber depth | Places several points/drills at once, spaced either proportionally across a line/area or at a fixed distance (e.g., buttonholes, trim marks). |
| Modify points (category) | Gerber: Modifying Points; Modify Points | Gerber depth | Grouping of commands to change existing points — adjusting notch angle, aligning points, or repositioning — via several constrained move modes. |
| Point intersect | Gerber: Point Intersect | Gerber depth | Marks the actual or extended crossing point of two lines; if off-line, creates a drill hole instead of a regular point. |
| Delete point | Gerber: Delete Point | Gerber depth | Removes an intermediate/notch/grading point from a line and auto-redraws the line smoothly; cannot delete true endpoints. |
| Reduce points | Gerber: Reduce Points | Gerber depth | Auto-removes unnecessary points along a line based on a 0–5 Reduce Factor, with option to smooth or keep sharp corners. |
| Align two points | Gerber: Modify Points - Align 2 Points | Gerber depth | Moves a selected point to align exactly horizontally or vertically with a chosen reference point (e.g., matching drill holes or notches). |
| Moving points overview | Gerber: Moving Points | Gerber depth | Overview of constrained point-move commands (X, Y, both, or along-line) applicable to perimeter, internal, extension, or standalone points. |
| Move point (non-smoothing) | Gerber: Modify Points - Move Point | Gerber depth | Shifts one or more points in X/Y without smoothing neighboring geometry — only the local area at the point changes. |
| Move point along line/slide | Gerber: Modify Points - Move Pt Line/Slide | Gerber depth | Slides a graded point, notch, or intermediate point along its line's direction (or a virtual extension) without adding/removing points. |
| Move point horizontal | Gerber: Modify Points - Move Point Horiz | Gerber depth | Constrains point movement to the X axis only (e.g., dropping an armhole along a side seam), by drag or exact value. |
| Move point vertical | Gerber: Modify Points - Move Point Vert | Gerber depth | Constrains point movement to the Y axis only, by drag or exact signed value entry. |
| Move point smooth | Gerber: Modify Points - Move Smooth | Gerber depth | Moves a point in any direction while auto-curving the surrounding line/range to preserve a natural shape. |
| Move smooth along line | Gerber: Modify Points - Move Smooth Line | Gerber depth | Moves a point smoothly along a line or its extension, reshaping the full line or a thumbtack-selected range into a new curve. |
| Move smooth horizontal | Gerber: Modify Points - Move Smooth Horiz | Gerber depth | Moves a point/thumbtack range smoothly along X only, reshaping curvature (e.g., adding fullness). |
| Move smooth vertical | Gerber: Modify Points - Move Smooth Vert | Gerber depth | Moves a point/range smoothly along Y only, reshaping curvature for height/fullness adjustments. |
| Verify points (view-only overview) | Gerber: Verifying Points | Gerber depth | Overview of non-destructive point-checking view commands: all points, intermediate points, sequential numbers, grade rule numbers, notch types, attributes. |
| Line menu overview | Gerber: Overview of Line Menu | Gerber depth | Describes the Line menu's scope: create, modify, add, delete, move perimeter and internal lines; references Create Line, Perp Line, Conics, Modify Line submenus. |
| Delete line | Gerber: Delete Line; Richpeace: Eraser (line-deletion use), Delete Stitching Line | Both (union) | Removes a selected perimeter or internal line (or stitching line) from the piece; Richpeace's eraser variant also deletes points/notches/buttonholes/darts in one tool, and stitching-line deletion has a dedicated blank-type toggle. |
| Replace line | Gerber: Replace Line | Gerber depth | Swaps an existing style line for a newly drawn one, replacing shape/position while keeping it part of the piece. |
| Swap line | Gerber: Swap Line | Gerber depth | Exchanges a drawn line (e.g., curve/offset) into the piece boundary/design in place of another line. |
| Extend-to-intersection corner trim | Gerber: (line intersection behavior within Point Intersect) · Richpeace: Corner; Corner connection | Novel — Richpeace | Extends two lines to their crossing point and trims the unwanted protruding segments beyond it, keeping the selected branch — a direct trim-to-corner tool Gerber's set does not expose as a standalone command. |
| Draw freehand line/curve | Richpeace: Draw line; Curve | Novel — Richpeace | Freeform tool to draw straight lines (via two points + length/angle dialog) or multi-point curves, with in-line switching to horizontal/vertical/45°/free-direction modes. |
| Draw line at specified angle/length | Richpeace: Draw line with Angel | Novel — Richpeace | Creates a line at an explicit angle and length, with an "opposite direction" option dispersing the angle 360° from the base heading. |
| Angle line construction | Richpeace: Angel line | Novel — Richpeace | Constructs vertical, tangent, or parallel lines through a point on or off a reference line, toggling reference orientation with Shift. |
| Angle bisector | Richpeace: Angel Bisector | Novel — Richpeace | Divides a selected angle/corner into N equal segments, with configurable bisector length, usable on draft lines or finished patterns. |
| Arc corner (rounding) | Richpeace: Arc Corner | Novel — Richpeace | Rounds the junction of two lines with an equal- or non-equal-distance arc, with options to preserve/delete the original corner point. |
| Arc cut line between unparallel lines | Richpeace: ARC cutline | Novel — Richpeace | Generates a tangent/radius curve connecting two non-parallel lines by inputting a single curvature value. |
| Arc spread (localized curvature injection) | Richpeace: ARC spread | Novel — Richpeace | Applies an arc-shaped deformation to a chosen line/area relative to a fixed reference point and an input value, usable on draft lines, patterns, or blank space. |
| Auto-smooth on move/rotate adjust | Richpeace: Auto smooth | Novel — Richpeace | Option that automatically smooths a line after a move/rotate adjustment instead of requiring manual point cleanup. |
| Change border segment (line swap between pieces) | Richpeace: Change border segment | Novel — Richpeace | Interchanges a design/assistant line with a pattern border line, or replaces one pattern's border with another's, with horizontal/vertical flip option. |
| Convert border to assistant curve (merge outlines) | Richpeace: Change border to assistant curve | Novel — Richpeace | Converts one pattern's border into a closed assistant line matching key points of another pattern, merging two outlines into one assistant line. |
| Clear all assistant curves on pattern | Richpeace: Clear all assist curve in pattern | Novel — Richpeace | Bulk-deletes all assistant/auxiliary curves on a selected pattern (or all patterns) in one operation. |
| Clear pending pattern edits | Richpeace: Clear select pattern | Novel — Richpeace | Reverts a pattern being modified back to its pre-edit state and returns it to the pattern list without deleting it from the saved version. |
| Closed assistant line tool | Richpeace: Closed Assistant Line | Novel — Richpeace | Adds a closed-loop internal assistant line to a pattern by reading the border and entering points sequentially, finished with a completion key. |
| Compasses (fixed-length construction lines) | Richpeace: Compasses; Double compasses | Novel — Richpeace | Single-compass mode draws a fixed-length line from a key point to a line (e.g., bias lines at armhole/shoulder); double-compass mode draws two fixed-length lines from two reference points simultaneously. |
| Curve length/straightness adjust | Richpeace: Curve adjust; Fix length | Novel — Richpeace | Checks/edits a curve's length or straightness relative to its chord, offsets a side point, or fixes total curve length while reshaping via a moved control point. |
| Disjoin border and assistant curve grading link | Richpeace: Disjoin border and assist curve | Novel — Richpeace | Breaks the grading linkage between a border line and its assistant line so grading one no longer affects the other. |
| Divider (equal/equal-distance point placement) | Richpeace: Divider | Novel — Richpeace | Adds evenly spaced points along a line, or mirrored equal-distance points in opposite directions, with toggles for point spacing mode. |
| Equidistant (parallel offset) curve | Richpeace: Equidistance curve; Add/replace unparallel curve | Novel — Richpeace | Draws a new line at a specified parallel offset from an existing line, or reshapes an existing unparallel line by an incremental distance value. |
| Equidistant curve intersecting two curves | Richpeace: Equidistance curve intersect with two curve | Novel — Richpeace | Generates one or more offset curves from a source line constrained to intersect two other selected curves in a single operation. |
| Guide line parallel to two points | Richpeace: Guide line parrallel | Novel — Richpeace | Builds a dashed reference guide line parallel to a line through two selected points, with Ctrl-click distance copy for placement marking. |
| Auto seam allowance on pattern creation | Richpeace: Add seam val auto | Novel — Richpeace | Automatically applies a default (adjustable, e.g. 10mm) seam allowance to every new pattern piece as it's created. |
| Princess-line perpendicular cut-corner | Richpeace: 2 vertical length | Novel — Richpeace | Specialized cut-corner construction that extends one border to intersect another, then drops a perpendicular through the intersection — used for princess-seam armholes. |
| Sewing template creation setup | Richpeace: Create sewing template | Novel — Richpeace | Dialog defining blank width (pattern-to-screen distance) and radius (cut area) for generating a physical plastic sewing template. |
| Plotter selection setting | Richpeace: Current plotter | Novel — Richpeace | Output-device setup option selecting the active plotter model from a pull-down list. |

**Part 2 of 2:**

This category merges Gerber's deep line/point manipulation toolset (extension, tangent, perpendicular, conics, modify-line operations) with Richpeace's DGS tool set, which covers much of the same ground with different naming plus several genuinely novel additions (Intelligent Pen multi-modal tool, relevant/irrelevant crossing-line linkage, symmetry adjust, sleeve/armhole notch automation, assist-line output typing). Per the depth guidance, the catalogue is built to Gerber's granularity for core line creation/modification/tangent/perpendicular/conic operations, with Richpeace capabilities folded in only where they add something Gerber's list doesn't already cover.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Unclipped Perimeter (line extension) | Gerber: Unclipped Perimeter | Novel — Gerber | Allows a perimeter line to extend past its corner intersection point instead of being auto-trimmed, for grading setups requiring extra geometry. |
| Clipped Perimeter (trim extension) | Gerber: Clipped Perimeter | Novel — Gerber | Pulls an overhanging perimeter line back to its true intersection point, restoring a clean corner. |
| Create Line - Digitized (freehand trace) | Gerber: Create Line - Digitized | Gerber depth | Draws a straight/curved internal line by clicking a sequence of points, creating a default-type internal line attached to the piece. |
| Create Line - Curved | Gerber: Create Line - Curved | Gerber depth | Draws a curved internal line on a piece via interactive point entry (basic curve-drawing tool). |
| Create Line - 2 Point | Gerber: Create Line - 2 Point | Gerber depth | Draws a straight internal line instantly between two clicked points, which may lie on the same or different pieces. |
| Create Line - Offset Even | Gerber: Create Line - Offset Even | Gerber depth | Generates a parallel copy of an edge/internal line at a uniform offset distance, e.g. for facings. |
| Create Line - Offset Uneven | Gerber: Create Line - Offset Uneven | Gerber depth | Generates a copy of a line offset by varying distances along its length, for uneven reshaping of curves. |
| Create Line - Copy Line | Gerber: Create Line - Copy Line | Gerber depth | Duplicates selected line(s) preserving exact shape/length and places the copy on the same or another piece. |
| Create Line - Mirror | Gerber: Create Line - Mirror | Gerber depth | Creates a flipped mirror-image copy of a line about a chosen axis line, for symmetric feature duplication. |
| Create Line - Create Blend | Gerber: Create Line - Create Blend | Gerber depth | Draws a new internal line that pivots from a near-endpoint blend point to smoothly merge into an existing line. |
| Hide/Ignore Lines (view visibility & labels) | Gerber: Hide/Ignore Lines | Gerber depth | Toggles visibility of line types (perimeter, internal, cut, sew) by view layer and allows inspection/edit of line names/labels, without deleting data. |
| Hide Assistant Line | Richpeace: Hide part assistant line | Novel — Richpeace | Hides selected construction/assistant lines via marquee selection (Shift+U) to declutter grading views, independent of the general line-visibility toggle. |
| Moving Lines (menu category) | Gerber: Moving Lines | Gerber depth | Umbrella category grouping all line-repositioning tools (perimeter, internal, grain/grade, annotation, style) — implemented as a menu grouping, not a standalone op. |
| Internal Line Labels | Gerber: Internal Line Labels | Gerber depth | Assigns letter codes (A, D, G, I, etc.) that classify internal line function/type for downstream system logic, some auto-assigned. |
| Set Curve Color/Type & Output Type | Richpeace: Set curve color and type · Richpeace: Set curve colour and type · Richpeace: Set assist curve output type · Richpeace: Set curve shape | Novel — Richpeace | Sets line rendering (color, solid/dashed/pattern, width/height) and cut/plot output classification (whole-knife, half-knife, cutting vs plotting) for design/assist lines — a display+manufacturing-output tagging capability beyond Gerber's naming-only labels. |
| Tangent Lines (menu category) | Gerber: Tangent Lines · Gerber: Creating Tangent Lines | Gerber depth | Umbrella/help grouping and selector for the tangent-line tool family (on-line, off-line, 2-circle tangents). |
| Create Line - Tangent On Line | Gerber: Create Line - Tangent On Line | Gerber depth | Draws a straight line tangent to a chosen point on a curve, extending to a typed/dragged length. |
| Create Line - Tangent Off Line | Gerber: Create Line - Tangent Off Line | Gerber depth | Draws a line tangent to one point on a curve that terminates at a separately chosen second point. |
| Create Line - Tangent 2 Circ | Gerber: Create Line - Tangent 2 Circ · Richpeace: Tagent line of ARC | Both (union) | Draws a straight line tangent to two circles (or a point-to-circle tangent), touch points selected interactively on each circle. |
| Perpendicular Lines (menu category) | Gerber: Perpendicular Lines · Gerber: Creating Perpendicular Lines | Gerber depth | Umbrella/help grouping and selector for the perpendicular-line tool family (on-line, off-line, 2-point). |
| Perp Line - Perp On Line | Gerber: Perp Line - Perp On Line | Gerber depth | Draws a line perpendicular to a chosen point on an existing line, with Half/Whole extension-side control. |
| Perp Line - Perp Off Line | Gerber: Perp Line - Perp Off Line | Gerber depth | Draws a line crossing a perimeter edge at 90° at a chosen point, with Half/Whole extension-side control. |
| Perp Line - Perp 2 Points | Gerber: Perp Line - Perp 2 Points | Gerber depth | Draws a perpendicular line at the midpoint between two picked points on the same line, with Half/Whole extension control. |
| Horizontal/Vertical Line Creation | Richpeace: Horizontal line · Richpeace: Horizontal or vertical line · Richpeace: Horz or vert line | Novel — Richpeace | Draws a strictly horizontal or vertical line between clicked points (with right-click toggling orientation), a dedicated axis-aligned line tool Gerber's set lacks. |
| Horizontal/Vertical Adjust | Richpeace: Horz/vertical adjust | Novel — Richpeace | Snaps an existing line (and its connected pattern edge) to horizontal or vertical orientation, for cleaning up digitized input. |
| Conics (menu category) | Gerber: Conics | Gerber depth | Umbrella grouping for circle/curve (conic) creation tools — center holes, rounded corners, tangent circles. |
| Conics - Circle Ctr Rad | Gerber: Conics - Circle Ctr Rad | Gerber depth | Creates a circle from a center point plus radius/circumference input, as a standalone piece or internal line. |
| Conics - Circle Ctr Cirm | Gerber: Conics - Circle Ctr Cirm | Gerber depth | Creates a circle from a center point sized primarily by circumference input, as a standalone piece or internal line. |
| Conics - Curved Intersection (corner rounding) | Gerber: Conics - Curved Intersection | Gerber depth | Replaces a sharp corner between two edge lines with a smooth curve of a specified radius, trimming back the originals. |
| Modify Lines (menu category) | Gerber: Modify Lines | Gerber depth | Umbrella category for line-editing operations (move, rotate, smooth, split, merge, etc.) — a menu grouping, not a standalone op. |
| Modify Line - Move Offset | Gerber: Modify Line - Move Offset | Gerber depth | Slides an edge/internal line parallel to its original position; adjacent edges auto-stretch to reconnect. |
| Modify Line - Move Line | Gerber: Modify Line - Move Line | Gerber depth | Moves a line freely in any direction using a reference point for exact distance/direction control. |
| Modify Line - Move Line Anchor | Gerber: Modify Line - Move Line Anchor | Gerber depth | Moves a line to a new position keeping its length fixed, blending into neighboring lines via reference point or "Bump to Line" rotation. |
| Modify Line - Move Range | Gerber: Modify Line - Move Range | Gerber depth | Moves a single point on a line while auto-smoothing neighboring points/curvature to avoid kinks. |
| Modify Line - Make Move Parallel | Gerber: Modify Line - Make Move Parallel | Gerber depth | Moves and re-orients a line to be parallel to another line or to X/Y axis in one combined operation. |
| Modify Line - Make Parallel | Gerber: Modify Line - Make Parallel | Gerber depth | Rotates a line in place to become parallel to another line or the X/Y axis without relocating it. |
| Modify Line - Rotate Line | Gerber: Modify Line - Rotate Line | Gerber depth | Rotates a line about a fixed pivot point via typed angle or dragged distance, e.g. for bias grain lines. |
| Modify Line - Move and Rotate | Gerber: Modify Line - Move and Rotate | Both (union) | Simultaneously translates and rotates a line via drag or typed angle/distance, with optional opposite-direction motion of adjacent edges. |
| Modify Line - Set and Rotate | Gerber: Modify Line - Set and Rotate | Gerber depth | Moves and pivots an internal line to align through a specific point on another (possibly cross-piece) line, keeping the target line fixed. |
| Modify Line - Reshape Line | Gerber: Modify Line - Reshape Line | Novel — Gerber | Intended to alter the shape/curvature of an existing line (feature under construction in source manual; retained as a placeholder capability). |
| Modify Line - Adjust Length | Gerber: Modify Line - Adjust Length | Gerber depth | Changes a line's interior shape while holding both endpoints fixed (currently behaves as Move Smooth Line). |
| Modify Line / Darts - Smooth | Gerber: Modify Line - Smooth · Gerber: Darts - Smooth Line | Gerber depth | Repositions intermediate points along a line (endpoints fixed) to remove digitizing bumps, with draggable markers to bound the smoothed section, including near notches. |
| Modify Line - Merge | Gerber: Modify Line - Merge | Gerber depth | Joins two or more selected lines (edges or non-touching internals) into one continuous line, removing the shared endpoint. |
| Modify Line - Split (Snip) | Gerber: Modify Line - Split · Richpeace: Snip (connect) line · Richpeace: Snip curve | Both (union) | Cuts one line into two-plus segments at a chosen or typed point, or the reverse operation connecting lines back together, with support for group-cut against a reference line. |
| Modify Line - Clip | Gerber: Modify Line - Clip | Gerber depth | Trims the portion of an internal line extending past the piece's perimeter, keeping the segment the user selects. |
| Modify Line - Open Line | Gerber: Modify Line - Open Line | Gerber depth | Marks an internal line on a mirrored piece so it is excluded from the mirrored copy (e.g. one-sided drill holes). |
| Modify Line - Flatten Line Segment | Gerber: Modify Line - Flatten Line Segment | Both (union) | Removes redundant in-between points to simplify a line, with options to preserve notches and dart points. |
| Point Clean Up | Richpeace: Point clean up | Both (union) | Automatically deletes superfluous redundant points from a pattern's lines in a single command, without manual marker selection. |
| Darts - Fold/Close Dart End | Gerber: Darts - Fold/Close Dart End | Gerber depth | Converts an edge-cut dart into a folded internal dart, adjusting the outer edge, with optional fold lines, drill hole, and notches. |
| Point Filter (digitizing pen smoothing) | Gerber: Point Filter | Gerber depth | Controls how many extra points are retained/removed from a hand-drawn line after pen-lift, based on a threshold value. |
| Trim/Extend Line | Gerber: Trim/Extend Line · Richpeace: One way extend · Richpeace: Two way extend | Both (union) | Shortens or lengthens a line along its existing direction to meet one (one-way) or two (two-way) target lines, or trims it, with auto-detection of the nearest intersection. |
| Create Line - Parallel Design (dialog offset) | Richpeace: Parallel Design | Novel — Richpeace | Creates a parallel line at a numerically-entered offset distance via a dedicated dialog box, distinct from drag-based offset creation. |
| Modify Line - Parallel Modify | Richpeace: Parallel modify | Novel — Richpeace | Adjusts one or more selected points via an offset-value dialog to parallel-shift a line, with axis/45°-constrained dragging via Shift. |
| Modify - Curve/Control Point Editor | Richpeace: Modify | Novel — Richpeace | Combined tool for reshaping curves, adding/removing control points, converting curve↔turn point type, and editing drill/buttonhole/pleat/dart properties via right-click, exposed as one multi-mode editor. |
| Resmooth Curve (overlay redraw) | Richpeace: Resmooth curve | Both (union) | Redraws/smooths a curve while pinning original key/grading points, by overlaying a new curve attached at chosen control points. |
| Move / Copy (points or lines, with mirror) | Richpeace: Move · Richpeace: Move (copy) | Gerber depth | Moves or copies a selected set of points/lines to a target position via reference point and drag, with toggles for copy-vs-move and horizontal/vertical mirroring. |
| Offset Point/Line (quick offset) | Richpeace: Offset point/offset line | Gerber depth | Creates an offset copy of a single point or line via a quick key-point-and-Enter shortcut, with toggle to keep or discard the original. |
| Non Cross Isometry Line | Richpeace: Non Cross isometry line | Novel — Richpeace | Creates an equal-distance (isometric) derived line from a dragged line without crossing another line — a specialized offset variant for non-intersecting geometry. |
| Non-grading Point on One Line | Richpeace: Non-grading Point on One Line (Key A) | Novel — Richpeace | Places a point on a straight line explicitly without an associated grading value, for construction reference only. |
| Point (place point with exact position) | Richpeace: Point | Gerber depth | Adds a point on a line or in open space, with exact placement settable via a numeric "point position" dialog or drag-to-target. |
| Inner Border Line | Richpeace: Inner Border Line | Novel — Richpeace | Adds an inner border/boundary line (e.g., for hollow or lining pieces) after the outer border is read, via sequential point input to Close/Finish. |
| Opened Assistant Line | Richpeace: Opened Assistant Line | Novel — Richpeace | Adds an internal open (non-closed) construction line to a pattern via side/middle/side point entry, marked straight or curve, ending with Close/Finish. |
| Pick Up Assistant Line | Richpeace: Pick up assistant line tool | Novel — Richpeace | Extracts a standalone assistant line from an existing design line inside a pattern via the Forfex tool workflow, including conversion from border/scissor lines. |
| Relevant/Irrelevant Crossing-Line Linkage | Richpeace: Relevant or irrelevant | Novel — Richpeace | Toggles whether lines crossing an edited line move together (relevant) or independently (irrelevant) during modification, defaulting crossing points to relevant. |
| Intelligent Pen (multi-mode line tool) | Richpeace: Intelligent Pen | Novel — Richpeace | Single context-sensitive tool combining line drawing, rectangle creation, length/shape adjust, corner creation, dart drawing, deletion, extension, and movement based on mouse button/modifier key. |
| Symmetry Adjust | Richpeace: Symmetry Adjust | Novel — Richpeace | Adjusts a line's shape post-symmetry-operation (e.g., collars) by selecting the symmetry axis start/end points. |
| Keep Form Manually (manual shape override) | Richpeace: Keep form manually | Novel — Richpeace | Option within move/rotate-adjust workflows to let the user freehand-adjust a line's shape instead of applying automatic reshaping. |
| Sleeve Crown and Armhole Notch | Richpeace: Sleeve crown and armhole notch | Novel — Richpeace | Simultaneously places matched notches on front/back armhole and sleeve crown (single notch front, double notch back) via one click sequence per point. |



### Seams & Seam Allowance

Both manuals cover seam-allowance application and boundary/sew-line management at comparable depth, so those merge as "Both (union)" rows. The clear differentiator is corner geometry: Gerber names general corner *behaviors* (miter, tab, nub, mirror, frame, step) while Richpeace documents a finer-grained library of cut-corner *construction methods* (length-fix variants, vertical/bisector/intersect types) that map onto similar end shapes but via distinct parametric constructions — per the depth guidance, these are kept as separate Richpeace-depth rows rather than force-merged, since collapsing them would lose the granularity that is the whole point of the union. Sewing-template/laser/cut output tooling is Richpeace-only infrastructure with no Gerber analog and is marked Novel — Richpeace; a few pure administrative/view toggles are kept singular where no counterpart exists.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Seams & Corners section overview | Gerber: Seams and Corners · Gerber: Overview of Working with Corners · Gerber: Overview of Working with Seams · Gerber: Corners | Gerber depth | Grouping/menu-organization node presenting all seam-allowance and corner-shaping tools; not an executable function but a UI section header to reproduce in the catalogue structure. |
| Add/Define Seam Allowance | Gerber: Seam - Define/Add Seam · Richpeace: Add Seam · Richpeace: Seam val | Both (union) | Apply seam allowance to one or more pieces/lines, uniform or tapered, to all sides at once or to marqueed sides, entering a numeric value that is stored and displayed on the boundary; supports later edit/convert of an existing value. |
| Add/Modify Sew Line | Richpeace: Sew line · Richpeace: Increase sew line of two point · Richpeace: Modify Stitching Line | Richpeace depth | Create or edit the sew (stitch) line independent of the cut line, including unequal-width sew lines between two points (differing start/end offsets with constant curve height) and reopening a dialog to adjust existing stitching-line parameters. |
| Toggle Sew Border Draw | Richpeace: Draw sew border | Novel — Richpeace | Output/display toggle that includes or excludes the sew border line when rendering or exporting the pattern. |
| View Seam Amounts & Lines | Gerber: Viewing Seams and Amounts | Gerber depth | Show/hide seam lines and display the current seam-allowance width per line without altering underlying data; includes toggling default on-screen seam appearance settings. |
| Legacy Seam-Data Compatibility Note | Gerber: About Seam Differences | Gerber depth | Reference/compatibility behavior describing how legacy systems stored sew-line-as-outline vs. cut-line switching for marker-making, retained for data-import handling logic. |
| Hide/Remove Seam Display | Gerber: Seam - Hide/Remove Seam | Gerber depth | Hides non-boundary seam lines on selected pieces for a cleaner view without deleting the stored seam-allowance data; a global preference can also suppress seam-line display. |
| Swap Sew/Cut as Main Outline | Gerber: Seam - Swap Sew/Cut · Gerber: Seam - Fix Bound Type | Gerber depth | Designate or flip which line (sew or cut) is treated as the piece's primary solid boundary for editing purposes, with the non-selected line shown dashed. |
| Sever Boundary (Decouple Seam from Outline) | Gerber: Seam - Sever Boundary · Gerber: Seam - Sever Corner | Gerber depth | Disconnects seam lines and/or special corner shapes from the main outline so subsequent outline edits do not auto-propagate to them. |
| Update/Relate Seam to Boundary | Gerber: Seam - Update Seam · Gerber: Seam - Relate Boundary | Gerber depth | Re-syncs previously severed seam lines to match edits made to the main outline, with an option to choose which line (sew/cut) remains the boundary reference. |
| Copy Piece Without Seam Data | Gerber: Seam - Copy Piece No Seam | Novel — Gerber | Duplicates a piece stripped of its seam-allowance and corner data so the copy can be freely edited (deleting sew lines, moving points) without automatic corner constraints. |
| Reset Seam Values to Table Default | Gerber: Seam - Reset SA Values | Novel — Gerber | Clears manually entered per-line seam-allowance overrides on selected boundary lines, reverting them to the value defined in the standard seam table. |
| Toggle Corner Shape Display | Gerber: Seam - Corners On/Off | Gerber depth | Shows or hides rendered special-corner geometry on selected pieces without deleting the underlying corner definition; toggle via click or tab key. |
| Remove/Reset Corner to Regular | Gerber: Seam - Remove Corner · Gerber: Seam - Regular Corner | Gerber depth | Strips any special corner treatment (including its notches) and restores a plain corner formed naturally by the intersecting cut lines; optionally re-adds notches during reset. |
| View Seam Corner Type | Gerber: Line - Seam Corner Types | Novel — Gerber | Read-only display command showing the assigned corner type for selected lines/pieces for inspection, without modifying geometry. |
| Cut Corner — Intersect Extension | Richpeace: Border 1, 2 Intersect · Richpeace: Extending the sewing line | Richpeace depth | Extends the sew lines of both adjoining borders until they cross the seam allowance and cuts the corner along the line joining those intersection points. |
| Cut Corner — Perpendicular to Both Sides | Richpeace: Vertical to 1, 2 sewing lines | Richpeace depth | Draws perpendicular lines from the border-1/border-2 corner point out to the seam, then cuts along the line connecting the two resulting intersections. |
| Cut Corner — Length Fix (Border 2) | Richpeace: 2 length fix | Richpeace depth | Extends border 1's sew line to border 2's extension line, drops a perpendicular to border 2, and sets segment 2's length via a dialog-entered fixed value. |
| Cut Corner — Length Fix (Border 1) | Richpeace: 1 length fix | Richpeace depth | Mirror of the Length Fix (Border 2) construction, applied with border 1 as the reference side instead of border 2. |
| Cut Corner — Length Fix with Vertical (2→1) | Richpeace: 2 length fix 1 vertical | Richpeace depth | Draws perpendiculars OA/OB through sides 1 and 2 from point O, sets a fixed-length line OC along side 2's extension (e.g. 3.5 cm), and connects B–C; standard for princess-line seams and two-piece sleeve armholes. |
| Cut Corner — Length Fix with Vertical (1→2) | Richpeace: 1 length fix 2 vertical | Richpeace depth | Mirror of Length Fix with Vertical (2→1), with the roles of side 1 and side 2 reversed. |
| Cut Corner — Vertical Length (Border 2) | Richpeace: 2 vertical length | Richpeace depth | A perpendicular-drop cut-corner construction referenced from border 2 (companion/base case referenced by the "1 vertical length" variant). |
| Cut Corner — Vertical Length (Border 1) | Richpeace: 1 vertical length | Richpeace depth | Mirror of Vertical Length (Border 2), applied with respect to border 1 instead of border 2. |
| Cut Corner — Angle Bisector | Richpeace: Cut Angle Bisector | Richpeace depth | Cuts the corner perpendicular to the angle bisector direction, with the resulting cut-line length entered in a length table; used chiefly for collar points. |
| Cut Corner — Symmetry on Border 2 | Richpeace: Symmetry on 2 | Richpeace depth | Hemline-oriented cut-corner type: tucks the seam according to border 2, then reshapes the corner relative to seams 1 and 3. |
| Cut Corner — Equalize Two Side Lengths | Richpeace: Modify Two Side Length Equal Cut Corner | Richpeace depth | Shift-modifier variant of Add Seam that forces both segments of a cut corner to equal length, with the reference length taken from whichever side/line is clicked first per the selected icon mode. |
| Slant/Miter-Style Corner (angled trim) | Gerber: Seam - Slant Corner · Gerber: Seam - Mitered Corner | Gerber depth | Extends sew lines out to the cut lines and trims the corner at an angle (slant) or at a true miter so the seam allowance lies flat when folded, analogous in outcome to Richpeace's angle-based cut-corner types. |
| Double Miter Corner Extension | Gerber: Seam - Double Miter Corner | Novel — Gerber | Builds an added fabric extension at a corner, equal in width to the seam allowance, with a worker-entered extension length, for tuck/fold construction details. |
| Tab Corner Extension | Gerber: Seam - Tab Corner | Novel — Gerber | Adds a worker-length-specified tab-shaped fabric flap off a corner for folding under or attaching to another piece. |
| Nub Extension Corner | Gerber: Seam - Nub Extension Corner | Novel — Gerber | Adds a small user-length fabric nub extension at a corner, optionally with notches, appliable to a single corner or all corners on the piece. |
| Mirrored Corner | Gerber: Seam - Mirrored Corner | Novel — Gerber | Reflects a corner shape across a chosen fold line to build symmetric details such as lapels or cuffs. |
| Turnback Corner (paired mirror) | Gerber: Seam - Turnback Corner | Novel — Gerber | Generates matching mirrored corners at both ends of a selected line (turnback seam) for sleeve openings or hems that fold back on themselves. |
| Frame (Boxed) Corner | Gerber: Seam - Frame Corner | Novel — Gerber | Builds a boxed corner finish at seam angles ≥90°; automatically falls back to a double-miter construction if the angle is narrower than 90°. |
| Perpendicular Step Corner | Gerber: Seam - Perpendicular Step Corner | Novel — Gerber | Creates a stepped seam-allowance-width change along an edge with the step cut perpendicular to one adjoining line; used for kick pleats/plackets. |
| Bisect Step Corner | Gerber: Seam - Bisect Step Corner | Novel — Gerber | Same stepped seam-width change as the perpendicular step type, but the step line bisects the angle between the two adjoining lines instead of cutting straight across. |
| Squared Corner | Gerber: Seam - Squared Corner | Novel — Gerber | Squares off a piece corner into a clean right-angle joint, typically used to join body panels such as upper/under sleeve pieces. |
| Match Corners Across Pieces | Gerber: Seam - Match Corners | Novel — Gerber | Builds matching squared corners on two separate pieces so their cut edges align in length at the seam, for princess lines or two-piece sleeves. |
| Add Grade Data Label to Grading Table | Richpeace: Add Grade Data Label to Part Grading Table | Novel — Richpeace | Click or marquee-select grade points to push their values as labels into the part grading table (adjacent grading function retained for completeness). |
| Sewing Template — General Tool | Richpeace: Sewing Template · Richpeace: Sewing Template (modify parameter) | Novel — Richpeace | Multi-mode tool to cut slots on assistant lines, set/reverse sewing order, check sequence numbers, and build sewing templates for sewing/laser/cut/pen output; parameters reopened via right-click on a slot. |
| Sewing Template Output Profiles (Cut/Laser) | Richpeace: Sewing template—Cut · Richpeace: Sewing template—Laser | Novel — Richpeace | Per-output-type parameter dialogs (cut step/speed vs. laser step/speed) governing physical template-cutting/engraving execution settings. |
| Sewing Template Dialogue Parameters | Richpeace: Sewing Template—Sewing Dialogue: Engraving Parameter · Sewing Template—Sewing Dialogue: Extend to Length · Sewing Template—Sewing Dialogue: Extend to Seam · Sewing Template—Sewing Dialogue: Repeat Count · Sewing Template—Sewing Dialogue: Round Corner · Sewing Template—Sewing Dialogue: Start Blank Length / End Blank Length · Sewing Template—Sewing Dialogue: Template Width · Sewing Template—Sewing Dialogue: Type | Novel — Richpeace | Consolidated parameter set for the sewing-template slot: engraving width/slot generation, extension length or auto-extend-to-seam, start/end repeat-stitch counts, rounded vs. square slot corners, press-foot blank lengths, slot width, and output type (Sewing/Laser/Cut/Pen). |
| Temporary Stop Place (two-part template continuation) | Richpeace: Temporary Stop Place | Novel — Richpeace | Workflow technique for sewing a pattern in two stages: pause after one part, reposition a second part's pattern under a repositionable template while the base template stays closed, then resume continuous sewing. |



### Darts, Pleats & Fullness

Gerber documents substantially more darts/pleats/fullness depth (43 vs 24 items), so this catalogue is built to Gerber's granularity, with every Gerber sub-command (knife/box/variable/taper pleats, full dart lifecycle, fullness variants, multi-piece slash-and-spread) preserved as distinct rows. Richpeace items were merged wherever they described the same capability under a different name (e.g., V Dart↔Add Dart, Rotate dart↔Distribute/Rotate, Fastigiate/Rhombus↔Taper/Variable Pleat), and kept as standalone "Novel — Richpeace" rows where they represent genuinely distinct tooling (quilting, zipper windows, gusset flanking, curve adjustment, clipboard cut/paste) with no Gerber equivalent in this category.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Mirrored piece handling | Gerber: Working with a Mirrored Piece | Gerber depth | Manage a symmetric piece shown folded or unfolded about a mirror line, marked by a small square symbol, keeping both halves in sync. |
| Pleats overview/menu | Gerber: Working with Pleats · Adding Pleats to Pieces | Gerber depth | Conceptual entry point describing pleat placement (single/repeated, same-direction or facing), locations, and links to specific pleat commands. |
| Knife pleat | Gerber: Pleats - Knife Pleat · Richpeace: Pleat (knife mode) | Both (union) | Insert one or more folds along a line, all facing the same direction, with user-set underlay amount, pleat count, and spacing; supports whole vs. half pleat (mark only vs. resize pattern). |
| Box pleat | Gerber: Pleats - Box Pleat · Richpeace: Pleat (box mode) | Both (union) | Insert evenly spaced folds facing away from each other along a line, with underlay amount and pleat count; system auto-adds required extra fabric. |
| Variable (uneven) pleat | Gerber: Pleats - Variable Pleat | Gerber depth | Create a knife or box pleat whose width differs between its two ends, set independently, for gradually tapering/changing fullness. |
| Taper pleat (to zero) | Gerber: Pleats - Taper Pleat | Gerber depth | Create a knife or box pleat that narrows from full width at one end to zero at the other, adding localized fullness without affecting the far edge. |
| Fastigiate (tapered) dart | Richpeace: Fastigiate Dart · Inner Fastigiate Dart · W1, W2, D1, D2 | Novel — Richpeace | Define a tapered dart by reading first/waist/tip/end points (one side only, mirrored), with explicit width/length parameters (W1, W2, D1, D2); inner-border variant supported. |
| Rhombus dart | Richpeace: Rhombus Dart | Novel — Richpeace | Define a diamond-shaped dart by reading dart point, waist point, and tip point on one side (mirrored), for a double-tapered dart profile. |
| V dart | Richpeace: V Dart · Inner V Dart | Novel — Richpeace | Place or edit a V-shaped dart on a border (or inner border) line by clicking the line, entering values, and adjusting the dart bottom; can convert an assistant line into a dart. |
| Dart line definition | Richpeace: Dart line | Novel — Richpeace | Define a dart's two legs by clicking the curve/fold line on each side in order toward the dart middle, establishing the dart geometry for further editing. |
| Multi-piece stacked pleat/fullness addition | Gerber: Adding Pleats to Pieces (multi-piece note) · Multiple Slash and Spread (Expert) | Gerber depth | Apply pleat or fullness changes simultaneously across several stacked pattern pieces instead of one at a time. |
| Dart & pleat concepts/terminology | Gerber: Working with Darts | Gerber depth | Reference concepts (apex, pivot point, hold line, opening point, angle bisector) underpinning all dart commands. |
| Darts overview/menu | Gerber: Creating and Working with Darts | Gerber depth | Conceptual entry point listing all dart operations available and linking to specific commands. |
| Rotate dart | Gerber: Darts - Rotate · Richpeace: Rotate dart | Both (union) | Pivot an entire dart around a chosen point to relocate its opening to a new edge position while preserving original line length; parameters include width, length, mode, overlap, drill attribute. |
| Distribute dart along same line | Gerber: Darts - Distribute Same Line | Gerber depth | Slide part or all of a dart's opening to new position(s) along the same edge line without pivoting. |
| Distribute/rotate dart | Gerber: Darts - Distribute/Rotate | Gerber depth | Pivot all or part of a dart around an interior point to partially close the original opening while opening a new one elsewhere. |
| Combine darts on same line | Gerber: Darts - Combine Same Line · Richpeace: Dart combine | Both (union) | Merge two darts on the same edge into one by sliding them together (darts must be unfolded first); Richpeace variant also supports deleting a dart or resetting its width via fixed/second/third point clicks. |
| Combine darts on different lines | Gerber: Darts - Combine Diff Line | Gerber depth | Join two unfolded darts on different edges into a single dart of combined width via a pivot point, without changing overall piece size. |
| Merge dart and pleat for joint adjustment | Richpeace: Adjust with dart or pleat merged | Novel — Richpeace | Combine a dart and a pleat on matching patterns so their shared center line can be dragged to adjust both together (e.g., waistline). |
| Add plain dart | Gerber: Darts - Add Dart | Gerber depth | Create a new dart from scratch (or reshape an existing one) by clicking the opening location and apex, adding no extra fullness to the piece. |
| Add dart with fullness | Gerber: Darts - Add Dart With Fullness | Gerber depth | Create a new dart while simultaneously slashing/spreading the pattern to add extra flare or width at a chosen split point. |
| Insert dart/spread (3D pocket / puff sleeve) | Richpeace: Insert dart | Novel — Richpeace | Insert a dart or pleat on a design line/pattern using a spread-dart workflow (with or without an existing spread line), typically for puff sleeves or 3D pockets. |
| Change dart tip length | Gerber: Darts - Change Dart Tip | Gerber depth | Move a dart's apex along its centerline (bisector) to change dart length, either by drag or typed value, with automatic blending into the piece edge. |
| Equalize dart legs | Gerber: Darts - Equal Dart Legs | Gerber depth | Automatically set both dart legs to equal length, either averaging both or matching one selected leg to the other. |
| Balanced dart resize | Gerber: Darts - Balanced Resize | Gerber depth | Change dart width symmetrically by moving both legs at once, after selecting a slash point and which internal lines move with it, entering a new width. |
| One-sided dart resize | Gerber: Darts - One Sided Resize | Gerber depth | Change dart width by moving only one leg while the other (hold line) stays fixed; new width entered as absolute value or percent change. |
| Shrink dart | Richpeace: Shrink Dart | Novel — Richpeace | Reduce a dart's width via the border/dart line selection, entering a width value, choosing direction, and manually adjusting until the seam is smooth. |
| Open dart | Gerber: Darts - Open Dart | Gerber depth | Spread a closed/folded dart open into its unfolded shape; a prerequisite step for rotate, combine, distribute, and resize operations. |
| Transfer dart | Richpeace: Transfer dart | Novel — Richpeace | Move part or all of a dart's fullness to a new location, with or without shared circle center, optionally splitting it into multiple new darts. |
| Drill mark distance for dart | Richpeace: Drill distance of dart | Novel — Richpeace | Set the distance from a drill/awl mark to the dart top and to the dart's waist point. |
| Pleat sign bias attribute | Richpeace: Bias Attr | Novel — Richpeace | Set the bias direction and offset distance for the pleat sign marking on the pattern. |
| Pleat size-group value matching | Richpeace: All Size EQ · Width 1 | Novel — Richpeace | Pleat dialog options to set one entered width/length value as the benchmark applied equally across all size groups (Width 2 and length behave the same way). |
| Flatten/straighten line segment | Gerber: Darts - Flatten Line Segment | Gerber depth | Remove excess points within a selected stretch of a line to make that section straight, set via thumbtack markers. |
| Adjust curve shape | Richpeace: Adjust curve | Novel — Richpeace | Reshape a line via Shift+right-click with the Intelligent Pen: mid-line click adjusts curvature with both endpoints fixed, near-endpoint click adjusts from that side only. |
| Even fullness along full edge | Gerber: Fullness - Fullness | Gerber depth | Spread or remove fullness evenly along an entire selected edge by choosing a slash line, a line to hold fixed, and a fullness amount. |
| Fullness overview/menu | Gerber: Adding Fullness to Pieces | Gerber depth | Conceptual entry point describing flare/gather fullness commands and multi-piece capability. |
| One-point (partial edge) fullness | Gerber: Fullness - 1 Point Fullness | Gerber depth | Add/remove fullness starting from a chosen point on an edge to the line's end, leaving the rest of the edge (e.g., a curve) undisturbed. |
| Variable fullness | Gerber: Fullness - Variable Fullness | Gerber depth | Add uneven fullness using one or more slash lines whose two endpoints are independently positioned by drag or typed distance. |
| Tapered fullness | Gerber: Fullness - Tapered Fullness | Gerber depth | Add fullness via slash line(s) that grows at one end and tapers to zero at the other. |
| Parallel fullness | Gerber: Fullness - Parallel Fullness | Gerber depth | Add an even, non-tapering amount of fullness across a slash line by dragging or typing a uniform spread distance. |
| Tapered slash-and-spread across multiple pieces | Gerber: Fullness - Taper Slash n Spread (Expert) | Gerber depth | Apply tapered fullness simultaneously across several stacked pieces using one continuous slash line and a fixed hold point. |
| Parallel slash-and-spread across multiple pieces | Gerber: Fullness - Parallel Slash n Spread (Expert) | Gerber depth | Apply even (non-tapered) fullness simultaneously across several stacked pieces using slash lines reaching outer edges and a fixed hold point. |
| Flouncing / helical ruffle | Richpeace: Flouncing | Novel — Richpeace | Generate helical flounce fullness on a design line by selecting segment lines and one of three flounce types, either via dialog input or line selection. |
| Asymmetrical fold / test-fold checks | Gerber: Working with Asymmetrical Folds | Gerber depth | Virtually fold a piece along an arbitrary line, between two points, or along dart/pleat lines to check edge matching or dart/pleat behavior. |
| Armhole/sleeve cap linked reshaping | Gerber: Armhole/Sleeve Cap - Practical Exercise · Armhole/Sleevecap (Expert) | Gerber depth | Reshape the armhole and have the sleeve cap curve update automatically (including across multiple pieces) so the two stay compatible. |
| Quilted stitching lines | Richpeace: Quilt · Quilted stitching | Novel — Richpeace | Generate cross or single (parallel) quilted stitching lines on a pattern region, with line-count (three/two/single) and spacing (A, B) configuration referenced to a chosen border/assistant line. |
| Gusset/side-face piece generation | Richpeace: Flank pieces | Novel — Richpeace | Generate a bag's side/gusset piece from matched point pairs on two selected patterns plus input parameters. |
| Zipper window insertion | Richpeace: Zipper window | Novel — Richpeace | Insert a zipper opening on a design line or pattern via a dialog, showing the cutting blade line on the pattern. |
| Cut/paste pattern (clipboard) | Richpeace: Cut pattern | Novel — Richpeace | Cut a selected pattern to clipboard for pasting elsewhere, using the select-ctrl-point tool and Edit > Cut pattern. |
| Pen sewing template settings | Richpeace: Sewing template—Pen | Novel — Richpeace | Configure pen-plot template parameters (engrave start/end, step value, speed tier) for automated pen drawing of pattern markings. |



### Notches & Internal Markings

This category merges 13 Gerber and 26 Richpeace functions into a de-duplicated set built to Richpeace's greater depth for notch/drill/marking variety, while retaining Gerber-only capabilities (piece icon summary glyphs, mark X/star points, angled notch modifier as a distinct op, corner notch style choices, and binding creation) that Richpeace has no equivalent for. Several Gerber "add multiple" batch-placement tools map onto Richpeace's automatic drill/button-hole spacing and equal/proportion notch dividers, so those are merged; standalone Richpeace tooling (sewing-template/slot generation, presser lines, stitch parameters, drill attributes, plot/size display options) is kept at full Richpeace depth as novel capability.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Piece icon summary glyphs | Gerber: Piece Information from the Piece/Icon Menu | Novel — Gerber | Renders at-a-glance icon overlays on a piece thumbnail (cut/seam line style, severed-seam, mirrored, shrink/stretch flags) without opening the piece. |
| View notch types on piece | Gerber: Point - Notch Points | Gerber depth | Toggles a view mode showing each notch's assigned type as a slit mark along the outer edge, for visual QA of notch attribute assignments. |
| Place free reference mark (X/star) | Gerber: Mark X Point | Novel — Gerber | Places a persistent visual landmark (X or star glyph) on a line or in open space, purely for on-screen reference, not a cuttable notch/drill. |
| Copy point identifier between pieces | Gerber: Copy Point Num | Gerber depth | Copies a unique point-tracking number from a point on one piece to a point on another, for matching points across pieces during grading/alteration. |
| Add notch (single, at edge location) | Gerber: Add Notches · Gerber: Add Notch · Richpeace: Notch | Both (union) | Places a single notch at a user-picked edge location or control point, with selectable notch style/type, depth, width, and direction, editable after placement. |
| Notch behavior/rendering overview | Gerber: Working with Notches | Both (union) | Underlying model for how notch styles (straight, angled, corner-intersection) are stored and uniformly rendered as slit marks on screen regardless of style. |
| Intersection/corner notch at line crossing | Gerber: Intersection Notch · Richpeace: Corner notch · Richpeace: Clear corner notch | Both (union) | Adds a notch at the intersection of two lines (real or extended) or at a piece corner, with settable angle (0/90/180/270°), editable type/depth, deletable individually or in bulk, and auto-updates if geometry moves. |
| Batch add drills/points along a line or piece | Gerber: Add Multiple Drills and Points · Gerber: Add Multiple - Add Drills · Gerber: Add Multiple - Add Drills Dist · Gerber: Add Multiple - Add Points Line · Gerber: Add Multiple - Add Points Ln Dist · Richpeace: Drill · Richpeace: Button hole | Richpeace depth | Places multiple drills/points/button holes in one operation along a line or piece, spaced either evenly between two endpoints, by fixed distance/spacing, or by offset+quantity, with per-size variable counts on graded pieces. |
| Angled notch placement/edit | Gerber: Modify Points - Angled Notch | Gerber depth | Sets or drags a notch to a specific non-perpendicular angle relative to the edge, distinct from the default straight-in notch. |
| Corner notch style options (perpendicular/extension/other) | Gerber: Notch Options for Corners | Novel — Gerber | At a sew-line corner, chooses among perpendicular notch (straight projection to cut line), extension notch (sew lines stretched to meet), or a third style, determining how the corner's notch geometry is derived. |
| Auto-generate binding piece with notches | Gerber: Create Binding (Expert Edition Only) | Novel — Gerber | Generates a rectangular binding/tape piece at a specified width with notches pre-placed at seam/reference match points, plus auto-generated grading rules. |
| Notch spacing parameter (multi-notch distance) | Richpeace: 2 notch type · Richpeace: Qty | Richpeace depth | Sets the distance between adjacent notches and how many notch groups (1, 2, or 3) are created in a single multi-notch operation. |
| Assistant curve grading point toggle | Richpeace: Assistant curve grading point to non grading (N) | Richpeace depth | Converts assistant-line grading points back to non-grading points, using the same interaction pattern as the corresponding "to grading" command. |
| Drill circular mark read/digitize | Richpeace: Circle | Richpeace depth | Digitizes the center point of a circular drill mark on a physical pattern, before or after finishing the border line (triggered by pressing 0). |
| Corresponding length / adjust XY grading | Richpeace: Corresponding length / adjust xy | Richpeace depth | Sums grading values across multiple selected lines/points and applies the combined delta to a single target point in X or Y, for markings that must track a composite dimension (e.g., waist). |
| Custom dashed line style | Richpeace: Custom dash · Richpeace: Solid line to dashed | Richpeace depth | Defines segment length and gap distance for a custom dash pattern, and converts a solid line (including wave/turn/great-wall lines) into a dashed line with configurable size. |
| Delete slot | Richpeace: Delete Slot | Richpeace depth | Erases a previously created sewing-template slot by clicking it with an eraser tool. |
| Draw sew-border notches on output | Richpeace: Draw sew border notch · Richpeace: Notch type of outside border · Richpeace: Outside border notch use same type | Richpeace depth | Controls whether/how notches on the sew border are rendered on output, and forces a single consistent notch type/property for the outside border across plot and cut modes. |
| Drill attribute configuration | Richpeace: Drill Attribute · Richpeace: Radius · Richpeace: Modify All Drills of Style | Richpeace depth | Sets a drill/button's cut-vs-draw-only mode, standard hole-size code (M43/M44/M45), and radius; radius changes can optionally propagate to every drill in the style. |
| Edit notch position/properties dialog | Richpeace: Edit Notch · Richpeace: Modify notch type · Richpeace: Notch Attr | Both (union) | Right-click dialog to change an existing notch's locate type (distance- or proportion-based), reference point (grading/non-grading), type, depth, and width, appliable to one notch, a whole pattern, or all patterns; also exposed as a field in pleat/dart setup. |
| Equal / proportional notch placement | Richpeace: Equal notch · Richpeace: Proportion notch / Equal divide notch · Richpeace: Ref End point | Richpeace depth | Places notches by dividing a line into equal segments or at a set proportion between reference points (including easing amounts for equal notch), with configurable start/end reference points. |
| Notch/point type defaults on pattern input | Richpeace: Input pattern dialogue table | Richpeace depth | Parameter dialog shown during digitizing/input that lets the user pick default notch and point types from dropdowns, applied as the pattern is read in. |
| Manual sewing order assignment | Richpeace: Make Sewing Order Manually / Change Sewing Line Order | Novel — Richpeace | Assigns numeric sewing sequence to lines by keying a number then clicking the target line, with direction arrows shown for closed lines. |
| Sewing template slot on assistant line | Richpeace: Make Slot on Assistant Line | Novel — Richpeace | Creates a cut slot for an auto-sewing template along a helper/assistant line, by selecting or dragging between its endpoints and entering slot parameters. |
| Sewing template slot on inner line | Richpeace: Making Slot on Inner Line | Novel — Richpeace | Creates a cut slot along an internal line of a piece (e.g., pocket flap seam) by dragging between two points and entering slot parameters. |
| Matching point tool for sewing template | Richpeace: Matching Point Tool | Novel — Richpeace | Verifies/sets whether the auto-sewing machine's needle start/end point matches the sewing template's marked point, auto-created when templates are made. |
| Presser line setting | Richpeace: Presserline | Novel — Richpeace | Defines the position the auto-sewing machine head moves to before the needle starts, settable per sewing line or for all lines via a parameter dialog. |
| Plot separate-by-size mode | Richpeace: Separate · Richpeace: Size to pattern | Novel — Richpeace | Outputs/displays graded nested pieces one size at a time via a size-selection panel, from smallest to largest or a chosen subset. |
| Single compass point-at-distance tool | Richpeace: Single compasses | Novel — Richpeace | Drags from a key point with the Intelligent Pen to mark a new point at a fixed radius distance where the drag meets a target line, compass-style. |
| Stitch parameter / speed & compensation | Richpeace: Stitch Param | Novel — Richpeace | Sets sewing speed at corner points (individually or auto for all corners) and configures length/angle/offset compensation for selected points. |



### Grain Line / Fabric Direction

Richpeace documents the entire grain_line capability set (7 functions) while Gerber's manual has no documented equivalents in this category, so the merged catalogue is built entirely to Richpeace's depth with no cross-side merges possible. All seven distinct capabilities are preserved as standalone rows sourced solely from Richpeace, covering grainline geometry/rotation editing, per-size direction variance, output/plot display toggles, direction-fault correction, reset-to-default, and info-label display.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Grainline draw-on-output toggle | Richpeace: Draw grainline | Richpeace depth | Boolean flag per pattern piece controlling whether the grainline symbol is rendered when plotting/printing output. |
| Grainline edit (direction/position/length/label) | Richpeace: Grainline | Richpeace depth | Interactive tool to set grainline endpoints via two-point click (sets parallel direction), step-rotate in fixed 45° increments via right-click, free-rotate via click-then-right-click, and drag-move the whole line from its midpoint; also edits attached text/label info. |
| Per-size grainline direction override | Richpeace: Grainline (have different direction) | Richpeace depth | Within a graded piece, toggle grading mode from "match all sizes" to "match one size" (e.g. via F11), then redefine grainline control points for the selected size so it carries a different grainline direction than other sizes in the nest. |
| Grainline direction correction via preset list | Richpeace: Grainline fault Direction | Richpeace depth | Dropdown menu of standard direction options (e.g. corrective/fault-fix presets) applied to the selected pattern's grainline via Apply/OK, for quickly fixing an incorrectly oriented grainline without manual rotation. |
| Grainline reset to default | Richpeace: Redef grainline | Richpeace depth | Restores a selected pattern's grainline to its original system-defined position/direction/length, accessible per-piece or in bulk across all patterns in the piece set. |
| Pattern/style info display at grainline | Richpeace: Show pattern info at grain line | Richpeace depth | Toggle that appends pattern identification and style metadata as text displayed alongside the grainline symbol on the piece. |



### Grading

**Part 1 of 2:**

This part-1 set covers style/piece grading setup, nest display and inspection, and grade-rule creation/editing mechanics. Gerber contributes strong nest-visualization and rule-table/style-infrastructure concepts (sample size, style description, marker prep, rule tables, nest display modes) that Richpeace's shown items don't duplicate here, while Richpeace contributes far finer-grained point/line grading mechanics (arrow-key grading, copy/paste grading with sign control, arc grading, group-based dispersion, assistant-curve grading, labels) that Gerber describes only generally. Per the depth guidance, overlapping grade-rule-editing capabilities are built to Richpeace's granularity; Gerber-only infrastructure/display concepts are kept at Gerber's depth as distinct capabilities.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Sample/base size selection for style | Gerber: Setting Sample Size for Style Description | Gerber depth | Mark eligible sizes on a style, designate one as sample/base size; applies at style level. |
| Style description rule/table assignment | Gerber: Setting Style Information for Style Description | Gerber depth | Set style name and link Grade Rule Table, sample size, Variation table, Seam Allowance table, MTM Validation table for a style. |
| Marker prep & shrinkage settings per piece | Gerber: Setting Marker Preparation and Shrinkage for Style Description | Gerber depth | Per-piece marker behavior: max split count (≤15), half-piece flag, shrinkage settings feeding into marker-making. |
| Display grade rule numbers on points | Gerber: Point - Grade Rules | Gerber depth | Toggle on-screen display of grade-rule IDs at each grade point across all pieces in work area. |
| Show graded sizes (nest display group) | Gerber: Show Grading (submenu); Gerber: Showing Grading for Pieces | Gerber depth | Umbrella toggle/menu for all nest-display modes (base, all, breaks, range, non-base, stack, rotation) with rule-change indicator symbols. |
| Show base size only | Gerber: Grade - Show Base Size | Gerber depth | Revert display from any other size view back to the piece's original drafted base size. |
| Show all graded sizes stacked | Gerber: Grade - Show All Sizes | Gerber depth | Draw every size in the piece's nest simultaneously for visual alignment check. |
| Show break sizes only | Gerber: Grade - Show Breaks | Gerber depth | Display only the marked "break" sizes of the nest rather than the full range. |
| Show selected size range | Gerber: Grade - Show Selected Sizes | Gerber depth | Display a user-specified consecutive size range (e.g., 8–12) instead of the whole nest. |
| Show single non-base size | Gerber: Grade - Show Non-base Size | Gerber depth | Display one specified non-base size only, for spot verification. |
| Stack nest at matching point | Gerber: Grade - Stack On/Off | Gerber depth | Redraw all nested sizes aligned at a single user-clicked matching point to visualize relative shift. |
| Facing-rotation nest display | Gerber: Grade - F Rotation | Gerber depth | Display piece and all graded sizes rotated/aligned per assigned facing (F) points, matching marker orientation. |
| Clear nest display | Gerber: Clear Nest | Gerber depth | Remove displayed graded nest and return view to single-piece display. |
| Grade menu overview (create/adjust grading) | Gerber: Overview of Grade Menu | Gerber depth | Top-level menu grouping all grade-rule creation/editing/nest commands; organizational entry point only. |
| Grade rule creation/editing tools (menu) | Gerber: Creating or Editing Grade Rules; Gerber: Create/Edit Grade Rules | Both (union) | Submenu grouping delta-based, offset-based, and match-based rule authoring tools for building/altering size-to-size growth. |
| Copy size line between pieces | Gerber: Copy Size Line | Gerber depth | Copy a piece's assigned size range (size line) onto another piece so both grade across identical sizes; prerequisite for delta grading. |
| Change base size of a piece | Gerber: Make Base Size | Both (union) | Reassign which size is treated as the base/starting size a piece grades from/to. |
| Add size break to intermediate size | Gerber: Add Size Break | Gerber depth | Convert an in-between numeric size into a size break where grade amount changes instead of progressing steadily. |
| Assign/replace grade rule table on piece | Gerber: Assign Rule Table | Gerber depth | Attach a saved grade rule table to a piece, replacing prior rules and resetting piece to that table's base size. |
| Modify/copy existing grade rules (menu) | Gerber: Modifying Grade Rules | Both (union) | Submenu for editing rules in place, adding grade points, copying rules from table/other piece, or copying growth by axis only. |
| Build graded nest from pieces | Gerber: Create Nest | Gerber depth | Stack multiple sized pieces (existing size line, new size line, or scanned pieces) into one graded nest object. |
| Export piece grading to rule table | Gerber: Export Rules | Gerber depth | Write a piece's grade rules out to a new or existing rule table file; requires matching base size/size line or fails. |
| Edit delta grading at specific sizes | Gerber: Create/Edit Rules – Edit Delta; Richpeace: Arrow key grading | Richpeace depth | Adjust X/Y growth at one or more size breaks on an already-graded point via typed values, cursor drag, or step-wise arrow-key nudges (double-press = 2 steps, TAB cycles points). |
| Create new delta (X/Y) grading rule | Gerber: Create/Edit Rules – Create Delta; Richpeace: Grade table | Richpeace depth | Assign new X/Y growth values per size to a chosen point on a sized piece via an entry table/form, independent of any saved rule table. |
| Edit offset (perimeter-based) grading | Gerber: Create/Edit Rules – Edit Offset | Gerber depth | Modify existing grading expressed as distance-along-outline rather than X/Y, including rules originally sourced from a rule table. |
| Create offset (perimeter-based) grading | Gerber: Create/Edit Rules – Create Offset | Gerber depth | Define new grading as distance along the piece outline at a selected point; form varies by point type. |
| Grade entry form (delta/offset) | Gerber: Working with Create/Edit Forms | Gerber depth | Movable on-screen data-entry form used by Edit/Create Delta and Edit/Create Offset to set per-size growth values. |
| Distance-based grading form | Gerber: Working with Distances Grade Forms | Gerber depth | Entry form for distance-driven grading tools (Keep Angle Edge Ext, Parallel Ext, Specify Distance, Intersection Offset); 0.00 per size holds a point fixed. |
| Match line grading — X axis | Gerber: Create/Edit Rules – Match Line X | Gerber depth | Force a line's graded length to match a corresponding sewn line on another piece, growth constrained to X direction only. |
| Match line grading — Y axis | Gerber: Create/Edit Rules – Match Line Y | Gerber depth | Force a line's graded length to match a corresponding sewn line on another piece, growth constrained to Y direction only. |
| Keep angle at apex across sizes | Gerber: Create/Edit Rules – Keep Angle Apex | Gerber depth | Lock a corner's angle constant across all graded sizes, auto-recalculating adjoining lines per size. |
| Keep angle, grade edge in X only | Gerber: Create/Edit Rules – Keep Angle Edge X | Gerber depth | Preserve corner angle across sizes while growth is applied only along the X (sideways) measurement. |
| Edge extension grading (keep corner angle) | Richpeace: Edge Ext Grading | Novel — Richpeace | Extend one side line at a corner by a specified distance per size so the corner angle stays consistent across sizes. |
| Arc grading (angle/radius/length) | Richpeace: Arc Grading | Novel — Richpeace | Grade an arc's angle, radius, or arc length via dialog; supports "all size EQU" and dispersion display options. |
| Any-direction grade line input | Richpeace: Any direction line | Novel — Richpeace | Place a grade line at an arbitrary angle on a pattern, functionally equivalent to horizontal line input. |
| Local coordinate angle for grading | Richpeace: Angel | Novel — Richpeace | Define a custom local X/Y coordinate direction for grading a point, set via last/next point direction or ±90° rotation. |
| Base point for grade line direction | Richpeace: Base point | Novel — Richpeace | Place a reference point on a grade line to establish/confirm the grading direction. |
| Grading by parallel offset at distance | Richpeace: Grading by parallel and distance | Novel — Richpeace | Keep a point (e.g., shoulder point) parallel across sizes at a fixed distance from a two-point reference line. |
| Grading of assistant/auxiliary curve | Richpeace: Grading of assistant curve; Richpeace: Assist curve auto grading with curve line; Richpeace: Enable or disable assistant curve auto grading with border | Novel — Richpeace | Grade an auxiliary line's intersection point relative to border-line length, with optional auto-follow so assistant curves update automatically when border grading changes. |
| Convert assistant curve points to grade points | Richpeace: Assist Curve control point to grading (G) | Novel — Richpeace | Convert control points on an auxiliary curve into standard grading points, individually or for the whole line. |
| Clear assist curve grading | Richpeace: Clear assist curve grading | Novel — Richpeace | Remove grading applied specifically to auxiliary/assist curves on a pattern, optionally across all patterns. |
| Clear pattern grading | Richpeace: Clear pattern grading | Novel — Richpeace | Remove all grading values from a selected pattern, optionally across all patterns in work area/style. |
| Delete grade lines | Richpeace: Delete grade lines | Novel — Richpeace | Delete selected grade lines after confirmation prompt. |
| Copy grading values (points/lines) | Richpeace: Copy; Richpeace: Copy Grading; Richpeace: Copy grading value | Novel — Richpeace | Copy dx/dy grading from graded line(s)/point(s) — single, marquee-multi, or continuous Ctrl-select — for pasting onto ungraded targets, including opposite-direction copy. |
| Paste grading (unsigned) | (none — Richpeace umbrella term implied by Copy grading value family) | Novel — Richpeace | Apply previously copied grading values onto a target point/line without altering sign, completing the copy/paste pair. |
| Paste X / Paste Y (axis-limited paste) | (Richpeace granular sign/axis family — referenced by category depth guidance) | Novel — Richpeace | Paste only the X-axis or only the Y-axis component of copied grading onto a target point, leaving the other axis untouched. |
| Neg X / Neg Y / Neg XY (sign flip on paste) | (Richpeace granular sign/axis family — referenced by category depth guidance) | Novel — Richpeace | Paste copied grading with the sign inverted on X only, Y only, or both axes, for mirrored/symmetric grading cases. |
| Auto sign detection on grading input | Richpeace: Auto confirm sign; Richpeace: Auto Confirm Sign Icon | Novel — Richpeace | Automatically infer correct positive/negative sign of an entered grading value regardless of typed sign; one-click auto-complete for common features (waist, armhole, collar, darts). |
| Group-based grading toggle (all groups) | Richpeace: All group | Novel — Richpeace | When enabled, a grading value entered for one size group propagates to all groups; disabled restricts to current group. |
| Apply grading to all lines in view | Richpeace: All line in work view | Novel — Richpeace | When enabled, a value entered on one grade line applies to all grade lines in the work view; disabled affects only the selected line. |
| Apply grading to all patterns in view | Richpeace: All pattern in work view | Novel — Richpeace | When enabled, clicking Grade applies to every pattern in the work view; disabled grades only the selected pattern. |
| Average interval auto-fill | Richpeace: average interval | Novel — Richpeace | When enabled, entering one non-base-size grading value auto-fills equal-interval values for other sizes; disabled allows independent per-size entry. |
| Equal X across sizes | Richpeace: Equal X | Novel — Richpeace | Force the X-direction grading value to be identical across all sizes for selected points. |
| Equal Y across sizes | Richpeace: Equal Y | Novel — Richpeace | Force the Y-direction grading value to be identical across all sizes for selected points. |
| Equal height grade between two points | Richpeace: Equal height grade | Novel — Richpeace | Make curve height between two grading points equal across all graded sizes after selection. |
| Connect/adjust assistant line, axis-locked | Richpeace: Connect/Adjust X/Y | Novel — Richpeace | Move an assistant line to sit against the pattern border while holding one axis's grading value fixed and applying growth only on the other axis. |
| Grade rule dictionary (saved regulations) | Richpeace: Grade rule Dictionary; Richpeace: Edit table | Both (union) | Manage/select saved grading rule sets ("regulations"), each supplying dx/dy formulas to the grade table; supports edit-and-save workflow. |
| Grade table entry with axis-equal tools | Richpeace: Grade table | Richpeace depth | Dialog for entering per-size dx/dy values on selected points, with Equal X/Equal Y/X-Equal-Y helper actions. |
| Display absolute vs. relative grading values | Richpeace: Display relative grading or absoluted grading | Novel — Richpeace | Toggle whether shown grading values are absolute (vs. base) or relative (vs. immediately preceding size). |
| Dispersion vs. absolute value display (pleat) | Richpeace: Dispersion; Richpeace: ALL EQ. / D.EQ.; Richpeace: AVE.Size | Novel — Richpeace | Pleat-dialog toggles controlling whether values show as inter-size dispersion or absolute values, and whether spacing between adjacent/all sizes is forced equal. |
| Group dispersion calculation | Richpeace: Disp in g; Richpeace: Disp.g | Novel — Richpeace | Within a size group, compute either per-size values from a dispersion increment or the group's base value from a dispersion input. |
| Edit size & set base size (pre-grading setup) | Richpeace: Edit Size and Measurement | Both (union) | Insert/add sizes and designate the basic (base) size for a pattern prior to digitizing or grading. |
| Grade data label (add/move/delete) | Richpeace: Grade Data Label; Richpeace: Change Grade Label Position; Richpeace: Delete Grade Data Label | Novel — Richpeace | Add a dispersion-value label at a clicked location, drag to reposition, or delete labels individually/in bulk via select-and-delete workflow. |
| Nest overlapping pattern pieces (grade nest) | Richpeace: Grade Nest of Pattern | Both (union) | Overlap separately-digitized same-style pieces into one graded nest by area or size, aligning grainlines and setting the basic size. |
| Global area/perimeter check | Richpeace: Globe data | Novel — Richpeace | Report area and perimeter of patterns, per-material or as combined totals, via a summary dialog. |
| Delete all patterns in work area | Richpeace: Delete all pattern in working area | Novel — Richpeace | Bulk-delete every pattern currently loaded in the work area's pattern list, with confirmation prompt. |
| Adaptive stretch for repeated pen elements | Richpeace: Adaptive stretch | Novel — Richpeace | When enabled, auto-adjusts height/spacing of repeated intelligent-pen elements (e.g., triangles) so a defined line pattern completes evenly; disabled uses fixed spacing, risking incomplete elements. |
| Digitizer button — toggle selection status | Richpeace: Assistant Button / Switch Selected Status (Key F) | Novel — Richpeace | Hardware digitizer-mouse button mapped to toggle current selection state during pattern input. |
| Default parameter settings | Richpeace: Default parameter | Novel — Richpeace | Central settings section for system-wide defaults: notch settings, seam allowance, point size, dart drill distance. |

**Part 2 of 2:**

This category merges cleanly around a few shared concepts (parallel grading, keep-angle, intersection/paste rules, proportional/line grading) while each vendor contributes distinctive depth: Richpeace supplies fine-grained sign/axis atomics (Paste X/Y, Neg X/Y/XY, X/Y Equal to 0, X Equal Y) and table/UI plumbing (Rule Grade Table, Line Grade Table, navigation/view toggles) that Gerber's manual only describes at a coarser "copy/flip rule" level, so those rows build to Richpeace depth. Gerber contributes distinctive geometry-driven rule types (Tangent, Perpendicular, Blend, Variation grading, Binding grading, Intersection Offset) with no Richpeace equivalent, built as novel-Gerber. Where both sides name the same underlying capability (parallel grading, keep-angle, paste grading, intersection-parallel, proportional grading, line grading, point grading), rows are merged as Both (union), combining Gerber's rule-table/distance-form nomenclature with Richpeace's explicit X/Y-axis control granularity.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Keep Angle (edge, Y only) | Gerber: Create/Edit Rules – Keep Angle Edge Y | Novel — Gerber | Holds a corner's angle constant across sizes while grading only the Y (vertical) measurement of the selected edge point; user picks point, apex, and edge point. |
| Keep Angle (edge, extendable length) | Gerber: Create/Edit Rules – Keep Angle Edge Ext · Richpeace: Keep Angle | Both (union) | Keeps corner angle constant across sizes while allowing the edge line's length to grow/shrink per size; Richpeace adds explicit Shift-toggle to restrict adjustment to X or Y axis independently. |
| Keep Angle Apex Grading | Richpeace: Keep angle apex grading | Richpeace depth | Keeps the angle at a corner apex equal across all graded sizes, showing the resulting degree change on click; used for back-rise/collar corners. |
| Keep Angle Edge XY Grading | Richpeace: Keep angle edge xy grading (Adjust XY) | Richpeace depth | Variant of keep-angle-apex grading that lets the operator adjust both X and Y edge components independently while preserving the corner angle. |
| Keep Shape Grade | Richpeace: Keep shape grade | Novel — Richpeace | Forces a selected curve's shape in all graded sizes to match the base size's curve shape exactly, applied via drag-select plus one icon click. |
| Parallel Grading – X axis | Gerber: Create/Edit Rules – Parallel X | Gerber depth | Keeps one of two lines meeting at a grade point parallel across sizes, varying only the X (sideways) measurement; user picks the point and the line's far end. |
| Parallel Grading – Y axis | Gerber: Create/Edit Rules – Parallel Y | Gerber depth | Keeps a line parallel across sizes varying only the Y (vertical) measurement, via selecting the point and the line's far end. |
| Parallel Grading – Extendable Length (Distance form) | Gerber: Create/Edit Rules – Parallel Ext | Gerber depth | Keeps a line parallel to the base-size line across all sizes while letting the operator set per-size growth/shrink amounts via a Distance Grading form. |
| Parallel Grading (offset lines/general) | Richpeace: Parallel grading · Richpeace: Parrallel grading | Richpeace depth | Creates offset parallel border/assistant lines per size (via box-select + Parallel Grade dialog with per-line distance input), keeping each size's shape parallel to the base — includes lingerie/collar use cases. |
| Intersection of Two Parallel Lines | Gerber: Create/Edit Rules – Intersect Parallel · Richpeace: Intersection of two parallel | Both (union) | Auto-computes X and Y grading for an internal/border line's endpoint so it stays parallel and correctly intersects the adjacent outer edge across sizes; single-click target-point operation. |
| Intersection Grading – X | Gerber: Create/Edit Rules – Intersection X | Gerber depth | Auto-computes only the X grading needed for an internal line's endpoint to meet the outer edge correctly, given a known Y distance. |
| Intersection Grading – Y | Gerber: Create/Edit Rules – Intersection Y | Gerber depth | Auto-computes only the Y grading needed for an internal line's endpoint to meet the outer edge correctly, given a known X distance. |
| Intersection Offset Grading | Gerber: Create/Edit Rules - Intersection Offset | Novel — Gerber | Computes X/Y grading for an internal line's endpoint so it meets the outer edge at a specified offset distance in every size, with configurable joined-endpoint behavior. |
| Specify Distance (Notch Travel Grading) | Gerber: Create/Edit Rules – Specify Distance | Novel — Gerber | Controls how far a notch travels along an edge per size via a Distance Grading form with growth values, referenced from a chosen endpoint. |
| Modify Grade Rules (section/grouping) | Gerber: Modify Grade Rules | Gerber depth | Organizational menu grouping for tools that edit/copy/extend existing grade rules rather than create new ones (structural, not a standalone action). |
| Change Grade Rule | Gerber: Modify Rule – Change Grd Rule | Gerber depth | Swaps the grade rule applied to selected point(s) for a different existing rule number from a saved rule table. |
| Add Grade Point (non-grading→grading conversion) | Gerber: Modify Rule – Add Grade Point | Gerber depth | Converts an existing non-grade point on a line into a grade point without altering the nested/graded shape; point chosen by click or entered value. |
| Copy Table Rule (force apply from library) | Gerber: Modify Rule - Copy Table Rule | Gerber depth | Applies a rule table's X/Y values onto a piece's point, overriding any mismatched existing rule values already on that point. |
| Copy Grade Rule (point to point, full XY) | Gerber: Modify Rule - Copy Grade Rule | Gerber depth | Copies an entire existing grade rule (X and Y) from one reference point to one or more target points on the same or different piece. |
| Copy X Rule | Gerber: Modify Rule – Copy X Rule | Gerber depth | Copies only the X-axis growth value from a reference grade point onto target point(s), leaving Y untouched. |
| Copy Y Rule | Gerber: Modify Rule – Copy Y Rule | Gerber depth | Copies only the Y-axis growth value from a reference grade point onto target point(s), leaving X untouched. |
| Copy Nest Rule (XY, post-transform) | Gerber: Modify Rule – Copy Nest Rule | Gerber depth | Copies both X and Y growth values as displayed on a stacked nest onto a new point, for use after flip/rotate/pivot or Z-attribute operations. |
| Copy Nest X | Gerber: Modify Rule – Copy Nest X | Gerber depth | Copies only nest-displayed X growth values onto a new point post-transform, leaving Y untouched. |
| Copy Nest Y | Gerber: Modify Rule – Copy Nest Y | Gerber depth | Copies only nest-displayed Y growth values onto a new point post-transform, leaving X untouched. |
| Flip/Negate X Rule | Gerber: Modify Rule – Flip X Rule · Richpeace: Neg X | Both (union) | Reverses the sign of the selected grade point's X-direction growth value (positive↔negative) on the base size. |
| Flip/Negate Y Rule | Gerber: Modify Rule – Flip Y Rule · Richpeace: Neg Y | Both (union) | Reverses the sign of the selected grade point's Y-direction growth value (positive↔negative) on the base size. |
| Negate XY Rule | Richpeace: Neg XY | Richpeace depth | Reverses the sign of both X and Y grading values of a selected point simultaneously in one operation. |
| Rotate Grade Direction 90° | Gerber: Modify Rule – Rotate 90 | Novel — Gerber | Rotates a grade point's growth direction 90° clockwise, swapping the X and Y growth components on the base size. |
| MicroMark Grading Types (intro/section) | Gerber: MicroMark Grading Types | Gerber depth | Section heading introducing MicroMark grading data-format methods; no standalone function. |
| Delta/MicroMark Grading Overview | Gerber: Working with MicroMark Grading | Gerber depth | Describes Delta grading (moving a point by set X/Y distance) as the default MicroMark method, framing the specialized grading types that follow. |
| Tangent Grading | Gerber: Tangent Grading | Novel — Gerber | Special single-value grading (vs. X/Y pair) for notches, keeping notch position and adjacent curve smoothness consistent across sizes. |
| Perpendicular Grading | Gerber: Perpendicular Grading | Novel — Gerber | Keeps a grade line perpendicular to an adjacent sloped/curved edge across sizes, preserving dart/seam angle relative to the curve. |
| Opposite Grading | Gerber: Opposite Grading | Novel — Gerber | Copies a grade rule's growth magnitude from another point but applies it in the mirrored/opposite X or Y direction, for symmetrical details. |
| Blend Grading | Gerber: Blend Grading | Novel — Gerber | Smooths growth-value transitions between two or more defined grade points so intermediate curve/line shape changes gradually across sizes. |
| Proportional Grading | Gerber: Proportional Grading · Richpeace: Proportion Grade · Richpeace: Two point proportion grade | Both (union) | Grades split/related sections or point pairs proportionally to each other rather than by independent fixed amounts; Richpeace variant adds margin-based (bedding) and two-point-reference proportional modes. |
| Paste Grading (full XY) | Gerber: Paste Grading · Richpeace: Paste grading | Both (union) | Carries over previously defined/copied grading values (X and Y) onto a merged piece or newly selected point(s), avoiding re-grading from scratch. |
| Paste Grading Value (to ungraded lines) | Richpeace: Paste grading value | Richpeace depth | Pastes previously copied grading values specifically onto grade line(s) that currently have no grading value assigned. |
| Paste X (X-only) | Richpeace: Paste X | Richpeace depth | Pastes only the copied X-direction (Dx) grading value onto selected grading point(s), leaving Y unaffected. |
| Paste Y (Y-only) | Richpeace: Paste Y | Richpeace depth | Pastes only the copied Y-direction (Dy) grading value onto selected grading point(s), leaving X unaffected. |
| Line Grading | Gerber: Line Grading · Richpeace: Line grade · Richpeace: Line grade table · Richpeace: Select line · Richpeace: Vertical line | Both (union) | Applies grade rules to whole lines (not just points) via a line-grade table: define horizontal/vertical/any-direction lines and a base point outside the pattern, assign per-size q1/q2/q3 values, then apply to grade the pattern. |
| Variation Grading (length variants) | Gerber: Variation Grading | Novel — Gerber | Generates length-based size variations (Longs, Shorts, XLongs) from a base size using Alternate Grade Reference lines, independent of standard size increments. |
| Grading of Binding (Expert Edition) | Gerber: Grading of Binding (Expert Edition Only) | Novel — Gerber | Auto-calculates binding-piece X grading from notch/endpoint distance growth between sizes; Y handled per separate rule. |
| Grading Point on a Curve (Key 7) | Richpeace: Grading Point on a Curve (Key 7) | Richpeace depth | Digitizer input function to place a grading point that carries its own value directly on a curve segment. |
| Grading Point on One Line (Key 1) | Richpeace: Grading Point on One Line (Key 1) | Richpeace depth | Digitizer input function to place a grading point constrained to lie on a straight line. |
| Middle Grading Point | Richpeace: Middle point | Richpeace depth | Inserts a grading point at the exact center of a grade line. |
| Point Grading (method) | Richpeace: Point Grading | Richpeace depth | General method of grading a pattern piece (e.g., sleeve, collar) by assigning individual X/Y grading values to discrete points. |
| Next Grading Point Navigation | Richpeace: Next Grading Point | Richpeace depth | Selects the next grading point in clockwise contour order relative to the current selection. |
| Previous Grading Point Navigation | Richpeace: Previous Grading Point | Richpeace depth | Selects the previous grading point in clockwise contour order relative to the current selection. |
| Rule/Grade Table Editing – Insert Row | Richpeace: Insert line | Richpeace depth | Inserts a new row into the grade rule table while in edit mode; requires explicit Save/Save As to persist. |
| Rule Grade Table (measurement/formula-driven) | Richpeace: Rule Grade Table · Gerber: Modify Rule – Change Grd Rule (table reference concept) | Both (union) | Grades points using values pulled from the Size & Measurement table or manually entered/formula-based (e.g., Bust/4) values, editable via right-click calculator on X/Y fields. |
| Open Grading Formula Editor | Richpeace: Open | Richpeace depth | Opens the formula editor for the selected grading point's current rule in the Rule Grade Table, applying edits on next Grade action. |
| X Equal to 0 | Richpeace: X Equal to 0 | Richpeace depth | Zeroes all X-direction grading values for the selected point(s) across sizes, eliminating X growth. |
| Y Equal to 0 | Richpeace: Y Equal to 0 | Richpeace depth | Zeroes all Y-direction grading values for the selected point(s) across sizes, eliminating Y growth. |
| X Equal Y | Richpeace: X Equal Y | Richpeace depth | Applies identical grading increments to both X and Y directions simultaneously for the selected point(s). |
| X Non-Equal Grading | Richpeace: X non equal grading | Richpeace depth | Allows distinct, per-size (non-uniform) X-direction grading values to be entered and applied for a selected point. |
| Y Non-Equal Grading | Richpeace: Y non equal grading | Richpeace depth | Allows distinct, per-size (non-uniform) Y-direction grading values to be entered and applied for a selected point. |
| X,Y Non-Equal Grading (combined) | Richpeace: X、Y non equal | Richpeace depth | Applies per-size grading values (uniform or non-uniform) for both X and Y directions together from the grade table in one action. |
| Group / Size-Table Display Toggle | Richpeace: Group · Richpeace: Only group basic size | Richpeace depth | Toggles size-table display between showing a full size group and a single base size only. |
| q1,q2,q3 Equalize Toggle | Richpeace: q1,q2,q3 all equal | Richpeace depth | When enabled, entering a value in one of the three line-grade value columns (q1/q2/q3) auto-fills the other two identically; disabling allows independent values. |
| Relative/Absolute Value Toggle | Richpeace: Relative /absolute value | Richpeace depth | Switches whether entered/displayed line (or point) grading values are interpreted as relative deltas or absolute measurements. |
| Set Square (parallel/perpendicular construction line) | Richpeace: Set square | Richpeace depth | Constructs a new line parallel or perpendicular to a reference line by clicking the reference line's ends then dragging to define the new line's direction. |
| Element Grading Enable/Disable ("setting") | Richpeace: setting | Richpeace depth | Marks whether a specific pattern element (notch, drill hole, etc.) is included in grading via a selection dialog. |
| Show/Hide Grade Line | Richpeace: Show or hide grade line | Richpeace depth | Toggles visibility of grade lines overlaid on the pattern piece. |
| Drill Size Assignment | Richpeace: Size | Richpeace depth | Dialog for specifying which sizes a drill hole applies to, by checking/unchecking each size individually. |
| Size Align (grading value alignment) | Richpeace: Size Align | Richpeace depth | Aligns grading values of points/lines to a reference point or line (horizontally, vertically, or restored to original) via click, with X/Y key modifiers forcing axis alignment. |
| View Grading Points Toggle (Ctrl+F) | Richpeace: View grading point | Richpeace depth | Keyboard toggle to show/hide all grading points on the pattern. |
| View Non-Grading Points Toggle (Ctrl+K) | Richpeace: View non grading point | Richpeace depth | Keyboard toggle to show/hide all non-grading points on the pattern. |



### Measurement & Spec Charts

Merging Gerber's 26-item measurement/spec toolset with Richpeace's 19 yields 22 distinct capabilities after collapsing clear naming overlaps (line length ↔ compare length, two-point distance ↔ distance 2 pt, angle ↔ protractor, point-count duplicates on the Gerber side, etc.). Depth target follows Gerber throughout for shared capabilities, with Richpeace's genuinely distinctive size-table/grading-data and notch-matching tools retained as novel additions since Gerber has no equivalent for them.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Piece Seam Allowance Display | Gerber: Piece - Seam Amounts | Gerber depth | Non-destructive on-screen display of assigned seam allowance per selected line/piece; clears and re-selects without altering geometry. |
| Total Piece Point Count | Gerber: Point - Total Piece Points · Gerber: Total Piece Points | Gerber depth | Reports total point count on a selected piece (boundary, internal lines, drill holes counted as 4 pts each, stripe/plaid lines) to flag proximity to system point limits (~4000 AccuMark / 256 MicroMark). |
| Perimeter Clipped/Unclipped Display Reference | Gerber: Perimeter Clipped/Unclipped Sample | Novel — Gerber | Visual toggle/reference showing seam lines trimmed to corner (Clipped) vs. extended past corner (Unclipped) so users can identify current display mode. |
| Clear Measurement Charts | Gerber: Clear Charts | Gerber depth | Closes and removes all open measurement charts (e.g., from Measure Line) from the work area without affecting underlying pattern data. |
| Compare Line Length Across Sizes | Gerber: Measure Line · Gerber: Working with Line Size Charts · Richpeace: Compare length · Richpeace: Compare Length Tool | Gerber depth | Generates a size-by-size chart (rows = sizes, columns = selected lines) of line lengths, supports summing/grouping lines (e.g., sleeve arc vs. armhole) and displays computed differences, with dispersion of the delta across multiple lines. |
| Notch/Point Path Matching & Comparison | Richpeace: Compare path work | Novel — Richpeace | Dialogue-driven tool for matching notches/points between two pattern paths, supporting fixed/stepped placement, offsets, single/double flipping, and automatic matching for seam alignment. |
| Overview / Measure Menu Summary | Gerber: Overview of Measure Menu | Gerber depth | Reference documentation summarizing available distance/length/angle/perimeter/area tools and support for a customizable measurement toolbar. |
| Line Length Measurement | Gerber: Line Length | Gerber depth | Measures length of one or more selected boundary or internal lines (across pieces if needed) and displays the result(s) on completion of selection. |
| Distance Between Two Lines | Gerber: Distance 2 Line | Gerber depth | Measures distance between two separate lines (possibly on different pieces) with selectable measurement mode: vertical, horizontal, perpendicular-to-grain, or parallel-to-grain. |
| Measure Along Piece Edge (Perimeter Between 2 Points) | Gerber: Perimeter 2 Pt/ Measure Along Piece | Gerber depth | Measures the along-boundary (non-straight) distance between two user-picked points on a piece's edge; highlights the segment and reports its length. |
| Straight-Line Distance Between Two Points | Gerber: Distance 2 Pt/ Measure Straight · Richpeace: Measure two point distance | Gerber depth | Measures straight-line distance between any two selected points (on boundary, internal, or grainline), with support for point-to-line and horizontal/vertical distance variants; supports repeated chained measurements. |
| Piece Perimeter Total | Gerber: Piece Perimeter | Gerber depth | Sums all boundary line lengths of one or more selected pieces and displays total perimeter centered on each piece. |
| Piece Area Calculation | Gerber: Piece Area | Gerber depth | Calculates and displays total surface area of selected piece(s), useful for fabric usage estimation and size comparison. |
| Angle Measurement | Gerber: Angle · Richpeace: Protractor | Gerber depth | Measures angle between two selected lines (degrees shown in input box); extended mode supports single-line horizontal/vertical angle, three-point angle, and Shift-modified two-point horizontal/vertical angle. |
| Clear All Measurements | Gerber: Clear Measurements | Gerber depth | Removes all measurement annotations/lines currently displayed from any Measure menu tool, resetting the work area display. |
| Style Spec Sheet / Measurement Template Builder | Gerber: Measure Specs (Expert Edition Only) | Gerber depth | Builds a cross-size spec sheet from a user-authored .mct measurement template listing named measurements, applied against an open graded style to auto-populate values per size. |
| Edit Size & Measurement Data | Richpeace: Edit Size &Measurement | Novel — Richpeace | Dialogue for entering/editing size names, per-part measurements, and size colors used to drive auto-grading; stores detailed size dataset per style. |
| Edit Size Table | Richpeace: Edit size table | Novel — Richpeace | Manages the size table: open/save tables, maintain size/part-name dictionaries, switch single vs. group size view, import size files, and calculate dispersions. |
| Cut/Replace Pattern (Forfex) | Richpeace: Forfex (with replace pattern dialogue) | Novel — Richpeace | Cuts a new sub-pattern from an existing piece by clicking along lines, then right-click dialogue to either create a new separate pattern or replace the original with the new one. |
| Record Measurement Variables | Richpeace: Measurement var | Novel — Richpeace | Stores/records named measurement variables per size and allows viewing/editing variable names and values via dialogue, feeding spec/grading calculations. |
| Fraction Precision Default Setting | Richpeace: No Denomination, Default is precision | Novel — Richpeace | Sets a default fraction denominator tied to chosen precision so decimal and fractional values (e.g., 10.3 ≈ 103/16 at 1/16 precision) are treated as equivalent throughout measurement displays. |
| Status Bar Toggle | Richpeace: Status bar | Novel — Richpeace | Simple UI toggle to show/hide the application status bar. |



### Piece Transformation

This category maps cleanly across both suites, with most Gerber piece-transformation tools (move, flip, rotate, mirror, split, fold) finding a direct Richpeace counterpart, confirming the audited near-parity (32 vs 26). The union yields roughly 34 distinct capabilities: a handful of Richpeace-only tools (Cut Apart, Equal Spread, Move & Rotate Adjust, Parallel Move, Proportion Adjust, Scale, Shrink-partial, Style Info, Symmetry-on-border, Fixed Path) are genuinely novel and folded in as-is, while Gerber's finer-grained Asymmetrical Fold sub-tools and position-management commands (Use/Define/Remove Position, Lock to Grid, Anchor) have no Richpeace equivalent and are kept at Gerber's depth. Naming and breakdown default to Gerber per instructions, with Richpeace terms merged into the source column wherever the underlying capability matches.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Cursor Shape Changes | Gerber: Cursor Shape Changes | Gerber depth | System changes on-screen cursor icon contextually to indicate current selectable/executable action (point pick, line pick, zoom, command mode). |
| Delete Pieces from Work Area | Gerber: Delete Pieces from Work Area · Richpeace: Delete selected Pattern | Both (union) | Removes one, several, or all pieces from the active work area/pattern list, with confirmation prompt; unsaved edits are lost unless piece was previously saved. |
| Delete Shadow | Richpeace: Delete shadow | Novel — Richpeace | Removes a previously generated shadow/reference copy attached to a pattern piece without affecting the piece itself. |
| Fold Keep | Gerber: Fold Keep | Gerber depth | Folds an unfolded mirrored piece back to half, or discards part of a piece's shape, using a selected internal fold line or two matched points; supports auto re-mirroring. |
| Combine/Merge Pieces | Gerber: Combine/Merge · Richpeace: Pattern jion | Both (union) | Joins two pieces into one along a shared/selected seam (straight two-point or curved join); retains first piece's grading rules, with options to update second piece's rules and the merged seam. |
| Shrink/Stretch (whole piece) | Gerber: Shrink/Stretch · Richpeace: Shrink, Increase/Decrease pattern | Both (union) | Resizes an entire piece up or down via linear measurement or percentage to compensate for fabric shrink/stretch; whole-pattern shrink can be driven by material weft/warp values. |
| Partial Shrink (line/border) | Richpeace: Shrink (partial mode) | Novel — Richpeace | Applies shrink/scale adjustment to a selected line or border segment rather than the entire piece. |
| Cut Apart / Expand with Divide | Richpeace: Cut Apart | Novel — Richpeace | Divides or expands a pattern along an operation line using non-spread/spread/divide line selections and a total expansion value, e.g., for big-bottom shirts or hem borders. |
| Equal Spread | Richpeace: Equal spread | Novel — Richpeace | Spreads/expands a pattern evenly between a designated non-spread line and spread line. |
| Modify Pieces (category) | Gerber: Modify Pieces, Modifying Pieces | Gerber depth | Umbrella menu/section grouping all piece position/orientation editing tools (move, flip, rotate, lock, anchor, etc.). |
| Move Piece | Gerber: Modify Piece - Move Piece · Richpeace: Move pattern | Both (union) | Relocates a piece by typed X/Y offset, grid snap, or reference-point matching to another piece; supports point-to-point overlap alignment. |
| Move Pattern to Design Position | Richpeace: Move pattern to design pos | Novel — Richpeace | Restores a repositioned pattern back to its original design-line location, individually or for all patterns at once. |
| All Patterns Down (load to work area) | Richpeace: All pattern down | Novel — Richpeace | Bulk-moves every pattern from the pattern list into the active work area in one step. |
| Hang Up Selected Pattern | Richpeace: Hang up select pattern | Novel — Richpeace | Sends a selected piece from the work area back into the pattern list (inverse of All Patterns Down/Move Piece into workspace). |
| Flip Piece | Gerber: Modify Piece - Flip Piece · Richpeace: Pattern flip | Both (union) | Mirrors a piece's orientation across a chosen line or the horizontal/vertical axis to produce an opposite-hand version; Richpeace toggles axis via Shift with confirmation if piece has distinct L/R sides. |
| Rotate Piece | Gerber: Modify Piece - Rotate Piece · Richpeace: Pattern rotate | Both (union) | Rotates a piece freely by drag, by typed angle, by fixed distance, or in fixed 90° increments; can auto-align a reference point/grainline to horizontal or vertical. |
| Set and Rotate/Lock (overlap two pieces) | Gerber: Modify Piece - Set and Rotate/Lock · Richpeace: Move and rotate, Move and Rotate Adjust | Both (union) | Aligns one piece onto another at matching reference point(s), then pivots/adjusts it for comparison or tracing, e.g., matching front/back armholes, seams, darts, collars. |
| Walk Pieces | Gerber: Modify Piece - Walk Pieces | Gerber depth | Simulates walking one piece's edge along another's to verify matching seam lengths/curves; user selects stationary and moving lines and a walk distance. |
| Use Position (saved layout) | Gerber: Modify Piece - Use Position | Gerber depth | Recalls a previously saved on-screen piece arrangement by name and auto-snaps pieces into that layout. |
| Define Position (save layout) | Gerber: Modify Piece - Define Position | Gerber depth | Saves the current arrangement of one or more pieces under a name (or auto-numbered) for later reuse via Use Position. |
| Remove Position | Gerber: Modify Piece - Remove Position | Gerber depth | Deletes a saved piece arrangement, for all positions of on-screen pieces, one named position, or a single piece within the group. |
| Realign Grain/Grade Reference | Gerber: Modify Piece - Realign Grain/Grade Ref | Gerber depth | Restores a piece to its original orientation or straightens its grainline/grade reference to the horizontal axis; can also adjust grading rules if "Modify Grade Rules" is enabled. |
| Lock to Grid | Gerber: Modify Piece - Lock to Grid | Gerber depth | Snaps a piece to on-screen grid lines, an exact X/Y coordinate, or a matching point on another piece for precise multi-piece positioning. |
| Anchor/Unanchor Piece | Gerber: Modify Piece - Anchor/Unanchor | Gerber depth | Locks a piece in place to prevent accidental dragging, and unlocks it again; locked pieces remain saveable/deletable. |
| Split Pieces (category) | Gerber: Split Pieces | Gerber depth | Section grouping all commands that divide a single piece into two or more pieces along a chosen line. |
| Split on Existing Line | Gerber: Split on Line · Richpeace: Divide pattern | Both (union) | Cuts a piece into two along an already-drawn internal/assistant line, e.g., for color-blocking; options to add resulting pieces to style, delete original, add seam allowance. |
| Split on Digitized Line | Gerber: Split on Digitized Line | Gerber depth | Splits a piece along a freehand/digitized line drawn by the user, with options to add to style, delete original, and add seam allowance. |
| Split Point to Point | Gerber: Split Point to Point | Gerber depth | Splits a piece along a straight line drawn between two user-selected points, with add-to-style/delete-original/seam-allowance options. |
| Split Horizontal | Gerber: Split Horizontal | Gerber depth | Splits a piece along a straight horizontal line from a selected start point, with the standard split options. |
| Split Vertical | Gerber: Split Vertical | Gerber depth | Splits a piece along a straight vertical line from a selected start point, with the standard split options. |
| Split Diagonal Left | Gerber: Split Diagonal Left | Gerber depth | Splits a piece along a diagonal cut angled left from a selected point, with the standard split options. |
| Split Diagonal Right | Gerber: Split Diagonal Right | Gerber depth | Splits a piece along a diagonal cut angled right from a selected point, with the standard split options. |
| Mirrored Pieces (category) | Gerber: Mirrored Pieces | Gerber depth | Section grouping tools for building and managing symmetrical (fold-on-center) pieces from a half-pattern. |
| Mirror Piece (build full from half) | Gerber: Mirror Piece · Richpeace: Mirror, Pattern symmetry | Both (union) | Generates the complete symmetric piece by reflecting a half-piece's shape/details across a selected mirror line/axis; Richpeace supports "relevant" (linked-edit) and "irrelevant" (independent) mirror modes, and copy vs. move via Shift. |
| Fold Mirror | Gerber: Fold Mirror | Gerber depth | Collapses a fully displayed mirrored piece back to its half view for editing, marking the fold with a dashed line. |
| Unfold Mirror / Open Mirror | Gerber: Unfold Mirror, Open Mirror | Gerber depth | Expands a folded mirrored piece to show both symmetric halves on screen; auto-refolds on save/reopen unless edited while unfolded. |
| Symmetry on Border 1/2 | Richpeace: Symmetry on 1 | Novel — Richpeace | Applies the same mirror/symmetry operation relative to a specified border (border 1 vs. border 2) as an alternate reference edge. |
| Asymmetrical Fold - Line Fold | Gerber: Asymm Fold - Line Fold | Gerber depth | Folds a piece along a selected internal line (e.g., grain/grade reference) and a chosen boundary edge to visually check symmetry/proportion. |
| Asymmetrical Fold - Line to Line Fold | Gerber: Asymm Fold - Line to Line Fold | Gerber depth | Folds a piece by matching two selected lines to each other, verifying equal length/alignment (e.g., pant crease check), drawing a dashed fold line. |
| Asymmetrical Fold - Match Points | Gerber: Asymm Fold - Match Points | Gerber depth | Folds a piece by matching a second selected point onto a fixed first point (e.g., aligning knee notches), redrawing the piece folded. |
| Asymmetrical Fold - Dart Fold | Gerber: Assym Fold - Dart Fold | Gerber depth | Folds a selected dart closed to preview the piece edge as it will appear once the dart is sewn, shifting fullness to the opposite side. |
| Asymmetrical Fold - Pleat Fold | Gerber: Asymm Fold - Pleat Fold | Gerber depth | Creates a pleat fold between two selected points, auto-computing the fold line at their midpoint; supports up to two pleat folds per piece. |
| Asymmetrical Fold - Perimeter Point Fold | Gerber: Asymm Fold - Perim Pt Fold | Gerber depth | Creates a fold line between two selected perimeter points and a chosen boundary section (e.g., a sleeve cuff fold), drawn as a dashed line. |
| Asymmetrical Fold - Unfold | Gerber: Asymm Fold - Unfold | Gerber depth | Removes any asymmetrical fold, restoring the piece to its original unfolded shape and deleting the system-drawn fold line(s). |
| Asymmetrical Fold - Unfold Keep | Gerber: Asymm Fold - Unfold Keep | Gerber depth | Reverses an asymmetrical fold like Unfold, but retains the internal fold line for future reference. |
| Alter Patterns (pivot-method fit alteration) | Gerber: Alter Patterns | Novel — Gerber | Applies fit/style alterations during initial tracing/digitizing using the pivot method (rotating around a fixed point) to reshape the pattern in one pass. |
| Parallel Move (line offset) | Richpeace: Parallel Move | Novel — Richpeace | Moves a selected line parallel to itself relative to the pattern by a signed distance value (positive lengthens, negative shortens). |
| Proportion Adjust | Richpeace: Proportion adjust | Novel — Richpeace | Proportionally drags one or more lines/control points and applies a numeric offset via a dialog, for proportional reshaping rather than uniform scale. |
| Rotate (design/assistant lines, rotate-copy) | Richpeace: Rotate | Novel — Richpeace | Rotates or rotate-copies a selected group of points/lines (not whole pattern pieces) around an axis point to a target position, defaulting to copy mode (Shift toggles to move-only). |
| Scale (line/pattern to target size) | Richpeace: Scale | Novel — Richpeace | Resizes a draft line or pattern to an appointed length or proportion by selecting reference points/lines and entering the target value. |
| Select Pattern Control Point | Richpeace: Select pattern control point | Novel — Richpeace | Selects whole patterns, border points, or assistant-line points (single/multiple, click/marquee/Ctrl+click) to enable subsequent parameter edits. |
| Style Info | Richpeace: Style info (S) | Novel — Richpeace | Stores and imports style metadata (name, comment, customer, order, picture path, material) per file, displayable on the grainline and exportable to the marker system. |
| Fixed Path (save-location lock) | Richpeace: Fixed path | Novel — Richpeace | When enabled, restricts all file saves to one designated path, prompting the user if they attempt to save elsewhere, to prevent lost files. |



### Text / Annotation

Gerber documents seven distinct capabilities in text_annotation versus Richpeace's four, so the merged catalogue is built to Gerber's depth per the audited comparison. Two clear overlaps emerge (annotation authoring, and show/hide annotation toggle), while Gerber contributes three novel capabilities (line naming, line-name copying, and stylus illustration) and Richpeace contributes two novel capabilities (image insertion and structured pattern-info editing) not present on the Gerber side. This yields nine total distinct rows covering all eleven source items.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Annotate Piece / Add Text | Gerber: Plot Text · Gerber: Annotate Piece · Richpeace: Text | Both (union) | Click or drag on a pattern/design line to place a text note; enter content in a dialog with configurable angle, height, font, and color, or set angle by dragging relative to a line; supports later edit, move, or delete, and text is included when the piece is plotted. |
| Show/Hide Annotations | Gerber: Hide Annotations · Richpeace: Display/Hide remark | Both (union) | Toggle command that shows or hides all text notes, remarks, and tool-generated measurement labels on a piece to reduce screen clutter, without deleting the underlying data; toggles back to fully visible on demand. |
| Clear Pattern Text | Richpeace: Clear text of pattern | Richpeace depth | Select a pattern and run Pattern > Clear text of pattern to bulk-remove text previously added with the Text tool, excluding grainline-associated pattern info; confirm via a selection dialog and OK. |
| Edit Line Names | Gerber: Modify Line - Edit Line Names | Novel — Gerber | Assign or rename an alphanumeric label (up to 10 characters) to a selected line on a pattern piece so downstream automated procedures and other functions can identify that line by name. |
| Copy Line Names | Gerber: Modify Line - Copy Line Names | Novel — Gerber | Copy line-name labels from one piece's lines to matching lines on another piece; internal lines are copied one at a time, while outer boundary lines can be copied individually or all at once, avoiding manual retyping. |
| Stylus Illustration Notes | Gerber: Note - Illustrate | Novel — Gerber | Freehand handwriting/drawing tool for adding sketched notes, diagrams, or construction illustrations directly on a piece using a stylus; saved with the piece for production viewing, with guidance to delete before final release. |
| Insert or Edit Image | Richpeace: Insert or Edit Image | Novel — Richpeace | Place a raster/embroidery-format image (BMP, JPG, GIF, PNG, TIF, DST, DSZ, DSB) onto a pattern by dragging a placement box, loading the file, and specifying length, width, vertex, and angle; resulting image object can be repositioned afterward. |
| Pattern Info Editor | Richpeace: Pattern info (P) | Novel — Richpeace | Structured dialog (double-click shortcut) for editing a selected pattern's metadata — name, comment, material, and copy/fold orientation (left/right) — with Apply to continue editing other patterns without closing the dialog. |
| Style Image Panel Toggle | Richpeace: Style image | Novel — Richpeace | Show/hide the style image reference panel used alongside the pattern workspace, independent of piece-level annotation visibility. |



### Digitizing & Scanning Input

Digitizing input in the merged catalogue centers on two parallel hardware paths — legacy digitizer-table/stylus tracing (Gerber's Silhouette table, Richpeace's digitizer board) and modern camera-based capture (Richpeace only) — plus a shared vocabulary of point-type markers (notch, drill, grainline, dart, grading point) that both systems implement via different input mechanisms. Per the depth guidance, camera/scan input and Richpeace's granular point-type/button-mapping model are built out fully, while Gerber's table-specific workflows (Reorient, Stream Sketch, worked examples) are retained as optional/legacy rows rather than expanded. Worked-example/tutorial entries from Gerber are folded into their underlying capability rows rather than kept as separate catalogue functions, since they don't represent distinct system capabilities.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Freehand sketch input | Gerber: Sketch · Gerber: Stream Sketch | Novel — Gerber | Draw new pattern lines in real time on a digitizer table with a pen/stylus, mirrored live on screen; supports a "hover" sub-mode (pen near but not touching surface) for tracing paths without marking the physical material. |
| Point-to-point line/curve digitizing | Gerber: Line - Curve · Richpeace: Input Pattern | Both (union) | Digitize an existing paper pattern by sequentially touching points along its border/internal lines with a stylus or digitizer mouse; system auto-generates straight or curved segments between points in a defined point order. |
| Digitizer table/board setup & calibration | Gerber: Working with Silhouette Table, Screen, and Pen · Gerber: Drafting on the Silhouette Table · Gerber: Using the Pen · Richpeace: Digitizer setup · Richpeace: Setup Menu | Richpeace depth | Configure and calibrate the input device: register digitizer model/size/comm port, map mouse/stylus button functions, define menu area by clicking reference corners, and calibrate precision by digitizing a known-size (e.g., 50cm×50cm) reference rectangle so table coordinates map exactly to screen coordinates. |
| Reorient/realign taped pattern | Gerber: Reorient | Novel — Gerber | Re-sync a physical pattern already taped to the table with its on-screen counterpart (needed after the paper shifts) by selecting two matching reference points on paper and screen. |
| Notch point input | Richpeace: Notch (Key 3) · Richpeace: Digitizer notch type | Richpeace depth | Mark a notch point on the pattern border via a dedicated input-device button; default notch reference type is configurable and applied by the pattern-reading function. |
| Drill hole input | Richpeace: Drill (Key 6) | Richpeace depth | Mark a drill/awl hole reference point on the pattern via a dedicated input-device button during digitizing. |
| Button hole input | Richpeace: Button Hole (Key 9) | Richpeace depth | Mark a button hole location on the pattern via a dedicated input-device button during digitizing. |
| Circle marking point input | Richpeace: Circle (Key 0) | Richpeace depth | Mark a circular reference point on the pattern via a dedicated input-device button during digitizing. |
| Grainline input | Richpeace: Grainline (Key D) | Richpeace depth | Input the pattern's fabric grainline direction via a dedicated input-device button during digitizing. |
| Dart/pleat input | Richpeace: Dart pleat | Richpeace depth | Digitize a dart or pleat by reading at least one border line; V-darts need no additional menu selection, and dart/pleat type is selected once and reused for subsequent same-type entries. |
| Assistant (internal) line input with parallel grading | Richpeace: Assist curve parallel grading | Richpeace depth | Digitize an internal/assistant line and grade it to stay parallel to and intersecting a chosen border line, by clicking the graded-side point, non-graded-side point, then the border line. |
| Non-grading curve point input | Richpeace: Non Grading Point on a Curve (Key 4) | Richpeace depth | Input a point along a curve that carries no independent grading value, via a dedicated input-device button. |
| Grading point input | Richpeace: Graded (Key E) | Richpeace depth | Mark a point as a graded point, stepping sequentially from the base size through all other sizes in the grade rule, via a dedicated input-device button. |
| Start new pattern piece read | Richpeace: Read New Pattern (Key B) | Richpeace depth | Clear the active digitizing session/dialogue and begin reading the next pattern piece, via a dedicated input-device button. |
| Close/finish current input | Richpeace: Close/Finish (Key 2) | Richpeace depth | Close the current line or finish the current input operation (e.g., completing a border, dart, or assistant line read), via a dedicated input-device button. |
| Undo last digitized input | Richpeace: Undo (Key C) | Richpeace depth | Revert the most recent point/line input action during digitizing, via a dedicated input-device button. |
| Digitizing capture & batch quantity settings | Richpeace: Pattern qty and capture | Richpeace depth | Set the capture-point pixel/dimension tolerance (recommended 5–15) that centers point-snapping on the touched location, and set how many pattern pieces will be digitized in the current batch. |
| Camera-based pattern capture | Richpeace: Camera Input | Novel — Richpeace | Digitize patterns by photographing them on a flat table against a printed grid background, using a fixed-rig camera (min. 3MP, remote-triggerable) per specified setup dimensions, as an alternative to stylus/board tracing. |
| Camera background calibration | Richpeace: Recognize Background | Novel — Richpeace | One-time calibration: photograph the empty grid background alone first, then photograph plain paper and finally the actual pattern on the same background for accurate camera-based digitizing. |
| Trace sloper/existing pattern as new design basis | Gerber: Design From Sloper | Gerber depth | Digitize a plotted/cut hard copy of an existing sloper by aligning it via Reorient and locking it in place (Anchor) so it can be used as the starting basis for a new design. |
| Digitize draped/fit-adjusted muslin as first pattern | Gerber: Create and Modify a First Pattern | Gerber depth | Trace a draped muslin or fabric mockup (including fit adjustments) into a digital first pattern using a non-marking stylus tip to avoid marring the material. |
| Digitize finished garment shape | Gerber: Copy an Assembled Garment | Gerber depth | Trace a flat, pinned-down section of an already-sewn garment (fabric up to ~3/8") with a non-marking stylus tip to reverse-engineer its pattern piece. |
| Trace decorative/trim placement guides onto pattern | Gerber: Add Designs to Patterns | Gerber depth | Digitize the outline of lace, appliqué, or beading placement guides onto an existing secured pattern piece, then convert the traced outline into a usable piece. |



### Import / Export & File Interchange

Given the scope constraint, this catalogue keeps only native piece open/save/manage functions from the Data Management Platform and single-piece DXF/AAMA-ASTM interop — bulk format translation, legacy migration engines, TIIP/AAMA batch converters, and general graphics/clip-art import stay out of scope per the suite architecture. Many Gerber "File menu" items are workspace/session management (New, Open, Close, Delete from Work Area) rather than true import/export, but are included since they define the native file lifecycle this app owns; several Richpeace items (Copy/Paste pattern, Pic lib, Unit file, Auto Design, grading-rule Delete/Delete line) are pattern-editing or library features, not import/export, and are excluded from this category's table entirely as out-of-category rather than out-of-scope. Bulk-format items (Export ASTM, Open AAMA/ASTM, Open TIIP) are narrowed to single-piece exchange per the depth guidance, not built as general translators.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| New Work Area | Gerber: New | Gerber depth | Ctrl+N opens a blank native work area for building pieces from scratch; multiple work areas may be open, newest becomes active. |
| Open Native File | Gerber: Open · Richpeace: Browse File · Richpeace: Preview · Richpeace: Latest used 5 file · Richpeace: Search File | Both (union) | Opens a native piece/model/style via the Data Management Platform API, with directory browsing (flagging entries lacking pattern data), thumbnail/comment preview, recent-file quick list, and keyword search-and-open. |
| Close Work Area | Gerber: Close | Gerber depth | Closes the active work area, prompting to save unsaved changes first; equivalent to clicking the work area's close button. |
| Close Style/Model | Gerber: Close Style/Model | Gerber depth | Closes a named style/model and unloads its pieces from the Piece/Icon menu and memory even while other work areas remain open, prompting to save unsaved changes. |
| Save Native File | Gerber: Save Pieces, Models, or Styles · Gerber: Saving Pieces, Models, or Styles · Gerber: Save - Current Model, Style, or Pieces · Richpeace: Save As | Both (union) | Saves the current piece/model/style to disk via the Data Management Platform API under its existing name (Ctrl+S), with an option to preserve piece screen position; first-time saves prompt for name/path; a file list lets the user pick which open items to save. |
| Save As / Save Copy | Gerber: Saving Pieces, Models, or Styles (save-as behavior) | Gerber depth | Saves the current piece/model/style under a new name or location without overwriting the original. |
| Save All Open Files | Gerber: Saving Pieces, Models, or Styles (save-all behavior) | Gerber depth | Saves every currently open piece/model/style in one action. |
| New File (native) | Richpeace: New | Richpeace depth | Ctrl+N creates a new native file; if unsaved changes exist in the work area, prompts Save As for the current file before proceeding. |
| Delete Piece from Work Area | Gerber: Delete Piece from Work Area | Gerber depth | Removes selected piece(s) from the on-screen work area only; disk copies are untouched but unsaved edits on those pieces are lost. |
| Piece to Menu | Gerber: Piece to Menu | Gerber depth | Sends a created/edited piece from the work area into the Piece/Icon library, prompting for a name if unsaved, then clears it from the work area. |
| Safety Restore | Richpeace: Safety restore | Novel — Richpeace | Recovers an unsaved file lost to a power outage/crash by selecting the auto-saved recovery copy from File > Safety restore; requires "Use Auto design" pre-enabled in System setup. |
| Import Single-Piece DXF/AAMA File | Gerber: Import (graphic/plot file import, narrowed to DXF/AAMA single-piece scope) · Richpeace: Open AAMA/ASTM Format file (narrowed to single-piece) | Both (union) | Imports one pattern piece in DXF or AAMA-ASTM format for interop with the marker-making/plotting step, with directory selection and file preview/thumbnail before import; general clip-art/plot-file import and bulk multi-piece batch translation are out of scope for this app. |
| Export Single-Piece DXF/AAMA File | Richpeace: Export ASTM file (narrowed to single-piece) | Novel — Richpeace | Converts the current single native piece to AAMA-ASTM (DXF) format for downstream marker-making/plotting, prompting for save path and filename; bulk/model-wide ASTM export is out of scope. |
| Export Plot File for Later Plotting | Richpeace: Export to file | Novel — Richpeace | Writes the current piece/pattern to a .PLT file on disk instead of sending directly to a plotter, so it can be opened and plotted later (e.g., from a plot queue) without the design app open. |
| Exit Application | Gerber: Exit | Gerber depth | Closes the application via the File menu command or (in legacy mode) the Escape key from a main menu context. |



### Plotting / Printing

Note: two items in the input list — "Cross isometry line" and "Cut on bias" and "Create Regular Sewing Template..." and "Select rotate Group" and "Creat shadow" and "Redo" — are pattern-drafting/grading tools unrelated to plotting/printing, and "Auto Arrange Patterns"/"Autoarrange pattern" are duplicate Richpeace entries; these are handled below per the merge rules (drafting tools excluded as out-of-category, duplicates merged).

Richpeace clearly out-documents Gerber on plot/print granularity (line-type/weight control, paper/orientation setup, calibration, measurement/pattern-info printing, remote plot routing) — the catalogue is built to Richpeace's depth throughout, with Gerber's job-submission/queue framing (job number tracking, sample-cut request) folded in as distinct, novel additions. Several Richpeace entries supplied ("Cross isometry line," "Cut on bias," "Create Regular Sewing Template," "Select rotate Group," "Creat shadow," "Redo") are drafting/grading operations, not plotting functions, and are therefore excluded from this plotting catalogue rather than force-merged; "Auto Adjust Patterns" and "Autoarrange pattern" are the same capability documented twice and are merged into one row.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Recent Files | Gerber: Recent File | Novel — Gerber | File menu submenu listing most-recently-opened files for one-click reopening. |
| Save As | Gerber: Save As | Novel — Gerber | Saves the current piece/model/style under a new name and chosen format without overwriting the original; prompts for target location, unique filename, and file type. |
| Printing (section) | Gerber: Printing (heading) | Novel — Gerber | Organizational grouping for standard paper-output commands (Print, Print Preview, Print Setup); implemented as a menu section, not a standalone action. |
| Print | Gerber: Print · Richpeace: Print measure table—Print · Print pattern info · Print style info | Richpeace depth | Sends selected content to a standard printer; supports distinct print targets — work-area pieces, measurement/size table, per-pattern info (name, comments, material, quantity, with all-patterns/selected/work-area-only scope), and style-level info (area, perimeter, per-size/material filters, list preview, Excel export). |
| Print Preview | Gerber: Print Preview · Richpeace: Print measure table—Preview | Richpeace depth | Renders a paged, zoomable preview of paper output prior to printing, covering both pattern-piece printouts and the measurement/size table. |
| Printer Setup | Gerber: Print Setup · Richpeace: Printer setup | Richpeace depth | Dialog to select target printer/default printer, paper size, and paper orientation (portrait/landscape) using system or app-native printer settings. |
| Auto-Fit Print Font Height | Richpeace: Auto Adjust font height for printing | Novel — Richpeace | Automatically rescales grade-label and measurement-variable font size when printing to a single sheet (e.g., A4) so text doesn't shrink illegibly; adjustable per current printer settings via a click action. |
| Plotting/Cutting (section) | Gerber: Plotting/Cutting (heading) | Novel — Gerber | Organizational grouping covering plot-to-plotter and send-to-cutter workflows; implemented as a menu section. |
| Plot | Gerber: Plot · Gerber: Plotting (process) · Richpeace: Plot · Setup | Richpeace depth | Submits arranged pieces to a plotter at real size (1:1) or user-defined scale; workflow includes arranging pieces within the plot border (directly or via a Plot Form showing usable width/length), selecting sizes/plotter, configuring plot parameters, and submitting — Gerber additionally returns a trackable job number on submission. |
| Plot Preview | Gerber: Plot Preview | Both (union) | Displays a pre-plot layout view of arranged pieces to check spacing/fit against material width before sending the job, avoiding wasted stock. |
| Plotter Setup / Default Plotter | Gerber: Plot Setup | Richpeace depth | Selects the active/default plotter for jobs; distinct from general plot-parameter configuration (paper size, line settings), which lives in the Plot Parameter panel. |
| Plot Scale | Richpeace: Plot scale | Novel — Richpeace | Lets the user specify a plotted-output-to-real-size ratio as an alternative to default 1:1 plotting. |
| Plot Parameter Panel | Richpeace: Plot parameter · Line width · Assistant line · Outside border | Novel — Richpeace | Central options panel controlling plot line rendering: line width/point size for the inkjet plotter, line-type assignment for construction ("assistant") lines vs. the outside border, and spacing for dashed/dash-dot line styles. |
| Design Line Plot Mode | Richpeace: Design line | Novel — Richpeace | Plot filter that includes unfinalized draft/construction lines in the output, for reviewing work-in-progress patterns. |
| Pattern-Only Plot Mode | Richpeace: Pattern | Novel — Richpeace | Plot filter that outputs only finished pattern outlines, suppressing draft/design lines. |
| Overlap Plot Mode | Richpeace: Overlap | Novel — Richpeace | Plots multiple graded sizes superimposed on the same output sheet rather than laid out separately, for compact comparison printing. |
| Paper Size Setup | Richpeace: Paper size | Novel — Richpeace | Selects plot paper size from a preset list or defines a custom width/length for plotter output. |
| Plot Orientation | Richpeace: Portrait/Landscape | Novel — Richpeace | Sets plotted output orientation to portrait or landscape independent of printer-orientation setting. |
| Plot Size Calibration (Error Correction) | Richpeace: Error | Novel — Richpeace | Password-protected calibration tool: user plots a 1m×1m test rectangle, enters the actual measured width/height, and the system computes a correction factor to fix systematic plot-size inaccuracy. |
| Cut Length | Richpeace: Cut length | Novel — Richpeace | Sets the material length fed/cut per single cutting pass on connected cutting hardware. |
| Networked Plot Data Path | Richpeace: Work Data Path | Novel — Richpeace | Specifies the plot-center data path of the machine physically attached to the plotter, so networked computers without a direct connection can route plot jobs to it. |
| Auto-Arrange Patterns for Plotting | Richpeace: Auto Arrange Patterns · Autoarrange pattern | Novel — Richpeace | Automatically lays out all work-area patterns to fit paper/plot width, with an option to exclude specific sizes from arrangement, prior to plotting. |
| Submit Cutter Sample Request | Gerber: Submit Sample Request | Novel — Gerber | Sends selected work-area pieces to a connected cutting machine to cut a physical fabric sample, for prototyping/approval ahead of full production. |



### Customization, Preferences & Workspace Setup

**Part 1 of 2:**

Gerber's manual overwhelmingly dominates this category with a granular, tab-by-tab preferences system (piece display, selection/tracking, colors, plotter, style conversion, paths) plus full screen-layout/toolbar customization infrastructure, while Richpeace contributes mostly discrete UI toggles (toolbar visibility, color/line setup, units, language, pattern lock) and a handful of genuinely novel drafting/utility tools with no Gerber equivalent. The AccuMark/MicroMark legacy-menu-compatibility items are retained but flagged as deferred/optional per the depth guidance. Build depth follows Gerber for all workspace/preferences/toolbar granularity; Richpeace-only items are folded in at their native depth or marked novel where they add real distinct capability (3PARC, custom curve save/reuse, dart/pleat digitizer key, assist-curve notch logic, fixed length for cutting).

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Interactive workspace tour | Gerber: Get Acquainted with the Work Space | Novel — Gerber | Hover-triggered tooltip/label overlay identifying every menu, toolbar, and panel region for onboarding new users. |
| Menu bar | Gerber: Menu Bar | Gerber depth | Top-level row of drop-down menus (File, Edit, View, Point, Line, Piece, Grade, Measure, Draft, Window, Help) exposing every command in the system. |
| Main tool bar | Gerber: Tool Bar | Gerber depth | Icon-button strip grouped by task (Point, Line, Piece, Grade, Measure, Draft) for one-click access to frequent commands; user-configurable per Custom Toolbars. |
| Legacy AccuMark menu mode (deferred) | Gerber: Using the AccuMark Menu | Novel — Gerber (deferred/optional) | Toggleable classic AccuMark-style floating menu layout for migration familiarity; low priority, not required for initial build. |
| Legacy MicroMark menu mode (deferred) | Gerber: Using the MicroMark Menu | Novel — Gerber (deferred/optional) | Toggleable classic MicroMark-style menu with added Exit/Exit-to-Main buttons; low priority, not required for initial build. |
| Legacy MicroMark function-key bar (deferred) | Gerber: MicroMark Function Keys | Novel — Gerber (deferred/optional) | On-screen F-key shortcut row mapped to legacy MicroMark commands lacking toolbar icons; optional migration aid. |
| Legacy MicroMark quick-menu toolbar (deferred) | Gerber: MicroMark Tool Bar | Novel — Gerber (deferred/optional) | Icon shortcuts opening legacy MicroMark Points/Lines/Pieces/Grading/Seams sub-menus directly; optional migration aid. |
| Piece/icon panel | Gerber: Piece/Icon Menu · Gerber: Working with Piece/Icon Menu · Richpeace: Pattern listbox | Both (union) | Dockable, repositionable panel listing all pattern pieces as icons/names/both, with right-click for piece details or an options pop-up; supports quick selection and management. |
| User input/prompt box | Gerber: User Input Box · Gerber: Options Input Section · Gerber: User Input Command/Prompt Section · Gerber: User Input Controls Section · Gerber: Value Input Section · Gerber: Prompt Bar | Gerber depth | Multi-section interactive command dialog showing current instruction/prompt, command-specific options (radio/checkbox/value pick), numeric value vs. cursor-tracking input mode, and OK/Cancel/Tracking controls; configurable to show always or only during commands. |
| Status bar | Gerber: Status Bar | Gerber depth | Standard toggleable, repositionable Windows-style bar showing system status at screen edge. |
| Info bar | Gerber: Info Bar | Gerber depth | Context strip showing current style/piece name, size, Sew/Cut line mode, and unit system (inches/metric). |
| Quick Open file search | Gerber: Quick Open | Novel — Gerber | Type-ahead field to open a model/style/piece by exact name, filtered by file types configured in Preferences General page. |
| On-screen rulers | Gerber: Rulers | Gerber depth | Horizontal/vertical measuring guides along work-area edges, unit display following system inch/metric setting. |
| Workspace customization overview | Gerber: Customizing Pattern Design Work Space · Gerber: Use Screen Layout · Gerber: Overview of Customizing with Screen Layout | Gerber depth | Umbrella capability letting users reposition menus/toolbars, add tool-bar buttons, and set default colors via the Preferences/Options and Screen Layout dialogs. |
| Multi-window work area management | Gerber: Open, Close, and Arrange Work Areas | Gerber depth | Open multiple patterns/models/styles simultaneously in separate resizable/arrangeable windows, with one active at a time. |
| Piece display view options | Gerber: Display Pieces in the Work Area | Both (union) | View-menu toggles for outlines/symbols, solid fill, orientation symbols, seam lines, notes, and forced screen refresh to current piece state. |
| Toolbar/menu docking | Gerber: Docking Tool Bars, Menus, and User Input Box | Gerber depth | Drag-to-dock or float toolbars, menus, function keys, and the User Input box at screen edges; layout persists across sessions. |
| Preferences/Options system (entry point) | Gerber: Use Preferences/Options · Gerber: Preferences/Options | Gerber depth | Central tabbed settings dialog (General, Color, Plotter, Style, Paths, Draft) accessed from the View menu, governing display, behavior, and connectivity settings. |
| Draft/digitizer preferences | Gerber: Setting Draft Preferences/Options | Gerber depth | Digitizing-table setup tab controlling Point Filter (extra-point removal sensitivity) and Sketch/Note Pen Resolution (points recorded while tracing). |
| General preferences page | Gerber: General Page · Gerber: Setting General Preferences/Options | Gerber depth | Tab consolidating everyday settings (piece display, selection sensitivity, workspace behavior) with Save (applies globally) and Reset actions. |
| Piece display preferences | Gerber: Changing Preferences/Options for Piece Display | Gerber depth | Checkboxes for Filled Pieces (solid color fill), Symbols (point/grade-rule markers), and Fit Pieces in Work Area (auto-scale to view). |
| Selection & tracking preferences | Gerber: Changing Preferences/Options for Piece Selection and Tracking | Gerber depth | Magnetic Tolerance (click-grab radius) and Auto Tracking (automatic line-following on cursor proximity) settings. |
| Workspace/backup preferences | Gerber: Changing Preferences/Options for Work Space and Misc. | Gerber depth | AutoSave Timer (periodic crash-recovery backup interval) and AutoSave Undo Buffer (persist undo history) settings. |
| Color preferences page | Gerber: Color Page · Gerber: Setting Color Preferences/Options | Both (union) | Tab/dialog for configuring on-screen colors for pieces, grading sizes, text, and backgrounds. |
| Piece status colors | Gerber: Changing Piece Colors | Gerber depth | Distinct colors for Original, Highlighted, and Modified piece states to visually track edit status. |
| Nest/grading colors | Gerber: Changing Nest Colors | Gerber depth | Colors for nested-size views: Base (sample size), Intermediate (in-between sizes), and Breaks (size extremes). |
| Text & background colors | Gerber: Changing Text and Miscellaneous Colors | Gerber depth | Colors for Prompt text, Annotation (labels/point/rule numbers), Work Area background, and Grid lines. |
| Design/assistant line color setup | Richpeace: Colour setup | Richpeace depth | Sets or changes the draw color for new or selected design/assistant lines via pull-down palette and select-to-recolor operation. |
| Interface element color setup | Richpeace: Color Setup | Both (union) | Configures colors for the pattern list box, working-area background, prompt/measure/remark text, selected/unselected pattern colors, fill/scan/grid colors, and size colors. |
| Plotter preferences page | Gerber: Plotter Page · Gerber: Setting Plotter Preferences/Options | Gerber depth | Tab for configuring general and cut-specific plotter output defaults, accessed via View > Preferences/Options > Plotter. |
| Plotter default behavior | Gerber: Changing Plotter Defaults | Gerber depth | Sets default Piece Plot Parameter Table, Annotation Table, Stacking (multi-piece paper-width packing) behavior, and Plot flags. |
| Cut parameter overrides | Gerber: Changing Cut Parameter Overrides | Gerber depth | Fine-tunes oak-tag cutting-plotter settings: Cut Line Length, Tab Line Length, and related perforation/gap parameters. |
| Plot at actual size | Richpeace: Actual | Richpeace depth | Plot option outputting pattern pieces at true 1:1 scale. |
| Fixed length for cutting alignment | Richpeace: Fixed length | Novel — Richpeace | Sets a fixed reference length to keep the pattern aligned/consistent with the paper feed during plot/cut. |
| Style conversion preferences page | Gerber: Style Page · Gerber: Setting Style Preferences/Options | Gerber depth | Tab governing AccuMark↔MicroMark style conversion rules: naming, notches, grain/grading reference lines. |
| Piece naming conversion rules | Gerber: Changing Preferences/Options for Naming Styles | Gerber depth | Controls automatic piece-name adjustment (e.g., Retrieve Style/Prefix Style Name) when converting between per-piece and grouped naming schemes. |
| Grain line export rule | Gerber: Changing Preferences/Options for Exporting Grain Line | Gerber depth | Auto-generates a grain/grade reference line on export based on the original grain line, avoiding manual redraw. |
| Notch-type conversion mapping | Gerber: Changing Style Preferences/Options for Notches | Gerber depth | Maps notch type definitions between two differing notch-numbering systems during data conversion. |
| Paths preferences page | Gerber: Paths Page · Gerber: Setting Paths Preferences/Options | Gerber depth | Tab for setting where piece, style, model, and import files are located/stored across environments. |
| Storage area path settings | Gerber: Changing Paths for Storage Areas | Gerber depth | Configures Device, Storage Area, and Environment locations for primary pattern-data storage. |
| Style path settings | Gerber: Changing Paths for Styles | Gerber depth | Configures Device, Style Path, and Grade Path locations for style and grading-rule-table storage. |
| Import file path settings | Gerber: Changing Paths for Import Files | Gerber depth | Configures Device and Path for locating/saving externally imported graphic files. |
| Screen Layout dialog | Gerber: Screen Layout | Gerber depth | Central dialog toggling visibility of menus, toolbars, and status bars, plus guideline/snap settings; Apply/OK persists layout. |
| Display guidelines/grid | Gerber: Display Guidelines | Gerber depth | On-screen alignment grid with selectable style (None/Lines/Dots/Crosshairs) and configurable spacing. |
| Snap settings | Gerber: Snap to Grid, Geometry, or Precision | Gerber depth | Cursor snapping to grid guidelines, geometry (piece edges/points), or precision targets, independently toggleable. |
| Keyboard layout selection | Gerber: Keyboard | Gerber depth | Selects the shortcut-key layout style used by the system, set via Screen Layout. |
| Custom toolbars | Gerber: Use Custom Toolbars · Gerber: Custom Toolbars · Richpeace: Design toolbar · Richpeace: Grading toolbar | Both (union) | Add/remove buttons on standard toolbars or build new custom toolbars; individually toggle module-specific bars (e.g., Design, Grading) on/off. |
| Pattern assist curve display toggle | Richpeace: Pattern assist curve | Richpeace depth | Toggles visibility of assistant/construction curves on pieces. |
| Fill pattern toggle | Richpeace: Fill pattern | Richpeace depth | Toggle (Ctrl+J) to render selected pieces with solid color fill versus outline-only. |
| Isolate single piece (focus lock) | Richpeace: Only display one piece | Novel — Richpeace | Locks display/editing to one selected piece full-screen, hiding/protecting all others from accidental edits; toggle to release. |
| Line thickness & smoothing | Richpeace: Line thickness | Richpeace depth | Slider control for design/border/assistant line display thickness, plus a smooth-curve rendering toggle to reduce jagged edges. |
| Line type/style setup | Richpeace: Line type | Richpeace depth | Sets line style for new or selected design/assistant lines via pull-down, including dash length and gap distance parameters. |
| Length unit & precision setup | Richpeace: Length unit · Richpeace: Inch fraction format | Richpeace depth | Sets measurement unit (cm/mm/inch) and display precision; for inch, additionally choose fraction vs. decimal display format. |
| Interface language selection | Richpeace: Language | Novel — Richpeace | Selects UI display language, also controlling text used in printed pattern/global info outputs. |
| Size/part name dictionary | Richpeace: Dictionary | Novel — Richpeace | Stores and sorts size names and part names into a reusable, sorted pick-list for consistent naming. |
| Exit application | Richpeace: EXIT | Richpeace depth | Closes and exits the software system. |
| Three-point arc/circle tool | Richpeace: 3PARC | Novel — Richpeace | Draws an arc or circle through three clicked points for design/assistant lines; Shift toggles between arc and full-circle mode. |
| Multi-line extend/align to target(s) | Richpeace: Curve aline | Novel — Richpeace | Extends multiple selected lines to align with one (one-way) or two (two-way) target lines via select-then-confirm workflow. |
| Custom curve save & reuse | Richpeace: Custom curve · Richpeace: Custom Curve (User-defined curve properties) | Novel — Richpeace | Saves a user-drawn curve shape (e.g., star, triangle) as a reusable named tool, with editable properties (Height, Gap, Adaptive Stretch, Count/Gap for repeats). |
| Dart/Pleat digitizer input key | Richpeace: Dart/Pleat (Key 5) | Novel — Richpeace | Dedicated digitizer-mouse button mapped to sequential dart/pleat point entry (first point, waist point, tip point, end point). |
| Assistant-curve-driven notch placement | Richpeace: Assistant curve notch | Novel — Richpeace | Adds a border notch at the point an assistant line references; side/direction of the assistant line and click position (one side vs. center) determine which border(s) get notched. |

**Part 2 of 2:**

This part-2 slice covers workspace/view toggles, preferences, keyboard/mouse interaction modes, style/piece description setup, and add-on tooling. Overlap between the two systems is modest — mostly around toolbar customization, zoom/view commands, point/line display toggles, and general system/UI preferences — while Gerber contributes far more granularity (input modes, tracking setup, zoom variants, style/piece description sub-pages, legacy AccuMark/MicroMark compatibility) and Richpeace contributes a handful of novel UI/display toggles (theme sets, demo playback, shadow/assist-line visibility, auto-save interval). Per depth guidance, preference/toolbar/view-option granularity builds to Gerber's level, and the AccuMark/MicroMark legacy-menu-compatibility items are flagged as deferred/optional rather than required.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Custom toolbars & buttons | Gerber: Add or Delete Tool Bar and Buttons · Richpeace: Toolbar, Pattern toolbar | Both (union) | Let users show/hide, build, or resize toolbars and add/remove command buttons per category; persist per-user layout. |
| Piece/Icon menu display & management | Gerber: Displaying the Piece/Icon Menu, Deleting Pieces from the Piece/Icon Menu · Richpeace: Patternlist box | Gerber depth | Dockable panel listing all pieces (icon/name/both), sortable/resizable, with delete-one/several/all; deleting from a MicroMark-linked style removes the underlying piece, not just the icon. |
| AccuMark/MicroMark system setup | Gerber: Setup for AccuMark or MicroMark Grading/Marking System, Set Preferences for Environment and Paths | Novel — Gerber (deferred) | Configure environment mode (AccuMark vs MicroMark) and file paths for legacy-compatible marker/model workflows; optional migration aid, not a required build item. |
| AccuMark/MicroMark workspace tutor | Gerber: Customize Work Space for AccuMark, Customize Work Space for MicroMark | Novel — Gerber (deferred) | Interactive hover-help overlay teaching legacy-trained operators the AccuMark/MicroMark screen layout equivalents; low-priority migration aid, defer. |
| Piece geometry model | Gerber: Piece Geometry | Novel — Gerber | Defines the internal building blocks (lines, points, specific point locations) of a pattern piece that all selection/editing/tracking operations act on. |
| Geometry status colors | Gerber: Geometry Colors | Gerber depth | Configurable color coding by line/point state (unmodified, highlighted, selected, unsaved edit) with live-update behavior. |
| Move / remove piece in work area | Gerber: Moving Pieces in Work Area | Novel — Gerber | Click-drag-drop repositioning of a piece within the work area; separate command to delete a piece from the work area (not the style). |
| Multi-window work area management | Gerber: Arranging Multiple Work Areas | Novel — Gerber | Switch, minimize, maximize, cascade, or close multiple open pattern windows via title bar or Window menu list. |
| Keyboard shortcut system (Quick/Hot/Function/Short/Keyboard keys) | Gerber: Quick Keys, Short Cuts, Function Keys, Hot Keys, Keyboard Keys | Gerber depth | Unified shortcut layer: Alt+underlined-letter menu shortcuts, dedicated Alt+function-key hotkeys, F-keys for view/redraw actions, and standard Enter/Escape/Shift key behaviors for confirming, canceling, and multi-selecting. |
| Cursor vs Value input mode | Gerber: Work in Cursor and Value Modes, Changing between Input Modes, Work in Value/Cursor Mode, Working in Cursor Mode, Working in Value Mode | Novel — Gerber | Toggleable editing mode where geometry is adjusted by mouse-drag (Cursor) or by typed numeric entry in a Value Input box (Value); switch via a mode button or combined mouse-button press. |
| User Input box (command prompt panel) | Gerber: Getting Acquainted with User Input Box | Novel — Gerber | Dockable/floating panel showing context-sensitive step prompts and numeric entry fields driven by the active command. |
| Options pop-up (right-click contextual) menu | Gerber: Options Pop-up Menus, Options Pop-up Menu, Using Options Pop-up Menus for Commands, Options for Making Selections in Commands, Options for Point Location | Gerber depth | Context-sensitive right-click menu offering OK/Cancel/Select All/Clear and step-specific point-placement options, changing contents based on the current command and prompt. |
| End multi-select / confirm command step | Gerber: Ending Selection to Continue | Novel — Gerber | Right-click-and-choose-OK (or double-click) gesture used to terminate a multi-item selection and advance the active command. |
| Style Description — style-level page | Gerber: Using the Style Description Page | Novel — Gerber | Editable tab of style-level metadata (style info, sample size) set once per style. |
| Style Description — piece-level page | Gerber: Using the Piece Description Page | Novel — Gerber | Per-piece metadata tab within Style Description, selectable via icon slider or dropdown, for entering piece-specific defaults. |
| Cutter's Must list generation | Gerber: Using the Cutter's Must Page | Novel — Gerber | Generates a printable text file of piece names/quantities/messages for the cutting room from Style Description data. |
| Style revision history | Gerber: Checking Style History | Novel — Gerber | Read-only log of previous/last revision dates, creation date, and creator User ID for a style. |
| Piece blocking settings (plaid/stripe alignment) | Gerber: Setting Piece Blocking for Style Description | Novel — Gerber | Primary/Secondary X & Y blocking values (percent of repeat or fixed measurement) controlling piece alignment to plaid/striped fabric during marker making. |
| Piece identification info (name/message/type/quantities) | Gerber: Setting Piece Information for Style Description, Edit Piece Info | Novel — Gerber | Editable core piece record: name (≤10 chars, no spaces), print message, Normal/Standard type, unflipped/opposite quantities, category, grade rule table link, and file/style path lookup. |
| Piece marker-making restrictions | Gerber: Setting Piece Restrictions for Style Description | Novel — Gerber | Per-piece constraints for automatic marker placement: CW/CCW tilt limits, forced bias angle, and nap-matching enforcement across same-size pieces. |
| Tracking mode setup (General Preferences) | Gerber: Setting Up for Tracking | Novel — Gerber | Preferences page toggles (Auto Tracking, Show Point Info) enabling click-through navigation of points/lines/pieces before editing. |
| Tracking-based selection/edit | Gerber: Use Tracking to Edit | Novel — Gerber | Sequential step-through selection of points/lines/pieces using Auto Tracking and info popups to drive edits. |
| View menu overview (display toggles, non-destructive) | Gerber: Overview of View Menu | Gerber depth | Umbrella set of display-only controls (zoom, names, seam allowances, grading info) that never alter underlying pattern data and are generally not undoable. |
| Refresh/redraw display | Gerber: Refresh Display | Both (union) | Forces a screen redraw to clear stray on-screen marks without touching pattern data. |
| Zoom command set (in/out/full-scale/selected/1:1/separate) | Gerber: Using Zoom Commands, Use Zoom Commands, Zoom In, Zoom Out, Zoom - Full Scale, Zoom to Selected, Zoom - 1:1, Zoom - Separate Pieces · Richpeace: Zoom in | Gerber depth | Full magnification toolset: marquee zoom-in, step-back zoom-out, fit-all-to-screen, fit-selection-to-screen, true 1:1 scale, and auto-separate/spread overlapping pieces at full scale; each bound to a dedicated key (F1–F8) or shortcut gesture. |
| Point display/verification submenu | Gerber: Verify Points | Gerber depth | Grouping header for point-inspection commands (all points, intermediate points, numbers, grade rules, notches, attributes). |
| Show all points | Gerber: Point - All Points | Gerber depth | Displays every point type (intermediate, grade, smoothing, end) on selected piece(s) simultaneously. |
| Show intermediate points | Gerber: Point - Intermediate Points | Gerber depth | Displays only non-corner/non-endpoint points as squares, for isolating a specific point to edit. |
| Line display info | Gerber: View Lines | Gerber depth | Grouping header for line-related display commands such as showing line numbers. |
| Show/hide design (draft) lines | Richpeace: Show/Hide design line | Novel — Richpeace | Toggle visibility of underlying design/draft lines on a pattern piece. |
| Show/hide seam line | Richpeace: View seam line | Novel — Richpeace | F7 toggle to show/hide the seam allowance line on a pattern. |
| Show/hide finished pattern | Richpeace: View Pattern | Novel — Richpeace | Toggle visibility of the finished (as-cut) pattern outline. |
| Show/hide pattern shadow | Richpeace: Show or hide shadow | Novel — Richpeace | Toggle a shadow overlay behind the pattern piece for visual reference. |
| Show/hide assistant lines | Richpeace: Show/Hide assistant line | Novel — Richpeace | Ctrl+U toggle for construction/assistant line visibility. |
| Show/hide temporary pattern assist curves | Richpeace: Pattern temp assist curve | Novel — Richpeace | Toggle display of temporary assist curves generated during pattern drafting. |
| Bring in matching pattern pieces by name/material | Richpeace: View same material pattern | Novel — Richpeace | Pulls pieces into the work area filtered by pattern name or material, with whole-word-match and base-material/copy inclusion options. |
| Point display size | Richpeace: Point size | Novel — Richpeace | Sets on-screen point size, also used as the reference scale when measuring distances. |
| Note/Sketch pen point resolution | Gerber: Note Pen Resolution, Sketch Pen Resolution | Gerber depth | Sets spacing (default one point per 0.1 in/0.25 cm) of auto-placed points along freehand Note/Illustrate or Sketch lines; lower spacing = smoother, heavier line data. |
| Draft/table display scale calibration | Gerber: Draft Scale | Novel — Gerber | Calibrates on-screen scale to match the physical digitizing/Silhouette table surface for accurate sketch/reorient correspondence. |
| Undo-last-stroke eraser | Gerber: Using the Eraser | Novel — Gerber | On-screen "E" button that removes the most recent sketch line or placed point in reverse order while in Sketch/Note/Line-Curve commands. |
| Recommended drafting preference defaults | Gerber: Hints on Setting Preferences/Options | Gerber depth | Guidance/preset bundle (Display Symbols on, Display Internals dashed, default view = Full Scale) for optimal piece-drafting display. |
| Advanced production add-on toolset | Gerber: Expert Edition | Novel — Gerber | Optional package adding multi-piece fullness edits, curve reshaping, armhole/sleevecap updates, spec sheets, and binding creation. |
| Play tool operation demo | Richpeace: Play demo | Novel — Richpeace | Selecting this then clicking any tool plays a short video demonstrating that tool's operation. |
| Ruler bar display toggle | Richpeace: Ruler bar | Both (union) | Shows/hides the on-screen ruler bar. |
| Auto-save interval configuration | Richpeace: Save interval, Use Auto save | Both (union) | Enables automatic saving and sets the time interval between auto-saves. |
| Physical screen size calibration | Richpeace: Screen size | Both (union) | Enter true monitor/screen physical dimensions so patterns render at accurate 1:1 scale. |
| System setup dialog (multi-card preferences) | Richpeace: System setup | Both (union) | Central preferences dialog with eight configuration cards for system-wide parameters; changes require clicking Apply per card. |
| Interface theme presets | Richpeace: Theme | Both (union) | Save, select, or delete named UI themes controlling which tools/buttons are visible; managed via right-click menu. |
| UI setup panel (list position, language, line weight, theme) | Richpeace: UI Setup | Both (union) | Consolidated settings panel for pattern-list-box position, screen size, display language, on-screen line thickness, and active theme. |
| Split shared drill/buttonhole for independent grading | Richpeace: Split (drill, buttonhole) | Novel — Richpeace | Breaks a linked group of drill holes/buttonholes so each can be graded independently instead of moving together. |
| Drill strip-number assignment | Richpeace: Strip Info | Novel — Richpeace | Attribute field assigning a strip number to a drill, auto-applied when a marker is generated. |
| Compare-length display format (decimal + fraction) | Richpeace: View exact values a compare length dialogue when use inch fraction format | Novel — Richpeace | Toggle whether the length-comparison dialogue shows decimal and fraction values together or fraction only. |



### Automation (Macros, Templates, Batch)

This category's overlap is minimal: Gerber and Richpeace share only the Undo capability, while everything else is distinct to one side. Per the depth guidance, template/motif save-and-reuse and sewing-order automation are built out to Richpeace's fuller documented depth, and Gerber's macro record/replay is implemented as a separate novel capability despite being underdocumented in its own manual. No input item is merged away except the genuine Undo duplicate.

| Function (canonical name) | Source function(s) | Build target | Description / behavior |
|---|---|---|---|
| Undo | Gerber: Undo · Richpeace: Undo | Both (union) | Reverts the most recent action; repeatable to step backward through multiple prior operations one at a time, via icon, Ctrl+Z, or menu, with the control visibly disabled when no history remains. |
| Prefix Names on Piece Add | Gerber: Prefix Names | Gerber depth | On/off toggle that, when enabled prior to adding pieces to a model, automatically prepends the model name to each added piece's name (e.g., model "313" + piece "Front" → "313 Front"). |
| Edit Menu Overview (help/documentation section) | Gerber: Overview of the Edit Menu | Gerber depth | Non-functional introductory documentation node describing that the Edit menu groups undo, selection, and selection-clearing commands; retained as a catalogue/help entry, not an executable feature. |
| Remove Pieces from Model | Gerber: Remove Pieces | Gerber depth | Deletes one or more selected pieces from a specified (or last-used) model without removing the underlying piece definition from the system library; accessed via Create/Edit Model → Remove Pieces. |
| Auto Arrange Sewing Order | Richpeace: Auto Arrange Sewing Order | Richpeace depth | Automatically sequences sewing order across multiple selected sewing lines given a user-picked starting line, an operating-range filter (e.g., parallel lines only), and a direction/effect option, via a dedicated dialogue. |
| Check Sewing Order | Richpeace: Check Sewing Order | Richpeace depth | Interactive inspection mode where the cursor switches to a sewing-template tool and typing sequential numbers highlights/selects the correspondingly numbered sewing lines, scoped to a selected pattern or shown globally if none is selected. |
| Motif Library (save custom motif) | Richpeace: Motif Lib | Richpeace depth | Captures a user-drawn repeating stitch shape (via intelligent pen tool plus point selection) and saves it as a named, reusable motif file into a dedicated motif library folder for later retrieval. |
| Use Motif (apply from library) | Richpeace: Use Motif | Richpeace depth | Loads a saved motif from the library into a sewing-template slot, displaying a marker point indicating one repeat's length and height for placement/scaling. |
| Save Patterns Position (workspace layout snapshot) | Richpeace: Save patterns position | Richpeace depth | Records the current arrangement/positions of patterns in the work area and stores it under a user-chosen name so the layout can be restored later. |
| Save Each Step (auto-save per operation) | Richpeace: Save each step | Richpeace depth | Setting that, when enabled, automatically saves the file after every individual editing operation, providing granular recovery checkpoints. |
| Sewing Template Auto-Sewing Stitch Length | Richpeace: Sewing Template—Sewing Dialogue: Use Stitch Length | Richpeace depth | Pre-configures stitch length(s) for auto-sewing machine output, accepting a single value (0.1–2.55 cm) or multiple alternating values (e.g., 0.25, 0.4 repeating) applied cyclically during sewing. |
| Macro Record/Replay | Gerber: (undocumented Expert Edition macro record/replay capability) | Novel — Gerber | Records a sequence of user actions/commands as a reusable macro and replays it on demand to automate repetitive pattern-editing workflows; implemented as a first-class feature despite minimal documentation in the source manual. |



## 5. Workflow diagrams

Four workflows, covering piece creation, grading, digitizing/import, and seam/dart editing — each
with explicit decision branches for the error/retry paths a real implementation needs (validation
failures, calibration mismatches, geometry conflicts).

### 5.1 Piece creation from scratch
![Piece creation from scratch]({{artifact:3eb9a51e-968f-4004-9054-95b913134d26}})

### 5.2 Grading a piece across a size range
![Grading workflow]({{artifact:f8e36aec-38d3-4901-9bc8-78e9f07346e2}})

### 5.3 Digitizing / importing a piece
![Digitizing and import workflow]({{artifact:4b9d752b-f32c-4b52-825f-507011e46b43}})

### 5.4 Editing seams / darts / pleats
![Seam and dart editing workflow]({{artifact:f5ca3243-872e-477a-a4a7-360ac51f04c1}})

## 6. UI / rendering approach for the 2D pattern-drawing canvas

**Confirmed web-based, no desktop packaging.** React + TypeScript (Vite), rendering the pattern
canvas with Konva.js on top of HTML5 Canvas.

### 6.1 Canvas layering
Konva's layer model maps directly onto the editing needs of a pattern piece:
- **Background/grid layer** — ruler, grid, unit markers (mm/inch toggle); redrawn only on
  zoom/pan, never on edit.
- **Piece geometry layer** — the perimeter, internal lines, seams, darts/pleats, notches, grain
  line, text annotations for the piece(s) currently open. One Konva `Group` per piece so multiple
  pieces (e.g., a trace source and its copy) can be shown and manipulated independently.
- **Digitized-source overlay layer** — the raw scanned/camera image, shown at reduced opacity
  under the geometry layer during the digitizing workflow (§5.3) so the operator can trace or
  verify against it; hidden once the piece is finalized.
- **Grade-nest overlay layer** — during grading review (§5.2), every size's graded outline is
  drawn as a separate low-opacity `Group`, color-coded by size, on top of the base-size outline;
  toggling a size on/off is a Konva `visible` flag flip, not a re-render.
- **Selection/handle layer** — control points, drag handles, selection marquee; the only layer
  redrawn on every mouse-move during an active drag, kept separate so dragging a handle never
  forces a re-render of the (potentially large) geometry layer underneath it.

### 6.2 Coordinate system and precision
Pattern geometry is authored and stored in real-world units (mm, per §3.3's document schema) and
mapped to canvas pixels through a single zoom/pan transform matrix shared by all layers, matching
Konva's `Stage` scale/position rather than converting coordinates per-shape. Snapping (to grid, to
existing points, to perpendicular/tangent construction guides) is computed in real-world units
before the transform, so snap tolerance stays constant across zoom levels.

### 6.3 Tool architecture
Every drawing/editing tool (draw line, place notch, insert dart, trace, etc.) is implemented as a
command object with `apply(pieceDocument)` / `invert()` — the same command list backs undo/redo
(§4 Point/Line Editing category includes Undo/Redo) and, on save, is what gets diffed against the
last-saved geometry document (§3.3) before the whole document is re-serialized and pushed as a new
Blob Storage version through the platform API. Tools are registered against the current mode
(Draw / Edit / Grade Review / Digitize) so the same click-on-canvas gesture means "place a point"
in Draw mode and "select for editing" in Edit mode, mirroring how Gerber's PDS2000 switches tool
behavior by active menu.

### 6.4 Performance considerations at enterprise piece complexity
A complex piece can carry hundreds of points across dozens of internal lines; a grade-nest overlay
multiplies that by the number of sizes in range (a 20-size range means 20 outlines on screen at
once). Konva's shape caching (`Shape.cache()`) is used per-piece-per-size so an unchanged graded
outline is a single bitmap blit rather than a vector re-render on every pan/zoom frame; only the
actively-edited piece/size stays as live vector shapes. This keeps grade-nest review responsive
without needing WebGL-level custom rendering — Konva's Canvas 2D backend is sufficient at this
piece-complexity scale, and is reserved as a fallback: if profiling later shows nest-overlay
rendering is a bottleneck at real piece counts, that is the point to introduce a WebGL layer, not
before.

### 6.5 Digitizer table / camera input
The browser cannot talk to a legacy serial digitizer table directly. Digitizer-table input (lower
priority per §4's Digitizing category — legacy hardware, kept for parity but not the primary
modern path) is captured via a small local bridge service on the operator's workstation that
converts table strokes into point events over a WebSocket to the browser session; camera/scan
input (the higher-priority modern path) is a standard file/image upload handled entirely in-
browser plus server-side contour detection (Shapely/NumPy on the backend, §1) — no bridge needed.

## 7. Phased build plan

This app is built in **Phase 2** of the suite-wide roadmap, in parallel with Marker Making's core
nesting logic, once the Data Management Platform's API is stubbed and stable (`development_
roadmap.md`). Internally, Phase 2's Pattern Design track is sequenced as follows:

**Phase 2.1 — Platform integration scaffolding + core piece lifecycle**
`pattern-design-service` FastAPI skeleton; piece-geometry document schema (§3.3) and its Alembic-
migrated reference tables (§3.2); create/open/save/delete a piece through the platform API;
Konva canvas skeleton with the layering model (§6.1) and pan/zoom/grid. Exit criteria: a piece with
just a drawn perimeter round-trips through Blob Storage and Postgres correctly, including workflow
status.

**Phase 2.2 — Piece creation and point/line editing (build to Gerber's depth)**
Full draw/trace/extract/rectangle toolset; point/line add/delete/move/curve editing; undo/redo
command stack (§6.3). This is the largest single category pair (piece creation + point/line
editing together account for 179 of the 713 catalogue rows — 41 in Piece Creation, 138 in
Point/Line Editing) and is Gerber-depth per §4, so it is the first full-depth category pair built,
establishing the command/tool architecture every later category reuses.

**Phase 2.3 — Seams, darts/pleats/fullness, notches, grain line**
Seam allowance (union depth — Gerber's allowance model + Richpeace's corner-type library, §4),
darts/pleats/fullness (Gerber depth), notches/internal markings and grain line (Richpeace depth).
Exit criteria: the seam/dart editing workflow (§5.4) runs end-to-end including its conflict/retry
branches.

**Phase 2.4 — Grading engine**
Grade rule tables and grade rules (§3.2); grading computation service (delta application across a
size range); grade-nest overlay rendering (§6.1, §6.4). Built to Richpeace's grading-granularity
depth per §4, including the sign/axis operations (Neg X/Y/XY, Paste X/Y). Exit criteria: the
grading workflow (§5.2) runs end-to-end including per-size review and validation-failure retry.

**Phase 2.5 — Measurement, digitizing/import, plotting, text/annotation**
Measurement charts (Gerber depth); digitizing/camera input (Richpeace depth) including the
digitizer-table bridge service (§6.5); plotting/print preview (Richpeace depth); text/annotation
(Gerber depth). Exit criteria: the digitizing workflow (§5.3) runs end-to-end.

**Phase 2.6 — Customization/preferences and automation**
Preferences, toolbar customization, view options (Gerber depth, minus the legacy AccuMark/
MicroMark menu-emulation mode, deferred per §4's customization guidance); sewing-template/motif
save-and-reuse (Richpeace depth) and macro record/replay. This is deliberately last: it is the
largest category pair by raw function count (162 catalogue-input items) but the lowest-risk to
build once every underlying tool already exists to attach a preference or macro-recording to.

**Exit criteria for Phase 2 as a whole** (matching `development_roadmap.md`'s Phase 2 exit
criteria): Pattern Design can create, edit, and grade a piece and save it through the platform,
independent of Marker Making's parallel progress on nesting.
