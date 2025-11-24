#!/bin/bash
#
# Cron job for schedule_config.yml ↔ PostgreSQL sync.
#
# Runs every 5 minutes as safety net to ensure YAML and DB stay in sync.
# Detects conflicts and logs them for manual resolution.
#
# Installation:
#   chmod +x sync_cron_job.sh
#   crontab -e
#   Add: */5 * * * * /path/to/sync_cron_job.sh >> /var/log/yaml_sync.log 2>&1
#
# Monitoring:
#   tail -f /var/log/yaml_sync.log

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"
YAML_PATH="${BACKEND_DIR}/config/schedule_config.yml"
LOG_FILE="${BACKEND_DIR}/logs/yaml_sync.log"
LOCK_FILE="/tmp/yaml_sync.lock"
PYTHON_BIN="${BACKEND_DIR}/../venv/bin/python"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Timestamp function
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

log() {
    echo "[$(timestamp)] $*" | tee -a "$LOG_FILE"
}

# Check if another sync is running
if [ -f "$LOCK_FILE" ]; then
    LOCK_PID=$(cat "$LOCK_FILE")
    if ps -p "$LOCK_PID" > /dev/null 2>&1; then
        log "⚠️  Another sync job is running (PID: $LOCK_PID). Skipping."
        exit 0
    else
        log "🧹 Removing stale lock file"
        rm -f "$LOCK_FILE"
    fi
fi

# Create lock file
echo $$ > "$LOCK_FILE"

# Cleanup function
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

log "🔄 Starting scheduled YAML ↔ DB sync"

# Run sync Python script
SYNC_RESULT=$(cat <<EOF | $PYTHON_BIN
import sys
import asyncio
sys.path.insert(0, "${BACKEND_DIR}")

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sync.yaml_db_sync import SyncEngine
from app.config.settings import DATABASE_URL

async def run_sync():
    # Create async database engine
    engine = create_async_engine(DATABASE_URL, echo=False)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        sync_engine = SyncEngine(session, yaml_path="${YAML_PATH}")

        # Sync YAML → DB
        conflicts = await sync_engine.sync_yaml_to_db()

        if conflicts:
            print(f"CONFLICTS:{len(conflicts)}")
            for conflict in conflicts:
                print(f"  - Task {conflict.task_id}: {conflict.conflict_reason}")
        else:
            print("SUCCESS:0")

        await session.commit()

    await engine.dispose()

# Run async sync
asyncio.run(run_sync())
EOF
)

# Parse result
if [[ "$SYNC_RESULT" == SUCCESS:* ]]; then
    log "✅ Sync completed successfully"
elif [[ "$SYNC_RESULT" == CONFLICTS:* ]]; then
    CONFLICT_COUNT=$(echo "$SYNC_RESULT" | grep -oP 'CONFLICTS:\K\d+')
    log "⚠️  Sync detected $CONFLICT_COUNT conflict(s)"
    log "$SYNC_RESULT"
    log "👉 Resolve conflicts via API: POST /api/sync/conflicts/{conflict_id}/resolve"
else
    log "❌ Sync failed with unexpected output:"
    log "$SYNC_RESULT"
    exit 1
fi

log "✅ Scheduled sync completed"
