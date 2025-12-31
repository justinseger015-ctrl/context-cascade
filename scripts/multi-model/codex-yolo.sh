#!/bin/bash
# codex-yolo.sh - Fully autonomous Codex execution with YOLO/Full-Auto mode
# Uses: codex --yolo or codex --full-auto for unattended operation
# Part of Context Cascade Multi-Model Integration
#
# CRITICAL: Uses bash -lc to ensure login shell PATH is available
# This fixes the "command not found" issue in Claude Code tool context

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_ID="${2:-$(date +%s)-$(head -c 4 /dev/urandom 2>/dev/null | xxd -p || echo $$)}"
MAX_ITERATIONS="${4:-10}"
OUTPUT_DIR="$HOME/.claude/memory-mcp-data/multi-model/codex/yolo"

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

TASK="$1"
CONTEXT="${3:-.}"  # Default to current directory
MODE="${5:-full-auto}"  # yolo, full-auto, sandbox, zdr

usage() {
    cat <<'EOF'
Usage: codex-yolo.sh <task> [task_id] [context] [max_iterations] [mode]

Modes:
  full-auto - Autonomous mode with workspace write (default)
  yolo      - Auto-accept all actions, bypass sandbox
  sandbox   - Full isolation with network disabled
  zdr       - Zero Data Retention for sensitive code

Examples:
  codex-yolo.sh 'Build REST API with tests'
  codex-yolo.sh 'Fix all failing tests' task-123 tests/ 15 full-auto
  codex-yolo.sh 'Audit sensitive code' task-456 src/ 5 zdr

CRITICAL: This script uses login shell to ensure codex is on PATH.
EOF
    exit 1
}

if [ -z "$TASK" ]; then
    usage
fi

# ============================================================================
# PREFLIGHT: Verify codex exists (NEVER install)
# ============================================================================

echo "[codex-yolo] Running preflight check..."

# Use login shell to check for codex
if ! bash -lc "command -v codex >/dev/null 2>&1"; then
    echo "ERROR: codex not found on PATH in login shell context." >&2
    echo "DEBUG: PATH=$(bash -lc 'echo $PATH' | head -c 500)" >&2
    echo "" >&2
    echo "SOLUTION: Install codex manually: npm install -g @openai/codex" >&2
    echo "DO NOT let Claude install it - it's a PATH issue, not missing install." >&2
    exit 10
fi

CODEX_VERSION=$(bash -lc "codex --version" 2>&1 | head -1)
echo "[codex-yolo] Found codex: $CODEX_VERSION"

# ============================================================================
# BUILD COMMAND
# ============================================================================

echo "[codex-yolo] Starting task: $TASK_ID"
echo "[codex-yolo] Mode: $MODE"
echo "[codex-yolo] Context: $CONTEXT"
echo "[codex-yolo] Max iterations: $MAX_ITERATIONS"
echo "[codex-yolo] Task: $TASK"
echo ""

# Build command based on mode
case "$MODE" in
    "yolo")
        # YOLO mode - auto-accept everything, bypass sandbox
        CMD="codex --yolo exec"
        ;;
    "full-auto")
        # Full-auto mode - autonomous with workspace write
        CMD="codex --full-auto exec"
        ;;
    "sandbox")
        # Sandbox mode - full isolation
        CMD="codex --full-auto --sandbox true --network disabled exec"
        ;;
    "zdr")
        # Zero Data Retention - for sensitive/proprietary code
        CMD="codex --full-auto --zdr exec"
        ;;
    *)
        CMD="codex --full-auto exec"
        ;;
esac

# Escape the task for shell
ESCAPED_TASK=$(printf "%q" "$TASK")

# ============================================================================
# EXECUTE (via login shell)
# ============================================================================

echo "[codex-yolo] Executing via login shell: $CMD $ESCAPED_TASK"
echo "---"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Temp files for output
STDOUT_FILE="$OUTPUT_DIR/${TASK_ID}.stdout"
STDERR_FILE="$OUTPUT_DIR/${TASK_ID}.stderr"

# Run Codex via login shell to get correct PATH
set +e
bash -lc "cd \"$CONTEXT\" && $CMD $ESCAPED_TASK" >"$STDOUT_FILE" 2>"$STDERR_FILE"
EXIT_CODE=$?
set -e

RESULT=$(cat "$STDOUT_FILE" 2>/dev/null || echo "Execution completed")

# ============================================================================
# STORE RESULT TO MEMORY-MCP
# ============================================================================

MEMORY_KEY="multi-model/codex/yolo/$TASK_ID"

# Escape for JSON (using python if available, fallback to simple escape)
json_escape() {
    python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1" 2>/dev/null || \
    python -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1" 2>/dev/null || \
    echo "\"$(echo "$1" | sed 's/"/\\"/g' | tr '\n' ' ')\""
}

PAYLOAD=$(cat <<EOF
{
    "content": $(json_escape "$RESULT"),
    "exit_code": $EXIT_CODE,
    "metadata": {
        "WHO": "codex-cli:$MODE",
        "WHEN": "$(date -Iseconds)",
        "PROJECT": "context-cascade",
        "WHY": "yolo-execution",
        "MODE": "$MODE",
        "MAX_ITERATIONS": $MAX_ITERATIONS,
        "CONTEXT": "$CONTEXT",
        "TASK_ID": "$TASK_ID",
        "TASK": $(json_escape "$TASK"),
        "CODEX_VERSION": "$CODEX_VERSION"
    }
}
EOF
)

# Store to Memory-MCP data directory
echo "$PAYLOAD" > "$OUTPUT_DIR/$TASK_ID.json"

# ============================================================================
# OUTPUT
# ============================================================================

echo ""
echo "[codex-yolo] Exit code: $EXIT_CODE"
echo "[codex-yolo] Result stored at: $MEMORY_KEY"
echo "[codex-yolo] Stdout file: $STDOUT_FILE"
echo "[codex-yolo] Stderr file: $STDERR_FILE"
echo "---"

# Show first 100 lines of output
head -100 "$STDOUT_FILE" 2>/dev/null || true

# Show stderr if present
if [ -s "$STDERR_FILE" ]; then
    echo ""
    echo "--- STDERR ---"
    cat "$STDERR_FILE"
fi

exit $EXIT_CODE
