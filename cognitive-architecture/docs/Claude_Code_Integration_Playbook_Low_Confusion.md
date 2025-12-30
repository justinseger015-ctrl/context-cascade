# Claude Code Integration Playbook (Low‑Confusion Edition)
## VERILINGUA × VERIX × DSPy × GlobalMOO inside a multi‑agent / multi‑model / multi‑skill system

**Audience:** engineers implementing a Claude Code–style agent workspace  
**Goal:** make the system *easy to integrate* and *hard to misuse*.

This playbook assumes you already have (or will adopt) the core architecture described in the existing integration manual: VERILINGUA frames + VERIX notation as the prompt layer; DSPy as per‑cluster prompt expression optimizer; GlobalMOO as the outer multi‑objective optimizer; and a closed feedback loop from runtime logs → optimization → mode updates. fileciteturn2file2L14-L29 fileciteturn2file2L133-L159

---

## 0) 10‑minute mental model (thin waist)

You are building an **agent platform** with a **thin waist**:

### The only two contracts that must never change
1) **Prompt contract:** `PromptBuilder.build(task, task_type) -> (system, user)` fileciteturn3file12L1-L15  
2) **Optimization contract:** `evaluate(config_vector) -> outcomes_vector` fileciteturn3file6L80-L91

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

The existing guide already specifies a reference layout that cleanly separates these concerns (core/eval/optimization/modes/claude_integration). fileciteturn2file2L187-L225

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

- `FullConfig` dataclasses and a stable vector mapping are explicitly recommended. fileciteturn2file2L229-L236
- Keep mapping stable and versioned (VectorCodec pattern). fileciteturn2file2L283-L289

### 2.3 EvalOutcome (what learning consumes)
Use a compact outcomes vector (≈10–14 dimensions) to avoid slow learning and overfitting. fileciteturn3file1L12-L13

The GlobalMOO guide’s example 11‑dim outcome codec is a solid default. fileciteturn3file9L15-L25

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

1) **Mode** (intent preset) — maps to a stable config. Mode library is explicitly the user‑facing abstraction over vectors. fileciteturn3file0L54-L69  
2) **Model** — choose based on task_type + risk + budget  
3) **Skill budget** — which tools are permitted + max calls  
4) **Prompt config** — produced by config→prompt layer

---

## 4) Model plane: multi‑model selection (capability routing)

### 4.1 Treat “model choice” as part of the config space (but gated)
You *can* include model_id in the optimization vector, but only after:
- you have stable evaluation metrics
- you log model/version/commit hashes (auditability) fileciteturn3file13L55-L57

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

Your eval layer explicitly expects deterministic graders plus optional LLM judges. fileciteturn2file2L197-L203

### 5.3 The “skills don’t touch prompts” rule
Skills operate on:
- TaskSpec
- intermediate artifacts
- responses
- metrics/logs

Only PromptBuilder touches prompt construction. fileciteturn3file12L1-L15

This prevents prompt logic from leaking everywhere.

---

## 6) Prompt plane: VERILINGUA + VERIX + DSPy (minimal integration)

### 6.1 VERILINGUA frames (developer view)
Implement frames with a tiny interface: activation instructions + required markers + compliance score. fileciteturn2file2L70-L88

**Low‑confusion rule:** cap active frames per task (e.g., 1–3) using `max_frames_per_task`. fileciteturn2file2L264-L266

### 6.2 VERIX (developer view)
Implement a parser + compliance checker; use strictness as a config knob. fileciteturn2file2L90-L113

### 6.3 DSPy Level 2: optimize “prompt expression,” not framework structure
Cluster configs (frames + VERIX strictness + activation style) and cache compiled prompts per cluster key. fileciteturn3file6L43-L53

Minimal DSPy module pattern is provided in the guide. fileciteturn3file7L3-L20

---

## 7) Learning plane: evaluation + GlobalMOO + governance

