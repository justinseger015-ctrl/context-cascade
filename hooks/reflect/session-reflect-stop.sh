#!/bin/bash
# session-reflect-stop.sh
# Hook: Stop
# Purpose: Trigger automatic reflection when session ends (if enabled)
#
# This hook:
# 1. Checks if reflect-on is enabled
# 2. If enabled, invokes the reflect skill in quick mode
# 3. Auto-applies MEDIUM/LOW learnings
# 4. Displays summary of learnings captured

STATE_DIR="${HOME}/.claude"
STATE_FILE="${STATE_DIR}/reflect-enabled"
LOG_FILE="${STATE_DIR}/reflect-history.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure state directory exists
mkdir -p "$STATE_DIR"

# Function to log
log_message() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" >> "$LOG_FILE"
}

# Check if reflection is enabled
if [[ ! -f "$STATE_FILE" ]]; then
    # Not configured, skip silently
    exit 0
fi

REFLECT_ENABLED=$(cat "$STATE_FILE" 2>/dev/null | tr -d '[:space:]')

if [[ "$REFLECT_ENABLED" != "true" ]]; then
    # Disabled, skip silently
    exit 0
fi

log_message "Session ending - automatic reflection triggered"

# Output reflection trigger message
cat << 'EOF'

==========================================
   SESSION REFLECTION (Automatic)
==========================================

Reflect-on is enabled. Analyzing session for learnings...

Scanning for:
- Corrections (HIGH confidence - will show for approval)
- Approvals and patterns (MEDIUM - auto-applied)
- Observations (LOW - auto-applied)

EOF

# The actual reflection logic would be handled by Claude
# when this hook triggers a re-prompt with reflection context

# Check if there's session context to analyze
# This is a placeholder - actual implementation depends on
# how session transcripts are accessible

SESSION_TRANSCRIPT="${STATE_DIR}/current-session.txt"
if [[ -f "$SESSION_TRANSCRIPT" ]]; then
    WORD_COUNT=$(wc -w < "$SESSION_TRANSCRIPT")

    if [[ $WORD_COUNT -lt 100 ]]; then
        log_message "Session too short ($WORD_COUNT words), skipping reflection"
        cat << 'EOF'
Session too short for meaningful reflection.
No learnings captured.

Use /reflect manually after longer sessions.
==========================================
EOF
        exit 0
    fi
fi

# Output instruction for Claude to perform reflection
cat << 'EOF'
Please analyze this session for learning signals:

1. Look for corrections: "No, use X instead", "That's wrong"
2. Look for explicit rules: "Always do X", "Never do Y"
3. Look for approvals: "Perfect", "Yes, exactly"
4. Look for patterns that worked well

For MEDIUM/LOW confidence learnings, auto-apply to skill files.
For HIGH confidence learnings, note them for next manual /reflect.

After analysis, summarize:
- Skills updated
- Learnings captured
- Any HIGH confidence items pending approval

==========================================
EOF

log_message "Reflection prompt injected"

# Exit normally - Claude will handle the reflection
exit 0
