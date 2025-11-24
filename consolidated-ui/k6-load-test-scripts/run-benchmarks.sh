#!/bin/bash
#
# k6 Performance Benchmark Runner
# Executes all load tests and generates reports
#

set -e

echo "======================================"
echo "k6 Performance Benchmark Suite"
echo "======================================"

# Configuration
API_URL="${API_URL:-http://localhost:8000}"
WS_URL="${WS_URL:-ws://localhost:8000/ws}"
OUTPUT_DIR="./benchmark-results"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to run k6 test with JSON output
run_k6_test() {
  local test_file=$1
  local test_name=$2
  local json_output="${OUTPUT_DIR}/${test_name}-$(date +%Y%m%d-%H%M%S).json"
  local html_output="${OUTPUT_DIR}/${test_name}-$(date +%Y%m%d-%H%M%S).html"

  echo ""
  echo "Running: $test_name"
  echo "Output: $json_output"

  k6 run \
    --out json="$json_output" \
    --summary-export="$html_output" \
    "$test_file"

  echo "✅ $test_name completed"
}

# Check if k6 is installed
if ! command -v k6 &> /dev/null; then
  echo "❌ k6 is not installed"
  echo "Install k6: https://k6.io/docs/get-started/installation/"
  exit 1
fi

# Check if API is running
if ! curl -s "$API_URL/api/v1/health" > /dev/null 2>&1; then
  echo "⚠️  Warning: API at $API_URL is not responding"
  echo "Make sure the backend is running before benchmarking"
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi

# Run API benchmarks
echo ""
echo "1️⃣  API Performance Benchmarks"
run_k6_test "api-benchmark.js" "api-benchmark"

# Run WebSocket benchmarks
echo ""
echo "2️⃣  WebSocket Performance Benchmarks"
run_k6_test "websocket-benchmark.js" "websocket-benchmark"

# Generate summary report
echo ""
echo "======================================"
echo "Benchmark Results Summary"
echo "======================================"
echo "Results saved to: $OUTPUT_DIR"
echo ""
echo "To view detailed results:"
echo "  - JSON reports: $OUTPUT_DIR/*.json"
echo "  - HTML summaries: $OUTPUT_DIR/*.html"
echo ""
echo "To analyze with Grafana k6 Cloud (optional):"
echo "  k6 cloud run api-benchmark.js"
echo ""
echo "✅ All benchmarks completed successfully"
echo "======================================"
