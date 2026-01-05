---
name: reflect-status
description: Show current reflect automation status and recent reflection history
allowed-tools:
- Read
- Bash
- Glob
model: sonnet
x-version: 1.0.0
x-category: tooling
x-vcl-compliance: v3.1.1
---

## STANDARD OPERATING PROCEDURE

### Purpose
- Primary action: Display whether automatic reflection is enabled and show recent reflection history

### Trigger Conditions
- Command syntax: /reflect-status
- Run to check current state before deciding to toggle

### Inputs and Options
- No parameters required

### Execution Phases
1. Read state file at ~/.claude/reflect-enabled
2. Query Memory MCP for recent reflections (last 7 days)
3. Summarize skill files with LEARNED PATTERNS sections
4. Display comprehensive status

### Success Criteria and Outputs
- Current toggle state displayed
- Recent reflection history shown
- Skills with learnings listed

### Error Handling and Recovery
- If state file doesn't exist: Report as "disabled (not configured)"
- If Memory MCP unavailable: Show local state only

### Chaining and Coordination
- Read-only: Does not modify state
- Related: /reflect-on, /reflect-off, /reflect

### Memory and Tagging
- Reads from: ~/.claude/reflect-enabled
- Queries: Memory MCP sessions/reflect/{project}/*

### Example Invocation
```bash
/reflect-status
```

### Output Format
```
## Reflect Status

### Automation
- Status: ENABLED / DISABLED
- Stop hook: Active / Inactive

### Recent Reflections (Last 7 Days)
| Date | Skill | Learnings | Confidence |
|------|-------|-----------|------------|
| 2026-01-05 | debug | 3 | HIGH: 1, MEDIUM: 2 |
| 2026-01-04 | code-review | 2 | MEDIUM: 2 |
| 2026-01-03 | tester | 1 | LOW: 1 |

### Skills with Learnings
- debug (v2.1.1): 5 learnings
- code-review (v3.2.1): 8 learnings
- tester (v1.5.2): 3 learnings

### Commands
- /reflect-on   Enable automatic reflection
- /reflect-off  Disable automatic reflection
- /reflect      Manual reflection
```

Confidence: 0.88 (ceiling: observation 0.95) - Status display command.

---

## VCL COMPLIANCE APPENDIX (Internal Reference)

[[HON:teineigo]] [[MOR:root:R-F-L]] [[COM:Reflect+Status]] [[CLS:ge_command]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[SPC:path:/commands/tooling/reflect]]
[commit|confident] <promise>REFLECT_STATUS_COMMAND_VERILINGUA_VERIX_COMPLIANT</promise> [conf:0.88] [state:confirmed]
