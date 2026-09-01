"""Section 4.8: search / cross-reference ("Find" utility equivalent)."""

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.deps import (
    Actor,
    get_current_actor,
    get_db,
    get_request_id,
    require_permission,
)
from app.errors import not_found
from app.models import Bundle, Marker, Order, Piece, Style
from app.schemas import (
    CrossReferenceOut,
    SearchRequest,
    SearchResponse,
    SuggestResultRow,
)
from app.search_service import cross_reference_graph, run_search, run_suggest

router = APIRouter(tags=["search"])

_ANCHOR_MODELS = {"piece": Piece, "style": Style, "marker": Marker, "order": Order, "bundle": Bundle}


@router.post("/search", response_model=SearchResponse)
def search(
    body: SearchRequest,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "search.read", request_id=request_id, entity_type="search", action="search.query")
    results, total_by_type = run_search(
        db,
        actor.user_id,
        actor.organization_id,
        entity_types=body.entity_types,
        text=body.text,
        filters=body.filters,
        cross_reference=body.cross_reference,
        page=body.page,
        page_size=body.page_size,
    )
    return SearchResponse(results=results, total_by_type=total_by_type)


@router.get("/search/suggest", response_model=list[SuggestResultRow])
def suggest(
    q: str = Query(..., min_length=1),
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    require_permission(db, actor, "search.read", request_id=request_id, entity_type="search", action="search.suggest")
    return run_suggest(db, actor.user_id, actor.organization_id, q)


@router.get("/cross-reference/{entity_type}/{entity_id}", response_model=CrossReferenceOut)
def cross_reference(
    entity_type: str,
    entity_id: uuid.UUID,
    actor: Actor = Depends(get_current_actor),
    db: Session = Depends(get_db),
    request_id: uuid.UUID = Depends(get_request_id),
):
    model = _ANCHOR_MODELS.get(entity_type)
    if model is None:
        raise not_found("Entity type")

    entity = db.get(model, entity_id)
    if entity is None or entity.organization_id != actor.organization_id:
        raise not_found(entity_type.capitalize())

    # Bundles have no folder_id of their own (Section 2.8) -- scope through the owning order.
    folder_id = entity.folder_id if hasattr(entity, "folder_id") else db.get(Order, entity.order_id).folder_id
    require_permission(
        db, actor, f"{entity_type}.read", request_id=request_id, entity_type=entity_type,
        action="cross_reference.read", folder_id=folder_id, entity_id=entity_id,
    )

    related = cross_reference_graph(db, actor.organization_id, entity_type, entity_id)
    return CrossReferenceOut(entity_type=entity_type, id=entity_id, related=related)
