from typing import Any

from pydantic import BaseModel


class PlacementData(BaseModel):
    x: float
    y: float
    rotation_deg: float = 0
    flip_x: bool = False
    flip_y: bool = False
    width: float
    height: float
    stripe_mark_id: str | None = None
    cutter_stripe_needed: bool = True
    weave_line_angle_deg: float | None = None
    weave_line_offset: float | None = None
    stripe_independent_in_set: bool = False
    block_buffer_rule_no: int | None = None
    bundle_id: str | None = None


class PlacementIn(BaseModel):
    piece_id: str
    size_code: str
    quantity: int = 1
    placement_data: PlacementData


class WorkspacePiece(BaseModel):
    """A style piece available to nest, with a synthetic width/height standing in for real
    silhouette geometry -- Pattern Design doesn't exist yet to provide the real outline."""

    id: str
    piece_code: str
    piece_name: str
    width: float
    height: float


class WorkspacePlacement(BaseModel):
    piece_id: str
    piece_version_id: str | None
    size_code: str
    quantity: int
    placement_data: dict[str, Any]


class WorkspaceOut(BaseModel):
    marker_id: str
    marker_code: str
    workflow_status: str
    order_id: str | None
    style_id: str | None
    fabric_width: float | None = None
    matching_method: str | None = None
    matching_rule_table_id: str | None = None
    available_pieces: list[WorkspacePiece]
    placements: list[WorkspacePlacement]


class SaveWorkspaceRequest(BaseModel):
    placements: list[PlacementIn]


class NestingJobSubmitRequest(BaseModel):
    marker_id: str
    order_id: str


class NestingJobOut(BaseModel):
    id: str
    status: str
    progress_pct: float | None
    result_ref: dict[str, Any] | None
    error_detail: str | None


# -- Matching (marker_making_production_plan.md Sec 1.4, new) -----------------------------------


class OffsetsIn(BaseModel):
    horizontal: list[float] = []
    vertical: list[float] = []


class StripeDefinitionIn(BaseModel):
    name: str
    kind: str = "stripe"  # stripe | grid | stamp | imitation
    origin_x: float = 0.0
    origin_y: float = 0.0
    h_distance: float = 0.0
    v_distance: float = 0.0
    h_angle_deg: float = 0.0
    v_angle_deg: float = 90.0
    params_abcd: dict[str, float] | None = None


class StripeDefinitionPatch(BaseModel):
    name: str | None = None
    kind: str | None = None
    origin_x: float | None = None
    origin_y: float | None = None
    h_distance: float | None = None
    v_distance: float | None = None
    h_angle_deg: float | None = None
    v_angle_deg: float | None = None
    params_abcd: dict[str, float] | None = None


class StripeDefinitionOut(StripeDefinitionIn):
    id: str


class StripeMarkIn(BaseModel):
    name: str
    size: float = 1.0
    stripe_definition_id: str | None = None
    position: dict[str, float] = {}


class StripeMarkPatch(BaseModel):
    name: str | None = None
    size: float | None = None
    stripe_definition_id: str | None = None
    position: dict[str, float] | None = None


class StripeMarkOut(StripeMarkIn):
    id: str
    sequence: int


class StripeMarkStepRequest(BaseModel):
    direction: str  # "next" | "prev"


class MatchingRuleTableCreate(BaseModel):
    name: str
    method: str
    plaid_repeat: float | None = None
    stripe_repeat: float | None = None


class MatchingRuleTablePatch(BaseModel):
    name: str | None = None
    method: str | None = None
    plaid_repeat: float | None = None
    stripe_repeat: float | None = None


class WeaveLineIn(BaseModel):
    angle_deg: float = 0.0
    offset: float = 0.0
    visible: bool = True


class MaterialPatternInfo(BaseModel):
    name: str | None = None
    visible: bool = True


class MatchingRuleTableOut(BaseModel):
    id: str
    name: str
    method: str
    plaid_repeat: float | None
    stripe_repeat: float | None
    offsets: OffsetsIn
    stripe_definitions: list[StripeDefinitionOut]
    stripe_marks: list[StripeMarkOut]
    weave_line: WeaveLineIn | None
    material_pattern: MaterialPatternInfo | None
    version: int


class ApplyMatchingRequest(BaseModel):
    matching_rule_table_id: str | None = None
    matching_method: str | None = None


class MatchGuidanceRequest(BaseModel):
    piece_id: str
    stripe_mark_id: str | None = None
    x: float
    y: float


class MatchGuidanceTarget(BaseModel):
    axis: str
    dx: float
    dy: float
    target_x: float
    target_y: float


class MatchGuidanceOut(BaseModel):
    found: bool
    targets: list[MatchGuidanceTarget]
    message: str | None = None


class BiteViolation(BaseModel):
    piece_id_a: str
    piece_id_b: str
    stripe_mark_id: str
    bite_index_a: int
    bite_index_b: int


class ValidateBiteOut(BaseModel):
    bite_length: float
    ok: bool
    violations: list[BiteViolation]


# -- Define Material / Material Pattern (marker_making_production_plan.md Sec 1.4, new) ----------


class MaterialPatternBeginRequest(BaseModel):
    file_format: str = "png"
    size_bytes: int


class MaterialPatternBeginResponse(BaseModel):
    upload_url: str
    storage_container: str
    storage_key: str
    expires_at: str


class MaterialPatternCompleteRequest(BaseModel):
    storage_container: str
    storage_key: str
    checksum_sha256: str
    material_name: str | None = None


class MaterialPatternVisibilityRequest(BaseModel):
    visible: bool = True


class MaterialPatternDownloadUrlOut(BaseModel):
    download_url: str
    expires_at: str


