"""Section 4.8: structured cross-reference search, typeahead suggest, and the one-hop
cross-reference graph. Built on the Postgres FTS (`search_vector`) + pg_trgm indexes from
Section 2 and migration 0004 -- no separate search engine, per Section 1's explicit choice to
defer that until Postgres FTS proves insufficient at scale.
"""

import uuid
from dataclasses import dataclass

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models import (
    Bundle,
    Folder,
    Marker,
    MarkerPiece,
    Order,
    Permission,
    Piece,
    RolePermission,
    Style,
    StylePiece,
    UserRole,
    WorkflowStatus,
)
from app.schemas import CrossReferenceAnchor, SearchFilters, SearchResultRow

ENTITY_TYPES = ["piece", "style", "marker", "order", "bundle"]


# -- Permission-scoped visibility ------------------------------------------------------------


@dataclass
class ReadScope:
    org_wide: bool
    granted_folder_paths: list[str]

    def allows(self, folder_path: str | None) -> bool:
        if self.org_wide:
            return True
        if folder_path is None:
            return False
        return any(
            folder_path == p or folder_path.startswith(p.rstrip("/") + "/") for p in self.granted_folder_paths
        )


def resolve_read_scope(session: Session, user_id: uuid.UUID, entity_type: str) -> ReadScope:
    """Section 5.2's per-request permission resolution, specialized for search: rather than
    resolving one folder at a time (as app.auth.resolve_permissions does for a single resource),
    this resolves *every* folder the caller can read `entity_type` in, once, so a page of search
    results can be filtered in memory instead of re-querying RBAC per row."""
    code = f"{entity_type}.read"
    org_wide = (
        session.query(Permission.id)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .filter(UserRole.user_id == user_id, UserRole.folder_id.is_(None), Permission.code == code)
        .first()
        is not None
    )
    if org_wide:
        return ReadScope(org_wide=True, granted_folder_paths=[])

    paths = (
        session.query(Folder.path)
        .join(UserRole, UserRole.folder_id == Folder.id)
        .join(RolePermission, RolePermission.role_id == UserRole.role_id)
        .join(Permission, Permission.id == RolePermission.permission_id)
        .filter(UserRole.user_id == user_id, Permission.code == code)
        .all()
    )
    return ReadScope(org_wide=False, granted_folder_paths=[p for (p,) in paths])


# -- Cross-reference resolution ----------------------------------------------------------------


def _cross_reference_ids(session: Session, entity_type: str, anchor: CrossReferenceAnchor) -> set[uuid.UUID] | None:
    """Resolves the anchor in `anchor` to the set of `entity_type` ids connected to it. Returns
    None if no anchor field is set (meaning "no cross-reference constraint")."""
    if anchor.piece_id is not None:
        if entity_type == "style":
            return {r for (r,) in session.query(StylePiece.style_id).filter_by(piece_id=anchor.piece_id).all()}
        if entity_type == "marker":
            return {r for (r,) in session.query(MarkerPiece.marker_id).filter_by(piece_id=anchor.piece_id).all()}
        return None

    if anchor.style_id is not None:
        if entity_type == "piece":
            return {r for (r,) in session.query(StylePiece.piece_id).filter_by(style_id=anchor.style_id).all()}
        if entity_type == "order":
            return {r for (r,) in session.query(Order.id).filter_by(style_id=anchor.style_id).all()}
        return None

    if anchor.marker_id is not None:
        if entity_type == "piece":
            return {r for (r,) in session.query(MarkerPiece.piece_id).filter_by(marker_id=anchor.marker_id).all()}
        if entity_type == "bundle":
            return {r for (r,) in session.query(Bundle.id).filter_by(marker_id=anchor.marker_id).all()}
        if entity_type == "order":
            marker = session.get(Marker, anchor.marker_id)
            return {marker.order_id} if marker and marker.order_id else set()
        return None

    if anchor.order_id is not None:
        if entity_type == "marker":
            return {r for (r,) in session.query(Marker.id).filter_by(order_id=anchor.order_id).all()}
        if entity_type == "bundle":
            return {r for (r,) in session.query(Bundle.id).filter_by(order_id=anchor.order_id).all()}
        if entity_type == "style":
            order = session.get(Order, anchor.order_id)
            return {order.style_id} if order else set()
        return None

    return None


