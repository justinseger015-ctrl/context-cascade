# COGNITIVE ARCHITECTURE SYSTEM INDEX

**Version**: 2.0.0
**Updated**: 2025-12-28
**System**: MOO x DSPy x VERILINGUA x VERIX

---

## SYSTEM OVERVIEW

This is a **dual-layer optimization system** for improving AI prompts and the language that expresses them:

```
                     OPTIMIZATION LAYERS
                            |
         +------------------+------------------+
         |                                     |
    LAYER 1 (SLOW)                       LAYER 2 (FAST)
    Language Evolution                   Prompt Expression
    - Monthly cadence                    - Per-cluster caching
    - Structural changes                 - Config-based compilation
    - Frame selection                    - Task-specific prompts
         |                                     |
         +------------------+------------------+
                            |
                    TWO-STAGE MOO
                            |
              +-------------+-------------+
              |                           |
        GlobalMOO (5D)              PyMOO (14D)
        Broad exploration           Local refinement
        API subscription            NSGA-II algorithm
```

---

## DIRECTORY STRUCTURE

```
cognitive-architecture/
|
+-- core/                          # FOUNDATION (all modules depend on these)
|   +-- config.py                  # FrameworkConfig, PromptConfig, VectorCodec (14D)
|   +-- verilingua.py              # 7 cognitive frames from natural languages
|   +-- verix.py                   # Epistemic notation system
|   +-- prompt_builder.py          # Prompt construction from config
|   +-- runtime.py                 # Runtime execution engine
|
+-- optimization/                  # OPTIMIZATION LAYER
|   +-- dspy_level1.py             # Layer 1: Monthly structural evolution
|   +-- dspy_level2.py             # Layer 2: Per-cluster prompt caching
|   +-- two_stage_optimizer.py     # GlobalMOO (5D) + PyMOO NSGA-II (14D)
|   +-- globalmoo_client.py        # GlobalMOO API client
|   +-- cascade.py                 # CASCADE optimization algorithm
|   +-- distill_modes.py           # Mode distillation (named modes)
|   +-- task_prompt_optimizer.py   # Task-specific prompt optimization
|   +-- skill_execution_tracker.py # Execution tracking for feedback
|   +-- language_evolution.py      # Language evolution proposals
|   +-- cascade_optimizer.py       # Real cascade implementation
|   +-- real_cascade_optimizer.py  # Production cascade optimizer
|
+-- eval/                          # EVALUATION SYSTEM
|   +-- metrics.py                 # Metric definitions
|   +-- edge_cases.py              # Edge case testing
|   +-- consistency.py             # Consistency checking
|   +-- graders/                   # Grading systems
|       +-- deterministic.py       # Rule-based grading
|       +-- llm_judge.py           # LLM-based grading
|
+-- modes/                         # MODE SYSTEM
|   +-- library.py                 # Mode library
|   +-- selector.py                # Mode selection logic
|
+-- commands/                      # CLI COMMANDS
|   +-- mode.py                    # /mode command
|   +-- frame.py                   # /frame command
|   +-- verix.py                   # /verix command
|   +-- pareto.py                  # /pareto command
|
+-- hooks/                         # HOOK SYSTEM
|   +-- (integration hooks)
|
+-- storage/                       # PERSISTENT STORAGE
|   +-- two_stage_optimization/
|   |   +-- named_modes.json       # Distilled named modes
|   |   +-- stage1_pareto.json     # GlobalMOO Pareto front
|   |   +-- stage2_pareto.json     # PyMOO Pareto front
|   |   +-- two_stage_report.md    # Optimization report
|   |
|   +-- telemetry/                 # Layer 1 telemetry data
|   +-- prompts/                   # Layer 2 prompt cache
|   +-- cascade/                   # CASCADE results
|   +-- proposals/                 # Evolution proposals
|
+-- tasks/                         # EVALUATION TASKS
|   +-- core_corpus.jsonl          # Core test tasks
|   +-- edge_corpus.jsonl          # Edge case tasks
|   +-- holdout.jsonl              # Holdout test set
|
+-- skills/                        # SKILL INTEGRATION
|   +-- cognitive-mode/SKILL.md    # Cognitive mode skill
|
+-- docs/                          # DOCUMENTATION
|   +-- SYSTEM-INDEX.md            # This file
|   +-- VERILINGUA-GUIDE.md        # VERILINGUA documentation
|   +-- VERIX-GUIDE.md             # VERIX documentation
|   +-- META-LOOP-BOOTSTRAP-PLAN.md
|   +-- META-LOOP-BOOTSTRAP-RESULTS.md
|   +-- IMPROVEMENT-DELTA-METALOOP-STACK.md
|   +-- AUDIT-RESULTS-20251228.md
|
+-- tests/                         # TEST SUITE
    +-- test_config.py
    +-- test_verilingua.py
    +-- test_verix.py
    +-- test_prompt_builder.py
    +-- test_runtime.py
    +-- test_metrics.py
    +-- test_dspy.py
    +-- test_globalmoo.py
    +-- test_cascade.py
    +-- test_modes.py
```

