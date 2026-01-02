#!/bin/bash
# sop-compliance-verifier.sh
# PURPOSE: Verify that Skill SOPs are being followed with CASCADE architecture
# HOOK TYPE: PreToolUse (runs before Write/Edit)
# UPDATED: 2026-01-02 - Integrated cascade discovery paths
#
# CASCADE ARCHITECTURE:
#   Skills define SOPs -> Agents execute via Task() -> Commands for actions

# Read tool execution data from stdin (with timeout)
TOOL_DATA=$(timeout 3 cat 2>/dev/null || echo '{}')

# Extract tool name
TOOL_NAME=$(echo "$TOOL_DATA" | jq -r '.tool_name // empty' 2>/dev/null)

# Only show reminder for Write/Edit operations
if [[ "$TOOL_NAME" == "Write" ]] || [[ "$TOOL_NAME" == "Edit" ]]; then
    cat << 'EOF'

!! CASCADE SOP COMPLIANCE !!
============================================================

Before modifying files, verify CASCADE pattern is active:

1. SKILL LOADED?
   - Read the skill's SKILL.md for the SOP
   - Check discovery/SKILL-INDEX.md for routing

2. AGENTS SPAWNED?
   - Skills invoke agents via Task()
   - Find agents in: discovery/AGENT-REGISTRY.md
   - Pattern: Task("desc", "prompt", "agent-type")

3. TODOS TRACKED?
   - TodoWrite() for progress tracking
   - 5-10 items for substantial work

4. PARALLEL EXECUTION?
   - 1 MESSAGE = ALL PARALLEL Task() calls
   - Don't spawn sequentially

CASCADE INDEXES:
- Skills:   discovery/SKILL-INDEX.md (237 skills)
- Agents:   discovery/AGENT-REGISTRY.md (217 agents)
- Commands: discovery/COMMAND-INDEX.md (245 commands)

============================================================
EOF
fi

exit 0
