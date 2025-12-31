# Multi-Model Architecture Plan: Codex + Gemini + Claude Integration

## Executive Summary

This document designs how Codex CLI and Gemini CLI integrate with the Context Cascade cognitive architecture, meta-loop, and Ralph Wiggum persistence system.

**Core Philosophy**:
- **Gemini** = Discovery engine (find existing solutions, research, 1M context analysis)
- **Codex** = Execution engine (autonomous coding, debugging, auditing, sandbox experimentation)
- **Claude** = Orchestration brain (complex reasoning, coordination, decision synthesis)
- **LLM Council** = Consensus mechanism (critical decisions requiring multi-perspective validation)

---

## Part 1: Complete Capability Map

### Codex CLI Capabilities

#### Execution Modes

| Mode | Command | Use Case | Risk Level |
|------|---------|----------|------------|
| **Basic Exec** | `codex exec "prompt"` | Non-interactive tasks | Low |
| **Full-Auto** | `codex --full-auto exec "prompt"` | Autonomous iteration | Medium |
| **YOLO** | `codex --yolo exec "prompt"` | Bypass all approvals | High |
| **Sandbox Read-Only** | `codex --sandbox read-only exec "prompt"` | Safe exploration | Very Low |
| **Sandbox Workspace** | `codex --sandbox workspace-write exec "prompt"` | Controlled changes | Low |
| **Sandbox Full** | `codex --sandbox danger-full-access exec "prompt"` | Full access | High |
| **ZDR (Zero Data Retention)** | `codex --zdr exec "prompt"` | HIPAA/GDPR sensitive code | Low (privacy) |
| **JSON Output** | `codex exec --json "prompt"` | Machine-parseable results | Low |

#### Slash Commands (TUI)

| Command | Purpose | Integration Value |
|---------|---------|-------------------|
| `/approvals` | Change approval preset | Dynamic safety adjustment |
| `/compact` | Summarize conversation | Context management |
| `/diff` | Show git diff | Change tracking |
| `/init` | Generate AGENTS.md | Agent scaffolding |
| `/mcp` | List MCP tools | Tool discovery |
| `/mention <path>` | Attach file to context | Targeted analysis |
| `/model` | Switch model | Model routing |
| `/review` | Review working tree | Code review automation |
| `/status` | Config + token usage | Resource monitoring |
| `/undo` | Revert last turn | Safe rollback |

#### Unique Strengths

1. **Long-horizon coding** - Can iterate for extended periods
2. **Sandbox experimentation** - Safe to try risky refactors
3. **Zero Data Retention** - Handles sensitive/proprietary code
4. **Autonomous iteration** - Fix tests until they pass
5. **GPT-5.2-Codex model** - Optimized for agentic coding

---

### Gemini CLI Capabilities

#### Execution Modes

| Mode | Command | Use Case | Strength |
|------|---------|----------|----------|
| **Basic Query** | `gemini "prompt"` | General tasks | Versatile |
| **All-Files** | `gemini --all-files "prompt"` | Codebase analysis | 1M token context |
| **YOLO** | `gemini --yolo "prompt"` | Auto-accept actions | Fast iteration |
| **Sandbox** | `gemini -s "prompt"` | Isolated execution | Safe exploration |
| **JSON Output** | `gemini -o json "prompt"` | Machine-parseable | Automation |

#### Slash Commands

| Command | Purpose | Integration Value |
|---------|---------|-------------------|
| `/model` | Choose Gemini model | Model routing |
| `/tools` | List available tools | Capability discovery |
| `/mcp` | Manage MCP servers | Tool integration |
| `/memory` | Hierarchical memory from GEMINI.md | Context persistence |
| `/directory` | Multi-directory workspace | Cross-project analysis |
| `/restore` | Restore to checkpoint | Safe rollback |
| `/resume` | Resume saved sessions | Long-running tasks |
| `/chat save/resume` | Conversation management | Context preservation |
| `/compress` | Summarize context | Token efficiency |
| `/stats` | Token/session stats | Resource monitoring |
| `/init` | Generate GEMINI.md | Project scaffolding |

