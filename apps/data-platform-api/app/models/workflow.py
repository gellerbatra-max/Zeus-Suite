from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from app.db import Base


class WorkflowStatus(Base):
    __tablename__ = "workflow_statuses"
    __table_args__ = (UniqueConstraint("entity_type", "code"),)

    id = Column(SmallInteger, primary_key=True)
    entity_type = Column(Text, nullable=False)
    code = Column(Text, nullable=False)
    label = Column(Text, nullable=False)
    sequence = Column(SmallInteger, nullable=False)
    is_terminal = Column(Boolean, nullable=False, server_default=text("false"))
    is_initial = Column(Boolean, nullable=False, server_default=text("false"))


class WorkflowTransition(Base):
    __tablename__ = "workflow_transitions"
    __table_args__ = (UniqueConstraint("entity_type", "from_status_id", "to_status_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    entity_type = Column(Text, nullable=False)
    from_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    to_status_id = Column(SmallInteger, ForeignKey("dmp.workflow_statuses.id"), nullable=False)
    required_permission = Column(Text, nullable=False)
