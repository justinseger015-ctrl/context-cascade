#!/bin/bash
# multi-model-router.sh - Intelligent routing of tasks to optimal model
# Routes tasks to Gemini, Codex, Council, or Claude based on keywords
# Part of Context Cascade Multi-Model Integration
#
# CRITICAL: Uses bash -lc to ensure login shell PATH is available

set -e

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_ID="${2:-$(date +%s)-$(head -c 4 /dev/urandom 2>/dev/null | xxd -p || echo $$)}"
OUTPUT_DIR="$HOME/.claude/memory-mcp-data/multi-model/router"

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

TASK="$1"
FORCE_MODEL="${3:-auto}"  # auto, gemini, codex, council, claude

usage() {
    cat <<'EOF'
Usage: multi-model-router.sh <task> [task_id] [force_model]

Automatic Routing (based on keywords):
  - Research keywords --> Gemini (search grounding)
  - Megacontext keywords --> Gemini --all-files (1M context)
  - Implementation keywords --> Codex (autonomous coding)
  - Decision keywords --> LLM Council (consensus)
  - Default --> Claude (complex reasoning)

Force Model:
  auto    - Automatic detection (default)
  gemini  - Force Gemini
  codex   - Force Codex
  council - Force LLM Council
  claude  - Force Claude (return task for Claude to handle)

Examples:
  multi-model-router.sh 'Find existing solutions for auth'
  multi-model-router.sh 'Fix all failing tests'
  multi-model-router.sh 'Should we use microservices?' task-123 council
  multi-model-router.sh 'Map entire architecture' task-456 gemini

Keyword Detection:
  GEMINI (Research):
    - "search", "latest", "documentation", "best practices"
    - "how do others", "find existing", "examples"

  GEMINI (Megacontext):
    - "entire codebase", "all files", "architecture overview"
    - "full analysis", "codebase map"

  CODEX (Implementation):
    - "fix", "implement", "build", "create", "refactor"
    - "debug", "test", "prototype", "iterate"

  COUNCIL (Decision):
    - "decide", "choose", "which approach", "should we"
    - "architecture decision", "technology selection"

EOF
    exit 1
}

if [ -z "$TASK" ]; then
    usage
fi

# ============================================================================
# KEYWORD DETECTION
# ============================================================================

detect_model() {
    local task="$1"
    local task_lower=$(echo "$task" | tr '[:upper:]' '[:lower:]')

    # GEMINI: Megacontext keywords (1M token codebase analysis)
    if echo "$task_lower" | grep -qE '(entire codebase|all files|architecture overview|full analysis|codebase map|analyze.*codebase|map.*architecture|onboard|understand.*codebase)'; then
        echo "gemini-megacontext"
        return
    fi

    # GEMINI: Research keywords (Google Search grounding)
    if echo "$task_lower" | grep -qE '(search|latest|documentation|best practices|how do others|find existing|examples|current|what are|research|look up|find out)'; then
        echo "gemini-research"
        return
    fi

    # COUNCIL: Decision keywords (multi-model consensus)
    if echo "$task_lower" | grep -qE '(decide|choose|which approach|should we|architecture decision|technology selection|critical decision|consensus|compare options|trade.?offs)'; then
        echo "council"
        return
    fi

    # CODEX: Implementation keywords (autonomous coding)
    if echo "$task_lower" | grep -qE '(fix|implement|build|create|refactor|debug|test|prototype|iterate|write code|add feature|update|modify|change|edit|delete|remove|rename)'; then
        echo "codex"
        return
    fi

    # Default to Claude for complex reasoning
    echo "claude"
}

# ============================================================================
# ROUTING LOGIC
# ============================================================================

echo "[router] Starting task: $TASK_ID"
echo "[router] Task: $TASK"
echo "[router] Force model: $FORCE_MODEL"
echo ""

# Determine target model
if [ "$FORCE_MODEL" = "auto" ]; then
    TARGET=$(detect_model "$TASK")
    echo "[router] Auto-detected model: $TARGET"
else
    TARGET="$FORCE_MODEL"
    echo "[router] Forced model: $TARGET"
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# ============================================================================
# EXECUTE BASED ON TARGET
# ============================================================================

echo "[router] Routing to: $TARGET"
echo "---"

case "$TARGET" in
    "gemini-research")
        # Route to Gemini for research
        echo "[router] Executing: gemini-yolo.sh (research mode)"
        "$SCRIPT_DIR/gemini-yolo.sh" "$TASK" "$TASK_ID" "research"
        EXIT_CODE=$?
        ;;

    "gemini-megacontext")
        # Route to Gemini for megacontext analysis
        echo "[router] Executing: gemini-yolo.sh (megacontext mode)"
        "$SCRIPT_DIR/gemini-yolo.sh" "$TASK" "$TASK_ID" "megacontext"
        EXIT_CODE=$?
        ;;

    "gemini")
        # Generic gemini (default to research)
        echo "[router] Executing: gemini-yolo.sh (research mode)"
        "$SCRIPT_DIR/gemini-yolo.sh" "$TASK" "$TASK_ID" "research"
        EXIT_CODE=$?
        ;;

    "codex")
        # Route to Codex for implementation
        echo "[router] Executing: codex-yolo.sh (full-auto mode)"
        "$SCRIPT_DIR/codex-yolo.sh" "$TASK" "$TASK_ID" "." "10" "full-auto"
        EXIT_CODE=$?
        ;;

    "council")
        # Route to LLM Council for decisions
        echo "[router] Executing: llm-council.sh"
        "$SCRIPT_DIR/llm-council.sh" "$TASK" "0.75" "claude"
        EXIT_CODE=$?
        ;;

    "claude")
        # Return to Claude for handling
        echo "[router] Task routed to Claude for complex reasoning"
        echo ""
        echo "ROUTE_TARGET=claude"
        echo "ROUTE_REASON=Complex reasoning task, best handled by Claude"
        echo "ROUTE_TASK=$TASK"
        EXIT_CODE=0
        ;;

    *)
        echo "ERROR: Unknown target model: $TARGET" >&2
        exit 1
        ;;
esac

# ============================================================================
# STORE ROUTING DECISION
# ============================================================================

ROUTING_LOG="$OUTPUT_DIR/${TASK_ID}.routing.json"

cat > "$ROUTING_LOG" <<EOF
{
    "task_id": "$TASK_ID",
    "task": $(python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$TASK" 2>/dev/null || echo "\"$TASK\""),
    "detected_model": "$(detect_model "$TASK")",
    "force_model": "$FORCE_MODEL",
    "actual_target": "$TARGET",
    "exit_code": $EXIT_CODE,
    "timestamp": "$(date -Iseconds)",
    "metadata": {
        "WHO": "multi-model-router",
        "WHY": "intelligent-routing"
    }
}
EOF

echo ""
echo "[router] Routing decision logged: $ROUTING_LOG"
echo "[router] Exit code: $EXIT_CODE"

exit $EXIT_CODE
