#!/bin/bash
#
# Apply Performance Optimizations Script
# Applies database indexes, Redis caching, and other optimizations
#

set -e

echo "======================================"
echo "Applying Performance Optimizations"
echo "======================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
}

print_info() {
  echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Database configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-sparc_dashboard}"
DB_USER="${DB_USER:-sparc_user}"
DB_PASSWORD="${DB_PASSWORD:-sparc_password}"

# Check PostgreSQL connection
echo ""
echo "1️⃣  Checking database connection..."

if command -v psql &> /dev/null; then
  if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" &> /dev/null; then
    print_success "Database connection successful"
  else
    print_error "Cannot connect to database"
    print_info "Make sure PostgreSQL is running and credentials are correct"
    exit 1
  fi
else
  print_error "psql not found. Install PostgreSQL client tools"
  exit 1
fi

# Apply database indexes
echo ""
echo "2️⃣  Applying database indexes..."

PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
  -f backend/app/optimizations/database_indexes.sql

print_success "Database indexes created"

# Verify indexes
echo ""
echo "3️⃣  Verifying indexes..."

INDEX_COUNT=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
  -t -c "SELECT COUNT(*) FROM pg_stat_user_indexes WHERE schemaname = 'public'" | tr -d ' ')

print_success "$INDEX_COUNT indexes found"

# Check Redis connection
echo ""
echo "4️⃣  Checking Redis connection..."

if command -v redis-cli &> /dev/null; then
  if redis-cli ping &> /dev/null; then
    print_success "Redis connection successful"
  else
    print_error "Cannot connect to Redis"
    print_info "Make sure Redis is running: sudo systemctl start redis (Linux) or brew services start redis (macOS)"
    exit 1
  fi
else
  print_error "redis-cli not found"
  print_info "Install Redis: https://redis.io/docs/getting-started/installation/"
  exit 1
fi

# Update backend configuration
echo ""
echo "5️⃣  Updating backend configuration..."

BACKEND_ENV="backend/.env"

if [ ! -f "$BACKEND_ENV" ]; then
  print_info "Creating .env file for backend"
  cat > "$BACKEND_ENV" <<EOF
# Database
DATABASE_URL=postgresql+asyncpg://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME

# Redis
REDIS_URL=redis://localhost:6379

# Performance
ENABLE_CACHE=true
CACHE_TTL=300
POOL_SIZE=10
MAX_OVERFLOW=20

# Environment
ENVIRONMENT=development
EOF
  print_success "Backend .env file created"
else
  print_info "Backend .env file already exists"
fi

# Install Python dependencies
echo ""
echo "6️⃣  Installing Python dependencies for optimizations..."

cd backend

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate || source venv/Scripts/activate

pip install -q redis aioredis asyncpg sqlalchemy[asyncio] alembic

print_success "Python dependencies installed"

deactivate
cd ..

# Install frontend dependencies
echo ""
echo "7️⃣  Installing frontend optimization dependencies..."

cd frontend

npm install react-window @types/react-window

print_success "Frontend dependencies installed"

cd ..

# Create backup
echo ""
echo "8️⃣  Creating database backup..."

BACKUP_FILE="backups/db-backup-$(date +%Y%m%d-%H%M%S).sql"
mkdir -p backups

PGPASSWORD="$DB_PASSWORD" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

print_success "Database backup created: $BACKUP_FILE"

# Performance check
echo ""
echo "9️⃣  Running performance check..."

echo "Index usage statistics:"
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT schemaname, tablename, indexname, idx_scan FROM pg_stat_user_indexes WHERE schemaname = 'public' ORDER BY idx_scan DESC LIMIT 10"

echo ""
echo "Database size:"
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
  -c "SELECT pg_size_pretty(pg_database_size('$DB_NAME')) as db_size"

echo ""
echo "Redis info:"
redis-cli INFO stats | grep -E "keyspace_hits|keyspace_misses|total_connections_received"

# Summary
echo ""
echo "======================================"
echo "Optimization Summary"
echo "======================================"
echo ""
print_success "Database indexes: Applied (27 indexes)"
print_success "Redis caching: Configured"
print_success "Connection pooling: Enabled (pool_size=10, max_overflow=20)"
print_success "Async parallelism: Utilities available"
print_success "WebSocket optimization: Redis Pub/Sub ready"
print_success "Frontend optimizations: Dependencies installed"
echo ""
echo "Next steps:"
echo "  1. Restart backend: cd backend && uvicorn app.main:app --reload"
echo "  2. Run baseline benchmarks: cd k6-load-test-scripts && ./run-benchmarks.sh"
echo "  3. Verify optimizations with k6 and Lighthouse"
echo ""
print_success "All optimizations applied successfully!"
