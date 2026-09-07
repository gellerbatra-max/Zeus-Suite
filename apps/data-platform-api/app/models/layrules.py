from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, UUID

from app.db import Base


class LayruleSearchTable(Base):
    __tablename__ = "layrule_search_tables"
    __table_args__ = (UniqueConstraint("organization_id", "name"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    name = Column(Text, nullable=False)
    area_compare = Column(Boolean, nullable=False, server_default=text("true"))
    area_deviation_pct = Column(Numeric(5, 2), nullable=False, server_default=text("5.0"))
    copy_dynamics = Column(Boolean, nullable=False, server_default=text("true"))
    allow_overrides = Column(Boolean, nullable=False, server_default=text("true"))
    include_marker_name = Column(Boolean, nullable=False, server_default=text("true"))
    include_marker_description = Column(Boolean, nullable=False, server_default=text("false"))
    comment = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))


class Layrule(Base):
    __tablename__ = "layrules"
    __table_args__ = (UniqueConstraint("organization_id", "name"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    name = Column(Text, nullable=False)
    source_marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=False)
    placements_json = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    piece_count = Column(Integer, nullable=False, server_default=text("0"))
    comment = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))
