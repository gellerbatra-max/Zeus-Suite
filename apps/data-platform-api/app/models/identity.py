from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    SmallInteger,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from app.db import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(Text, nullable=False)
    code = Column(Text, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("organization_id", "sso_subject"),
        UniqueConstraint("organization_id", "username"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    organization_id = Column(UUID(as_uuid=True), ForeignKey("dmp.organizations.id"), nullable=False)
    sso_subject = Column(Text, nullable=False)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    full_name = Column(Text, nullable=False)
    status = Column(Text, nullable=False, server_default=text("'active'"))
    last_login_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class ServiceAccount(Base):
    __tablename__ = "service_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False, unique=True)
    client_id = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Role(Base):
    __tablename__ = "roles"

    id = Column(SmallInteger, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(SmallInteger, primary_key=True)
    code = Column(Text, nullable=False, unique=True)
    resource = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
    description = Column(Text, nullable=False)


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(SmallInteger, ForeignKey("dmp.roles.id"), primary_key=True)
    permission_id = Column(SmallInteger, ForeignKey("dmp.permissions.id"), primary_key=True)


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", "folder_id"),)

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    role_id = Column(SmallInteger, ForeignKey("dmp.roles.id"), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("dmp.folders.id"), nullable=True)
    granted_by = Column(UUID(as_uuid=True), ForeignKey("dmp.users.id"), nullable=False)
    granted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
