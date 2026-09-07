"""Pydantic request/response schemas for the Section 4 REST surface. One module, since the
shapes are small and mostly mirror the ORM models directly -- splitting per-entity would just add
import overhead for no organizational benefit at this size."""

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkflowStatusOut(BaseModel):
    code: str
    label: str


class Page(BaseModel):
    items: list[Any]
    page: int
    page_size: int
    total: int


# -- Auth / session (4.1) --------------------------------------------------------------------


class MeOut(BaseModel):
    id: uuid.UUID
    username: str
    full_name: str
    organization_id: uuid.UUID
    permissions: list[str]


# -- Folders (4.2) ------------------------------------------------------------------------------


class FolderCreate(BaseModel):
    parent_id: uuid.UUID | None = None
    name: str
    folder_type: str = "general"


class FolderRename(BaseModel):
    name: str


class FolderMove(BaseModel):
    new_parent_id: uuid.UUID | None


class FolderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    parent_id: uuid.UUID | None
    name: str
    path: str
    folder_type: str
    version: int
    created_at: datetime
    created_by: uuid.UUID


# -- Pieces (4.3) -------------------------------------------------------------------------------


class PieceCreate(BaseModel):
    folder_id: uuid.UUID
    piece_code: str
    piece_name: str
    piece_type: str = "pattern"
    base_size: str | None = None
    description: str | None = None


class PiecePatch(BaseModel):
    piece_name: str | None = None
    description: str | None = None
    base_size: str | None = None
    folder_id: uuid.UUID | None = None


class PieceOut(BaseModel):
    id: uuid.UUID
    folder_id: uuid.UUID
    piece_code: str
    piece_name: str
    piece_type: str
    base_size: str | None
    description: str | None
    current_version_id: uuid.UUID | None
    workflow_status: WorkflowStatusOut
    lock_owner_id: uuid.UUID | None
    version: int
    created_at: datetime
    created_by: uuid.UUID


class StatusTransitionRequest(BaseModel):
    to_status: str
    comment: str | None = None


class BeginVersionRequest(BaseModel):
    file_format: str = "native"
    size_bytes: int
    comment: str | None = None


class BeginVersionResponse(BaseModel):
    version_id: uuid.UUID
    upload_url: str
    upload_method: str = "PUT"
    expires_at: datetime


class CompleteVersionRequest(BaseModel):
    checksum_sha256: str


class DownloadUrlResponse(BaseModel):
    download_url: str
    expires_at: datetime


# -- Styles (4.4) -------------------------------------------------------------------------------


class StyleCreate(BaseModel):
    folder_id: uuid.UUID
    style_number: str
    style_name: str
    season: str | None = None
    customer: str | None = None
    description: str | None = None


class StylePatch(BaseModel):
    style_name: str | None = None
    season: str | None = None
    customer: str | None = None
    description: str | None = None
    folder_id: uuid.UUID | None = None


class StyleOut(BaseModel):
    id: uuid.UUID
    folder_id: uuid.UUID
    style_number: str
    style_name: str
    season: str | None
    customer: str | None
    description: str | None
    workflow_status: WorkflowStatusOut
    version: int
    created_at: datetime
    created_by: uuid.UUID


class StylePieceAdd(BaseModel):
    piece_id: uuid.UUID
    piece_role: str = "primary"
    sequence: int = 0


class StylePieceOut(BaseModel):
    piece_id: uuid.UUID
    piece_role: str
    sequence: int


# -- Markers (4.5) ------------------------------------------------------------------------------


class MarkerCreate(BaseModel):
    folder_id: uuid.UUID
    marker_code: str
    marker_name: str
    order_id: uuid.UUID | None = None
    fabric_width: float | None = None


class MarkerPatch(BaseModel):
    marker_name: str | None = None
    fabric_width: float | None = None
    matching_method: str | None = None
    matching_rule_table_id: uuid.UUID | None = None
    marker_length: float | None = None
    ply_count: int | None = None
    utilization_pct: float | None = Field(default=None, ge=0, le=100)
    fabric_weight_per_unit_area: float | None = None
    splice_min_length: float | None = None
    splice_max_length: float | None = None
    splice_margin: float | None = None
    splice_separation: float | None = None
    force_layrule_name: str | None = None
    layrule_search_table_id: uuid.UUID | None = None


class MarkerOut(BaseModel):
    id: uuid.UUID
    folder_id: uuid.UUID
    marker_code: str
    marker_name: str
    order_id: uuid.UUID | None
    fabric_width: float | None
    marker_length: float | None
    ply_count: int | None
    utilization_pct: float | None
    fabric_weight_per_unit_area: float | None
    splice_min_length: float | None
    splice_max_length: float | None
    splice_margin: float | None
    splice_separation: float | None
    force_layrule_name: str | None
    layrule_search_table_id: uuid.UUID | None
    matching_method: str | None
    matching_rule_table_id: uuid.UUID | None
    current_version_id: uuid.UUID | None
    workflow_status: WorkflowStatusOut
    version: int
    created_at: datetime
    created_by: uuid.UUID


