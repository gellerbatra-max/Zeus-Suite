"""Unit tests for the Sec 2.5 diff-highlight catalogue (app/migration_diff.py). Exercised directly
against constructed source_summary/converted_geometry fixtures rather than through the full
pipeline, since the pipeline's own default options (Step 3's fixed `ImportIgesOptions()`) don't
move or drop outline/notch points for a clean file -- a genuine before/after difference is a
property of the *source data*, not something worth contorting a real IGES fixture to produce."""

from app.migration_diff import compute_diff


def _source_summary(raw_lines: list[dict], raw_points: list[dict]) -> dict:
    return {"raw_lines": raw_lines, "raw_points": raw_points, "line_count": len(raw_lines), "point_count": len(raw_points)}


def _outline_lines(points: list[tuple[float, float]]) -> list[dict]:
    n = len(points)
    return [
        {"x1": points[i][0], "y1": points[i][1], "x2": points[(i + 1) % n][0], "y2": points[(i + 1) % n][1], "label": "OUTLINE"}
        for i in range(n)
    ]


def _geometry(perimeter: list[tuple[float, float]], notches: list[str] = ()) -> dict:
    return {
        "perimeter": [{"point_ref": f"p{i + 1}", "x": x, "y": y, "type": "corner"} for i, (x, y) in enumerate(perimeter)],
        "notches": [{"point_ref": ref, "notch_type": "V"} for ref in notches],
    }


def test_identical_geometry_has_no_diff():
    points = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    summary = _source_summary(_outline_lines(points), [{"x": 100.0, "y": 0.0, "label": "NOTCH"}])
    geometry = _geometry(points, notches=["p2"])

    diff = compute_diff(summary, geometry)
    assert diff["perimeter_offset"] is None
    assert diff["moved_points"] == []
    assert diff["notches"] == {"added": [], "removed": [], "moved": []}


def test_uniform_translation_reports_perimeter_offset():
    raw = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    converted = [(x + 5.0, y + 12.0) for x, y in raw]
    summary = _source_summary(_outline_lines(raw), [])
    geometry = _geometry(converted)

    diff = compute_diff(summary, geometry)
    assert diff["moved_points"] == []
    assert diff["perimeter_offset"] is not None
    assert diff["perimeter_offset"]["magnitude_mm"] == 13.0  # 3-4-5-style triangle: hypot(5, 12)


def test_non_uniform_change_reports_individual_moved_points():
    raw = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    converted = [(0.0, 0.0), (110.0, 0.0), (100.0, 100.0), (0.0, 100.0)]  # only point index 1 moved
    summary = _source_summary(_outline_lines(raw), [])
    geometry = _geometry(converted)

    diff = compute_diff(summary, geometry)
    assert diff["perimeter_offset"] is None
    assert len(diff["moved_points"]) == 1
    assert diff["moved_points"][0]["index"] == 1
    assert diff["moved_points"][0]["distance_mm"] == 10.0


def test_mismatched_vertex_count_skips_point_level_diff():
    raw = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0)]  # triangle
    converted = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]  # square
    summary = _source_summary(_outline_lines(raw), [])
    geometry = _geometry(converted)

    diff = compute_diff(summary, geometry)
    assert diff["perimeter_offset"] is None
    assert diff["moved_points"] == []  # neither a uniform offset nor a point-by-point diff applies


def test_notch_added_removed_and_moved():
    points = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    raw_notches = [
        {"x": 100.0, "y": 0.0, "label": "NOTCH"},  # will move slightly -> "moved"
        {"x": 0.0, "y": 100.0, "label": "NOTCH"},  # missing from converted -> "removed"
    ]
    summary = _source_summary(_outline_lines(points), raw_notches)
    # Converted: the first notch nudged 5mm, plus a brand-new one not present in the raw source.
    geometry = _geometry(points, notches=[])
    geometry["perimeter"][1]["x"] = 105.0  # simulate the notch's anchor point having shifted
    geometry["notches"] = [{"point_ref": "p2", "notch_type": "V"}, {"point_ref": "p3", "notch_type": "V"}]

    diff = compute_diff(summary, geometry)
    assert len(diff["notches"]["moved"]) == 1
    assert diff["notches"]["moved"][0]["distance_mm"] == 5.0
    assert len(diff["notches"]["added"]) == 1
    assert diff["notches"]["added"][0] == {"x": 100.0, "y": 100.0}
    assert len(diff["notches"]["removed"]) == 1
    assert diff["notches"]["removed"][0] == {"x": 0.0, "y": 100.0}


def test_missing_inputs_return_none():
    assert compute_diff(None, {"perimeter": []}) is None
    assert compute_diff({"raw_lines": []}, None) is None
