# VERILINGUA x VERIX x DSPy x GlobalMOO Integration Plan

## Executive Summary

This document outlines the integration of a **self-improving prompting architecture** into the existing Context Cascade plugin system. The system combines:

1. **VERILINGUA** - Cognitive frames from natural language distinctions
2. **VERIX** - Epistemic notation for auditable claims
3. **DSPy** - Programmatic prompt optimization
4. **GlobalMOO** - Multi-objective Pareto optimization

## Current System Integration Points

### Existing Components to Enhance

| Component | Current | Enhanced With |
|-----------|---------|---------------|
| **5-Phase Workflow** | intent -> prompt -> plan -> route -> execute | + VERILINGUA frame selection in Phase 2 |
| **Prompt Architect** | Evidence-based prompting | + VERIX notation enforcement |
| **Eval Harness** | Frozen gate for changes | + GlobalMOO metrics |
| **Foundry Skills** | prompt-forge, skill-forge, agent-creator | + DSPy Level 2 optimization |
| **Ralph Wiggum** | Persistence loops | + Three-MOO Cascade phases |
| **Meta Loop** | Recursive improvement | + Pareto frontier distillation |

### Architecture Alignment

```
EXISTING (Context Cascade)         ENHANCED (+ Cognitive Architecture)
========================           ================================

5-Phase Workflow                   5-Phase Workflow
    |                                  |
    v                                  v
intent-analyzer  ----------------> + VERILINGUA frame detection
    |                                  |
    v                                  v
prompt-architect ----------------> + VERIX notation injection
    |                              + Frame activation instructions
    v                                  |
planner          ----------------> + Config vector optimization
    |                              + DSPy cluster routing
    v                                  |
router           ----------------> + Mode selection (Pareto-derived)
    |                              + GlobalMOO target matching
    v                                  |
execute          ----------------> + Structured logging
                                   + Outcomes for optimization loop
```

## Implementation Phases

### Phase A: Core Infrastructure (Week 1)

1. **Config Dataclasses**
   - `FrameworkConfig` with frame toggles
   - `PromptConfig` with VERIX settings
   - `FullConfig` combining both
   - `VectorCodec` for stable vector mapping

2. **VERIX Parser**
   - Parse VERIX-formatted claims from responses
   - Extract: illocution, affect, ground, confidence, state
   - Format compliance scoring

3. **Frame Registry**
   - 7 initial frames (Russian aspect, Turkish evidential, etc.)
   - Activation instructions per frame
   - Compliance markers and scoring

4. **PromptBuilder**
   - Config -> prompts transformation
   - Frame activation injection
   - VERIX requirement injection

### Phase B: Evaluation System (Week 2)

1. **Core Metrics**
   - task_accuracy (deterministic + rubric)
   - token_efficiency (cost per task)
   - edge_case_robustness
   - epistemic_consistency

2. **Graders**
   - Deterministic: format, tokens, latency, regex
   - LLM Judge: rubric scoring (optional)

3. **Anti-Gaming**
   - Length normalization
   - Format compliance as sub-metric
   - Holdout regression set

4. **JSONL Logging**
   - Config vector
   - Prompt hash
   - Response
   - Token counts
   - All metrics

### Phase C: Optimization Integration (Week 3)

1. **DSPy Level 2**
   - Cluster configs by frame set + VERIX strictness
   - Compile prompts per cluster
   - Cache artifacts

2. **GlobalMOO Client**
   - Forward model: config -> outcomes
   - Inverse queries: targets -> configs
   - Impact factor extraction

3. **Three-MOO Cascade**
   - Phase A: Framework structure
   - Phase B: Edge discovery
   - Phase C: Production frontier

### Phase D: Mode Distillation (Week 4)

1. **Pareto Frontier Mapping**
   - Identify efficient configurations
   - Cluster by objective emphasis

2. **Named Modes**
   - Audit Mode: consistency + sourcing + strict VERIX
   - Speed Mode: low tokens/latency
   - Research Mode: accuracy + robustness
   - Math Mode: stepwise + consistency
   - Synthesis Mode: structure + clarity

3. **Mode Library**
   - YAML/JSON storage
   - Claude Code command integration
   - `/mode` command update

## File Structure