class MarkerPieceIn(BaseModel):
    piece_id: uuid.UUID
    piece_version_id: uuid.UUID
    size_code: str
    quantity: int
    placement_data: dict | None = None


class MarkerPieceOut(MarkerPieceIn):
    pass


# -- Matching rule tables (Marker Making Sec 1.4/2, new) ------------------------------------------


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
    id: uuid.UUID
    name: str
    method: str
    plaid_repeat: float | None
    stripe_repeat: float | None
    offsets_json: dict[str, Any] | None
    stripe_definitions_json: list[dict[str, Any]]
    stripe_marks_json: list[dict[str, Any]]
    weave_line_json: dict[str, Any] | None
    material_pattern_json: dict[str, Any] | None
    version: int
    created_at: datetime
    created_by: uuid.UUID


class WeaveLineReplace(BaseModel):
    angle_deg: float = 0.0
    offset: float = 0.0
    visible: bool = True


class MaterialPatternBeginRequest(BaseModel):
    file_format: str = "png"
    size_bytes: int


class MaterialPatternBeginResponse(BaseModel):
    upload_url: str
    storage_container: str
    storage_key: str
    expires_at: datetime


class MaterialPatternCompleteRequest(BaseModel):
    storage_container: str
    storage_key: str
    checksum_sha256: str
    material_name: str | None = None


class MaterialPatternVisibility(BaseModel):
    visible: bool = True


class OffsetsReplace(BaseModel):
    horizontal: list[float] = []
    vertical: list[float] = []


class JsonArrayReplace(BaseModel):
    items: list[dict[str, Any]]


# -- Block / buffer / fuse-blocking (Marker Making Sec 1.6, new) ----------------------------------


class BlockBufferRuleTableCreate(BaseModel):
    name: str
    rule_no: int
    rule_type: str
    mode: str
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
    id: uuid.UUID
    name: str
    rule_no: int
    rule_type: str
    mode: str
    left_amt: float
    top_amt: float
    right_amt: float
    bottom_amt: float
    version: int
    created_at: datetime
    created_by: uuid.UUID


class FuseBlockCreate(BaseModel):
    piece_placement_ids: list[str]
    x: float
    y: float
    width: float
    height: float
    block_amount: float = 0.5
    reduce_amount: float = 0.0


class FuseBlockPatch(BaseModel):
    piece_placement_ids: list[str] | None = None
    x: float | None = None
    y: float | None = None
    width: float | None = None
    height: float | None = None
    block_amount: float | None = None
    reduce_amount: float | None = None


class FuseBlockOut(BaseModel):
    id: uuid.UUID
    marker_id: uuid.UUID
    shape: str
    x: float
    y: float
    width: float
    height: float
    piece_placement_ids: list[str]
    block_amount: float
    reduce_amount: float
    version: int
    created_at: datetime
    created_by: uuid.UUID


# -- Splice marks (Marker Making Sec 1.8) --------------------------------------------------------


class SpliceMarkCreate(BaseModel):
    start_x: float
    end_x: float
    source: str = "manual"
    roll_id: str | None = None


class SpliceMarkPatch(BaseModel):
    start_x: float | None = None
    end_x: float | None = None
    roll_id: str | None = None


class SpliceMarkOut(BaseModel):
    id: uuid.UUID
    marker_id: uuid.UUID
    start_x: float
    end_x: float
    source: str
    roll_id: str | None
    version: int
    created_at: datetime
    created_by: uuid.UUID


# -- Layrules (Marker Making Sec 1.5) ------------------------------------------------------------


class LayruleSearchTableCreate(BaseModel):
    name: str
    area_compare: bool = True
    area_deviation_pct: float = 5.0
    copy_dynamics: bool = True
    allow_overrides: bool = True
    include_marker_name: bool = True
    include_marker_description: bool = False
    comment: str | None = None


class LayruleSearchTablePatch(BaseModel):
    name: str | None = None
    area_compare: bool | None = None
    area_deviation_pct: float | None = None
    copy_dynamics: bool | None = None
    allow_overrides: bool | None = None
    include_marker_name: bool | None = None
    include_marker_description: bool | None = None
    comment: str | None = None


class LayruleSearchTableOut(BaseModel):
    id: uuid.UUID
    name: str
    area_compare: bool
    area_deviation_pct: float
    copy_dynamics: bool
    allow_overrides: bool
    include_marker_name: bool
    include_marker_description: bool
    comment: str | None
    version: int
    created_at: datetime
    created_by: uuid.UUID


class LayruleCreate(BaseModel):
    name: str
    source_marker_id: uuid.UUID
    placements_json: list[dict[str, Any]]
    comment: str | None = None


class LayrulePatch(BaseModel):
    name: str | None = None
    comment: str | None = None


class LayruleOut(BaseModel):
    id: uuid.UUID
    name: str
    source_marker_id: uuid.UUID
    placements_json: list[dict[str, Any]]
    piece_count: int
    comment: str | None
    version: int
    created_at: datetime
    created_by: uuid.UUID


# -- Orders and bundles (4.6) --------------------------------------------------------------------


class OrderCreate(BaseModel):
    folder_id: uuid.UUID
    order_number: str
    style_id: uuid.UUID
    customer: str | None = None
    due_date: date | None = None


