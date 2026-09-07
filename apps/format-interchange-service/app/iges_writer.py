"""A purpose-built IGES 5.3 ASCII writer (format_interchange_plan.md Sec 6: "no full CAD kernel is
needed -- pieces are flat 2D outlines, not solids... sufficient and keeps the dependency footprint
small"). Implements the entity subset Sec 1.1's mapping table calls for that this service's
geometry model (app/geometry.py) actually has data for:

  outline (straight segments only -- no curve/spline data exists in the geometry model)
    -> Type 110 (Line) per segment, assembled into one Type 102 (Composite Curve)
  internal lines -> Type 110 (Line), independent entities
  grain line     -> Type 110 (Line), independent entity
  notches        -> Type 116 (Point) at the notch location

Deliberately NOT built in this slice: Type 126 (rational B-spline) -- no curve data to map to it;
Type 106 form 11 (Copious Data) for notches with a Type 406 property tagging them as notches, per
the plan's fuller suggestion -- a single Type 116 Point is a faithful-enough placement for a point
that HAS no multi-point shape (this model's notch is one point + a depth/type attribute, not a
point sequence), but it loses the "tagged as a notch" metadata a real Type 406 property entity
would carry; drill holes (Type 116 in the plan's table) -- this geometry model has no distinct
drill-hole concept from a notch. All flagged here rather than silently mapped to Type 110/nothing.

Every record is a fixed 80-column IGES "card": columns 1-72 are content, column 73 is the section
letter (S/G/D/P/T), columns 74-80 are a right-justified sequence number local to that section.
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.geometry import PieceGeometryDocument

LINE_WIDTH = 80
CONTENT_WIDTH = 72


def _card(content: str, section: str, seq: int) -> str:
    if len(content) > CONTENT_WIDTH:
        raise ValueError(f"IGES card content exceeds {CONTENT_WIDTH} columns: {content!r}")
    return content.ljust(CONTENT_WIDTH) + section + str(seq).rjust(7)


def _hollerith(s: str) -> str:
    """IGES's string encoding: "<char count>H<string>", e.g. "5HHello"."""
    return f"{len(s)}H{s}"


@dataclass
class _Entity:
    entity_type: int
    parameter_data: str  # the comma-joined parameter values, WITHOUT the leading type or trailing ';'
    form_number: int = 0
    label: str = ""


@dataclass
class IgesDocument:
    entities: list[_Entity] = field(default_factory=list)

    def add_line(self, x1: float, y1: float, x2: float, y2: float, label: str = "") -> int:
        """Type 110 (Line). Returns this entity's index (1-based, in creation order) -- used as
        the reference when another entity (e.g. a Composite Curve) needs to point back to it."""
        self.entities.append(_Entity(110, f"{x1},{y1},0.0,{x2},{y2},0.0", label=label))
        return len(self.entities)

    def add_point(self, x: float, y: float, label: str = "") -> int:
        """Type 116 (Point)."""
        self.entities.append(_Entity(116, f"{x},{y},0.0", label=label))
        return len(self.entities)

    def add_composite_curve(self, member_indices: list[int], label: str = "") -> int:
        """Type 102 (Composite Curve), referencing other entities by their DE pointer (each
        entity's line-1 sequence number, i.e. (index-1)*2 + 1)."""
        pointers = ",".join(str(_de_pointer(i)) for i in member_indices)
        self.entities.append(_Entity(102, f"{len(member_indices)},{pointers}", label=label))
        return len(self.entities)


def _de_pointer(entity_index_1based: int) -> int:
    """Each entity occupies 2 Directory Entry lines; its "pointer" (used by anything referencing
    it, and as the entity's own Parameter Data back-reference) is its first DE line's sequence
    number: entity 1 -> DE line 1, entity 2 -> DE line 3, entity 3 -> DE line 5, ..."""
    return (entity_index_1based - 1) * 2 + 1


def _start_section(product_name: str) -> list[str]:
    text = f"Zeus Suite Format Interchange export -- {product_name}"
    return [_card(text, "S", 1)]


def _global_section(file_name: str, product_name: str, units: str) -> list[str]:
    now = datetime.now(UTC).strftime("%Y%m%d.%H%M%S")
    units_flag, units_name = (2, "MM") if units == "mm" else (1, "IN")
    params = [
        _hollerith(","),
        _hollerith(";"),
        _hollerith(product_name),
        _hollerith(file_name),
        _hollerith("Zeus Suite"),
        _hollerith("format-interchange-service 0.1"),
        "32",
        "38",
        "6",
        "15",
        "15",
        _hollerith(product_name),
        "1.0",
        str(units_flag),
        _hollerith(units_name),
        "1",
        "0.01",
        _hollerith(now),
        "0.001",
        "10000.0",
        _hollerith("Zeus Suite"),
        _hollerith("Zeus Suite"),
        "11",
        "0",
    ]
    body = ",".join(params) + ";"
    # Wrap across as many 72-col G lines as needed, breaking only between whole parameters so a
    # Hollerith string's character count is never split across a line boundary.
    lines: list[str] = []
    current = ""
    for chunk in _split_preserving_commas(body):
        if len(current) + len(chunk) > CONTENT_WIDTH:
            lines.append(current)
            current = chunk
        else:
            current += chunk
    if current:
        lines.append(current)
    return [_card(line, "G", i + 1) for i, line in enumerate(lines)]


