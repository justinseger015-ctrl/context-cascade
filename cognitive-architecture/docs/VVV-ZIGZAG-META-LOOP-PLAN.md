# VVV Zig-Zag Meta-Loop Plan (RMIS)

## Recursive Meta-Improvement System (RMIS)

This document describes the formalized recursive improvement strategy for the foundry meta-tools.

---

## Foundational Axioms

### A0 - Everything is an Artifact
Every skill/agent/command/script prompt is an **artifact** with:
- `source` (text/spec/prompt)
- `tests/evals` (how we measure "better")
- `version` (git hash)

### A1 - Improvements Must Be Measurable
No patch merges without running evals. "Better" means **score up** on a defined scorecard.

### A2 - Local Optimization First, Then Cross-Pollination
Each component is improved **in isolation** until diminishing returns, *then* you use it to improve other components.

### A3 - Dogfooding is Mandatory at Each Tier
A tool must eventually try to improve **itself** (prompt level first, then architecture level).

### A4 - Zig-Zag Beats One-Way Updates
Alternating improvements across components (PA - SF - AM) discovers gains a linear pipeline misses.

### A5 - Stop Criteria Are Explicit
A loop ends when improvement is below threshold for N iterations (or fails significance tests).

### A6 - Safety Rail: Reversible, Logged, Bounded
All changes are:
- reversible (git)
- logged (what changed + why)
- bounded (token budget / iteration caps)

---

## Components (Named Labels)

| Label | Full Name | Function |
|-------|-----------|----------|
| **PA** | Prompt Architect | Rewrites prompts/docs for clarity/power/consistency |
| **SF** | Skill Forge | Creates/edits skills; engineering focus |
| **AM** | Agent Maker | Creates/edits agents; structural composition |
| **CMD** | Commands | Plugin commands' prompts/docs (245 total) |
| **DOCS** | Documents | Skill/agent documents and specs |
| **HOOKS** | Hooks | Scripts/hooks with embedded prompts |

---

## The Loop System (L0-L8)

### Loop L0: Baseline and Scorecard (Foundation)

**Purpose:** Establish "what is better" before recursion.

```
Inputs: current artifacts
Process: run eval suite, record baseline metrics
Outputs: baseline scorecard + regression gates
```

**Metrics:**
- Task success rate
- Constraint adherence
- VVV compliance (VERIX grounding ratio)
- Token cost
- L2 purity
- Schema validity

---

### Loop L1: Prompt Architect Self-Refinement (PA -> PA)

**Purpose:** Make PA maximally strong as a prompt rewriter.

```
Operation: PA reviews its own docs/prompts and improves them
Stop: delta < 2% (diminishing returns)
```

---

### Loop L2: Prompt-Upgrade Skill Forge (PA -> SF)

**Purpose:** Rewrite SF's prompts/docs using best PA.

```
1. PA rewrites SF prompts/docs
2. Run SF unit tests/evals
3. Accept patch if score increases
```

---

### Loop L3: Skill Forge Dogfooding (SF -> SF)

**Purpose:** SF improves its own architecture/prompt structure once prompt-level is saturated.

```
Operation: SF proposes structural changes to itself
           (templates, modules, eval hooks, prompt composition)
Stop: delta < 2%
```

---

### Loop L4: Core Zig-Zag Co-Evolution (SF <-> PA)

**Purpose:** The engine that produces "gains we aren't imagining."

```
CYCLE:
1. SF improves PA (structural + operational improvements)
2. PA improves SF (prompt clarity, language consistency)
3. Each side dogfoods after being updated
4. Repeat until convergence
```

This is the critical loop - alternating improvements discover compound gains.

---

### Loop L5: Add Agent Maker (PA+SF -> AM -> AM)

**Purpose:** Once PA and SF are "strong," bring AM into the co-evolution.

```
Stages:
1. PA rewrites AM prompts/docs
2. SF improves AM architecture/tooling
3. AM dogfoods (AM -> AM)
4. Repeat until diminishing returns
```

---

### Loop L6: Global Prompt Rewrite (PA -> CMD + DOCS)

**Purpose:** Apply evolved "language" across the whole plugin.

```
Operation:
- PA rewrites ALL commands (245)
- PA rewrites ALL agent docs (217)
- PA rewrites ALL skill docs (226)
- Run eval suite for regressions
```

