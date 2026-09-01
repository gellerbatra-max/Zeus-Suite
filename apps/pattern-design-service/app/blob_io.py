"""Uploads/downloads a piece's geometry document bytes directly to/from Azure Blob Storage, using
the SAS URLs data-platform-api hands back from its `/pieces/{id}/versions` (upload) and
`/pieces/{id}/versions/{version_id}/download-url` (download) endpoints.

Unlike marker-making-service, this service's core job *is* writing/reading piece geometry, so
talking to Blob Storage directly (via a SAS URL the platform issued, never a container credential
of this service's own) is production behavior here, not just a test-seeding convenience.
"""

from azure.storage.blob import BlobClient


def upload_blob(sas_url: str, payload: bytes) -> None:
    BlobClient.from_blob_url(sas_url).upload_blob(payload, overwrite=True)


def download_blob(sas_url: str) -> bytes:
    return BlobClient.from_blob_url(sas_url).download_blob().readall()
