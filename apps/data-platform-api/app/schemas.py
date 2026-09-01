"""Pydantic request/response schemas for the Section 4 REST surface. One module, since the
shapes are small and mostly mirror the ORM models directly -- splitting per-entity would just add
import overhead for no organizational benefit at this size."""

import uuid
from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


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
    matching_method: str | None
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


class OrderOut(BaseModel):
    id: uuid.UUID
    folder_id: uuid.UUID
    order_number: str
    style_id: uuid.UUID
    customer: str | None
    due_date: date | None
    total_quantity: int
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
