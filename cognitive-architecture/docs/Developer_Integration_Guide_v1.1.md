# Developer Integration Guide v1.1  
## VERILINGUA × VERIX × DSPy × GlobalMOO — integrated into a Claude Code workflow

**Version:** 1.1  
**Audience:** Developers integrating into a Claude Code–style agent framework  
**Language:** Python 3.10+  
**Scope:** Architecture + implementation patterns + operational workflow  
**Companion Specs:** (Provided separately by you) **VERILINGUA Guide** + **VERIX Guide**

---

## 0) Executive summary

This guide describes a **self-improving prompting architecture** that continuously discovers better prompt configurations **without relying on intuition alone**.

It integrates four components:

1. **VERILINGUA** — a library of “cognitive frames” derived from obligatory distinctions in natural languages (e.g., evidentials, aspect, morphology). Frames are *constraints that shape reasoning*.
2. **VERIX** — a compact epistemic notation that makes claims auditable: what is being done (illocution), how sure (confidence), why (ground), and whether the matter is settled (state). VERIX is your *invariant layer*.
3. **DSPy** — programmatic prompt optimization: define signatures/modules and let optimizers learn the best prompt expression for a given config “cluster.”
4. **GlobalMOO** — multi-objective optimization that finds Pareto-optimal trade-offs **and** supports inverse queries (“find configs that hit these targets”). GlobalMOO is the outer optimizer.

Together they form a **closed loop**:

- Runtime usage generates structured logs (config → prompt → response → measured outcomes).
- Optimizers learn the trade-off structure.
- The system distills Pareto-optimal “modes” (Audit/Speed/Research/Math/Synthesis).
- Periodic evolution updates routing rules and the frame library.

---

## 1) Mental model (what the system is optimizing)

### 1.1 What makes this different from “prompt engineering”
Traditional prompt engineering optimizes *one thing at a time* and hides trade-offs.

This architecture treats prompt design as a **multi-objective search** over a structured configuration space:

- Improve accuracy → costs tokens/latency
- Increase transparency → costs brevity/speed
- Add robustness to ambiguity → risks under-commitment
- Increase confidence calibration → may reduce “smoothness” in outputs

Instead of collapsing these into arbitrary weights, we **map the Pareto frontier**.

### 1.2 Why VERILINGUA frames matter
A VERILINGUA frame is a **productive constraint**. It forces specific distinctions to be made, reducing the chance of vague reasoning.

Examples (detailed definitions live in your VERILINGUA spec):
- **Turkish evidentiality**: forces “how do you know?” (direct vs inferred vs reported)
- **Russian aspect**: forces “done vs ongoing vs partial”
- **Arabic morphology**: encourages root-pattern semantic decomposition
- **German compounding**: encourages compositional primitives → compounds

Frames define **axes** in the cognitive trade-off landscape that GlobalMOO can tune.

### 1.3 Why VERIX is the invariant layer
VERIX makes the epistemic structure explicit, enabling:
- calibration measurement (confidence vs correctness)
- consistency checks (avoid contradictory high-confidence claims)
- automatic parsing for logs/metrics
- compression policies (L0/L1/L2) as knobs

Think: in physics you want invariants preserved; here you want **epistemic coherence** preserved.

---

## 2) Component primers (minimal, developer-facing)

### 2.1 VERILINGUA (developer view)
**Input:** task + frame selection + activation style  
**Output:** prompt requirements + expected structural markers to grade

Developer responsibilities:
- implement `Frame` objects (activation templates + compliance checks)
- implement frame routing (manual selection, heuristic, or learned)
- expose frame toggles in config vectors

Recommended minimal interface:

```python
class Frame(Protocol):
    name: str

    def activation_instructions(self, style: str, verbosity: int) -> str: ...
    def required_markers(self) -> list[str]: ...
    def compliance_score(self, response: str) -> float: ...
```

### 2.2 VERIX (developer view)
**Input:** response text  
**Output:** parsed claim records + structural compliance

