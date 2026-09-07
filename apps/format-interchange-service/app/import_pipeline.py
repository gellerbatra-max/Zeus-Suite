"""The IGES import pipeline (format_interchange_plan.md Sec 1.2/Sec 7 Step 2): turns a parsed IGES
document (app/iges_reader.py) into this service's geometry mirror (app/geometry.py), applying the
option set from Sec 1.2's table as explicit, individually-warned pipeline stages -- Gerber's
`IGES.EXE` applies these silently; this pipeline surfaces every decision it made as a structured
warning instead, per Sec 1.4's "every warning generated during conversion" requirement.

Two reconstruction paths, tried in order:

1. **Composite-curve path** (the round-trip case, and any well-formed external file that follows
   the standard IGES convention of wrapping a closed profile in a Type 102 Composite Curve): the
   chosen composite curve's member Type 110 lines are already in edge order, so the perimeter is
   read directly off them -- no chaining, no guessing, exact reproduction.
2. **Heuristic chaining path** (no composite curve present at all): candidate Type 110 lines are
   chained by matching coincident endpoints into loops; the largest resulting loop is treated as
   the outline (Sec 1.2's own suggested heuristic for unlabeled/external data), and every line
   whose role could not be read from its Entity Label is flagged with a warning rather than
   silently classified.

Deliberately scoped out, with a warning emitted naming the option rather than a silent no-op if the
caller asks for it: `infer_grade_points`/`numbering_scheme` (no grading integration exists in this
service yet -- see app/geometry.py's own scope note), `max_arc_points`/`max_spline_points` (no
arc/spline entity type exists to tessellate -- iges_writer.py never emits one), `force_sharp_corners`
(no curve-smoothing exists in this geometry model to disable in the first place).
"""

import math
from dataclasses import dataclass, field

from pydantic import BaseModel
from shapely.geometry import LineString
from shapely.geometry import Point as ShapelyPoint

from app.geometry import (
    ExportValidationError,
    FreePoint,
    GrainLine,
    InternalLine,
    Notch,
    PieceGeometryDocument,
    Point,
    validate_perimeter,
)
from app.iges_reader import ParsedIgesDocument, ParsedLine

POINT_MATCH_TOLERANCE = 1e-3  # mm: coincident-endpoint matching, chaining, and vertex snapping
MIN_PLAUSIBLE_SPAN_MM = 10.0
MAX_PLAUSIBLE_SPAN_MM = 3000.0


class ImportIgesOptions(BaseModel):
    closure_amount_mm: float = 2.0
    trim_tolerance: float = 0.0
    infer_grade_points: bool = False
    numbering_scheme: str | None = None
    max_arc_points: int | None = None
    max_spline_points: int | None = None
    paste_internal_to_notch: bool = False
    points_to_drill_holes: bool = False
    unit_override: str | None = None
    force_sharp_corners: bool = False
    target_collection: str | None = None
    stage_only: bool = True
    auto_approve: bool = False
    import_profile_id: str | None = None


@dataclass
class ImportWarning:
    code: str
    message: str
    detail: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return {"code": self.code, "message": self.message, "detail": self.detail}


class ImportPipelineError(Exception):
    def __init__(self, code: str, message: str, detail: dict | None = None):
        self.code = code
        self.message = message
        self.detail = detail or {}
        super().__init__(message)


@dataclass
class ImportPipelineResult:
    geometry: PieceGeometryDocument
    warnings: list[ImportWarning]
    source_summary: dict


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _key(pt: tuple[float, float], tolerance: float = POINT_MATCH_TOLERANCE) -> tuple[int, int]:
    return (round(pt[0] / tolerance), round(pt[1] / tolerance))


