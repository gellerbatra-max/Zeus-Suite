"""A thin wrapper over data-platform-api's real REST API. This service holds no ORM models and no
database connection of its own -- every persistence call goes through here.

Identity is forwarded, not owned: every call carries the *caller's* X-Dev-User/X-Dev-Org headers
untouched (see app/deps.py), the local-dev stand-in for forwarding/exchanging the operator's own
Entra ID token in production. This service never authenticates as a separate identity of its own
for these calls -- it acts *as* the operator, not *instead of* them.
"""

import httpx

from app.config import settings

_shared_client: httpx.Client | None = None


def configure_client(client: httpx.Client) -> None:
    """Test hook: inject an ASGITransport-backed client pointed at data-platform-api's real app
    in-process, instead of making real network calls to a second running server."""
    global _shared_client
    _shared_client = client


def _get_client() -> httpx.Client:
    global _shared_client
    if _shared_client is None:
        _shared_client = httpx.Client(base_url=settings.platform_api_url, timeout=30.0)
    return _shared_client


class PlatformError(Exception):
    def __init__(self, status_code: int, payload: object):
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"data-platform-api returned {status_code}: {payload}")


class PlatformClient:
    def __init__(self, identity_headers: dict[str, str]):
        self._headers = identity_headers

    def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        headers = {**self._headers, **kwargs.pop("headers", {})}
        response = _get_client().request(method, path, headers=headers, **kwargs)
        if response.status_code >= 400:
            try:
                payload = response.json()
            except ValueError:
                payload = response.text
            raise PlatformError(response.status_code, payload)
        return response

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs).json()

    def post(self, path: str, json: object = None, **kwargs):
        response = self._request("POST", path, json=json, **kwargs)
        return response.json() if response.content else None

    def put(self, path: str, json: object = None, **kwargs):
        response = self._request("PUT", path, json=json, **kwargs)
        return response.json() if response.content else None
