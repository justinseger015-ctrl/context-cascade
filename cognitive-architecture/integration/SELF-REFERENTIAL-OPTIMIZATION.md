# Self-Referential Optimization Blueprint

## Core Principle: Languages Optimizing Themselves

```
VERIX + VERILINGUA
        |
        v
    GlobalMOO (Multi-Objective Optimization)
        |
        v
    Better VERIX + VERILINGUA
        |
        v
    Better Prompts Using Languages
        |
        v
    Better Commands -> Subagents -> Skills -> Playbooks
```

## Phase 0: Language Self-Optimization

### 0.1 VERIX Notation Optimization

**Objectives for GlobalMOO**:
```yaml
project_id: verix-self-optimization
objectives:
  - name: epistemic_clarity
    description: How clearly does VERIX express confidence and grounding?
    direction: maximize
    weight: 0.35

  - name: parsing_accuracy
    description: Can VerixParser correctly extract all elements?
    direction: maximize
    weight: 0.25

  - name: token_efficiency
    description: Tokens per claim (lower is better)
    direction: minimize
    weight: 0.20

  - name: human_readability
    description: Can humans understand VERIX-annotated text?
    direction: maximize
    weight: 0.20

parameters:
  - name: notation_format
    type: categorical
    values: [L0_full, L1_compressed, L2_minimal, L3_hybrid]

  - name: ground_syntax
    type: categorical
    values: ["[ground:X]", "{source:X}", "<<X>>", "(ref:X)"]

  - name: confidence_syntax
    type: categorical
    values: ["[conf:0.X]", "{c:0.X}", "(p=0.X)", "[P:X%]"]

  - name: illocution_markers
    type: categorical
    values: [explicit_bracket, implicit_context, hybrid]
```

**Self-Referential Test**:
```python
# Optimize VERIX by USING VERIX to describe optimization results
def optimize_verix_with_verix():
    """
    Meta-optimization: Use VERIX notation to report on VERIX optimization.

    Example output after optimization:
    [assert|neutral] The optimized VERIX notation achieves 0.87 epistemic clarity
    [ground:globalmoo/pareto/verix-v2.0] [conf:0.92]

    [propose|emphatic] L3_hybrid format balances readability and precision
    [ground:moo/experiment/format-comparison] [conf:0.85] [state:recommended]
    """

    moo_client = GlobalMOOClient(use_mock=False)  # Use real API

    # Run optimization
    results = moo_client.optimize(
        project_id="verix-self-optimization",
        iterations=100,
        population_size=50
    )

    # Report results USING VERIX
    for point in results.pareto_frontier:
        verix_claim = f"""
[assert|neutral] Configuration {point.config_id} achieves:
  - Epistemic clarity: {point.outcomes['epistemic_clarity']:.2f} [ground:moo/eval/{point.config_id}]
  - Parsing accuracy: {point.outcomes['parsing_accuracy']:.2f} [conf:{point.confidence}]
  - Token efficiency: {point.outcomes['token_efficiency']:.2f} tokens/claim
  - Readability: {point.outcomes['human_readability']:.2f} [state:measured]
"""
        print(verix_claim)

    return results
```

### 0.2 VERILINGUA Frame Optimization

**Objectives for GlobalMOO**:
```yaml
project_id: verilingua-self-optimization
objectives:
  - name: frame_activation_success
    description: Does the frame activate intended cognitive pattern?
    direction: maximize
    weight: 0.40

  - name: linguistic_authenticity
    description: Is multi-lingual embedding culturally accurate?
    direction: maximize
    weight: 0.25

  - name: task_alignment
    description: Does frame selection match task requirements?
    direction: maximize
    weight: 0.25

  - name: cognitive_load
    description: Mental effort to use frame correctly
    direction: minimize
    weight: 0.10

parameters:
  - name: frame_selection_method
    type: categorical
    values: [goal_based, keyword_based, domain_based, hybrid]

  - name: activation_phrase_length
    type: ordinal
    values: [short_3lines, medium_5lines, long_10lines]

  - name: multilingual_depth
    type: ordinal
    values: [single_phrase, paragraph, full_section]

  - name: frame_combinations
    type: categorical
    values: [single_only, primary_secondary, multi_frame]
```

**Self-Referential Test**:
```python
# Optimize VERILINGUA by USING VERILINGUA frames to describe optimization
def optimize_verilingua_with_verilingua():
    """
    Meta-optimization: Use cognitive frames to report on frame optimization.

    Example output (using Evidential frame for source verification):

    ## Kanitsal Cerceve Aktivasyonu (Evidential Frame Activation)

    [WITNESSED] I directly tested frame activation patterns across 7 frames
    [INFERRED] Goal-based selection method outperforms keyword-based by 23%
    [REPORTED] GlobalMOO Pareto frontier contains 15 optimal configurations

    Kaynak dogrulama:
    - moo/experiment/frame-selection-v2.0
    - eval/frame-effectiveness/run-2025-12-28
    """

    moo_client = GlobalMOOClient(use_mock=False)

    results = moo_client.optimize(
        project_id="verilingua-self-optimization",
        iterations=100,
        population_size=50
    )

    # Report using VERILINGUA Evidential frame
    print("## Kanitsal Cerceve (Evidential Mode Report)")
    print()
    for point in results.pareto_frontier[:5]:
        print(f"[MEASURED] Frame activation success: {point.outcomes['frame_activation_success']:.2f}")
        print(f"[INFERRED] Best method: {point.config['frame_selection_method']}")
        print(f"[ground:moo/pareto/{point.config_id}]")
        print()

    return results
```