def _chain_loops(lines: list[ParsedLine]) -> list[dict]:
    """Chains an unordered set of line segments into maximal paths by matching coincident
    endpoints. Returns one entry per resulting path: `{points, closed, gap, line_indices}`."""
    endpoint_index: dict[tuple[int, int], list[tuple[int, bool]]] = {}
    for i, ln in enumerate(lines):
        endpoint_index.setdefault(_key((ln.x1, ln.y1)), []).append((i, True))
        endpoint_index.setdefault(_key((ln.x2, ln.y2)), []).append((i, False))

    used: set[int] = set()
    loops: list[dict] = []
    for i in range(len(lines)):
        if i in used:
            continue
        used.add(i)
        start_pt = (lines[i].x1, lines[i].y1)
        current_end = (lines[i].x2, lines[i].y2)
        points = [start_pt, current_end]
        line_indices = [i]
        closed = False
        while True:
            if _key(current_end) == _key(start_pt) and len(line_indices) > 1:
                closed = True
                break
            candidates = [c for c in endpoint_index.get(_key(current_end), []) if c[0] not in used]
            if not candidates:
                break
            nxt_idx, nxt_is_start = candidates[0]
            used.add(nxt_idx)
            line_indices.append(nxt_idx)
            nxt = lines[nxt_idx]
            next_end = (nxt.x2, nxt.y2) if nxt_is_start else (nxt.x1, nxt.y1)
            points.append(next_end)
            current_end = next_end
        loops.append(
            {
                "points": points[:-1] if closed else points,
                "closed": closed,
                "gap": 0.0 if closed else _dist(current_end, start_pt),
                "line_indices": line_indices,
            }
        )
    return loops


def _reconstruct_outline(
    parsed: ParsedIgesDocument, options: ImportIgesOptions, warnings: list[ImportWarning]
) -> tuple[list[tuple[float, float]], list[ParsedLine]]:
    """Returns (outline_points, leftover_lines) -- leftover_lines are every Type 110 line not
    consumed by the chosen outline, i.e. internal-line and grain-line candidates."""
    lines_by_pointer = {ln.de_pointer: ln for ln in parsed.lines}

    if parsed.composite_curves:
        chosen = next((cc for cc in parsed.composite_curves if cc.label == "OUTLINE"), None)
        if chosen is None:
            chosen = max(parsed.composite_curves, key=lambda cc: len(cc.member_pointers))
            if len(parsed.composite_curves) > 1:
                warnings.append(
                    ImportWarning(
                        "outline_composite_curve_inferred",
                        "Multiple Composite Curves found with no \"OUTLINE\" label; the one with "
                        "the most members was assumed to be the outline.",
                        {"member_count": len(chosen.member_pointers)},
                    )
                )
        member_lines = [lines_by_pointer[p] for p in chosen.member_pointers if p in lines_by_pointer]
        if len(member_lines) != len(chosen.member_pointers):
            raise ImportPipelineError(
                "malformed_composite_curve",
                "The outline Composite Curve references a Line entity that could not be found.",
            )
        outline_points = [(ln.x1, ln.y1) for ln in member_lines]
        consumed_pointers = {ln.de_pointer for ln in member_lines}
        leftover = [ln for ln in parsed.lines if ln.de_pointer not in consumed_pointers]
        return outline_points, leftover

    # No Composite Curve at all -- heuristic chaining over every candidate line not already
    # excluded by an explicit label (Sec 1.2: unlabeled/external data falls back to "largest
    # closed loop = outline").
    candidates = [ln for ln in parsed.lines if ln.label not in ("INTERNAL", "GRAIN")]
    if not candidates:
        raise ImportPipelineError("no_outline_found", "File has no Line entities usable as an outline.")

    loops = _chain_loops(candidates)
    closed_loops = [loop for loop in loops if loop["closed"]]
    if closed_loops:
        outline_loop = max(closed_loops, key=lambda loop: len(loop["points"]))
    else:
        best = max(loops, key=lambda loop: len(loop["points"]))
        if best["gap"] > options.closure_amount_mm:
            raise ImportPipelineError(
                "outline_not_closed",
                f"Largest candidate outline loop has a {best['gap']:.3f}mm gap, exceeding "
                f"closure_amount_mm ({options.closure_amount_mm}mm).",
                {"gap_mm": best["gap"]},
            )
        warnings.append(
            ImportWarning(
                "gap_auto_closed",
                f"Outline loop had a {best['gap']:.3f}mm gap, auto-closed (within closure_amount_mm).",
                {"gap_mm": best["gap"]},
            )
        )
        # Drop the dangling final vertex -- it's within tolerance of the start point, so bridging
        # the gap means closing directly back to the start, not keeping it as its own tiny vertex.
        outline_loop = {**best, "points": best["points"][:-1]}

    if not any(ln.label == "OUTLINE" for ln in candidates):
        warnings.append(
            ImportWarning(
                "outline_inferred_from_unlabeled_geometry",
                "No Composite Curve or \"OUTLINE\"-labeled entity found; the largest closed loop "
                "of line segments was assumed to be the outline.",
                {"vertex_count": len(outline_loop["points"])},
            )
        )

    consumed = {candidates[i].de_pointer for i in outline_loop["line_indices"]}
    leftover = [ln for ln in parsed.lines if ln.de_pointer not in consumed]
    return outline_loop["points"], leftover


