from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, TSVECTOR, UUID

from app.db import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("organization_id", "folder_id", "order_number"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("dmp.folders.id"), nullable=False)
    order_number = Column(Text, nullable=False)
    style_id = Column(UUID(as_uuid=True), ForeignKey("dmp.styles.id"), nullable=False)
    customer = Column(Text)
    due_date = Column(Date)
    total_quantity = Column(Integer, nullable=False, server_default=text("0"))
    workflow_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    search_vector = Column(TSVECTOR)
    created_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    version = Column(Integer, nullable=False, server_default=text("1"))


class OrderLine(Base):
    __tablename__ = "order_lines"
    __table_args__ = (UniqueConstraint("order_id", "size_code", "color"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    order_id = Column(UUID(as_uuid=True), ForeignKey("dmp.orders.id"), nullable=False)
    size_code = Column(Text, nullable=False)
    color = Column(Text)
    quantity = Column(Integer, nullable=False)
    marker_id = Column(UUID(as_uuid=True), ForeignKey("dmp.markers.id"), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
