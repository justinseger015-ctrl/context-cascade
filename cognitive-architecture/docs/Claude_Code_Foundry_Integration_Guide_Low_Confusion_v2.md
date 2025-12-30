# Claude Code Foundry Integration Guide (Low‑Confusion)
## Integrating Foundry Skills into a multi‑agent / multi‑model / multi‑skill VERILINGUA×VERIX×DSPy×GlobalMOO system

**Audience:** engineers implementing a Claude Code–style agent workspace

**Goal:** make Foundry (self‑improvement) powerful **without** letting it leak complexity into day‑to‑day runtime.

---

## 0) The one mental model that prevents 90% of confusion

You are running **two lanes** in one repo:

1) **Runtime Lane (Production)** — serve user tasks reliably.
2) **Foundry Lane (Improvement)** — generate changes to prompts/agents/skills *offline*, run them through the frozen eval harness, and only then promote.

If you keep these lanes separate, you can scale to multi‑agent/multi‑model/multi‑skill without the system becoming a recursive mess.

### The two thin‑waist contracts (do not break)

1) **Prompt contract**
   - `PromptBuilder.build(task, task_type) -> (system_prompt, user_prompt)`

2) **Optimization contract**
   - `evaluate(config_vector) -> outcomes_vector`

Everything else (agents, skills, Foundry, models, routing rules) can evolve as long as these stay stable.

---

## 1) Runtime Lane (Production): the boring 3‑agent graph

Keep runtime orchestration minimal and deterministic:

```
            ┌──────────────┐
TaskSpec ──>│ Router Agent  │  selects: mode + model + allowed skills
            └──────┬───────┘
                   │
                   v
            ┌──────────────┐
            │ Executor      │  runs PromptBuilder (and DSPy‑compiled prompt)
            └──────┬───────┘
                   │
                   v
            ┌──────────────┐
            │ Critic/Grader │  parses VERIX + checks frame markers + (optional) rubric judge
            └──────────────┘
```

**Rule:** if you want “more experts,” implement them as **skills** (callable tools) rather than more autonomous agents.

---

## 2) Foundry Lane (Improvement): what the Foundry Skills *are*

Foundry is a set of *meta‑skills* that operate on artifacts:

| Foundry Skill | Input Artifact | Output Artifact |
|---|---|---|
| **Prompt Architect** | user prompt (what the user types) | improved user prompt |
| **Prompt Forge** | system prompt (agent instructions) | improved system prompt + rationale |
| **Agent Creator** | agent requirements/spec | new agent system prompt (+metadata) |
| **Skill Forge** | skill requirements/spec | new `SKILL.md` (+tests + docs) |

### Decision rule (single router for Foundry)

When someone asks “improve/create something,” classify the target:

- **User prompt?** → Prompt Architect
- **System prompt?**
  - existing agent? → Prompt Forge
  - new agent? → Agent Creator
- **Reusable workflow/skill?** → Skill Forge

**Low‑confusion boundary:** Foundry tools should never run implicitly during normal `/eval` or task execution.

---

## 3) The Meta Loop: safe recursive improvement without runaway recursion

### The invariant: the Eval Harness is frozen

- The eval harness is **not allowed** to self‑modify.
- It is the only authority that can ACCEPT / REJECT changes.

### Meta Loop flow (recommended)

```
         (Foundry Lane)

     Prompt Forge ──────┐
        │               │
        v               │  (improves skill prompts)
     Skill Forge ───────┤
        │               │  (creates/improves skills)
        v               │
     Agent Creator ─────┘
        │
        v
   Auditor set (prompt/skill/expertise/output)
        │
        v
  ┌───────────────────────┐
  │  EVAL HARNESS (FROZEN) │
  └───────────┬───────────┘
              │
        ACCEPT│REJECT
              │
            COMMIT
              │
        MONITOR (7 days)
```

### The “no silent promotion” rule

- Foundry outputs **proposals** and **diffs**.
- Only the eval harness can mark them as promotable.

---

### 3.1 Ralph Wiggum hook loop (anti‑production‑theater)

**Ralph Wiggum** is a Claude Code *hook loop* that prevents “looks done” outputs by **blocking process exit** until explicit completion criteria are met.

