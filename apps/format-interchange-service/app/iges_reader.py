"""A purpose-built IGES 5.3 ASCII reader -- the symmetrical counterpart to iges_writer.py, parsing
the same fixed-80-column card format back into entities (format_interchange_plan.md Sec 1.2/Sec 7
Step 2: "Build the IGES reader").

Only parses the entity subset iges_writer.py actually emits (Sec 6's scope: no full CAD kernel,
flat 2D outlines only): Type 110 (Line), Type 116 (Point), Type 102 (Composite Curve). A file
containing other entity types (splines, arcs, property entities) simply has those Directory
Entries skipped -- they carry no data this service's geometry model (app/geometry.py) can hold,
same "flag rather than silently corrupt" posture as the writer's own docstring, except here the
caller (app/import_pipeline.py) is the one that turns "skipped entity" into a warning, since only
it knows whether the skip actually lost meaningful geometry.

Directory Entry Line 2's Entity Label field (columns 9-16, i.e. the 7th of 9 right/left-justified
8-column fields) is read back verbatim -- this is how a round-tripped file recovers "OUTLINE" /
"INTERNAL" / "GRAIN" / "NOTCH" semantics without re-guessing them; a file from an external system
with no recognizable label is still parsed, just with `label == ""`, and it's the pipeline's job
to apply the documented heuristic fallback (largest closed loop = outline) in that case.
"""

from dataclasses import dataclass

CONTENT_WIDTH = 72


class IgesParseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


@dataclass
class ParsedLine:
    x1: float
    y1: float
    x2: float
    y2: float
    label: str
    de_pointer: int  # this entity's own DE pointer, i.e. what a Composite Curve references it by


@dataclass
class ParsedPoint:
    x: float
    y: float
    label: str
    de_pointer: int


@dataclass
class ParsedCompositeCurve:
    label: str
    member_pointers: list[int]


@dataclass
class ParsedIgesDocument:
    units: str  # "mm" | "in", read from the Global section's units flag
    lines: list[ParsedLine]
    points: list[ParsedPoint]
    composite_curves: list[ParsedCompositeCurve]


def _split_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"S": [], "G": [], "D": [], "P": [], "T": []}
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        line = raw_line.ljust(80)
        section = line[72]
        if section not in sections:
            continue
        sections[section].append(line[:CONTENT_WIDTH])
    return sections


def _parse_global_units(g_lines: list[str]) -> str:
    """Field 14 (units flag: 1=in, 2=mm) of the Global section's Hollerith/comma-separated
    parameter list -- the same field iges_writer.py's `_global_section` writes. Defaults to "mm"
    if the Global section is missing or malformed rather than raising, since the units are only
    ever a fallback (an explicit `unit_override` on import always wins -- see import_pipeline.py)."""
    # Global section lines wrap on whole-parameter boundaries (iges_writer.py's `_global_section`),
    # so any line that ends before column 72 has pure padding blanks after its last comma -- strip
    # each line individually before joining, or that padding would land mid-stream as a bogus token.
    body = "".join(line.rstrip() for line in g_lines).rstrip(";").rstrip()
    fields = _split_hollerith_aware(body)
    if len(fields) > 13:
        return "mm" if fields[13].strip() == "2" else "in"
    return "mm"


def _split_hollerith_aware(body: str) -> list[str]:
    """Splits a comma-separated IGES parameter list, respecting Hollerith strings ("<n>H...")
    whose own content may itself contain commas."""
    fields: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        j = i
        while j < n and body[j].isdigit():
            j += 1
        if j > i and j < n and body[j] == "H":
            count = int(body[i:j])
            start = j + 1
            fields.append(body[start : start + count])
            i = start + count
            if i < n and body[i] == ",":
                i += 1
            continue
        comma = body.find(",", i)
        if comma == -1:
            fields.append(body[i:])
            i = n
        else:
            fields.append(body[i:comma])
            i = comma + 1
    return fields


def _de_pointer_for_de_line_index(de_line_index_0based: int) -> int:
    """The DE pointer format both this reader and iges_writer.py use is the entity's first DE
    line's own sequence number (odd numbers: 1, 3, 5, ...) -- see iges_writer.py's `_de_pointer`."""
    return de_line_index_0based + 1


def _parse_directory_entries(d_lines: list[str]) -> list[dict]:
    entries = []
    for i in range(0, len(d_lines) - 1, 2):
        line1, line2 = d_lines[i], d_lines[i + 1]
        entity_type = int(line1[0:8])
        # Line 2 is 7 right-justified 8-col numeric fields (56 cols), then the left-justified
        # 8-col Entity Label field, then a trailing 8-col field -- see iges_writer.py's
        # `_directory_entries` for the exact layout this mirrors.
        label = line2[56:64].strip()
        entries.append(
            {
                "entity_type": entity_type,
                "label": label,
                "de_pointer": _de_pointer_for_de_line_index(i),
            }
        )
    return entries


def _parse_parameter_data(p_lines: list[str]) -> dict[int, str]:
    """Groups PD lines by their owning DE pointer (columns 65-72 of each PD card) and
    concatenates each entity's own lines back into one semicolon-terminated parameter string."""
    by_pointer: dict[int, list[str]] = {}
    for line in p_lines:
        pd_body_width = CONTENT_WIDTH - 8
        content, de_pointer_field = line[:pd_body_width], line[pd_body_width:]
        de_pointer = int(de_pointer_field)
        by_pointer.setdefault(de_pointer, []).append(content)
    return {ptr: "".join(chunks).rstrip() for ptr, chunks in by_pointer.items()}


def parse_iges(text: str) -> ParsedIgesDocument:
    sections = _split_sections(text)
    if not sections["D"] or not sections["P"]:
        raise IgesParseError("File has no Directory Entry / Parameter Data sections -- not a valid IGES file.")
    if len(sections["D"]) % 2 != 0:
        raise IgesParseError("Directory Entry section has an odd number of lines (expected 2 per entity).")

    units = _parse_global_units(sections["G"])
    entries = _parse_directory_entries(sections["D"])
    pd_by_pointer = _parse_parameter_data(sections["P"])

    lines: list[ParsedLine] = []
    points: list[ParsedPoint] = []
    composite_curves: list[ParsedCompositeCurve] = []

    for entry in entries:
        pd_pointer = entry["de_pointer"]
        raw_pd = pd_by_pointer.get(pd_pointer)
        if raw_pd is None:
            continue
        body = raw_pd.rstrip(";")
        fields = _split_hollerith_aware(body)
        if not fields:
            continue
        try:
            entity_type = int(fields[0])
        except ValueError:
            continue
        params = fields[1:]

        if entity_type == 110 and len(params) >= 6:
            lines.append(
                ParsedLine(
                    x1=float(params[0]), y1=float(params[1]),
                    x2=float(params[3]), y2=float(params[4]),
                    label=entry["label"], de_pointer=entry["de_pointer"],
                )
            )
        elif entity_type == 116 and len(params) >= 2:
            points.append(
                ParsedPoint(
                    x=float(params[0]), y=float(params[1]),
                    label=entry["label"], de_pointer=entry["de_pointer"],
                )
            )
        elif entity_type == 102 and params:
            count = int(params[0])
            member_pointers = [int(p) for p in params[1 : 1 + count]]
            composite_curves.append(ParsedCompositeCurve(label=entry["label"], member_pointers=member_pointers))
        # Any other entity type (splines, arcs, property entities) carries no data this service's
        # geometry model can hold -- deliberately skipped, per this module's own docstring.

    return ParsedIgesDocument(units=units, lines=lines, points=points, composite_curves=composite_curves)