### 7.1 Keep objectives small and anti‑gameable
Core objectives recommended:
- task accomplishment
- token efficiency
- edge‑case robustness (reward useful uncertainty)
- epistemic consistency fileciteturn3file6L3-L18

Guardrails:
- normalize for length so “verbosity doesn’t win.” fileciteturn3file6L27-L30
- treat format compliance as a sub‑metric so it can’t be gamed. fileciteturn3file6L21-L23

### 7.2 Three‑MOO cascade (how to scale safely)
- Phase A: structure selection
- Phase B: edge discovery + stability radius
- Phase C: production frontier → modes fileciteturn3file11L9-L27

### 7.3 GlobalMOO integration checkpoints
Before deploying:
- vector codecs stable/versioned
- forward model tested
- seed data (10–20 evals)
- holdout set reserved fileciteturn3file2L35-L45

GlobalMOO API is model/project/trial; it supports inverse queries and impact factors. fileciteturn3file5L57-L67

---

## 8) Claude Code integration: keep the command surface tiny

The guide recommends exposing a small tool API and a few commands: `/mode`, `/eval`, `/optimize`, `/pareto`. fileciteturn3file7L48-L62

### 8.1 Minimal CLAUDE.md template (drop into repo)
```md
# Project rules (Claude Code)

## Defaults
- Default mode: auto (router selects)
- Never run optimization in production sessions.

## How to run a task
1) Build prompts via PromptBuilder
2) Execute model client
3) Parse VERIX + score frame compliance
4) Log JSONL record

## Commands
- /mode <audit|speed|math|research|synthesis|auto>
- /eval <task_type> [--mode X]
- /optimize [--phase a|b|c] [--iters N]
- /pareto [--objective tokens|accuracy|robustness|consistency]

## Safety / governance
- Optimization runs only in scheduled jobs.
- Always keep a holdout regression set.
```

This matches the manual’s recommended CLAUDE.md contents and guardrails. fileciteturn3file0L18-L24

---

## 9) “Do this first” implementation checklist (MVP → full system)

### MVP (1–2 days)
- [ ] Implement `FullConfig` + VectorCodec (stable order) fileciteturn2file2L229-L236
- [ ] Implement PromptBuilder `build()` fileciteturn3file12L1-L15
- [ ] Implement VERIX parser + format compliance fileciteturn2file2L90-L113
- [ ] Implement frame registry + compliance scoring fileciteturn2file2L70-L88
- [ ] Implement JSONL logging (config vector + prompt hash + response + metrics) fileciteturn3file7L74-L81

### Production (week)
- [ ] Build mode library (Pareto → named modes) fileciteturn3file0L54-L69
- [ ] Add deterministic graders + optional LLM judge fileciteturn2file2L197-L203
- [ ] Add edge case corpus + robustness metric fileciteturn3file6L11-L14
- [ ] DSPy Level 2 clustering + cache fileciteturn3file6L43-L53

### Optimization (month)
- [ ] GlobalMOO forward model + objectives fileciteturn3file10L11-L16
- [ ] Seed data + holdout suite fileciteturn3file2L39-L45
- [ ] Phase A/B/C cadence fileciteturn3file0L38-L46

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
Fix: holdout set + human spot checks + anti‑verbosity penalties. fileciteturn3file0L75-L78

4) **Robustness becomes cowardice**  
Fix: define robustness to reward *useful uncertainty* (not hedging). fileciteturn3file6L11-L14

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
fileciteturn2file2L79-L88 fileciteturn2file2L99-L113

### GlobalMOO forward model skeleton
```python
def forward_model(config_vector: list[int]) -> list[float]:
    config = decode_config(config_vector)
    prompts = build_prompts(config)
    responses = execute_tasks(prompts, task_corpus)
    outcomes = measure_outcomes(responses, task_corpus)
    return encode_outcomes(outcomes)
```
fileciteturn3file10L23-L48
