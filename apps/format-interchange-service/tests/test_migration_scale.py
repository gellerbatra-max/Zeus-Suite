"""Step 5 exit criteria (format_interchange_plan.md Sec 7): "load-test batch migration at
realistic legacy-library scale (thousands of styles, per Gerber's own ~2,000-style chunking
guidance as a floor, not a ceiling)." `/run` processes at most `settings.migration_chunk_size`
still-`pending` items per call (app/api/migration.py) -- these tests exercise that chunking logic
both at a small, fast, deterministic scale and at the real multi-thousand-item scale the plan
names."""

import time

from fastapi.testclient import TestClient
from helpers import unique_suffix
from test_migration import _bowtie_iges, _create_batch, _run_batch, _seed_folder

from app.config import settings
from app.main import app

client = TestClient(app)


def _n_copies_of_a_valid_iges_file(n: int) -> dict[str, bytes]:
    """A single hand-built (not exported) valid IGES square, reused under N distinct filenames --
    building N real, independent MigrationItem rows without needing N real platform pieces."""
    doc_text = _valid_square_iges()
    return {f"style-{i:05d}.igs": doc_text for i in range(n)}


def _valid_square_iges() -> bytes:
    from test_import import _assemble_iges

    from app.iges_writer import IgesDocument

    doc = IgesDocument()
    points = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    indices = [
        doc.add_line(points[i][0], points[i][1], points[(i + 1) % 4][0], points[(i + 1) % 4][1], label="OUTLINE")
        for i in range(4)
    ]
    doc.add_composite_curve(indices, label="OUTLINE")
    return _assemble_iges(doc).encode("ascii")


def test_run_only_processes_one_chunk_at_a_time(monkeypatch):
    monkeypatch.setattr(settings, "migration_chunk_size", 3)
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)

    batch = _create_batch(headers, _n_copies_of_a_valid_iges_file(8))
    assert batch["item_count"] == 8

    first = _run_batch(headers, batch["id"])
    assert first["status"] == "running"
    assert first["remaining_pending"] == 5
    assert first["counts"].get("converted", 0) == 3

    second = _run_batch(headers, batch["id"])
    assert second["status"] == "running"
    assert second["remaining_pending"] == 2
    assert second["counts"].get("converted", 0) == 6

    third = _run_batch(headers, batch["id"])
    assert third["status"] == "completed"
    assert third["remaining_pending"] == 0
    assert third["counts"] == {"converted": 8}


def test_run_is_safe_to_call_again_after_completion(monkeypatch):
    monkeypatch.setattr(settings, "migration_chunk_size", 10)
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)
    batch = _create_batch(headers, _n_copies_of_a_valid_iges_file(3))

    _run_batch(headers, batch["id"])
    again = _run_batch(headers, batch["id"])
    assert again["status"] == "completed"
    assert again["counts"] == {"converted": 3}


def test_chunking_still_classifies_error_items_correctly(monkeypatch):
    monkeypatch.setattr(settings, "migration_chunk_size", 2)
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)

    files = _n_copies_of_a_valid_iges_file(3)
    files["bowtie.igs"] = _bowtie_iges().encode("ascii")
    batch = _create_batch(headers, files)

    for _ in range(3):  # 4 items, chunk_size 2 -> 2 calls needed; a 3rd is a safe no-op
        result = _run_batch(headers, batch["id"])
    assert result["status"] == "completed"
    assert result["counts"] == {"converted": 3, "error": 1}


def test_load_test_thousands_of_styles():
    """Sec 7 Step 5's own literal exit criteria: thousands of styles, chunked via the *real*
    default `migration_chunk_size` (2000), not an overridden test value."""
    unique = unique_suffix()
    headers, _folder = _seed_folder(unique)
    item_count = 2200  # > the real default chunk size (2000) -- forces a genuine 2-call chunk sequence

    create_start = time.monotonic()
    batch = _create_batch(headers, _n_copies_of_a_valid_iges_file(item_count))
    create_elapsed = time.monotonic() - create_start
    assert batch["item_count"] == item_count
    assert batch["chunk_count"] == 2

    run_start = time.monotonic()
    first = _run_batch(headers, batch["id"])
    assert first["status"] == "running"
    assert first["remaining_pending"] == item_count - 2000

    second = _run_batch(headers, batch["id"])
    assert second["status"] == "completed"
    assert second["counts"] == {"converted": item_count}
    run_elapsed = time.monotonic() - run_start

    # Generous bounds -- this is a correctness/scale smoke test, not a strict perf benchmark.
    assert create_elapsed < 120
    assert run_elapsed < 120
