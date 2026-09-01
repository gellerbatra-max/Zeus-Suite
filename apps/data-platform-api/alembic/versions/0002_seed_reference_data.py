"""Seed reference/catalogue data: workflow statuses & transitions, permissions, roles,
role_permissions, report_definitions.

Sources: data_management_platform_plan.md Appendix A (workflow statuses), Appendix B (roles +
permission-generation formula), Section 5.3 (permission catalogue), Section 6.4 (report codes).

Two deliberate extensions beyond the literal appendix tables (both appendices are marked
"representative; extend per deployment"), flagged for follow-up:
  - a `bundle` / `cancelled` workflow status, since Section 5.3 states bundles are "never deleted,
    only status-transitioned to cancelled" even though Appendix A's bundle row list omits it.
  - a `job_worker` role holding only `job.worker`, since Appendix B says that permission is
    service-account-only but does not name a role to carry it.

The exact workflow_transitions pairs are not enumerated in the source document (only the status
lists are) -- the set below is a straightforward sequential derivation, provisional pending real
business-rule confirmation.

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-01
"""

import sqlalchemy as sa

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

# -- Workflow statuses ----------------------------------------------------------------------
# (id, entity_type, code, label, sequence, is_initial, is_terminal)
WORKFLOW_STATUSES = [
    (1, "piece", "unmade", "Unmade", 1, True, False),
    (2, "piece", "needs_approval", "Needs Approval", 2, False, False),
    (3, "piece", "made", "Made", 3, False, False),
    (4, "piece", "approved", "Approved", 4, False, True),
    (5, "piece", "cancelled", "Cancelled", 5, False, True),
    (6, "style", "draft", "Draft", 1, True, False),
    (7, "style", "active", "Active", 2, False, False),
    (8, "style", "discontinued", "Discontinued", 3, False, True),
    (9, "marker", "unmade", "Unmade", 1, True, False),
    (10, "marker", "needs_approval", "Needs Approval", 2, False, False),
    (11, "marker", "partial", "Partial", 3, False, False),
    (12, "marker", "made", "Made", 4, False, False),
    (13, "marker", "approved", "Approved", 5, False, True),
    (14, "order", "open", "Open", 1, True, False),
    (15, "order", "in_production", "In Production", 2, False, False),
    (16, "order", "complete", "Complete", 3, False, True),
    (17, "order", "cancelled", "Cancelled", 4, False, True),
    (18, "bundle", "pending", "Pending Cut", 1, True, False),
    (19, "bundle", "cut", "Cut", 2, False, False),
    (20, "bundle", "bundled", "Bundled", 3, False, False),
    (21, "bundle", "sewn", "Sewn", 4, False, False),
    (22, "bundle", "shipped", "Shipped", 5, False, True),
    (23, "bundle", "cancelled", "Cancelled", 6, False, True),  # extension, see module docstring
]

# -- Workflow transitions ---------------------------------------------------------------------
# (entity_type, from_code, to_code) -- required_permission is derived as "<entity>.status.<to_code>"
WORKFLOW_TRANSITIONS = [
    ("piece", "unmade", "needs_approval"),
    ("piece", "needs_approval", "made"),
    ("piece", "made", "approved"),
    ("piece", "unmade", "cancelled"),
    ("piece", "needs_approval", "cancelled"),
    ("piece", "made", "cancelled"),
    ("style", "draft", "active"),
    ("style", "active", "discontinued"),
    ("style", "draft", "discontinued"),
    ("marker", "unmade", "needs_approval"),
    ("marker", "needs_approval", "partial"),
    ("marker", "needs_approval", "made"),
    ("marker", "partial", "made"),
    ("marker", "made", "approved"),
    ("order", "open", "in_production"),
    ("order", "in_production", "complete"),
    ("order", "open", "cancelled"),
    ("order", "in_production", "cancelled"),
    ("bundle", "pending", "cut"),
    ("bundle", "cut", "bundled"),
    ("bundle", "bundled", "sewn"),
    ("bundle", "sewn", "shipped"),
    ("bundle", "pending", "cancelled"),
    ("bundle", "cut", "cancelled"),
    ("bundle", "bundled", "cancelled"),
    ("bundle", "sewn", "cancelled"),
]

