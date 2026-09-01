# Phase-Wise Development Roadmap

*How to sequence building the five applications defined in `suite_architecture.md`. Read alongside
the build-order flowchart below — this document explains the reasoning; the flowchart is the
reference diagram to keep visible while planning sprints.*

![Application build order]({{artifact:65d8bc1e-094e-46a8-a071-d404aadd29d5}})

## Phase 1 — Foundation (sequential; nothing else can start in earnest without it)
**Build:** object storage, relational metadata database, identity/RBAC layer, and the Data
Management App (virtual folder browser, search, Activity Log, reporting) — the full scope of
`data_management_platform_plan.md`.

**Why sequential:** every other application is a thin client against this platform's API. Building
Pattern Design or Marker Making before the platform's data model (piece/style/marker/order schema)
is stable means rework the moment that schema changes. This mirrors why Gerber's own manual treats
Storage Areas as a prerequisite configuration step before any of its five applications run.

**Exit criteria:** the platform API can create/read/update/delete piece and marker records, enforce
a workflow status field, log every action to the audit trail, and authenticate/authorize a request
— even before Pattern Design or Marker Making exist to call it. Stub/mock clients should be able to
exercise the full API.

## Phase 2 — Core applications (parallel, once Phase 1's API is stubbed and stable)
**Build in parallel:** Pattern Design & Grading, and the core of Marker Making (manual + automatic
nesting, matching, fuse-blocking) — deliberately *not* including cut-data/plot/export yet.

**Why these two in parallel:** they depend on the Data Management Platform but not meaningfully on
each other during initial development — Pattern Design produces pieces, Marker Making's core nesting
logic can be developed and tested against synthetic/sample piece data without waiting for Pattern
Design's UI to be finished. Splitting them into two independent build tracks is exactly the kind of
task-seam parallelism that shortens calendar time without adding integration risk, since both only
need the Phase 1 API contract, not each other's internals.

**Exit criteria:** Pattern Design can create, edit, and grade a piece and save it through the
platform; Marker Making can retrieve pieces from the platform, nest them (both automation modes),
and save a marker back through the platform.

## Phase 3 — Production output, 3D & utilities (parallel, depends on Phase 2's data model being real)
**Build in parallel:** the Production Output module (cut-data generation, plot/export, order/piece
metadata, bundle/RFID tracking hooks), the Format Interchange & Legacy Migration Utility, and the
3D Virtual Sampling / Digital Twin application.

**Why these wait for Phase 2 but can run parallel to each other:** Production Output needs a real
marker data model to generate cut data from — it's the direct downstream consumer of Marker
Making's output, so it can't meaningfully start until Marker Making's marker schema is real (not
just planned). The Format Interchange utility needs Pattern Design's piece format to convert into,
for the same reason. The 3D application needs Pattern Design's finished piece data (outlines,
seam/sew-line data, fabric properties) to construct a simulatable garment mesh, so it likewise
can't meaningfully start until Pattern Design's piece schema is real. All three have no dependency
on each other, so once each one's respective upstream data model is real, they proceed in
parallel.

**Exit criteria:** a marker can be turned into cut data, plotted, and exported; a bundle/RFID tag
can be generated from a marker's piece data at the moment of cutting; an external pattern file can
be converted into the suite's native piece format with an error/warning triage report; a finished
pattern piece can be constructed into a 3D garment mesh, draped on an avatar, and reviewed for fit.

## Phase 4 — Integration & hardening (sequential; needs every application present)
**Build:** end-to-end workflow testing (design → nest → cut → track), scale/performance testing
under concurrent multi-user load and large piece/order volumes, and a security/permission audit
covering RBAC coverage and audit-log completeness.

**Why this is last and sequential:** these are cross-cutting concerns that can only be verified
once every application exists and is wired to the real platform — this is where the "built to
enterprise scale from day one" commitment gets tested against the actual ~25,000-piece-class
volumes that broke Gerber's original flat-storage design, rather than assumed.

## Summary table

| Phase | Applications | Parallel or sequential | Depends on |
|---|---|---|---|
| 1 | Data Management Platform | — (single track) | nothing |
| 2 | Pattern Design & Grading; Marker Making (core) | Parallel with each other | Phase 1 API |
| 3 | Production Output; Format Interchange & Migration; 3D Virtual Sampling / Digital Twin | Parallel with each other | Phase 2 data models |
| 4 | Integration & hardening | Sequential (cross-cutting) | All applications present |
