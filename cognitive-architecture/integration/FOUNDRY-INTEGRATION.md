# VERILINGUA x VERIX x DSPy x GlobalMOO - Foundry Skills Integration

## Overview

This document defines how the cognitive architecture (Phases 0-3) integrates with the foundry skills:
- **prompt-architect**: Prompt optimization with epistemic notation
- **skill-forge**: Skill creation with cognitive frames
- **agent-creator**: Agent design with multi-objective optimization

## Integration Architecture

```
                    +-------------------+
                    |   GlobalMOO API   |
                    |  (Multi-Objective |
                    |   Optimization)   |
                    +---------+---------+
                              |
              +---------------+---------------+
              |               |               |
    +---------v----+  +-------v------+  +-----v--------+
    | prompt-      |  | skill-       |  | agent-       |
    | architect    |  | forge        |  | creator      |
    | (prompts)    |  | (skills)     |  | (agents)     |
    +---------+----+  +-------+------+  +-----+--------+
              |               |               |
              +-------+-------+-------+-------+
                      |               |
              +-------v-------+ +-----v--------+
              |  VERILINGUA   | |    VERIX     |
              | (7 Cognitive  | | (Epistemic   |
              |    Frames)    | |  Notation)   |
              +-------+-------+ +-----+--------+
                      |               |
                      +-------+-------+
                              |
                      +-------v-------+
                      |     DSPy      |
                      | (Prompt Opt)  |
                      +---------------+
```

## Bottom-Up Optimization Strategy

### Level 0: Core Primitives (Lowest Level)
**Target**: VERIX notation + VERILINGUA frames

**Optimization Goals**:
1. Epistemic clarity (VERIX compliance)
2. Cognitive frame alignment (VERILINGUA accuracy)
3. Token efficiency (compression without loss)
4. Robustness (edge case handling)

**DSPy Integration**:
```python
# DSPy signature for VERIX-enhanced prompts
class VERIXPrompt(dspy.Signature):
    """Generate epistemic-aware prompt with VERIX notation."""

    task = dspy.InputField(desc="Task description")
    context = dspy.InputField(desc="Domain context")

    illocution = dspy.OutputField(desc="[assert|query|propose|commit]")
    affect = dspy.OutputField(desc="[neutral|emphatic|mitigated|dubitative]")
    content = dspy.OutputField(desc="The actual statement")
    ground = dspy.OutputField(desc="Evidence source")
    confidence = dspy.OutputField(desc="0.0-1.0 confidence score")
    state = dspy.OutputField(desc="[hypothetical|actual|counterfactual]")
```

### Level 1: Commands (Build on Level 0)
**Target**: /mode, /eval, /optimize, /pareto, /frame, /verix

**Optimization Goals**:
1. Command success rate (>95%)
2. User satisfaction (NPS-based)
3. Token efficiency (<500 per call)
4. Consistency (low variance)

**GlobalMOO Configuration**:
```yaml
project_id: cognitive-arch-commands
objectives:
  - name: success_rate
    direction: maximize
    weight: 0.3
  - name: user_satisfaction
    direction: maximize
    weight: 0.3
  - name: token_efficiency
    direction: maximize
    weight: 0.2
  - name: consistency
    direction: maximize
    weight: 0.2

parameters:
  - name: verix_strictness
    type: ordinal
    values: [relaxed, moderate, strict]
  - name: frame_selection
    type: categorical
    values: [auto, evidential, aspectual, morphological, compositional, honorific, classifier, spatial]
  - name: output_verbosity
    type: ordinal
    values: [minimal, balanced, detailed]
```

### Level 2: Agents (Build on Level 1)
**Target**: Agents that use cognitive architecture commands

**Optimization Goals**:
1. Task completion accuracy
2. VERIX compliance in outputs
3. Frame utilization effectiveness
4. Inter-agent coordination

