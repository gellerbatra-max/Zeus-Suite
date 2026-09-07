"""Migration Viewer diff-highlight catalogue (format_interchange_plan.md Sec 2.5), computed from
an item's already-stored `source_summary` (raw parsed source) and `converted_geometry` -- both
persisted at classification time (app/api/migration.py's `/run`), so rendering a diff needs no
re-parse.

Two catalogue rows have no computation here: "Curves Different" (no curve/spline entity exists in
this geometry model -- see app/geometry.py's own scope note) and "Sizes has variations and cannot
be converted" (already the `unresolvable_size_synonym` error code from app/migration_checks.py,
surfaced by the Viewer via that finding's own deep link rather than a separate diff computation).

Outline-vertex ordering assumption: raw OUTLINE-labeled lines are read back in Directory-Entry
order, which matches true edge order for anything iges_writer.py produces (this suite's own
exports, and every round-trip test fixture) since it writes them in walk order. A genuinely
external file whose OUTLINE lines are not DE-sequential in edge order would produce a nonsensical
point-by-point diff here; properly re-chaining that case would duplicate import_pipeline.py's own
heuristic chaining for a secondary, best-effort visualization feature, so it's left as a known gap
-- the vertex-count mismatch guard below at least keeps a mis-chained file from producing garbage
"moved point" noise (it just reports no per-point diff instead).
"""

import math

POINT_MOVED_THRESHOLD_MM = 1.0
NOTCH_MATCH_RADIUS_MM = 20.0


def _dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def compute_diff(source_summary: dict | None, converted_geometry: dict | None) -> dict | None:
    if not source_summary or not converted_geometry:
        return None

    raw_outline = [(ln["x1"], ln["y1"]) for ln in source_summary.get("raw_lines", []) if ln.get("label") == "OUTLINE"]
    converted_outline = [(p["x"], p["y"]) for p in converted_geometry.get("perimeter", [])]

    perimeter_offset = None
    moved_points: list[dict] = []
    if raw_outline and len(raw_outline) == len(converted_outline):
        deltas = [(c[0] - r[0], c[1] - r[1]) for r, c in zip(raw_outline, converted_outline, strict=True)]
        avg_dx = sum(d[0] for d in deltas) / len(deltas)
        avg_dy = sum(d[1] for d in deltas) / len(deltas)
        is_uniform_translation = all(_dist(d, (avg_dx, avg_dy)) <= POINT_MOVED_THRESHOLD_MM for d in deltas)
        if is_uniform_translation and _dist((avg_dx, avg_dy), (0, 0)) > POINT_MOVED_THRESHOLD_MM:
            perimeter_offset = {
                "magnitude_mm": _dist((avg_dx, avg_dy), (0, 0)),
                "direction_deg": math.degrees(math.atan2(avg_dy, avg_dx)),
            }
        elif not is_uniform_translation:
            for i, (r, c) in enumerate(zip(raw_outline, converted_outline, strict=True)):
                distance = _dist(r, c)
                if distance > POINT_MOVED_THRESHOLD_MM:
                    moved_points.append(
                        {"index": i, "before": {"x": r[0], "y": r[1]}, "after": {"x": c[0], "y": c[1]}, "distance_mm": distance}
                    )

    raw_notches = [(p["x"], p["y"]) for p in source_summary.get("raw_points", []) if p.get("label") == "NOTCH"]
    points_by_ref = {p["point_ref"]: p for p in converted_geometry.get("perimeter", [])}
    converted_notches = [
        (points_by_ref[n["point_ref"]]["x"], points_by_ref[n["point_ref"]]["y"])
        for n in converted_geometry.get("notches", [])
        if n["point_ref"] in points_by_ref
    ]

    added, moved, matched_raw = [], [], set()
    for cx, cy in converted_notches:
        best_idx, best_dist = None, None
        for i, raw_pt in enumerate(raw_notches):
            if i in matched_raw:
                continue
            d = _dist((cx, cy), raw_pt)
            if best_dist is None or d < best_dist:
                best_idx, best_dist = i, d
        if best_idx is not None and best_dist <= NOTCH_MATCH_RADIUS_MM:
            matched_raw.add(best_idx)
            if best_dist > POINT_MOVED_THRESHOLD_MM:
                rx, ry = raw_notches[best_idx]
                moved.append({"before": {"x": rx, "y": ry}, "after": {"x": cx, "y": cy}, "distance_mm": best_dist})
        else:
            added.append({"x": cx, "y": cy})
    removed = [{"x": x, "y": y} for i, (x, y) in enumerate(raw_notches) if i not in matched_raw]

    return {
        "perimeter_offset": perimeter_offset,
        "moved_points": moved_points,
        "notches": {"added": added, "removed": removed, "moved": moved},
    }