#### @ Commands (File Injection)

```text
@README.md Explain this repo
@src/ Summarize all modules
@package.json What dependencies?
```

#### ! Commands (Shell Passthrough)

```text
!git status           # Run shell command
!ls -la               # File listing
!                     # Toggle shell mode
```

#### Custom Slash Commands (TOML)

Location: `~/.gemini/commands/` or `.gemini/commands/`

```toml
# Example: .gemini/commands/review.toml
[command]
name = "review"
description = "Review PR with context"
prompt = """
Review this PR:
!{gh pr view --json title,body,additions,deletions}
!{gh pr diff}
Provide detailed feedback.
"""
```

#### Unique Strengths

1. **1M token context** - Analyze 30K+ lines at once
2. **Google Search grounding** - Real-time current information
3. **70+ extensions** - Figma, Stripe, Shopify, etc.
4. **Custom slash commands** - Reusable workflow macros
5. **Shell embedding** - `!{...}` in prompts

---

## Part 2: Agent vs Skill Determination

### Decision Framework

**SKILL** = Procedural SOP that Claude orchestrates
- Defines WHAT to do and HOW
- Claude remains in control
- Used for standard workflows

**AGENT** = Autonomous entity spawned via Task()
- Executes independently
- Returns results to coordinator
- Used for parallel/specialized work

### Categorization

#### SKILLS (Claude-Orchestrated SOPs)

| Skill Name | Description | Why Skill |
|------------|-------------|-----------|
| `gemini-research` | Research with Google Search grounding | Discovery workflow, Claude synthesizes results |
| `gemini-megacontext` | 1M token codebase analysis | Analysis workflow, Claude interprets findings |
| `codex-sandbox` | Safe experimentation in isolation | Risky operations need Claude oversight |
| `codex-zdr` | Zero Data Retention for sensitive code | Compliance requires Claude tracking |
| `codex-audit` | Code quality/security auditing | Audit results feed Claude decisions |
| `llm-council` | Multi-model consensus | Decision-making process |
| `ralph-multimodel` | Persistence loop with model routing | Orchestration workflow |

#### AGENTS (Autonomous Execution)

| Agent Name | Description | Why Agent |
|------------|-------------|-----------|
| `codex-yolo-agent` | Autonomous coding with no approvals | Fire-and-forget execution |
| `codex-full-auto-agent` | Autonomous iteration until done | Long-running independent work |
| `codex-debugger-agent` | Fix tests until they pass | Self-contained debugging loop |
| `gemini-discovery-agent` | Find existing solutions/patterns | Independent research |
| `gemini-architecture-agent` | Analyze full codebase structure | Large-scale analysis |
| `council-decision-agent` | Run 3-stage consensus | Multi-model coordination |

---

## Part 3: Capability-to-Use-Case Mapping

### Gemini Use Cases (Discovery Engine)

| Use Case | Command/Mode | When to Use |
|----------|--------------|-------------|
| **Find existing solutions** | `gemini "How do others implement X?"` | Before building from scratch |
| **Research best practices** | `gemini "What are current best practices for X?"` | Architecture decisions |
| **Analyze entire codebase** | `gemini --all-files "Map architecture"` | Onboarding, refactoring |
| **Find code patterns** | `gemini --all-files "@src/ Find all API patterns"` | Pattern discovery |
| **Security audit (breadth)** | `gemini --all-files "Find security vulnerabilities"` | Wide-scope scanning |
| **Migration analysis** | `gemini --all-files "Identify Python 2 to 3 issues"` | Change impact assessment |
| **Documentation generation** | `gemini --all-files "Generate API docs"` | Full-context docs |
| **Dependency analysis** | `gemini --all-files "Map all dependencies"` | Dependency graph |

