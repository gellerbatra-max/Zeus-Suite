from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic.config import Config
from sqlalchemy.orm import Session

from alembic import command
from app.db import SessionLocal, engine

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _alembic_config() -> Config:
    cfg = Config(str(PROJECT_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(PROJECT_ROOT / "alembic"))
    return cfg


def _drop_everything() -> None:
    """Directly drops the dmp schema and the alembic bookkeeping table, rather than stepping
    through each migration's own downgrade(). 0002's downgrade deletes seed/catalogue rows in FK
    order, which only holds if nothing references them yet -- once tests (or real usage) insert
    entity rows against those seeded ids, that ordering breaks. A direct CASCADE drop is the
    correct way to reset a scratch test database regardless of what data exists on top."""
    with engine.begin() as conn:
        conn.execute(sa.text("DROP SCHEMA IF EXISTS dmp CASCADE"))
        conn.execute(sa.text("DROP TABLE IF EXISTS alembic_version"))


@pytest.fixture(scope="session", autouse=True)
def _migrated_database():
    """Runs the full migration chain (schema + seed data) once for the test session, then tears
    the schema back down. This is the "migrations alone, no manual SQL" path the Milestone 1 exit
    check requires."""
    cfg = _alembic_config()
    _drop_everything()  # defensive cleanup in case a previous run was interrupted
    command.upgrade(cfg, "head")
    yield
    _drop_everything()
    engine.dispose()


@pytest.fixture()
def db_session():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