## Phase 0b: Prompt Meta-Optimization

### Using Optimized Languages to Optimize Prompts

**Strategy**: After optimizing VERIX and VERILINGUA, use them to improve prompts:

```python
def meta_optimize_prompts():
    """
    Layer 1: Optimize languages (VERIX, VERILINGUA)
    Layer 2: Use optimized languages in prompts
    Layer 3: Evaluate prompts WITH optimized languages
    Layer 4: Feed back into language optimization
    """

    # Step 1: Load optimized VERIX configuration
    verix_config = load_optimized_verix()  # From Phase 0.1

    # Step 2: Load optimized VERILINGUA frames
    verilingua_config = load_optimized_verilingua()  # From Phase 0.2

    # Step 3: Create prompt using optimized languages
    optimized_prompt = f"""
## {verilingua_config.activation_phrase}

Task: [Your task here]

Requirements:
{verix_config.format_requirements()}

Expected Output Format:
{verix_config.output_template}

Cognitive Frame: {verilingua_config.primary_frame}
"""

    # Step 4: Evaluate prompt effectiveness
    evaluation = eval_prompt_with_cognitive_metrics(
        prompt=optimized_prompt,
        metrics=[
            "epistemic_compliance",  # Uses VERIX
            "frame_alignment",       # Uses VERILINGUA
            "task_accuracy",
            "token_efficiency"
        ]
    )

    # Step 5: Feed results back to MOO for next iteration
    moo_client.record_outcome(
        project_id="prompt-meta-optimization",
        config={"verix": verix_config, "verilingua": verilingua_config},
        outcomes=evaluation
    )

    return optimized_prompt, evaluation
```

## Phase 1: Command Group Optimization

### Group 1a: Core Cognitive Commands

**Commands**: `/mode`, `/frame`, `/verix`

**Why grouped**: These commands directly implement VERIX and VERILINGUA - optimizing them expands the language capabilities.

```yaml
project_id: command-group-1-cognitive
objectives:
  - name: language_expansion
    description: Do optimized commands expand VERIX/VERILINGUA vocabulary?
    direction: maximize
    weight: 0.30

  - name: command_success_rate
    description: % successful command executions
    direction: maximize
    weight: 0.30

  - name: output_epistemic_quality
    description: VERIX compliance of command outputs
    direction: maximize
    weight: 0.25

  - name: frame_effectiveness
    description: VERILINGUA frame activation in outputs
    direction: maximize
    weight: 0.15
```

### Group 1b: Evaluation Commands

**Commands**: `/eval`, `/optimize`, `/pareto`

**Why grouped**: These commands USE the optimized languages to evaluate - creates feedback loop.

```yaml
project_id: command-group-2-evaluation
objectives:
  - name: metric_accuracy
    description: Evaluation metrics correctly measure cognitive architecture
    direction: maximize
    weight: 0.35

  - name: optimization_convergence
    description: MOO optimization reaches stable Pareto frontier
    direction: maximize
    weight: 0.30

  - name: pareto_diversity
    description: Frontier covers diverse trade-offs
    direction: maximize
    weight: 0.20

  - name: actionability
    description: Results lead to concrete improvements
    direction: maximize
    weight: 0.15
```

## Phase 2: Subagent Optimization

### Group 2a: Foundry Agents

**Agents**: prompt-architect, skill-forge, agent-creator

**Integration with Languages**:
- prompt-architect: Uses VERIX to annotate prompt quality claims
- skill-forge: Uses VERILINGUA to select cognitive frames for skills
- agent-creator: Embeds both in generated agent system prompts

```yaml
project_id: agent-group-1-foundry
objectives:
  - name: verix_integration_depth
    description: How deeply does agent use VERIX in outputs?
    direction: maximize
    weight: 0.30

  - name: verilingua_frame_usage
    description: How effectively does agent apply cognitive frames?
    direction: maximize
    weight: 0.30

  - name: agent_task_success
    description: Created prompts/skills/agents meet quality gates
    direction: maximize
    weight: 0.25

  - name: self_improvement_rate
    description: Agent improves through recursive loop
    direction: maximize
    weight: 0.15
```

### Group 2b: Quality Agents

**Agents**: code-analyzer, reviewer, tester, functionality-audit

**Integration with Languages**:
- code-analyzer: Reports violations using VERIX claims with confidence
- reviewer: Uses VERILINGUA frames for different review perspectives
- tester: Expresses test results with epistemic grounding

