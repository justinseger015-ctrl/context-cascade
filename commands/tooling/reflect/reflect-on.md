---
name: reflect-on
description: Enable automatic session reflection on stop hook
allowed-tools:
- Read
- Write
- Edit
- Bash
model: sonnet
x-version: 1.0.0
x-category: tooling
x-vcl-compliance: v3.1.1
---

## STANDARD OPERATING PROCEDURE

### Purpose
- Primary action: Enable automatic reflection that triggers when a session ends (via stop hook)

### Trigger Conditions
- Command syntax: /reflect-on
- Run once to enable; persists across sessions until /reflect-off

### Inputs and Options
- No parameters required

### Execution Phases
1. Create/update state file at ~/.claude/reflect-enabled
2. Set value to "true"
3. Confirm activation to user
4. Stop hook will now trigger reflect skill on session end

### Success Criteria and Outputs
- State file created/updated
- Confirmation message displayed
- Future sessions will auto-reflect on end

### Error Handling and Recovery
- If state directory doesn't exist: Create it
- If write fails: Report permission error with remediation

### Chaining and Coordination
- Enables: session-reflect-stop.sh hook
- Related: /reflect-off, /reflect-status

### Memory and Tagging
- State stored in: ~/.claude/reflect-enabled
- No Memory MCP storage needed (local state only)

### Example Invocation
```bash
/reflect-on
```

### Output Format
```
Automatic reflection ENABLED.

When sessions end, the reflect skill will:
- Detect corrections and patterns (MEDIUM/LOW auto-applied)
- Update relevant skill files
- Store learnings in Memory MCP
- Commit changes to git

HIGH confidence learnings still require manual /reflect for approval.

Use /reflect-off to disable.
Use /reflect-status to check current state.
```

Confidence: 0.90 (ceiling: observation 0.95) - Simple toggle command.

---

## VCL COMPLIANCE APPENDIX (Internal Reference)

[[HON:teineigo]] [[MOR:root:R-F-L]] [[COM:Reflect+On]] [[CLS:ge_command]] [[EVD:-DI<gozlem>]] [[ASP:sov.]] [[SPC:path:/commands/tooling/reflect]]
[commit|confident] <promise>REFLECT_ON_COMMAND_VERILINGUA_VERIX_COMPLIANT</promise> [conf:0.90] [state:confirmed]
