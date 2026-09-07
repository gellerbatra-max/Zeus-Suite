"""format-interchange-service has its own database (unlike pattern-design-service/
marker-making-service) but still calls data-platform-api for piece metadata + geometry bytes.
Tests need both: a real data-platform-api subprocess (spawned the same way every other service's
tests do -- see marker-making-service/tests/conftest.py for why not an in-process ASGI transport)
AND this service's own schema migrated against the same test database, since its Postgres tables
(interchange_job) are real, not proxied.
"""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx
import pytest
from azure.storage.blob import BlobServiceClient

from app import platform_client

REPO_ROOT = Path(__file__).resolve().parents[2]
SERVICE_DIR = REPO_ROOT / "format-interchange-service"
PLATFORM_DIR = REPO_ROOT / "data-platform-api"
PLATFORM_PYTHON = PLATFORM_DIR / ".venv" / "bin" / "python3"
SERVICE_PYTHON = SERVICE_DIR / ".venv" / "bin" / "python3"
PLATFORM_PORT = 8097
PLATFORM_BASE_URL = f"http://127.0.0.1:{PLATFORM_PORT}"

TEST_DATABASE_URL = "postgresql+psycopg://zeus:zeus@localhost:5432/zeus_suite_format_interchange_test"

_AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)
_STORAGE_CONTAINERS = [
    "dmp-pieces", "dmp-markers", "dmp-nesting-jobs", "dmp-reports", "dmp-audit-archive",
    "format-interchange-exports",
]


def _ensure_storage_containers() -> None:
    service_client = BlobServiceClient.from_connection_string(_AZURITE_CONNECTION_STRING)
    for container in _STORAGE_CONTAINERS:
        container_client = service_client.get_container_client(container)
        if not container_client.exists():
            container_client.create_container()


def _ensure_test_database() -> None:
    """Own isolated database, not the shared `zeus_suite` one -- see this service's README for
    why (another branch/session's own migrations on the shared DB are a real, repeatedly-hit
    collision risk in this monorepo's local-dev setup)."""
    import psycopg

    admin_conn = psycopg.connect("postgresql://zeus:zeus@localhost:5432/zeus_suite", autocommit=True)
    with admin_conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", ("zeus_suite_format_interchange_test",))
        if cur.fetchone() is None:
            cur.execute("CREATE DATABASE zeus_suite_format_interchange_test OWNER zeus")
    admin_conn.close()


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
    if not SERVICE_PYTHON.exists():
        pytest.skip(f"format-interchange-service venv not found at {SERVICE_PYTHON}.")

    _ensure_test_database()

    subprocess.run(
        [str(PLATFORM_PYTHON), "-m", "alembic", "upgrade", "head"],
        cwd=PLATFORM_DIR, check=True, capture_output=True, text=True,
        env={**os.environ, "DATABASE_URL": TEST_DATABASE_URL},
    )
    subprocess.run(
        [str(SERVICE_PYTHON), "-m", "alembic", "upgrade", "head"],
        cwd=SERVICE_DIR, check=True, capture_output=True, text=True,
        env={**os.environ, "DATABASE_URL": TEST_DATABASE_URL},
    )
    _ensure_storage_containers()

    with tempfile.NamedTemporaryFile(mode="w+", prefix="platform-server-", suffix=".log") as log_file:
        proc = subprocess.Popen(
            [str(PLATFORM_PYTHON), "-m", "uvicorn", "app.main:app", "--port", str(PLATFORM_PORT)],
            cwd=PLATFORM_DIR, stdout=log_file, stderr=subprocess.STDOUT, text=True,
            env={**os.environ, "DATABASE_URL": TEST_DATABASE_URL},
        )
        try:
            _wait_for_healthz()
        except Exception:  # noqa: BLE001 - report the subprocess's own output regardless of cause
            proc.terminate()
            log_file.seek(0)
            raise RuntimeError(f"data-platform-api failed to start:\n{log_file.read()}") from None

        platform_client.configure_client(httpx.Client(base_url=PLATFORM_BASE_URL, timeout=30.0))
        yield
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        log_file.seek(0)
        print("\n----- data-platform-api server log (full test session) -----", file=sys.stderr)
        print(log_file.read(), file=sys.stderr)
        print("----- end data-platform-api server log -----\n", file=sys.stderr)


@pytest.fixture(autouse=True)
def _use_test_database(monkeypatch):
    """This service's own DB engine (app/db.py) is created at import time from settings.database_url
    -- point it at the test database for the whole session by patching the module-level `engine`/
    `SessionLocal` the same way conftest patches `platform_client`'s module-level client."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app import db as db_module

    test_engine = create_engine(TEST_DATABASE_URL, future=True)
    monkeypatch.setattr(db_module, "engine", test_engine)
    monkeypatch.setattr(db_module, "SessionLocal", sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False))
    # app/deps.py imports SessionLocal by reference at module load time, so it also needs patching.
    from app import deps as deps_module

    monkeypatch.setattr(deps_module, "SessionLocal", db_module.SessionLocal)
