# Claude Code Integration Playbook (Low‑Confusion Edition)
## VERILINGUA × VERIX × DSPy × GlobalMOO inside a multi‑agent / multi‑model / multi‑skill system

**Audience:** engineers implementing a Claude Code–style agent workspace
**Goal:** make the system *easy to integrate* and *hard to misuse*.

This playbook assumes you already have (or will adopt) the core architecture described in the existing integration manual: VERILINGUA frames + VERIX notation as the prompt layer; DSPy as per‑cluster prompt expression optimizer; GlobalMOO as the outer multi‑objective optimizer; and a closed feedback loop from runtime logs → optimization → mode updates.

---

## 0) 10‑minute mental model (thin waist)

You are building an **agent platform** with a **thin waist**:

### The only two contracts that must never change
1) **Prompt contract:** `PromptBuilder.build(task, task_type) -> (system, user)`
2) **Optimization contract:** `evaluate(config_vector) -> outcomes_vector`

Everything else (agents, skills, models, routing rules, UI) can evolve as long as those two stay stable.

### Why this is low‑confusion
- Agents and skills can churn without breaking optimization.
- Models can swap without rewriting prompts.
- Optimization can run offline without touching runtime.

---

## 1) System shape (MECE)

Your platform has five MECE planes:

1) **Orchestration plane** — agent graph + control flow
2) **Model plane** — multi‑model selection + fallbacks
3) **Skill plane** — callable tools and reusable “skills”
4) **Prompt plane** — VERILINGUA + VERIX + DSPy‑compiled expression
5) **Learning plane** — evaluation + GlobalMOO + governance cadence

The existing guide already specifies a reference layout that cleanly separates these concerns (core/eval/optimization/modes/claude_integration).

---

## 2) Core data objects (copy‑paste schema)

### 2.1 TaskSpec (what the router sees)
```json
{
  "task_id": "uuid",
  "task_type": "audit|speed|math|research|synthesis|other",
  "input": "string or structured payload",
  "constraints": {
    "hard": ["must cite sources", "must output JSON", "must be < 200 tokens"],
    "soft": ["prefer concise", "prefer bullet list"]
  },
  "risk": "low|medium|high",
  "mode_hint": "auto|audit|speed|math|research|synthesis",
  "model_hint": "auto|claude|gpt|gemini|..."
}
```

### 2.2 RunConfig (what the prompt layer needs)
RunConfig is just the **vector‑decoded config** plus some execution metadata.

- `FullConfig` dataclasses and a stable vector mapping are explicitly recommended.
- Keep mapping stable and versioned (VectorCodec pattern).

### 2.3 EvalOutcome (what learning consumes)
Use a compact outcomes vector (≈10–14 dimensions) to avoid slow learning and overfitting.

The GlobalMOO guide’s example 11‑dim outcome codec is a solid default.

---

## 3) Orchestration plane: multi‑agent without chaos

### 3.1 Recommended agent graph (3 roles, fixed interfaces)
Keep the agent graph boring. Complexity lives in configs and skills.

```
            ┌──────────────┐
TaskSpec ──>│ Router Agent  │── selects: mode + model + skills
            └──────┬───────┘
                   │
                   v
            ┌──────────────┐
            │ Executor      │── runs PromptBuilder/DSPy prompt, calls tools
            └──────┬───────┘
                   │
                   v
            ┌──────────────┐
            │ Critic/Grader │── optional: VERIX parse, frame compliance, rubrics
            └──────────────┘
```

**Why only 3?**
Because every additional agent increases:
- token cost
- coordination failures
- non‑determinism

If you want more “experts,” make them **skills** (callable modules) rather than autonomous agents.

### 3.2 Router logic (simple and deterministic)
Order of decisions:

1) **Mode** (intent preset) — maps to a stable config. Mode library is explicitly the user‑facing abstraction over vectors.
2) **Model** — choose based on task_type + risk + budget
3) **Skill budget** — which tools are permitted + max calls
4) **Prompt config** — produced by config→prompt layer

---

## 4) Model plane: multi‑model selection (capability routing)

