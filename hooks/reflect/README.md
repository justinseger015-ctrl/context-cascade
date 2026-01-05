# Reflect Hooks

Hooks for automatic session reflection in Claude Code.

## Files

| File | Purpose |
|------|---------|
| `session-reflect-stop.sh` | Stop hook that triggers reflection on session end |
| `reflect-state.sh` | Utility script for managing reflection state |

## Installation

Add to your `.claude/settings.local.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "bash /path/to/hooks/reflect/session-reflect-stop.sh",
        "timeout": 5000
      }
    ]
  }
}
```

Or add to existing hooks array if you have other Stop hooks.

## Usage

### Enable Automatic Reflection

```bash
# Via command
/reflect-on

# Or via utility script
./hooks/reflect/reflect-state.sh enable
```

### Disable Automatic Reflection

```bash
# Via command
/reflect-off

# Or via utility script
./hooks/reflect/reflect-state.sh disable
```

### Check Status

```bash
# Via command
/reflect-status

# Or via utility script
./hooks/reflect/reflect-state.sh status
```

## How It Works

1. **State File**: `~/.claude/reflect-enabled` stores the toggle state
2. **Stop Hook**: When session ends, `session-reflect-stop.sh` checks state
3. **If Enabled**: Hook outputs prompt for Claude to analyze session
4. **Reflection**: Claude scans for corrections/patterns and updates skills
5. **History**: All reflections logged to `~/.claude/reflect-history.log`

## Behavior

When `reflect-on` is enabled:

- **MEDIUM/LOW** confidence learnings are auto-applied
- **HIGH** confidence learnings are noted for manual `/reflect`
- Skill files are updated with LEARNED PATTERNS section
- Memory MCP stores learnings for Meta-Loop aggregation
- Git commits track skill evolution

When `reflect-off` or not configured:

- Stop hook exits silently
- Manual `/reflect` still available
- No automatic skill updates

## State Files

| File | Purpose |
|------|---------|
| `~/.claude/reflect-enabled` | Toggle state (true/false) |
| `~/.claude/reflect-history.log` | Reflection history log |
| `~/.claude/current-session.txt` | Session transcript (if available) |

## Integration

- **Ralph Wiggum**: Compatible with Ralph loop stop hooks
- **Memory MCP**: Stores learnings for cross-session retrieval
- **Meta-Loop**: Aggregates learnings every 3 days

## Safety

- Never modifies eval-harness (frozen per Bootstrap Loop)
- HIGH confidence changes require manual approval
- Auto-apply only for MEDIUM/LOW when enabled
- All changes are reversible via git

---

Confidence: 0.88 (ceiling: observation 0.95)
