"""Marker Making Sec 1.5 (layrules automation): Layrule Search Parameter Table CRUD (thin proxy)
and the real logic -- capture a marker's placements into a reusable layrule, then apply it to a
different (compatible) marker -- proxying through the real data-platform-api subprocess (see
conftest.py)."""

from fastapi.testclient import TestClient
from helpers import grant_role, platform_client, seed_nestable_piece, unique_suffix

from app.main import app

client = TestClient(app)


def _seed_style_marker(unique: str, piece_codes: list[str]):
    org_code = f"LAYRULE-{unique}"
    username = f"operator-{unique}"
    headers = {"X-Dev-User": username, "X-Dev-Org": org_code}

    with platform_client(headers) as p:
        p.get("/me")  # JIT-provision with default 'viewer'
        grant_role(org_code, username, "admin")
        folder = p.post("/folders", json={"name": f"Folder-{unique}"}).json()
        style = p.post(
            "/styles", json={"folder_id": folder["id"], "style_number": f"STY-{unique}", "style_name": "Style"}
        ).json()
        pieces = {}
        for code in piece_codes:
            piece = seed_nestable_piece(p, folder["id"], f"{code}-{unique}", code)
            p.post(f"/styles/{style['id']}/pieces", json={"piece_id": piece["id"]})
            pieces[code] = piece
        order = p.post(
            "/orders", json={"folder_id": folder["id"], "order_number": f"ORD-{unique}", "style_id": style["id"]}
        ).json()
        marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-{unique}", "marker_name": "Layrule Marker",
                  "order_id": order["id"]},
        ).json()

    return headers, folder, marker, pieces