### Codex Use Cases (Execution Engine)

| Use Case | Command/Mode | When to Use |
|----------|--------------|-------------|
| **Fix failing tests** | `codex --full-auto "Fix all failing tests"` | Autonomous test fixing |
| **Implement feature** | `codex --full-auto "Implement X feature"` | Feature development |
| **Debug issue** | `codex --full-auto "Debug and fix X"` | Root cause + fix |
| **Refactor safely** | `codex --sandbox workspace-write "Refactor X"` | Safe experimentation |
| **Risky experiment** | `codex --sandbox read-only "Try X approach"` | Exploration |
| **Code audit** | `codex exec "Audit X for security issues"` | Targeted analysis |
| **HIPAA/GDPR code** | `codex --zdr "Process medical records"` | Sensitive data |
| **Rapid prototyping** | `codex --yolo "Build quick prototype"` | Speed over safety |

### Claude Use Cases (Orchestration Brain)

| Use Case | Role |
|----------|------|
| **Complex reasoning** | Multi-step logic, trade-off analysis |
| **Decision synthesis** | Combine Gemini research + Codex results |
| **Architecture design** | High-level system design |
| **Coordination** | Manage multiple agents/skills |
| **User communication** | Explain results, gather requirements |
| **Quality judgment** | Review agent outputs, validate changes |

### LLM Council Use Cases (Consensus Mechanism)

| Use Case | Threshold | Reason |
|----------|-----------|--------|
| **Architecture decisions** | 0.75 | Multiple valid approaches |
| **Technology selection** | 0.75 | Long-term impact |
| **Security assessment** | 0.80 | High stakes |
| **Breaking changes** | 0.80 | Irreversible impact |
| **Design disagreements** | 0.67 | Need tiebreaker |

---

## Part 4: Meta-Loop Integration

### Current Meta-Loop Architecture

```
META-LOOP (Recursive Improvement Cycle):
    |
    +---> PROPOSE (auditors detect issues)
    |         |
    |         +---> Skill-gap-analyzer
    |         +---> Connascence-analyzer
    |         +---> Quality auditors
    |
    +---> TEST (frozen eval harness)
    |
    +---> COMPARE (baseline vs candidate)
    |
    +---> COMMIT (if improved)
    |
    +---> MONITOR (7-day window)
    |
    +---> ROLLBACK (if regressed)
```

### Enhanced Meta-Loop with Multi-Model

```
ENHANCED META-LOOP v2.0:
    |
    +---> PROPOSE (auditors detect issues)
    |         |
    |         +---> Gemini: Research existing solutions (!NEW!)
    |         +---> Gemini: Analyze codebase impact (--all-files)
    |         +---> Connascence-analyzer: Quality check
    |         +---> Skill-gap-analyzer: Capability check
    |
    +---> IMPLEMENT (!NEW PHASE!)
    |         |
    |         +---> Claude: Design approach (synthesize research)
    |         +---> Codex: Execute implementation (--full-auto)
    |         +---> Codex: Sandbox testing (--sandbox workspace-write)
    |
    +---> DECIDE (!NEW PHASE!)
    |         |
    |         +---> LLM Council: Validate approach (if high-risk)
    |         +---> Threshold check: >= 0.75 to proceed
    |
    +---> TEST (frozen eval harness)
    |         |
    |         +---> Codex: Run tests (--full-auto)
    |         +---> Codex: Fix failures iteratively
    |
    +---> COMPARE (baseline vs candidate)
    |
    +---> COMMIT (if improved)
    |
    +---> MONITOR (7-day window)
    |
    +---> ROLLBACK (if regressed)
```

---

## Part 5: Ralph Wiggum Integration

### Current Ralph Architecture