def _split_preserving_commas(body: str) -> list[str]:
    parts = body.split(",")
    return [p + "," for p in parts[:-1]] + [parts[-1]]


def _directory_entries(entities: list[_Entity], pd_line_counts: list[int]) -> list[str]:
    lines: list[str] = []
    pd_start = 1
    for i, entity in enumerate(entities):
        de_seq = i * 2 + 1
        pd_count = pd_line_counts[i]
        line1_fields = [
            str(entity.entity_type),
            str(pd_start),
            "0",
            "0",
            "0",
            "0",
            "0",
            "0",
            "00000000",
        ]
        line1 = "".join(f.rjust(8) for f in line1_fields)
        lines.append(_card(line1, "D", de_seq))

        # Line 2 fields: entity type, line weight, color, param line count, form number,
        # reserved x2 (blank), entity label, entity subscript number -- 9 fields x 8 cols = 72.
        line2_numeric_fields = [
            str(entity.entity_type),
            "0",
            "0",
            str(pd_count),
            str(entity.form_number),
            "",
            "",
        ]
        line2 = (
            "".join(f.rjust(8) for f in line2_numeric_fields)
            + (entity.label or "").ljust(8)[:8]
            + "0".rjust(8)
        )
        lines.append(_card(line2, "D", de_seq + 1))
        pd_start += pd_count
    return lines


def _parameter_data(entities: list[_Entity]) -> tuple[list[str], list[int]]:
    lines: list[str] = []
    line_counts: list[int] = []
    for i, entity in enumerate(entities):
        de_pointer = _de_pointer(i + 1)
        body = f"{entity.entity_type},{entity.parameter_data};"
        # Parameter Data cards reserve columns 65-72 (of the 72-col content area) for the owning
        # DE pointer, so the usable body width is narrower than a plain content card.
        pd_body_width = CONTENT_WIDTH - 8
        chunks = [body[i : i + pd_body_width] for i in range(0, len(body), pd_body_width)] or [""]
        start_seq = len(lines) + 1
        for chunk in chunks:
            content = chunk.ljust(pd_body_width) + str(de_pointer).rjust(8)
            lines.append(_card(content, "P", len(lines) + 1))
        line_counts.append(len(lines) - start_seq + 1)
    return lines, line_counts


def _terminate_section(s: int, g: int, d: int, p: int) -> list[str]:
    content = f"S{s:7d}G{g:7d}D{d:7d}P{p:7d}"
    return [_card(content, "T", 1)]


def write_iges(doc: PieceGeometryDocument, piece_code: str, file_name: str) -> str:
    """Builds the full IGES document. Returns the ASCII text, CRLF-free (IGES cards don't need an
    internal line-length marker beyond the fixed 80 columns, and a plain "\n" join is what every
    IGES reader in practice expects)."""
    iges = IgesDocument()

    outline_indices = [
        iges.add_line(a.x, a.y, b.x, b.y, label="OUTLINE")
        for a, b in _closed_edges(doc.perimeter)
    ]
    if outline_indices:
        iges.add_composite_curve(outline_indices, label="OUTLINE")

    points_by_ref = {p.point_ref: p for p in doc.perimeter}
    for line in doc.internal_lines:
        if len(line.point_refs) != 2:
            continue
        a = points_by_ref.get(line.point_refs[0])
        b = points_by_ref.get(line.point_refs[1])
        if a and b:
            iges.add_line(a.x, a.y, b.x, b.y, label="INTERNAL")

    if doc.grain_line:
        gl = doc.grain_line
        iges.add_line(gl.start.x, gl.start.y, gl.end.x, gl.end.y, label="GRAIN")

    for notch in doc.notches:
        p = points_by_ref.get(notch.point_ref)
        if p:
            iges.add_point(p.x, p.y, label="NOTCH")

    pd_lines, pd_line_counts = _parameter_data(iges.entities)
    de_lines = _directory_entries(iges.entities, pd_line_counts)

    s_lines = _start_section(piece_code)
    g_lines = _global_section(file_name, piece_code, doc.units)
    t_lines = _terminate_section(len(s_lines), len(g_lines), len(de_lines), len(pd_lines))

    all_lines = s_lines + g_lines + de_lines + pd_lines + t_lines
    return "\n".join(all_lines) + "\n"


def _closed_edges(points: list) -> list[tuple]:
    if len(points) < 3:
        return []
    return [(points[i], points[(i + 1) % len(points)]) for i in range(len(points))]
