"""Milestone 1 exit check: a fresh database stood up from migrations alone inserts one row per
table across a realistic dependency chain, exercising every foreign key -- including the two
FKs added after the fact (pieces.current_version_id, markers.order_id)."""

import uuid

from app.models import (
    AuditLog,
    Bundle,
    Folder,
    Job,
    JobEvent,
    JobType,
    Marker,
    MarkerPiece,
    MarkerVersion,
    Order,
    OrderLine,
    Organization,
    Permission,
    Piece,
    PieceVersion,
    Role,
    RolePermission,
    ServiceAccount,
    Style,
    StylePiece,
    User,
    UserRole,
    WorkflowStatus,
)


def _status_id(session, entity_type: str, code: str) -> int:
    return (
        session.query(WorkflowStatus)
        .filter_by(entity_type=entity_type, code=code)
        .one()
        .id
    )


def test_full_insert_chain(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]

    org = Organization(name="Acme Apparel", code=f"ACME-{unique}")
    session.add(org)
    session.flush()

    user = User(
        organization_id=org.id,
        sso_subject=f"sub-{unique}",
        username=f"jsmith-{unique}",
        email="jsmith@example.com",
        full_name="Jamie Smith",
    )
    session.add(user)
    session.flush()

    service_account = ServiceAccount(
        user_id=user.id,
        client_id=f"svc-{unique}",
        description="Nesting worker service account",
    )
    session.add(service_account)

    # Roles/permissions/role_permissions are seeded by migration 0002 -- just reference them.
    admin_role = session.query(Role).filter_by(code="admin").one()
    a_permission = session.query(Permission).first()
    role_permission = (
        session.query(RolePermission)
        .filter_by(role_id=admin_role.id, permission_id=a_permission.id)
        .one()
    )
    assert role_permission is not None

    folder = Folder(
        organization_id=org.id,
        parent_id=None,
        name=f"FW26-{unique}",
        path=f"/FW26-{unique}",
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(folder)
    session.flush()

    user_role = UserRole(
        user_id=user.id,
        role_id=admin_role.id,
        folder_id=None,
        granted_by=user.id,
    )
    session.add(user_role)

    piece = Piece(
        organization_id=org.id,
        folder_id=folder.id,
        piece_code=f"FRONT-PANEL-{unique}",
        piece_name="Front Panel",
        workflow_status_id=_status_id(session, "piece", "unmade"),
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(piece)
    session.flush()

    piece_version = PieceVersion(
        piece_id=piece.id,
        version_number=1,
        storage_container="dmp-pieces",
        storage_key=f"{org.id}/{piece.id}/1.pat",
        checksum_sha256="0" * 64,
        size_bytes=1024,
        created_by=user.id,
    )
    session.add(piece_version)
    session.flush()

    piece.current_version_id = piece_version.id  # exercises the deferred FK from Section 2.4.1
    session.flush()

    style = Style(
        organization_id=org.id,
        folder_id=folder.id,
        style_number=f"STY-{unique}",
        style_name="FW26 Jacket",
        workflow_status_id=_status_id(session, "style", "draft"),
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(style)
    session.flush()

    style_piece = StylePiece(
        style_id=style.id,
        piece_id=piece.id,
        added_by=user.id,
    )
    session.add(style_piece)

    order = Order(
        organization_id=org.id,
        folder_id=folder.id,
        order_number=f"ORD-{unique}",
        style_id=style.id,
        workflow_status_id=_status_id(session, "order", "open"),
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(order)
    session.flush()

    order_line = OrderLine(
        order_id=order.id,
        size_code="M",
        color="Navy",
        quantity=240,
    )
    session.add(order_line)

    marker = Marker(
        organization_id=org.id,
        folder_id=folder.id,
        marker_code=f"MRK-{unique}",
        marker_name="FW26 Jacket Marker",
        order_id=order.id,  # exercises the deferred FK from Section 2.7
        workflow_status_id=_status_id(session, "marker", "unmade"),
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(marker)
    session.flush()

    marker_version = MarkerVersion(
        marker_id=marker.id,
        version_number=1,
        storage_container="dmp-markers",
        storage_key=f"{org.id}/{marker.id}/1.native",
        checksum_sha256="1" * 64,
        size_bytes=2048,
        created_by=user.id,
    )
    session.add(marker_version)
    session.flush()

    marker.current_version_id = marker_version.id
    session.flush()

    marker_piece = MarkerPiece(
        marker_id=marker.id,
        piece_id=piece.id,
        piece_version_id=piece_version.id,
        size_code="M",
        quantity=60,
        placement_data={"x": 10, "y": 20, "rotation": 0},
    )
    session.add(marker_piece)

    bundle = Bundle(
        organization_id=org.id,
        order_id=order.id,
        marker_id=marker.id,
        piece_id=piece.id,
        bundle_code=f"BND-{unique}",
        qr_code=f"QR-{unique}",
        size_code="M",
        color="Navy",
        ply_range_start=1,
        ply_range_end=60,
        quantity=60,
        workflow_status_id=_status_id(session, "bundle", "pending"),
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(bundle)

    audit_entry = AuditLog(
        organization_id=org.id,
        user_id=user.id,
        action="piece.create",
        entity_type="piece",
        entity_id=piece.id,
        folder_id=folder.id,
        after_state={"piece_code": piece.piece_code},
        request_id=uuid.uuid4(),
        client_app="pattern-design",
        result="success",
    )
    session.add(audit_entry)

    job_type = session.query(JobType).filter_by(code="marker_nesting_solve").one()
    job = Job(
        organization_id=org.id,
        job_type_id=job_type.id,
        submitted_by=user.id,
        input_ref={"marker_id": str(marker.id), "order_id": str(order.id)},
    )
    session.add(job)
    session.flush()

    job_event = JobEvent(job_id=job.id, event_type="queued", detail={})
    session.add(job_event)

    session.commit()

    # Sanity: everything is actually reachable back out through the ORM.
    reloaded_piece = session.get(Piece, piece.id)
    assert reloaded_piece.current_version_id == piece_version.id
    reloaded_marker = session.get(Marker, marker.id)
    assert reloaded_marker.order_id == order.id