---

### Loop L7: Global Structural Upgrade (AM + SF -> Agents + Skills)

**Purpose:** Do structural improvements now that prompt-level is unified.

```
Operation:
- AM improves all agents (roles, interfaces, IO schemas)
- SF improves all skills (tool contracts, modularity, test harness)
- Run integration tests + scenario evals
```

---

### Loop L8: Embedded Prompt Sweep (PA -> HOOKS)

**Purpose:** Find "hidden prompts" in scripts/hooks and upgrade them.

```
Operation:
- Scan repo for prompt-like strings
- PA rewrites
- Run relevant tests
```

---

## Visual Loop Map

```
                 +---------------------------+
                 | L0: BASELINE + SCORECARD  |
                 +-------------+-------------+
                               |
               +---------------+---------------+
               |                               |
       +-------v-------+               +-------v-------+
       | L1: PA -> PA  |               | L3: SF -> SF  |
       | (self-refine) |               | (dogfood)     |
       +-------+-------+               +-------+-------+
               |                               |
       +-------v-------+               +-------^-------+
       | L2: PA -> SF  |               |               |
       | (prompt fix)  +---------------+               |
       +---------------+                               |
                                                       |
               +---------------------------------------+
               |           L4: ZIG-ZAG                 |
               |                                       |
               |   SF* --[improve]--> PA  ===> PA*     |
               |                       |               |
               |   PA* --[dogfood]--> PA* ===> PA**    |
               |                       |               |
               |   PA** --[improve]--> SF* ===> SF**   |
               |                       |               |
               |   SF** --[dogfood]--> SF** ===> SF*** |
               |                       |               |
               |   REPEAT until diminishing returns    |
               +---------------+-----------------------+
                               |
               +---------------v---------------+
               | L5: PA+SF --> AM --> AM       |
               | (agent maker optimization)    |
               +---------------+---------------+
                               |
               +---------------v---------------+
               | L6: PA --> CMD + DOCS         |
               | (global prompt rewrite)       |
               +---------------+---------------+
                               |
               +---------------v---------------+
               | L7: AM+SF --> Agents + Skills |
               | (global structural upgrade)   |
               +---------------+---------------+
                               |
               +---------------v---------------+
               | L8: PA --> HOOKS              |
               | (embedded prompt sweep)       |
               +-------------------------------+
```

---

## Developer API (Pseudo-Code)

```python
Artifact = {
    id: str,
    type: str,          # "skill" | "agent" | "command" | "hook"
    source_text: str,
    tests: List[Test],
    metrics: Scorecard,
    version: str        # git hash
}

def Improve(improver: Artifact, target: Artifact) -> Patch:
    """Use improver to generate improvement patch for target."""
    pass

def Evaluate(patch: Patch, eval_suite: List[Test]) -> Scorecard:
    """Run tests and return scorecard."""
    pass

def Accept(scorecard: Scorecard, baseline: Scorecard) -> bool:
    """Returns True if scorecard beats baseline and passes gates."""
    return scorecard.overall > baseline.overall and scorecard.passes_gates()

def RunLoop(loop_name: str, improver: Artifact, target_set: List[Artifact]) -> Artifact:
    baseline = Evaluate(target_set)
    iteration = 0
    while not diminishing_returns(iteration):
        patch = Improve(improver, target_set)
        score = Evaluate(patch)
        if Accept(score, baseline):
            Commit(patch)
            baseline = score
        else:
            Reject(patch)
        iteration += 1
    return best_version

def diminishing_returns(iteration: int, threshold: float = 0.02) -> bool:
    """Returns True if delta < threshold for last 3 iterations."""
    pass
```

---

## Expected Compound Gains

| Phase | Loop | Prompt Gain | Structural Gain | Cumulative |
|-------|------|-------------|-----------------|------------|
| 1 | L1 (PA->PA) | 15-20% | - | 15-20% |
| 2 | L2 (PA->SF) | 15-20% | - | 30-40% |
| 3 | L3 (SF->SF) | - | 10-15% | 40-55% |
| 4 | L4 (zig-zag) | 10-15% | 10-15% | 60-85% |
| 5 | L5 (AM) | 10-15% | 10-15% | 80-115% |
| 6-8 | Global | 20-30% | 10-20% | 100-170% |

The final system could be **2-3x better** than the starting point.

