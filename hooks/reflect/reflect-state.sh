#!/bin/bash
# reflect-state.sh
# Utility script for managing reflect state
#
# Usage:
#   ./reflect-state.sh enable   - Enable automatic reflection
#   ./reflect-state.sh disable  - Disable automatic reflection
#   ./reflect-state.sh status   - Check current state
#   ./reflect-state.sh history  - Show recent reflection history

STATE_DIR="${HOME}/.claude"
STATE_FILE="${STATE_DIR}/reflect-enabled"
LOG_FILE="${STATE_DIR}/reflect-history.log"

# Ensure state directory exists
mkdir -p "$STATE_DIR"

case "$1" in
    enable|on)
        echo "true" > "$STATE_FILE"
        echo "Automatic reflection ENABLED"
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Reflection enabled" >> "$LOG_FILE"
        ;;

    disable|off)
        echo "false" > "$STATE_FILE"
        echo "Automatic reflection DISABLED"
        echo "[$(date +%Y-%m-%d\ %H:%M:%S)] Reflection disabled" >> "$LOG_FILE"
        ;;

    status)
        if [[ -f "$STATE_FILE" ]]; then
            CURRENT=$(cat "$STATE_FILE" | tr -d '[:space:]')
            if [[ "$CURRENT" == "true" ]]; then
                echo "Status: ENABLED"
                echo "Sessions will auto-reflect on end"
            else
                echo "Status: DISABLED"
                echo "Manual /reflect required"
            fi
        else
            echo "Status: NOT CONFIGURED"
            echo "Run 'reflect-state.sh enable' to enable"
        fi
        ;;

    history)
        if [[ -f "$LOG_FILE" ]]; then
            echo "=== Recent Reflection History ==="
            tail -20 "$LOG_FILE"
        else
            echo "No reflection history found"
        fi
        ;;

    *)
        echo "Usage: $0 {enable|disable|status|history}"
        echo ""
        echo "Commands:"
        echo "  enable   Enable automatic session reflection"
        echo "  disable  Disable automatic session reflection"
        echo "  status   Show current reflection state"
        echo "  history  Show recent reflection history"
        exit 1
        ;;
esac

exit 0
