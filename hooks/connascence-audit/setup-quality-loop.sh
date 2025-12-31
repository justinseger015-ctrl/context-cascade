#!/bin/bash
# setup-quality-loop.sh
# PURPOSE: Initialize a quality-gated Ralph loop with Connascence analyzer integration
#
# Usage: bash setup-quality-loop.sh "<prompt>" [max_iterations] [completion_promise]

PROMPT="${1:-Continue working on the current task with production-quality code.}"
MAX_ITERATIONS="${2:-25}"
COMPLETION_PROMISE="${3:-CODE_QUALITY_PASSED}"

STATE_DIR="${HOME}/.claude/ralph-wiggum"
AUDIT_DIR="${HOME}/.claude/connascence-audit"
STATE_FILE="${STATE_DIR}/loop-state.md"
LOG_FILE="${STATE_DIR}/loop-history.log"

# Create directories
mkdir -p "$STATE_DIR"
mkdir -p "$AUDIT_DIR"

# Generate session ID
SESSION_ID="quality-$(date +%Y%m%d-%H%M%S)"

# Create state file with quality gate enabled
cat > "$STATE_FILE" << EOF
---
session_id: $SESSION_ID
active: true
iteration: 0
max_iterations: $MAX_ITERATIONS
completion_promise: "$COMPLETION_PROMISE"
quality_gate: true
started_at: $(date -Iseconds)
---
$PROMPT

QUALITY REQUIREMENTS:
- No CRITICAL connascence violations allowed
- Maximum 3 HIGH severity issues
- Code must pass Connascence Safety Analyzer audit

The analyzer will automatically audit your code after each file change.
Fix all blocking issues before completing.

To complete this loop, output: <promise>$COMPLETION_PROMISE</promise>
(This only works when the quality gate passes)
EOF

# Log the start
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Quality Gate Loop started: $SESSION_ID" >> "$LOG_FILE"
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Max iterations: $MAX_ITERATIONS" >> "$LOG_FILE"
echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Completion promise: $COMPLETION_PROMISE" >> "$LOG_FILE"

# Clear any previous audit results
rm -f "$AUDIT_DIR/latest-results.json" 2>/dev/null
rm -f "$AUDIT_DIR/pending-issues.md" 2>/dev/null

echo ""
echo "=========================================="
echo "   QUALITY GATE LOOP INITIALIZED"
echo "=========================================="
echo ""
echo "Session ID: $SESSION_ID"
echo "Max Iterations: $MAX_ITERATIONS"
echo "Quality Gate: ENABLED"
echo ""
echo "The Connascence Safety Analyzer will audit your code"
echo "after each file change. The loop continues until:"
echo ""
echo "  1. All quality issues are resolved"
echo "  2. You output: <promise>$COMPLETION_PROMISE</promise>"
echo ""
echo "Quality Thresholds:"
echo "  - CRITICAL: 0 allowed (blocking)"
echo "  - HIGH: Max 3 (blocking if exceeded)"
echo "  - MEDIUM/LOW: Recommendations only"
echo ""
echo "=========================================="
echo ""
