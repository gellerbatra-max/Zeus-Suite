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
