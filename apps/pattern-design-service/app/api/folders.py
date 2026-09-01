"""Thin passthrough to data-platform-api's real folder browser -- a piece can't be created
without a folder_id, and this app has no folder concept of its own to build."""

from fastapi import APIRouter, Depends, Query

from app.deps import get_platform_client
from app.platform_client import PlatformClient
from app.schemas import FolderCreateRequest, FolderOut

router = APIRouter(prefix="/folders", tags=["folders"])


@router.get("", response_model=list[FolderOut])
def list_folders(parent_id: str | None = Query(None), client: PlatformClient = Depends(get_platform_client)):
    params = {"parent_id": parent_id} if parent_id else {}
    return client.get("/folders", params=params)["items"]


@router.post("", response_model=FolderOut, status_code=201)
def create_folder(body: FolderCreateRequest, client: PlatformClient = Depends(get_platform_client)):
    return client.post("/folders", json=body.model_dump())
