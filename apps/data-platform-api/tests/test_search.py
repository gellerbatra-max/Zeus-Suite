"""Milestone 5 exit check: a seeded dataset of ~500 interlinked pieces/styles/markers/orders
returns correct, permission-scoped, sub-200ms results for both free-text and
cross-reference-anchored queries."""

import time
import uuid

from fastapi.testclient import TestClient

from app.auth import dev_login
from app.main import app
from app.models import (
    Folder,
    Marker,
    Order,
    Organization,
    Piece,
    Role,
    Style,
    StylePiece,
    User,
    UserRole,
    WorkflowStatus,
)
from app.schemas import SearchFilters
from app.search_service import resolve_read_scope, run_search

client = TestClient(app)


def _status_id(session, entity_type: str, code: str) -> int:
    return session.query(WorkflowStatus).filter_by(entity_type=entity_type, code=code).one().id


def _seed_dataset(session, org, folder, user, n_styles=60, pieces_per_style=3, orders_per_style=2):
    """~60 styles x (1 + 3 pieces + 2 orders + 2 markers) = ~480 interlinked rows, in the
    ballpark of the exit check's "~500" scale."""
    piece_status = _status_id(session, "piece", "unmade")
    style_status = _status_id(session, "style", "draft")
    order_status = _status_id(session, "order", "open")
    marker_status = _status_id(session, "marker", "unmade")

    seeded = {"styles": [], "pieces": [], "orders": [], "markers": []}

    for s in range(n_styles):
        style = Style(
            organization_id=org.id, folder_id=folder.id, style_number=f"STY-{s:04d}",
            style_name=f"Style {s}", customer="Acme" if s % 2 == 0 else "Globex",
            workflow_status_id=style_status, created_by=user.id, updated_by=user.id,
        )
        session.add(style)
        session.flush()
        seeded["styles"].append(style)

        for p in range(pieces_per_style):
            piece = Piece(
                organization_id=org.id, folder_id=folder.id, piece_code=f"PANEL-{s:04d}-{p}",
                piece_name=f"Panel {s}-{p}", workflow_status_id=piece_status,
                created_by=user.id, updated_by=user.id,
            )
            session.add(piece)
            session.flush()
            seeded["pieces"].append(piece)
            session.add(StylePiece(style_id=style.id, piece_id=piece.id, added_by=user.id))

        for o in range(orders_per_style):
            order = Order(
                organization_id=org.id, folder_id=folder.id, order_number=f"ORD-{s:04d}-{o}",
                style_id=style.id, customer=style.customer, workflow_status_id=order_status,
                created_by=user.id, updated_by=user.id,
            )
            session.add(order)
            session.flush()
            seeded["orders"].append(order)

            marker = Marker(
                organization_id=org.id, folder_id=folder.id, marker_code=f"MRK-{s:04d}-{o}",
                marker_name=f"Marker {s}-{o}", order_id=order.id,
                workflow_status_id=marker_status, created_by=user.id, updated_by=user.id,
            )
            session.add(marker)
            session.flush()
            seeded["markers"].append(marker)

    session.commit()
    total = sum(len(v) for v in seeded.values())
    assert total > 400  # in the "~500" ballpark the exit check names
    return seeded


