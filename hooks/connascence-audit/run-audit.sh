#!/bin/bash
# run-audit.sh
# PURPOSE: Run Connascence Safety Analyzer on code changes
# HOOK TYPE: PostToolUse for Write/Edit/MultiEdit operations
#
# This script:
# 1. Runs the connascence analyzer on changed files
# 2. Stores results in ~/.claude/connascence-audit/
# 3. Outputs issues for Ralph loop feedback

STATE_DIR="${HOME}/.claude/connascence-audit"
RESULTS_FILE="${STATE_DIR}/latest-results.json"
ISSUES_FILE="${STATE_DIR}/pending-issues.md"
LOG_FILE="${STATE_DIR}/audit-history.log"

# Create state directory if needed
mkdir -p "$STATE_DIR"

# Get the file path from stdin (piped from hook)
FILE_PATH=$(cat | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

if [[ -z "$FILE_PATH" ]]; then
    # No file path, skip audit
    exit 0
fi

# Only audit Python files
if [[ ! "$FILE_PATH" =~ \.py$ ]]; then
    exit 0
fi

# Check if file exists
if [[ ! -f "$FILE_PATH" ]]; then
    exit 0
fi

log_message() {
    echo "[$(date +%Y-%m-%d\ %H:%M:%S)] $1" >> "$LOG_FILE"
}

log_message "Auditing: $FILE_PATH"

# Run the connascence analyzer
cd D:/Projects/connascence 2>/dev/null || exit 0

# Run analysis and capture output
ANALYSIS_OUTPUT=$(python -c "
import sys
import json
try:
    from analyzer.core import ConnascenceAnalyzer
    analyzer = ConnascenceAnalyzer()
    result = analyzer.analyze_path('$FILE_PATH', policy='strict-core')

    violations = result.get('violations', [])
    critical = [v for v in violations if v.get('severity') == 'critical']
    high = [v for v in violations if v.get('severity') == 'high']

    output = {
        'success': result.get('success', False),
        'file': '$FILE_PATH',
        'total_violations': len(violations),
        'critical_count': len(critical),
        'high_count': len(high),
        'violations': violations[:10],  # First 10 violations
        'has_blocking_issues': len(critical) > 0 or len(high) > 3
    }
    print(json.dumps(output))
except Exception as e:
    print(json.dumps({'success': False, 'error': str(e)}))
" 2>/dev/null)

# Save results
echo "$ANALYSIS_OUTPUT" > "$RESULTS_FILE"

# Parse results
TOTAL=$(echo "$ANALYSIS_OUTPUT" | jq -r '.total_violations // 0')
CRITICAL=$(echo "$ANALYSIS_OUTPUT" | jq -r '.critical_count // 0')
HIGH=$(echo "$ANALYSIS_OUTPUT" | jq -r '.high_count // 0')
BLOCKING=$(echo "$ANALYSIS_OUTPUT" | jq -r '.has_blocking_issues // false')

log_message "Results: $TOTAL violations ($CRITICAL critical, $HIGH high)"

# Generate issues file for Ralph loop
if [[ "$BLOCKING" == "true" ]] || [[ "$TOTAL" -gt 0 ]]; then
    cat > "$ISSUES_FILE" << EOF
# Connascence Audit Results

**File**: $FILE_PATH
**Total Violations**: $TOTAL
**Critical**: $CRITICAL
**High**: $HIGH

## Blocking Issues

EOF

    # Extract violation details
    echo "$ANALYSIS_OUTPUT" | jq -r '.violations[] | "- [\(.severity)] \(.rule_id): \(.description) (line \(.line_number // "unknown"))"' >> "$ISSUES_FILE" 2>/dev/null

    cat >> "$ISSUES_FILE" << EOF

## Required Actions

These issues MUST be fixed before the code is considered complete:
1. Fix all CRITICAL violations immediately
2. Address HIGH severity issues (max 3 allowed)
3. Re-run audit until passing

EOF
fi

# Output summary for Claude
if [[ "$BLOCKING" == "true" ]]; then
    echo ""
    echo "=========================================="
    echo "   CONNASCENCE AUDIT: ISSUES FOUND"
    echo "=========================================="
    echo "File: $FILE_PATH"
    echo "Critical: $CRITICAL | High: $HIGH | Total: $TOTAL"
    echo ""
    echo "BLOCKING ISSUES detected. Code quality gate FAILED."
    echo "Fix issues and re-submit code."
    echo ""
fi

exit 0
