#!/bin/bash
echo "=== LOOP 3: COMPREHENSIVE ENDPOINT TESTING ==="
echo ""

# Test each endpoint with various scenarios
BASE_URL="http://localhost:8000"

echo "[1/6] Health Check - Comprehensive"
curl -s "$BASE_URL/health" | python -m json.tool
curl -s "$BASE_URL/" | python -m json.tool
echo ""

echo "[2/6] Registry Agents - Multiple Scenarios"
echo "  - Fetch 1 agent:"
curl -s "$BASE_URL/api/v1/registry/agents?limit=1" | python -m json.tool | head -20
echo "  - Fetch with role filter (developer):"
curl -s "$BASE_URL/api/v1/registry/agents?role=developer&limit=1" | python -m json.tool | head -15
echo ""

echo "[3/6] Agent Activity - Multiple Queries"
echo "  - Recent activity (24h):"
curl -s "$BASE_URL/api/v1/agent-activity?hours=24&limit=5"
echo "  - Specific agent (if exists):"
curl -s "$BASE_URL/api/v1/agent-activity?limit=1"
echo ""

echo "[4/6] Events - Multiple Queries"
echo "  - Recent events:"
curl -s "$BASE_URL/api/v1/events/?limit=5"
echo "  - With pagination:"
curl -s "$BASE_URL/api/v1/events/?limit=2&offset=0"
echo ""

echo "[5/6] Quality Metrics - Time Ranges"
echo "  - 7 days:"
curl -s "$BASE_URL/api/v1/metrics/quality/?days=7" | python -m json.tool
echo "  - 30 days:"
curl -s "$BASE_URL/api/v1/metrics/quality/?days=30" | python -m json.tool
echo ""

echo "[6/6] Resource Usage - Time Ranges"
echo "  - 7 days:"
curl -s "$BASE_URL/api/v1/metrics/resources/usage/?days=7" | python -m json.tool
echo "  - 90 days:"
curl -s "$BASE_URL/api/v1/metrics/resources/usage/?days=90" | python -m json.tool
echo ""

echo "=== COMPREHENSIVE TESTING COMPLETE ==="
