#!/bin/bash
# model-router-pretool.sh - Automatic model routing based on task characteristics
# Integrates: Gemini (megacontext, search, media, extensions) + Codex (yolo, sandbox, audit)
# Part of Context Cascade Multi-Model Integration

# =============================================================================
# MODEL CAPABILITY MATRIX (from research)
# =============================================================================
# GEMINI STRENGTHS:
#   - 1M token context (5x Claude) -> megacontext analysis
#   - Google Search grounding -> real-time info
#   - Imagen/Veo -> image/video generation
#   - 70+ extensions -> Figma, Stripe, Postman, Shopify
#   - --yolo mode -> semi-autonomous
#
# CODEX STRENGTHS:
#   - --full-auto/--yolo -> fully autonomous execution
#   - Sandbox isolation -> safe experimentation
#   - Test-fix-retest loops -> automatic bug fixing
#   - GPT-5-Codex -> different reasoning patterns
#   - --zdr -> zero data retention for sensitive code
# =============================================================================

TOOL_NAME="$1"
TOOL_INPUT="$2"

# State file for tracking routing decisions
STATE_FILE="$HOME/.claude/runtime/model-routing-state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# =============================================================================
# ROUTING LOGIC
# =============================================================================

detect_task_type() {
    local input="$1"
    local input_lower=$(echo "$input" | tr '[:upper:]' '[:lower:]')

    # GEMINI MEGACONTEXT triggers (1M token analysis)
    if echo "$input_lower" | grep -qE "entire codebase|full project|all files|architecture overview|whole system|30k|large codebase|complete analysis"; then
        echo "gemini-megacontext"
        return
    fi

    # GEMINI SEARCH triggers (real-time web info)
    if echo "$input_lower" | grep -qE "latest|current|2025|search|find online|real-time|breaking changes|cve|vulnerability|documentation|best practices"; then
        echo "gemini-search"
        return
    fi

    # GEMINI MEDIA triggers (image/video generation)
    if echo "$input_lower" | grep -qE "generate image|create diagram|flowchart|mockup|wireframe|architecture diagram|video|visualization|imagen|veo"; then
        echo "gemini-media"
        return
    fi

    # GEMINI EXTENSIONS triggers (third-party integrations)
    if echo "$input_lower" | grep -qE "figma|stripe|postman|shopify|dynatrace|elastic|snyk|harness|extension"; then
        echo "gemini-extensions"
        return
    fi

    # CODEX YOLO/FULL-AUTO triggers (autonomous execution)
    if echo "$input_lower" | grep -qE "autonomous|overnight|unattended|full auto|yolo|fire and forget|weekend|batch"; then
        echo "codex-yolo"
        return
    fi

    # CODEX SANDBOX triggers (isolated execution)
    if echo "$input_lower" | grep -qE "sandbox|isolated|safe|experimental|risky|untrusted|prototype quickly"; then
        echo "codex-sandbox"
        return
    fi

    # CODEX AUDIT triggers (test-fix loops)
    if echo "$input_lower" | grep -qE "fix all tests|debug|audit|test failures|auto-fix|iterate until"; then
        echo "codex-audit"
        return
    fi

    # CODEX REASONING triggers (second opinion)
    if echo "$input_lower" | grep -qE "alternative approach|second opinion|different perspective|gpt-5|codex reasoning"; then
        echo "codex-reasoning"
        return
    fi

    # LLM COUNCIL triggers (consensus needed)
    if echo "$input_lower" | grep -qE "consensus|critical decision|high stakes|multiple perspectives|council|vote"; then
        echo "llm-council"
        return
    fi

    # Default: Claude (complex reasoning, multi-step)
    echo "claude"
}

get_routing_command() {
    local task_type="$1"
    local query="$2"

    case "$task_type" in
        "gemini-megacontext")
            echo "gemini --all-files \"$query\""
            ;;
        "gemini-search")
            echo "gemini \"@search $query\""
            ;;
        "gemini-media")
            echo "gemini \"Generate: $query\""
            ;;
        "gemini-extensions")
            echo "gemini -e auto \"$query\""
            ;;
        "gemini-yolo")
            echo "gemini --yolo \"$query\""
            ;;
        "codex-yolo")
            echo "codex --yolo \"$query\""
            ;;
        "codex-sandbox")
            echo "codex --full-auto --sandbox true \"$query\""
            ;;
        "codex-audit")
            echo "codex --full-auto --max-iterations 10 \"$query\""
            ;;
        "codex-reasoning")
            echo "codex \"$query\""
            ;;
        "llm-council")
            echo "bash scripts/multi-model/llm-council.sh \"$query\""
            ;;
        *)
            echo "claude"
            ;;
    esac
}

# =============================================================================
# HOOK EXECUTION
# =============================================================================

# Only process Task tool calls
if [ "$TOOL_NAME" != "Task" ]; then
    exit 0
fi

# Extract task description from input
TASK_DESC=$(echo "$TOOL_INPUT" | jq -r '.prompt // .description // empty' 2>/dev/null)

if [ -z "$TASK_DESC" ]; then
    exit 0
fi

# Detect optimal model
TASK_TYPE=$(detect_task_type "$TASK_DESC")

# If not Claude, suggest routing
if [ "$TASK_TYPE" != "claude" ]; then
    ROUTING_CMD=$(get_routing_command "$TASK_TYPE" "$TASK_DESC")

    # Log routing decision
    echo "{
        \"timestamp\": \"$(date -Iseconds)\",
        \"task_type\": \"$TASK_TYPE\",
        \"routing_command\": \"$ROUTING_CMD\",
        \"original_task\": $(echo "$TASK_DESC" | jq -Rs .)
    }" >> "$STATE_FILE"

    # Output suggestion (displayed to user)
    cat << EOF

================================================================================
!! MULTI-MODEL ROUTING SUGGESTION !!
================================================================================

Detected task type: $TASK_TYPE

This task may benefit from external model routing:

  $ROUTING_CMD

Rationale:
EOF

    case "$TASK_TYPE" in
        "gemini-megacontext")
            echo "  - Task requires analyzing large codebase (Gemini has 1M token context)"
            ;;
        "gemini-search")
            echo "  - Task needs real-time web information (Gemini has Google Search grounding)"
            ;;
        "gemini-media")
            echo "  - Task requires image/video generation (Gemini has Imagen/Veo)"
            ;;
        "gemini-extensions")
            echo "  - Task involves third-party integration (Gemini has 70+ extensions)"
            ;;
        "codex-yolo")
            echo "  - Task can run autonomously overnight (Codex --yolo mode)"
            ;;
        "codex-sandbox")
            echo "  - Task needs isolated execution (Codex sandbox with network disabled)"
            ;;
        "codex-audit")
            echo "  - Task involves test-fix-retest loops (Codex auto-iteration)"
            ;;
        "codex-reasoning")
            echo "  - Task benefits from alternative perspective (GPT-5-Codex reasoning)"
            ;;
        "llm-council")
            echo "  - Critical decision benefits from multi-model consensus"
            ;;
    esac

    echo "
================================================================================
Proceeding with Claude agent (override with suggested command if preferred)
================================================================================
"
fi

# Always allow Claude to proceed (suggestion only)
exit 0
