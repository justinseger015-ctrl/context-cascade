#!/bin/bash
# update-counts.sh - Updates skill and agent counts in registry and CLAUDE.md

PLUGIN_DIR="C:/Users/17175/claude-code-plugins/context-cascade"

# Count skills (SKILL.md files)
SKILL_COUNT=$(find "$PLUGIN_DIR/skills" -name "SKILL.md" 2>/dev/null | wc -l)

# Count agents (.md files excluding READMEs and reports)
AGENT_COUNT=$(find "$PLUGIN_DIR/agents" -name "*.md" \
  -not -name "README*" \
  -not -name "*SUMMARY*" \
  -not -name "*REPORT*" \
  -not -name "*INDEX*" \
  -not -name "*MIGRATION*" \
  2>/dev/null | wc -l)

# Count commands
COMMAND_COUNT=$(find "$PLUGIN_DIR/commands" -name "*.md" 2>/dev/null | wc -l)

# Count playbooks
PLAYBOOK_COUNT=$(find "$PLUGIN_DIR/playbooks" -name "*.md" 2>/dev/null | wc -l)

echo "=== Context Cascade Component Counts ==="
echo "Skills:    $SKILL_COUNT"
echo "Agents:    $AGENT_COUNT"
echo "Commands:  $COMMAND_COUNT"
echo "Playbooks: $PLAYBOOK_COUNT"
echo "Total:     $((SKILL_COUNT + AGENT_COUNT + COMMAND_COUNT + PLAYBOOK_COUNT))"
echo ""

# Update registry.json
REGISTRY="$PLUGIN_DIR/agents/foundry/registry/registry.json"
if [ -f "$REGISTRY" ]; then
  sed -i "s/\"total_agents\": [0-9]*/\"total_agents\": $AGENT_COUNT/" "$REGISTRY"
  echo "Updated registry.json: total_agents = $AGENT_COUNT"
fi

# Update CLAUDE.md in plugin
CLAUDE_MD="$PLUGIN_DIR/CLAUDE.md"
if [ -f "$CLAUDE_MD" ]; then
  sed -i "s/Skills | [0-9]*/Skills | $SKILL_COUNT/" "$CLAUDE_MD"
  sed -i "s/Agents | [0-9]*/Agents | $AGENT_COUNT/" "$CLAUDE_MD"
  echo "Updated plugin CLAUDE.md"
fi

# Update user's global CLAUDE.md
USER_CLAUDE="C:/Users/17175/.claude/CLAUDE.md"
if [ -f "$USER_CLAUDE" ]; then
  sed -i "s/Skills | [0-9]*/Skills | $SKILL_COUNT/" "$USER_CLAUDE"
  sed -i "s/Agents | [0-9]*/Agents | $AGENT_COUNT/" "$USER_CLAUDE"
  echo "Updated user CLAUDE.md"
fi

echo ""
echo "Done!"
