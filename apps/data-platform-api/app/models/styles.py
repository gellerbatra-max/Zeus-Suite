from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, TSVECTOR, UUID

from app.db import Base


class Style(Base):
    __tablename__ = "styles"
    __table_args__ = (UniqueConstraint("organization_id", "folder_id", "style_number"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("dmp.folders.id"), nullable=False)
    style_number = Column(Text, nullable=False)
    style_name = Column(Text, nullable=False)
    season = Column(Text)
    customer = Column(Text)
    description = Column(Text)
    workflow_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    search_vector = Column(TSVECTOR)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)


class StylePiece(Base):
    __tablename__ = "style_pieces"
    __table_args__ = (UniqueConstraint("style_id", "piece_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    style_id = Column(UUID(as_uuid=True), ForeignKey("dmp.styles.id"), nullable=False)
    piece_id = Column(UUID(as_uuid=True), ForeignKey("dmp.pieces.id"), nullable=False)
    piece_role = Column(Text, nullable=False, server_default=text("'primary'"))
    sequence = Column(Integer, nullable=False, server_default=text("0"))
    added_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
