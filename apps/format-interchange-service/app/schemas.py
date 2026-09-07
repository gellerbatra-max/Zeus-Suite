from pydantic import BaseModel


class ExportIgesRequest(BaseModel):
    """Sec 1.1's export param set, narrowed to what this slice's geometry model and IGES writer
    actually support. `entity_profile` (target-system curve-type preferences) isn't included --
    there's no curve/spline entity type built yet to have preferences about (see
    iges_writer.py's docstring)."""

    include_internal_lines: bool = True
    include_notches: bool = True
    include_grain_line: bool = True


class ExportIgesJobOut(BaseModel):
    job_id: str
    status: str
    piece_id: str
    piece_code: str | None = None
    download_url: str | None = None
    error_detail: str | None = None


class ImportIgesJobOut(BaseModel):
    """The Import Viewer payload (Sec 1.4): job status plus everything needed to render the
    converted-vs-raw comparison and warnings list, without a save round-trip through Pattern
    Design. `geometry`/`source_summary` are omitted once a job is `committed` (the piece itself,
    not this job row, is the source of truth for a committed piece's geometry from then on)."""

    job_id: str
    status: str  # queued | staged | committed | failed
    target_piece_id: str | None = None
    geometry: dict | None = None
    source_summary: dict | None = None
    warnings: list[dict] = []
    error_detail: str | None = None


class ImportProfileIn(BaseModel):
    name: str
    trading_partner: str | None = None
    params: dict = {}


class ImportProfileOut(BaseModel):
    id: str
    name: str
    trading_partner: str | None = None
    params: dict = {}