### 4.1 Treat “model choice” as part of the config space (but gated)
You *can* include model_id in the optimization vector, but only after:
- you have stable evaluation metrics
- you log model/version/commit hashes (auditability)

**Practical default:** keep model selection outside GlobalMOO at first; optimize prompt/config within each model.

### 4.2 Safe fallback policy
- If the chosen model errors, fall back to next cheapest compatible model.
- Always record the fallback event in logs.

---

## 5) Skill plane: make skills boring, typed, and budgeted

### 5.1 Skill = Tool contract + policy
Define every skill as:
- **schema** (inputs/outputs)
- **preconditions** (when allowed)
- **cost model** (tokens/time/$$)
- **side‑effects** (writes logs? reads files?)
- **failure modes** (what exceptions mean)

### 5.2 Two buckets (MECE)
1) **Deterministic skills** (preferred): regex checks, parsing, math, file transforms
2) **LLM skills** (expensive): judge grading, synthesis, red‑team prompts

Your eval layer explicitly expects deterministic graders plus optional LLM judges.

### 5.3 The “skills don’t touch prompts” rule
Skills operate on:
- TaskSpec
- intermediate artifacts
- responses
- metrics/logs

Only PromptBuilder touches prompt construction.

This prevents prompt logic from leaking everywhere.

---

## 6) Prompt plane: VERILINGUA + VERIX + DSPy (minimal integration)

### 6.1 VERILINGUA frames (developer view)
Implement frames with a tiny interface: activation instructions + required markers + compliance score.

**Low‑confusion rule:** cap active frames per task (e.g., 1–3) using `max_frames_per_task`.

### 6.2 VERIX (developer view)
Implement a parser + compliance checker; use strictness as a config knob.

### 6.3 DSPy Level 2: optimize “prompt expression,” not framework structure
Cluster configs (frames + VERIX strictness + activation style) and cache compiled prompts per cluster key.

Minimal DSPy module pattern is provided in the guide.

---

## 7) Learning plane: evaluation + GlobalMOO + governance

### 7.1 Keep objectives small and anti‑gameable
Core objectives recommended:
- task accomplishment
- token efficiency
- edge‑case robustness (reward useful uncertainty)
- epistemic consistency

Guardrails:
- normalize for length so “verbosity doesn’t win.”
- treat format compliance as a sub‑metric so it can’t be gamed.

### 7.2 Three‑MOO cascade (how to scale safely)
- Phase A: structure selection
- Phase B: edge discovery + stability radius
- Phase C: production frontier → modes

### 7.3 GlobalMOO integration checkpoints
Before deploying:
- vector codecs stable/versioned
- forward model tested
- seed data (10–20 evals)
- holdout set reserved

GlobalMOO API is model/project/trial; it supports inverse queries and impact factors.

---

## 8) Claude Code integration: keep the command surface tiny

The guide recommends exposing a small tool API and a few commands: `/mode`, `/eval`, `/optimize`, `/pareto`.

### 8.1 Minimal CLAUDE.md template (drop into repo)
```md
# Project rules (Claude Code)

## Defaults
- Default mode: auto (router selects)
- Never run optimization in production sessions.
- Foundry changes are offline only; promotion requires the frozen eval harness.

## How to run a task
1) Build prompts via PromptBuilder
2) Execute model client
3) Parse VERIX + score frame compliance
4) Log JSONL record

## Commands (runtime)
- /mode <audit|speed|math|research|synthesis|auto>
- /eval <task_type> [--mode X]

## Commands (learning / optimization)
- /optimize [--phase a|b|c] [--iters N]
- /pareto [--objective tokens|accuracy|robustness|consistency]

## Commands (foundry / meta loop)
- /foundry architect <target>         # improve a user prompt
- /foundry forge <target>             # improve a system prompt
- /foundry agent <spec>               # create a new agent
- /foundry skill <spec>               # create a new skill
- /ralph-loop <completion_promise>    # guarded loop; blocks exit until promise + gates pass
- bash scripts/meta-loop/meta-loop-setup.sh start "<goal>" --target "<path>" --foundry "<tool>"
- bash scripts/meta-loop/meta-loop-setup.sh status
- bash scripts/meta-loop/meta-loop-setup.sh next-phase
- bash scripts/meta-loop/meta-loop-setup.sh cancel

## Safety / governance
- Optimization runs only in scheduled jobs.
- Always keep a holdout regression set.
- Never allow “silent promotion” of Foundry outputs.
```

