from typing import Any

from pydantic import BaseModel

GEOMETRY_SCHEMA_VERSION = 1


class Point(BaseModel):
    """A perimeter/internal point, keyed by a stable `point_ref` UUID assigned at creation time
    and preserved across edits -- see pattern_design_plan.md Sec 3.3. Grade rules and measurement
    points will reference points by this id once grading (Phase 2.4) exists; nothing does yet."""

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


class PieceGeometryDocument(BaseModel):
    """One structured JSON document per piece per version (pattern_design_plan.md Sec 3.3).
    seams/darts/notches/grain_line/annotations are carried in the schema now so later phases
    don't need a schema_version bump to add them, but no tool writes them yet -- that's Phase 2.3."""

    schema_version: int = GEOMETRY_SCHEMA_VERSION
    units: str = "mm"
    perimeter: list[Point] = []
    internal_lines: list[InternalLine] = []
    seams: list[Any] = []
    darts: list[Any] = []
    notches: list[Any] = []
    grain_line: Any | None = None
    annotations: list[Any] = []


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
