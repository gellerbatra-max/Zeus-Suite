"""FastAPI application entrypoint: Milestone 4's Section 4 REST surface (folders, pieces, styles,
markers, orders/bundles, workflow metadata, audit log) on top of Milestones 1-3's schema, object
storage, and permission-resolution/JIT-provisioning building blocks."""

import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import audit_log, folders, markers, meta, orders, pieces, styles, workflow

app = FastAPI(title="data-platform-api", version="0.1.0")


@app.middleware("http")
async def assign_request_id(request: Request, call_next):
    request.state.request_id = uuid.uuid4()
    response = await call_next(request)
    response.headers["X-Request-Id"] = str(request.state.request_id)
    return response


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = getattr(request.state, "request_id", None)
    detail = exc.detail
    if isinstance(detail, dict) and "code" in detail and "message" in detail:
        error = {**detail, "request_id": str(request_id)}
    else:
        error = {"code": "http_error", "message": str(detail), "request_id": str(request_id)}
    return JSONResponse(status_code=exc.status_code, content={"error": error})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=400,
        content={"error": {"code": "validation_error", "message": str(exc.errors()), "request_id": str(request_id)}},
    )


app.include_router(meta.router)
app.include_router(folders.router)
app.include_router(pieces.router)
app.include_router(styles.router)
app.include_router(markers.router)
app.include_router(orders.router)
app.include_router(workflow.router)
app.include_router(audit_log.router)
