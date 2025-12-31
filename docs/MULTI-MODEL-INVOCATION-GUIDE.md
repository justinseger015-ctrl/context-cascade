# Multi-Model Invocation Guide

## CRITICAL: How Claude Code Should Invoke Codex and Gemini CLIs

This guide solves the PATH mismatch problem where Claude Code runs in a non-interactive shell that cannot find your installed binaries.

---

## The Core Problem

Claude Code runs commands in a **non-interactive/non-login shell** with a different PATH than your terminal. This causes:
- Binary not found errors for `codex` and `gemini`
- Claude "helpfully" trying to reinstall them
- Chasing file paths instead of using the command name

## The Solution

1. **ALWAYS use login shell**: `bash -lc "<command>"`
2. **NEVER install or upgrade** - binaries are already installed
3. **Hard-check before invoking** - verify binary exists first
4. **Use the delegate.sh wrapper** for reliable execution

---

## Installed CLIs

| CLI | Version | Location | Install Method |
|-----|---------|----------|----------------|
| Codex | 0.66.0 | `/c/Users/17175/AppData/Roaming/npm/codex` | npm global |
| Gemini | 0.20.2 | `/c/Users/17175/AppData/Roaming/npm/gemini` | npm global |

---

## MANDATORY Rules for Claude

```text
WHEN DELEGATING TO CODEX CLI OR GEMINI CLI:

1. NEVER install or upgrade codex or gemini. They are ALREADY INSTALLED.

2. ALWAYS run preflight checks FIRST:
   bash -lc "command -v codex && codex --version"
   bash -lc "command -v gemini && gemini --version"

3. If preflight FAILS, STOP and report:
   "Binary not on PATH in tool environment"
   Include: bash -lc "echo $PATH"
   DO NOT attempt to install.

4. When invoking, ALWAYS use login shell:
   bash -lc "codex exec 'your prompt here'"
   bash -lc "gemini 'your prompt here'"

5. Use PLAIN command names (codex, gemini), NOT file paths.

6. After success, summarize:
   - What command was run
   - What changed (files, diff summary)
   - Test results if applicable
```

---

## Using delegate.sh Wrapper (Recommended)

The `delegate.sh` wrapper at `scripts/multi-model/delegate.sh` handles all the edge cases:

### Codex Examples

```bash
# Fix tests autonomously
./scripts/multi-model/delegate.sh codex "Fix all failing tests" --full-auto

# Get JSON output for parsing
./scripts/multi-model/delegate.sh codex "List all API endpoints" --json

# Use specific model
./scripts/multi-model/delegate.sh codex "Optimize this code" --model gpt-5.2-codex

# YOLO mode (bypass all approvals)
./scripts/multi-model/delegate.sh codex "Refactor auth system" --yolo
```

### Gemini Examples

```bash
# Research with Google Search grounding
./scripts/multi-model/delegate.sh gemini "What are React 19 best practices?"

# Analyze entire codebase (1M token context)
./scripts/multi-model/delegate.sh gemini "Map the full architecture" --all-files

# Custom directory
./scripts/multi-model/delegate.sh gemini "Review this code" --cwd /path/to/project
```

---

## Direct Invocation (Without Wrapper)

### Codex CLI Commands

```bash
# Non-interactive (for scripting/CI)
bash -lc "codex exec 'your task here'"

# With JSON output
bash -lc "codex exec --json 'your task here'"

# Full-auto mode (autonomous)
bash -lc "codex --full-auto exec 'your task here'"

# YOLO mode (bypass approvals + sandbox)
bash -lc "codex --yolo exec 'your task here'"

# With specific model
bash -lc "codex --model gpt-5.2-codex exec 'your task here'"
```

### Gemini CLI Commands

```bash
# Basic query
bash -lc "gemini 'your query here'"

# Analyze entire codebase
bash -lc "gemini --all-files 'analyze architecture'"

# JSON output
bash -lc "gemini -o json 'your query here'"

# With sandbox mode
bash -lc "gemini -s 'your query here'"
```

---

## Codex CLI Reference

### Terminal Flags

| Flag | Description |
|------|-------------|
| `--model NAME` | Set model (e.g., gpt-5.2-codex) |
| `--yolo` | Bypass approvals and sandbox |
| `--full-auto` | Autonomous mode with workspace write |
| `exec "PROMPT"` | Non-interactive execution |
| `exec --json "PROMPT"` | JSON output (JSONL events) |
| `--sandbox MODE` | read-only, workspace-write, danger-full-access |
| `--zdr` | Zero Data Retention (for sensitive code) |
| `--max-iterations N` | Limit iteration count |