**Mechanism (how it actually runs):**
- A single state file is created/updated at: `~/.claude/ralph-wiggum/loop-state.md`
- The state tracks: `session_id`, `iteration`, `max_iterations`, `completion_promise`, `active`, plus the current prompt text.
- When Claude attempts to stop, a **Stop hook** intercepts:
  - If `active: true` and the promise + quality gates are **not** satisfied → return **exit code 2**, re‑inject the prompt, increment `iteration`.
  - If satisfied → return **exit code 0**, deactivate the loop, allow normal exit.

**Non‑negotiable constraints (keep it simple):**
- **Sequential only.** One active loop at a time (one state file).
- **No nested loops.** Parallelism happens *inside* the loop via Task agents, not by spinning multiple Ralph loops.

> Design intent: Ralph is a “truth serum” for the Foundry Lane—if the criteria aren’t met, the run literally cannot end.

---

### 3.2 Correct Meta Loop flow (sequential Ralph phases)

Each phase is a **separate Ralph run** with a different `completion_promise`.

1) **PHASE 1: EXECUTE**  
   Promise: `{FOUNDRY}_PROPOSAL_READY`  
   Output: proposal(s) + diff plan (no file writes yet)

2) **PHASE 2: IMPLEMENT**  
   Promise: `CHANGES_APPLIED`  
   Output: apply diffs to target paths + update artifact envelope(s)

3) **PHASE 3: AUDIT**  
   Promise: `ALL_AUDITS_PASS`  
   Inside the single Ralph loop: spawn **4 parallel Task agents** (prompt / skill / expertise / output).  
   Only emit the promise if **all 4** return PASS with evidence.

4) **PHASE 4: EVAL**  
   Promise: `EVAL_HARNESS_PASS`  
   Output: frozen harness results + comparison vs baseline

Then: **COMPARE → COMMIT → MONITOR (7 days)**

---

### 3.3 The meta‑loop driver script interface

Recommended operator surface (bash only; no magic):

```bash
# Start the meta loop (sequential Ralph phases)
bash scripts/meta-loop/meta-loop-setup.sh start   "Add cognitive frames"   --target "skills/foundry/skill-forge/SKILL.md"   --foundry "prompt-forge"

# Check status
bash scripts/meta-loop/meta-loop-setup.sh status

# Advance to next phase
bash scripts/meta-loop/meta-loop-setup.sh next-phase

# Cancel
bash scripts/meta-loop/meta-loop-setup.sh cancel
```

---

### 3.4 Promise tokens: make them parsable, unambiguous, and grep‑friendly

Use a single line token that your hook can detect reliably:

- `PROMISE: FOUNDRY_PROPOSAL_READY`
- `PROMISE: CHANGES_APPLIED`
- `PROMISE: ALL_AUDITS_PASS`
- `PROMISE: EVAL_HARNESS_PASS`

**Rules:**
- Emit the promise **only once** and only at the end.
- Never “speculate” a promise (“should pass”)—either the gate is satisfied or it isn’t.
- In AUDIT phase, require an aggregator summary that lists each auditor result before the promise.

---

### 3.5 Where Ralph belongs

- **Use Ralph only in the Foundry Lane** (changes to prompts/agents/skills).  
- **Do not** wrap normal runtime requests in Ralph; runtime should fail fast, log, and defer improvements to the Foundry lane.

---

## 4) How to represent artifacts so Claude Code doesn’t get lost

Use **four artifact types** with a uniform envelope:

1) `USER_PROMPT` (Prompt Architect)
2) `SYSTEM_PROMPT` (Prompt Forge)
3) `AGENT_SPEC` / `AGENT_PROMPT` (Agent Creator)
4) `SKILL_SPEC` / `SKILL_MD` (Skill Forge)

### Standard envelope (every Foundry tool reads/writes this)

```json
{
  "id": "2025-12-28T12-34-56Z__short_slug",
  "artifact_type": "SYSTEM_PROMPT",
  "target_path": ".claude/agents/research/system.md",
  "summary": "One sentence describing what changed and why",
  "inputs": {"...": "..."},
  "outputs": {"...": "..."},
  "risks": ["what could go wrong"],
  "tests_to_run": ["eval:holdout", "lint", "unit:parser"],
  "requires_eval": true
}
```