Developer responsibilities:
- implement parser/validator for your VERIX schema
- implement compression levels L0/L1/L2 as a config knob
- compute calibration + epistemic consistency from parsed claims

Minimal interface:

```python
@dataclass
class VerixClaim:
    text: str
    confidence: float | None
    ground: str | None
    state: str | None
    illocution: str | None

class VerixParser:
    def parse(self, response: str) -> list[VerixClaim]: ...
    def format_compliance(self, response: str) -> float: ...
```

### 2.3 DSPy (developer view)
DSPy shifts you from writing prompt strings to defining **Signatures** + **Modules**, then compiling them with optimizers.

You’ll use DSPy mainly in **Level 2** (prompt expression optimization):
- for each config cluster, learn the best phrasing + few-shot demos

### 2.4 GlobalMOO (developer view)
GlobalMOO is the “outer loop” that:
- suggests next configs to evaluate
- learns which variables drive which objectives
- supports inverse queries (hit target bounds)
- efficiently explores Pareto trade-offs with fewer evaluations than many EA methods

Your code provides **the expensive function**:  
`f(config) -> outcomes`

---

## 3) Integrated architecture

### 3.1 High-level dataflow

```
   ┌───────────────┐
   │ GlobalMOO      │  suggests config vectors
   └───────┬───────┘
           │
           v
   ┌──────────────────────┐     ┌─────────────────┐
   │ Config → Prompt       │ --> │ Claude runtime   │
   │ (VERILINGUA+VERIX)    │     │ (execution)      │
   └──────────┬───────────┘     └─────────┬───────┘
              │                            │
              v                            v
     ┌────────────────┐           ┌──────────────────┐
     │ DSPy Level 2   │           │ Evaluation        │
     │ (prompt expr)  │           │ metrics + logs    │
     └───────┬────────┘           └─────────┬────────┘
             │                              │
             └──────────────┬───────────────┘
                            v
                     ┌───────────────┐
                     │ GlobalMOO      │  learns frontier + impacts
                     └───────────────┘
```

### 3.2 The Three-MOO Cascade (recommended)

**Phase A — Framework structure optimization**  
- Decide *what the system contains*: which frames exist, routing rule family, VERIX strictness options.
- Search discrete structures for: **expressiveness**, **parsimony**, **stability**.
- Output: a stable parameter space for later phases.

**Phase B — Edge discovery**  
- Find boundaries where reasoning “cliffs” occur (e.g., too much compression → accuracy collapse).
- Output: constraints + *stability radius* (how far you can perturb before failure).

**Phase C — Production optimization**  
- Optimize within bounds; map Pareto frontier across 4 core objectives:
  1) Task accomplishment  
  2) Token efficiency  
  3) Edge-case robustness  
  4) Epistemic consistency  
- Output: Pareto set → distilled “modes”

### 3.3 DSPy two-layer learning (recommended)

**Level 2 (fast, per-cluster):** optimize prompt expression for a fixed config cluster  
**Level 1 (slow, periodic):** propose structural changes (new frames, routing rules) based on aggregate logs

---

## 4) Reference implementation layout

```
cognitive-architecture/
├── core/
│   ├── verilingua.py            # frames + routing
│   ├── verix.py                 # notation + parsing
│   ├── config.py                # dataclasses + vector mapping
│   ├── prompt_builder.py        # config → system/user prompts
│   └── runtime.py               # claude client wrapper
├── eval/
│   ├── metrics.py               # objective functions
│   ├── graders/
│   │   ├── deterministic.py      # format, tokens, latency, regex checks
│   │   └── llm_judge.py          # optional: rubric scoring
│   ├── edge_cases.py            # curated edge corpus
│   └── consistency.py           # epistemic consistency logic
├── optimization/
│   ├── globalmoo_client.py       # SDK wrapper
│   ├── dspy_level2.py            # per-cluster compile/cache
│   ├── dspy_level1.py            # evolution analysis (monthly)
│   ├── cascade.py                # Phase A/B/C orchestration
│   └── distill_modes.py          # Pareto → named modes
├── modes/
│   ├── library.py                # Audit/Speed/etc
│   └── selector.py               # auto selection heuristics
├── storage/
│   ├── logs/                     # structured JSONL
│   ├── prompts/                  # cached compiled prompts
│   └── results/                  # optimization artifacts
├── claude_integration/
│   ├── CLAUDE.md                 # project memory + rules
│   ├── tools.py                  # callable tools for agents
│   └── commands/                 # /mode /eval /optimize etc
└── cli/
    ├── run_task.py
    ├── optimize.py
    └── report.py
```

