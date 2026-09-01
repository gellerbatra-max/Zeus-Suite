from sqlalchemy import BigInteger, Column, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import INET, JSONB, TIMESTAMP, UUID

from app.db import Base


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    occurred_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=True)
    action = Column(Text, nullable=False)
    entity_type = Column(Text, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("dmp.folders.id"), nullable=True)
    before_state = Column(JSONB)
    after_state = Column(JSONB)
    request_id = Column(UUID(as_uuid=True), nullable=False)
    client_app = Column(Text)
    ip_address = Column(INET)
    result = Column(Text, nullable=False)
    detail = Column(Text)
