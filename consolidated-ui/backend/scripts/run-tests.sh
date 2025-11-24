#!/bin/bash
# Run Backend Testing Suite
# P2_T8 - Comprehensive Test Execution Script

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Backend Testing Suite - P2_T8${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Parse command line arguments
TEST_TYPE=${1:-all}
PARALLEL=${2:-false}

# Function to print colored status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Start test infrastructure
print_status "Starting test infrastructure (PostgreSQL + Redis)..."
docker-compose -f docker-compose.test.yml up -d

# Wait for services to be healthy
print_status "Waiting for services to be ready..."
sleep 5

# Check PostgreSQL
until docker-compose -f docker-compose.test.yml exec -T postgres-test pg_isready -U test > /dev/null 2>&1; do
    print_warning "Waiting for PostgreSQL..."
    sleep 2
done
print_success "PostgreSQL is ready"

# Check Redis
until docker-compose -f docker-compose.test.yml exec -T redis-test redis-cli ping > /dev/null 2>&1; do
    print_warning "Waiting for Redis..."
    sleep 2
done
print_success "Redis is ready"

# Load test environment
print_status "Loading test environment..."
export $(cat .env.test | xargs)

# Run tests based on type
case $TEST_TYPE in
    all)
        print_status "Running ALL tests with coverage..."
        if [ "$PARALLEL" = "true" ]; then
            pytest -n auto --cov=app --cov-report=html --cov-report=term-missing
        else
            pytest --cov=app --cov-report=html --cov-report=term-missing
        fi
        ;;

    unit)
        print_status "Running UNIT tests (mocked dependencies)..."
        pytest -m unit -v
        ;;

    integration)
        print_status "Running INTEGRATION tests (real database)..."
        pytest -m integration -v
        ;;

    websocket)
        print_status "Running WEBSOCKET tests..."
        pytest -m websocket -v
        ;;

    circuit-breaker)
        print_status "Running CIRCUIT BREAKER tests..."
        pytest -m circuit_breaker -v
        ;;

    performance)
        print_status "Running PERFORMANCE tests..."
        pytest -m performance -v
        ;;

    concurrent)
        print_status "Running CONCURRENT operation tests..."
        pytest -m concurrent -v
        ;;

    fast)
        print_status "Running FAST tests (unit + websocket)..."
        pytest -m "unit or websocket" -v
        ;;

    slow)
        print_status "Running SLOW tests (integration + performance)..."
        pytest -m "integration or performance or slow" -v
        ;;

    coverage)
        print_status "Generating coverage report..."
        pytest --cov=app --cov-report=html --cov-report=term-missing
        print_success "Coverage report generated at htmlcov/index.html"
        ;;

    *)
        print_error "Unknown test type: $TEST_TYPE"
        echo ""
        echo "Usage: ./run-tests.sh [TEST_TYPE] [parallel]"
        echo ""
        echo "TEST_TYPE options:"
        echo "  all             - Run all tests (default)"
        echo "  unit            - Run unit tests only"
        echo "  integration     - Run integration tests only"
        echo "  websocket       - Run WebSocket tests only"
        echo "  circuit-breaker - Run circuit breaker tests only"
        echo "  performance     - Run performance tests only"
        echo "  concurrent      - Run concurrent operation tests only"
        echo "  fast            - Run fast tests (unit + websocket)"
        echo "  slow            - Run slow tests (integration + performance)"
        echo "  coverage        - Generate coverage report"
        echo ""
        echo "Examples:"
        echo "  ./run-tests.sh                    # Run all tests"
        echo "  ./run-tests.sh unit               # Run unit tests"
        echo "  ./run-tests.sh all true           # Run all tests in parallel"
        exit 1
        ;;
esac

TEST_EXIT_CODE=$?

# Cleanup
if [ "$TEST_EXIT_CODE" -eq 0 ]; then
    print_success "All tests passed! ✅"

    # Display coverage summary if available
    if [ -f "htmlcov/index.html" ]; then
        echo ""
        print_status "Coverage report available at: htmlcov/index.html"
    fi
else
    print_error "Tests failed! ❌"
fi

# Optional: Stop test infrastructure
read -p "Stop test infrastructure? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Stopping test infrastructure..."
    docker-compose -f docker-compose.test.yml down
    print_success "Test infrastructure stopped"
fi

exit $TEST_EXIT_CODE
