"""Phase 2 Slice 1 verification: an operator can open a marker's workspace, see the pieces its
order's style calls for, save a manual placement covering every piece (reaching 'made' status
through the platform's real workflow-transition rules), and submit/poll an Engine B nesting job
through the platform's existing generic job queue."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_order_with_two_pieces(unique: str):
    org_code = f"MM-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")

        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
        style = p.post(
            "/styles",
            json={"folder_id": folder["id"], "style_number": f"STY-{unique}", "style_name": "Test Style"},
        ).json()

        piece_a = seed_nestable_piece(p, folder["id"], f"PANEL-A-{unique}", "Panel A")
        piece_b = seed_nestable_piece(p, folder["id"], f"PANEL-B-{unique}", "Panel B")
        for piece in (piece_a, piece_b):
            p.post(f"/styles/{style['id']}/pieces", json={"piece_id": piece["id"]})

        order = p.post(
            "/orders",
            json={"folder_id": folder["id"], "order_number": f"ORD-{unique}", "style_id": style["id"]},
        ).json()
        marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Test Marker",
                  "order_id": order["id"]},
        ).json()

    return headers, order, marker, piece_a, piece_b


def test_workspace_load_save_and_status_transition():
    unique = unique_suffix()
    headers, _order, marker, piece_a, piece_b = _seed_order_with_two_pieces(unique)

    resp = client.get(f"/markers/{marker['id']}/workspace", headers=headers)
    assert resp.status_code == 200, resp.text
    workspace = resp.json()
    assert workspace["workflow_status"] == "unmade"
    assert {p["piece_code"] for p in workspace["available_pieces"]} == {
        f"PANEL-A-{unique}", f"PANEL-B-{unique}",
    }
    assert workspace["placements"] == []

    save_body = {
        "placements": [
            {
                "piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
                "placement_data": {"x": 10, "y": 10, "rotation_deg": 0, "width": 80, "height": 120},
            },
            {
                "piece_id": piece_b["id"], "size_code": "M", "quantity": 1,
                "placement_data": {"x": 100, "y": 10, "rotation_deg": 90, "flip_x": True, "width": 60, "height": 90},
            },
        ]
    }
    resp = client.put(f"/markers/{marker['id']}/workspace", json=save_body, headers=headers)
    assert resp.status_code == 200, resp.text
    workspace = resp.json()

    # Both style pieces are placed -> the platform's real workflow_transitions walk
    # unmade -> needs_approval -> made (there is no direct unmade -> made transition).
    assert workspace["workflow_status"] == "made"
    assert len(workspace["placements"]) == 2
    placement_by_piece = {p["piece_id"]: p for p in workspace["placements"]}
    assert placement_by_piece[piece_a["id"]]["placement_data"]["x"] == 10
    assert placement_by_piece[piece_b["id"]]["placement_data"]["rotation_deg"] == 90
    assert placement_by_piece[piece_b["id"]]["placement_data"]["flip_x"] is True

    # Reload independently -- confirms this actually persisted through the real platform API,
    # not just an in-memory echo of the request.
    resp = client.get(f"/markers/{marker['id']}/workspace", headers=headers)
    assert len(resp.json()["placements"]) == 2


def test_workspace_partial_placement_status():
    unique = unique_suffix()
    headers, _order, marker, piece_a, _piece_b = _seed_order_with_two_pieces(unique)

    save_body = {
        "placements": [
            {"piece_id": piece_a["id"], "size_code": "M", "quantity": 1,
             "placement_data": {"x": 0, "y": 0, "width": 80, "height": 120}},
        ]
    }
    resp = client.put(f"/markers/{marker['id']}/workspace", json=save_body, headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["workflow_status"] == "partial"


def test_nesting_job_submit_and_worker_completion():
    unique = unique_suffix()
    headers, order, marker, _piece_a, _piece_b = _seed_order_with_two_pieces(unique)

    resp = client.post(
        "/nesting-jobs", json={"marker_id": marker["id"], "order_id": order["id"]}, headers=headers
    )
    assert resp.status_code == 202, resp.text
    job = resp.json()
    assert job["status"] == "queued"

    resp = client.get(f"/nesting-jobs/{job['id']}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "queued"

    # Simulate the platform's real worker completing the job -- via the exact same HTTP contract
    # data-platform-api's own app/job_worker.py uses (heartbeat then complete), authenticated as
    # a service-account-flavored identity holding only job.worker. This proves our /nesting-jobs
    # wrapper correctly proxies the platform's real job lifecycle; the platform's own worker
    # mechanics are already covered by that service's own Milestone 6 test suite.
    worker_username = f"worker-{unique}"
    worker_headers = {"X-Dev-User": worker_username, "X-Dev-Org": f"MM-{unique}"}
    with platform_client(worker_headers) as p:
        p.get("/me")  # JIT-provision the worker identity before granting it a role
        grant_role(f"MM-{unique}", worker_username, "job_worker")
        p.post(f"/jobs/{job['id']}/heartbeat", json={"progress_pct": 100})
        p.post(f"/jobs/{job['id']}/complete", json={"status": "succeeded", "result_ref": {"note": "stub result"}})

    resp = client.get(f"/nesting-jobs/{job['id']}", headers=headers)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "succeeded"
    assert body["result_ref"] == {"note": "stub result"}
