"""Section 4.0's shared error envelope: `{"error": {"code", "message", "request_id"}}`."""

from fastapi import HTTPException


def api_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def not_found(entity_type: str) -> HTTPException:
    return api_error(404, "not_found", f"{entity_type} not found.")


def conflict(message: str, current: dict | None = None) -> HTTPException:
    detail: dict = {"code": "conflict", "message": message}
    if current is not None:
        detail["current"] = current
    return HTTPException(status_code=409, detail=detail)


def bad_request(message: str) -> HTTPException:
    return api_error(400, "bad_request", message)
