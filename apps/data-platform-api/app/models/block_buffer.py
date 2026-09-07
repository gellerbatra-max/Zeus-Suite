from sqlalchemy import (
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


class BlockBufferRuleTable(Base):
    __tablename__ = "block_buffer_rule_tables"
    __table_args__ = (UniqueConstraint("organization_id", "rule_no"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    name = Column(Text, nullable=False)
    rule_no = Column(Integer, nullable=False)
    rule_type = Column(Text, nullable=False)
    mode = Column(Text, nullable=False)
    left_amt = Column(Numeric(8, 3), nullable=False, server_default=text("0"))
    top_amt = Column(Numeric(8, 3), nullable=False, server_default=text("0"))
    right_amt = Column(Numeric(8, 3), nullable=False, server_default=text("0"))
    bottom_amt = Column(Numeric(8, 3), nullable=False, server_default=text("0"))
    comment = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))


class FuseBlock(Base):
    __tablename__ = "fuse_blocks"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=False)
    shape = Column(Text, nullable=False, server_default=text("'rectangle'"))
    x = Column(Numeric(10, 3), nullable=False)
    y = Column(Numeric(10, 3), nullable=False)
    width = Column(Numeric(10, 3), nullable=False)
    height = Column(Numeric(10, 3), nullable=False)
    piece_placement_ids = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    block_amount = Column(Numeric(8, 3), nullable=False, server_default=text("0.5"))
    reduce_amount = Column(Numeric(8, 3), nullable=False, server_default=text("0"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))
