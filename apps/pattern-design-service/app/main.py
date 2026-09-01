"""pattern-design-service: a thin FastAPI client over data-platform-api. Holds no database of its
own -- see app/platform_client.py's module docstring."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api import folders, pieces
from app.platform_client import PlatformError

app = FastAPI(title="pattern-design-service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://127.0.0.1:5175"],
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


app.include_router(folders.router)
app.include_router(pieces.router)
