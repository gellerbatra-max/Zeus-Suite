from sqlalchemy import (
    BigInteger,
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


class Piece(Base):
    __tablename__ = "pieces"
    __table_args__ = (UniqueConstraint("organization_id", "folder_id", "piece_code"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("dmp.folders.id"), nullable=False)
    piece_code = Column(Text, nullable=False)
    piece_name = Column(Text, nullable=False)
    piece_type = Column(Text, nullable=False, server_default=text("'pattern'"))
    description = Column(Text)
    base_size = Column(Text)
    current_version_id = Column(UUID(as_uuid=True), ForeignKey("dmp.piece_versions.id"), nullable=True)
    workflow_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    lock_owner_id = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=True)
    lock_acquired_at = Column(TIMESTAMP(timezone=True), nullable=True)
    search_vector = Column(TSVECTOR)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))


class PieceVersion(Base):
    __tablename__ = "piece_versions"
    __table_args__ = (UniqueConstraint("piece_id", "version_number"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    piece_id = Column(UUID(as_uuid=True), ForeignKey("dmp.pieces.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    storage_container = Column(Text, nullable=False)
    storage_key = Column(Text, nullable=False)
    file_format = Column(Text, nullable=False, server_default=text("'native'"))
    checksum_sha256 = Column(Text, nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    comment = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
