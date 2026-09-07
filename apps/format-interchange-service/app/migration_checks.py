"""The Legacy Migration classification pipeline (format_interchange_plan.md Sec 2.3/2.4, Step 3 of
Sec 7's phased build plan): the error and warning catalogues, each translated into a concrete check
function against this suite's data model.

Most catalogue rows need legacy-system data this suite's own geometry model has no concept of yet
-- corner-treatment types, plaid/stripe match lines, grade-rule-table references, size-synonym
tables, grade-axis assignments, flip/rotation flags. A real DXF/AAMA-ASTM source parser (Sec 6:
"one parser module per supported source format... each normalizing to the same internal
piece-geometry representation") would extract these directly from the source file's own
structures. Since Step 3 only builds an IGES-based source path (reusing Step 2's reader/pipeline
per Sec 7's own instruction, and IGES carries none of this legacy-specific metadata), the caller
supplies it explicitly per item as `LegacyMetadata` alongside the uploaded file -- this keeps every
catalogue check real and independently testable now, and is the natural extension point a future
DXF/AAMA-ASTM parser module would populate automatically instead of requiring the caller to.

Two catalogue rows are NOT check functions here:
- `self_intersection` -- already enforced by `import_pipeline.run_import_pipeline` (via
  `geometry.validate_perimeter`) before a `PieceGeometryDocument` even exists to classify; a
  self-intersecting outline surfaces as an `ImportPipelineError`, translated to a finding by the
  caller (app/api/migration.py) rather than re-detected here. "every graded size" from the
  catalogue's own wording is out of scope -- no grading integration exists yet (see
  app/geometry.py's own scope note), so only the base-size outline is checked.
- `multiple_grain_lines` -- already detected by the import pipeline itself (as a `warning`, since a
  single-piece import can reasonably auto-resolve it by using the first grain line); this
  classification layer re-emits the same signal at `error` severity instead, since a legacy-batch
  item should not silently commit with an ambiguous grain line the way a manually-reviewed
  single-piece import can.
"""

from dataclasses import dataclass, field
from math import acos, degrees, hypot

from pydantic import BaseModel

from app.geometry import PieceGeometryDocument

DESCRIPTION_MAX_LEN = 20  # Sec 2.4: "Piece message has been truncated (32->20-char field)"
MATCH_LINE_ANGLE_TOLERANCE_DEG = 5.0


class CornerTreatment(BaseModel):
    point_ref: str
    treatment: str
    valid_angle_min_deg: float
    valid_angle_max_deg: float


class MatchLine(BaseModel):
    point_refs: list[str]


class GradeRuleReference(BaseModel):
    point_ref: str
    rule_number: int


class GradePoint(BaseModel):
    point_ref: str
    requires_axis: bool = False
    axis_dx: float | None = None
    axis_dy: float | None = None


class LegacyMetadata(BaseModel):
    """Per-item legacy-system metadata a real source-format parser would extract; see this
    module's own docstring for why the caller supplies it directly in this slice."""

    description: str | None = None
    corner_treatments: list[CornerTreatment] = []
    match_lines: list[MatchLine] = []
    grade_rule_table_ref: str | None = None
    # This suite has no grade-rule-table registry yet (Sec 4's platform data model doesn't define
    # one) -- the caller supplies the set of names that WOULD resolve, standing in for that
    # registry lookup until one exists.
    known_rule_tables: list[str] = []
    rule_references: list[GradeRuleReference] = []
    valid_rule_numbers: list[int] = []
    unavailable_rule_references: list[GradeRuleReference] = []
    tangent_rule_points: list[str] = []
    size_synonyms: dict[str, str | None] = {}
    grade_points: list[GradePoint] = []
    flip_applied: bool = False
    old_grain_angle_deg: float | None = None
    new_grain_angle_deg: float | None = None
    rotation_type: str | None = None  # "F" triggers rotation_behavior_change
    cut_line_present: bool = True
    # Simulates a failed structural/checksum check on the source's own grade-rule data -- a real
    # parser would run this against the source format's own table structure.
    grading_source_corrupt: bool = False


@dataclass
class Finding:
    code: str
    severity: str  # error | warning
    message: str
    geometry_ref: dict = field(default_factory=dict)


def _angle_at(prev_pt, vertex, next_pt) -> float:
    v1x, v1y = prev_pt.x - vertex.x, prev_pt.y - vertex.y
    v2x, v2y = next_pt.x - vertex.x, next_pt.y - vertex.y
    len1, len2 = hypot(v1x, v1y), hypot(v2x, v2y)
    if len1 == 0 or len2 == 0:
        return 0.0
    cos_angle = max(-1.0, min(1.0, (v1x * v2x + v1y * v2y) / (len1 * len2)))
    return degrees(acos(cos_angle))


