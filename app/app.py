"""FastAPI application entrypoint."""

from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .internal.config import get_settings
from .internal.logs import get_logger, setup_logging
from .internal.models import ErrorResponse, HealthResponse, MessageResponse
from .orchestrator.manager import ConversionManager
from .routers import convert

settings = get_settings()
setup_logging(settings.log_level)
logger = get_logger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    # Startup
    app.state.started_at = datetime.now(timezone.utc)
    try:
        app.state.manager = ConversionManager(settings)
        logger.info("Application started in %s mode", settings.app_env)
    except Exception as e:
        logger.error("Failed to initialize application: %s", e)
        raise

    yield

    # Shutdown
    logger.info("Application shutdown complete")


def _uptime_seconds(started_at: datetime) -> int:
    """Calculate uptime in seconds."""
    return max(0, int((datetime.now(timezone.utc) - started_at).total_seconds()))


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    docs_url = "/docs" if settings.docs_enabled else None
    redoc_url = "/redoc" if settings.docs_enabled else None
    openapi_url = "/openapi.json" if settings.docs_enabled else None

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,
    )

    # === Middleware Stack ===

    trusted_hosts = settings.allowed_hosts or ["*"]
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)
    app.add_middleware(GZipMiddleware, minimum_size=settings.gzip_min_size)

    if settings.cors_origins:
        allow_credentials = "*" not in settings.cors_origins
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=allow_credentials,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(convert.router, prefix=settings.api_prefix)

    # === Custom Middleware - Request Context ===

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        """Add request tracking and timing to all requests."""
        request_id = request.headers.get("x-request-id", str(uuid4()))
        request.state.request_id = request_id
        start = time.perf_counter()

        try:
            response = await asyncio.wait_for(
                call_next(request), timeout=settings.request_timeout_seconds
            )
        except asyncio.TimeoutError:
            duration_ms = int((time.perf_counter() - start) * 1000)
            payload = ErrorResponse(
                error_code="REQUEST_TIMEOUT",
                message=(
                    f"Request exceeded timeout of {settings.request_timeout_seconds} seconds."
                ),
                request_id=request_id,
            )
            response = JSONResponse(status_code=504, content=payload.model_dump())
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time-Ms"] = str(duration_ms)
            logger.warning(
                "Request timeout request_id=%s method=%s path=%s duration_ms=%s",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )
            return response

        duration_ms = int((time.perf_counter() - start) * 1000)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)
        logger.info(
            "Request request_id=%s method=%s path=%s status=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    # === Exception Handlers ===

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTPException with structured response."""
        request_id = getattr(request.state, "request_id", None)
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error_code="HTTP_ERROR",
                message=str(exc.detail),
                request_id=request_id,
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle validation errors with structured response."""
        request_id = getattr(request.state, "request_id", None)
        details = "; ".join([error.get("msg", "invalid value") for error in exc.errors()])
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                error_code="VALIDATION_ERROR",
                message=details or "Validation failed.",
                request_id=request_id,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        """Handle unhandled exceptions with structured response."""
        request_id = getattr(request.state, "request_id", None)
        logger.exception("Unhandled error (request_id=%s)", request_id)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code="INTERNAL_SERVER_ERROR",
                message="Unexpected internal error.",
                request_id=request_id,
            ).model_dump(),
        )

    # === Health & Info Endpoints ===

    @app.get("/", response_model=MessageResponse)
    def root() -> MessageResponse:
        """Root endpoint."""
        return MessageResponse(message=f"{settings.app_name} is running.")

    @app.get("/health/liveness", response_model=HealthResponse)
    def liveness(request: Request) -> HealthResponse:
        """Liveness probe endpoint."""
        started_at = getattr(request.app.state, "started_at", datetime.now(timezone.utc))
        return HealthResponse(
            status="alive",
            service=settings.app_name,
            version=settings.app_version,
            uptime_seconds=_uptime_seconds(started_at),
        )

    @app.get("/health/readiness", response_model=HealthResponse)
    def readiness(request: Request):
        """Readiness probe endpoint."""
        started_at = getattr(request.app.state, "started_at", datetime.now(timezone.utc))
        manager = getattr(request.app.state, "manager", None)
        is_ready = bool(manager and manager.is_ready())
        payload = HealthResponse(
            status="ready" if is_ready else "not_ready",
            service=settings.app_name,
            version=settings.app_version,
            uptime_seconds=_uptime_seconds(started_at),
        )

        if not is_ready:
            return JSONResponse(status_code=503, content=payload.model_dump())

        return payload

    return app


app = create_app()
