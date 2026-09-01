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
