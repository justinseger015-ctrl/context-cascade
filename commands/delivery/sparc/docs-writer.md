---

<!-- META-LOOP v2.1 INTEGRATION -->
## Phase 0: Expertise Loading
expertise_check:
  domain: agent-creation
  file: .claude/expertise/agent-creation.yaml
  fallback: discovery_mode

## Recursive Improvement Integration (v2.1)
benchmark: docs-writer-benchmark-v1
  tests:
    - command_execution_success
    - output_validation
  success_threshold: 0.9
namespace: "commands/delivery/sparc/docs-writer/{project}/{timestamp}"
uncertainty_threshold: 0.85
coordination:
  related_skills: [sparc-methodology, coder]
  related_agents: [coder, reviewer, tester]

## COMMAND COMPLETION VERIFICATION
success_metrics:
  execution_success: ">95%"
<!-- END META-LOOP -->

name: sparc-docs-writer
description: 📚 Documentation Writer - You write concise, clear, and modular Markdown documentation that explains usage, integration, se...
---

## Command Purpose
One-line description of what this command does.

## Input Requirements
- **Parameters**: What parameters are needed
- **Context**: What context must be available
- **Prerequisites**: What must be true before running

## Expected Output
- **Primary**: Main deliverable/result
- **Side Effects**: Files created, state changes
- **Format**: Structure of output (reports, files, logs)

## Success Indicators
- [assert|neutral] How to verify the command completed successfully [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] What to check/validate [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Expected metrics/benchmarks [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Error Handling
- **Common Errors**: Typical failure modes
- **Recovery**: How to handle failures
- **Fallbacks**: Alternative approaches

## Related Commands
- **Before**: Commands that should run first
- **After**: Commands that typically follow
- **Complementary**: Commands that work together

## SPARC Integration
- **Phase**: Which SPARC phase this command supports (Specification/Pseudocode/Architecture/Refinement/Completion)
- **Activation**: MCP vs NPX vs local execution
- **Memory**: What gets stored in Memory MCP


# 📚 Documentation Writer

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Role Definition
You write concise, clear, and modular Markdown documentation that explains usage, integration, setup, and configuration.

## Custom Instructions
Only work in .md files. Use sections, examples, and headings. Keep each file under 500 lines. Do not leak env values. Summarize what you wrote using `attempt_completion`. Delegate large guides with `new_task`.

## Available Tools
- **read**: File reading and viewing
- **edit**: Markdown files only (Files matching: \.md$)

## Usage

### Option 1: Using MCP Tools (Preferred in Claude Code)
```javascript
mcp__claude-flow__sparc_mode {
  mode: "docs-writer",
  task_description: "create API documentation",
  options: {
    namespace: "docs-writer",
    non_interactive: false
  }
}
```

### Option 2: Using NPX CLI (Fallback when MCP not available)
```bash
# Use when running from terminal or MCP tools unavailable
npx claude-flow sparc run docs-writer "create API documentation"

# For alpha features
npx claude-flow@alpha sparc run docs-writer "create API documentation"

# With namespace
npx claude-flow sparc run docs-writer "your task" --namespace docs-writer

# Non-interactive mode
npx claude-flow sparc run docs-writer "your task" --non-interactive
```

### Option 3: Local Installation
```bash
# If claude-flow is installed locally
./claude-flow sparc run docs-writer "create API documentation"
```

## Memory Integration

### Using MCP Tools (Preferred)
```javascript
// Store mode-specific context
mcp__claude-flow__memory_usage {
  action: "store",
  key: "docs-writer_context",
  value: "important decisions",
  namespace: "docs-writer"
}

// Query previous work
mcp__claude-flow__memory_search {
  pattern: "docs-writer",
  namespace: "docs-writer",
  limit: 5
}
```

### Using NPX CLI (Fallback)
```bash
# Store mode-specific context
npx claude-flow memory store "docs-writer_context" "important decisions" --namespace docs-writer

# Query previous work
npx claude-flow memory query "docs-writer" --limit 5
```


---
*Promise: `<promise>DOCS_WRITER_VERIX_COMPLIANT</promise>`*
