"""marker-making-service has no database and no ORM models of its own -- its tests need a real
data-platform-api running, exactly like production. This starts that service as a real subprocess
(not an in-process ASGI transport: both services' top-level package is named `app`, so importing
data-platform-api's `app.main` into this process's `sys.modules["app"]` would collide with this
service's own `app` package) using the platform's own venv, waits for /healthz, and points
app.platform_client at it for the whole test session.

Requires: apps/data-platform-api/.venv already set up (see that service's README) and its
Postgres + Azurite containers running (docker compose up -d from the repo root).
"""

import subprocess
import time
from pathlib import Path

import httpx
import pytest

from app import platform_client

REPO_ROOT = Path(__file__).resolve().parents[2]
PLATFORM_DIR = REPO_ROOT / "data-platform-api"
PLATFORM_PYTHON = PLATFORM_DIR / ".venv" / "bin" / "python3"
PLATFORM_PORT = 8099
PLATFORM_BASE_URL = f"http://127.0.0.1:{PLATFORM_PORT}"


def _wait_for_healthz(timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            response = httpx.get(f"{PLATFORM_BASE_URL}/healthz", timeout=2.0)
            if response.status_code == 200:
                return
        except httpx.HTTPError as exc:
            last_error = exc
        time.sleep(0.5)
    raise RuntimeError(f"data-platform-api did not become healthy in time: {last_error}")


@pytest.fixture(scope="session", autouse=True)
def platform_server():
    if not PLATFORM_PYTHON.exists():
        pytest.skip(f"data-platform-api venv not found at {PLATFORM_PYTHON} -- set it up first (see its README).")

    subprocess.run(
        [str(PLATFORM_PYTHON), "-m", "alembic", "upgrade", "head"],
        cwd=PLATFORM_DIR, check=True, capture_output=True, text=True,
    )

    proc = subprocess.Popen(
        [str(PLATFORM_PYTHON), "-m", "uvicorn", "app.main:app", "--port", str(PLATFORM_PORT)],
        cwd=PLATFORM_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    try:
        _wait_for_healthz()
    except Exception:  # noqa: BLE001 - report the subprocess's own output regardless of cause
        proc.terminate()
        output = proc.stdout.read() if proc.stdout else ""
        raise RuntimeError(f"data-platform-api failed to start:\n{output}") from None

    platform_client.configure_client(httpx.Client(base_url=PLATFORM_BASE_URL, timeout=30.0))
    yield
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