def _trim_collinear_indices(points: list[tuple[float, float]], tolerance: float, protected: set[int]) -> set[int]:
    """Single-pass collinear-point removal (Sec 1.2's `-T` trimming), skipping any index a notch,
    internal line, or grain-line endpoint is anchored to -- removing those would silently move a
    referenced feature, which trim_tolerance is not meant to do. Returns the set of indices to
    remove (indices, not coordinates, since outline coordinates are not guaranteed unique)."""
    if tolerance <= 0 or len(points) < 4:
        return set()
    to_remove: set[int] = set()
    n = len(points)
    for i in range(n):
        if i in protected:
            continue
        prev_pt = points[(i - 1) % n]
        next_pt = points[(i + 1) % n]
        seg = LineString([prev_pt, next_pt])
        if seg.length > 0 and seg.distance(ShapelyPoint(points[i])) <= tolerance:
            to_remove.add(i)
    if len(points) - len(to_remove) < 3:
        return set()
    return to_remove


def _match_existing_point(x: float, y: float, perimeter: list[Point]) -> str | None:
    for p in perimeter:
        if _dist((p.x, p.y), (x, y)) <= POINT_MATCH_TOLERANCE:
            return p.point_ref
    return None


def _resolve_or_paste_internal_endpoint(
    x: float, y: float, perimeter: list[Point], next_ref: list[int], options: ImportIgesOptions
) -> tuple[str | None, bool]:
    """Resolves an internal line's endpoint to an existing perimeter point_ref, or -- if it lies on
    an outline edge and `paste_internal_to_notch` is enabled -- splits that edge with a new point
    and returns its ref (Sec 1.2: "convert that endpoint into a notch"). Returns
    (point_ref, became_notch)."""
    existing = _match_existing_point(x, y, perimeter)
    if existing is not None:
        return existing, False

    if not options.paste_internal_to_notch:
        return None, False

    n = len(perimeter)
    for i in range(n):
        a, b = perimeter[i], perimeter[(i + 1) % n]
        seg = LineString([(a.x, a.y), (b.x, b.y)])
        if seg.length == 0:
            continue
        if seg.distance(ShapelyPoint((x, y))) <= POINT_MATCH_TOLERANCE:
            ref = f"p{next_ref[0]}"
            next_ref[0] += 1
            perimeter.insert(i + 1, Point(point_ref=ref, x=x, y=y, type="notch"))
            return ref, True

    return None, False


