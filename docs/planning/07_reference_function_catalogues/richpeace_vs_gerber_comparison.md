# Richpeace DGS/GMS vs. Gerber PDS2000/AccuMark — Function Comparison
*(Corrected — a category-normalization bug in the first pass silently dropped LLM classification
labels that came back numbered (e.g. "14. Customization...") or bare-numbered ("14"), discarding
up to half of Gerber's classified pattern-design functions from the counts. All counts below are
recomputed with every classified function accounted for — see coverage note at the end.)*

Comparing the Richpeace V8.0 "Design and Grading System" (DGS) and "Garment Marking System" (GMS)
manual against the Gerber function catalogue already built in this project (Pattern Design /
PDS2000: 552 functions; Marker Making / AccuMark Professional Edition: 200 functions).

## Method
The Richpeace manual (346 pages) has no formal function-level table of contents, so its toolbar
and menu-bar sections — the actual function catalog, pages 26–227 for DGS and 239–346 for GMS —
were extracted page-by-page with the same excerpt-then-rewrite method used for the Gerber
manuals, producing 437 distinct named DGS functions and 312 distinct
named GMS functions. Both software's function lists were then classified into the same fixed
capability taxonomy (one for pattern design, one for marker making) so the two products could be
compared on equal terms rather than by matching menu names, which differ completely between them.

**Caveat on the counts:** a function count in a category is a *documentation density* signal, not
a quality or capability score by itself — a vendor that splits one action into five sub-menu
entries will out-count a vendor who covers the same ground in one flexible dialog. Read the counts
alongside the qualitative notes below, not instead of them.

![Capability comparison]({{artifact:1d4fde7c-a7da-4bd5-9022-61a62e00393d}})

## Pattern Design: Gerber PDS2000 vs. Richpeace DGS

| Category | Gerber PDS2000 | Richpeace DGS |
|---|---:|---:|
| Piece creation (draw/trace/extract/rectangle) | 57 | 21 |
| Point & line editing (add/delete/move points, curves, lines) | 88 | 50 |
| Seams & seam allowance | 32 | 43 |
| Darts, pleats, fullness, flouncing | 43 | 24 |
| Notches & internal markings (drill holes, buttonholes, symbols) | 13 | 26 |
| Grain line / fabric direction | 1 | 7 |
| Grading (rules, deltas, offsets, nest/size display) | 70 | 82 |
| Measurement & spec charts | 26 | 19 |
| Piece transformation (flip, rotate, mirror, combine, split, fold) | 32 | 26 |
| Text / annotation on pattern | 7 | 4 |
| Digitizing & scanning input (camera, digitizer table) | 10 | 19 |
| Import / export & file interchange (DXF, IGES, other CAD formats) | 3 | 4 |
| Plotting / printing | 11 | 27 |
| Customization, preferences, toolbars, work space setup | 103 | 42 |
| Automation (macros, templates, batch) | 0 | 12 |
| File/data management (open, save, storage areas) | 32 | 31 |

### Where they're comparable
Both systems cover the same core pattern-making ground: drawing/tracing/extracting pieces, editing
points and lines, seams, darts/pleats, grain lines, notches and drill holes, grading, measurement,
digitizing input, and plotting. **Seams & seam allowance** (32 vs. 43), **piece transformation**
(32 vs. 26), and **file/data management** (32 vs. 31) are close on both sides.