```
cognitive-architecture/
  core/
    verilingua.py         # Frame registry + routing
    verix.py              # Parser + compliance
    config.py             # Dataclasses + VectorCodec
    prompt_builder.py     # Config -> prompts
    runtime.py            # Claude client wrapper

  eval/
    metrics.py            # Objective functions
    graders/
      deterministic.py    # Format, tokens, latency
      llm_judge.py        # Rubric scoring
    edge_cases.py         # Curated adversarial corpus
    consistency.py        # Epistemic consistency

  optimization/
    globalmoo_client.py   # GlobalMOO SDK wrapper
    dspy_level2.py        # Per-cluster compile/cache
    dspy_level1.py        # Evolution analysis
    cascade.py            # Three-MOO orchestration
    distill_modes.py      # Pareto -> named modes

  modes/
    library.py            # Mode definitions
    selector.py           # Auto-selection heuristics

  storage/
    logs/                 # JSONL execution logs
    prompts/              # Cached compiled prompts
    results/              # Optimization artifacts

  tasks/
    core_corpus.jsonl     # Standard evaluation tasks
    edge_corpus.jsonl     # Adversarial tasks
    holdout.jsonl         # Regression suite (never optimized on)
```

## VERILINGUA Frames (Initial Set)

| Frame | Linguistic Source | Forces | Use When |
|-------|------------------|--------|----------|
| **Evidential** | Turkish -mis/-di | "How do you know?" | Claims need sourcing |
| **Aspectual** | Russian pfv/ipfv | "Complete or ongoing?" | Tracking progress |
| **Morphological** | Arabic trilateral roots | Semantic decomposition | Complex concepts |
| **Compositional** | German compounding | Primitives -> compounds | Building definitions |
| **Honorific** | Japanese keigo | Audience calibration | Documentation |
| **Classifier** | Chinese measure words | Object comparison | Selection tasks |
| **Spatial** | Guugu Yimithirr | Absolute positioning | Navigation/structure |

## VERIX Integration

### Statement Grammar

```
STATEMENT := ILLOCUTION + AFFECT + CONTENT + GROUND + CONFIDENCE + STATE
```

### Compression Levels

| Level | Audience | Example |
|-------|----------|---------|
| L0 | AI<->AI | Emoji shorthand |
| L1 | AI+Human Inspector | Annotated format |
| L2 | Human Reader | Natural language (lossy) |

### Integration with Responses

All Claude responses in optimized modes include:
- VERIX-tagged claims (machine-parseable)
- Ground chains for audit trail
- Confidence propagation

## GlobalMOO API Integration

### Environment Setup

```bash
# .env file
GLOBALMOO_API_KEY=your_key_here
GLOBALMOO_BASE_URI=https://api.globalmoo.ai/api
```

### Workflow

1. **Create Model + Project**
2. **Load Initial Cases** (seed data)
3. **Define Objectives** (thresholds or Pareto)
4. **Inverse Suggestion Loop** (suggest -> evaluate -> report)
5. **Extract Impact Factors** (input -> output sensitivity)

## Commands (New)

| Command | Purpose |
|---------|---------|
| `/mode <name>` | Select named mode (audit/speed/research/math/synthesis) |
| `/eval <task_type>` | Run evaluation on task corpus |
| `/optimize [--phase a\|b\|c]` | Run GlobalMOO optimization |
| `/pareto [--objective X]` | View Pareto frontier |
| `/frame <name>` | Activate specific VERILINGUA frame |
| `/verix [--level 0\|1\|2]` | Set VERIX compression level |

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Task accuracy | >90% | Deterministic + rubric |
| Calibration | <0.1 Brier | Confidence vs correctness |
| Token efficiency | 30% reduction | Baseline comparison |
| Edge robustness | >85% | Adversarial corpus |
| Epistemic consistency | >95% | Cross-claim checks |

## Migration Path

### Week 1: Foundation
- [ ] FullConfig + VectorCodec
- [ ] VERIX parser
- [ ] Frame registry (3 frames)
- [ ] PromptBuilder

### Week 2: Evaluation
- [ ] Metrics implementation
- [ ] Graders (deterministic)
- [ ] Edge corpus creation
- [ ] JSONL logging

### Week 3: Optimization
- [ ] GlobalMOO client
- [ ] DSPy Level 2 clustering
- [ ] Three-MOO Phase C

### Week 4: Modes
- [ ] Pareto mapping
- [ ] Mode distillation
- [ ] Command integration
- [ ] Documentation

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Optimization theater | Holdout set + human spot checks |
| Overfitting to corpus | Diverse tasks + regression suite |
| Robustness as cowardice | Reward useful uncertainty |
| Metric redundancy | Correlation tracking + pruning |

## Next Steps

1. **User provides GlobalMOO API key** -> Add to .env
2. **Create Python package** with core/ modules
3. **Implement VectorCodec** with stable ordering
4. **Build initial frame set** (3 frames minimum)
5. **Create task corpus** for evaluation

---

**Branch**: `feature/veralingua-moo-integration`
**Status**: Planning Complete - Ready for Implementation
**Version**: 1.0.0