---

## Execution Status

- [ ] L0: Baseline scorecard established
- [ ] L1: PA self-optimization (PA -> PA)
- [ ] L2: PA -> SF prompt upgrade
- [ ] L3: SF dogfooding (SF -> SF)
- [ ] L4: Zig-zag co-evolution (SF <-> PA)
- [ ] L5: Agent Maker optimization
- [ ] L6: Global prompt rewrite (245 commands, 217 agents, 226 skills)
- [ ] L7: Global structural upgrade
- [ ] L8: Embedded prompt sweep
- [ ] Post: Ultrathink analysis

---

## Key Insight: Why This Works

The system exploits **three orthogonal improvement dimensions**:

1. **Language/Prompt Quality (PA)** - How clearly instructions are expressed
2. **Architectural Structure (SF)** - How components are organized
3. **Behavioral Design (AM)** - How agents coordinate and act

By recursively improving each, then cross-applying, you capture gains that no single-pass optimization could find. The "zigzag" ensures improvements in one dimension get propagated to enhance the others.

---

## Biological Mental Model

Think: **adaptive immune system / evolution**

- **Mutations** = prompt/structure edits
- **Selection** = eval harness + scorecard
- **Inheritance** = committing the best patch
- **Speciation** = splitting skills/agents into specialized variants
- **Dogfooding** = organism evolves its own mutation operator

---

## Cognitive Architecture Integration (DSPy + VCL Evolution)

The RMIS dogfooding loops generate rich data that feeds into the cognitive architecture's two-layer optimization system.

### Data Flow Architecture

```
                      RMIS LOOPS (L0-L8)
                            |
                            | (eval outcomes, VERIX claims, configs)
                            v
    +-------------------+---+---+-------------------+
    |                   |       |                   |
    v                   v       v                   v
+--------+        +--------+  +--------+      +--------+
| DSPy   |        | DSPy   |  | Language|     | Two-   |
| Level 2|        | Level 1|  | Evolution|    | Stage  |
| (cache)|        | (struct)|  | (VCL)   |    | MOO    |
+--------+        +--------+  +--------+      +--------+
    |                   |         |               |
    | (minutes)         | (monthly)| (daily)      | (3-day)
    v                   v         v               v
+-----------------------------------------------------------+
|                    OPTIMIZED CONFIGS                       |
|   (named_modes, frame_mappings, verix_patterns)           |
+-----------------------------------------------------------+
                            |
                            v
                    APPLY TO NEXT RMIS CYCLE
```

### Layer Responsibilities

| Layer | Cadence | Input from RMIS | Output | Files |
|-------|---------|-----------------|--------|-------|
| **DSPy Level 2** | Minutes | Cluster keys + prompts | Cached compiled prompts | `dspy_level2.py` |
| **DSPy Level 1** | Monthly | Aggregated telemetry | EvolutionProposals | `dspy_level1.py` |
| **Language Evolution** | Daily | VERIX claims + success | Pattern effectiveness | `language_evolution.py` |
| **Two-Stage MOO** | 3-Day | TelemetryStore batch | Named modes | `two_stage_optimizer.py` |

### RMIS -> Telemetry Mapping

Each evaluation in L0-L8 produces telemetry:

```python
# For each eval task (PA-001, AC-001, etc.)
ExecutionTelemetry(
    task_id="PA-001",
    config_vector=[...],           # 14-dim configuration used
    active_frames=["evidential", "aspectual"],
    verix_strictness=1,            # MODERATE
    task_success=True,             # From claude-as-judge
    aggregate_frame_score=0.85,    # Frame compliance
    verix_compliance_score=0.90,   # VERIX adherence
    skill_name="prompt-architect", # Which skill tested
)
```

### Language Evolution Data Capture

Every skill evaluation also feeds Language Evolution:

```python
# For each skill output containing VERIX claims
LanguageEvolutionOptimizer.analyze_execution(
    output="[assert|neutral] Intent analyzed... [conf:0.9]",
    context="prompt-architect",     # Skill context
    success=True,                   # From eval result
    config_vector=[...],            # Config used
)
```

This captures:
- **VERIX patterns**: Which `[illocution|affect]` combos work
- **Frame effectiveness**: Which frames succeed in which contexts
- **Illocution-context mapping**: Best speech acts per task type

### Integration Points in Loop System

