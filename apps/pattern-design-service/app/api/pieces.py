"""The pattern-design canvas's piece lifecycle surface: create/open pieces (proxied straight to
data-platform-api, no new platform schema needed -- pieces/folders/versions/workflow already
exist there, see pattern_design_plan.md Sec 3.1) and, the part that's actually new, a piece's
*geometry* -- save/load the structured JSON document (Sec 3.3) as a Blob Storage-backed piece
version.

Phase 2.1 exit criteria (pattern_design_plan.md Sec 7): a piece with just a drawn perimeter
round-trips through Blob Storage and Postgres correctly, including workflow status. Seams, darts,
notches, and grain line are carried in the geometry schema already (app/schemas.py) so later
phases don't need a schema_version bump to add them, but no tool in this slice writes them --
that's Phase 2.3.
"""

import hashlib

from fastapi import APIRouter, Depends, Query

from app.blob_io import download_blob, upload_blob
from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import (
    PieceCreateRequest,
    PieceGeometryDocument,
    PieceOut,
    StatusTransitionRequest,
    empty_geometry_document,
)

router = APIRouter(prefix="/pieces", tags=["pieces"])


@router.get("", response_model=list[PieceOut])
def list_pieces(folder_id: str | None = Query(None), client: PlatformClient = Depends(get_platform_client)):
    params = {"folder_id": folder_id} if folder_id else {}
    return client.get("/pieces", params=params)["items"]


@router.post("", response_model=PieceOut, status_code=201)
def create_piece(body: PieceCreateRequest, client: PlatformClient = Depends(get_platform_client)):
    return client.post("/pieces", json=body.model_dump())


@router.get("/{piece_id}", response_model=PieceOut)
def get_piece(piece_id: str, client: PlatformClient = Depends(get_platform_client)):
    return client.get(f"/pieces/{piece_id}")


@router.get("/{piece_id}/geometry", response_model=PieceGeometryDocument)
def get_geometry(piece_id: str, client: PlatformClient = Depends(get_platform_client)):
    """A freshly created piece has no committed version yet -- returns an empty document (an
    empty perimeter to draw into) rather than 404, since "open a new piece" and "open an
    existing-but-still-blank piece" are the same operation from the canvas's point of view."""
    piece = client.get(f"/pieces/{piece_id}")
    version_id = piece.get("current_version_id")
    if version_id is None:
        return empty_geometry_document()

    download = client.get(f"/pieces/{piece_id}/versions/{version_id}/download-url")
    payload = download_blob(download["download_url"])
    return PieceGeometryDocument.model_validate_json(payload)


@router.put("/{piece_id}/geometry", response_model=PieceOut)
def save_geometry(piece_id: str, body: PieceGeometryDocument, client: PlatformClient = Depends(get_platform_client)):
    """Every save is a brand-new immutable piece version (Blob Storage versioning, never an
    in-place overwrite -- pattern_design_plan.md Sec 3.1), the same begin/upload/complete
    3-step protocol data-platform-api's SAS-URL upload flow requires of any client."""
    payload = body.model_dump_json().encode("utf-8")
    begin = client.post(
        f"/pieces/{piece_id}/versions",
        json={"file_format": "native", "size_bytes": len(payload), "comment": "geometry save"},
    )
    upload_blob(begin["upload_url"], payload)
    checksum = hashlib.sha256(payload).hexdigest()
    return client.post(
        f"/pieces/{piece_id}/versions/{begin['version_id']}/complete",
        json={"checksum_sha256": checksum},
    )


@router.post("/{piece_id}/status", response_model=PieceOut)
def transition_status(
    piece_id: str, body: StatusTransitionRequest, client: PlatformClient = Depends(get_platform_client)
):
    return client.post(f"/pieces/{piece_id}/status", json=body.model_dump())
