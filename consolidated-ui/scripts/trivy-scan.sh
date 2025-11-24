#!/bin/bash
# Trivy security scanning for Docker images
# Ensures zero CRITICAL CVEs as per Loop 1 requirements

set -e

SCAN_RESULTS_DIR="./docker/trivy-reports"
mkdir -p "$SCAN_RESULTS_DIR"

echo "🔍 Starting Trivy security scan..."

# Check if Trivy is installed
if ! command -v trivy &> /dev/null; then
    echo "❌ Trivy not found. Installing..."
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
fi

# Update Trivy database
echo "📥 Updating Trivy vulnerability database..."
trivy image --download-db-only

# Scan backend image
echo "🔍 Scanning backend image..."
trivy image \
    --severity CRITICAL,HIGH \
    --format json \
    --output "$SCAN_RESULTS_DIR/backend-scan.json" \
    ruv-sparc-backend:latest

trivy image \
    --severity CRITICAL,HIGH \
    --format table \
    ruv-sparc-backend:latest | tee "$SCAN_RESULTS_DIR/backend-scan.txt"

# Scan frontend image
echo "🔍 Scanning frontend image..."
trivy image \
    --severity CRITICAL,HIGH \
    --format json \
    --output "$SCAN_RESULTS_DIR/frontend-scan.json" \
    ruv-sparc-frontend:latest

trivy image \
    --severity CRITICAL,HIGH \
    --format table \
    ruv-sparc-frontend:latest | tee "$SCAN_RESULTS_DIR/frontend-scan.txt"

# Scan PostgreSQL image
echo "🔍 Scanning PostgreSQL image..."
trivy image \
    --severity CRITICAL,HIGH \
    --format json \
    --output "$SCAN_RESULTS_DIR/postgres-scan.json" \
    postgres:15-alpine

trivy image \
    --severity CRITICAL,HIGH \
    --format table \
    postgres:15-alpine | tee "$SCAN_RESULTS_DIR/postgres-scan.txt"

# Scan Redis image
echo "🔍 Scanning Redis image..."
trivy image \
    --severity CRITICAL,HIGH \
    --format json \
    --output "$SCAN_RESULTS_DIR/redis-scan.json" \
    redis:7-alpine

trivy image \
    --severity CRITICAL,HIGH \
    --format table \
    redis:7-alpine | tee "$SCAN_RESULTS_DIR/redis-scan.txt"

# Check for CRITICAL vulnerabilities
echo "📊 Analyzing scan results..."
CRITICAL_COUNT=$(jq '[.Results[].Vulnerabilities[]? | select(.Severity=="CRITICAL")] | length' "$SCAN_RESULTS_DIR"/*.json | awk '{s+=$1} END {print s}')

if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "❌ CRITICAL: Found $CRITICAL_COUNT critical vulnerabilities!"
    echo "🛑 Build FAILED - Must resolve CRITICAL CVEs before deployment"
    exit 1
else
    echo "✅ SUCCESS: Zero CRITICAL vulnerabilities found"
fi

echo "📄 Scan reports saved to $SCAN_RESULTS_DIR"
