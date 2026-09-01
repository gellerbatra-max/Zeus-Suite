from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID

from app.db import Base


class JobType(Base):
    __tablename__ = "job_types"

    id = Column(SmallInteger, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    owning_app = Column(Text, nullable=False)
    default_timeout_seconds = Column(Integer, nullable=False, server_default=text("3600"))
    description = Column(Text)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    job_type_id = Column(SmallInteger, ForeignKey("dmp.job_types.id"), nullable=False)
    status = Column(Text, nullable=False, server_default=text("'queued'"))
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    input_ref = Column(JSONB, nullable=False)
    result_ref = Column(JSONB)
    progress_pct = Column(Numeric(5, 2))
    error_detail = Column(Text)
    queue_message_id = Column(Text)
    worker_instance = Column(Text)
    callback_url = Column(Text)
    submitted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    started_at = Column(TIMESTAMP(timezone=True))
    completed_at = Column(TIMESTAMP(timezone=True))
    timeout_at = Column(TIMESTAMP(timezone=True))
    last_heartbeat_at = Column(TIMESTAMP(timezone=True))


class JobEvent(Base):
    __tablename__ = "job_events"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    job_id = Column(UUID(as_uuid=True), ForeignKey("dmp.jobs.id"), nullable=False)
    occurred_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    event_type = Column(Text, nullable=False)
    detail = Column(JSONB)
