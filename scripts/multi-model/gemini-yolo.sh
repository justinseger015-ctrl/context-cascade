#!/bin/bash
# gemini-yolo.sh - Autonomous Gemini execution for research and analysis
# Uses: gemini with various modes for discovery, research, and codebase analysis
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
OUTPUT_DIR="$HOME/.claude/memory-mcp-data/multi-model/gemini/yolo"

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

TASK="$1"
MODE="${3:-research}"  # research, megacontext, yolo, sandbox

usage() {
    cat <<'EOF'
Usage: gemini-yolo.sh <task> [task_id] [mode]

Modes:
  research    - Standard research with Google Search grounding (default)
  megacontext - Load entire codebase with 1M token context (--all-files)
  yolo        - Auto-accept all actions
  sandbox     - Run in sandbox mode

Examples:
  gemini-yolo.sh 'What are React 19 best practices?'
  gemini-yolo.sh 'Find existing solutions for auth' task-123 research
  gemini-yolo.sh 'Map entire architecture' task-456 megacontext
  gemini-yolo.sh 'Analyze codebase for patterns' task-789 megacontext

Unique Gemini Capabilities:
  - Google Search grounding for current information
  - 1M token context (--all-files) for full codebase analysis
  - @ commands for file injection (@README.md, @src/)
  - Custom slash commands via .gemini/commands/*.toml

CRITICAL: This script uses login shell to ensure gemini is on PATH.
EOF
    exit 1
}

if [ -z "$TASK" ]; then
    usage
fi

# ============================================================================
# PREFLIGHT: Verify gemini exists (NEVER install)
# ============================================================================

echo "[gemini-yolo] Running preflight check..."

# Use login shell to check for gemini
if ! bash -lc "command -v gemini >/dev/null 2>&1"; then
    echo "ERROR: gemini not found on PATH in login shell context." >&2
    echo "DEBUG: PATH=$(bash -lc 'echo $PATH' | head -c 500)" >&2
    echo "" >&2
    echo "SOLUTION: Install gemini manually: npm install -g @google/gemini-cli" >&2
    echo "DO NOT let Claude install it - it's a PATH issue, not missing install." >&2
    exit 10
fi

GEMINI_VERSION=$(bash -lc "gemini --version" 2>&1 | head -1)
echo "[gemini-yolo] Found gemini: $GEMINI_VERSION"

# ============================================================================
# BUILD COMMAND
# ============================================================================

echo "[gemini-yolo] Starting task: $TASK_ID"
echo "[gemini-yolo] Mode: $MODE"
echo "[gemini-yolo] Task: $TASK"
echo ""

# Build command based on mode
case "$MODE" in
    "research")
        # Standard research mode - uses Google Search grounding
        CMD="gemini"
        ;;
    "megacontext")
        # Megacontext mode - load entire codebase (1M tokens)
        CMD="gemini --all-files"
        ;;
    "yolo")
        # YOLO mode - auto-accept all actions
        CMD="gemini --yolo"
        ;;
    "sandbox")
        # Sandbox mode - isolated execution
        CMD="gemini -s"
        ;;
    *)
        CMD="gemini"
        ;;
esac

# Escape the task for shell
ESCAPED_TASK=$(printf "%q" "$TASK")

# ============================================================================
# EXECUTE (via login shell)
# ============================================================================

echo "[gemini-yolo] Executing via login shell: echo $ESCAPED_TASK | $CMD"
echo "---"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Temp files for output
STDOUT_FILE="$OUTPUT_DIR/${TASK_ID}.stdout"
STDERR_FILE="$OUTPUT_DIR/${TASK_ID}.stderr"

# Run Gemini via login shell to get correct PATH
# Using echo to pipe the prompt for non-interactive mode
set +e
bash -lc "echo $ESCAPED_TASK | $CMD" >"$STDOUT_FILE" 2>"$STDERR_FILE"
EXIT_CODE=$?
set -e

RESULT=$(cat "$STDOUT_FILE" 2>/dev/null || echo "Execution completed")

# ============================================================================
# STORE RESULT TO MEMORY-MCP
# ============================================================================

MEMORY_KEY="multi-model/gemini/yolo/$TASK_ID"

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
        "WHO": "gemini-cli:$MODE",
        "WHEN": "$(date -Iseconds)",
        "PROJECT": "context-cascade",
        "WHY": "discovery-execution",
        "MODE": "$MODE",
        "TASK_ID": "$TASK_ID",
        "TASK": $(json_escape "$TASK"),
        "GEMINI_VERSION": "$GEMINI_VERSION"
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
echo "[gemini-yolo] Exit code: $EXIT_CODE"
echo "[gemini-yolo] Result stored at: $MEMORY_KEY"
echo "[gemini-yolo] Stdout file: $STDOUT_FILE"
echo "[gemini-yolo] Stderr file: $STDERR_FILE"
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
