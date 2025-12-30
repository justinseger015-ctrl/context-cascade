#!/bin/bash

# Ralph Wiggum Stop Hook - INTEGRATED VERSION
#
# This hook is DUMB. It only calls loopctl.
# loopctl is the single throat to choke.
#
# INVARIANTS:
# - Ralph is executor, not governor (doesn't decide goodness)
# - Governance + harness decide block/allow continuation
# - Ralph produces ARTIFACTS; harness produces TRUTH
#
# Integration Flow:
#   1. Ralph iteration produces artifact
#   2. Stop-hook intercepts exit
#   3. loopctl grades artifact with FROZEN harness
#   4. loopctl asks UnifiedBridge for decision
#   5. Stop-hook returns decision to Claude Code

set -euo pipefail

# Read hook input from stdin (advanced stop hook API)
HOOK_INPUT=$(cat)

# Configuration
STATE_FILE="${RALPH_STATE_FILE:-.claude/ralph-loop.local.md}"
LOOP_DIR="${RALPH_LOOP_DIR:-cognitive-architecture/integration/.loop}"
LOOPCTL_PATH="${LOOPCTL_PATH:-cognitive-architecture/loopctl}"

# Check if ralph-loop is active
if [[ ! -f "$STATE_FILE" ]]; then
  # No active loop - allow exit
  exit 0
fi

# Parse markdown frontmatter for iteration and completion_promise
FRONTMATTER=$(sed -n '/^---$/,/^---$/{ /^---$/d; p; }' "$STATE_FILE")
ITERATION=$(echo "$FRONTMATTER" | grep '^iteration:' | sed 's/iteration: *//')
COMPLETION_PROMISE=$(echo "$FRONTMATTER" | grep '^completion_promise:' | sed 's/completion_promise: *//' | sed 's/^"\(.*\)"$/\1/')

# Validate iteration is numeric
if [[ ! "$ITERATION" =~ ^[0-9]+$ ]]; then
  echo "Warning: State file corrupted (iteration not numeric)" >&2
  rm "$STATE_FILE"
  exit 0
fi

# Get transcript path from hook input
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path')

# Check for completion promise in last output (before calling loopctl)
if [[ -f "$TRANSCRIPT_PATH" ]] && [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  LAST_LINE=$(grep '"role":"assistant"' "$TRANSCRIPT_PATH" | tail -1 || echo "")
  if [[ -n "$LAST_LINE" ]]; then
    LAST_OUTPUT=$(echo "$LAST_LINE" | jq -r '
      .message.content |
      map(select(.type == "text")) |
      map(.text) |
      join("\n")
    ' 2>/dev/null || echo "")

    # Extract promise text
    PROMISE_TEXT=$(echo "$LAST_OUTPUT" | perl -0777 -pe 's/.*?<promise>(.*?)<\/promise>.*/$1/s; s/^\s+|\s+$//g; s/\s+/ /g' 2>/dev/null || echo "")

    if [[ -n "$PROMISE_TEXT" ]] && [[ "$PROMISE_TEXT" = "$COMPLETION_PROMISE" ]]; then
      echo "Completion promise detected: <promise>$COMPLETION_PROMISE</promise>" >&2
      rm "$STATE_FILE"
      exit 0
    fi
  fi
fi

# === THE KEY INTEGRATION ===
# Stop-hook is DUMB. It only calls loopctl.
# loopctl is the single authority for decisions.

# Call loopctl for decision
DECISION_JSON=$(python -m loopctl ralph_iteration_complete \
  --state "$STATE_FILE" \
  --loop-dir "$LOOP_DIR" \
  --iteration "$ITERATION" \
  2>/dev/null || echo '{"decision":"allow","reason":"loopctl error"}')

# Parse decision
DECISION=$(echo "$DECISION_JSON" | jq -r '.decision // "allow"')
REASON=$(echo "$DECISION_JSON" | jq -r '.reason // "unknown"')

if [[ "$DECISION" == "allow" ]]; then
  # Allow exit - cleanup state file
  echo "Loop ending: $REASON" >&2
  rm -f "$STATE_FILE"
  exit 0
fi

# Decision is "block" - continue loop
NEXT_ITERATION=$((ITERATION + 1))

# Extract original prompt from state file
PROMPT_TEXT=$(awk '/^---$/{i++; next} i>=2' "$STATE_FILE")

if [[ -z "$PROMPT_TEXT" ]]; then
  echo "Warning: No prompt text in state file" >&2
  rm "$STATE_FILE"
  exit 0
fi

# Update iteration in state file (atomic)
TEMP_FILE="${STATE_FILE}.tmp.$$"
sed "s/^iteration: .*/iteration: $NEXT_ITERATION/" "$STATE_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$STATE_FILE"

# Build system message
if [[ "$COMPLETION_PROMISE" != "null" ]] && [[ -n "$COMPLETION_PROMISE" ]]; then
  SYSTEM_MSG="Ralph iteration $NEXT_ITERATION | loopctl: $REASON | To stop: output <promise>$COMPLETION_PROMISE</promise>"
else
  SYSTEM_MSG="Ralph iteration $NEXT_ITERATION | loopctl: $REASON"
fi

# Output JSON to block the stop and feed prompt back
jq -n \
  --arg prompt "$PROMPT_TEXT" \
  --arg msg "$SYSTEM_MSG" \
  '{
    "decision": "block",
    "reason": $prompt,
    "systemMessage": $msg
  }'

exit 0