# -- Per-entity-type search --------------------------------------------------------------------


def _search_piece(
    session: Session, org_id: uuid.UUID, text: str | None, filters: SearchFilters, ids: set[uuid.UUID] | None
):
    query = session.query(Piece, Folder.path).join(Folder, Folder.id == Piece.folder_id).filter(
        Piece.organization_id == org_id, Piece.deleted_at.is_(None)
    )
    if text:
        query = query.filter(
            or_(
                Piece.search_vector.op("@@")(func.plainto_tsquery("english", text)),
                Piece.piece_code.ilike(f"%{text}%"),
                Piece.piece_name.ilike(f"%{text}%"),
            )
        )
    if filters.folder_id:
        query = query.filter(Piece.folder_id == filters.folder_id)
    if filters.workflow_status:
        status_ids = session.query(WorkflowStatus.id).filter(
            WorkflowStatus.entity_type == "piece", WorkflowStatus.code.in_(filters.workflow_status)
        )
        query = query.filter(Piece.workflow_status_id.in_(status_ids))
    if filters.updated_after:
        query = query.filter(Piece.updated_at >= filters.updated_after)
    if filters.updated_before:
        query = query.filter(Piece.updated_at <= filters.updated_before)
    if ids is not None:
        query = query.filter(Piece.id.in_(ids))
    return query


def _search_style(
    session: Session, org_id: uuid.UUID, text: str | None, filters: SearchFilters, ids: set[uuid.UUID] | None
):
    query = session.query(Style, Folder.path).join(Folder, Folder.id == Style.folder_id).filter(
        Style.organization_id == org_id, Style.deleted_at.is_(None)
    )
    if text:
        query = query.filter(
            or_(
                Style.search_vector.op("@@")(func.plainto_tsquery("english", text)),
                Style.style_number.ilike(f"%{text}%"),
                Style.style_name.ilike(f"%{text}%"),
            )
        )
    if filters.folder_id:
        query = query.filter(Style.folder_id == filters.folder_id)
    if filters.workflow_status:
        status_ids = session.query(WorkflowStatus.id).filter(
            WorkflowStatus.entity_type == "style", WorkflowStatus.code.in_(filters.workflow_status)
        )
        query = query.filter(Style.workflow_status_id.in_(status_ids))
    if filters.customer:
        query = query.filter(Style.customer.ilike(f"%{filters.customer}%"))
    if filters.updated_after:
        query = query.filter(Style.updated_at >= filters.updated_after)
    if filters.updated_before:
        query = query.filter(Style.updated_at <= filters.updated_before)
    if ids is not None:
        query = query.filter(Style.id.in_(ids))
    return query


def _search_marker(
    session: Session, org_id: uuid.UUID, text: str | None, filters: SearchFilters, ids: set[uuid.UUID] | None
):
    query = session.query(Marker, Folder.path).join(Folder, Folder.id == Marker.folder_id).filter(
        Marker.organization_id == org_id, Marker.deleted_at.is_(None)
    )
    if text:
        query = query.filter(
            or_(
                Marker.search_vector.op("@@")(func.plainto_tsquery("english", text)),
                Marker.marker_code.ilike(f"%{text}%"),
                Marker.marker_name.ilike(f"%{text}%"),
            )
        )
    if filters.folder_id:
        query = query.filter(Marker.folder_id == filters.folder_id)
    if filters.workflow_status:
        status_ids = session.query(WorkflowStatus.id).filter(
            WorkflowStatus.entity_type == "marker", WorkflowStatus.code.in_(filters.workflow_status)
        )
        query = query.filter(Marker.workflow_status_id.in_(status_ids))
    if filters.updated_after:
        query = query.filter(Marker.updated_at >= filters.updated_after)
    if filters.updated_before:
        query = query.filter(Marker.updated_at <= filters.updated_before)
    if ids is not None:
        query = query.filter(Marker.id.in_(ids))
    return query