This matches the manual’s recommended CLAUDE.md contents and guardrails.

---

### 8.2 Meta Loop (Foundry Lane) powered by Ralph Wiggum

**Ralph Wiggum** is a hook loop that prevents “production theater” by **refusing to let the run end** until explicit criteria are met.

Operationally:
- Ralph maintains a **single** loop state file: `~/.claude/ralph-wiggum/loop-state.md`
- When Claude tries to exit, a Stop hook checks for:
  - the required `completion_promise` token
  - phase‑specific quality gates (e.g., diffs applied, audits pass, eval passes)
  - `iteration < max_iterations`
- Not satisfied → exit code **2** → prompt is re‑injected and the loop continues
- Satisfied → exit code **0** → loop deactivates

**Correct Meta Loop flow (sequential phases; no nesting):**
1) EXECUTE → promise `{FOUNDRY}_PROPOSAL_READY`
2) IMPLEMENT → promise `CHANGES_APPLIED`
3) AUDIT → promise `ALL_AUDITS_PASS` (spawn 4 parallel Task auditors inside the loop)
4) EVAL → promise `EVAL_HARNESS_PASS`

Best practice: promises should be emitted as a single grep‑friendly line: `PROMISE: <TOKEN>` at the end of the phase output.

## 9) “Do this first” implementation checklist (MVP → full system)

### MVP (1–2 days)
- [ ] Implement `FullConfig` + VectorCodec (stable order)
- [ ] Implement PromptBuilder `build()`
- [ ] Implement VERIX parser + format compliance
- [ ] Implement frame registry + compliance scoring
- [ ] Implement JSONL logging (config vector + prompt hash + response + metrics)

### Production (week)
- [ ] Build mode library (Pareto → named modes)
- [ ] Add deterministic graders + optional LLM judge
- [ ] Add edge case corpus + robustness metric
- [ ] DSPy Level 2 clustering + cache

### Optimization (month)
- [ ] GlobalMOO forward model + objectives
- [ ] Seed data + holdout suite
- [ ] Phase A/B/C cadence

---

## 10) Where the conlang PDFs fit (without confusing engineering)

Treat conlang/constructed‑language materials as:
- **frame design & expansion docs** (how to invent new frames)
- **theoretical justification** (why a frame should help)

But day‑to‑day engineering should treat frames as:
- named toggles
- activation templates
- compliance checkers

Keep that boundary strict; it prevents “theory sprawl” from leaking into runtime code.

---

## 11) Common multi‑agent failure modes (and the simplest fixes)

1) **Agent disagreement loops**
Fix: router chooses a single executor; critics only grade, they don’t rewrite.

2) **Skill spam**
Fix: per‑task skill budgets (max calls, max time).

3) **Over‑optimization theater**
Fix: holdout set + human spot checks + anti‑verbosity penalties.

4) **Robustness becomes cowardice**
Fix: define robustness to reward *useful uncertainty* (not hedging).

---

## Appendix: minimal interfaces (code sketch)

### Frame + VERIX parser (from the integration guide)
```python
class Frame(Protocol):
    name: str
    def activation_instructions(self, style: str, verbosity: int) -> str: ...
    def required_markers(self) -> list[str]: ...
    def compliance_score(self, response: str) -> float: ...

class VerixParser:
    def parse(self, response: str) -> list[VerixClaim]: ...
    def format_compliance(self, response: str) -> float: ...
```

### GlobalMOO forward model skeleton
```python
def forward_model(config_vector: list[int]) -> list[float]:
    config = decode_config(config_vector)
    prompts = build_prompts(config)
    responses = execute_tasks(prompts, task_corpus)
    outcomes = measure_outcomes(responses, task_corpus)
    return encode_outcomes(outcomes)
```

