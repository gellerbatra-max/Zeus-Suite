from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# format_interchange_plan.md Sec 4: "This service's own database ... holds only
# interchange-specific bookkeeping" -- interchange_job, import_profile, migration_batch,
# migration_item, migration_finding. Unlike pattern-design-service (a pure thin client, no DB of
# its own), this app genuinely owns tables, in the same shared Postgres instance as every other
# app, namespaced into its own schema -- same multi-tenancy convention data-platform-api's own
# `dmp` schema uses.
metadata = MetaData(schema="format_interchange")


class Base(DeclarativeBase):
    metadata = metadata


engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
