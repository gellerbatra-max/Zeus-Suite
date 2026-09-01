from sqlalchemy import Column, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID

from app.db import Base


class ReportDefinition(Base):
    __tablename__ = "report_definitions"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    entity_type = Column(Text, nullable=False)
    description = Column(Text)


class ReportRun(Base):
    __tablename__ = "report_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    report_definition_id = Column(UUID(as_uuid=True), ForeignKey("dmp.report_definitions.id"), nullable=False)
    requested_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    parameters = Column(JSONB, nullable=False)
    status = Column(Text, nullable=False, server_default=text("'pending'"))
    result_storage_key = Column(Text)
    result_inline = Column(JSONB)
    requested_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    completed_at = Column(TIMESTAMP(timezone=True))