```
RALPH WIGGUM LOOP:
    |
    +---> Execute task
    |
    +---> Check for <promise>DONE</promise>
    |         |
    |         +---> Found? --> EXIT SUCCESS
    |         +---> Not found? --> CONTINUE
    |
    +---> ITERATION N+1 (until max)
```

### Enhanced Ralph Multi-Model

```
RALPH MULTI-MODEL v2.0:
    |
    +---> PHASE DETECTION
    |         |
    |         +---> Research keywords? --> Route to Gemini
    |         +---> Media/diagram keywords? --> Route to Gemini
    |         +---> Iteration/fix keywords? --> Route to Codex
    |         +---> Decision keywords? --> Route to LLM Council
    |         +---> Default --> Claude
    |
    +---> EXECUTE WITH OPTIMAL MODEL
    |         |
    |         +---> Gemini: Research/discovery tasks
    |         +---> Codex: Implementation/debugging tasks
    |         +---> Claude: Reasoning/coordination tasks
    |         +---> Council: Decision validation
    |
    +---> CHECK COMPLETION PROMISE
    |         |
    |         +---> Found? --> EXIT SUCCESS
    |         +---> Not found? --> CONTINUE
    |
    +---> STORE TO MEMORY-MCP
    |         |
    |         +---> multi-model/gemini/ralph/{iteration}
    |         +---> multi-model/codex/ralph/{iteration}
    |         +---> multi-model/council/ralph/{iteration}
    |
    +---> ITERATION N+1 (until max)
```

### Phase Detection Keywords

| Phase | Detection Keywords | Model |
|-------|-------------------|-------|
| Research | "search", "latest", "documentation", "best practices", "how do others" | Gemini |
| Megacontext | "entire codebase", "all files", "architecture overview", "full analysis" | Gemini --all-files |
| Media | "diagram", "mockup", "image", "video", "visualization" | Gemini (Imagen/Veo) |
| Autonomous | "fix tests", "debug", "iterate", "prototype", "implement" | Codex --full-auto |
| Sandbox | "experiment", "try", "risky", "refactor safely" | Codex --sandbox |
| Decision | "decide", "choose", "architecture decision", "which approach" | LLM Council |
| Reasoning | Default | Claude |

---

## Part 6: New Skills to Create

### Skill: `multi-model-discovery`

```yaml
name: multi-model-discovery
description: Use Gemini to find existing solutions before implementation
trigger_keywords: ["find existing", "how do others", "best practices", "don't reinvent"]
workflow:
  1. Gemini: Search for existing solutions
  2. Gemini: Find code examples/patterns
  3. Claude: Synthesize findings
  4. Decision: Build from scratch vs adapt existing
output: { existing_solutions, recommended_approach, adaptation_plan }
```

### Skill: `codex-iterative-fix`

```yaml
name: codex-iterative-fix
description: Use Codex to fix issues until tests pass
trigger_keywords: ["fix all tests", "make tests pass", "debug until working"]
workflow:
  1. Codex: Run tests, identify failures
  2. Codex: Fix failures iteratively (--full-auto)
  3. Codex: Verify all pass
  4. Claude: Review changes, summarize
output: { tests_passed, changes_made, summary }
```

### Skill: `codex-safe-experiment`

```yaml
name: codex-safe-experiment
description: Try risky changes in Codex sandbox
trigger_keywords: ["experiment", "try approach", "risky refactor"]
workflow:
  1. Codex: Clone to sandbox (--sandbox read-only)
  2. Codex: Implement experiment
  3. Codex: Run tests in sandbox
  4. Decision: Apply to real codebase?
  5. If yes: Codex applies changes (--sandbox workspace-write)
output: { experiment_results, recommendation, applied }
```

### Skill: `gemini-codebase-onboard`

```yaml
name: gemini-codebase-onboard
description: Use Gemini 1M context to understand entire codebase
trigger_keywords: ["understand codebase", "onboard", "explain architecture"]
workflow:
  1. Gemini: Load all files (--all-files)
  2. Gemini: Generate architecture map
  3. Gemini: Identify key patterns
  4. Gemini: Document component interactions
  5. Claude: Create onboarding guide
output: { architecture_map, key_patterns, onboarding_guide }
```