**Agent Enhancement Template**:
```markdown
## Cognitive Architecture Integration

### VERIX Output Protocol
All outputs MUST include epistemic markers:
- [ground:{source}] for claims
- [conf:{0.0-1.0}] for confidence
- Use [assert|query|propose] illocutions

### VERILINGUA Frame Activation
Based on task type, activate appropriate frame:
- **Research tasks**: Evidential frame (Turkish mode)
- **Build tasks**: Aspectual frame (Russian mode)
- **Analysis tasks**: Morphological frame (Arabic mode)
- **Coordination tasks**: Honorific frame (Japanese mode)

### DSPy Optimization Hooks
This agent uses DSPy-optimized prompts:
- Prompt version: {dspy_optimized_version}
- Last optimization: {optimization_date}
- Performance delta: {improvement_percentage}
```

### Level 3: Skills (Build on Level 2)
**Target**: Skill SOPs that spawn agents

**Optimization Goals**:
1. End-to-end success rate
2. Time to completion
3. Quality gate pass rate
4. Cognitive load reduction

**Skill Enhancement Pattern**:
```yaml
# Cognitive Architecture Metadata (add to skill frontmatter)
cognitive_architecture:
  version: "1.0.0"
  verilingua:
    primary_frame: evidential
    secondary_frames: [aspectual, morphological]
    activation_triggers:
      - task_type: research
        frame: evidential
      - task_type: build
        frame: aspectual
  verix:
    strictness: moderate
    required_markers:
      - ground
      - confidence
    optional_markers:
      - state
  dspy:
    optimization_level: 2  # Per-cluster caching
    cached_prompts:
      - intro_prompt
      - validation_prompt
  globalmoo:
    project_id: skill-{skill-name}
    objectives: [accuracy, efficiency, robustness]
```

### Level 4: Playbooks (Build on Level 3)
**Target**: End-to-end workflow orchestration

**Optimization Goals**:
1. Workflow completion rate
2. Total time reduction
3. Error recovery success
4. User override frequency (minimize)

## Meta-Loop Integration

### Foundry Triangle Enhancement

```
                    PROMPT-ARCHITECT
                    (VERIX-enhanced)
                         /\
                        /  \
                       /    \
                      /      \
    GlobalMOO <------/        \------> GlobalMOO
    Optimize        /          \       Optimize
                   /            \
                  /              \
          SKILL-FORGE -------- AGENT-CREATOR
          (Frame-aware)        (DSPy-optimized)
```

### Enhancement Protocol

1. **prompt-architect Enhancement**:
   - Add VERIX notation to all generated prompts
   - Include [ground:technique] for evidence-based techniques
   - Add [conf:0.XX] for effectiveness claims
   - Optimize with DSPy for clarity/completeness/precision

2. **skill-forge Enhancement**:
   - Embed cognitive frame selection in Phase 0.5
   - Add VERILINGUA markers to skill instructions
   - Include GlobalMOO configuration in skill schema
   - Track skill effectiveness via multi-objective metrics

3. **agent-creator Enhancement**:
   - Generate VERIX-compliant system prompts
   - Embed frame activation based on agent domain
   - Optimize agent prompts via DSPy Level 2 caching
   - Track agent performance via GlobalMOO Pareto frontier

## Implementation Checklist

### Phase A: Foundation Enhancement (Current)
- [x] Core VERILINGUA module (7 frames)
- [x] Core VERIX module (epistemic notation)
- [x] DSPy integration (prompt optimization)
- [x] GlobalMOO client (multi-objective)
- [x] Three-MOO Cascade
- [x] Mode distillation
- [ ] Foundry skill integration hooks

### Phase B: Foundry Skill Updates
- [ ] prompt-architect v2.3.0 (VERIX integration)
- [ ] skill-forge v3.1.0 (GlobalMOO integration)
- [ ] agent-creator v3.1.0 (DSPy integration)
- [ ] Auditor skills (prompt, skill, expertise, output)

