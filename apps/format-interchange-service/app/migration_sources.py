"""Legacy source format dispatch (format_interchange_plan.md Sec 6: "one parser module per
supported source format... each normalizing to the same internal piece-geometry representation
before the shared validation/classification pipeline in Sec 2 runs -- new source formats are added
as new parser modules, not new pipeline logic").

Step 3 supports exactly one source format: `iges`, reusing Step 2's reader/pipeline verbatim per
Sec 7's own instruction ("reusing Step 2's geometry-handling code where the source format
allows"). Proprietary-binary and DXF/AAMA-ASTM parsers are new modules for a future slice -- there
is no real specification or sample data for either in this suite to build against yet; this
module is the extension point they would register into.
"""

from app.iges_reader import IgesParseError, parse_iges
from app.import_pipeline import (
    ImportIgesOptions,
    ImportPipelineError,
    ImportPipelineResult,
    run_import_pipeline,
)

SUPPORTED_SOURCE_FORMATS = ("iges",)


class UnsupportedSourceFormatError(Exception):
    def __init__(self, source_format: str):
        self.source_format = source_format
        super().__init__(f"Unsupported source format: {source_format!r}")


def parse_source(source_format: str, raw_bytes: bytes) -> ImportPipelineResult:
    """Raises `UnsupportedSourceFormatError`, `IgesParseError`, or `ImportPipelineError` -- all
    three are caught and translated into a migration_finding by app/api/migration.py."""
    if source_format != "iges":
        raise UnsupportedSourceFormatError(source_format)
    text = raw_bytes.decode("ascii", errors="replace")
    parsed = parse_iges(text)
    return run_import_pipeline(parsed, ImportIgesOptions())


__all__ = ["SUPPORTED_SOURCE_FORMATS", "IgesParseError", "ImportPipelineError", "UnsupportedSourceFormatError", "parse_source"]
