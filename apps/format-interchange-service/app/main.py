"""format-interchange-service: IGES piece export + import (Steps 1-2 of format_interchange_plan.md
Sec 7). Unlike pattern-design-service/marker-making-service, this app owns a real database (Sec 4)
-- see app/db.py's docstring."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import export, import_, import_profiles
from app.platform_client import PlatformError

app = FastAPI(title="format-interchange-service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5176", "http://127.0.0.1:5176"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(PlatformError)
async def platform_error_handler(request: Request, exc: PlatformError):
    return JSONResponse(status_code=exc.status_code, content={"error": {"source": "data-platform-api", "detail": exc.payload}})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": {"message": str(exc.detail)}})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"error": {"message": str(exc.errors())}})


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


app.include_router(export.router)
app.include_router(import_.router)
app.include_router(import_profiles.router)
