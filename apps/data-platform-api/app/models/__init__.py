"""Import every model module so Base.metadata is fully populated for Alembic autogenerate.

Note: the initial schema (alembic/versions/0001_initial_schema.py) is authored as raw SQL
transcribed from the spec document, not generated from these models -- it owns triggers,
tsvector-update wiring, and gin/trgm indexes that don't have a clean ORM-level representation.
These models are the query-time mapping over that same schema. Keep both in sync by hand when the
schema changes; don't trust `alembic revision --autogenerate` to diff against triggers/tsvector
columns without a careful manual review.
"""

from app.models.audit import AuditLog
from app.models.bundles import Bundle
from app.models.folders import Folder
from app.models.identity import (
    Organization,
    Permission,
    Role,
    RolePermission,
    ServiceAccount,
    User,
    UserRole,
)
from app.models.jobs import Job, JobEvent, JobType
from app.models.markers import Marker, MarkerPiece, MarkerVersion
from app.models.orders import Order, OrderLine
from app.models.pieces import Piece, PieceVersion
from app.models.reports import ReportDefinition, ReportRun
from app.models.styles import Style, StylePiece
from app.models.workflow import WorkflowStatus, WorkflowTransition

__all__ = [
    "AuditLog",
    "Bundle",
    "Folder",
    "Job",
    "JobEvent",
    "JobType",
    "Marker",
    "MarkerPiece",
    "MarkerVersion",
    "Order",
    "OrderLine",
    "Organization",
    "Permission",
    "Piece",
    "PieceVersion",
    "ReportDefinition",
    "ReportRun",
    "Role",
    "RolePermission",
    "ServiceAccount",
    "Style",
    "StylePiece",
    "User",
    "UserRole",
    "WorkflowStatus",
    "WorkflowTransition",
]