**Reason:** Claude Code thrives when every tool returns a predictable structure.

---

## 5) Multi‑model policy for Foundry (so it’s cheap and stable)

### Default policy

- **Drafting / brainstorming:** cheaper model.
- **Final proposal text:** mid model.
- **Eval harness runs:** pinned “judge model(s)” + deterministic checks.

### Why

- Your optimization/eval workflow already assumes you log model + version and pin for reproducibility.
- DSPy explicitly supports compiling with a cheaper model and deploying with a better one; the same idea applies to Foundry.

---

## 6) Cognitive frames: keep them as toggles, not theory

Foundry can *select* frames (aspectual/evidential/morphological/etc.), but runtime code should treat frames as:

- **named toggles** (on/off)
- **activation templates** (how to instruct the model)
- **compliance checks** (did the output follow the markers)

Keep the deep constructed‑language theory docs out of runtime.

---

## 7) Quality gates (unified)

### Minimum accept criteria for any Foundry proposal

- **No CRITICAL issues** in adversarial/edge tests
- **Format compliance** (VERIX + frame markers) does not regress
- **Holdout regression suite** does not regress
- **Token/latency budget** not blown for the targeted mode

### Anti‑gaming

- Normalize for length.
- Treat “format compliance” as a sub‑metric, not the whole score.

---

## 8) Mandatory Claude Code completion pattern (prevents dangling work)

After any Foundry invocation, output a single “completion” message containing:

- 2–4 `Task(...)` items (work units you created)
- `TodoWrite({ todos: [...] })` with 5–10 concrete steps

This makes the system auditable and prevents Claude Code from “thinking it finished” without producing the operational next steps.

---

## 9) Memory namespaces (so logs don’t collide)

Use these **top‑level namespaces**:

```
foundry/
  prompt-architect/
  prompt-forge/
  agent-creator/
  skill-forge/

improvement/
  audits/
```

Within each, store:

- `proposals/` (human‑readable)
- `diffs/` (machine‑apply)
- `metrics/` (what changed + measured deltas)
- `generations/` (raw outputs for debugging)

---

## 10) Repo layout (drop‑in)

Add a clean separation between runtime and foundry:

```
.claude/
  agents/
  skills/
  expertise/
  foundry/
    playbooks/
    proposals/
    diffs/
    runs/
core/
  prompt_builder.py
  runtime.py
  verix.py
  verilingua.py
  config.py

eval/
  harness/          # FROZEN
  metrics.py
  graders/
  edge_cases.py

optimization/
  globalmoo_client.py
  dspy_level2.py
  dspy_level1.py
  cascade.py

storage/
  logs/
  prompts/
  results/
```

**Key idea:** Foundry outputs land in `.claude/foundry/…` until accepted.

---

## 11) Commands (keep tiny)

### Runtime commands (from the main integration manual)

- `/mode <audit|speed|math|research|synthesis|auto>`
- `/eval <task_type> [--mode X]`

### Improvement commands (recommended minimal additions)

- `/foundry <architect|forge|agent|skill> <target>`
- `/meta-loop <iters N> [--scope prompts|skills|agents]`

**Rule:** `/meta-loop` always runs in an “offline job” context, never in a production session.

---

## 12) The simplest way to wire Foundry into the existing VERILINGUA×VERIX loop

### Runtime produces logs
- config vector
- prompt hash
- response
- tokens/latency
- compliance + outcome metrics

### Optimization uses logs
- DSPy Level 2 optimizes prompt expression per cluster
- GlobalMOO explores config vectors and distills “modes”

### Foundry uses the same logs, but targets *artifacts*
- Prompt Architect targets user prompts
- Prompt Forge targets system prompts
- Skill Forge targets skills
- Agent Creator targets agents

Everything ends at the frozen eval harness.

---

## 13) Practical defaults (copy/paste)

### Default mode policy
- default mode: `auto`
- max frames per task: 3
- VERIX strictness: 1 (tight enough to audit, not so strict it breaks casual use)

### Default Foundry policy
- Foundry tools only run when explicitly invoked
- They must output a proposal envelope + a diff
- They must name tests to run

---

## 14) What to do next (2‑hour setup)