```
L0 (Baseline)
    |
    +---> TelemetryStore.store() [initial data batch]
    |
L1-L5 (Dogfooding Loops)
    |
    +---> Per-iteration:
    |       TelemetryAggregator.record_outcome()
    |       LanguageEvolutionOptimizer.analyze_execution()
    |
    +---> Per-loop-completion:
    |       LanguageEvolutionOptimizer.evolve() [daily]
    |       DSPyLevel1Analyzer.analyze() [if monthly]
    |
L6-L8 (Global Sweeps)
    |
    +---> TwoStageOptimizer.run_with_telemetry()
    |       [Major 3-day optimization cycle]
    |
    +---> Distill named_modes for next RMIS round
```

### Why This Integration Matters

1. **Volume**: One RMIS run (L0-L8) generates 500+ eval telemetry points
2. **Diversity**: Tests prompt-level AND structural changes
3. **Ground Truth**: Claude-as-judge provides real success signals
4. **VCL Discovery**: Pattern analysis finds what VERIX constructs work
5. **Feedback Loop**: Improved VCL -> Better prompts -> Higher scores

### Expected Data Yield

| RMIS Phase | Telemetry Records | VERIX Claims | Language Patterns |
|------------|-------------------|--------------|-------------------|
| L0 (100 evals) | 100 | ~500 | ~50 unique |
| L1-L5 (5 loops x 50) | 250 | ~1250 | ~100 unique |
| L6-L8 (688 artifacts) | 688 | ~3440 | ~200 unique |
| **Total per RMIS** | **~1000** | **~5000** | **~300 unique** |

This is equivalent to ~30 days of normal usage compressed into one RMIS cycle.

### Implementation Hooks

The following hooks capture RMIS data for the cognitive architecture:

```python
# In cli_evaluator.py - after each eval
def on_eval_complete(task_id, skill, result, config):
    # 1. Store telemetry
    telemetry = ExecutionTelemetry(
        task_id=task_id,
        skill_name=skill,
        config_vector=config.to_vector(),
        task_success=result.passed,
        ...
    )
    TelemetryStore().store(telemetry)

    # 2. Analyze language patterns
    if hasattr(result, 'output'):
        LanguageEvolutionOptimizer().analyze_execution(
            output=result.output,
            context=skill,
            success=result.passed,
            config_vector=config.to_vector(),
        )
```

### Post-RMIS Optimization Cycle

After L8 completes:

```bash
# Run two-stage optimization with accumulated telemetry
python cognitive-architecture/optimization/two_stage_optimizer.py

# Expected output:
# - storage/two_stage_optimization/named_modes.json
# - storage/language_evolution/evolution_state.json
# - storage/proposals/proposals.json
```

---

## Production Vision: VCL-ified Subagent Prompts + Pipeline Telemetry

The RMIS system serves a larger purpose: **Claude Code IS a prompt writer** whenever it spawns subagents.

### The Core Insight

```
Current:
  Task("Explore", "find all API endpoints", "general-purpose")
                   ^
                   |
        This IS a prompt, written ad-hoc in plain English

Future:
  Task("Explore", VCL_Prompt({
    intent: "codebase_exploration",
    frames: ["evidential", "spatial"],
    constraints: ["API", "endpoints", "REST"],
    verix: "[query|neutral] Locate API endpoints [ground:codebase]"
  }), "general-purpose")
                   ^
                   |
        Structured VCL prompt, optimizable by DSPy
```

### Two Data Sources

1. **RMIS Dogfooding (Manual/Scheduled)**
   - Runs L1-L8 loops on foundry skills
   - Generates ~1000 telemetry records per run
   - Feeds VCL pattern discovery

2. **Daily Automated Pipelines (Continuous)**
   - Content pipeline, research synthesis, etc.
   - Same prompts executed daily in sequence
   - Massive telemetry from real usage
   - A/B testing of prompt variants

### Pipeline Telemetry Architecture

