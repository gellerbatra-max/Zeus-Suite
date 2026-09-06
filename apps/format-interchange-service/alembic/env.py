from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app import models  # noqa: F401 - populates Base.metadata for autogenerate
from app.config import settings
from app.db import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata

# This service's migrations run against the same shared Postgres instance/database as
# data-platform-api's own -- in local dev, often literally the same database (see this service's
# README). A bare `alembic_version` table would collide with data-platform-api's own migration
# tracking (both would fight over `public.alembic_version`), so this service tracks its own
# history in a distinctly-named table instead. Left in the default `public` schema, not
# `format_interchange`, since Alembic creates the version table before running migration 0001 --
# the one that CREATEs the `format_interchange` schema in the first place.
VERSION_TABLE = "alembic_version_format_interchange"


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table=VERSION_TABLE,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table=VERSION_TABLE,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