### Phase C: Command Optimization
- [ ] /mode with DSPy-optimized selection
- [ ] /eval with VERIX compliance scoring
- [ ] /optimize with real GlobalMOO API
- [ ] /pareto with interactive visualization
- [ ] /frame with frame effectiveness metrics
- [ ] /verix with auto-annotation

### Phase D: Meta-Loop Activation
- [ ] Ralph Wiggum + foundry integration
- [ ] Continuous optimization pipeline
- [ ] Eval harness with cognitive metrics
- [ ] Expertise system with frame learnings

## Metrics Dashboard

### Key Performance Indicators

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| VERIX compliance | 0% | 90% | Claims with ground+conf markers |
| Frame utilization | 35% | 80% | Tasks with frame activation |
| DSPy improvement | - | +25% | Pre/post optimization delta |
| Pareto optimality | 0 | 50+ | Points on frontier |
| Command success | 85% | 98% | Successful command executions |
| Agent accuracy | 75% | 92% | Task completion rate |
| Skill pass rate | 80% | 95% | Quality gate passage |
| Playbook completion | 70% | 90% | End-to-end success |

## Usage Examples

### Example 1: Enhanced Prompt Creation

```python
# Before (baseline)
prompt = "Create a REST API endpoint for user authentication"

# After (VERIX + VERILINGUA + DSPy enhanced)
prompt = """
## Evidential Frame Activation
Kaynak dogrulama modu etkin. Her karar icin referans gerekli.

## Task
[assert|emphatic] Create a REST API endpoint for user authentication [ground:requirements.md] [conf:0.95]

## Requirements
- [assert|neutral] Use JWT tokens for session management [ground:security-policy.md] [conf:0.90]
- [propose|neutral] Consider refresh token rotation for enhanced security [ground:OWASP] [conf:0.85]

## Expected Output
- Express.js route handler
- JWT token generation/validation
- Error handling with [epistemic markers]
"""
```

### Example 2: Enhanced Skill Output

```yaml
# skill-forge output with cognitive architecture
---
name: api-development
version: 1.0.0
cognitive_architecture:
  verilingua:
    primary_frame: aspectual  # Build task
    activation: "Sostoyanie Gotovnosti - Track completion state"
  verix:
    strictness: moderate
    required: [ground, confidence]
  dspy:
    optimization_level: 2
    prompts_optimized: 3
  globalmoo:
    project_id: skill-api-development
    pareto_points: 12
---
```

### Example 3: Enhanced Agent System Prompt

```markdown
# API Developer Agent - v1.0.0

## Cognitive Architecture Integration

### Aspectual Frame (Build Mode)
Etot agent otslezhivaet zavershenie:
- [SV] Zaversheno - Endpoint complete and tested
- [NSV] V protsesse - Currently implementing
- [BLOCKED] Ozhidaet - Waiting for dependencies

### VERIX Output Protocol
All code comments include:
- [ground:spec] for requirement traceability
- [conf:0.XX] for implementation confidence
- [assert|query|propose] for decision type

### DSPy Optimization
System prompt optimized via DSPy Level 2:
- Clarity: 0.92 (baseline 0.75)
- Completeness: 0.88 (baseline 0.70)
- Token efficiency: 0.85 (baseline 0.60)
```

## Conclusion

This integration module provides the blueprint for enhancing all foundry skills with:

1. **VERIX**: Epistemic transparency in all outputs
2. **VERILINGUA**: Cognitive frame precision for task alignment
3. **DSPy**: Evidence-based prompt optimization
4. **GlobalMOO**: Multi-objective performance optimization

The bottom-up strategy ensures each level builds on optimized primitives, creating compounding improvements throughout the system.

Next Steps:
1. Run connascence analysis on existing implementations
2. Apply Ralph Wiggum meta-loop to each foundry skill
3. Validate improvements against eval harness
4. Deploy to Context Cascade plugin system