# -- Block / buffer / fuse-blocking (marker_making_production_plan.md Sec 1.6, new) --------------


class BlockBufferRuleTableCreate(BaseModel):
    name: str
    rule_no: int
    rule_type: str  # block | buffer
    mode: str  # static | dynamic
    left_amt: float = 0.0
    top_amt: float = 0.0
    right_amt: float = 0.0
    bottom_amt: float = 0.0


class BlockBufferRuleTablePatch(BaseModel):
    name: str | None = None
    rule_no: int | None = None
    rule_type: str | None = None
    mode: str | None = None
    left_amt: float | None = None
    top_amt: float | None = None
    right_amt: float | None = None
    bottom_amt: float | None = None


class BlockBufferRuleTableOut(BaseModel):
    id: str
    name: str
    rule_no: int
    rule_type: str
    mode: str
    left_amt: float
    top_amt: float
    right_amt: float
    bottom_amt: float
    version: int


class CreateFuseBlockRequest(BaseModel):
    piece_ids: list[str]
    block_amount: float = 0.5
    reduce_amount: float = 0.0


class ModifyFuseBlockRequest(BaseModel):
    piece_ids: list[str] | None = None
    block_amount: float | None = None
    reduce_amount: float | None = None


class FuseBlockOut(BaseModel):
    id: str
    marker_id: str
    shape: str
    x: float
    y: float
    width: float
    height: float
    piece_placement_ids: list[str]
    block_amount: float
    reduce_amount: float
    notch_depth: float
    version: int


# -- Material calculation / utilization (Sec 1.7) ------------------------------------------------


class MaterialSummaryOut(BaseModel):
    fabric_width: float | None
    ply_count: int | None
    fabric_weight_per_unit_area: float | None
    marker_length: float | None
    utilization_pct: float | None
    computed_marker_length: float | None
    computed_total_piece_area: float | None
    computed_total_perimeter: float | None
    computed_utilization_pct: float | None
    target_length: float | None
    target_utilization_pct: float | None


class MaterialPatchRequest(BaseModel):
    ply_count: int | None = None
    fabric_weight_per_unit_area: float | None = None


class OrderTargetPatchRequest(BaseModel):
    target_length: float | None = None
    target_utilization_pct: float | None = None


class RequiredLengthRequest(BaseModel):
    target_efficiency_pct: float


class RequiredLengthOut(BaseModel):
    required_length: float


class MaterialWeightRequest(BaseModel):
    weight_per_unit_area: float | None = None
    plies: int | None = None
    length: float | None = None


class MaterialWeightOut(BaseModel):
    weight: float


# -- Marker transformations (Sec 1.9) -------------------------------------------------------------


class ShrinkStretchPatchRequest(BaseModel):
    shrink_x_pct: float | None = None
    shrink_y_pct: float | None = None


class TransformSettingsOut(BaseModel):
    fabric_width: float | None
    shrink_x_pct: float | None
    shrink_y_pct: float | None


class ChangeWidthRequest(BaseModel):
    fabric_width: float


class ChangeWidthOut(BaseModel):
    fabric_width: float


# -- Splice marks / fabric-roll handling (Sec 1.8) -------------------------------------------------


class SpliceMarkOut(BaseModel):
    id: str
    marker_id: str
    start_x: float
    end_x: float
    source: str
    roll_id: str | None
    version: int


class SpliceMarkCreateRequest(BaseModel):
    start_x: float
    end_x: float
    roll_id: str | None = None


class SpliceMarkPatchRequest(BaseModel):
    start_x: float | None = None
    end_x: float | None = None
    roll_id: str | None = None


class SpliceSettingsOut(BaseModel):
    min_length: float | None
    max_length: float | None
    margin: float | None
    separation: float | None


class SpliceSettingsPatchRequest(BaseModel):
    min_length: float | None = None
    max_length: float | None = None
    margin: float | None = None
    separation: float | None = None


class AutoSpliceRequest(BaseModel):
    roll_length: float


# -- Layrules (Sec 1.5) -----------------------------------------------------------------------


class LayruleSearchTableCreateRequest(BaseModel):
    name: str
    area_compare: bool = True
    area_deviation_pct: float = 5.0
    copy_dynamics: bool = True
    allow_overrides: bool = True
    include_marker_name: bool = True
    include_marker_description: bool = False
    comment: str | None = None


class LayruleSearchTablePatchRequest(BaseModel):
    name: str | None = None
    area_compare: bool | None = None
    area_deviation_pct: float | None = None
    copy_dynamics: bool | None = None
    allow_overrides: bool | None = None
    include_marker_name: bool | None = None
    include_marker_description: bool | None = None
    comment: str | None = None


class LayruleSearchTableOut(BaseModel):
    id: str
    name: str
    area_compare: bool
    area_deviation_pct: float
    copy_dynamics: bool
    allow_overrides: bool
    include_marker_name: bool
    include_marker_description: bool
    comment: str | None
    version: int


class LayruleOut(BaseModel):
    id: str
    name: str
    source_marker_id: str
    piece_count: int
    comment: str | None
    version: int


class LayrulePatchRequest(BaseModel):
    name: str | None = None
    comment: str | None = None


class CaptureLayruleRequest(BaseModel):
    name: str
    comment: str | None = None


class ApplyLayruleRequest(BaseModel):
    layrule_id: str


class ApplyLayruleResult(BaseModel):
    applied_piece_ids: list[str]
    unmatched_piece_ids: list[str]
    area_deviation_pct: float | None
    warning: str | None


class LayruleSettingsPatchRequest(BaseModel):
    force_layrule_name: str | None = None
    layrule_search_table_id: str | None = None
