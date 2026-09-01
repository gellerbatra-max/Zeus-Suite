# marker-making-app

Marker Making's manual-nesting canvas, Phase 2 Slice 1 (see
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
  to render.
- **Piece tray** (`PieceTray.tsx`) — the style's pieces not yet placed on this marker.
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

Opened a real marker's workspace, placed 3 synthetic pieces via drag-and-drop, rotated one, saved
(confirmed the platform's real workflow-transition graph walks `unmade → needs_approval → made`
across two calls, not a single direct hop), reloaded the page and confirmed the placements
persisted through the real platform API, then submitted an Auto-Nest job and watched the UI poll
it to `succeeded` after the platform's worker drained it.