### Skill: `council-critical-decision`

```yaml
name: council-critical-decision
description: Use LLM Council for high-stakes decisions
trigger_keywords: ["critical decision", "need consensus", "high stakes"]
workflow:
  1. Claude: Frame the decision
  2. Council: Collect perspectives (Claude, Gemini, Codex)
  3. Council: Cross-review (anonymized)
  4. Council: Synthesize consensus
  5. Claude: Present decision with rationale
threshold: 0.75 (configurable)
output: { decision, consensus_score, perspectives, rationale }
```

---

## Part 7: New Agents to Create

### Agent: `gemini-discovery-agent`

```yaml
name: gemini-discovery-agent
type: research
description: Find existing solutions and code patterns
tools: Read, WebFetch, Bash (gemini commands)
model: sonnet
workflow:
  - Search for existing implementations
  - Find code examples on GitHub
  - Analyze patterns and approaches
  - Return synthesis of findings
memory_namespace: agents/research/gemini-discovery/{project}/{timestamp}
```

### Agent: `codex-autonomous-agent`

```yaml
name: codex-autonomous-agent
type: execution
description: Execute coding tasks autonomously
tools: Read, Write, Edit, Bash (codex commands)
model: sonnet
workflow:
  - Invoke Codex with task
  - Monitor for completion
  - Capture results and changes
  - Return summary to coordinator
memory_namespace: agents/execution/codex-autonomous/{project}/{timestamp}
```

### Agent: `codex-sandbox-agent`

```yaml
name: codex-sandbox-agent
type: experimentation
description: Run risky experiments in isolated sandbox
tools: Read, Bash (codex sandbox commands)
model: sonnet
workflow:
  - Set up sandbox environment
  - Execute experiment
  - Capture results
  - Return recommendation
memory_namespace: agents/experimentation/codex-sandbox/{project}/{timestamp}
```

---

## Part 8: Integration Architecture Diagram

```
+------------------------------------------------------------------+
|                    CONTEXT CASCADE v3.2                           |
+------------------------------------------------------------------+
|                                                                   |
|  +-------------------+    +-------------------+                   |
|  |   USER REQUEST    |    |   5-PHASE HOOK    |                   |
|  +--------+----------+    +--------+----------+                   |
|           |                        |                              |
|           v                        v                              |
|  +-------------------------------------------+                    |
|  |          PHASE 1: INTENT ANALYZER         |                    |
|  +-------------------------------------------+                    |
|           |                                                       |
|           v                                                       |
|  +-------------------------------------------+                    |
|  |    PHASE 2: MODEL ROUTER (NEW)            |                    |
|  |                                           |                    |
|  |  Keywords --> Model Selection:            |                    |
|  |  - research/find --> Gemini               |                    |
|  |  - implement/fix --> Codex                |                    |
|  |  - decide/choose --> Council              |                    |
|  |  - default --> Claude                     |                    |
|  +-------------------------------------------+                    |
|           |                                                       |
|           +-------------+-------------+-------------+             |
|           |             |             |             |             |
|           v             v             v             v             |
|  +----------+   +----------+   +----------+   +----------+        |
|  | GEMINI   |   | CODEX    |   | COUNCIL  |   | CLAUDE   |        |
|  | (Disc.)  |   | (Exec.)  |   | (Decide) |   | (Orch.)  |        |
|  +----------+   +----------+   +----------+   +----------+        |
|       |             |             |             |                 |
|       v             v             v             v                 |
|  +-------------------------------------------+                    |
|  |          RESULTS SYNTHESIZER              |                    |
|  |          (Claude Coordination)            |                    |
|  +-------------------------------------------+                    |
|           |                                                       |
|           v                                                       |
|  +-------------------------------------------+                    |
|  |          MEMORY-MCP STORAGE               |                    |
|  |                                           |                    |
|  |  multi-model/gemini/{type}/{id}           |                    |
|  |  multi-model/codex/{type}/{id}            |                    |
|  |  multi-model/council/{type}/{id}          |                    |
|  +-------------------------------------------+                    |
|           |                                                       |
|           v                                                       |
|  +-------------------------------------------+                    |
|  |          META-LOOP INTEGRATION            |                    |
|  |                                           |                    |
|  |  PROPOSE --> IMPLEMENT --> DECIDE -->     |                    |
|  |  TEST --> COMPARE --> COMMIT --> MONITOR  |                    |
|  +-------------------------------------------+                    |
|                                                                   |
+------------------------------------------------------------------+
```

