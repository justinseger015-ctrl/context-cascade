#!/bin/bash
# Verify FastAPI version for CVE-2024-47874 mitigation
# CVSS 8.7 DoS vulnerability patched in 0.115.4+

set -e

MIN_VERSION="0.121.0"

echo "🔍 Verifying FastAPI version for CVE-2024-47874 mitigation..."

# Build backend image
docker-compose build backend

# Check FastAPI version in container
FASTAPI_VERSION=$(docker run --rm ruv-sparc-backend:latest python -c "import fastapi; print(fastapi.__version__)")

echo "📦 Installed FastAPI version: $FASTAPI_VERSION"
echo "✅ Required minimum version: $MIN_VERSION"

# Compare versions
if [ "$(printf '%s\n' "$MIN_VERSION" "$FASTAPI_VERSION" | sort -V | head -n1)" = "$MIN_VERSION" ]; then
    echo "✅ SUCCESS: FastAPI $FASTAPI_VERSION >= $MIN_VERSION"
    echo "✅ CVE-2024-47874 (CVSS 8.7 DoS) is PATCHED"
else
    echo "❌ CRITICAL: FastAPI $FASTAPI_VERSION < $MIN_VERSION"
    echo "🛑 CVE-2024-47874 vulnerability NOT patched!"
    exit 1
fi

# Display CVE details
echo ""
echo "📋 CVE-2024-47874 Details:"
echo "   Severity: HIGH (CVSS 8.7)"
echo "   Type: Denial of Service (DoS)"
echo "   Affected: FastAPI < 0.115.4"
echo "   Patched: FastAPI >= 0.115.4"
echo "   Current: FastAPI $FASTAPI_VERSION ✅"