---

## CORE COMPONENTS

### 1. VERILINGUA (7 Cognitive Frames)

**File**: `core/verilingua.py`
**Purpose**: Force explicit cognitive distinctions from natural languages

| Frame | Source Language | Forces | Example Markers |
|-------|-----------------|--------|-----------------|
| Evidential | Turkish (-mis/-di) | How do you know? | [witnessed], [reported], [inferred] |
| Aspectual | Russian (pfv/ipfv) | Complete or ongoing? | [complete], [ongoing] |
| Morphological | Arabic (trilateral) | Semantic decomposition | [root:], [derived:] |
| Compositional | German (compounds) | Build from primitives | [primitive:], [builds:] |
| Honorific | Japanese (keigo) | Audience calibration | [audience:], [formality:] |
| Classifier | Chinese (measure words) | Type and count | [type:], [measure:] |
| Spatial | Guugu Yimithirr | Absolute positioning | [path:], [location:] |

### 2. VERIX (Epistemic Notation)

**File**: `core/verix.py`
**Purpose**: Structured epistemic annotations for AI responses

**Format**: `[illocution|stance] content [conf:0.X] [state:X]`

| Strictness Level | Requirements |
|------------------|--------------|
| RELAXED (0) | Only illocution required |
| MODERATE (1) | Illocution + confidence |
| STRICT (2) | All fields required |

| Compression Level | Output Format |
|-------------------|---------------|
| L0_AI_AI | Emoji shorthand (machine-to-machine) |
| L1_AI_HUMAN | Annotated format (human inspector) |
| L2_HUMAN | Natural language (end user, lossy) |

### 3. VectorCodec (14-Dimensional Config)

**File**: `core/config.py`
**Purpose**: Stable config <-> vector mapping for optimization

**Dimensions**:
```
Index | Dimension          | Range | Description
------|--------------------| ------|------------------------
0     | evidential         | 0-1   | Evidential frame toggle
1     | aspectual          | 0-1   | Aspectual frame toggle
2     | morphological      | 0-1   | Morphological frame toggle
3     | compositional      | 0-1   | Compositional frame toggle
4     | honorific          | 0-1   | Honorific frame toggle
5     | classifier         | 0-1   | Classifier frame toggle
6     | spatial            | 0-1   | Spatial frame toggle
7     | verix_strictness   | 0-2   | RELAXED/MODERATE/STRICT
8     | compression_level  | 0-2   | L0/L1/L2
9     | require_ground     | 0-1   | Require evidence citations
10    | require_confidence | 0-1   | Require confidence values
11    | temperature        | 0-1   | Response temperature
12    | coherence_weight   | 0-1   | Weight for coherence scoring
13    | evidence_weight    | 0-1   | Weight for evidence scoring
```

---

## OPTIMIZATION SYSTEM

### Layer 1: Language Evolution (Monthly)

**File**: `optimization/dspy_level1.py`
**Cadence**: Monthly
**Scope**: Structural changes to prompt architecture

**Components**:
- `TelemetryAggregator`: Collects execution outcomes
- `DSPyLevel1Analyzer`: Analyzes patterns, proposes changes
- `EvolutionProposal`: Structured change proposals

**Proposal Types**:
- `FRAME_ACTIVATION`: Change default frames
- `VERIX_ADJUSTMENT`: Change VERIX defaults
- `PROMPT_STRUCTURE`: Change prompt template
- `COMPRESSION_LEVEL`: Change compression default
- `NEW_FRAME`: Propose new cognitive frame

### Layer 2: Prompt Expression (Minutes-Hours)

**File**: `optimization/dspy_level2.py`
**Cadence**: Minutes to hours
**Scope**: Per-cluster prompt compilation and caching

**Components**:
- `CompiledPrompt`: Cached prompt with metadata
- `ClusterCache`: LRU cache by cluster key
- `DSPyLevel2Optimizer`: Cache management

**Cluster Key**: `frame_set + verix_strictness + task_type`

### Two-Stage Optimization

**File**: `optimization/two_stage_optimizer.py`
**Purpose**: GlobalMOO exploration + PyMOO refinement

