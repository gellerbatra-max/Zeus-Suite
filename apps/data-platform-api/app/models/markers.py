from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, TSVECTOR, UUID

from app.db import Base


class Marker(Base):
    __tablename__ = "markers"
    __table_args__ = (UniqueConstraint("organization_id", "folder_id", "marker_code"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("dmp.folders.id"), nullable=False)
    marker_code = Column(Text, nullable=False)
    marker_name = Column(Text, nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("dmp.orders.id"), nullable=True)
    fabric_width = Column(Numeric(8, 2))
    marker_length = Column(Numeric(10, 2))
    ply_count = Column(Integer)
    utilization_pct = Column(Numeric(5, 2))
    matching_method = Column(Text)
    current_version_id = Column(UUID(as_uuid=True), ForeignKey("dmp.marker_versions.id"), nullable=True)
    workflow_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    search_vector = Column(TSVECTOR)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))


class MarkerVersion(Base):
    __tablename__ = "marker_versions"
    __table_args__ = (UniqueConstraint("marker_id", "version_number"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    storage_container = Column(Text, nullable=False)
    storage_key = Column(Text, nullable=False)
    file_format = Column(Text, nullable=False, server_default=text("'native'"))
    checksum_sha256 = Column(Text, nullable=False)
    size_bytes = Column(BigInteger, nullable=False)
    comment = Column(Text)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class MarkerPiece(Base):
    __tablename__ = "marker_pieces"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=False)
    piece_id = Column(UUID(as_uuid=True), ForeignKey("dmp.pieces.id"), nullable=False)
    piece_version_id = Column(UUID(as_uuid=True), ForeignKey("dmp.piece_versions.id"), nullable=False)
    size_code = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    placement_data = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
