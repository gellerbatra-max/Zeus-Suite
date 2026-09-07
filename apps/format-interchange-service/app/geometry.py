"""A mirror of pattern-design-service's `PieceGeometryDocument` (app/schemas.py there), covering
only the fields the §1.1 IGES entity mapping needs (outline, internal lines, notches, grain line --
not seams/darts/grade_rule_table/annotations/measurements, out of scope for Step 1's export-only
slice). This service never imports pattern-design-service's code or calls it over HTTP (Sec 0: "It
never talks to Pattern Design or Marker Making directly") -- it fetches the same Blob Storage bytes
directly from data-platform-api and parses them with its own copy of the shape, the same
cross-service-schema-mirroring pattern `pattern-design-app`'s `api/types.ts` already uses.
"""

from pydantic import BaseModel
from shapely.geometry import LineString, Polygon
from shapely.validation import explain_validity


class Point(BaseModel):
    point_ref: str
    x: float
    y: float
    type: str = "corner"


class InternalLine(BaseModel):
    line_ref: str
    point_refs: list[str]
    line_type: str = "internal"


class Notch(BaseModel):
    point_ref: str
    notch_type: str = "V"
    depth_mm: float = 5.0


class FreePoint(BaseModel):
    point_ref: str
    x: float
    y: float


class GrainLine(BaseModel):
    start: FreePoint
    end: FreePoint
    angle_deg: float


class PieceGeometryDocument(BaseModel):
    schema_version: int = 1
    units: str = "mm"
    perimeter: list[Point] = []
    internal_lines: list[InternalLine] = []
    notches: list[Notch] = []
    grain_line: GrainLine | None = None
    # Everything else (seams, darts, grade_rule_table, annotations, measurements) is ignored by
    # this service's export pipeline -- pydantic drops unknown extra fields by default, so parsing
    # a full pattern-design-service document here doesn't fail, it just reads what it needs.


class ExportValidationError(Exception):
    def __init__(self, code: str, message: str, detail: dict | None = None):
        self.code = code
        self.message = message
        self.detail = detail or {}
        super().__init__(message)


def validate_perimeter(points: list[Point]) -> None:
    """The self-intersection + minimum-point-count check shared by the export validation gate
    (Sec 1.1) and the import pipeline's post-reconstruction check (Sec 1.2/7 Step 2) -- both
    directions need the same "reject with the offending coordinate rather than silently
    producing broken geometry" guarantee Pattern Design's own save validation uses."""
    if len(points) < 3:
        raise ExportValidationError(
            "insufficient_points", "Perimeter needs at least 3 points to form a closed outline."
        )

    coords = [(p.x, p.y) for p in points] + [(points[0].x, points[0].y)]
    ring = LineString(coords)
    if not ring.is_simple:
        # is_simple (LineString self-intersection) has no explain_validity support in Shapely --
        # that's a Polygon/is_valid concept -- so build a Polygon from the same ring purely to get
        # its human-readable "Self-intersection at or near POINT (x y)" message; the ring itself,
        # not the polygon, is the actual thing being validated.
        validity = explain_validity(Polygon(ring))
        raise ExportValidationError(
            "self_intersection",
            f"Perimeter outline self-intersects: {validity}",
            {"perimeter": coords},
        )


def validate_for_export(doc: PieceGeometryDocument) -> None:
    """The export validation gate (Sec 1.1): re-run the same self-intersection and closure checks
    Pattern Design's own save validation uses, before mapping to IGES entities. "A piece that
    fails either check is rejected with the offending segment's coordinates rather than silently
    exporting broken geometry -- Gerber's IGESOUT has no equivalent check.\""""
    validate_perimeter(doc.perimeter)