def run_import_pipeline(parsed: ParsedIgesDocument, options: ImportIgesOptions) -> ImportPipelineResult:
    warnings: list[ImportWarning] = []

    for option_name, requested in (
        ("infer_grade_points", options.infer_grade_points),
        ("max_arc_points", options.max_arc_points),
        ("max_spline_points", options.max_spline_points),
        ("force_sharp_corners", options.force_sharp_corners),
    ):
        if requested:
            warnings.append(
                ImportWarning(
                    "option_not_implemented",
                    f"'{option_name}' was requested but is not implemented in this pipeline; it was ignored.",
                    {"option": option_name},
                )
            )

    outline_coords, leftover_lines = _reconstruct_outline(parsed, options, warnings)

    effective_unit = options.unit_override or parsed.units
    if options.unit_override and options.unit_override != parsed.units:
        warnings.append(
            ImportWarning(
                "unit_override_applied",
                f"File declared unit '{parsed.units}' but unit_override '{options.unit_override}' was used instead.",
                {"file_unit": parsed.units, "unit_override": options.unit_override},
            )
        )
    scale = 25.4 if effective_unit == "in" else 1.0
    outline_coords = [(x * scale, y * scale) for x, y in outline_coords]
    leftover_lines = [
        ParsedLine(x1=ln.x1 * scale, y1=ln.y1 * scale, x2=ln.x2 * scale, y2=ln.y2 * scale, label=ln.label, de_pointer=ln.de_pointer)
        for ln in leftover_lines
    ]
    raw_points_mm = [(p.x * scale, p.y * scale, p.label) for p in parsed.points]

    xs = [c[0] for c in outline_coords]
    ys = [c[1] for c in outline_coords]
    span = max(max(xs) - min(xs), max(ys) - min(ys)) if outline_coords else 0.0
    if span and not (MIN_PLAUSIBLE_SPAN_MM <= span <= MAX_PLAUSIBLE_SPAN_MM):
        warnings.append(
            ImportWarning(
                "implausible_piece_size",
                f"Converted outline's largest bounding-box dimension is {span:.1f}mm, outside the "
                f"plausible range for a garment piece ({MIN_PLAUSIBLE_SPAN_MM}-{MAX_PLAUSIBLE_SPAN_MM}mm) "
                "-- double-check unit_override.",
                {"span_mm": span},
            )
        )

    perimeter = [Point(point_ref=f"p{i + 1}", x=x, y=y, type="corner") for i, (x, y) in enumerate(outline_coords)]
    next_ref = [len(perimeter) + 1]

    grain_lines = [ln for ln in leftover_lines if ln.label == "GRAIN"]
    if len(grain_lines) > 1:
        warnings.append(
            ImportWarning(
                "multiple_grain_lines",
                f"File has {len(grain_lines)} grain-line entities; only one is supported per piece. "
                "The first was used.",
                {"count": len(grain_lines)},
            )
        )
    grain_line = None
    if grain_lines:
        gl = grain_lines[0]
        angle = math.degrees(math.atan2(gl.y2 - gl.y1, gl.x2 - gl.x1))
        grain_line = GrainLine(
            start=FreePoint(point_ref="g1", x=gl.x1, y=gl.y1),
            end=FreePoint(point_ref="g2", x=gl.x2, y=gl.y2),
            angle_deg=angle,
        )

    internal_candidates = [ln for ln in leftover_lines if ln.label in ("INTERNAL", "")]
    unrecognized_leftover_lines = [ln for ln in leftover_lines if ln.label not in ("INTERNAL", "", "GRAIN")]
    for ln in unrecognized_leftover_lines:
        warnings.append(
            ImportWarning(
                "unrecognized_line_label_dropped",
                f"A Line entity labeled '{ln.label}' was not consumed by the outline and is not a "
                "recognized label (INTERNAL/GRAIN/OUTLINE); it was dropped.",
                {"label": ln.label, "x1": ln.x1, "y1": ln.y1, "x2": ln.x2, "y2": ln.y2},
            )
        )

    internal_lines: list[InternalLine] = []
    notches: list[Notch] = []
    for i, ln in enumerate(internal_candidates):
        ref_a, became_notch_a = _resolve_or_paste_internal_endpoint(ln.x1, ln.y1, perimeter, next_ref, options)
        ref_b, became_notch_b = _resolve_or_paste_internal_endpoint(ln.x2, ln.y2, perimeter, next_ref, options)
        if ref_a is None or ref_b is None:
            warnings.append(
                ImportWarning(
                    "internal_line_endpoint_unresolved",
                    "An internal line's endpoint does not coincide with any outline point and could "
                    "not be pasted onto the outline; the line was dropped.",
                    {"x1": ln.x1, "y1": ln.y1, "x2": ln.x2, "y2": ln.y2},
                )
            )
            continue
        if became_notch_a:
            notches.append(Notch(point_ref=ref_a, notch_type="V"))
        if became_notch_b:
            notches.append(Notch(point_ref=ref_b, notch_type="V"))
        internal_lines.append(InternalLine(line_ref=f"l{i + 1}", point_refs=[ref_a, ref_b]))
        if ln.label == "":
            warnings.append(
                ImportWarning(
                    "unlabeled_line_classified_as_internal",
                    "A Line entity outside the outline had no recognizable label; it was treated as an internal line.",
                    {"x1": ln.x1, "y1": ln.y1, "x2": ln.x2, "y2": ln.y2},
                )
            )

    for x, y, label in raw_points_mm:
        ref = _match_existing_point(x, y, perimeter)
        if ref is None:
            code = "notch_point_not_on_outline" if label == "NOTCH" else "unclassified_point_dropped"
            warnings.append(
                ImportWarning(
                    code,
                    f"A Point entity{' labeled NOTCH' if label == 'NOTCH' else ''} does not lie on the "
                    "reconstructed outline (this geometry model anchors points to the outline); it was dropped.",
                    {"x": x, "y": y},
                )
            )
            continue
        if label == "NOTCH":
            notches.append(Notch(point_ref=ref, notch_type="V"))
        elif options.points_to_drill_holes:
            notches.append(Notch(point_ref=ref, notch_type="drill"))
        else:
            warnings.append(
                ImportWarning(
                    "unclassified_point_dropped",
                    "An unlabeled Point entity on the outline was not classified (points_to_drill_holes "
                    "was not requested) and was dropped.",
                    {"x": x, "y": y},
                )
            )

    referenced_refs = {r for il in internal_lines for r in il.point_refs} | {n.point_ref for n in notches}
    protected_indices = {i for i, p in enumerate(perimeter) if p.point_ref in referenced_refs}
    remove_indices = _trim_collinear_indices([(p.x, p.y) for p in perimeter], options.trim_tolerance, protected_indices)
    if remove_indices:
        perimeter = [p for i, p in enumerate(perimeter) if i not in remove_indices]
        warnings.append(
            ImportWarning(
                "points_trimmed",
                f"{len(remove_indices)} near-collinear outline point(s) removed (trim_tolerance={options.trim_tolerance}mm).",
                {"removed_count": len(remove_indices)},
            )
        )

    try:
        validate_perimeter(perimeter)
    except ExportValidationError as exc:
        raise ImportPipelineError(exc.code, exc.message, exc.detail) from exc

    geometry = PieceGeometryDocument(
        units="mm",
        perimeter=perimeter,
        internal_lines=internal_lines,
        notches=notches,
        grain_line=grain_line,
    )

    source_summary = {
        "line_count": len(parsed.lines),
        "point_count": len(parsed.points),
        "composite_curve_count": len(parsed.composite_curves),
        "raw_lines": [{"x1": ln.x1, "y1": ln.y1, "x2": ln.x2, "y2": ln.y2, "label": ln.label} for ln in parsed.lines],
        "raw_points": [{"x": p.x, "y": p.y, "label": p.label} for p in parsed.points],
        "declared_unit": parsed.units,
    }

    return ImportPipelineResult(geometry=geometry, warnings=warnings, source_summary=source_summary)