# Entities that carry the base read/write/delete + workflow-status permission families
# (Section 5.3). Bundles deliberately have no `.delete` permission.
ENTITY_BASE_ACTIONS = {
    "folder": ["read", "write", "delete"],
    "piece": ["read", "write", "delete"],
    "style": ["read", "write", "delete"],
    "marker": ["read", "write", "delete"],
    "order": ["read", "write", "delete"],
    "bundle": ["read", "write"],
}

STANDALONE_PERMISSIONS = [
    ("search.read", "search", "read"),
    ("audit.read", "audit_log", "read"),
    ("audit.export", "audit_log", "export"),
    ("report.run", "report", "run"),
    ("rbac.read", "rbac", "read"),
    ("rbac.admin", "rbac", "admin"),
    ("piece.force_unlock", "piece", "force_unlock"),
    ("marker.force_unlock", "marker", "force_unlock"),
    ("job.submit", "job", "submit"),
    ("job.read", "job", "read"),
    ("job.cancel", "job", "cancel"),
    ("job.worker", "job", "worker"),
]

ROLES = [
    (1, "admin", "Administrator", "Every permission, org-wide."),
    (2, "pattern_maker", "Pattern Maker", "Creates/edits/deletes pieces; reads/edits styles."),
    (3, "marker_maker", "Marker Maker", "Creates/edits/deletes markers; submits nesting jobs."),
    (4, "production_planner", "Production Planner", "Manages orders and bundle status."),
    (5, "viewer", "Viewer", "Read-only across all resources."),
    (6, "auditor", "Auditor", "Read-only plus audit log access/export."),
    (7, "contractor_qa", "Contractor QA", "Approves pieces/markers; typically folder-scoped."),
    (8, "job_worker", "Job Worker (service account only)", "Holds job.worker; never a human grant."),
]


def _build_permissions():
    """Generate the permission catalogue per Section 5.3 / Appendix B's formula. Returns a list
    of (id, code, resource, action, description) tuples with stable, deterministic ids."""
    rows = []
    next_id = 1

    for entity, actions in ENTITY_BASE_ACTIONS.items():
        for action in actions:
            rows.append((next_id, f"{entity}.{action}", entity, action, f"{action.capitalize()} a {entity}."))
            next_id += 1

    for status_id, entity_type, code, label, *_ in WORKFLOW_STATUSES:
        perm_code = f"{entity_type}.status.{code}"
        rows.append(
            (next_id, perm_code, entity_type, f"status.{code}",
             f"Transition a {entity_type} to '{label}'.")
        )
        next_id += 1

    for code, resource, action in STANDALONE_PERMISSIONS:
        description_map = {
            "job.worker": "Held only by the async nesting-job worker's service account.",
        }
        rows.append((next_id, code, resource, action, description_map.get(code, f"{action.capitalize()} on {resource}.")))
        next_id += 1

    return rows


def _role_permission_codes(all_codes: list[str]) -> dict[str, list[str]]:
    """Resolve each role's permission grants (Appendix B) to concrete permission codes."""

    def prefixed(prefix: str) -> list[str]:
        return [c for c in all_codes if c == prefix or c.startswith(prefix + ".")]

    read_all = [f"{e}.read" for e in ENTITY_BASE_ACTIONS]
    bundle_status_all = [c for c in all_codes if c.startswith("bundle.status.")]

    return {
        "admin": list(all_codes),
        "pattern_maker": prefixed("piece") + ["style.read", "style.write", "folder.read", "search.read", "report.run"],
        "marker_maker": (
            prefixed("marker") + ["order.read", "bundle.write"] + bundle_status_all
            + ["piece.read", "folder.read", "search.read", "report.run", "job.submit", "job.read", "job.cancel"]
        ),
        "production_planner": (
            prefixed("order") + ["bundle.read"] + bundle_status_all
            + ["style.read", "folder.read", "search.read", "report.run", "job.read"]
        ),
        "viewer": read_all + ["search.read", "job.read"],
        "auditor": ["audit.read", "audit.export"] + read_all + ["job.read"],
        "contractor_qa": ["piece.status.approved", "marker.status.approved"] + read_all,
        "job_worker": ["job.worker"],
    }


