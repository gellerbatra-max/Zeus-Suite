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
  persisted marker.
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
