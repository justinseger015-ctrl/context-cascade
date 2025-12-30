#!/bin/bash
# ralph-loop-stop-hook-wrapper.sh
# PURPOSE: Wrapper that delegates to enhanced JS hook when available
# HOOK TYPE: Stop (runs when Claude tries to end session)
#
# This wrapper:
# 1. Checks if Node.js is available
# 2. Checks if enhanced JS hook exists
# 3. Delegates to JS hook for Memory-MCP integration
# 4. Falls back to shell script if JS unavailable
#
# @version 3.0.0
# @see docs/META-LOOP-ENHANCEMENT-PLAN-v4.md Phase E

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENHANCED_HOOK="${SCRIPT_DIR}/ralph-loop-stop-hook-enhanced.js"
FALLBACK_HOOK="${SCRIPT_DIR}/ralph-loop-stop-hook.sh"

# Check if Node.js is available
if command -v node &> /dev/null && [[ -f "$ENHANCED_HOOK" ]]; then
    # Delegate to enhanced JS hook
    # Pass stdin through to the JS hook
    exec node "$ENHANCED_HOOK"
else
    # Fall back to shell script
    if [[ -f "$FALLBACK_HOOK" ]]; then
        exec bash "$FALLBACK_HOOK"
    else
        # No hook available, allow exit
        exit 0
    fi
fi
