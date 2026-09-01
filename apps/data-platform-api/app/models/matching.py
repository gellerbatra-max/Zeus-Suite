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


class MatchingRuleTable(Base):
    __tablename__ = "matching_rule_tables"
    __table_args__ = (UniqueConstraint("organization_id", "name"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    name = Column(Text, nullable=False)
    method = Column(Text, nullable=False)
    plaid_repeat = Column(Numeric(10, 4))
    stripe_repeat = Column(Numeric(10, 4))
    offsets_json = Column(JSONB)
    stripe_definitions_json = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    stripe_marks_json = Column(JSONB, nullable=False, server_default=text("'[]'::jsonb"))
    comment = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))
