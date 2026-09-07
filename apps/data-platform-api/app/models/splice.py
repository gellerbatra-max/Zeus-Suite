from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.db import Base


class SpliceMark(Base):
    __tablename__ = "splice_marks"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=False)
    start_x = Column(Numeric(10, 3), nullable=False)
    end_x = Column(Numeric(10, 3), nullable=False)
    source = Column(Text, nullable=False)
    roll_id = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))
