# Developer Integration Guide v1.1 — Unified Manual
**Last updated:** 2025-12-28  
**Audience:** engineers integrating VERILINGUA × VERIX with DSPy + GlobalMOO inside a Claude Code workflow.  
**You will also receive:** the standalone VERILINGUA and VERIX specification guides (authoritative definitions).

---

## How this manual is organized (MECE)
1) **Core Guide (v1.1)** — what the system is and how to integrate it end-to-end  
2) **Appendix A (DSPy Guide)** — deep DSPy onboarding + implementation playbook  
3) **Appendix B (GlobalMOO Guide)** — deep GlobalMOO onboarding + optimization playbook

---

## What changed from Claude’s draft (debug + critique highlights)
This v1.1 manual:
- makes **version pinning + reproducibility** a first-class requirement (DSPy/LM changes otherwise invalidate results)
- clarifies **cluster key design** and cache invalidation rules (to avoid “cluster explosion” and stale prompts)
- separates **constraints vs objectives** to reduce “optimization theater”
- adds **regression + edge-case gates** as required acceptance checks
- documents **security boundaries** for compile-time vs runtime prompt generation
- adds operational cadence + artifact governance for long-running systems

---

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

---

# Appendix A — DSPy Developer Guide (v1.1)
**Purpose:** onboarding + internal handoff for engineers integrating DSPy into the VERILINGUA × VERIX × GlobalMOO system.  
**Scope:** DSPy concepts, architecture, implementation patterns, evaluation, optimization, debugging, and ops.

> **Mental model**
> - **You write a program** (signatures + modules) that *describes* what you want.
> - **DSPy compiles** that program into prompt(s) / demonstrations that work for your data.
> - **Optimizers search** prompt space using a metric you control.
> - **Artifacts are cacheable** (compiled prompts per “prompt cluster”), and can be versioned like model weights.

---

## A.1 DSPy in this project: where it sits

### A.1.1 The two DSPy layers we use
We use DSPy at two distinct timescales:

1) **Level 2 — Prompt Expression Optimization (fast loop)**  
Optimizes how to express a *fixed* configuration: which instructions, which demos, what ordering, what verbosity.  
Output: **compiled prompts** per prompt cluster.

2) **Level 1 — Framework Evolution (slow loop)**  
Uses aggregated telemetry to propose changes to the framework itself (frames, routing rules, VERIX strictness defaults, etc.).  
Output: **framework diffs** (PRs), not just prompts.

> **Rule of thumb:**  
> If the change can be captured by a prompt rewrite or example set, it’s Level 2.  
> If the change modifies the config space or schemas, it’s Level 1.

---

## A.2 Core DSPy concepts you must grok

### A.2.1 Signatures
A **Signature** is a typed contract: inputs + outputs + descriptions.  
The signature is the “what”, not the “how”.

```python
import dspy

class FrameActivatedReasoning(dspy.Signature):
    """Solve the task using specified cognitive frames and VERIX requirements."""
    task = dspy.InputField(desc="User task / problem statement")
    active_frames = dspy.InputField(desc="List of VERILINGUA frame names to apply")
    verix_requirements = dspy.InputField(desc="VERIX strictness + formatting requirements")
    answer = dspy.OutputField(desc="Final response")
    verix_audit = dspy.OutputField(desc="List of VERIX-tagged claims (machine-readable)")
```

**Project conventions**
- Keep signatures **small** (avoid megasignatures).
- Prefer **two outputs**: `answer` (human) and `verix_audit` (machine).
- Do not embed long policies in `desc`; put policies in the system prompt builder.

### A.2.2 Modules
A **Module** composes calls. Typical patterns:

- `dspy.Predict(Signature)` — direct prediction
- `dspy.ChainOfThought(Signature)` — structured reasoning (note: we do *not* expose chain-of-thought; we use structured fields)

```python
class CognitiveAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.solve = dspy.ChainOfThought(FrameActivatedReasoning)

    def forward(self, task: str, active_frames: list[str], verix_requirements: str):
        return self.solve(task=task, active_frames=active_frames, verix_requirements=verix_requirements)
```

### A.2.3 Metrics
DSPy optimizers need a `metric(example, prediction) -> float` (or bool).  
Metrics are *the product*. Garbage metric = garbage optimization.

