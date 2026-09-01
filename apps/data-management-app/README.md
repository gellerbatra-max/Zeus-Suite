# data-management-app

The Data Management App (Section 6 of [`data_management_platform_plan.md`](../../docs/planning/01_data_management_platform/data_management_platform_plan.md)) — the direct modern equivalent of AccuMark Explorer, and Milestone 7 of that document's phased build plan. React + TypeScript + Vite, calling `data-platform-api`'s REST surface like any other client (no special back-door access).

## What's here

- **Folder browser** (`FolderBrowser.tsx` + `FolderTreeNode.tsx`, Section 6.1) — a lazily-expanded tree pane and a content pane, plus folder creation.
- **Structured search** (`SearchPanel.tsx`, Section 6.2) — free-text + entity-type filters against `POST /search`.
- **Cross-reference view** (`CrossReferenceView.tsx`) — the one-hop reference graph from `GET /cross-reference/{type}/{id}`, reachable from both the browser and search results, with a direct link into the Activity Log pre-filtered to that entity.
- **Activity Log viewer** (`ActivityLogViewer.tsx`, Section 6.3) — filterable, with an expandable before/after diff per entry. No "Clear Log" control exists, by design (Section 4.9/2.9).
- **Reports** (`ReportsPanel.tsx`, Section 6.4) — runs a report definition and displays the result. `single_piece`, `all_piece`, and `all_marker` are implemented on the backend; the geometry-dependent report codes (`piece_perimeter`, `all_layrule`, `all_plot`, `all_cut`, `splice`) return a 501, since they need piece/marker geometry this platform stores as an opaque blob (see `app/report_service.py` on the backend).

## Auth

There is no real login screen. `src/identity.ts` + `IdentityBar.tsx` implement the same local-dev
auth stand-in the backend uses (`app/auth.py::dev_login`): you type a username (and optionally an
org code) instead of signing in through Entra ID, and every API call carries it as
`X-Dev-User`/`X-Dev-Org` headers. **A brand-new identity gets the `viewer` role only** (read
everything, write nothing) — creating a folder, running a report, etc. needs a role grant made
directly against the database today, since Section 4.11's RBAC-admin endpoints aren't built yet.

## Local setup

Needs `data-platform-api` running first (see [`../data-platform-api/README.md`](../data-platform-api/README.md)) — this app is a pure client of that API, with no server of its own.

```bash
npm install
npm run dev        # http://localhost:5173
```

`.env.development` points at `http://localhost:8000` by default; override with `VITE_API_BASE_URL`
if the backend runs elsewhere. The backend's CORS config (`app/main.py`) currently only allows
`localhost:5173` — update both sides together if you change the frontend's port.

```bash
npx tsc -b          # type-check
npx oxlint           # lint
npm run build        # production build (type-checks, then bundles to dist/)
```

## Verifying the Milestone 7 exit check manually

*"A non-technical tester can, using only the UI, create a folder, find a piece by structured
search, view its cross-references, and pull an Activity Log filtered to that piece."*

1. **Browse** → type a name → **Create folder**.
2. Create a piece in that folder (no piece-creation UI exists yet — Pattern Design owns that
   workflow in the real suite; use the API directly for now, e.g. `POST /pieces`).
3. **Search** → search text matching the piece's code → **Cross-references** on the result row.
4. In the cross-reference panel → **View Activity Log for this item** → the Activity Log tab opens
   pre-filtered to that exact entity, showing its `piece.create` audit entry; click the row to see
   the before/after diff.

This flow was walked through manually end-to-end against a real running backend during
development, including the cross-reference panel and the before/after diff expansion.
