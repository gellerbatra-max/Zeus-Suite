"""Blob Storage I/O. Two distinct directions:
  - downloading a piece's geometry document from data-platform-api's own SAS download-url (bytes
    pattern-design-service wrote; this service reads them directly, per app/geometry.py's docstring)
  - uploading this service's own export artifacts (IGES files) to ITS OWN container -- an export is
    a derived artifact tied to an interchange_job, not a new piece version, so it doesn't go through
    the platform's begin_version/piece-version dance at all.

SAS generation mirrors data-platform-api/app/storage.py's own account-key SAS pattern (the Azurite
local-dev stand-in for real Azure's user-delegation SAS -- see that module's docstring).
"""

from datetime import UTC, datetime, timedelta

from azure.storage.blob import (
    BlobClient,
    BlobSasPermissions,
    BlobServiceClient,
    ContentSettings,
    generate_blob_sas,
)

from app.config import settings

EXPORTS_CONTAINER = "format-interchange-exports"
# Staged import bundles (raw IGES source + converted geometry + warnings) -- a distinct container
# from exports since an import artifact isn't a piece version either, and isn't downloadable as a
# plain file the way an export is (the Import Viewer reads it back as structured JSON, not a link).
IMPORTS_CONTAINER = "format-interchange-imports"

_service_client: BlobServiceClient | None = None


def get_blob_service_client() -> BlobServiceClient:
    global _service_client
    if _service_client is None:
        _service_client = BlobServiceClient.from_connection_string(settings.storage_connection_string)
    return _service_client


def _parse_connection_string(conn_str: str) -> dict[str, str]:
    parts: dict[str, str] = {}
    for segment in conn_str.split(";"):
        if not segment:
            continue
        key, _, value = segment.partition("=")
        parts[key] = value
    return parts


def _account_credentials() -> tuple[str, str]:
    parsed = _parse_connection_string(settings.storage_connection_string)
    return parsed["AccountName"], parsed["AccountKey"]


def download_bytes(sas_url: str) -> bytes:
    return BlobClient.from_blob_url(sas_url).download_blob().readall()


def ensure_exports_container() -> None:
    _ensure_container(EXPORTS_CONTAINER)


def upload_export(blob_key: str, payload: bytes, content_type: str = "text/plain") -> None:
    ensure_exports_container()
    container = get_blob_service_client().get_container_client(EXPORTS_CONTAINER)
    container.upload_blob(blob_key, payload, overwrite=True, content_settings=ContentSettings(content_type=content_type))


def _ensure_container(name: str) -> None:
    container = get_blob_service_client().get_container_client(name)
    if not container.exists():
        container.create_container()


def upload_import_bundle(blob_key: str, payload: bytes) -> None:
    _ensure_container(IMPORTS_CONTAINER)
    container = get_blob_service_client().get_container_client(IMPORTS_CONTAINER)
    container.upload_blob(blob_key, payload, overwrite=True, content_settings=ContentSettings(content_type="application/json"))


def download_import_bundle(blob_key: str) -> bytes:
    return get_blob_service_client().get_blob_client(IMPORTS_CONTAINER, blob_key).download_blob().readall()


def download_url_for_export(blob_key: str, expiry_minutes: int = 15) -> str:
    account_name, account_key = _account_credentials()
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=EXPORTS_CONTAINER,
        blob_name=blob_key,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.now(UTC) + timedelta(minutes=expiry_minutes),
    )
    blob_client = get_blob_service_client().get_blob_client(EXPORTS_CONTAINER, blob_key)
    return f"{blob_client.url}?{sas_token}"