```
+------------------+     +------------------+     +------------------+
| Daily Pipeline 1 |     | Daily Pipeline 2 |     | Daily Pipeline N |
| (Content)        |     | (Research)       |     | (Trading)        |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                        |
         v                        v                        v
    +----+----+              +----+----+              +----+----+
    | VCL     |              | VCL     |              | VCL     |
    | Prompt  |              | Prompt  |              | Prompt  |
    | v1.2    |              | v2.1    |              | v1.0    |
    +----+----+              +----+----+              +----+----+
         |                        |                        |
         v                        v                        v
+--------+------------------------+------------------------+--------+
|                    RMIS TELEMETRY HARNESS                         |
|  - Capture outcome (success/failure)                              |
|  - Capture output (VERIX claims)                                  |
|  - Capture config (which prompt version)                          |
+--------+------------------------+------------------------+--------+
         |                        |                        |
         v                        v                        v
+------------------+     +------------------+     +------------------+
| Language         |     | DSPy Level 2    |     | Two-Stage        |
| Evolution        |     | (A/B variants)   |     | Optimizer        |
+------------------+     +------------------+     +------------------+
         |                        |                        |
         +------------------------+------------------------+
                                  |
                                  v
                    +---------------------------+
                    | IMPROVED VCL PROMPTS      |
                    | (deployed to pipelines)   |
                    +---------------------------+
```

### A/B Testing Framework

```python
# Pipeline step with A/B testing
class PipelineStep:
    prompt_variants: Dict[str, VCLPrompt] = {
        "control": VCLPrompt(version="v1.0", ...),
        "treatment_a": VCLPrompt(version="v1.1", ...),
        "treatment_b": VCLPrompt(version="v1.2", ...),
    }

    def execute(self):
        # Select variant (weighted by historical performance)
        variant = self.select_variant()

        # Execute with telemetry
        result = self.run_with_telemetry(variant)

        # Record outcome
        harness.on_eval_complete(
            loop="PIPELINE",
            skill=self.step_name,
            task_id=f"{self.pipeline}_{self.run_id}",
            passed=result.success,
            output=result.output,
            metrics={"variant": variant.version}
        )
```

### VCL Prompt Schema

```python
@dataclass
class VCLPrompt:
    """A VCL-formatted prompt for subagent invocation."""
    version: str
    intent_type: str                    # codebase_exploration, code_generation, etc.
    active_frames: List[str]            # evidential, aspectual, etc.
    constraints: List[str]              # Domain constraints
    verix_statement: str                # The core VERIX-annotated instruction
    compression_level: str = "L2"       # Output format
    grounding_required: bool = True     # Must ground claims

    def to_prompt(self) -> str:
        """Compile to executable prompt string."""
        return f"""[Context: {self.intent_type}]
[Frames: {', '.join(self.active_frames)}]
[Constraints: {', '.join(self.constraints)}]

{self.verix_statement}

[Output: {self.compression_level} compression, {'grounded' if self.grounding_required else 'ungrounded'}]"""
```

### Daily Pipeline Examples

| Pipeline | Cadence | Steps | Prompts to Optimize |
|----------|---------|-------|---------------------|
| Content Pipeline | Daily 6AM | 5 | zeitgeist_analysis, transcript_synthesis, blog_draft |
| Research Synthesis | Daily 8AM | 3 | source_gather, synthesis, report_gen |
| Trading Analysis | Hourly | 4 | market_scan, signal_detect, risk_eval, action_rec |
| Hackathon Prep | Weekly | 6 | trend_scan, idea_gen, scope_def, tech_stack, pitch_draft |

### Expected Telemetry Volume

| Source | Frequency | Records/Day | Records/Month |
|--------|-----------|-------------|---------------|
| Content Pipeline | 1x daily | 5 | 150 |
| Research Synthesis | 1x daily | 3 | 90 |
| Trading Analysis | 24x daily | 96 | 2,880 |
| RMIS Dogfooding | 1x weekly | 143 (1000/7) | 4,300 |
| **Total** | - | **~250** | **~7,500** |

This continuous telemetry stream enables:
- Daily language evolution cycles
- Weekly DSPy L1 proposals
- Monthly named mode refinement
- Quarterly VCL spec updates

### Implementation Phases

1. **Phase 1 (Current)**: RMIS dogfooding with telemetry capture
2. **Phase 2**: VCL prompt schema + compiler
3. **Phase 3**: Pipeline integration + A/B framework
4. **Phase 4**: Automated daily optimization cycle
5. **Phase 5**: Self-evolving VCL spec based on pattern analysis

---

*This plan represents a systematic approach to recursive self-improvement that compounds gains across prompt, structural, and agent dimensions.*
