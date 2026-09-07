"""Marker Making Sec 1.11 (file/data management): the marker search/browse proxy and the
folder-scoped, alphanumerically-sorted sibling list "Open Next/Previous" stepping needs -- both
proxying through the real data-platform-api subprocess (see conftest.py)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_org_folder(unique: str):
    org_code = f"PICKER-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}
    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
    return headers, folder


def test_search_markers_by_text():
    unique = unique_suffix()
    headers, folder = _seed_org_folder(unique)
    with platform_client(headers) as p:
        p.post("/markers", json={"folder_id": folder["id"], "marker_code": f"ALPHA-{unique}", "marker_name": "Alpha Marker"})
        p.post("/markers", json={"folder_id": folder["id"], "marker_code": f"BRAVO-{unique}", "marker_name": "Bravo Marker"})

    resp = client.post("/markers/search", json={"text": f"ALPHA-{unique}"}, headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["total"] == 1
    assert body["results"][0]["code"] == f"ALPHA-{unique}"


def test_search_markers_browse_mode_with_status_filter():
    unique = unique_suffix()
    headers, folder = _seed_org_folder(unique)
    with platform_client(headers) as p:
        p.post("/markers", json={"folder_id": folder["id"], "marker_code": f"UNMADE-{unique}", "marker_name": "Unmade"})

    resp = client.post(
        "/markers/search", json={"folder_id": folder["id"], "workflow_status": ["unmade"]}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["total"] == 1
    assert body["results"][0]["workflow_status"] == "unmade"

    resp = client.post(
        "/markers/search", json={"folder_id": folder["id"], "workflow_status": ["made"]}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["total"] == 0


def test_marker_siblings_sorted_alphanumerically_and_scoped_to_folder():
    unique = unique_suffix()
    headers, folder = _seed_org_folder(unique)
    with platform_client(headers) as p:
        marker_c = p.post(
            "/markers", json={"folder_id": folder["id"], "marker_code": f"C-{unique}", "marker_name": "C"}
        ).json()
        p.post("/markers", json={"folder_id": folder["id"], "marker_code": f"A-{unique}", "marker_name": "A"})
        p.post("/markers", json={"folder_id": folder["id"], "marker_code": f"B-{unique}", "marker_name": "B"})

        other_folder = p.post("/folders", json={"name": f"Other-{unique}"}).json()
        p.post(
            "/markers", json={"folder_id": other_folder["id"], "marker_code": f"Z-{unique}", "marker_name": "Z"}
        )

    resp = client.get(f"/markers/{marker_c['id']}/siblings", headers=headers)
    assert resp.status_code == 200, resp.text
    codes = [row["marker_code"] for row in resp.json()]
    assert codes == [f"A-{unique}", f"B-{unique}", f"C-{unique}"]
    assert all(row["workflow_status"] == "unmade" for row in resp.json())