## Phase 3: Skill SOP Optimization

**Target**: Skills that spawn the optimized agents

**Key Skills**:
- ai-dev-orchestration (spawns foundry agents)
- code-review-assistant (spawns quality agents)
- deep-research-orchestrator (spawns research agents)

```yaml
project_id: skill-optimization
objectives:
  - name: sop_clarity
    description: Skill SOP clearly defines agent coordination
    direction: maximize
    weight: 0.25

  - name: verix_propagation
    description: VERIX notation flows from skill to agents to outputs
    direction: maximize
    weight: 0.25

  - name: frame_consistency
    description: Cognitive frames consistent across skill execution
    direction: maximize
    weight: 0.25

  - name: end_to_end_success
    description: Complete skill execution meets quality gates
    direction: maximize
    weight: 0.25
```

## Phase 4: Playbook Optimization

**Target**: End-to-end workflows using optimized skills

**Key Playbooks**:
- three-loop-development (research -> implementation -> CI/CD)
- deep-research-sop (9-pipeline research lifecycle)
- simple-feature-implementation (feature lifecycle)

```yaml
project_id: playbook-optimization
objectives:
  - name: workflow_completion
    description: Playbook completes without errors
    direction: maximize
    weight: 0.30

  - name: epistemic_traceability
    description: VERIX claims traced through entire playbook
    direction: maximize
    weight: 0.25

  - name: frame_adaptation
    description: VERILINGUA frames adapt to playbook phases
    direction: maximize
    weight: 0.25

  - name: total_quality_improvement
    description: Playbook output quality vs baseline
    direction: maximize
    weight: 0.20
```

## Expansion Pattern

```
Iteration 1: Languages
  VERIX ----optimize----> Better VERIX
  VERILINGUA ---optimize---> Better VERILINGUA

Iteration 2: Prompts (meta-optimization)
  Prompts + Better Languages ----optimize----> Better Prompts

Iteration 3: Commands (grouped)
  Commands + Better Languages + Better Prompts ----optimize----> Better Commands

Iteration 4: Subagents (grouped)
  Subagents + Better Commands ----optimize----> Better Subagents

Iteration 5: Skills
  Skills + Better Subagents ----optimize----> Better Skills

Iteration 6: Playbooks
  Playbooks + Better Skills ----optimize----> Better Playbooks

Loop Back:
  Better Playbooks contain Better Skills
  Better Skills spawn Better Subagents
  Better Subagents use Better Commands
  Better Commands implement Better Languages
  Better Languages enable Better Prompts
  -> CYCLE CONTINUES
```

## Implementation Order

### Week 1: Language Self-Optimization
1. [ ] Connect to real GlobalMOO API (currently mock)
2. [ ] Run VERIX self-optimization (100 iterations)
3. [ ] Run VERILINGUA self-optimization (100 iterations)
4. [ ] Generate optimized language configurations

### Week 2: Prompt Meta-Optimization
1. [ ] Apply optimized VERIX to prompt templates
2. [ ] Apply optimized VERILINGUA frames to prompts
3. [ ] Run prompt effectiveness evaluation
4. [ ] Feed back to language optimization

### Week 3: Command Groups
1. [ ] Optimize Group 1 (cognitive commands)
2. [ ] Optimize Group 2 (evaluation commands)
3. [ ] Validate command outputs use optimized languages

### Week 4: Subagent Groups
1. [ ] Optimize foundry agents with new commands
2. [ ] Optimize quality agents with new commands
3. [ ] Validate agent outputs propagate language improvements

### Week 5: Skills & Playbooks
1. [ ] Optimize skill SOPs with optimized agents
2. [ ] Optimize playbooks with optimized skills
3. [ ] Run full end-to-end validation

## Success Metrics

| Phase | Metric | Baseline | Target |
|-------|--------|----------|--------|
| Language | Epistemic clarity | 0.65 | 0.90 |
| Language | Frame activation | 0.55 | 0.85 |
| Prompts | VERIX compliance | 0% | 90% |
| Prompts | Frame usage | 35% | 80% |
| Commands | Success rate | 85% | 98% |
| Commands | Output quality | 0.70 | 0.90 |
| Agents | Task completion | 75% | 92% |
| Agents | Self-improvement | 0% | 30% |
| Skills | Quality gates | 80% | 95% |
| Skills | End-to-end success | 70% | 90% |
| Playbooks | Completion rate | 70% | 90% |
| Playbooks | Total improvement | baseline | +35% |

## Conclusion

This self-referential optimization strategy:

1. **Starts with languages** - VERIX and VERILINGUA optimize themselves
2. **Meta-optimizes** - Uses optimized languages to improve prompts
3. **Expands gradually** - Commands -> Agents -> Skills -> Playbooks
4. **Loops back** - Improvements flow back to language level
5. **Compounds** - Each level benefits from all previous optimizations

The result is a **self-improving cognitive architecture** where the languages, prompts, commands, agents, skills, and playbooks all enhance each other through GlobalMOO multi-objective optimization.