### Where Gerber documents more depth
- **Customization, preferences, toolbars, work space setup (103 vs. 42).** This is the largest gap
  in either direction. Gerber's manual documents an extensive, separately-switchable interface
  layer: a full legacy-menu-compatibility mode ("Using the AccuMark Menu" / "Using the MicroMark
  Menu" — turning on an older-style layout for workers trained on the classic system), a
  customizable Tool Bar organized by task, and a large preferences system covering piece display,
  selection/tracking behavior, colors, plotter defaults, and paths. Richpeace documents fewer,
  more consolidated settings.
- **Piece creation (57 vs. 21)**, **Point & line editing (88 vs. 50)**, and **Darts/pleats/
  fullness (43 vs. 24).** Gerber's PDS2000 breaks piece drawing, point/line tools, and pleat/dart
  sub-types into more distinct named commands.
- **Grain line / fabric direction (1 vs. 7) and Notches (13 vs. 26) run the other way** — see
  below.

### Where Richpeace documents more depth
- **Grading (70 vs. 82).** Closer than it first appears, but Richpeace still documents more —
  including fine-grained sign/axis operations Gerber's manual describes more generally, e.g.
  `Paste grading` / `Paste X` / `Paste Y` / `Neg X` / `Neg Y` / `Neg XY` for copying and
  sign-flipping grade values independently on the X and Y axes.
- **Notches & internal markings (13 vs. 26)**, **Grain line (1 vs. 7)**, **Plotting/printing (11
  vs. 27)**, and **Digitizing input (10 vs. 19).**
- **Automation — macros/templates/batch (0 vs. 12).** Richpeace documents a set of reusable
  "sewing template" and "motif" functions (`Create sewing template`, `Motif Lib`, `Auto Arrange
  Sewing Order`) for saving and replaying stitch/cut patterns — a real, if narrow, template-reuse
  feature. Gerber's equivalent (macro record/replay) is an Expert-Edition add-on that barely
  surfaces in its own table of contents, so it undercounts here.

## Marker Making: Gerber AccuMark PE vs. Richpeace GMS

| Category | Gerber AccuMark PE | Richpeace GMS |
|---|---:|---:|
| Manual piece placement/nesting (drag, butt, overlap, align) | 21 | 27 |
| Automatic/assisted nesting | 10 | 21 |
| Bundle management (group pieces into garments) | 15 | 3 |
| Matching (plaid/stripe alignment) | 4 | 23 |
| Layrules / record-and-replay automation | 23 | 0 |
| Block / buffer / fuse blocking | 21 | 1 |
| Material calculation / utilization / consumption | 1 | 10 |
| Splice marks / fabric roll handling | 3 | 4 |
| Marker transformations (flip, split, copy, attach whole marker) | 28 | 30 |
| Cut data generation / plotting / export to cutter | 0 | 46 |
| File / data management (open, save, storage areas) | 28 | 40 |
| Piece window / size list / piece info management | 7 | 66 |

### The single biggest structural difference: what's bundled into the marker-making app
Richpeace's GMS manual documents **`Cut order set up`, `Output to DXF`, `Plot Preview`, `Export
Bitmap`, `Printer Setup`, and `Print marker`** directly inside the marking application (46
functions in "Cut data generation/plotting/export to cutter" alone) — along with 66 documented
"Piece window / size list" functions that read like order/style metadata management (`Piece
Info`, `Order, Pattern, Size, Material`, `Piece name, Code, Description`). Gerber splits this same
ground across **two separate applications**: Marker Making handles only nesting/placement, while
cut-data generation, plotting, and order/model metadata live in the separate Order Entry
application (documented earlier in this project). **This is an architectural choice, not a
missing feature** — Richpeace consolidates marker-making and order/output management into one
GMS module; Gerber deliberately splits them. Folding Gerber's Order Entry functions back in
closes most of this gap.

### A genuine philosophical difference in automation: replay vs. solve
- **Gerber's approach — Layrules (23 functions, 0 in Richpeace's GMS as documented).** AccuMark's
  automation is built around *recording and replaying a human-verified prior marker*: "Layrules
  are a feature that lets AccuMark automatically remember and rebuild markers you've made before,
  saving you the work of manually placing every piece again." It searches a parameter table for a
  past marker matching the new order's criteria and replays that exact placement.
- **Richpeace's approach — Auto Nesting (21 functions under "Automatic/assisted nesting", roughly
  double Gerber's 10).** Richpeace's automation is an *algorithmic solver run from scratch* each
  time: "Auto Nesting - Normal... places all pieces on the marker according to the priority order
  set in Nesting > Start Autonesting," with dedicated `Stop`/resume controls, `Compact Marker`,
  and `Embedded Pattern` (compacting overlapped pieces) functions to refine the solver's output
  afterward.

These are two different bets on how to reduce manual nesting labor: Gerber bets that most orders
resemble something already made and reuses it; Richpeace bets on a general-purpose packing
algorithm that doesn't need historical precedent but must be run (and tuned/compacted) fresh every
time, and documents roughly twice as many functions around that solver-driven workflow.

### Richpeace documents substantially more plaid/stripe matching tooling
**Matching (4 vs. 23)** — the corrected count reverses what a first look suggested. Richpeace's
GMS has a well-developed, named toolset for pattern-matched fabric: `Define Stripes` (setting up
stripe/grid/stamp positions with explicit X/Y start coordinates and horizontal/vertical spacing),
`Stripe only in a set` (letting different garment sizes stripe independently for better nesting
efficiency), `Overlapped checking`, and `Edit Weave Line`. Gerber's Order Entry/Marker Making
manuals describe matching more as a configuration (Standard vs. 5-Star Matching, point/line
matching rules) than as this many distinct named tools — a real difference in how much matching
gets its own dedicated UI.

### Where Gerber documents more depth
- **Block/buffer/fuse blocking (21 vs. 1).** Gerber's fuse-blocking toolset (`Create Block`,
  rectangular vs. manually-traced blocks, `Modify Block Fuse`, `Copy Fuse Block`, and their
  GERBERcutter-specific workflow) is considerably more developed than what's documented in
  Richpeace's GMS.
- **Bundle management (15 vs. 3).**

### Where Richpeace documents more depth (beyond the structural categories above)
- **Material calculation/utilization (1 vs. 10)** — Richpeace documents more named consumption/
  estimate functions.
- **Marker transformations (28 vs. 30)** and **File/data management (28 vs. 40)** are close, with
  Richpeace slightly ahead on both.

## Overall verdict
On pure pattern-design fundamentals (piece creation, editing, grading, seams, darts), the two
systems are close to feature-equivalent — each has areas of deeper documented granularity than the
other, and Gerber's interface-customization layer is documented in unusually fine detail. The most
consequential differences remain architectural rather than functional:

1. **Richpeace unifies marker-making with cut/plot/order-output in one application; Gerber splits
   these across Marker Making and Order Entry.** Folding Order Entry back in closes most of the
   apparent gap on cutting/output/order-metadata categories.
2. **The two products bet on different automation strategies for nesting** — replay-a-known-good-
   marker (Gerber's Layrules) versus solve-fresh-with-an-algorithm (Richpeace's Auto Nesting, with
   roughly double the documented tooling around it). A modern product design would likely want
   *both*: an algorithmic solver for novel orders, plus a replay/reuse layer for the common case
   of a near-repeat order, which is where Gerber's approach saves the most labor.
3. **Richpeace documents a materially larger, more explicit plaid/stripe matching toolset** and
   more granular material-utilization functions.
4. **Gerber's fuse-blocking, bundle-management, and interface-customization tooling is more
   developed** — the fuse-blocking depth likely reflects legacy Gerber's GERBERcutter hardware
   integration rather than a general capability gap.

## Coverage note
{sum(gerber_pd_counts.values())}/{len(pd_classifications["gerber_pd"])} Gerber pattern-design,
{sum(richpeace_dgs_counts.values())}/{len(pd_classifications["richpeace_dgs"])} Richpeace DGS,
{sum(gerber_mm_counts.values())}/{len(mm_classifications["gerber_mm"])} Gerber marker-making, and
{sum(richpeace_gms_counts.values())}/{len(mm_classifications["richpeace_gms"])} Richpeace GMS
classified functions are accounted for in the tables above (100% in every group after the fix;
a small number of items in each group — 552-547, 200-197 — were never successfully classified in
the first LLM pass and are excluded from both totals, not silently miscounted).
