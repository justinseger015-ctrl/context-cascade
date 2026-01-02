#!/bin/bash
# setup-slash-commands.sh
# Copies key commands to ~/.claude/commands/ for slash command access
# Updated: 2026-01-02

set -uo pipefail

PLUGIN_DIR="C:/Users/17175/claude-code-plugins/context-cascade"
GLOBAL_COMMANDS="C:/Users/17175/.claude/commands"

echo "=== Context Cascade Slash Commands Setup ==="
echo ""

# Create commands directory if needed
mkdir -p "$GLOBAL_COMMANDS"

# Key commands to expose as slash commands
# Format: source_path:slash_name
COMMANDS=(
    # Core SPARC Commands
    "commands/delivery/sparc/sparc.md:sparc"
    "commands/delivery/sparc/code.md:code"
    "commands/delivery/sparc/debug.md:debug"
    "commands/delivery/sparc/architect.md:architect"
    "commands/delivery/sparc/tdd.md:tdd"
    "commands/delivery/sparc/reviewer.md:reviewer"
    "commands/delivery/sparc/tester.md:tester"
    "commands/delivery/sparc/researcher.md:researcher"
    "commands/delivery/sparc/documenter.md:documenter"
    "commands/delivery/sparc/analyzer.md:analyzer"
    "commands/delivery/sparc/optimizer.md:optimizer"
    "commands/delivery/sparc/devops.md:devops"
    "commands/delivery/sparc/security-review.md:security-review"
    "commands/delivery/sparc/mcp.md:mcp"

    # Essential Commands
    "commands/delivery/essential-commands/build-feature.md:build-feature"
    "commands/delivery/essential-commands/fix-bug.md:fix-bug"
    "commands/delivery/essential-commands/review-pr.md:review-pr"
    "commands/delivery/essential-commands/quick-check.md:quick-check"
    "commands/delivery/essential-commands/smoke-test.md:smoke-test"
    "commands/delivery/essential-commands/e2e-test.md:e2e-test"

    # Quality Commands
    "commands/quality-loop.md:quality-loop"

    # Foundry Commands
    "commands/foundry/recursive-improvement/run-improvement-cycle.md:improve"
    "commands/foundry/expertise/expertise-create.md:expertise-create"

    # Operations Commands
    "commands/operations/automation/smart-spawn.md:smart-spawn"
    "commands/operations/automation/auto-agent.md:auto-agent"

    # Workflow Commands
    "commands/delivery/workflows/development.md:development"
    "commands/delivery/workflows/deployment.md:deployment"
    "commands/delivery/workflows/testing.md:testing"
)

echo "Creating command files in ~/.claude/commands/..."
echo ""

CREATED=0
SKIPPED=0
FAILED=0

for entry in "${COMMANDS[@]}"; do
    SOURCE_PATH="${entry%%:*}"
    SLASH_NAME="${entry##*:}"

    SOURCE_FULL="$PLUGIN_DIR/$SOURCE_PATH"
    TARGET="$GLOBAL_COMMANDS/$SLASH_NAME.md"

    if [ -f "$SOURCE_FULL" ]; then
        if [ -f "$TARGET" ]; then
            echo "[SKIP] /$SLASH_NAME (already exists)"
            SKIPPED=$((SKIPPED + 1))
        else
            cp "$SOURCE_FULL" "$TARGET"
            echo "[OK] /$SLASH_NAME"
            CREATED=$((CREATED + 1))
        fi
    else
        echo "[WARN] Not found: $SOURCE_PATH"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "=== Summary ==="
echo "Created: $CREATED"
echo "Skipped: $SKIPPED"
echo "Failed:  $FAILED"
echo ""
echo "Available slash commands:"
ls -1 "$GLOBAL_COMMANDS"/*.md 2>/dev/null | xargs -I{} basename {} .md | sed 's/^/  \//' || echo "  (none)"
echo ""
echo "=== Setup Complete ==="