class OrderPatch(BaseModel):
    customer: str | None = None
    due_date: date | None = None
    target_length: float | None = None
    target_utilization_pct: float | None = Field(default=None, ge=0, le=100)
    shrink_x_pct: float | None = Field(default=None, gt=-100)
    shrink_y_pct: float | None = Field(default=None, gt=-100)


class OrderOut(BaseModel):
    id: uuid.UUID
    folder_id: uuid.UUID
    order_number: str
    style_id: uuid.UUID
    customer: str | None
    due_date: date | None
    total_quantity: int
    target_length: float | None
    target_utilization_pct: float | None
    shrink_x_pct: float | None
    shrink_y_pct: float | None
    workflow_status: WorkflowStatusOut
    version: int
    created_at: datetime
    created_by: uuid.UUID


class OrderLineCreate(BaseModel):
    size_code: str
    color: str | None = None
    quantity: int


class OrderLinePatch(BaseModel):
    marker_id: uuid.UUID | None = None
    quantity: int | None = None


class OrderLineOut(BaseModel):
    id: uuid.UUID
    size_code: str
    color: str | None
    quantity: int
    marker_id: uuid.UUID | None


class BundleCreate(BaseModel):
    order_id: uuid.UUID
    marker_id: uuid.UUID
    piece_id: uuid.UUID
    bundle_code: str
    size_code: str
    color: str | None = None
    ply_range_start: int | None = None
    ply_range_end: int | None = None
    quantity: int
    rfid_tag: str | None = None
    qr_code: str | None = None


class BundleOut(BaseModel):
    id: uuid.UUID
    order_id: uuid.UUID
    marker_id: uuid.UUID
    piece_id: uuid.UUID
    bundle_code: str
    rfid_tag: str | None
    qr_code: str | None
    size_code: str
    quantity: int
    workflow_status: WorkflowStatusOut
    cut_at: datetime | None
    version: int
    created_at: datetime
    created_by: uuid.UUID


# -- Search / cross-reference (4.8) --------------------------------------------------------------


class SearchFilters(BaseModel):
    folder_id: uuid.UUID | None = None
    workflow_status: list[str] | None = None
    updated_after: datetime | None = None
    updated_before: datetime | None = None
    customer: str | None = None


class CrossReferenceAnchor(BaseModel):
    """Exactly one field should be set -- the anchor entity results are constrained to be
    connected to (Section 4.8)."""

    piece_id: uuid.UUID | None = None
    style_id: uuid.UUID | None = None
    marker_id: uuid.UUID | None = None
    order_id: uuid.UUID | None = None


DEFAULT_SEARCH_ENTITY_TYPES = ["piece", "style", "marker", "order", "bundle"]


class SearchRequest(BaseModel):
    entity_types: list[str] = DEFAULT_SEARCH_ENTITY_TYPES
    text: str | None = None
    filters: SearchFilters = SearchFilters()
    cross_reference: CrossReferenceAnchor | None = None
    page: int = 1
    page_size: int = 50


class SearchResultRow(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    folder_path: str | None
    workflow_status: str
    updated_at: datetime


class SearchResponse(BaseModel):
    results: dict[str, list[SearchResultRow]]
    total_by_type: dict[str, int]


class SuggestResultRow(BaseModel):
    entity_type: str
    id: uuid.UUID
    code: str
    name: str


class CrossReferenceOut(BaseModel):
    entity_type: str
    id: uuid.UUID
    related: dict[str, list[SearchResultRow]]


# -- Long-running jobs (2.12, 4.12) --------------------------------------------------------------


class JobSubmitRequest(BaseModel):
    job_type: str
    input_ref: dict[str, Any]
    callback_url: str | None = None


class JobOut(BaseModel):
    id: uuid.UUID
    job_type: str
    status: str
    progress_pct: float | None
    result_ref: dict[str, Any] | None
    error_detail: str | None
    submitted_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    timeout_at: datetime | None


class JobEventOut(BaseModel):
    id: int
    occurred_at: datetime
    event_type: str
    detail: dict[str, Any] | None


class HeartbeatRequest(BaseModel):
    progress_pct: float | None = None


class JobCompleteRequest(BaseModel):
    status: str
    result_ref: dict[str, Any] | None = None
    error_detail: str | None = None


# -- Reports (4.10) -----------------------------------------------------------------------------


class ReportDefinitionOut(BaseModel):
    code: str
    name: str
    entity_type: str
    description: str | None


class ReportRunRequest(BaseModel):
    report_code: str
    entity_id: uuid.UUID | None = None
    format: str = "json"


class ReportRunOut(BaseModel):
    id: uuid.UUID
    report_code: str
    status: str
    result_inline: dict[str, Any] | None
    requested_at: datetime
    completed_at: datetime | None


# -- Audit log (4.9) ----------------------------------------------------------------------------


class AuditLogOut(BaseModel):
    id: int
    occurred_at: datetime
    user_id: uuid.UUID | None
    action: str
    entity_type: str
    entity_id: uuid.UUID | None
    result: str
    detail: str | None
    before_state: dict | None
    after_state: dict | None