---

## 5) Configuration model (the core “vector”)

### 5.1 Why this matters
GlobalMOO optimizes vectors. Your framework must map:
- discrete choices (frame on/off, strictness enum, activation style)
- small integers (few-shot count, verbosity)
into a **stable vector representation**.

### 5.2 Suggested dataclasses

```python
from dataclasses import dataclass
from enum import IntEnum

class VerixStrictness(IntEnum):
    OPTIONAL = 0
    PARTIAL  = 1
    FULL     = 2

class ActivationStyle(IntEnum):
    IMPLICIT  = 0
    EXPLICIT  = 1
    CHECKLIST = 2

@dataclass(frozen=True)
class FrameworkConfig:
    # VERILINGUA frames (booleans)
    russian_aspect: bool
    turkish_evidential: bool
    arabic_morphology: bool
    german_composition: bool
    japanese_keigo: bool
    chinese_classifiers: bool
    guugu_spatial: bool

    max_frames_per_task: int          # 1..4
    verix_strictness: VerixStrictness
    verix_confidence_required: bool
    verix_ground_chain_required: bool

@dataclass(frozen=True)
class PromptConfig:
    activation_style: ActivationStyle
    activation_verbosity: int         # 0..2
    fewshot_count: int                # 0..3
    show_verix_legend: bool
    system_prompt_length: int         # 0..2

@dataclass(frozen=True)
class FullConfig:
    framework: FrameworkConfig
    prompt: PromptConfig
```

### 5.3 Vector mapping

```python
class VectorCodec:
    def to_vector(self, cfg: FullConfig) -> list[int]:
        # fixed order, stable mapping
        return [
            int(cfg.framework.russian_aspect),
            int(cfg.framework.turkish_evidential),
            int(cfg.framework.arabic_morphology),
            int(cfg.framework.german_composition),
            int(cfg.framework.japanese_keigo),
            int(cfg.framework.chinese_classifiers),
            int(cfg.framework.guugu_spatial),
            cfg.framework.max_frames_per_task,
            int(cfg.framework.verix_strictness),
            int(cfg.framework.verix_confidence_required),
            int(cfg.framework.verix_ground_chain_required),
            int(cfg.prompt.activation_style),
            cfg.prompt.activation_verbosity,
            cfg.prompt.fewshot_count,
            int(cfg.prompt.show_verix_legend),
            cfg.prompt.system_prompt_length,
        ]

    def from_vector(self, v: list[int]) -> FullConfig:
        # inverse mapping, with validation
        ...
```

---

## 6) Prompt building (VERILINGUA × VERIX → prompts)

### 6.1 PromptBuilder responsibilities
- choose frames (pre-selected, heuristic, or learned selector)
- render activation instructions
- render VERIX requirements and compression level
- insert few-shot examples (optional)
- output: `(system_prompt, user_prompt)`

```python
class PromptBuilder:
    def __init__(self, cfg: FullConfig, frame_registry, verix_spec):
        self.cfg = cfg
        ...

    def build(self, task: str, task_type: str) -> tuple[str, str]:
        # 1) select active frames
        frames = self._select_frames(task_type)
        # 2) system instructions (frames + VERIX)
        system = self._build_system(frames, task_type)
        # 3) user message template
        user = self._build_user(task, frames, task_type)
        return system, user
```