def _angle_between(v1x: float, v1y: float, v2x: float, v2y: float) -> float:
    """Unsigned angle between two vectors, folded into [0, 90] (a line has no inherent direction,
    so 170 degrees and 10 degrees both mean "nearly parallel")."""
    len1, len2 = hypot(v1x, v1y), hypot(v2x, v2y)
    if len1 == 0 or len2 == 0:
        return 0.0
    cos_angle = max(-1.0, min(1.0, (v1x * v2x + v1y * v2y) / (len1 * len2)))
    angle = degrees(acos(cos_angle))
    return min(angle, 180.0 - angle)


def check_invalid_corner_angle(geometry: PieceGeometryDocument, metadata: LegacyMetadata) -> list[Finding]:
    findings = []
    n = len(geometry.perimeter)
    index_by_ref = {p.point_ref: i for i, p in enumerate(geometry.perimeter)}
    for ct in metadata.corner_treatments:
        idx = index_by_ref.get(ct.point_ref)
        if idx is None:
            continue
        vertex = geometry.perimeter[idx]
        prev_pt = geometry.perimeter[(idx - 1) % n]
        next_pt = geometry.perimeter[(idx + 1) % n]
        angle = _angle_at(prev_pt, vertex, next_pt)
        if not (ct.valid_angle_min_deg <= angle <= ct.valid_angle_max_deg):
            findings.append(
                Finding(
                    "invalid_corner_angle",
                    "error",
                    f"Point {ct.point_ref} has a {angle:.1f}° corner angle, outside the valid "
                    f"range [{ct.valid_angle_min_deg}, {ct.valid_angle_max_deg}] for treatment "
                    f"'{ct.treatment}'.",
                    {"point_ref": ct.point_ref, "angle_deg": angle, "treatment": ct.treatment},
                )
            )
    return findings


def check_source_grading_corrupt(metadata: LegacyMetadata) -> list[Finding]:
    if metadata.grading_source_corrupt:
        return [
            Finding(
                "source_grading_corrupt",
                "error",
                "Source grade rule table failed structural validation.",
                {"grade_rule_table_ref": metadata.grade_rule_table_ref},
            )
        ]
    return []


def check_invalid_match_line(geometry: PieceGeometryDocument, metadata: LegacyMetadata) -> list[Finding]:
    if not geometry.grain_line or not metadata.match_lines:
        return []
    gx = geometry.grain_line.end.x - geometry.grain_line.start.x
    gy = geometry.grain_line.end.y - geometry.grain_line.start.y
    points_by_ref = {p.point_ref: p for p in geometry.perimeter}
    findings = []
    for ml in metadata.match_lines:
        if len(ml.point_refs) != 2:
            continue
        a = points_by_ref.get(ml.point_refs[0])
        b = points_by_ref.get(ml.point_refs[1])
        if a is None or b is None:
            continue
        angle = _angle_between(gx, gy, b.x - a.x, b.y - a.y)
        if MATCH_LINE_ANGLE_TOLERANCE_DEG < angle < (90.0 - MATCH_LINE_ANGLE_TOLERANCE_DEG):
            findings.append(
                Finding(
                    "invalid_match_line",
                    "error",
                    f"Match line {ml.point_refs} is {angle:.1f}° from the grain line, not within "
                    "tolerance of 0°/90°.",
                    {"point_refs": ml.point_refs, "angle_deg": angle},
                )
            )
    return findings


def check_rule_table_missing(metadata: LegacyMetadata) -> list[Finding]:
    if metadata.grade_rule_table_ref and metadata.grade_rule_table_ref not in metadata.known_rule_tables:
        return [
            Finding(
                "rule_table_missing",
                "error",
                f"Grade rule table '{metadata.grade_rule_table_ref}' could not be resolved.",
                {"grade_rule_table_ref": metadata.grade_rule_table_ref},
            )
        ]
    return []


def check_unresolvable_size_synonym(metadata: LegacyMetadata) -> list[Finding]:
    unresolved = [source for source, target in metadata.size_synonyms.items() if not target]
    if unresolved:
        return [
            Finding(
                "unresolvable_size_synonym",
                "error",
                f"{len(unresolved)} size synonym(s) do not resolve to a platform size: {unresolved}.",
                {"unresolved": unresolved},
            )
        ]
    return []


