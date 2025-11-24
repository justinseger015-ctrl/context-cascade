#!/bin/bash
# Deployment validation script for P1_T1
# Validates all success criteria

set -e

echo "🚀 Ruv-Sparc UI Dashboard - Deployment Validation"
echo "=================================================="
echo ""

# Track results
VALIDATION_RESULTS=()

# Function to check service health
check_service() {
    local service=$1
    echo "🔍 Checking $service..."

    if docker-compose ps | grep -q "$service.*Up.*healthy"; then
        echo "✅ $service: HEALTHY"
        VALIDATION_RESULTS+=("$service: PASS")
        return 0
    else
        echo "❌ $service: FAILED"
        VALIDATION_RESULTS+=("$service: FAIL")
        return 1
    fi
}

# 1. Check if services are running
echo "📋 Phase 1: Service Status Check"
echo "--------------------------------"
docker-compose ps

# 2. Health check for each service
echo ""
echo "📋 Phase 2: Health Checks"
echo "------------------------"
check_service "ruv-sparc-postgres"
check_service "ruv-sparc-redis"
check_service "ruv-sparc-backend"
check_service "ruv-sparc-frontend"

# 3. Verify FastAPI version
echo ""
echo "📋 Phase 3: FastAPI Version Verification (CVE-2024-47874)"
echo "---------------------------------------------------------"
FASTAPI_VERSION=$(docker-compose exec -T backend python -c "import fastapi; print(fastapi.__version__)" 2>/dev/null || echo "ERROR")

if [ "$FASTAPI_VERSION" != "ERROR" ]; then
    echo "✅ FastAPI version: $FASTAPI_VERSION"

    # Compare with minimum version 0.121.0
    MIN_VERSION="0.121.0"
    if [ "$(printf '%s\n' "$MIN_VERSION" "$FASTAPI_VERSION" | sort -V | head -n1)" = "$MIN_VERSION" ]; then
        echo "✅ CVE-2024-47874 (CVSS 8.7) is PATCHED"
        VALIDATION_RESULTS+=("CVE-2024-47874: PATCHED")
    else
        echo "❌ CVE-2024-47874 NOT patched (version < $MIN_VERSION)"
        VALIDATION_RESULTS+=("CVE-2024-47874: VULNERABLE")
    fi
else
    echo "❌ Failed to retrieve FastAPI version"
    VALIDATION_RESULTS+=("FastAPI version check: FAIL")
fi

# 4. Test database connectivity
echo ""
echo "📋 Phase 4: Database Connectivity"
echo "---------------------------------"
if docker-compose exec -T postgres pg_isready -U postgres &>/dev/null; then
    echo "✅ PostgreSQL: Connection successful"
    VALIDATION_RESULTS+=("PostgreSQL connectivity: PASS")
else
    echo "❌ PostgreSQL: Connection failed"
    VALIDATION_RESULTS+=("PostgreSQL connectivity: FAIL")
fi

# 5. Test Redis connectivity
echo ""
echo "📋 Phase 5: Redis Connectivity"
echo "------------------------------"
REDIS_PASSWORD=$(cat docker/secrets/redis_password.txt 2>/dev/null || echo "")
if [ -n "$REDIS_PASSWORD" ]; then
    if docker-compose exec -T redis redis-cli -a "$REDIS_PASSWORD" ping 2>/dev/null | grep -q "PONG"; then
        echo "✅ Redis: Connection successful"
        VALIDATION_RESULTS+=("Redis connectivity: PASS")
    else
        echo "❌ Redis: Connection failed"
        VALIDATION_RESULTS+=("Redis connectivity: FAIL")
    fi
else
    echo "⚠️  Redis password not found (secrets not initialized)"
    VALIDATION_RESULTS+=("Redis connectivity: SKIP")
fi

# 6. Test backend API
echo ""
echo "📋 Phase 6: Backend API Health"
echo "------------------------------"
BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null || echo "ERROR")
if echo "$BACKEND_HEALTH" | grep -q "healthy"; then
    echo "✅ Backend API: Responding"
    VALIDATION_RESULTS+=("Backend API: PASS")
else
    echo "❌ Backend API: Not responding"
    VALIDATION_RESULTS+=("Backend API: FAIL")
fi

# 7. Check Docker secrets
echo ""
echo "📋 Phase 7: Docker Secrets Validation"
echo "-------------------------------------"
SECRETS_COUNT=$(ls -1 docker/secrets/*.txt 2>/dev/null | wc -l)
if [ "$SECRETS_COUNT" -eq 4 ]; then
    echo "✅ All 4 Docker secrets present"
    VALIDATION_RESULTS+=("Docker secrets: PASS")
else
    echo "⚠️  Expected 4 secrets, found $SECRETS_COUNT"
    VALIDATION_RESULTS+=("Docker secrets: INCOMPLETE ($SECRETS_COUNT/4)")
fi

# 8. Summary
echo ""
echo "=================================================="
echo "📊 Validation Summary"
echo "=================================================="
for result in "${VALIDATION_RESULTS[@]}"; do
    echo "$result"
done

# Check if all critical tests passed
FAILURES=$(printf '%s\n' "${VALIDATION_RESULTS[@]}" | grep -c "FAIL" || true)
if [ "$FAILURES" -gt 0 ]; then
    echo ""
    echo "❌ VALIDATION FAILED: $FAILURES test(s) failed"
    exit 1
else
    echo ""
    echo "✅ ALL VALIDATIONS PASSED"
    echo "🎉 P1_T1 Docker Compose Infrastructure: COMPLETE"
fi
