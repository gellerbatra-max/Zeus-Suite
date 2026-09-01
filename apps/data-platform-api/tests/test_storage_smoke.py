"""Milestone 2 exit check: a script can request a SAS PUT URL, upload a test file, request a SAS
GET URL, and download back a byte-identical file, entirely without the API service touching the
bytes -- `app.storage` only ever mints URLs; the byte transfer below goes straight to Azurite via
`BlobClient.from_blob_url`, exactly as a real client application would against Azure Blob Storage.
"""

import uuid

from azure.storage.blob import BlobClient

from app.storage import (
    ensure_container,
    generate_download_sas_url,
    generate_upload_sas_url,
)


def test_sas_upload_and_download_roundtrip():
    container = "dmp-pieces"
    ensure_container(container)
    blob_name = f"smoke-test/{uuid.uuid4().hex}.bin"
    payload = b"hello from the milestone 2 smoke test"

    upload_url = generate_upload_sas_url(container, blob_name)
    BlobClient.from_blob_url(upload_url).upload_blob(payload, overwrite=True)

    download_url = generate_download_sas_url(container, blob_name)
    downloaded = BlobClient.from_blob_url(download_url).download_blob().readall()

    assert downloaded == payload
