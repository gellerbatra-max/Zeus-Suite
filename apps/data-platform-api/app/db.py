from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# All tables live in the `dmp` (Data Management Platform) schema per
# data_management_platform_plan.md Section 2.
metadata = MetaData(schema="dmp")


class Base(DeclarativeBase):
    metadata = metadata


engine = create_engine(settings.database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
