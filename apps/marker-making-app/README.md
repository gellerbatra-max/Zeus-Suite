# marker-making-app

Marker Making's manual-nesting canvas, Phase 2 Slices 1-2 (see
[`docs/planning/03_marker_making_production/marker_making_production_plan.md`](../../docs/planning/03_marker_making_production/marker_making_production_plan.md)).
React + TypeScript + Vite + [Konva.js](https://konvajs.org/), talking to
[`marker-making-service`](../marker-making-service) (which itself has no database — see that
service's README for the full architecture).

## What's here

- **Marker canvas** (`MarkerCanvas.tsx`) — a Konva `Stage`/`Layer`: drag a piece from the tray onto
  the marker boundary to place it, drag a placed piece to move it, click to select, then
  rotate (90° steps) / flip H / flip V / unplace. A red outline flags bounding-box overlap between
  placed pieces (visual only, no hard block). Each piece renders as a labeled rectangle with a
  synthetic width/height — Pattern Design doesn't exist yet, so there's no real silhouette geometry
  to render. **Overlapped checking** (§1.4): selecting an overlapping piece reads out the max
  overlap value against its neighbour(s) (`src/geometry.ts`'s `overlapAmount`, the axis-aligned
  intrusion extent on each axis) just below the canvas — e.g. "Overlaps PANEL-B by 80.0 (y-axis)".
  Same axis-aligned-bounding-box simplification as the overlap outline itself (no rotation-aware
  polygon intersection).
- **Piece tray** (`PieceTray.tsx`) — the style's pieces not yet placed on this marker.
- **Matching panel** (`MatchingPanel.tsx`, Phase 2 Slice 2) — create/select a matching rule table,
  choose Standard/5-Star method, enter Standard's repeat offsets, define stripe geometry, add/edit/
  delete/step-through named stripe marks, assign the selected canvas piece to a mark, and run
  bite-boundary validation. Dragging a piece that has an assigned stripe mark calls the guidance
  endpoint (throttled ~150ms) and the canvas renders a green vector arrow toward the nearest valid
  grid point, with a "Matching Location Not Found" banner when none is within tolerance — a small
  tick on a placed piece marks that it has a stripe mark assigned, colored per the **cutter stripe
  setup toggle** (§1.4, orange = still needs auto-cutter stripe matching, blue = not needed) — a
  "Cutter Stripe: Needed/Not Needed" button in the piece toolbar flips it for the selected piece,
  persisted via `placement_data.cutter_stripe_needed` the same way `stripe_mark_id` is. **Known
  limitation**: there's no way to *unset* a marker's rule table once linked from this UI (or the API
  underneath it) — `PATCH` treats `null` as "field not provided," same as every other field on that
  resource, so selecting "(none)" in the rule-table dropdown updates local state but not the
  persisted marker. **Weave-line tools** (§1.4) — a global reference line (angle + perpendicular
  offset) editable via the Weave Line section: enter angle/offset directly, toggle Visible, or click
  "Center on Selected Piece" (`src/geometry.ts`'s `weaveLineOffsetForPoint` computes the offset that
  puts the line through that piece's center at the current angle) — the canvas renders it as a long
  dashed segment (`weaveLineSegment`, centered on whichever point of the infinite line is closest to
  the canvas middle, since exact line/rectangle clipping isn't done) with an always-upright "WEAVE"
  label, per the plan's "Font on Weaveline Upwards always." A "Piece override" subsection (only
  active once a piece is selected) covers "Edit Weave Line" for a single piece — its own angle/
  offset (with its own "Center for Selected Piece"), persisted via `placement_data.weave_line_
  angle_deg`/`weave_line_offset` the same way `stripe_mark_id` is; a piece with an override renders
  its own shorter dashed segment (scoped to just its own bounding box, in canvas space rather than
  inside the piece's own rotated Group, since the override angle is a marker-space direction) drawn
  *in addition to* the global line — the two aren't mutually exclusive on canvas, they just usually
  don't visually coincide since the override line is scoped to that piece's own bbox rather than
  spanning the whole marker. "Clear Override" removes the piece's own line, leaving only the global
  one wherever it happens to cross that piece. **Define Material / Material Pattern** (§1.4,
  "Show Marker's Pattern") — upload a fabric reference image (name + file picker), computing its
  SHA-256 checksum in-browser (`crypto.subtle.digest`) before completing the upload; a 40×40
  thumbnail (fetched via a fresh SAS download URL) plus Hide/Show and Delete buttons appear once
  one exists. When visible, the canvas renders it as a semi-transparent (`opacity=0.6`) full-marker
  background behind everything else, loaded through a small custom `useHtmlImage` hook in
  `MarkerCanvas.tsx` (this project has no `use-image`-style dependency). **Deferred**: "Show
  Piece's Pattern" (clipping the image to an individual piece's own silhouette) — there's no real
  piece geometry to clip against yet (only the synthetic placeholder rectangles). **Stripe-only-
  in-a-set** (§1.4) — since this canvas only ever places one instance per piece (no way to
  represent literal multiple physical "sets" of one garment size), this is built as: assigning a
  stripe mark to a piece syncs the same mark across every other placed piece sharing its garment
  size by default (`App.tsx`'s `handleAssignMark`), and a "Stripe Set: Linked/Independent" button
  in the piece toolbar opts a piece out of that sync — it neither pushes its own assignment onto
  its size group nor gets overwritten when another piece in that group is reassigned. A small
  purple "S" badge renders next to an independent piece's stripe-mark tick on the canvas.
- **Fuse Block panel** (`FuseBlockPanel.tsx`, §1.6) — create/delete block-buffer rule tables
  (name, rule #, block/buffer type, static/dynamic mode, L/T/R/B amounts), assign one to the
  selected piece (renders a small teal "BL"/"BU" badge on the canvas per the rule's type), and
  manage fuse blocks. **Known simplification**: this canvas has no marquee/ctrl-click multi-select,
  so grouping several pieces into one fuse block uses a sequential "draft" workflow instead — select
  a piece, click "Add Selected Piece" to accumulate it into a list, repeat, then "Create Fuse Block"
  once the whole group is queued. Each fuse block in the list shows its member pieces, current
  `block`/`reduce` amounts and derived `notch` depth, plus "Recompute Bounds" (re-fetches the
  member pieces' current placements and re-derives the bounding box — for after one has been
  dragged), `Block ±`/`Reduce ±` steppers, and Delete/Delete All. On canvas, a block renders as a
  dashed teal rectangle inflated by `block_amount` around the tight bbox of its member pieces, plus
  a small V-notch at the Op-Stop pause point labeled with the derived notch depth — visual/
  informational only, since no real cut-file pipeline exists yet.
- **Material panel** (`MaterialPanel.tsx`, §1.7) — reads `GET .../material/summary` on open: a
  "Live (from current placements)" readout (total piece area/perimeter, marker length needed, and
  utilization computed fresh every time, before anything is saved) next to a "Stored on marker"
  readout (the marker's actual `marker_length`/`utilization_pct` columns, which start empty and
  only change when "Apply Computed Length & Utilization" is clicked — deliberately two different
  numbers so the panel can show "here's what fits" alongside "here's what was actually committed
  to"). Ply count and fabric weight-per-unit-area are plain inputs saved immediately (not batched
  into the main Save button, same immediate-persistence pattern as matching's rule-table linking).
  A "Target (order)" section sets `target_length`/`target_utilization_pct` on the marker's linked
  order (disabled with a note when the marker has no order) — the canvas renders the target length
  as a long dashed purple vertical line labeled "TARGET" at that X position, the length axis this
  app already uses for bite-boundary validation. "Calculate Efficiency & Marker Length" and
  "Calculate Material Weight" are pure calculators (no Save button, nothing persists) that call the
  service's dedicated endpoints and print the result inline. **Deferred**: "Estimate Material"
  (cap-nesting, per-mode breakdown) and the standalone material-calculation-file what-if tool —
  see [`marker-making-service`](../marker-making-service)'s README for why.
- **Marker-wide Flip / Transform panel** (§1.9) — a "Flip whole marker: Flip X / Flip Y / Flip XY"
  row in the main toolbar mirrors every placed piece's position within the tight bounding box of
  everything currently placed (`src/geometry.ts`'s `computeBoundingBox`, the same bbox-as-reference-
  frame convention fuse-blocking and material-calc already use) and toggles each piece's own flip
  flag — a pure local-state edit persisted on the next Save, exactly like single-piece Flip H/V
  already work (no server round trip). `TransformPanel.tsx` covers the two server-backed
  capabilities: "Change Width of Marker" `PATCH`es the marker's `fabric_width`, which now actually
  drives the canvas's fabric-width axis (the canvas height — this app's established convention
  treats X as the unbounded cut-length axis and Y as the bounded fabric-width axis, the same one
  bite-boundary validation and material-calc's length math already assume) instead of a hardcoded
  constant; a note under the input makes explicit that this does **not** auto-rearrange pieces —
  there's no real nesting algorithm to call one. "Shrink / Stretch (order)" saves
  `shrink_x_pct`/`shrink_y_pct` onto the marker's linked order (disabled with a note when there
  isn't one), and "Apply to Placements" calls the service's stand-in endpoint that scales the
  current canvas geometry right now and refreshes it in place — a warning line makes explicit that
  clicking Apply twice double-scales, since nothing tracks whether it's already been applied.
- **Bundle panel** (`BundlePanel.tsx`, §1.3) — groups placed pieces (one garment, one size) by a
  shared `bundle_id` riding inside `placement_data`, the same opaque-passthrough pattern as
  `stripe_mark_id`/`blockBufferRuleNo` — no server round trip for any bundle operation, all
  persisted on the next Save. Uses the same sequential "draft" workflow fuse-blocking established
  (select a piece, "Add Selected Piece", repeat, "Create Bundle") since there's still no canvas
  multi-select; the auto-generated bundle number is just "how many distinct bundle ids already
  exist, plus one." **Validation**: Create is rejected if the draft pieces don't all share the
  same `sizeCode` (a bundle is one garment, one size) or if the selected piece is already in a
  bundle (unplace it first to move it). Each bundle's row offers Select (sets the canvas selection
  to its first member — every other member gets a lighter highlight fill so the "whole bundle"
  still reads visually, since there's no true multi-selection), Flip X/Y/XY (mirrors just that
  bundle's own members within their own combined bounding box — same math as the whole-marker flip
  above, scoped down), Reset Orientation (rotation back to 0°, both flips cleared), Unplace/Return
  (removes every member from the canvas back to the tray in one action — the plan's "Bundle/
  Unplace" and "Return Bundle" collapse into a single action here since there's no piece-splitting
  to merge back together first), and Set Quantity (bulk-sets every member's placement quantity).
  On canvas, each bundle renders as a dashed indigo rectangle around its tight combined bounding
  box labeled "Bundle N (size)", with a small indigo dot on each member piece. A 500-bundle cap is
  enforced as a fixed client-side warning — see
  [`marker-making-service`](../marker-making-service)'s README for why it isn't a real
  server-enforced, per-marker-configurable ceiling.
- **Splice panel** (`SplicePanel.tsx`, §1.8) — a settings form (min/max mark length, margin,
  separation, saved onto the marker), "Splice / Automatic" (enter a roll length by hand — there's
  no real fabric-roll data anywhere in this platform — and click "Regenerate Auto Splices" to call
  the service's placement algorithm), a manual-add mini-form (start/end/roll id), and a list of all
  marks sorted by position with per-mark Delete plus Delete All. On canvas, each mark renders as a
  shaded amber band spanning the full fabric-width axis at `[start_x, end_x]` — dashed border for
  `source: 'auto'`, solid for `'manual'`, so which marks survive a regenerate is visually obvious
  without opening the panel — labeled with its `roll_id` (or just its source, if none was given).
- **Layrule panel** (`LayrulePanel.tsx`, §1.5) — Layrule Search Parameter Table management (name,
  area-deviation threshold, allow-overrides toggle), this marker's own layrule settings (force
  layrule name / linked search table, saved independently of the main Save button), "Capture this
  marker's layout as a layrule" (a one-click stand-in for "Auto-Store Layrule" — there's no
  background hook to fire it on every save automatically), and "Apply a layrule to this marker"
  (picks from every layrule in the org, calls the service's real matching logic, and shows
  `Applied N, unmatched M[, area deviation X%][, warning]` inline). Applying a layrule can place
  pieces that had no local placement at all — a plain marker-length calc's "map over existing
  placements" pattern (used by Shrink and Stretch's Apply) would silently drop them, so this uses
  its own workspace-rebuild path that reconstructs the full placement list from what the server
  actually returns.
- **Auto-Nest panel** (`NestingJobPanel.tsx`) — submits to `marker-making-service`'s
  `POST /nesting-jobs` and polls to completion. Proves Engine B's async plumbing end-to-end; the
  result is still the platform's Milestone-6 stub placeholder, not a real placement-producing
  solver.
- `identity.ts`/`IdentityBar.tsx` — the same local-dev auth stand-in `data-management-app` uses
  (type a username instead of a real Entra ID login); forwarded through to the platform unchanged.

## Local setup

Needs `marker-making-service` running (which itself needs `data-platform-api` running — see that
chain of READMEs).

```bash
npm install
npm run dev   # http://localhost:5174
```

There's no marker picker UI yet — paste a marker's UUID into the "Marker ID" field to open it (get
one via `data-platform-api`'s own API, e.g. `POST /markers`, until Pattern Design/an order-entry
flow exists to create these through a UI).

```bash
npx tsc -b       # type-check
npx oxlint        # lint
npm run build     # production build
```

## Verified manually

**Slice 1**: opened a real marker's workspace, placed 3 synthetic pieces via drag-and-drop, rotated
one, saved (confirmed the platform's real workflow-transition graph walks
`unmade → needs_approval → made` across two calls, not a single direct hop), reloaded the page and
confirmed the placements persisted through the real platform API, then submitted an Auto-Nest job
and watched the UI poll it to `succeeded` after the platform's worker drained it.

**Slice 2** (matching): created a matching rule table through the panel, selected Standard method,
added a stripe definition (h_distance=40) and a stripe mark against it, placed a piece and assigned
it to that mark (a red tick appeared), dragged the piece and watched a live green guidance arrow
plus the "Matching Location Not Found" banner render from the real `/matching/guidance` endpoint,
saved and reloaded to confirm the marker's `placement_data.stripe_mark_id` and matching method/rule
table all persisted through the real platform API (verified directly via
`GET /markers/{id}/pieces`), and ran Validate Bite to confirm "No bite-boundary violations." with
a single piece (the violation-detected/cleared path is covered by
`marker-making-service`'s automated test instead, since it needs 1-canvas-unit precision that isn't
meaningful to demonstrate via manual mouse dragging).

**Cutter stripe setup toggle**: selected a matched piece (rendering an orange tick, the default
"still needs" state), clicked "Cutter Stripe: Needed" to flip it — the tick turned blue and the
button label updated to "Not Needed" — saved, and confirmed `placement_data.cutter_stripe_needed`
persisted through the real platform API via `GET /markers/{id}/pieces`; then flipped it back and
re-verified the same round trip in the other direction.

**Overlapped checking**: seeded two pieces at `{x:50,y:50,w:80,h:100}` and `{x:100,y:70,w:80,h:100}`
(hand-computed overlap: 30 on the x-axis, 80 on the y-axis), opened the marker, selected the second
piece, and confirmed the readout under the canvas showed exactly "Overlaps PANEL-OV-A by 80.0
(y-axis)" — matching the hand calculation and picking the correct (larger) axis.

**Weave-line tools**: created a matching rule table, selected a placed piece at
`{x:250,y:50,w:100,h:120}` (center `(300, 210)`), left angle at its default 0, clicked "Center on
Selected Piece" — confirmed the resulting offset was exactly `210` (hand calc: at angle 0 the
perpendicular is straight up/down, so the offset is just the center's Y) and the canvas rendered a
horizontal dashed line through the piece's vertical center with an upright "WEAVE" label. Unchecked
Visible and confirmed the line disappeared from the canvas.

**Per-piece weave-line override**: seeded two placed pieces on one marker linked to a table with a
global horizontal line (angle 0, offset 100) — one piece with no override (rendered the global line
through it) and one seeded with `weave_line_angle_deg=45`/`weave_line_offset=50` in its
`placement_data`. Confirmed the second piece rendered its own diagonal segment scoped to its own
bounding box instead of (in addition to) the global line, selecting it showed "Piece override
(active)" with the Angle/Offset inputs correctly prefilled `45`/`50` (distinct from the global
line's `0`/`100` shown just above), and clicking "Clear Override" removed that piece's diagonal
segment from the canvas immediately.

**Define Material / Material Pattern**: the actual file-picker upload step can't be driven through
this project's browser-automation tooling (native OS file dialogs are outside its reach — a
browser-security limitation, not a product one), so the full begin-upload → PUT bytes → complete
sequence is instead covered by `marker-making-service`'s automated test against real Azurite. What
*was* verified live in the browser: seeded a real material pattern via the same three HTTP calls
the UI makes, reloaded the marker, and confirmed (a) the canvas rendered the image as a semi-
transparent full-marker background, (b) the thumbnail `<img>` element had `complete: true` and
`naturalWidth/naturalHeight: 1×1` (matching the 1×1 test PNG) after loading from a real Azurite SAS
URL, and (c) clicking "Hide on Canvas" removed the background immediately, confirming the
visibility toggle reaches the canvas layer correctly.

**Fuse Blocking**: seeded two placed pieces on one marker at `{x:10,y:20,w:50,h:40}` and
`{x:80,y:5,w:30,h:60}` (hand-calculated tight bbox of both: `x=10,y=5,width=100,height=60`),
created a block-buffer rule table (`#1 Fuse Rule A`, block/static), selected the first piece and
assigned it that rule via the "Selected piece's rule" dropdown — confirmed the teal "BL" badge
rendered on the piece (verified both visually and by querying the Konva scene graph directly,
since this pane's `zoom` region-crop isn't supported here). Selected each piece in turn and used
"Add Selected Piece" to queue both into the fuse-block draft, then "Create Fuse Block" with the
default block=0.5/reduce=0 — confirmed via `GET /markers/{id}/fuse-blocks` that the stored bounds
were exactly `x=10.0, y=5.0, width=100.0, height=60.0`, matching the hand calculation precisely,
and via the Konva scene graph that the rendered dashed rectangle was `x=9.5, y=4.5, w=101, h=61`
(the stored bbox inflated by `block_amount=0.5` on every side, as intended) with a `"notch 0.50"`
label. Clicked "Block +" and confirmed the panel and the notch label both updated to `0.60`, then
deleted the fuse block and confirmed both the panel list and `GET /markers/{id}/fuse-blocks`
went empty.

**Stripe-only-in-a-set**: seeded two same-size (`M`) pieces on one marker, both defaulting to
"Stripe Set: Linked". Assigned Mark 1 to piece A and confirmed piece B's stripe-mark tick appeared
too (the sync). Toggled piece B to "Stripe Set: Independent", added Mark 2, selected piece A, and
assigned Mark 2 to it. Saved and confirmed via `GET /markers/{id}/pieces` that piece A now carried
Mark 2's id while piece B still carried Mark 1's — the independent toggle correctly excluded it
from being overwritten by the sync.

**Material calculation/utilization**: seeded a marker with `fabric_width=200` and two placed
pieces at the same coordinates as the fuse-blocking check above (total piece area by hand:
`50×40 + 30×60 = 3800`; marker length needed: `max(10+50, 80+30) = 110`; utilization:
`3800/(200×110)×100 = 17.27%`) — opened it and confirmed the "Live" readout showed exactly those
three numbers before anything was saved, while "Stored on marker" still read `—`/`—` (nothing
persisted yet). Clicked "Apply Computed Length & Utilization" and confirmed both the panel and
`GET /markers/{id}` (direct platform call) now showed `marker_length=110`, `utilization_pct=17.27`.
Entered ply count `10` and weight-per-area `0.02`, saved, and confirmed both round-tripped through
a page value check and the platform API. Entered target efficiency `50%` under "Calculate
Efficiency & Marker Length" and got `Required length: 38` (hand calc: `3800/(200×0.5)=38`).
Clicked "Calculate Material Weight" with no extra input (falls back to the stored ply
count/weight-per-area/marker length) and got `Weight: 4400` (hand calc:
`200×110×10×0.02=4400`). Entered target length `150`/target utilization `90` under "Target
(order)", saved, confirmed via `GET /orders/{id}` that both persisted on the linked order, and
confirmed via the Konva scene graph that the canvas rendered a dashed purple vertical line at
exactly `x=150` labeled "TARGET".

**Marker transformations**: seeded a marker with `fabric_width=200` and the same two placements as
the material-calc check above — opened it and confirmed the Konva stage's actual pixel height was
`200` (not the old hardcoded `450`), proving `fabric_width` now drives the canvas. Clicked "Flip
X": bbox of both pieces is `min_x=10, min_y=5, max_x=110, max_y=65`; hand calc for piece A
(`x=10,w=50`) is `new_x = 10+110-10-50 = 60`, for piece B (`x=80,w=30`) is
`new_x = 10+110-80-30 = 10` — confirmed both exactly via the Konva scene graph, along with
`scaleX=-1` on each Group (the flip flag toggled). Saved and confirmed the new `x`/`flip_x` values
persisted through `GET /markers/{id}/pieces` against the real platform API. Entered Shrink X
`-50%` / Shrink Y `+100%` under "Shrink / Stretch (order)", saved, and confirmed via
`GET /orders/{id}` that both persisted (`shrink_x_pct=-50, shrink_y_pct=100`). Clicked "Apply to
Placements" and confirmed via the platform API that piece A (`x=60,y=20,w=50,h=40` post-flip)
became exactly `x=35, y=35, w=25, h=80` and piece B (`x=10,y=5,w=30,h=60`) became exactly
`x=10, y=5, w=15, h=120` — both matching the hand calculation (`scale_x=0.5`, `scale_y=2.0`,
anchored at the combined bbox's top-left corner `(10,5)`) — and that the canvas re-rendered the
new geometry immediately, without a manual reload. Entered fabric width `300` under "Change Width
of Marker", clicked "Change Width", and confirmed both the Konva stage height (`300`) and
`GET /markers/{id}`'s `fabric_width` updated immediately.

**Bundle management**: seeded a marker with three pieces, placed two (`x=10,y=20,w=50,h=40` and
`x=80,y=5,w=30,h=60`, same coordinates as the fuse-blocking/flip checks above) leaving one
unplaced. Selected each placed piece in turn and used "Add Selected Piece" to queue both into the
bundle draft, then "Create Bundle" — confirmed "Bundle 1 (M) — BND-P1, BND-P2" appeared in the
list, and via the Konva scene graph that the dashed indigo group rectangle was drawn at exactly
`x=6, y=1, w=108, h=68` (the pieces' combined bbox `x=10,y=5,w=100,h=60` inflated by 4px on every
side) labeled "Bundle 1 (M)", with an indigo dot on both member pieces. Clicked "Flip X" and
confirmed via the Konva scene graph that both pieces moved to exactly `x=60`/`x=10` respectively
with `scaleX=-1` — matching the same bbox-mirror hand calculation as the whole-marker flip check.
Clicked "Select" and confirmed the first member got the primary blue selection fill while the
second got the lighter bundle-mate highlight fill, both distinct from an unrelated piece's default
fill. Clicked "Reset Orientation" and confirmed both pieces' `scaleX`/`scaleY` returned to `1`
without moving their (already-flipped) positions. Entered quantity `5` and clicked "Set Quantity",
then Saved, and confirmed via `GET /markers/{id}/pieces` (direct platform call) that both pieces
persisted with `quantity=5`, their flipped `x`/`y`, `flip_x=false`/`rotation_deg=0` (post-reset),
and a shared `bundle_id="bundle-1"`. Clicked "Unplace / Return" and confirmed the bundle
disappeared from the list and "Unplaced Pieces" count went from 1 to 3 — both former bundle
members returned to the tray alongside the piece that was never placed.

**Splice marks**: seeded a marker with `fabric_width=200` and the same two placements as the
material-calc/flip checks above (marker length by hand: 110). Entered splice settings
(min length `1.0`, max length `5.0`, margin `0.5`, separation `2.0`), saved, and confirmed via
`GET /markers/{id}` (direct platform call) that all four values persisted. Entered roll length
`40` and clicked "Regenerate Auto Splices" — hand calc: boundaries at `40` and `80` (both within
`[2, 108]`), mark length `clamp(0.5×2, 1.0, 5.0) = 1.0` — confirmed the panel listed exactly
`39.50–40.50 (auto, roll-2)` and `79.50–80.50 (auto, roll-3)`, and via the Konva scene graph that
the canvas rendered two dashed amber bands at exactly `x=39.5`/`x=79.5`, width `1`, spanning the
full canvas height, labeled `roll-2`/`roll-3`. Added a manual mark (`1.00–1.50`, roll id
`hand-added`) and confirmed it appeared with a `(manual, hand-added)` label. Clicked "Regenerate
Auto Splices" again and confirmed the mark count stayed at exactly 3 (no duplication) with the
manual mark's `id` unchanged — verified directly via `GET /markers/{id}/splice-marks` (the auto
marks got fresh ids, confirming they were deleted and recreated rather than left stale). Clicked
"Delete All" and confirmed the list and the platform API both went empty.

**Layrules**: seeded two markers on the same style/order (so both share the same available
pieces) — placed two pieces on the source marker at the same coordinates as the fuse-blocking
check above (`x=10,y=20,w=50,h=40` and `x=80,y=5,w=30,h=60`), captured them as "MyLayrule," and
confirmed via `GET /layrules` (direct platform call) that the captured `placements_json` matched
those coordinates exactly. Opened the second (empty) marker, selected "MyLayrule" under "Apply a
layrule to this marker," clicked Apply, and got `Applied 2, unmatched 0, area deviation 80.17%`
inline (no search table was linked, so the deviation was informational only, not gating) —
confirmed via `GET /markers/{id}/pieces` (direct platform call) that the target marker's
placements now matched the captured layout exactly. **Found and fixed a real bug during this
check**: the canvas didn't render the newly-applied pieces without a manual reload, because the
apply handler reused Shrink and Stretch's "map over existing placements" refresh function — which
does nothing when there were no existing placements to map over. Fixed by giving Apply its own
workspace-rebuild handler (reconstructs the full placement list from the server response, the same
way opening a marker does) and re-verified live: cleared the target marker's placements via the
API, reloaded, applied the layrule again through the UI, and confirmed via the Konva scene graph
that both pieces appeared at the correct positions immediately, with no reload needed. Clicked the
main "Save" button afterward and confirmed the marker's status badge advanced from "unmade" to
"made" — the documented catch-up for the "applying doesn't walk the workflow-status graph itself"
gap.
