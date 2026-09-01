# Product Suite Architecture — Final Application List
*The definitive scope for the apparel CAD/CAM/MES product suite, consolidating every decision
made in this engagement: the Gerber AccuMark function catalogue (1,174 functions across Pattern
Design, Marker Making, and Order Entry, plus 21 IGES command-line switches and 28 Style Converter
workflow/error/warning items catalogued separately), the Richpeace DGS/GMS comparison (749
functions), and the enterprise data-management architecture already specified.*

## The four applications

### 1. Data Management Platform (foundation — build first)
The shared substrate every other application reads and writes through: object storage for
pattern/marker/grading files, a relational database for metadata/workflow-status/cross-references/
audit log, a data-browsing application (the modern AccuMark Explorer equivalent), and an identity/
RBAC layer. Full spec already produced: `enterprise_data_architecture.md`.

![Enterprise architecture]({{artifact:63a81843-d85c-4385-a32b-f57626b3a9ae}})

### 2. Pattern Design & Grading
The 2D CAD application for creating, editing, and grading pattern pieces. Scope is the union of
Gerber PDS2000's documented function set (552 functions) and Richpeace DGS's (437 functions),
covering piece creation, point/line editing, seams, darts/pleats, notches, grain lines, grading,
measurement, digitizing input, and plotting. Gerber's greater depth in piece creation, point/line
editing, and darts/pleats sets the bar for those categories; Richpeace's greater depth in grading
granularity and its template/motif reuse feature are folded in as enhancements.

### 3. Marker Making & Production Output (unified)
**This app deliberately does NOT mirror Gerber's split between Marker Making and Order Entry.**
The Richpeace comparison found that Richpeace's single GMS module — bundling nesting, cut-data
generation, plotting/export, and order/piece metadata together — is a real architectural
advantage; Gerber's own split was flagged as a documented differentiator gap in the earlier
research pass, not a design worth repeating. This app owns:
- Manual and automatic nesting, including **both** automation strategies found in the comparison:
  Gerber's Layrule replay-a-known-good-marker, and Richpeace's algorithmic Auto-Nesting solver.
- The expanded plaid/stripe matching toolset (Richpeace's `Define Stripes` / `Stripe only in a
  set` / `Overlapped checking` pattern, richer than Gerber's).
- Fuse-blocking and bundle management at Gerber's documented depth (Gerber's clear advantage).
- Cut-data generation, plot/export to cutter, and order/piece metadata (Richpeace's GMS strength,
  Gerber's Order Entry strength) — unified in one module.
- Bundle/RFID/QR tracking hooks (the CAD-issued bundle_id integration designed earlier in this
  project, closing the gap identified with the user's own production team).

### 4. Format Interchange & Legacy Migration Utility
The smallest app: IGES import/export (piece-level CAD interchange) and a Style-Converter-equivalent
legacy-migration utility (bulk-converting an incoming customer's/predecessor system's pattern data
into this suite's native format), including the same kind of viewer-based error/warning triage
Gerber's Style Converter uses.

## Integration model
All three product applications (Pattern Design, Marker Making, Format Interchange) are thin
clients against the Data Management Platform — no local database, consistent with the "thin
client, centralized server" pattern already established. None of them talk to each other
directly; a piece created in Pattern Design becomes visible to Marker Making only via the shared
platform, mirroring how Storage Areas made Gerber's separate applications interoperate.

## Explicitly out of scope for this document set
The differentiator modules from the earlier "advanced product range" research pass (AI-native
pattern generation, a unified 3D digital twin, predictive sustainability analytics) are not
included in this build plan — they were flagged as R&D-track bets in that outline, not near-term
shipping commitments, and are not needed to reach feature-parity with Gerber/Richpeace.
