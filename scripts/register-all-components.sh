#!/bin/bash
# register-all-components.sh
# Registers ALL commands, skills, and agents for Claude Code discovery
# Updated: 2026-01-02

set -uo pipefail

PLUGIN_DIR="C:/Users/17175/claude-code-plugins/context-cascade"
GLOBAL_COMMANDS="C:/Users/17175/.claude/commands"

echo "=== Context Cascade Full Component Registration ==="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Create directories
mkdir -p "$GLOBAL_COMMANDS"
mkdir -p "$GLOBAL_COMMANDS/skills"
mkdir -p "$GLOBAL_COMMANDS/agents"

TOTAL_CREATED=0
TOTAL_SKIPPED=0

# ============================================
# REGISTER ALL COMMANDS (245)
# ============================================
echo "=== Registering Commands ==="

find "$PLUGIN_DIR/commands" -name "*.md" -type f ! -name "README*" | while read -r file; do
    # Get relative path and create flat name
    REL_PATH="${file#$PLUGIN_DIR/commands/}"
    # Convert path to slash command name (e.g., delivery/sparc/code.md -> delivery-sparc-code)
    SLASH_NAME=$(echo "$REL_PATH" | sed 's|/|-|g' | sed 's|\.md$||')
    TARGET="$GLOBAL_COMMANDS/$SLASH_NAME.md"

    if [ ! -f "$TARGET" ]; then
        cp "$file" "$TARGET"
        echo "[CMD] /$SLASH_NAME"
    fi
done

CMD_COUNT=$(find "$GLOBAL_COMMANDS" -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')
echo "Commands registered: $CMD_COUNT"
echo ""

# ============================================
# REGISTER ALL SKILLS (237)
# ============================================
echo "=== Registering Skills ==="

find "$PLUGIN_DIR/skills" -name "SKILL.md" -type f | grep -v "_merged" | grep -v "packaged" | while read -r file; do
    # Get skill directory name
    SKILL_DIR=$(dirname "$file")
    SKILL_NAME=$(basename "$SKILL_DIR")
    # Get category from path
    REL_PATH="${SKILL_DIR#$PLUGIN_DIR/skills/}"
    CATEGORY=$(echo "$REL_PATH" | cut -d'/' -f1)

    # Create skill command file
    SLASH_NAME="skill-${CATEGORY}-${SKILL_NAME}"
    TARGET="$GLOBAL_COMMANDS/skills/$SLASH_NAME.md"

    if [ ! -f "$TARGET" ]; then
        cp "$file" "$TARGET"
        echo "[SKILL] /$SLASH_NAME"
    fi
done

SKILL_COUNT=$(find "$GLOBAL_COMMANDS/skills" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "Skills registered: $SKILL_COUNT"
echo ""

# ============================================
# REGISTER ALL AGENTS (217)
# ============================================
echo "=== Registering Agents ==="

find "$PLUGIN_DIR/agents" -name "*.md" -type f ! -name "README*" ! -name "*SUMMARY*" ! -name "*REPORT*" ! -name "*INDEX*" | while read -r file; do
    # Get agent name
    AGENT_NAME=$(basename "$file" .md)
    # Get category from path
    REL_PATH="${file#$PLUGIN_DIR/agents/}"
    CATEGORY=$(echo "$REL_PATH" | cut -d'/' -f1)

    SLASH_NAME="agent-${CATEGORY}-${AGENT_NAME}"
    TARGET="$GLOBAL_COMMANDS/agents/$SLASH_NAME.md"

    if [ ! -f "$TARGET" ]; then
        cp "$file" "$TARGET"
        echo "[AGENT] /$SLASH_NAME"
    fi
done

AGENT_COUNT=$(find "$GLOBAL_COMMANDS/agents" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "Agents registered: $AGENT_COUNT"
echo ""

# ============================================
# SUMMARY
# ============================================
echo "=== Registration Complete ==="
echo ""
echo "Component Counts:"
echo "  Commands: $CMD_COUNT"
echo "  Skills:   $SKILL_COUNT"
echo "  Agents:   $AGENT_COUNT"
TOTAL=$((CMD_COUNT + SKILL_COUNT + AGENT_COUNT))
echo "  Total:    $TOTAL"
echo ""
echo "Locations:"
echo "  Commands: $GLOBAL_COMMANDS/*.md"
echo "  Skills:   $GLOBAL_COMMANDS/skills/*.md"
echo "  Agents:   $GLOBAL_COMMANDS/agents/*.md"
echo ""
echo "Usage examples:"
echo "  /sparc              - SPARC workflow"
echo "  /skill-quality-code-review-assistant"
echo "  /agent-delivery-feature-builder"
echo ""