**Our canonical metric bundle (weighted but auditable):**
- `task_success` (correctness / goal completion)
- `format_compliance` (VERIX + frame markers)
- `calibration` (Brier score proxy)
- `tokens` (penalty)
- `edge_case_robustness` (special test set)
- `epistemic_consistency` (cross-claim checks)

Implementation pattern:
- Return a dict of sub-metrics (for logging),
- Provide a scalar `score` for DSPy (for optimization),
- Store all sub-metrics in telemetry.

### A.2.4 Datasets
DSPy expects training and validation examples.  
We maintain **task corpora**:
- `core_corpus` (normal tasks)
- `edge_corpus` (epistemic singularities)
- `regression_corpus` (things we refuse to break)

**Example format (recommended):**
```python
from dataclasses import dataclass

@dataclass
class TaskExample:
    task: str
    expected: dict  # optional structured expectations
    task_type: str
    difficulty: str
```

---

## A.3 Integration pattern: DSPy + Claude (Anthropic)

### A.3.1 Configure DSPy LM
DSPy supports multiple backends. For Claude usage, the exact adapter can vary by DSPy version.
Prefer a thin wrapper in `infra/dspy_lm.py` so you can swap adapters without touching business logic.

```python
import os, dspy

def configure_dspy():
    # Pseudocode: pick the adapter matching your DSPy version
    # Example if available: dspy.LM("anthropic/claude-3-5-sonnet-latest", api_key=...)
    lm = dspy.LM(
        model="anthropic/claude-sonnet",
        api_key=os.environ["ANTHROPIC_API_KEY"],
        max_tokens=2048,
        temperature=0.2,
    )
    dspy.configure(lm=lm)
```

**Hard requirement:**  
Pin DSPy version in `requirements.txt` and record it in experiment metadata.

---

## A.4 Prompt clusters: making optimization cost-effective

### A.4.1 Why prompt clusters
Optimizing prompts per configuration is too expensive.  
We cluster configs by the dimensions that *actually change the prompt*:

**Cluster key (recommended):**
- active frames set (sorted)
- VERIX strictness + compression level
- activation style (implicit/explicit/checklist)
- few-shot count bucket (0,1,2+)
- system prompt length tier

```python
import hashlib, json

def cluster_key(cfg) -> str:
    key = {
        "frames": sorted(cfg.framework.active_frames()),
        "verix": {"strictness": cfg.framework.verix_strictness, "level": cfg.framework.verix_level},
        "style": cfg.prompt.activation_style,
        "fewshot": min(cfg.prompt.fewshot_count, 2),
        "syslen": cfg.prompt.system_prompt_length,
    }
    blob = json.dumps(key, sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]
```

### A.4.2 Cache artifacts
Cache compiled prompts per cluster:
- `cache/prompts/<cluster_key>/compiled.json`
- include: instruction string, demos, version info, metric summary

**Invalidate cache when:**
- signature changes
- metric changes materially
- frame/VERIX guides change
- LM model changes

---

## A.5 Optimizers: which one when

DSPy has multiple optimizers; the names and availability depend on version.

### A.5.1 BootstrapFewShot (BFS)
Use when:
- You have a decent base prompt
- You need good demonstrations
- You want quick wins

Pattern:
- Provide small trainset
- Metric emphasizes format compliance + correctness
- Output is a demo set

### A.5.2 MIPRO / MIPROv2
Use when:
- You want systematic search over instructions + demos
- You can afford more LLM calls
- You care about non-obvious prompt changes

From DSPy docs, MIPROv2 is positioned as a strong general-purpose teleprompter for prompt/program optimization. (See DSPy docs.) 

### A.5.3 GEPA / reflective evolution
Use when:
- You have failures you want the model to reason about
- You want a self-critique loop
- You can sandbox outputs (prevent prompt injection)

---

## A.6 How to compile our analyzer (Level 2)

### A.6.1 Training step
Inputs:
- prompt cluster
- trainset (task examples)
- base module (CognitiveAnalyzer)
- metric

Outputs:
- compiled module (instructions + demos)
- metric report
- regression checks

