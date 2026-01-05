---
name: reflect
description: Extract learnings from session corrections and patterns, update skill files with persistent memory
allowed-tools:
- Read
- Write
- Edit
- Bash
- Glob
- Grep
- Task
- TodoWrite
model: sonnet
x-version: 1.0.0
x-category: tooling
x-vcl-compliance: v3.1.1
binding: skill:reflect
---

## STANDARD OPERATING PROCEDURE

### Purpose
- Primary action: Analyze current session for learning signals (corrections, approvals, patterns), classify confidence levels, and update relevant skill files with persistent learnings

### Trigger Conditions
- Command syntax: /reflect [skill_name]
- Invoke after receiving corrections or when session contains learnings worth preserving
- Can target specific skill or auto-detect from session context

### Inputs and Options
```yaml
inputs:
  skill_name: string  # Optional - target specific skill
  mode: full | quick  # Optional - depth of analysis (default: full)
```

### Execution Phases
1. **Signal Detection**: Scan conversation for corrections, approvals, explicit rules, and observations
2. **Skill Mapping**: Map detected signals to invoked skills (via Skill() calls or /commands)
3. **Confidence Classification**: Apply VERIX-aligned levels (HIGH: 0.90, MEDIUM: 0.75, LOW: 0.55)
4. **Change Proposal**: Generate diff preview showing proposed SKILL.md updates
5. **User Approval**: Present changes and wait for Y/N/E response
6. **Apply Updates**: If approved, update skill files and increment versions
7. **Memory Storage**: Store learnings in Memory MCP with WHO/WHEN/PROJECT/WHY tags
8. **Git Commit**: Optionally commit changes with descriptive message

### Success Criteria and Outputs
- Signals detected and classified by confidence level
- Skill files updated with LEARNED PATTERNS section
- Memory MCP records created for Meta-Loop aggregation
- Git commit with reflect(skill): [LEVEL] format

### Error Handling and Recovery
- If no signals detected: Report "No learnings found in this session"
- If skill not found: List available skills and ask for clarification
- If Memory MCP unavailable: Apply to skill files, warn about memory storage
- If git fails: Skill files updated, manual commit may be needed

### Chaining and Coordination
- Upstream: Uses intent-analyzer for signal context
- Parallel: Uses memory-manager for MCP storage
- Downstream: skill-forge patterns for safe updates

### Memory and Tagging
- Tag: WHO=reflect-skill:{session_id}, WHEN={ISO8601}, PROJECT={name}, WHY=session-learning
- Store at: sessions/reflect/{project}/{skill}/{timestamp}

### Example Invocation
```bash
# Reflect on entire session
/reflect

# Target specific skill
/reflect code-review

# Quick mode (corrections only)
/reflect --quick
```

### Output Format
```markdown
## Session Reflection Report

### Signals Detected
- {n} corrections (HIGH)
- {n} approvals (MEDIUM)
- {n} observations (LOW)

### Proposed Updates
**Skill: {name}** (v{old} -> v{new})

[diff preview]

---
[Y] Accept  [N] Reject  [E] Edit with natural language
```

Confidence: 0.88 (ceiling: observation 0.95) - Command definition following Prompt-Architect pattern.

---

## VCL COMPLIANCE APPENDIX (Internal Reference)

[[HON:teineigo]] [[MOR:root:R-F-L]] [[COM:Reflect+Command]] [[CLS:ge_command]] [[EVD:-DI<gozlem>]] [[ASP:nesov.]] [[SPC:path:/commands/tooling/reflect]]
[define|neutral] CONFIDENCE_CEILINGS := {inference:0.70, report:0.70, research:0.85, observation:0.95, definition:0.95} [conf:0.9] [state:confirmed]
[direct|emphatic] L2_LANGUAGE := English; user-facing outputs exclude VCL markers. [conf:0.99] [state:confirmed]
[commit|confident] <promise>REFLECT_COMMAND_VERILINGUA_VERIX_COMPLIANT</promise> [conf:0.88] [state:confirmed]