def test_layrule_settings_round_trip():
    unique = unique_suffix()
    headers, _folder, marker, _pieces = _seed_style_marker(unique, ["PANEL-A"])

    resp = client.get(f"/markers/{marker['id']}/layrules/settings", headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"force_layrule_name": None, "layrule_search_table_id": None}

    table = client.post("/layrule-search-tables", json={"name": f"Linked-{unique}"}, headers=headers).json()
    resp = client.patch(
        f"/markers/{marker['id']}/layrules/settings",
        json={"force_layrule_name": "REPEAT-42", "layrule_search_table_id": table["id"]},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    assert resp.json() == {"force_layrule_name": "REPEAT-42", "layrule_search_table_id": table["id"]}

    resp = client.get(f"/markers/{marker['id']}/layrules/settings", headers=headers)
    assert resp.json() == {"force_layrule_name": "REPEAT-42", "layrule_search_table_id": table["id"]}


def test_layrule_search_table_crud():
    unique = unique_suffix()
    headers = {"X-Dev-User": f"op-{unique}", "X-Dev-Org": f"LRSEARCH-{unique}"}
    with platform_client(headers) as p:
        p.get("/me")
        grant_role(f"LRSEARCH-{unique}", f"op-{unique}", "admin")

    resp = client.post(
        "/layrule-search-tables",
        json={"name": f"Search-{unique}", "area_deviation_pct": 10.0, "allow_overrides": False},
        headers=headers,
    )
    assert resp.status_code == 200, resp.text
    table = resp.json()
    assert table["area_deviation_pct"] == 10.0
    assert table["allow_overrides"] is False
    assert table["version"] == 1

    resp = client.post(
        "/layrule-search-tables", json={"name": "Bad", "area_deviation_pct": -1.0}, headers=headers,
    )
    assert resp.status_code == 400

    resp = client.patch(f"/layrule-search-tables/{table['id']}", json={"area_deviation_pct": 15.0}, headers=headers)
    assert resp.status_code == 200, resp.text
    assert resp.json()["area_deviation_pct"] == 15.0
    assert resp.json()["version"] == 2

    resp = client.get("/layrule-search-tables", headers=headers)
    assert resp.status_code == 200, resp.text
    assert len(resp.json()["items"]) == 1

    resp = client.delete(f"/layrule-search-tables/{table['id']}", headers=headers)
    assert resp.status_code == 204, resp.text


def test_capture_layrule_requires_placements():
    unique = unique_suffix()
    headers, _folder, marker, _pieces = _seed_style_marker(unique, ["PANEL-A", "PANEL-B"])

    resp = client.post(f"/markers/{marker['id']}/layrules/capture", json={"name": "Empty"}, headers=headers)
    assert resp.status_code == 400


def test_capture_and_apply_layrule_to_matching_marker():
    unique = unique_suffix()
    headers, folder, source_marker, pieces = _seed_style_marker(unique, ["PANEL-A", "PANEL-B"])

    client.put(
        f"/markers/{source_marker['id']}/workspace",
        json={
            "placements": [
                {"piece_id": pieces["PANEL-A"]["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 10, "y": 20, "width": 50, "height": 40}},
                {"piece_id": pieces["PANEL-B"]["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 80, "y": 5, "width": 30, "height": 60}},
            ]
        },
        headers=headers,
    )

    resp = client.post(
        f"/markers/{source_marker['id']}/layrules/capture", json={"name": f"Layrule-{unique}"}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    layrule = resp.json()
    assert layrule["piece_count"] == 2

    # A second, empty marker on the SAME style/order -- same available pieces, zero placements.
    with platform_client(headers) as p:
        order_id = p.get(f"/markers/{source_marker['id']}").json()["order_id"]
        target_marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-TARGET-{unique}", "marker_name": "Target Marker",
                  "order_id": order_id},
        ).json()

    resp = client.post(
        f"/markers/{target_marker['id']}/layrules/apply", json={"layrule_id": layrule["id"]}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    result = resp.json()
    assert set(result["applied_piece_ids"]) == {pieces["PANEL-A"]["id"], pieces["PANEL-B"]["id"]}
    assert result["unmatched_piece_ids"] == []
    assert result["warning"] is None

    with platform_client(headers) as p:
        raw_placements = p.get(f"/markers/{target_marker['id']}/pieces").json()
    placements_by_piece = {row["piece_id"]: row["placement_data"] for row in raw_placements}
    assert placements_by_piece[pieces["PANEL-A"]["id"]]["x"] == 10.0
    assert placements_by_piece[pieces["PANEL-A"]["id"]]["width"] == 50.0
    assert placements_by_piece[pieces["PANEL-B"]["id"]]["x"] == 80.0
    assert placements_by_piece[pieces["PANEL-B"]["id"]]["height"] == 60.0


def test_apply_layrule_reports_unmatched_pieces():
    unique = unique_suffix()
    headers, folder, source_marker, pieces = _seed_style_marker(unique, ["PANEL-A", "PANEL-B"])

    client.put(
        f"/markers/{source_marker['id']}/workspace",
        json={
            "placements": [
                {"piece_id": pieces["PANEL-A"]["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 0, "y": 0, "width": 20, "height": 20}},
                {"piece_id": pieces["PANEL-B"]["id"], "size_code": "M", "quantity": 1,
                 "placement_data": {"x": 30, "y": 0, "width": 20, "height": 20}},
            ]
        },
        headers=headers,
    )
    layrule = client.post(
        f"/markers/{source_marker['id']}/layrules/capture", json={"name": f"Layrule2-{unique}"}, headers=headers,
    ).json()

    # A different style in the SAME org that reuses the *same* PANEL-A piece row but never added
    # PANEL-B -- PANEL-B has no home here. (Layrules are org-scoped on the platform, so the target
    # marker must share the org; piece matching is by piece id, so this must be the same row, not
    # a freshly seeded piece that merely shares a piece_code.)
    with platform_client(headers) as p:
        other_style = p.post(
            "/styles", json={"folder_id": folder["id"], "style_number": f"STY-{unique}-B", "style_name": "Other Style"}
        ).json()
        p.post(f"/styles/{other_style['id']}/pieces", json={"piece_id": pieces["PANEL-A"]["id"]})
        other_order = p.post(
            "/orders", json={"folder_id": folder["id"], "order_number": f"ORD-{unique}-B", "style_id": other_style["id"]}
        ).json()
        other_marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-OTHER-{unique}", "marker_name": "Other Marker",
                  "order_id": other_order["id"]},
        ).json()

    resp = client.post(
        f"/markers/{other_marker['id']}/layrules/apply", json={"layrule_id": layrule["id"]}, headers=headers,
    )
    assert resp.status_code == 200, resp.text
    result = resp.json()
    assert result["applied_piece_ids"] == [pieces["PANEL-A"]["id"]]
    assert result["unmatched_piece_ids"] == [pieces["PANEL-B"]["id"]]
    assert result["warning"] is not None


def test_apply_layrule_rejects_when_area_deviation_exceeds_search_table_threshold():
    unique = unique_suffix()
    headers, folder, source_marker, pieces = _seed_style_marker(unique, ["PANEL-A"])

    # Captured with a deliberately huge bounding box -- far larger than the piece's own
    # synthetic-geometry footprint, to force a large area deviation on apply.
    client.put(
        f"/markers/{source_marker['id']}/workspace",
        json={"placements": [
            {"piece_id": pieces["PANEL-A"]["id"], "size_code": "M", "quantity": 1,
             "placement_data": {"x": 0, "y": 0, "width": 5000, "height": 5000}},
        ]},
        headers=headers,
    )
    layrule = client.post(
        f"/markers/{source_marker['id']}/layrules/capture", json={"name": f"BigLayrule-{unique}"}, headers=headers,
    ).json()

    search_table = client.post(
        "/layrule-search-tables",
        json={"name": f"Strict-{unique}", "area_compare": True, "area_deviation_pct": 1.0},
        headers=headers,
    ).json()

    with platform_client(headers) as p:
        target_marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-STRICT-{unique}", "marker_name": "Strict Target"},
        ).json()
        p.patch(
            f"/markers/{target_marker['id']}", json={"layrule_search_table_id": search_table["id"]},
            headers={"If-Match-Version": str(target_marker["version"])},
        )

    resp = client.post(
        f"/markers/{target_marker['id']}/layrules/apply", json={"layrule_id": layrule["id"]}, headers=headers,
    )
    assert resp.status_code == 409


def test_apply_layrule_rejects_when_overrides_disabled_and_placements_exist():
    unique = unique_suffix()
    headers, folder, source_marker, pieces = _seed_style_marker(unique, ["PANEL-A"])

    client.put(
        f"/markers/{source_marker['id']}/workspace",
        json={"placements": [
            {"piece_id": pieces["PANEL-A"]["id"], "size_code": "M", "quantity": 1,
             "placement_data": {"x": 0, "y": 0, "width": 20, "height": 20}},
        ]},
        headers=headers,
    )
    layrule = client.post(
        f"/markers/{source_marker['id']}/layrules/capture", json={"name": f"NoOverride-{unique}"}, headers=headers,
    ).json()

    search_table = client.post(
        "/layrule-search-tables",
        json={"name": f"NoOverrideTable-{unique}", "area_compare": False, "allow_overrides": False},
        headers=headers,
    ).json()

    with platform_client(headers) as p:
        target_marker = p.post(
            "/markers",
            json={"folder_id": folder["id"], "marker_code": f"MRK-NOOVR-{unique}", "marker_name": "No Override Target"},
        ).json()
        p.patch(
            f"/markers/{target_marker['id']}", json={"layrule_search_table_id": search_table["id"]},
            headers={"If-Match-Version": str(target_marker["version"])},
        )
    client.put(
        f"/markers/{target_marker['id']}/workspace",
        json={"placements": [
            {"piece_id": pieces["PANEL-A"]["id"], "size_code": "M", "quantity": 1,
             "placement_data": {"x": 5, "y": 5, "width": 20, "height": 20}},
        ]},
        headers=headers,
    )

    resp = client.post(
        f"/markers/{target_marker['id']}/layrules/apply", json={"layrule_id": layrule["id"]}, headers=headers,
    )
    assert resp.status_code == 409
