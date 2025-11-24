# OpenAPI Customization Guide

This document explains how the RUV SPARC API's OpenAPI documentation is customized.

---

## 📋 Table of Contents

1. [FastAPI Configuration](#fastapi-configuration)
2. [Pydantic Schema Customization](#pydantic-schema-customization)
3. [Endpoint Documentation](#endpoint-documentation)
4. [Authentication Setup](#authentication-setup)
5. [Rate Limiting Documentation](#rate-limiting-documentation)
6. [Error Code Documentation](#error-code-documentation)
7. [Swagger UI Customization](#swagger-ui-customization)
8. [Static HTML Export](#static-html-export)

---

## 🚀 FastAPI Configuration

### Main Application Setup

Location: `app/main.py`

```python
app = FastAPI(
    title="RUV SPARC UI Dashboard API",
    description="""
    # Comprehensive markdown description
    - Features
    - Security details
    - Rate limits
    - Error codes
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
    openapi_tags=[
        {
            "name": "tasks",
            "description": "Task management endpoints"
        },
        # ... more tags
    ],
    servers=[
        {"url": "http://localhost:8000", "description": "Development"},
        {"url": "https://api.ruv-sparc.io", "description": "Production"}
    ],
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "defaultModelsExpandDepth": 3,
        "displayRequestDuration": True,
        "filter": True,
        "persistAuthorization": True
    }
)
```

---

## 📝 Pydantic Schema Customization

### Adding Descriptions to Models

Location: `app/schemas/task_schemas.py`

```python
class TaskCreate(BaseModel):
    """Schema for creating a new scheduled task"""

    skill_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of skill to execute",
        examples=["pair-programming", "code-review-assistant"]
    )

    schedule_cron: str = Field(
        ...,
        description="Cron expression (e.g., '0 0 * * *' for daily at midnight)",
        examples=["0 0 * * *", "*/15 * * * *"]
    )

    params: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Execution parameters for the skill",
        examples=[{"mode": "driver", "language": "python"}]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "skill_name": "pair-programming",
                    "schedule_cron": "0 9 * * 1-5",
                    "params": {"mode": "driver"}
                }
            ]
        }
    }
```

### Field Validators

```python
@field_validator("schedule_cron")
@classmethod
def validate_cron_expression(cls, v: str) -> str:
    """Validate cron expression syntax"""
    try:
        croniter(v, datetime.now())
        return v
    except (ValueError, KeyError) as e:
        raise ValueError(
            f"Invalid cron expression '{v}': {str(e)}. "
            f"Use format: 'minute hour day month weekday'"
        )
```

---

## 🛣️ Endpoint Documentation

### Comprehensive Endpoint Docstrings

Location: `app/routers/tasks.py`

```python
@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new scheduled task",
    description="""
    Create a new scheduled task for automated skill/agent execution.

    **Security:**
    - Requires JWT authentication
    - Task is automatically associated with authenticated user
    - OWASP API1:2023 BOLA protection enforced

    **Validation:**
    - Cron expression syntax validated
    - Skill name format validated
    - Parameters JSON validated

    **Integration:**
    - Task stored in PostgreSQL
    - Metadata stored in Memory MCP with WHO/WHEN/PROJECT/WHY tagging
    - Audit log created for compliance
    """,
    responses={
        201: {
            "description": "Task created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 123,
                        "skill_name": "pair-programming",
                        "schedule_cron": "0 9 * * 1-5",
                        "status": "pending"
                    }
                }
            }
        },
        400: {"description": "Invalid cron expression or parameters"},
        401: {"description": "Authentication required"},
        422: {"description": "Validation error"}
    }
)
async def create_task(...):
    """
    Create a new scheduled task with comprehensive validation and logging
    """
```

---

## 🔐 Authentication Setup

### JWT Bearer Authentication

Add security scheme to OpenAPI:

```python
# In app/main.py, add to FastAPI initialization:
from fastapi.security import HTTPBearer

security = HTTPBearer()

# Add to openapi schema
app.openapi_schema = {
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter your JWT token in the format: Bearer <token>"
            }
        }
    },
    "security": [{"BearerAuth": []}]
}
```

### Document in Endpoint

```python
@router.get("/tasks", dependencies=[Depends(security)])
async def list_tasks(...):
    """
    **Authentication**: Requires JWT Bearer token

    Example header:
    ```
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    """
```

---

## ⏱️ Rate Limiting Documentation

### Document Rate Limits

In `app/main.py` description:

```markdown
## 📊 Rate Limits

| Endpoint Type | Limit | Period |
|--------------|-------|--------|
| Standard API | 100 req | 1 min |
| Activity Logging | 1000 req | 1 min |
| Agent Creation | 60 req | 1 min |

**Headers**:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Remaining requests in window
- `X-RateLimit-Reset`: Unix timestamp when limit resets
```

### Document in Endpoint

```python
@router.post("/tasks")
@limiter.limit("100/minute")
async def create_task(...):
    """
    **Rate Limit**: 100 requests per minute per IP

    Response headers include:
    - `X-RateLimit-Limit: 100`
    - `X-RateLimit-Remaining: 95`
    - `X-RateLimit-Reset: 1699999999`
    """
```

---

## ❌ Error Code Documentation

### Document Error Responses

```python
@router.get(
    "/tasks/{task_id}",
    responses={
        200: {"description": "Task retrieved successfully"},
        401: {"description": "Authentication required"},
        403: {
            "description": "Forbidden - User does not own this resource",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to access this resource"
                    }
                }
            }
        },
        404: {
            "description": "Task not found or soft deleted",
            "content": {
                "application/json": {
                    "example": {"detail": "Task 123 not found"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Internal server error",
                        "error_id": "550e8400-e29b-41d4-a716-446655440000"
                    }
                }
            }
        }
    }
)
```

### Global Error Documentation

In `app/main.py` description:

```markdown
## 🔧 Error Codes

- **400 Bad Request**: Invalid input, malformed cron expression
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: User does not own the resource (BOLA protection)
- **404 Not Found**: Resource not found or soft deleted
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Unexpected error (includes X-Request-ID)
```

---

## 🎨 Swagger UI Customization

### Theme and Layout

```python
app = FastAPI(
    swagger_ui_parameters={
        # Syntax highlighting theme
        "syntaxHighlight.theme": "monokai",

        # Expand models by default
        "defaultModelsExpandDepth": 3,
        "defaultModelExpandDepth": 3,

        # Show request duration
        "displayRequestDuration": True,

        # Enable filtering
        "filter": True,

        # Remember authorization
        "persistAuthorization": True,

        # Custom CSS
        "customCss": ".swagger-ui .topbar { display: none }"
    }
)
```

### Custom Logo and Branding

Create custom Swagger UI template:

```python
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="RUV SPARC API Docs",
        swagger_favicon_url="/static/favicon.ico",
        swagger_ui_parameters={
            "syntaxHighlight.theme": "monokai"
        }
    )
```

---

## 📦 Static HTML Export

### Export Script

Location: `scripts/export_openapi_html.py`

```python
def export_html(output_dir: Path):
    """Export OpenAPI schema to static HTML"""

    # Fetch schema from running server or generate from app
    spec = fetch_openapi_schema()

    # Save raw JSON
    with open(output_dir / "openapi.json", "w") as f:
        json.dump(spec, f, indent=2)

    # Generate Swagger UI HTML
    swagger_html = SWAGGER_TEMPLATE.format(spec_json=json.dumps(spec))
    with open(output_dir / "swagger-ui.html", "w") as f:
        f.write(swagger_html)

    # Generate ReDoc HTML
    redoc_html = REDOC_TEMPLATE.format(spec_json=json.dumps(spec))
    with open(output_dir / "redoc.html", "w") as f:
        f.write(redoc_html)
```

### Usage

```bash
# Export static HTML documentation
python scripts/export_openapi_html.py

# Output: docs/api-static/
#   - openapi.json
#   - swagger-ui.html
#   - redoc.html
```

### Open in Browser

```bash
# Windows
start docs/api-static/swagger-ui.html

# macOS
open docs/api-static/swagger-ui.html

# Linux
xdg-open docs/api-static/swagger-ui.html
```

---

## 🚀 Testing Documentation

### Start Server

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Access Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

### Try API Calls

1. Click **Authorize** button
2. Enter JWT token: `Bearer <your-token>`
3. Try any endpoint with "Try it out"
4. Execute and view response

---

## 📚 Additional Resources

- **FastAPI OpenAPI**: https://fastapi.tiangolo.com/tutorial/metadata/
- **Pydantic Config**: https://docs.pydantic.dev/latest/usage/json_schema/
- **OpenAPI Specification**: https://spec.openapis.org/oas/v3.1.0
- **Swagger UI**: https://swagger.io/tools/swagger-ui/
- **ReDoc**: https://redocly.com/redoc/

---

**Last Updated**: 2025-11-08
**Version**: 1.0.0