def _search_order(
    session: Session, org_id: uuid.UUID, text: str | None, filters: SearchFilters, ids: set[uuid.UUID] | None
):
    query = session.query(Order, Folder.path).join(Folder, Folder.id == Order.folder_id).filter(
        Order.organization_id == org_id, Order.deleted_at.is_(None)
    )
    if text:
        query = query.filter(
            or_(
                Order.search_vector.op("@@")(func.plainto_tsquery("english", text)),
                Order.order_number.ilike(f"%{text}%"),
            )
        )
    if filters.folder_id:
        query = query.filter(Order.folder_id == filters.folder_id)
    if filters.workflow_status:
        status_ids = session.query(WorkflowStatus.id).filter(
            WorkflowStatus.entity_type == "order", WorkflowStatus.code.in_(filters.workflow_status)
        )
        query = query.filter(Order.workflow_status_id.in_(status_ids))
    if filters.customer:
        query = query.filter(Order.customer.ilike(f"%{filters.customer}%"))
    if filters.updated_after:
        query = query.filter(Order.updated_at >= filters.updated_after)
    if filters.updated_before:
        query = query.filter(Order.updated_at <= filters.updated_before)
    if ids is not None:
        query = query.filter(Order.id.in_(ids))
    return query


def _search_bundle(
    session: Session, org_id: uuid.UUID, text: str | None, filters: SearchFilters, ids: set[uuid.UUID] | None
):
    # Bundles have no folder_id or search_vector of their own (Section 2.8) -- folder scoping and
    # filtering go through the owning order.
    query = (
        session.query(Bundle, Folder.path)
        .join(Order, Order.id == Bundle.order_id)
        .join(Folder, Folder.id == Order.folder_id)
        .filter(Bundle.organization_id == org_id)
    )
    if text:
        query = query.filter(
            or_(
                Bundle.bundle_code.ilike(f"%{text}%"),
                Bundle.rfid_tag.ilike(f"%{text}%"),
                Bundle.qr_code.ilike(f"%{text}%"),
            )
        )
    if filters.folder_id:
        query = query.filter(Order.folder_id == filters.folder_id)
    if filters.workflow_status:
        status_ids = session.query(WorkflowStatus.id).filter(
            WorkflowStatus.entity_type == "bundle", WorkflowStatus.code.in_(filters.workflow_status)
        )
        query = query.filter(Bundle.workflow_status_id.in_(status_ids))
    if filters.updated_after:
        query = query.filter(Bundle.updated_at >= filters.updated_after)
    if filters.updated_before:
        query = query.filter(Bundle.updated_at <= filters.updated_before)
    if ids is not None:
        query = query.filter(Bundle.id.in_(ids))
    return query


_SEARCHERS = {
    "piece": (_search_piece, "piece_code", "piece_name"),
    "style": (_search_style, "style_number", "style_name"),
    "marker": (_search_marker, "marker_code", "marker_name"),
    "order": (_search_order, "order_number", "order_number"),
    "bundle": (_search_bundle, "bundle_code", "bundle_code"),
}


def _row_to_result(session: Session, entity_type: str, entity, folder_path: str | None) -> SearchResultRow:
    code_field, name_field = _SEARCHERS[entity_type][1], _SEARCHERS[entity_type][2]
    status = session.get(WorkflowStatus, entity.workflow_status_id)
    return SearchResultRow(
        id=entity.id,
        code=getattr(entity, code_field),
        name=getattr(entity, name_field),
        folder_path=folder_path,
        workflow_status=status.code,
        updated_at=entity.updated_at,
    )


def run_search(
    session: Session,
    user_id: uuid.UUID,
    org_id: uuid.UUID,
    entity_types: list[str],
    text: str | None,
    filters: SearchFilters,
    cross_reference: CrossReferenceAnchor | None,
    page: int,
    page_size: int,
) -> tuple[dict[str, list[SearchResultRow]], dict[str, int]]:
    results: dict[str, list[SearchResultRow]] = {}
    total_by_type: dict[str, int] = {}

    for entity_type in entity_types:
        if entity_type not in _SEARCHERS:
            continue
        scope = resolve_read_scope(session, user_id, entity_type)
        ids = _cross_reference_ids(session, entity_type, cross_reference) if cross_reference else None
        if cross_reference is not None and ids is not None and len(ids) == 0:
            results[entity_type] = []
            total_by_type[entity_type] = 0
            continue

        searcher = _SEARCHERS[entity_type][0]
        query = searcher(session, org_id, text, filters, ids)
        rows = query.all()

        visible = [row for row in rows if scope.allows(row[1])]
        total_by_type[entity_type] = len(visible)
        page_rows = visible[(page - 1) * page_size : (page - 1) * page_size + page_size]
        results[entity_type] = [_row_to_result(session, entity_type, entity, path) for entity, path in page_rows]

    return results, total_by_type


