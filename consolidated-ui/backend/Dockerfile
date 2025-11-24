# Multi-stage build for FastAPI backend with CVE-2024-47874 mitigation
FROM python:3.11-slim AS builder

# Security: Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies with specific FastAPI version for CVE mitigation
ARG FASTAPI_VERSION=0.121.0
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "fastapi>=${FASTAPI_VERSION}" "uvicorn[standard]>=0.30.0"

# Verify FastAPI version
RUN python -c "import fastapi; assert fastapi.__version__ >= '${FASTAPI_VERSION}', f'FastAPI {fastapi.__version__} < ${FASTAPI_VERSION}'"

# Production stage
FROM python:3.11-slim

# Security: Run as non-root user
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser ./app /app/app

# Create directories for logs and secrets
RUN mkdir -p /app/logs && \
    chown -R appuser:appuser /app/logs && \
    chmod 750 /app/logs

# Switch to non-root user
USER appuser

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run with Gunicorn + Uvicorn workers
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--access-logfile", "/app/logs/access.log", \
     "--error-logfile", "/app/logs/error.log", \
     "--log-level", "info"]
