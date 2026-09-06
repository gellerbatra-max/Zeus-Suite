"""Same error envelope shape as data-platform-api's own app/errors.py: {"code", "message"}."""

from fastapi import HTTPException


def api_error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def not_found(entity_type: str) -> HTTPException:
    return api_error(404, "not_found", f"{entity_type} not found.")


def bad_request(message: str) -> HTTPException:
    return api_error(400, "bad_request", message)