def run_suggest(session: Session, user_id: uuid.UUID, org_id: uuid.UUID, q: str, limit: int = 10) -> list[dict]:
    suggestions = []
    for entity_type in ENTITY_TYPES:
        scope = resolve_read_scope(session, user_id, entity_type)
        searcher = _SEARCHERS[entity_type][0]
        query = searcher(session, org_id, q, SearchFilters(), None)
        rows = query.all()
        visible = [row for row in rows if scope.allows(row[1])][:limit]
        for entity, _path in visible:
            code_field, name_field = _SEARCHERS[entity_type][1], _SEARCHERS[entity_type][2]
            suggestions.append(
                {
                    "entity_type": entity_type,
                    "id": entity.id,
                    "code": getattr(entity, code_field),
                    "name": getattr(entity, name_field),
                }
            )
    return suggestions


# -- One-hop cross-reference graph ---------------------------------------------------------------


def cross_reference_graph(
    session: Session, org_id: uuid.UUID, entity_type: str, entity_id: uuid.UUID
) -> dict[str, list[SearchResultRow]]:
    """Section 4.8's `/cross-reference/{entity_type}/{id}`: the full one-hop reference graph for
    one entity. Does not itself permission-filter the related rows -- the caller already checked
    `<entity_type>.read` on the anchor entity; the related entities returned are the direct,
    documented relationships of that one entity, not a second independent search."""
    related: dict[str, list[SearchResultRow]] = {}

    if entity_type == "piece":
        style_ids = {r for (r,) in session.query(StylePiece.style_id).filter_by(piece_id=entity_id).all()}
        marker_ids = {r for (r,) in session.query(MarkerPiece.marker_id).filter_by(piece_id=entity_id).all()}
        related["style"] = _rows_for_ids(session, org_id, "style", style_ids)
        related["marker"] = _rows_for_ids(session, org_id, "marker", marker_ids)

    elif entity_type == "style":
        piece_ids = {r for (r,) in session.query(StylePiece.piece_id).filter_by(style_id=entity_id).all()}
        order_ids = {r for (r,) in session.query(Order.id).filter_by(style_id=entity_id).all()}
        related["piece"] = _rows_for_ids(session, org_id, "piece", piece_ids)
        related["order"] = _rows_for_ids(session, org_id, "order", order_ids)

    elif entity_type == "marker":
        piece_ids = {r for (r,) in session.query(MarkerPiece.piece_id).filter_by(marker_id=entity_id).all()}
        marker = session.get(Marker, entity_id)
        order_ids = {marker.order_id} if marker and marker.order_id else set()
        bundle_ids = {r for (r,) in session.query(Bundle.id).filter_by(marker_id=entity_id).all()}
        related["piece"] = _rows_for_ids(session, org_id, "piece", piece_ids)
        related["order"] = _rows_for_ids(session, org_id, "order", order_ids)
        related["bundle"] = _rows_for_ids(session, org_id, "bundle", bundle_ids)

    elif entity_type == "order":
        marker_ids = {r for (r,) in session.query(Marker.id).filter_by(order_id=entity_id).all()}
        bundle_ids = {r for (r,) in session.query(Bundle.id).filter_by(order_id=entity_id).all()}
        related["marker"] = _rows_for_ids(session, org_id, "marker", marker_ids)
        related["bundle"] = _rows_for_ids(session, org_id, "bundle", bundle_ids)

    return related


def _rows_for_ids(session: Session, org_id: uuid.UUID, entity_type: str, ids: set[uuid.UUID]) -> list[SearchResultRow]:
    if not ids:
        return []
    searcher = _SEARCHERS[entity_type][0]
    query = searcher(session, org_id, None, SearchFilters(), ids)
    return [_row_to_result(session, entity_type, entity, path) for entity, path in query.all()]