---

## Part 9: Implementation Priority

### Phase 1: Core Infrastructure (Week 1)

1. [x] `delegate.sh` wrapper (DONE)
2. [x] CLAUDE.md invocation rules (DONE)
3. [x] `MULTI-MODEL-INVOCATION-GUIDE.md` (DONE)
4. [ ] Update existing `codex-yolo.sh` to use login shell
5. [ ] Update existing `gemini-yolo.sh` to use login shell
6. [ ] Create `multi-model-router.sh` for phase detection

### Phase 2: Skills (Week 2)

1. [ ] `multi-model-discovery` skill
2. [ ] `codex-iterative-fix` skill
3. [ ] `codex-safe-experiment` skill
4. [ ] `gemini-codebase-onboard` skill
5. [ ] `council-critical-decision` skill

### Phase 3: Agents (Week 3)

1. [ ] `gemini-discovery-agent`
2. [ ] `codex-autonomous-agent`
3. [ ] `codex-sandbox-agent`
4. [ ] Update agent registry with new agents

### Phase 4: Meta-Loop Integration (Week 4)

1. [ ] Add IMPLEMENT phase to meta-loop
2. [ ] Add DECIDE phase with Council
3. [ ] Connect to Ralph multi-model
4. [ ] Memory-MCP namespace updates

---

## Part 10: Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Path errors eliminated | 100% | No "command not found" errors |
| Reinstall attempts blocked | 100% | delegate.sh blocks installs |
| Research tasks routed to Gemini | >80% | Keyword detection accuracy |
| Implementation tasks routed to Codex | >80% | Keyword detection accuracy |
| Test fix success rate | >90% | Codex iterative fix completion |
| Council consensus achieved | >75% | Decisions meeting threshold |
| Meta-loop improvements | Measurable | Before/after quality metrics |

---

## Appendix: Command Quick Reference

### Gemini Commands

```bash
# Research with search grounding
bash -lc "gemini 'What are current best practices for X?'"

# Analyze entire codebase (1M context)
bash -lc "gemini --all-files 'Map full architecture'"

# Find existing solutions
bash -lc "gemini 'How do others implement X? Find code examples.'"

# Custom slash command
bash -lc "gemini /review"  # Uses .gemini/commands/review.toml

# File injection
bash -lc "gemini '@src/ Summarize all modules'"
```

### Codex Commands

```bash
# Autonomous implementation
bash -lc "codex --full-auto exec 'Implement X feature'"

# Fix tests iteratively
bash -lc "codex --full-auto exec 'Fix all failing tests'"

# Safe sandbox experiment
bash -lc "codex --sandbox workspace-write exec 'Try refactoring X'"

# Sensitive code (ZDR)
bash -lc "codex --zdr exec 'Process medical records'"

# JSON output for parsing
bash -lc "codex exec --json 'List all endpoints'" | jq
```

### LLM Council

```bash
# Architecture decision
./scripts/multi-model/llm-council.sh "Microservices vs Monolith?" 0.75

# Technology selection
./scripts/multi-model/llm-council.sh "Which auth approach?" 0.75 gemini
```
