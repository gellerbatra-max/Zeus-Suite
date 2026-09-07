"""Shared helper for committing a converted geometry document to a real platform piece -- used by
both the single-piece Import Viewer commit (app/api/import_.py, Sec 1.4) and the Migration batch
commit (app/api/migration.py, Sec 2.6/Step 4). Neither endpoint's conversion produced a platform
piece version on its own; this is the one place that does the actual `POST /pieces` +
`begin_version`/upload/`complete` dance against data-platform-api."""

import hashlib
import json

from azure.storage.blob import BlobClient

from app.platform_client import PlatformClient


def commit_geometry_to_platform(client: PlatformClient, folder_id: str, piece_code: str, geometry: dict) -> dict:
    piece = client.post("/pieces", json={"folder_id": folder_id, "piece_code": piece_code, "piece_name": piece_code})
    payload = json.dumps(geometry).encode()
    begin = client.post(
        f"/pieces/{piece['id']}/versions",
        json={"file_format": "native", "size_bytes": len(payload), "comment": "Format Interchange commit"},
    )
    BlobClient.from_blob_url(begin["upload_url"]).upload_blob(payload, overwrite=True)
    checksum = hashlib.sha256(payload).hexdigest()
    client.post(f"/pieces/{piece['id']}/versions/{begin['version_id']}/complete", json={"checksum_sha256": checksum})
    return piece