---

## 7) Evaluation: objective functions and anti-gaming

### 7.1 Core objectives (recommended)
1. **Task accomplishment** (maximize)  
   - deterministic accuracy when ground-truth exists  
   - rubric-based score (0..1) when open-ended

2. **Token efficiency** (minimize)  
   - total tokens or $ cost per task

3. **Edge-case robustness** (maximize)  
   - curated adversarial/ambiguous tasks  
   - reward “useful uncertainty,” not just hedging

4. **Epistemic consistency** (maximize)  
   - avoid contradictory high-confidence claims  
   - confidence propagation coherence (when entailments are detectable)

### 7.2 Practical metric details

**Format compliance (VERIX + frames)**  
- compute as a sub-metric (do not let it dominate by gaming)

**Calibration (Brier-like)**  
- requires extracted confidences + correctness labels for claims/tasks

**Length normalization**  
- critical to prevent “verbosity wins”
- penalize excess tokens relative to task type baseline

### 7.3 Stability radius (Phase B output)
A “fragility” estimate: how far config variables can change before metrics drop below thresholds.

Implementation sketch:
- sample neighbor vectors within Hamming distance / small integer deltas
- evaluate quickly on a small probe set
- compute radius where failure probability crosses e.g. 20%

---

## 8) DSPy integration (Level 2 prompt expression optimization)

### 8.1 Why cluster configs
You don’t want to compile a brand-new DSPy module for every vector.

Cluster by:
- active frame set
- VERIX strictness
- activation style
- few-shot count (optional)

Cache compiled prompts per cluster key.

### 8.2 DSPy module pattern (minimal)

```python
import dspy

class FrameActivatedReasoning(dspy.Signature):
    task = dspy.InputField(desc="Problem statement")
    active_frames = dspy.InputField(desc="Frame list or frame directives")
    verix_requirements = dspy.InputField(desc="VERIX requirements")
    answer = dspy.OutputField(desc="Analysis + final output per VERIX")

class CognitiveModule(dspy.Module):
    def __init__(self):
        self.cot = dspy.ChainOfThought(FrameActivatedReasoning)

    def forward(self, task, active_frames, verix_requirements):
        return self.cot(task=task, active_frames=active_frames, verix_requirements=verix_requirements)
```

### 8.3 Optimizers
- `BootstrapFewShot` to synthesize demonstrations
- `MIPROv2` for instruction + demo search (often best default)
- `GEPA` for reflective evolution (slower, useful periodically)

---

## 9) GlobalMOO integration (outer loop)

### 9.1 The core contract
You provide:
- vector bounds/types
- `evaluate(vector) -> outcomes_vector`

GlobalMOO provides:
- suggested vectors to test
- inverse suggestions to hit targets
- impact factors / sensitivity (useful for pruning variables)

### 9.2 Practical tips
- treat each LLM eval as expensive; batch tasks per evaluation
- log model/version/commit hash for every run (auditability)
- keep a **holdout set** that optimizers never see

---

## 10) Claude Code integration

### 10.1 Provide tools/commands
Expose a small tool API so agents can:
- select a mode
- get prompts
- record outcomes
- run optimization cycles (authorized)

Suggested command surface:
- `/mode <audit|speed|math|research|synthesis|auto>`
- `/eval <task_type> [--mode X]`
- `/optimize [--phase a|b|c] [--iters N]`
- `/pareto [--objective tokens|accuracy|robustness|consistency]`

### 10.2 CLAUDE.md content (recommended)
Include:
- default mode behavior
- how to call `PromptBuilder`
- logging expectations (JSONL schema)
- safety guardrails (no silent optimization in prod; run in scheduled jobs)

---

## 11) Operational cadence (continuous improvement)

**Daily (runtime):**
- record structured logs:
  - config vector
  - task type
  - prompts hash
  - response
  - tokens/latency
  - compliance + outcome metrics

