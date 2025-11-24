"""
FastAPI Backend Core - RUV SPARC UI Dashboard
Production-ready API with security, performance, and monitoring

Critical Risk Mitigations:
- CA001: FastAPI 0.121.0+ (CVE-2024-47874 patch)
- CA006: OWASP API1:2023 Broken Object Level Authorization checks
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import fastapi
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.config.settings import get_settings
from app.middleware.auth import verify_jwt_token
from app.routers import tasks, projects, agents, health, auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiter configuration
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan context manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting RUV SPARC UI Dashboard API...")
    logger.info(f"📦 FastAPI version: {fastapi.__version__}")
    logger.info(f"🔒 Security: JWT + Rate Limiting + CORS enabled")
    logger.info(f"🌐 CORS origins: {settings.CORS_ORIGINS}")

    # Initialize database connection pool
    from app.database import init_db
    await init_db()
    logger.info("✅ Database connection pool initialized")

    # P4_T3: Initialize WebSocket task status broadcaster
    from app.websocket.task_status_broadcaster import task_status_broadcaster
    from app.websocket.connection_manager import connection_manager

    try:
        await connection_manager.initialize()
        await task_status_broadcaster.initialize()
        await task_status_broadcaster.start_listening()
        logger.info("✅ Task status broadcaster initialized and listening")
    except Exception as e:
        logger.error(f"⚠️  Failed to initialize task status broadcaster: {e}")
        logger.warning("Real-time task updates will not be available")

    yield

    # Shutdown
    logger.info("🛑 Shutting down RUV SPARC UI Dashboard API...")

    # Stop task status broadcaster
    try:
        await task_status_broadcaster.stop_listening()
        await task_status_broadcaster.close()
        await connection_manager.close()
        logger.info("✅ Task status broadcaster stopped")
    except Exception as e:
        logger.error(f"Error stopping task status broadcaster: {e}")

    from app.database import close_db
    await close_db()
    logger.info("✅ Database connections closed")


# Initialize FastAPI application
app = FastAPI(
    title="RUV SPARC UI Dashboard API",
    description="""
# RUV SPARC UI Dashboard API

Production-ready FastAPI backend with comprehensive security, performance optimization, and real-time monitoring.

## 🚀 Features

- **Task Scheduling**: Automated skill/agent execution with cron expressions
- **Project Management**: Organize tasks into projects with nested hierarchies
- **Agent Registry**: Track agent activity, performance metrics, and execution history
- **Real-time Updates**: WebSocket support for live agent activity feeds
- **Security**: JWT authentication, rate limiting, OWASP BOLA protection
- **Performance**: Connection pooling, GZip compression, indexed queries
- **Observability**: Structured logging, request tracing, Memory MCP integration

## 🔒 Security

- **Authentication**: JWT Bearer tokens (Authorization: Bearer <token>)
- **Rate Limiting**: 100 requests/minute per IP (1000/min for activity logging)
- **BOLA Protection**: Resource ownership verification on all operations
- **Input Validation**: Comprehensive Pydantic schema validation
- **Security Headers**: CSP, HSTS, X-Frame-Options, X-Content-Type-Options

## 📊 Rate Limits

| Endpoint Type | Limit | Period |
|--------------|-------|--------|
| Standard API | 100 req | 1 min |
| Activity Logging | 1000 req | 1 min |
| Agent Creation | 60 req | 1 min |

## 🔧 Error Codes

- **400 Bad Request**: Invalid input, malformed cron expression, validation errors
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: User does not own the requested resource
- **404 Not Found**: Resource does not exist or has been soft deleted
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Unexpected server error (includes X-Request-ID for tracing)

## 📦 Technology Stack

- **Framework**: FastAPI 0.121.0+ (CVE-2024-47874 patched)
- **Database**: PostgreSQL 15+ with async connection pooling
- **Cache/Memory**: Memory MCP with ChromaDB vector storage
- **WebSocket**: Real-time agent activity broadcasting
- **Validation**: Pydantic 2.x with comprehensive schemas

## 🔗 Quick Links

- **Swagger UI**: `/api/docs` (interactive API explorer)
- **ReDoc**: `/api/redoc` (alternative documentation)
- **OpenAPI Schema**: `/api/openapi.json` (machine-readable spec)
- **Health Check**: `/api/v1/health` (system status)

## 📚 API Documentation

Complete API documentation available at:
- Interactive docs: `/api/docs`
- Markdown guide: `docs/API_DOCS.md`
- Example requests: `docs/api-examples/`

## 🌐 Base URL

Development: `http://localhost:8000`
Production: `https://api.ruv-sparc.io` (replace with actual URL)
    """,
    version="1.0.0",
    contact={
        "name": "RUV SPARC Team",
        "email": "support@ruv-sparc.io",
        "url": "https://github.com/ruvnet/ruv-sparc-ui-dashboard"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
    openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and system status endpoints"
        },
        {
            "name": "tasks",
            "description": "Scheduled task management - create, list, update, delete tasks with cron scheduling"
        },
        {
            "name": "projects",
            "description": "Project management - organize tasks into projects with search, pagination, and nested display"
        },
        {
            "name": "agents",
            "description": "Agent registry - track agent activity, performance metrics, and execution history"
        }
    ],
    lifespan=lifespan,
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        },
        {
            "url": "https://api.ruv-sparc.io",
            "description": "Production server"
        }
    ],
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,
        "displayRequestDuration": True,
        "filter": True,
        "persistAuthorization": True
    }
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware - Development configuration
# In production, replace with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # ["http://localhost:3000"] for dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"]
)

# GZip compression for responses > 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted host middleware (production)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors
    Prevents sensitive information leakage
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_id": str(request.state.request_id) if hasattr(request.state, "request_id") else None
        }
    )


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """
    Add unique request ID to each request for tracing
    """
    import uuid
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    return response


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add security headers to all responses
    """
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"

    return response


# Include routers with API versioning
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["health"]
)

# P5_T1: Authentication router (multi-user support with JWT)
app.include_router(
    auth.router,
    tags=["Authentication"]
)
    health.router,
    prefix="/api/v1",
    tags=["health"]
)

app.include_router(
    tasks.router,
    prefix="/api/v1/tasks",
    tags=["tasks"]
)

app.include_router(
    projects.router,
    prefix="/api/v1/projects",
    tags=["projects"]
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["agents"]
)


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """
    Root endpoint - redirect to API docs
    """
    return {
        "message": "RUV SPARC UI Dashboard API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn

    # Development server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
