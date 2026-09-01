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


class MatchingRuleTableOut(BaseModel):
    id: str
    name: str
    method: str
    plaid_repeat: float | None
    stripe_repeat: float | None
    offsets: OffsetsIn
    stripe_definitions: list[StripeDefinitionOut]
    stripe_marks: list[StripeMarkOut]
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