REPORT_DEFINITIONS = [
    ("single_piece", "Single Piece Report", "piece", "Full detail report for a single piece."),
    ("all_piece", "All Piece Report", "piece", "Listing of all pieces (optionally filtered)."),
    ("piece_perimeter", "Piece Perimeter Report", "piece", "Piece perimeter/measurement report."),
    ("all_marker", "All Marker Report", "marker", "Listing of all markers (optionally filtered)."),
    ("all_layrule", "All Layrule Report", "marker", "Listing of all layrules associated with markers."),
    ("all_plot", "All Plot Report", "marker", "Listing of all plot jobs/files for markers."),
    ("all_cut", "All Cut Report", "marker", "Listing of all cut-data records for markers."),
    ("splice", "Splice Report", "marker", "Splice report for marker cutting."),
]


def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(
        sa.text(
            "INSERT INTO dmp.workflow_statuses "
            "(id, entity_type, code, label, sequence, is_initial, is_terminal) "
            "VALUES (:id, :entity_type, :code, :label, :sequence, :is_initial, :is_terminal)"
        ),
        [
            {
                "id": r[0], "entity_type": r[1], "code": r[2], "label": r[3],
                "sequence": r[4], "is_initial": r[5], "is_terminal": r[6],
            }
            for r in WORKFLOW_STATUSES
        ],
    )

    status_id_by_key = {(r[1], r[2]): r[0] for r in WORKFLOW_STATUSES}
    conn.execute(
        sa.text(
            "INSERT INTO dmp.workflow_transitions "
            "(entity_type, from_status_id, to_status_id, required_permission) "
            "VALUES (:entity_type, :from_status_id, :to_status_id, :required_permission)"
        ),
        [
            {
                "entity_type": entity_type,
                "from_status_id": status_id_by_key[(entity_type, from_code)],
                "to_status_id": status_id_by_key[(entity_type, to_code)],
                "required_permission": f"{entity_type}.status.{to_code}",
            }
            for entity_type, from_code, to_code in WORKFLOW_TRANSITIONS
        ],
    )

    permissions = _build_permissions()
    conn.execute(
        sa.text(
            "INSERT INTO dmp.permissions (id, code, resource, action, description) "
            "VALUES (:id, :code, :resource, :action, :description)"
        ),
        [{"id": p[0], "code": p[1], "resource": p[2], "action": p[3], "description": p[4]} for p in permissions],
    )

    conn.execute(
        sa.text("INSERT INTO dmp.roles (id, code, name, description) VALUES (:id, :code, :name, :description)"),
        [{"id": r[0], "code": r[1], "name": r[2], "description": r[3]} for r in ROLES],
    )

    all_codes = [p[1] for p in permissions]
    permission_id_by_code = {p[1]: p[0] for p in permissions}
    role_id_by_code = {r[1]: r[0] for r in ROLES}
    grants = _role_permission_codes(all_codes)

    role_permission_rows = []
    for role_code, perm_codes in grants.items():
        for perm_code in sorted(set(perm_codes)):
            role_permission_rows.append(
                {"role_id": role_id_by_code[role_code], "permission_id": permission_id_by_code[perm_code]}
            )
    conn.execute(
        sa.text("INSERT INTO dmp.role_permissions (role_id, permission_id) VALUES (:role_id, :permission_id)"),
        role_permission_rows,
    )

    conn.execute(
        sa.text(
            "INSERT INTO dmp.report_definitions (code, name, entity_type, description) "
            "VALUES (:code, :name, :entity_type, :description)"
        ),
        [{"code": c, "name": n, "entity_type": e, "description": d} for c, n, e, d in REPORT_DEFINITIONS],
    )

    conn.execute(
        sa.text(
            "INSERT INTO dmp.job_types (id, code, name, owning_app, default_timeout_seconds, description) "
            "VALUES (1, 'marker_nesting_solve', 'Marker Nesting Solve', 'marker-making', 2400, "
            "'Runs the existing nesting algorithm against marker layout + order quantity data; "
            "produces a production cut plan and a new marker set.')"
        )
    )


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM dmp.job_types"))
    conn.execute(sa.text("DELETE FROM dmp.report_definitions"))
    conn.execute(sa.text("DELETE FROM dmp.role_permissions"))
    conn.execute(sa.text("DELETE FROM dmp.roles"))
    conn.execute(sa.text("DELETE FROM dmp.permissions"))
    conn.execute(sa.text("DELETE FROM dmp.workflow_transitions"))
    conn.execute(sa.text("DELETE FROM dmp.workflow_statuses"))