**Stage 1: GlobalMOO (5D)**
```
Dimensions: evidential, aspectual, verix_strictness, compression, require_ground
Method: API subscription (https://app.globalmoo.com/api)
Model ID: 2193
Project ID: 8318
Output: 100 Pareto solutions
```

**Stage 2: PyMOO NSGA-II (14D)**
```
Dimensions: All 14 config dimensions
Method: Evolutionary multi-objective optimization
Population: 200, Generations: 100
Crossover: SBX (eta=15), Mutation: PM (eta=20)
Output: 200 refined Pareto solutions
```

**Objectives** (4 total):
1. `task_accuracy` (maximize)
2. `token_efficiency` (maximize)
3. `edge_robustness` (maximize)
4. `epistemic_consistency` (maximize)

---

## NAMED MODES

**File**: `storage/two_stage_optimization/named_modes.json`

| Mode | Accuracy | Efficiency | Robustness | Consistency | Frames |
|------|----------|------------|------------|-------------|--------|
| audit | 0.960 | 0.763 | 0.890 | 0.950 | evidential, aspectual, morphological, classifier |
| speed | 0.734 | 0.950 | 0.760 | 0.584 | (none) |
| research | 0.980 | 0.824 | 0.950 | 0.950 | evidential, honorific, classifier, spatial |
| robust | 0.960 | 0.769 | 0.950 | 0.950 | evidential, aspectual, morphological, classifier |
| balanced | 0.882 | 0.928 | 0.950 | 0.950 | evidential, spatial |
| meta-loop | 0.970 | 0.780 | 0.920 | 0.980 | evidential, aspectual |

---

## GLOBALMOO API

**Base URL**: `https://app.globalmoo.com/api`
**Model ID**: 2193
**Project ID**: 8318

**Endpoints**:
- `POST /model/{id}/evaluate` - Submit config vector for evaluation
- `GET /model/{id}/pareto` - Get current Pareto front
- `GET /model/{id}/status` - Get optimization status

**Request Format**:
```json
{
  "config_vector": [0.9, 0.8, 1.5, 1.0, 0.7],
  "outcomes": {
    "task_accuracy": 0.85,
    "token_efficiency": 0.72,
    "edge_robustness": 0.91,
    "epistemic_consistency": 0.88
  }
}
```

---

## INTEGRATION WITH PLUGIN SYSTEM

### Skills That Use Cognitive Architecture

| Skill | Uses | Purpose |
|-------|------|---------|
| cognitive-mode | modes, frames | Switch cognitive modes |
| prompt-architect | Layer 2 | Optimize prompts |
| agent-creator | frames | Create agents with cognitive frames |
| skill-forge | frames | Create skills with frame markers |
| eval-harness | metrics | Gate changes with evaluation |

### Commands

| Command | File | Purpose |
|---------|------|---------|
| /mode | commands/mode.py | Select named mode |
| /frame | commands/frame.py | Activate/deactivate frames |
| /verix | commands/verix.py | Configure VERIX settings |
| /pareto | commands/pareto.py | View Pareto front |

---

## QUICK START

### Run Two-Stage Optimization

```bash
cd cognitive-architecture
python optimization/two_stage_optimizer.py
```

### Select a Named Mode

```python
from modes.library import ModeLibrary

library = ModeLibrary()
mode = library.get_mode("research")
config = mode.to_full_config()
```

### Build a Prompt with Frames

```python
from core.config import FrameworkConfig, PromptConfig, FullConfig
from core.prompt_builder import PromptBuilder

framework = FrameworkConfig(evidential=True, aspectual=True)
prompt = PromptConfig(verix_strictness=VerixStrictness.STRICT)
config = FullConfig(framework=framework, prompt=prompt)

builder = PromptBuilder(config)
system_prompt, user_template = builder.build("{task}", "coding")
```

### Record Telemetry for Layer 1

```python
from optimization.dspy_level1 import TelemetryAggregator

aggregator = TelemetryAggregator()
aggregator.record_outcome(
    config_vector=[0.9, 0.8, 0.1, 0.1, 0.1, 0.1, 0.1, 2.0, 1.0, 0.7, 0.5, 0.7, 0.6, 0.7],
    outcomes={"task_accuracy": 0.92, "token_efficiency": 0.78},
    task_type="coding"
)
aggregator.save()
```

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-12-28 | Meta-loop bootstrap, named modes, system index |
| 1.5.0 | 2025-12-28 | Two-stage optimization (GlobalMOO + PyMOO) |
| 1.0.0 | 2025-12-27 | Initial cognitive architecture |

---

*Generated: 2025-12-28*
*System: MOO x DSPy x VERILINGUA x VERIX*
