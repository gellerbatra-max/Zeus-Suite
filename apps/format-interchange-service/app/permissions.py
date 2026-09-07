"""Local RBAC gate (format_interchange_plan.md Sec 5: "All endpoints ... enforce RBAC roles
(interchange:export, interchange:import, interchange:migrate, interchange:review) at the API
layer") -- Step 5 hardening.

Every sibling thin-client service in this suite (see marker-making-service's own app/deps.py)
relies entirely on data-platform-api's own `require_permission` check: every mutation a thin
client makes eventually calls a platform endpoint that already enforces one, so the thin client
never needs its own gate. This service is different -- it owns real local state
(`migration_batch`/`migration_item`/`migration_finding`, `interchange_job`), and several endpoints
(item triage: resolve/block/accept-warning; batch/item reads; the report) never call the platform
at all, so there is no transitive check to lean on for those. This module is therefore this
service's own permission gate, the first one anywhere in the suite -- data-platform-api's own
`require_permission` (its own app/deps.py) is a plain function bound to a live DB `Session` and
`Actor` in that process; it isn't importable or callable cross-process, so this mirrors its 403
error shape rather than reusing its code, checking against the same flattened `permissions` list
`GET /me` already returns (see this module's own `get_actor`).

Permission-to-endpoint mapping (a deliberate choice this service makes, not dictated by the plan's
text beyond naming the four codes):
  interchange.export  -> app/api/export.py in full (submit + check status)
  interchange.import  -> app/api/import_.py + app/api/import_profiles.py in full
  interchange.migrate -> the migration BATCH lifecycle: create, run, commit
  interchange.review  -> the migration ITEM triage surface: list/get items, the report,
                          resolve, block, accept-warning -- plus this service's own audit log
"""

from fastapi import Depends, HTTPException

from app.deps import get_actor


def _require(actor: dict, code: str) -> dict:
    if code not in actor.get("permissions", []):
        raise HTTPException(status_code=403, detail={"code": "permission_denied", "message": f"Missing permission '{code}'."})
    return actor


def require_export(actor: dict = Depends(get_actor)) -> dict:
    return _require(actor, "interchange.export")


def require_import(actor: dict = Depends(get_actor)) -> dict:
    return _require(actor, "interchange.import")


def require_migrate(actor: dict = Depends(get_actor)) -> dict:
    return _require(actor, "interchange.migrate")


def require_review(actor: dict = Depends(get_actor)) -> dict:
    return _require(actor, "interchange.review")