def check_missing_grade_axis(metadata: LegacyMetadata) -> list[Finding]:
    findings = []
    for gp in metadata.grade_points:
        if gp.requires_axis and (gp.axis_dx is None or gp.axis_dy is None):
            findings.append(
                Finding(
                    "missing_grade_axis",
                    "error",
                    f"Grade point {gp.point_ref} requires a reference axis but none is defined.",
                    {"point_ref": gp.point_ref},
                )
            )
    return findings


def check_invalid_rule_reference(metadata: LegacyMetadata) -> list[Finding]:
    valid = set(metadata.valid_rule_numbers)
    findings = []
    for rr in metadata.rule_references:
        if rr.rule_number not in valid:
            findings.append(
                Finding(
                    "invalid_rule_reference",
                    "error",
                    f"Point {rr.point_ref} references rule {rr.rule_number}, which does not resolve.",
                    {"point_ref": rr.point_ref, "rule_number": rr.rule_number},
                )
            )
    return findings


def check_flip_grain_realigned(metadata: LegacyMetadata) -> list[Finding]:
    if metadata.flip_applied:
        return [
            Finding(
                "flip_grain_realigned",
                "warning",
                f"Piece was flipped; grain line realigned from {metadata.old_grain_angle_deg}° "
                f"to {metadata.new_grain_angle_deg}°.",
                {"old_grain_angle_deg": metadata.old_grain_angle_deg, "new_grain_angle_deg": metadata.new_grain_angle_deg},
            )
        ]
    return []


def check_rotation_behavior_change(metadata: LegacyMetadata) -> list[Finding]:
    if metadata.rotation_type == "F":
        return [
            Finding(
                "rotation_behavior_change",
                "warning",
                "Grain line uses F Rotation, which will not rotate the same way during nesting; "
                "spot-check Marker Making behavior for this piece.",
                {"rotation_type": metadata.rotation_type},
            )
        ]
    return []


def check_description_truncated(metadata: LegacyMetadata) -> list[Finding]:
    if metadata.description and len(metadata.description) > DESCRIPTION_MAX_LEN:
        return [
            Finding(
                "description_truncated",
                "warning",
                f"Description truncated to {DESCRIPTION_MAX_LEN} characters.",
                {"original": metadata.description, "truncated": metadata.description[:DESCRIPTION_MAX_LEN]},
            )
        ]
    return []


def check_cut_line_absent(metadata: LegacyMetadata) -> list[Finding]:
    if not metadata.cut_line_present:
        return [
            Finding(
                "cut_line_absent_used_sew_perimeter",
                "warning",
                "Cut lines not present in source; sew-line perimeter used for comparison.",
                {},
            )
        ]
    return []


def check_rule_unresolved_zero_growth(metadata: LegacyMetadata) -> list[Finding]:
    return [
        Finding(
            "rule_unresolved_zero_growth",
            "warning",
            f"Rule {rr.rule_number} for point {rr.point_ref} is unavailable; converted to 0 growth.",
            {"point_ref": rr.point_ref, "rule_number": rr.rule_number},
        )
        for rr in metadata.unavailable_rule_references
    ]


def check_invalid_tangent_rule(metadata: LegacyMetadata) -> list[Finding]:
    return [
        Finding(
            "invalid_tangent_rule_zero_growth",
            "warning",
            f"Tangent rule not valid at point {point_ref}; replaced with 0 growth.",
            {"point_ref": point_ref},
        )
        for point_ref in metadata.tangent_rule_points
    ]


_ERROR_CHECKS = (
    check_invalid_corner_angle,
    check_invalid_match_line,
)
_METADATA_ONLY_ERROR_CHECKS = (
    check_source_grading_corrupt,
    check_rule_table_missing,
    check_unresolvable_size_synonym,
    check_missing_grade_axis,
    check_invalid_rule_reference,
)
_WARNING_CHECKS = (
    check_flip_grain_realigned,
    check_rotation_behavior_change,
    check_description_truncated,
    check_cut_line_absent,
    check_rule_unresolved_zero_growth,
    check_invalid_tangent_rule,
)


def classify_item(geometry: PieceGeometryDocument, metadata: LegacyMetadata) -> list[Finding]:
    """Runs the full Sec 2.3/2.4 catalogue (minus self_intersection/multiple_grain_lines -- see
    module docstring) against one item's converted geometry and supplied legacy metadata."""
    findings: list[Finding] = []
    for check in _ERROR_CHECKS:
        findings.extend(check(geometry, metadata))
    for check in _METADATA_ONLY_ERROR_CHECKS:
        findings.extend(check(metadata))
    for check in _WARNING_CHECKS:
        findings.extend(check(metadata))
    return findings