**Weekly (optimization):**
- run Phase C on new logs
- update Pareto set
- distill/update mode library

**Monthly (evolution):**
- run DSPy Level 1 analysis + Phase A/B refresh
- propose changes (frames, routing rules, stricter/looser VERIX defaults)

**Quarterly (human governance):**
- review modes
- retire brittle configs
- validate against holdout regression suite

---

## 12) Mode library (Pareto → named modes)

### 12.1 Why distill modes
Most users don’t want vectors; they want stable “presets.”

### 12.2 Distillation method
- cluster Pareto points by objective emphasis
- pick representative point per cluster
- name by intent:
  - **Audit Mode**: consistency + sourcing + strict VERIX
  - **Speed Mode**: low tokens/latency
  - **Research Mode**: accuracy + robustness, moderate verbosity
  - **Math Mode**: stepwise calculation + strict consistency
  - **Synthesis Mode**: structure + clarity + medium tokens

Store as YAML/JSON for easy deployment.

---

## 13) Common failure modes (and fixes)

1) **Optimization theater**  
   - symptom: metrics improve but outputs “feel worse”  
   - fix: add holdout suite + human spot checks + anti-verbosity penalties

2) **Overfitting to corpus**  
   - symptom: great on training tasks, poor in real use  
   - fix: diversify tasks; keep a hidden regression set

3) **Robustness = cowardice**  
   - symptom: models hedge too much to avoid being wrong  
   - fix: robustness metric rewards *usefulness under uncertainty* not just caution

4) **Metric redundancy**  
   - symptom: multiple metrics measure the same thing  
   - fix: track correlations; prune metrics or reweight reporting

---

## Appendix A) Parameter reference (example)

### Framework params
- russian_aspect (0/1)
- turkish_evidential (0/1)
- arabic_morphology (0/1)
- german_composition (0/1)
- japanese_keigo (0/1)
- chinese_classifiers (0/1)
- guugu_spatial (0/1)
- max_frames_per_task (1–4)
- verix_strictness (0–2)
- verix_confidence_required (0/1)
- verix_ground_chain_required (0/1)

### Prompt params
- activation_style (0–2)
- activation_verbosity (0–2)
- fewshot_count (0–3)
- show_verix_legend (0/1)
- system_prompt_length (0–2)

---

## Appendix B) Outcome metrics (recommended baseline)

- task_accuracy (↑)
- calibration_score (↓)
- format_compliance (↑)
- ground_chain_validity (↑)
- tokens_total (↓)
- latency_seconds (↓)
- edge_case_robustness (↑)
- epistemic_consistency (↑)

---

## Appendix C) Settings template

```yaml
anthropic:
  api_key: ${ANTHROPIC_API_KEY}
  default_model: "claude-sonnet-4-20250514"

globalmoo:
  api_key: ${GLOBALMOO_API_KEY}
  base_uri: "https://api.globalmoo.ai/api"

storage:
  logs_dir: "./storage/logs"
  prompts_dir: "./storage/prompts"
  results_dir: "./storage/results"

optimization:
  weekly_phase_c_iterations: 80
  monthly_phase_a_iterations: 20
  monthly_phase_b_probes: 60
  holdout_suite: "./tasks/holdout.jsonl"

modes:
  default: "auto"
```

---

## Appendix D) Minimal “getting started” checklist

1) Implement `FullConfig` + `VectorCodec`  
2) Implement VERIX parser + compliance scoring  
3) Implement 2–3 frames with compliance checks  
4) Implement `PromptBuilder`  
5) Implement evaluation metrics and JSONL logging  
6) Integrate Claude runtime client  
7) Run baseline evaluation → generate first dataset  
8) Add DSPy Level 2 compile/cache for a single cluster  
9) Integrate GlobalMOO → Phase C first  
10) Add Phase B edge discovery → compute stability radius  
11) Distill modes → ship to Claude Code tools

---

**End of v1.1**