1) Add the repo layout folders above.
2) Implement the artifact envelope JSON format for Foundry proposals.
3) Add `/foundry` and `/meta-loop` commands to your Claude Code command surface.
4) Create `eval/harness/` and treat it as frozen (protected path).
5) Wire Foundry tools to write only into `.claude/foundry/…`.


---

## Appendix A) Foundry Phase 0: expertise loading (prevents dumb mistakes)

Before any Foundry tool does real work:

1) Detect domain (e.g., “python skill”, “agent prompt”, “eval harness”, “docs”).
2) Look for: `.claude/expertise/{domain}.yaml`
3) If present, load:
   - conventions / do‑and‑don’t
   - known failure modes
   - required tests
   - style rules
4) If absent, mark **DISCOVERY MODE** and require:
   - explicit assumptions list
   - extra eval cases

**Why this helps:** it keeps Foundry from re‑learning the same lessons every run.

---

## Appendix B) Foundry cognitive frames as a tiny switchboard (not a philosophy seminar)

Treat frames as **execution strategies** for Foundry tools:

| Frame | Use when | What it enforces |
|---|---|---|
| **Aspectual** (completion tracking) | multi‑phase migrations, checklists, refactors | finish‑state definition + “done” criteria |
| **Evidential** (source verification) | anything touching evals, metrics, claims | cite sources + state uncertainty |
| **Hierarchical** (audience calibration) | onboarding docs, handoff, CLAUDE.md | tuned verbosity + “what to do next” |
| **Morphological** (semantic decomposition) | conlang/VERILINGUA expansions, notation design | break meanings into parts before redesign |
| **Classifier** (object comparison) | model choice, tool choice, config choice | compare options with stable attributes |

**Runtime note:** you can keep these frames *available* in the registry, but cap the number activated per task.

---

## Appendix C) The unified quality gates (how Foundry outputs become deployable)

The “one true gate” is the frozen eval harness.

Recommended mapping:

1) **COV / confidence gate**
   - Require explicit “what I changed” + “what could break” + “tests to run”.

2) **Adversarial / edge gate**
   - No CRITICAL issues.
   - Add at least one new edge case if the change fixes a failure mode.

3) **Documentation audit gate**
   - Tier 1–2: must be complete.
   - Tier 3–4: should be strong enough for onboarding.

4) **Eval harness gate (authoritative)**
   - Must pass benchmarks and holdout regression suite.

---

## Appendix D) Cross‑skill coordination (how the Foundry tools feed each other)

| Skill | Uses | Improved by | Improves |
|---|---|---|---|
| **Prompt Architect** | user prompts | Prompt Forge / Skill Forge | user prompts |
| **Prompt Forge** | system prompts, eval harness feedback | Skill Forge | Skill Forge / Agent Creator |
| **Agent Creator** | cognitive frames, eval harness, memory | Skill Forge / Prompt Forge | creates agents |
| **Skill Forge** | cognitive frames, Prompt Forge, eval harness | Prompt Forge | all skills (including itself) |

Low‑confusion rule: treat this as a **directed graph**, not an invitation to “improve everything at once.”

---

## Appendix E) Minimal CLAUDE.md add‑on (Foundry section)

Paste this under your existing commands:

```md
## Foundry (offline only)
- /foundry architect <target>         # Prompt Architect: optimize user prompts
- /foundry forge <target>             # Prompt Forge: improve system prompts
- /foundry agent <spec>               # Agent Creator: generate new agent spec/prompt
- /foundry skill <spec>               # Skill Forge: generate new SKILL.md

## Meta Loop (Ralph Wiggum, sequential phases)
- /ralph-loop <completion_promise>    # starts a single guarded loop (one active at a time)
- bash scripts/meta-loop/meta-loop-setup.sh start "<goal>" --target "<path>" --foundry "<tool>"
- bash scripts/meta-loop/meta-loop-setup.sh status
- bash scripts/meta-loop/meta-loop-setup.sh next-phase
- bash scripts/meta-loop/meta-loop-setup.sh cancel

- /foundry skill <target>
- /meta-loop <iters N>

Rules:
- Foundry writes only to .claude/foundry/…
- Promotion requires eval/harness approval.
- Eval harness is frozen and never edited by Foundry.
```