```python
from dspy.teleprompt import MIPROv2

def compile_cluster(base_module, trainset, metric):
    opt = MIPROv2(metric=metric, auto="medium")
    compiled = opt.compile(base_module, trainset=trainset)
    return compiled
```

### A.6.2 Regression gate
Before accepting a compiled prompt:
- Must not regress `regression_corpus` beyond tolerance.
- Must not violate VERIX format compliance.
- Must not exceed token budget ceilings.

---

## A.7 Level 1: framework evolution (slow loop)

### A.7.1 Inputs
- Telemetry tables (configs → metric vectors)
- Pareto frontier snapshots
- Failure clusters (common failure modes)
- Impact factor analysis (from GlobalMOO)

### A.7.2 Outputs
- Proposed changes: frames, routing, defaults, schema tweaks
- Migration plan: config version bump + back-compat
- New tests: add to regression corpus

### A.7.3 Workflow
1) Aggregate last N weeks of runs
2) Identify stable Pareto improvements
3) Produce PR with:
   - config schema update
   - routing update
   - updated docs
   - updated tests

---

## A.8 Debugging DSPy in production

### A.8.1 Common failure modes
- **Metric drift** (labeling changed, or evaluators changed)
- **Overfitting to demos** (great on train, bad on edge cases)
- **Format gaming** (model optimizes for regex checks)
- **Cluster explosion** (too many clusters → no cache benefit)
- **Non-determinism** (temperature too high, missing seeding)

### A.8.2 Debug checklist
- Confirm: DSPy version pinned
- Confirm: LM model pinned
- Confirm: temperature <= 0.3 for optimization runs
- Inspect: compiled prompt length and demo selection
- Run: edge corpus and regression corpus side-by-side

---

## A.9 Ops: reproducibility + experiment tracking

Minimum metadata for every compile run:
- date, git commit, DSPy version, LM model name
- cluster key + config sample
- dataset snapshot hash
- metric function hash (e.g., sha256 of source file)

Store artifacts in:
- `results/dspy/<date>/<cluster_key>/...`

---

## A.10 Security + safety notes (prompt injection)

DSPy makes it easier to generate prompts and demos; it also increases injection surface.

Hard rules:
- Never compile on untrusted user content without sanitization.
- Never allow the model to modify system prompts directly (human review required).
- Keep compile pipelines separate from user-facing runtime.

---

## A.11 Quickstart (new engineer)
1) `pip install -r requirements.txt`
2) Set `ANTHROPIC_API_KEY`
3) Run `python -m cli.evaluate --mode audit --sample 10`
4) Run `python -m cli.dspy_compile --cluster <key> --train core_corpus`
5) Validate with `python -m cli.regression --cluster <key>`

---

## A.12 Reference: files + APIs (recommended)
- `optimization/dspy_level2.py` — compile prompts per cluster
- `optimization/dspy_level1.py` — framework evolution analysis
- `tasks/metrics.py` — metric bundle
- `cache/prompts/` — compiled prompt artifacts

---

# Appendix B — GlobalMOO Developer Guide (v1.1)
**Purpose:** onboarding + internal handoff for engineers integrating GlobalMOO into the VERILINGUA × VERIX optimization loop.  
**Scope:** concepts, API workflow, inverse optimization loop, objective design, constraints, debugging, ops.

> **Mental model**
> - You have **inputs** = configuration vector (frames, strictness, prompt knobs, etc.)
> - You have **outputs** = measured metrics (accuracy, tokens, robustness, etc.)
> - You want not one optimum but the **trade-off surface** (Pareto frontier)
> - GlobalMOO learns a surrogate and can propose new inputs that satisfy multi-objective targets efficiently.

---

## B.1 GlobalMOO in this project: what it does

GlobalMOO is the **outer optimizer**. It proposes configurations, we evaluate them by running Claude through DSPy-built prompts, and we feed results back. Over time it:
- finds **Pareto-efficient** configs faster than naive evolutionary search
- supports **inverse asks** (“find inputs that hit these targets”)
- provides **impact factors** (input → output influence) to guide framework evolution

> Note: public documentation availability varies; use this appendix + the SDK you have in your environment as the source of truth.

---

## B.2 Core concepts

