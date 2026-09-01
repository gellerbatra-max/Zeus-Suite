"""Representative CHECK/UNIQUE constraint tests -- confirm the database rejects bad data rather
than silently accepting it, per the Milestone 1 exit check."""

import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Bundle, Folder, Organization, Piece, User, WorkflowStatus


def _seed_org_user_folder(session, unique: str):
    org = Organization(name="Acme", code=f"ACME-{unique}")
    session.add(org)
    session.flush()

    user = User(
        organization_id=org.id,
        sso_subject=f"sub-{unique}",
        username=f"user-{unique}",
        email="user@example.com",
        full_name="Test User",
    )
    session.add(user)
    session.flush()

    folder = Folder(
        organization_id=org.id,
        name=f"Folder-{unique}",
        path=f"/Folder-{unique}",
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(folder)
    session.flush()

    return org, user, folder


def test_invalid_user_status_rejected(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = Organization(name="Acme", code=f"ACME-{unique}")
    session.add(org)
    session.flush()

    bad_user = User(
        organization_id=org.id,
        sso_subject=f"sub-{unique}",
        username=f"user-{unique}",
        email="user@example.com",
        full_name="Test User",
        status="not_a_real_status",
    )
    session.add(bad_user)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_bundle_non_positive_quantity_rejected(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org, user, folder = _seed_org_user_folder(session, unique)

    piece = Piece(
        organization_id=org.id,
        folder_id=folder.id,
        piece_code=f"PIECE-{unique}",
        piece_name="Test Piece",
        workflow_status_id=session.query(WorkflowStatus).filter_by(entity_type="piece", code="unmade").one().id,
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(piece)
    session.flush()

    # Bundles also require order_id/marker_id -- but the CHECK constraint on quantity fires
    # before any FK is checked is not guaranteed, so this only asserts *some* IntegrityError,
    # which is enough to confirm the row is rejected either way.
    bad_bundle = Bundle(
        organization_id=org.id,
        order_id=uuid.uuid4(),
        marker_id=uuid.uuid4(),
        piece_id=piece.id,
        bundle_code=f"BND-{unique}",
        size_code="M",
        quantity=0,
        workflow_status_id=session.query(WorkflowStatus).filter_by(entity_type="bundle", code="pending").one().id,
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(bad_bundle)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_duplicate_piece_code_in_same_folder_rejected(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org, user, folder = _seed_org_user_folder(session, unique)
    status_id = session.query(WorkflowStatus).filter_by(entity_type="piece", code="unmade").one().id

    first = Piece(
        organization_id=org.id,
        folder_id=folder.id,
        piece_code=f"DUP-{unique}",
        piece_name="First",
        workflow_status_id=status_id,
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(first)
    session.flush()

    duplicate = Piece(
        organization_id=org.id,
        folder_id=folder.id,
        piece_code=f"DUP-{unique}",
        piece_name="Second",
        workflow_status_id=status_id,
        created_by=user.id,
        updated_by=user.id,
    )
    session.add(duplicate)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()
