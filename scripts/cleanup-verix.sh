#!/bin/bash
# Script to remove VERIX markers from SKILL.md files
# Removes: VCL COMPLIANCE APPENDIX, ABSOLUTE RULES sections, [marker|type] patterns, <promise> tags

cleanup_file() {
    local file="$1"
    local temp_file="${file}.tmp"

    # Use awk to remove VERIX content while preserving the main SOP
    awk '
    BEGIN { in_verix_section = 0; skip_line = 0 }

    # Stop output at VCL COMPLIANCE APPENDIX
    /^## VCL COMPLIANCE APPENDIX/ { in_verix_section = 1 }
    /^---$/ && in_verix_section { next }
    /^<!-- S[0-9]/ { in_verix_section = 1 }

    # Skip lines with VERIX markers
    /\[define\|/ { next }
    /\[direct\|/ { next }
    /\[commit\|/ { next }
    /\[assert\|/ { next }
    /\[query\|/ { next }
    /\[\[HON:/ { next }
    /<promise>/ { next }
    /RULE_NO_UNICODE/ { next }
    /RULE_EVIDENCE/ { next }
    /RULE_REGISTRY/ { next }
    /SUCCESS_CRITERIA :=/ { next }
    /MCP_INTEGRATION :=/ { next }
    /MEMORY_NAMESPACE :=/ { next }
    /MEMORY_TAGGING :=/ { next }
    /COMPLETION_CHECKLIST :=/ { next }

    # Skip if in VERIX section
    in_verix_section { next }

    # Print everything else
    { print }
    ' "$file" > "$temp_file"

    # Remove trailing empty lines and extra separators
    sed -i ':a;/^[[:space:]]*$/{$d;N;ba}' "$temp_file" 2>/dev/null || \
    sed -i '' -e ':a' -e '/^[[:space:]]*$/{$d;N;ba' -e '}' "$temp_file"

    mv "$temp_file" "$file"
    echo "Cleaned: $file"
}

# Process all files passed as arguments
for file in "$@"; do
    if [ -f "$file" ]; then
        cleanup_file "$file"
    fi
done
