# Enterprise Data Management Architecture
*Modeled on Gerber AccuMark's proven three-layer design, rebuilt with modern technology for an
enterprise-scale apparel CAD/CAM product bundle.*

## Why this shape, not a lighter one
The staged recommendation from earlier in this project (start at StyleCAD's lightweight
files-plus-Access-database tier) was scoped to smaller/mid-size shops. At enterprise scale, the
constraints that forced Gerber to add a real SQL layer — concurrent multi-user editing,
referential integrity across thousands of cross-referenced pieces/markers/orders, and Gerber's own
documented flat-storage ceiling of roughly 25,000 pieces — apply from day one, not after growth.
Building the full model now avoids a disruptive mid-life migration.

![Architecture]({{artifact:63a81843-d85c-4385-a32b-f57626b3a9ae}})

## Layer-by-layer mapping: Gerber's design -> modern equivalent

| Gerber AccuMark (legacy) | What it actually provided | Modern equivalent | Why this substitution |
|---|---|---|---|
| Flat/default Storage Area (folder-look-alike with embedded status fields like Made/Unmade/Approved) | A workflow-status layer that blocks invalid actions (e.g. "cannot process the marker prior to approval") | **Object storage (Azure Blob Storage)** for the actual pattern/marker/grading files, versioned | Object storage gives durable, versioned, horizontally-scalable binary storage without the ~25,000-item ceiling a single flat directory hits: enterprise cloud object stores are designed for millions of objects natively. |
| MSDE / SQL Storage Areas (.mdf/.ldf database files, Device+SQL-name configuration, workgroup connections) | Centralized, queryable, concurrently-editable records; a client machine needs no local database install, only connection info | **PostgreSQL or a managed cloud SQL service** (e.g. Cloud SQL / RDS) holding piece, style, marker, and order records, cross-references, workflow status, and search indices | A modern managed relational database gives the same "thin client, centralized server" model Gerber's manual describes, but with mature replication, backup, and scaling well beyond what MSDE (a 2000s embedded SQL Server edition) was built for. |
| AccuMark Explorer (browse drives/storage areas, view data items, generate reports, import/export/manage data, monitor plotters) | The one application every worker actually touches for file/data management | **A purpose-built data management application** — folder-style virtual browsing (so it feels identical to a familiar file browser), structured cross-reference search (the Find utility's modern equivalent), reporting, an Activity Log viewer, and the DXF/AAMA-ASTM format converters already scoped earlier in this project | Keeps the UI paradigm workers already expect (addressing the change-management point raised earlier about Gerber's own legacy-menu-compatibility mode) while running on infrastructure that scales. |
| Dual "NT and SQL permissions" (Windows share permission + separate SQL Server grant) required to reach another machine's storage area | Two independent checks before data is reachable: network/identity layer, then data-layer authorization | **Enterprise SSO/identity provider for authentication + role-based access control (RBAC) inside the app/database for authorization** | Directly analogous two-layer model, implemented with standard enterprise identity tooling (SAML/OIDC) instead of Windows-domain-specific NT permissions. |
| Activity Log (audit trail of jobs processed, successes/failures) | A record of who did what, for troubleshooting and accountability | **Structured audit log table in the same database**, exposed through the data management app's Activity Log viewer | Same function, queryable by user/date/job-type rather than a flat log file. |

## What stays deliberately the same in spirit
- **The folder metaphor in the UI.** Workers should still browse "storage areas" that look and
  behave like folders — that's a proven, zero-retraining-cost interface choice Gerber, StyleCAD,
  and Tukatech all preserve in their own ways. What changes is what's underneath it.
- **Thin clients, centralized data.** Just as a Gerber machine "does not need to have MSDE
  installed in order to access other systems that have SQL storage areas... it only needs the
  connection information," the CAD applications (Pattern Design, Marker Making, Order Entry
  equivalents) should be thin clients against the central service — no local database to manage,
  patch, or lose sync with.

## What to build first
1. **Object storage + relational metadata DB**, wired together (DB rows reference object storage
   keys) — this is the foundation everything else depends on.
2. **Identity/RBAC layer** — non-negotiable at enterprise scale from day one, unlike the smaller-
   shop path where a simpler login model might suffice initially.
3. **The data management app itself** (virtual folder browser + search + activity log) — this is
   the direct AccuMark Explorer equivalent and the piece workers will interact with daily.
4. **Format converters and reporting** — lower priority than the above three, but should reuse the
   same underlying metadata schema rather than being bolted on separately.