### Codex Slash Commands (Inside TUI)

| Command | Description |
|---------|-------------|
| `/approvals` | Change approval preset |
| `/compact` | Summarize conversation |
| `/diff` | Show git diff |
| `/exit` or `/quit` | Exit |
| `/init` | Generate AGENTS.md scaffold |
| `/mcp` | List MCP tools |
| `/mention <path>` | Attach file to conversation |
| `/model` | Choose model |
| `/new` | New conversation |
| `/review` | Review working tree |
| `/status` | Show config + token usage |
| `/undo` | Revert last turn |

---

## Gemini CLI Reference

### Terminal Flags

| Flag | Description |
|------|-------------|
| `--all-files` | Load entire codebase (1M token context) |
| `-o json` | JSON output |
| `-s` | Sandbox mode |
| `--yolo` | Auto-accept all actions |

### Gemini Slash Commands (Inside CLI)

| Command | Description |
|---------|-------------|
| `/help` or `/?` | Help |
| `/model` | Choose Gemini model |
| `/tools` | List available tools |
| `/mcp` | Manage MCP servers |
| `/memory` | Manage hierarchical memory |
| `/directory` or `/dir` | Multi-directory workspace |
| `/restore` | Restore files to checkpoint |
| `/resume` | Resume saved session |
| `/chat` | Save/resume/list conversations |
| `/compress` | Replace context with summary |
| `/stats` | Token/session stats |
| `/init` | Generate GEMINI.md |
| `/quit` or `/exit` | Exit |

### Gemini @ Commands (File Injection)

```text
@README.md Explain what this repo does.
@src/ Summarize the key modules.
What does this file do? @package.json
```

### Gemini ! Commands (Shell Passthrough)

```text
!git status           # Run shell command
!ls -la               # Another command
!                     # Toggle shell mode (everything becomes shell)
```

---

## Model Strengths Matrix

| Task Type | Best Model | Why |
|-----------|------------|-----|
| Research (current info) | Gemini | Google Search grounding |
| Large codebase analysis | Gemini | 1M token context |
| Complex reasoning | Claude | Better at multi-step |
| Autonomous iteration | Codex | Full-auto/YOLO modes |
| Test fixing loops | Codex | Fast iteration |
| Critical decisions | LLM Council | Multi-model consensus |
| Implementation | Claude/Codex | Both good |
| Security audit | Claude | More thorough |

---

## Pipeline Patterns

### Pattern 1: Claude Orchestrates, Codex Executes

```text
1. Claude: Define scope, acceptance tests, rollback strategy
2. Codex: Make changes, run tests, iterate (--full-auto)
3. Claude: Review diff, validate, write summary
```

### Pattern 2: Gemini Research, Claude Implements

```text
1. Gemini: Research best practices (Google Search grounding)
2. Claude: Design architecture based on research
3. Claude: Implement solution
4. Gemini: Analyze entire codebase for impact (--all-files)
```

### Pattern 3: LLM Council for Critical Decisions

```text
1. Claude: Write plan + risks
2. Gemini: Check for missing steps
3. Codex: Propose alternative approaches
4. Council: Synthesize consensus answer
5. Claude: Execute chosen approach
```

---

## Troubleshooting

### "codex: command not found"

```bash
# Check login shell PATH
bash -lc "echo \$PATH | tr ':' '\n' | grep npm"
bash -lc "command -v codex"

# Verify installation
bash -lc "npm list -g @openai/codex"
```

### "gemini: command not found"

```bash
# Check login shell PATH
bash -lc "echo \$PATH | tr ':' '\n' | grep npm"
bash -lc "command -v gemini"

# Verify installation
bash -lc "npm list -g @google/gemini-cli"
```

### Claude keeps trying to install

Add to CLAUDE.md or system prompt:
```text
CRITICAL: codex and gemini CLIs are ALREADY INSTALLED.
NEVER run npm install, brew install, or any install commands.
Use: bash -lc "codex ..." or bash -lc "gemini ..."
```

---

## Memory Integration

All delegate.sh runs store results at:
```
~/.delegate-logs/{mode}_{timestamp}_{id}.stdout
~/.delegate-logs/{mode}_{timestamp}_{id}.stderr
~/.delegate-logs/{mode}_{timestamp}_{id}.meta.json
```

Memory-MCP keys:
- Codex: `multi-model/codex/yolo/{task_id}`
- Gemini: `multi-model/gemini/yolo/{task_id}`
- Council: `multi-model/council/decisions/{query_id}`
