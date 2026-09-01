from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.db import Base


class Bundle(Base):
    __tablename__ = "bundles"
    __table_args__ = (UniqueConstraint("organization_id", "bundle_code"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("dmp.orders.id"), nullable=False)
    marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=False)
    piece_id = Column(UUID(as_uuid=True), ForeignKey("dmp.pieces.id"), nullable=False)
    bundle_code = Column(Text, nullable=False)
    rfid_tag = Column(Text, unique=True)
    qr_code = Column(Text, unique=True)
    size_code = Column(Text, nullable=False)
    color = Column(Text)
    ply_range_start = Column(Integer)
    ply_range_end = Column(Integer)
    quantity = Column(Integer, nullable=False)
    workflow_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    cut_at = Column(TIMESTAMP(timezone=True))
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