def test_search_correctness_and_performance(db_session):
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = Organization(name="Search Test Org", code=f"SEARCH-{unique}")
    session.add(org)
    session.flush()

    seed_user = dev_login(session, org.id, username=f"seed-{unique}", email="seed@example.com", full_name="Seed")
    session.flush()

    folder = Folder(
        organization_id=org.id, name=f"Root-{unique}", path=f"/Root-{unique}",
        created_by=seed_user.id, updated_by=seed_user.id,
    )
    session.add(folder)
    session.flush()

    dataset = _seed_dataset(session, org, folder, seed_user)

    headers = {"X-Dev-User": f"searcher-{unique}", "X-Dev-Org": f"SEARCH-{unique}"}
    client.get("/me", headers=headers)  # JIT-provision with default 'viewer' (org-wide *.read)

    # -- Free-text search: substring match against a piece code, per Section 4.8's own example
    # ("PANEL" matches FRONT-PANEL-01") -- here "PANEL-0005" should match exactly the 3 pieces
    # belonging to style 5, and nothing else.
    start = time.monotonic()
    resp = client.post(
        "/search",
        json={"entity_types": ["piece"], "text": "PANEL-0005", "page": 1, "page_size": 50},
        headers=headers,
    )
    elapsed_ms = (time.monotonic() - start) * 1000
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["total_by_type"]["piece"] == 3
    assert {row["code"] for row in body["results"]["piece"]} == {
        "PANEL-0005-0", "PANEL-0005-1", "PANEL-0005-2",
    }
    assert elapsed_ms < 200, f"free-text search took {elapsed_ms:.1f}ms"

    # -- Cross-reference-anchored search: every piece connected to style 10, and nothing else.
    target_style = dataset["styles"][10]
    start = time.monotonic()
    resp = client.post(
        "/search",
        json={
            "entity_types": ["piece", "order"],
            "cross_reference": {"style_id": str(target_style.id)},
            "page": 1,
            "page_size": 50,
        },
        headers=headers,
    )
    elapsed_ms = (time.monotonic() - start) * 1000
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["total_by_type"]["piece"] == 3
    assert body["total_by_type"]["order"] == 2
    assert all(row["code"].startswith("PANEL-0010") for row in body["results"]["piece"])
    assert all(row["code"].startswith("ORD-0010") for row in body["results"]["order"])
    assert elapsed_ms < 200, f"cross-reference search took {elapsed_ms:.1f}ms"

    # -- /search/suggest typeahead.
    resp = client.get("/search/suggest", params={"q": "STY-0001"}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert any(row["code"] == "STY-0001" for row in resp.json())

    # -- /cross-reference/{type}/{id}: the one-hop graph for a specific order.
    anchor_order = dataset["orders"][20]
    resp = client.get(f"/cross-reference/order/{anchor_order.id}", headers=headers)
    assert resp.status_code == 200, resp.text
    related = resp.json()["related"]
    assert len(related["marker"]) == 1
    assert related["marker"][0]["code"] == f"MRK-{20 // 2:04d}-{20 % 2}"


def test_search_is_scoped_to_the_callers_organization(db_session):
    """Two orgs seed a piece with the same code -- a searcher in org A must never see org B's row."""
    session = db_session
    unique = uuid.uuid4().hex[:8]

    def _seed_org_with_piece(code_suffix: str):
        org = Organization(name="Org", code=f"TENANT-{code_suffix}-{unique}")
        session.add(org)
        session.flush()
        user = dev_login(session, org.id, username=f"u-{code_suffix}-{unique}", email="u@example.com", full_name="U")
        session.flush()
        folder = Folder(
            organization_id=org.id, name=f"F-{code_suffix}", path=f"/F-{code_suffix}-{unique}",
            created_by=user.id, updated_by=user.id,
        )
        session.add(folder)
        session.flush()
        piece = Piece(
            organization_id=org.id, folder_id=folder.id, piece_code=f"SHARED-CODE-{unique}",
            piece_name=f"Piece in {code_suffix}",
            workflow_status_id=_status_id(session, "piece", "unmade"),
            created_by=user.id, updated_by=user.id,
        )
        session.add(piece)
        session.commit()
        return org

    org_a = _seed_org_with_piece("A")
    _seed_org_with_piece("B")

    headers = {"X-Dev-User": f"searcher-a-{unique}", "X-Dev-Org": org_a.code}
    client.get("/me", headers=headers)

    resp = client.post(
        "/search",
        json={"entity_types": ["piece"], "text": f"SHARED-CODE-{unique}"},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    results = resp.json()["results"]["piece"]
    assert len(results) == 1
    assert results[0]["name"] == "Piece in A"


def test_search_respects_folder_scoped_permissions(db_session):
    """A user granted read only on a folder subtree must not see entities outside it, even
    though the search spans the whole search space before permission filtering."""
    session = db_session
    unique = uuid.uuid4().hex[:8]
    org = Organization(name="Scope Test Org", code=f"SCOPE-{unique}")
    session.add(org)
    session.flush()

    admin_user = dev_login(session, org.id, username=f"admin-{unique}", email="a@example.com", full_name="Admin")
    session.flush()

    visible_folder = Folder(
        organization_id=org.id, name=f"Visible-{unique}", path=f"/Visible-{unique}",
        created_by=admin_user.id, updated_by=admin_user.id,
    )
    hidden_folder = Folder(
        organization_id=org.id, name=f"Hidden-{unique}", path=f"/Hidden-{unique}",
        created_by=admin_user.id, updated_by=admin_user.id,
    )
    session.add_all([visible_folder, hidden_folder])
    session.flush()

    piece_status = _status_id(session, "piece", "unmade")
    visible_piece = Piece(
        organization_id=org.id, folder_id=visible_folder.id, piece_code=f"VIS-{unique}",
        piece_name="Visible Piece", workflow_status_id=piece_status,
        created_by=admin_user.id, updated_by=admin_user.id,
    )
    hidden_piece = Piece(
        organization_id=org.id, folder_id=hidden_folder.id, piece_code=f"HID-{unique}",
        piece_name="Hidden Piece", workflow_status_id=piece_status,
        created_by=admin_user.id, updated_by=admin_user.id,
    )
    session.add_all([visible_piece, hidden_piece])
    session.flush()

    # A fresh user with NO default role at all (bypassing JIT's usual org-wide 'viewer' grant),
    # holding only a folder-scoped 'contractor_qa' grant (which carries '*.read') on visible_folder.
    scoped_user = User(
        organization_id=org.id, sso_subject=f"scoped-{unique}", username=f"scoped-{unique}",
        email="scoped@example.com", full_name="Scoped User",
    )
    session.add(scoped_user)
    session.flush()
    contractor_role = session.query(Role).filter_by(code="contractor_qa").one()
    session.add(
        UserRole(
            user_id=scoped_user.id, role_id=contractor_role.id, folder_id=visible_folder.id,
            granted_by=admin_user.id,
        )
    )
    session.commit()

    scope = resolve_read_scope(session, scoped_user.id, "piece")
    assert scope.org_wide is False
    assert scope.allows(visible_folder.path) is True
    assert scope.allows(hidden_folder.path) is False

    results, totals = run_search(
        session, scoped_user.id, org.id, entity_types=["piece"], text=None,
        filters=SearchFilters(), cross_reference=None, page=1, page_size=50,
    )
    codes = {row.code for row in results["piece"]}
    assert f"VIS-{unique}" in codes
    assert f"HID-{unique}" not in codes
    assert totals["piece"] == 1