### B.2.1 Model, Project, Trial (terminology)
Most GlobalMOO workflows revolve around:
- **Model**: defines the dimensionality and overall “problem”
- **Project**: defines input bounds/types and initial sampling
- **Trial**: a set of evaluated cases (inputs + outputs) for optimization

### B.2.2 Inputs and outputs
- Inputs are the config vector (discrete + categorical + bounded ints).
- Outputs are metric vectors (floats; some minimized, some maximized).

**Best practice:** normalize outputs to stable ranges (0..1 for most quality metrics; raw values for tokens/latency but with sane scales).

### B.2.3 Objective styles
Two common patterns:
1) **Threshold objectives**: accuracy ≥ 0.85, tokens ≤ 500, etc.  
2) **Pareto exploration**: minimize tokens while maximizing robustness, etc.

We primarily use **threshold objectives** during inverse suggestion loops, and **Pareto exploration** for frontier mapping.

---

## B.3 The standard integration workflow (Python SDK style)

### B.3.1 Setup
- Install SDK (name depends on your internal distribution).
- Configure API key in environment variables.

### B.3.2 Create model + project
Pseudocode (aligns with the SDK patterns used in your existing integration code):

```python
from globalmoo.client import Client
from globalmoo.credentials import Credentials
from globalmoo.request.create_model import CreateModel
from globalmoo.request.create_project import CreateProject
from globalmoo.enums.input_type import InputType

credentials = Credentials(
    api_key=os.environ["GLOBALMOO_API_KEY"],
    base_uri="https://api.globalmoo.ai/api",
)
client = Client(credentials=credentials)

model = client.execute_request(CreateModel(name="VERILINGUA_VERIX_Optimizer"))

project = client.execute_request(CreateProject(
    model_id=model.id,
    input_count=len(INPUT_BOUNDS),
    minimums=[b.min for b in INPUT_BOUNDS],
    maximums=[b.max for b in INPUT_BOUNDS],
    input_types=[InputType.INTEGER] * len(INPUT_BOUNDS),
    categories=[],
))
```

### B.3.3 Evaluate initial cases
GlobalMOO typically provides initial input cases. For each:
1) Build config from vector
2) Build prompt via DSPy cluster cache (or compile if missing)
3) Execute Claude
4) Score metrics
5) Return output vector

### B.3.4 Load output cases (create a trial)
```python
from globalmoo.request.load_output_cases import LoadOutputCases

trial = client.execute_request(LoadOutputCases(
    model_id=model.id,
    project_id=project.id,
    output_count=len(OUTPUT_SCHEMA),
    output_cases=output_cases,
))
```

### B.3.5 Define objectives
```python
from globalmoo.request.load_objectives import LoadObjectives
from globalmoo.enums.objective_type import ObjectiveType

objective = client.execute_request(LoadObjectives(
    model_id=model.id,
    project_id=project.id,
    trial_id=trial.id,
    objectives=TARGETS,
    objective_types=OBJECTIVE_TYPES,
    initial_input=input_cases[-1],
    initial_output=output_cases[-1],
    minimum_bounds=[-0.1]*len(TARGETS),
    maximum_bounds=[0.1]*len(TARGETS),
    desired_l1_norm=0.0,
))
```

**Debug note:** `objective_types` must match the SDK’s enum; verify the names in your installed version.

---

## B.4 The inverse suggestion loop

### B.4.1 Suggest → evaluate → report
```python
from globalmoo.request.suggest_inverse import SuggestInverse
from globalmoo.request.load_inversed_output import LoadInversedOutput

for _ in range(max_iterations):
    inv = client.execute_request(SuggestInverse(
        model_id=model.id,
        project_id=project.id,
        trial_id=trial.id,
        objective_id=objective.id,
    ))

    cfg = FullConfig.from_vector(inv.input)
    out = evaluation_engine.evaluate_corpus(cfg)

    inv2 = client.execute_request(LoadInversedOutput(
        model_id=model.id,
        project_id=project.id,
        trial_id=trial.id,
        objective_id=objective.id,
        output=out.to_vector(),
    ))

    if getattr(inv2, "should_stop", lambda: False)():
        break
```

