"""Milestone 2: object storage integration (Section 3.3's SAS-URL issuance/verification path),
built and tested in isolation before it's wired to piece_versions/marker_versions in Milestone 4.

Real Azure Blob Storage uses **user-delegation SAS** backed by the API's managed identity
(Section 3.3) -- that requires a real Azure subscription/Entra ID tenant, which isn't available
yet (see the "Local dev infra" decision in the Milestone 1 plan). Azurite, the local emulator this
module targets, doesn't support user-delegation SAS at all -- only classic account-key SAS. The
functions below use account-key SAS against Azurite as the local-dev stand-in; swapping to
`generate_blob_sas` with a `UserDelegationKey` (obtained via `BlobServiceClient.get_user_delegation_key`)
is the only change needed once real Azure Blob Storage + Entra ID are available.
"""

from datetime import UTC, datetime, timedelta

from azure.storage.blob import BlobSasPermissions, BlobServiceClient, generate_blob_sas

from app.config import settings

_service_client: BlobServiceClient | None = None


def get_blob_service_client() -> BlobServiceClient:
    global _service_client
    if _service_client is None:
        _service_client = BlobServiceClient.from_connection_string(settings.azurite_connection_string)
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
    parsed = _parse_connection_string(settings.azurite_connection_string)
    return parsed["AccountName"], parsed["AccountKey"]


def ensure_container(container: str) -> None:
    """Idempotent container creation -- containers are provisioned once per deployment
    (Section 3.1) but tests need this to set up a throwaway container on demand."""
    container_client = get_blob_service_client().get_container_client(container)
    if not container_client.exists():
        container_client.create_container()


def _blob_sas_url(container: str, blob_name: str, permission: BlobSasPermissions, expiry_minutes: int) -> str:
    account_name, account_key = _account_credentials()
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        account_key=account_key,
        permission=permission,
        expiry=datetime.now(UTC) + timedelta(minutes=expiry_minutes),
    )
    blob_client = get_blob_service_client().get_blob_client(container, blob_name)
    return f"{blob_client.url}?{sas_token}"


def generate_upload_sas_url(container: str, blob_name: str, expiry_minutes: int = 15) -> str:
    """Section 3.3 step 1: a short-lived, write-only URL for one blob. The caller (client
    application) PUTs bytes directly to this URL -- the API service never sees the payload."""
    return _blob_sas_url(container, blob_name, BlobSasPermissions(write=True, create=True), expiry_minutes)


def generate_download_sas_url(container: str, blob_name: str, expiry_minutes: int = 15) -> str:
    """Section 3.3 download path: a short-lived, read-only URL for one blob (default 15-minute
    expiry per the spec)."""
    return _blob_sas_url(container, blob_name, BlobSasPermissions(read=True), expiry_minutes)
