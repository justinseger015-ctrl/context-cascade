#!/bin/bash
# skill-router-hook.sh
# PURPOSE: Smart skill routing via keyword matching with CASCADE DISCOVERY
# HOOK TYPE: UserPromptSubmit (runs before Claude processes user message)
# UPDATED: 2026-01-02 - Added cascade discovery integration
#
# CASCADE ARCHITECTURE:
#   User Request -> Skills (SKILL-INDEX) -> Agents (AGENT-REGISTRY) -> Commands
#
# This hook handles the TOP LEVEL: routing user intent to skills

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="${SCRIPT_DIR%/*}"
ROUTER="$PLUGIN_DIR/scripts/skill-index/route-skill.sh"
INDEX_FILE="$PLUGIN_DIR/scripts/skill-index/skill-index.json"
SKILL_INDEX="$PLUGIN_DIR/discovery/SKILL-INDEX.md"
AGENT_REGISTRY="$PLUGIN_DIR/discovery/AGENT-REGISTRY.md"

# Read the user's message from stdin (with timeout to prevent blocking)
USER_MESSAGE=$(timeout 5 cat 2>/dev/null || echo '{}')

# Extract the actual message text
MESSAGE_TEXT=$(echo "$USER_MESSAGE" | jq -r '.message // empty' 2>/dev/null || echo "$USER_MESSAGE")

# Trivial patterns (skip routing entirely)
TRIVIAL_PATTERNS=(
    "^(hi|hello|hey|thanks|thank you|ok|okay|yes|no|bye)$"
    "^(help|/help|/clear|/status|/tasks)"
    "^(git status|git log|ls|pwd)"
    "^what time"
    "^continue"
)

IS_TRIVIAL=false
for pattern in "${TRIVIAL_PATTERNS[@]}"; do
    if echo "$MESSAGE_TEXT" | grep -iqE "$pattern"; then
        IS_TRIVIAL=true
        break
    fi
done

# Skip for trivial requests
if [ "$IS_TRIVIAL" = true ]; then
    exit 0
fi

# Check if router and index exist
if [ ! -f "$ROUTER" ] || [ ! -f "$INDEX_FILE" ]; then
    echo "!! SKILL ROUTER NOT READY - Using fallback !!" >&2
    exit 0
fi

# Run the skill router
ROUTER_OUTPUT=$(bash "$ROUTER" "$MESSAGE_TEXT" 2>/dev/null)

# Check if we got matches
if [ -z "$ROUTER_OUTPUT" ] || echo "$ROUTER_OUTPUT" | grep -q "No matching skills"; then
    # No matches - fallback to standard 5-phase without skill suggestions
    cat << 'EOF'

!! CASCADE DISCOVERY - 5-PHASE WORKFLOW !!
================================================================

No specific skill matched. Execute standard 5-phase workflow:

1. Intent Analysis    -> Skill("intent-analyzer")
2. Prompt Optimization -> Skill("prompt-architect")
3. Strategic Planning  -> Skill("research-driven-planning")
4. Playbook Routing    -> Match tasks to skills from SKILL-INDEX
5. Execution           -> Skill -> Task(agent) -> TodoWrite

CASCADE DISCOVERY INDEXES:
- Skills:   discovery/SKILL-INDEX.md
- Agents:   discovery/AGENT-REGISTRY.md
- Commands: discovery/COMMAND-INDEX.md

================================================================
EOF
    exit 0
fi

# Output the smart routing result with CASCADE context
cat << EOF

!! CASCADE SKILL ROUTER !!
================================================================

MATCHED SKILLS (based on your request):

$ROUTER_OUTPUT

================================================================

CASCADE EXECUTION PATTERN:

  1. LOAD SKILL SOP:
     Read the matched skill's SKILL.md file
     Also check for ANTI-PATTERNS.md and examples/

  2. SKILL INVOKES AGENTS:
     Skill("skill-name")
         |
         v
     Task("description", "prompt", "agent-type")
         |
         v
     TodoWrite({ todos: [...] })

  3. AGENT DISCOVERY:
     Find agents in: discovery/AGENT-REGISTRY.md
     Or: agents/foundry/registry/registry.json

  4. COMMAND DISCOVERY:
     Agents use commands from: discovery/COMMAND-INDEX.md
     Registered at: ~/.claude/commands/

GOLDEN RULE: 1 MESSAGE = ALL PARALLEL Task() calls

================================================================

EOF

exit 0