### B.4.2 Parallelization
LLM evaluation is expensive; parallelize carefully:
- Batch suggestions (if SDK supports)
- Evaluate in a worker pool with concurrency limits
- Preserve ordering and attach run IDs

---

## B.5 Objective engineering (how not to fool yourself)

### B.5.1 The “optimization theater” trap
If your metrics can be gamed, they will be.  
Mitigations:
- include **robustness** objectives (edge corpus)
- include **consistency** objectives (cross-claim checks)
- include **human spot checks** for random samples
- include a **regression corpus** that must not degrade

### B.5.2 Recommended output schema (v1.1)
MECE grouping of outputs:

**(1) Correctness**
- `task_accuracy`
- `math_accuracy`

**(2) Epistemics**
- `calibration_score` (minimize)
- `epistemic_consistency`

**(3) Transparency / Compliance**
- `format_compliance`
- `ground_chain_validity`

**(4) Efficiency**
- `total_tokens` (minimize)
- `latency_seconds` (minimize)

**(5) Robustness**
- `edge_case_robustness`

**(6) Style / Fit**
- `focus_score`
- `nuance_appropriateness`

> Keep the number of outputs small (≈10–14). Too many dims slow learning and encourage overfitting.

### B.5.3 Constraints vs objectives
Prefer:
- **constraints** for hard requirements (e.g., must include VERIX confidence)
- **objectives** for tunable trade-offs (e.g., tokens vs nuance)

---

## B.6 The Three-MOO Cascade (operational view)

### B.6.1 Phase A — structure selection
Goal: select a *framework structure* (which frames exist, which routing rules, which schema features).  
Implementation: cheap proxy scoring + limited LLM calls.

### B.6.2 Phase B — edge discovery
Goal: find boundaries where performance collapses or constraints break.  
GlobalMOO is used as a boundary-finder:
- maximize “distance to failure”
- probe conflict regions (frame disagreement)
- estimate stability radius (local robustness)

### B.6.3 Phase C — production frontier
Goal: full Pareto frontier within feasible region from Phase B.  
Deliverable: mode library (audit/speed/research/etc.) backed by metrics.

---

## B.7 Impact factors (turning optimization into insight)
After enough evaluations, GlobalMOO can estimate **which inputs matter**.

Use impact factors to:
- prune dead parameters
- identify high-leverage routing rules
- detect interactions (frame combos that matter)

Feed the findings to DSPy Level 1 framework evolution.

---

## B.8 Debugging GlobalMOO runs

### B.8.1 Common failure modes
- **No feasible solutions**: targets impossible; loosen constraints
- **Non-stationary metrics**: evaluation rubric changed mid-run
- **Stuck suggestions**: too-tight bounds or discrete jumps too coarse
- **Surrogate mismatch**: outputs noisy; increase repeats per config

### B.8.2 Practical debug checklist
- Validate input bounds and types (ints vs categories)
- Validate output vector ordering and scaling
- Repeat evaluation of the same config 3–5x to estimate noise
- Log all requests/responses with run IDs (no keys)

---

## B.9 Ops: run scheduling + governance

### B.9.1 Suggested cadence
- Daily: collect telemetry from real usage
- Weekly: Phase C production optimization (short run)
- Monthly: Phase A + Phase B refresh (structural review)

### B.9.2 Artifact storage
Store:
- input vectors, configs, prompts, model IDs, project IDs
- output vectors + metric breakdowns
- Pareto snapshots
- impact factor reports

---

## B.10 Fallbacks when GlobalMOO is unavailable
If API access is down:
- use cached mode library (most of the time this is enough)
- fall back to `pymoo` NSGA-II for exploration (slower)
- or run random search constrained by known safe bounds (Phase B)

---

## B.11 Security + reliability
- Never commit API keys.
- Rotate keys via CI secrets.
- Rate-limit and exponential backoff.
- Treat all outputs as potentially sensitive; store securely.

---

## B.12 Quickstart (new engineer)
1) Set `GLOBALMOO_API_KEY` and `ANTHROPIC_API_KEY`
2) Run `python -m cli.optimize --phase c --iters 25` (smoke test)
3) Validate you can create: model → project → trial → objective
4) Run a tiny inverse loop (5 iterations) and confirm outputs ingest
