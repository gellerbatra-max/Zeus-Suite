"""marker_making_production_plan.md Sec 1.11 (file/data management): "Open by name" and "step to
the next Unmade/Made/any-status marker... alphanumerically." The platform already has both a
folder-scoped marker list (`GET /markers`) and a full-text/filtered search
(`POST /search`, Section 4.8's "Find" utility) -- neither was proxied here before this slice, so
the frontend had no way to open a marker except pasting its UUID.

`POST /markers/search` forwards to the platform's `POST /search` with `entity_types` hardcoded to
`["marker"]` (this service never lets the caller search other entity types through this route --
that's the Data Management app's job) and reshapes the response to a flat marker-only list.
`GET /markers/{marker_id}/siblings` is the "current storage area" for the Open Next/Previous
family: every marker in the same folder as the given one, sorted by `marker_code` -- the platform's
own `_search_marker` doesn't order results, so this endpoint fetches the folder's markers directly
and sorts them here, since that's where "alphanumerically" actually needs to be guaranteed. The
frontend walks this list client-side to find the next/previous entry (optionally filtered by
status for Next Unmade / Next Made) rather than this service exposing four near-identical stepping
endpoints.
"""

from fastapi import APIRouter, Depends

from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    MarkerSearchRequest,
    MarkerSearchResponse,
    MarkerSearchResult,
    MarkerSibling,
)

router = APIRouter(tags=["marker-picker"])


@router.post("/markers/search", response_model=MarkerSearchResponse)
def search_markers(body: MarkerSearchRequest, client: PlatformClient = Depends(get_platform_client)):
    payload = {
        "entity_types": ["marker"],
        "text": body.text,
        "filters": {"folder_id": body.folder_id, "workflow_status": body.workflow_status},
        "page": body.page,
        "page_size": body.page_size,
    }
    raw = client.post("/search", json=payload)
    rows = raw.get("results", {}).get("marker", [])
    total = raw.get("total_by_type", {}).get("marker", len(rows))
    return MarkerSearchResponse(
        results=[
            MarkerSearchResult(
                id=row["id"], code=row["code"], name=row["name"], folder_path=row["folder_path"],
                workflow_status=row["workflow_status"], updated_at=row["updated_at"],
            )
            for row in rows
        ],
        total=total,
    )


@router.get("/markers/{marker_id}/siblings", response_model=list[MarkerSibling])
def list_marker_siblings(marker_id: str, client: PlatformClient = Depends(get_platform_client)):
    marker = client.get(f"/markers/{marker_id}")
    raw = client.get("/markers", params={"folder_id": marker["folder_id"], "page_size": 200})
    items = sorted(raw["items"], key=lambda m: m["marker_code"])
    return [
        MarkerSibling(id=m["id"], marker_code=m["marker_code"], workflow_status=m["workflow_status"]["code"])
        for m in items
    ]
