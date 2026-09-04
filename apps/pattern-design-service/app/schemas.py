from pydantic import BaseModel

GEOMETRY_SCHEMA_VERSION = 1


class Point(BaseModel):
    """A perimeter/internal point, keyed by a stable `point_ref` UUID assigned at creation time
    and preserved across edits -- see pattern_design_plan.md Sec 3.3. `GradeRule.point_ref`
    (Phase 2.4) and `Measurement.point_ref_a/b` (Phase 2.5) both reference points by this id."""

    point_ref: str
    x: float
    y: float
    type: str = "corner"


class InternalLine(BaseModel):
    """A straight internal line connecting two existing points by `point_ref` (Gerber's
    "Create Line - 2 Point", pattern_design_plan.md Point/Line Editing Part 2) -- Phase 2.2's
    line-editing slice doesn't yet support lines with their own standalone points or curves, only
    lines between points that already exist on the perimeter or another line."""

    line_ref: str
    point_refs: list[str]
    line_type: str = "internal"


class SeamAllowance(BaseModel):
    """Seam allowance on one perimeter edge (Both/union depth per Sec 4 -- Gerber's allowance
    model + Richpeace's corner-type library). `edge_ref` is the two adjacent perimeter points the
    edge runs between. Corner-mitering across adjacent seamed edges (Sec 4's large cut-corner
    catalogue -- miter, tab, nub, frame, length-fix variants, etc.) is genuinely complex polygon
    offset geometry deferred to a real Shapely-backed implementation; this slice stores the value
    and renders a simple per-edge parallel offset, not a corner-accurate cut line."""

    edge_ref: list[str]
    allowance_mm: float
    corner_type: str = "regular"


class FreePoint(BaseModel):
    """A point that isn't part of the perimeter -- a dart leg/apex or a grain line endpoint. Still
    carries a stable `point_ref` per Sec 3.3's point-identity principle (grading will eventually
    need to reference these too), just not stored in the shared `perimeter` array, since adding it
    there would splice it into the outline polygon."""

    point_ref: str
    x: float
    y: float


class Dart(BaseModel):
    """Gerber depth per Sec 4 (Darts, Pleats & Fullness -- documented to 43 items vs Richpeace's
    24). This slice implements only "Add plain dart": two leg points on the perimeter edge and an
    apex, with an intake amount. Rotate/combine/distribute/fullness variants are deferred."""

    dart_ref: str
    leg_a: FreePoint
    apex: FreePoint
    leg_b: FreePoint
    intake_mm: float


class Notch(BaseModel):
    """Richpeace depth per Sec 4 (Notches & Internal Markings). This slice implements only
    "Add notch (single, at edge location)" anchored to an existing perimeter point -- corner/
    intersection notches, angled notches, and batch placement are deferred."""

    point_ref: str
    notch_type: str = "V"
    depth_mm: float = 5.0


class GrainLine(BaseModel):
    """Richpeace depth per Sec 4 (Grain Line / Fabric Direction -- the one category with no
    Gerber equivalent at all). One grain line per piece; `angle_deg` is derived from start/end at
    creation time, matching Richpeace's two-point-click definition."""

    start: FreePoint
    end: FreePoint
    angle_deg: float


class GradeRule(BaseModel):
    """One point's X/Y growth for one step between two adjacent sizes in the grade rule table's
    `size_range` (Richpeace's "Point Grading" / "Create new delta (X/Y) grading rule", Sec 4
    Grading). `size_step` is the index into `size_range` of the *smaller* size in the step -- e.g.
    for size_range ["S","M","L"], size_step 0 is the S->M increment, size_step 1 is M->L. This is
    the real AccuMark/Gerber grading model (deltas between adjacent sizes, not absolute per-size
    offsets), which is what lets a size outside the table's range still resolve by walking
    cumulative deltas outward from the base size."""

    point_ref: str
    size_step: int
    delta_x: float
    delta_y: float


class GradeRuleTable(BaseModel):
    """A piece's grading definition. pattern_design_plan.md Sec 3.2 proposes `grade_rule_tables`/
    `grade_rules` as their own Postgres tables (namespaced `pattern_design.*`); this keeps them in
    the geometry document instead, for the same reason Sec 3.3 gives for not normalizing points
    into per-point Postgres rows (doesn't scale to hundreds of points x tens of sizes), and because
    Phase 2.1 explicitly deferred the decision of whether this app ever gets a database of its own
    -- see pattern-design-service/README.md. `graded_pieces` (Sec 3.2's materialized per-size piece
    records) is not built in this slice: grading is computed and reviewed live in the canvas
    (pattern_design_plan.md Sec 5.2/6.1's grade-nest overlay) rather than persisted as separate
    platform `pieces` rows per size."""

    size_range: list[str]
    base_size: str
    rules: list[GradeRule] = []


class Annotation(BaseModel):
    """A free-floating text note (Gerber's "Annotate Piece / Add Text", Sec 4 Text/Annotation) --
    placed at an arbitrary x/y, not anchored to an existing perimeter/internal point, matching how
    the real tool works (click anywhere on or near a line to place a note)."""

    annotation_ref: str
    x: float
    y: float
    text: str


class Measurement(BaseModel):
    """A named point-to-point spec measurement (Gerber's "Straight-Line Distance Between Two
    Points" plus the spec-chart concept from pattern_design_plan.md Sec 3.2's `measurement_points`
    table -- kept in the geometry document instead, same reasoning as GradeRuleTable above).
    The actual distance is deliberately NOT stored here: it's computed live from the current point
    positions on every read, so it can never go stale if a point moves after the measurement was
    defined -- the whole point of a spec measurement is catching drift, not freezing a snapshot."""

    measurement_ref: str
    label: str
    point_ref_a: str
    point_ref_b: str
    target_value_mm: float | None = None
    tolerance_mm: float | None = None


class PieceGeometryDocument(BaseModel):
    """One structured JSON document per piece per version (pattern_design_plan.md Sec 3.3)."""

    schema_version: int = GEOMETRY_SCHEMA_VERSION
    units: str = "mm"
    perimeter: list[Point] = []
    internal_lines: list[InternalLine] = []
    seams: list[SeamAllowance] = []
    darts: list[Dart] = []
    notches: list[Notch] = []
    grain_line: GrainLine | None = None
    grade_rule_table: GradeRuleTable | None = None
    annotations: list[Annotation] = []
    measurements: list[Measurement] = []


def empty_geometry_document() -> PieceGeometryDocument:
    return PieceGeometryDocument()


class FolderCreateRequest(BaseModel):
    parent_id: str | None = None
    name: str
    folder_type: str = "general"


class FolderOut(BaseModel):
    id: str
    parent_id: str | None
    name: str
    path: str
    folder_type: str


class PieceCreateRequest(BaseModel):
    folder_id: str
    piece_code: str
    piece_name: str
    piece_type: str = "pattern"
    base_size: str | None = None
    description: str | None = None


class WorkflowStatusOut(BaseModel):
    code: str
    label: str


class PieceOut(BaseModel):
    id: str
    folder_id: str
    piece_code: str
    piece_name: str
    piece_type: str
    base_size: str | None
    description: str | None
    current_version_id: str | None
    workflow_status: WorkflowStatusOut
    version: int


class GeometrySaveResult(BaseModel):
    piece: PieceOut
    geometry: PieceGeometryDocument


class StatusTransitionRequest(BaseModel):
    to_status: str
    comment: str | None = None
