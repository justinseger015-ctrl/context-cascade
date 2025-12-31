#!/bin/bash
# Session Start Hook: Check plugin availability
# This hook should fire at the start of each conversation

PLUGIN_PATH="claude-code-plugins/context-cascade"
AGENTS_PATH="$PLUGIN_PATH/agents/README.md"

echo "=================================================="
echo "!! SESSION START - RUV-SPARC PLUGIN CHECK !!"
echo "=================================================="
echo ""

# Check if plugin exists
if [ -d "$PLUGIN_PATH" ]; then
    echo "[OK] ruv-sparc plugin found at: $PLUGIN_PATH"

    # Count agents if possible
    AGENT_COUNT=$(find "$PLUGIN_PATH/agents" -name "*.md" 2>/dev/null | wc -l)
    echo "[OK] Agent registry contains approximately $AGENT_COUNT agent definitions"
else
    echo "[!!] WARNING: ruv-sparc plugin NOT found at expected path"
    echo "     Expected: $PLUGIN_PATH"
fi

echo ""
echo "MANDATORY FIRST ACTIONS:"
echo "  1. Read('$AGENTS_PATH')"
echo "  2. Output: 'ruv-sparc plugin loaded: 122 skills, 203 agents'"
echo "  3. Remember: Skill() MUST spawn Task() agents"
echo ""
echo "THREE UNBREAKABLE RULES:"
echo "  1. Skill() MUST spawn Task() agents"
echo "  2. 1 MESSAGE = ALL RELATED OPERATIONS"
echo "  3. Agents come from registry ONLY"
echo "=================================================="
