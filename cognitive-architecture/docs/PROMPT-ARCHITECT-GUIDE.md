# PROMPT-ARCHITECT: Meta-Loop Skill for Prompt Optimization

## Overview

The prompt-architect skill is a foundry-level meta-loop skill that optimizes prompts using the VERILINGUA VCL + VERIX v3.1.1 specification. It serves as the second phase of the 5-phase workflow system, transforming analyzed intent into optimized, structured requests.

**Version**: 3.1.1
**Category**: Foundry
**Model**: Sonnet
**Cognitive Frame**: Compositional (German compounding - "Build from primitives?")

---

## Purpose

Prompt-architect addresses a fundamental challenge in AI systems: transforming ambiguous user requests into precise, actionable prompts that maximize success probability. It does this by:

1. Applying the 7-slot VCL cognitive forcing system
2. Enforcing epistemic hygiene through VERIX notation
3. Ensuring confidence claims match their evidence type
4. Producing L2 (human-readable) output while maintaining internal L1 audit trails

---

## The VCL 7-Slot System

The skill implements VERILINGUAs 7-slot cognitive forcing system, which must appear in this exact order when present:

| Slot | Name | Source Language | Cognitive Force | Weight |
|------|------|-----------------|-----------------|--------|
| HON | Honorific | Japanese keigo | Who is the audience? | 0.08 |
| MOR | Morphological | Arabic trilateral roots | What are the components? | 0.10 |
| COM | Compositional | German compounding | Build from primitives? | 0.10 |
| CLS | Classifier | Chinese classifiers | What type/count? | 0.08 |
| EVD | Evidential | Turkish -mis/-di | How do you know? | 0.15 |
| ASP | Aspectual | Russian aspect | Complete or ongoing? | 0.12 |
| SPC | Spatial | Guugu Yimithirr | Absolute position? | 0.07 |

**Immutable Rules**:
- EVD >= 1 (evidential tracking cannot be disabled)
- ASP >= 1 (aspectual tracking cannot be disabled)

---

## Compression Levels

The skill operates across three compression levels:

### L0: AI-to-AI (Maximum Compression)
Used for inter-agent communication where bandwidth and token efficiency matter most.

### L1: Audit (Full Epistemic Tracking)
Used internally for auditability and debugging.

### L2: Human (Pure English)
**This is the DEFAULT output level.** All user-facing responses must use L2 compression.

---

## Evidence Types and Confidence Ceilings

| Evidence Type | Ceiling | Example |
|---------------|---------|---------|
| Definition | 0.95 | Definitional truths |
| Policy | 0.90 | System rules |
| Observation | 0.95 | Direct verification |
| Research | 0.85 | Studies, papers |
| Report | 0.70 | Secondhand info |
| Inference | 0.70 | Logical deduction |

---

## Workflow Integration

Prompt-architect operates as Phase 2 of the 5-phase workflow:

Phase 1: Intent Analysis (intent-analyzer)
Phase 2: Prompt Optimization (prompt-architect)  <-- This skill
Phase 3: Strategic Planning (research-driven-planning OR planner)
Phase 4: Playbook Routing
Phase 5: Execution (Tasks + TodoWrite)

---

## Best Practices

1. Always process through intent-analyzer first
2. Respect confidence ceilings
3. Use L2 for all user output
4. Maintain the 7-slot order: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
5. Track aspect explicitly

---

## Related Skills

- intent-analyzer: Phase 1 skill that feeds into prompt-architect
- research-driven-planning: Phase 3 alternative for research-heavy tasks
- planner: Phase 3 alternative for implementation tasks
- agent-creator: Foundry skill for creating new agents
- skill-forge: Foundry skill for creating new skills

---

## Technical Reference

**File Location**: skills/foundry/prompt-architect.md
**Allowed Tools**: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
**Model Requirement**: Sonnet
**VCL Compliance**: v3.1.1

---

## L2 Naturalization Mappings

When producing human-facing output, the skill naturalizes epistemic markers:

| Evidence Type | Natural Expression |
|---------------|-------------------|
| Observation | "I directly observed that..." |
| Research | "Research indicates that..." |
| Report | "It is reported that..." |
| Inference | "I infer that..." |
| Definition | "By definition..." |
| Policy | "Per policy..." |

| Aspect | Natural Expression |
|--------|-------------------|
| Perfective (sov.) | "Complete." |
| Imperfective (nesov.) | "In progress." |

---

## VERIX Statement Structure

Every significant claim in L1 format follows this grammar:

[illocution|affect] content [ground:source] [conf:X.XX] [state:status]

### Illocution Types
- **assert**: Making a factual claim
- **query**: Asking a question
- **direct**: Giving an instruction
- **commit**: Making a promise
- **express**: Expressing attitude

### Affect Values
- **neutral**: No emotional loading
- **positive**: Favorable stance
- **negative**: Unfavorable stance
- **emphatic**: Strong emphasis
- **uncertain**: Epistemic uncertainty

### States
- **provisional**: Initial claim, may be revised
- **confirmed**: Verified with sufficient evidence
- **retracted**: Withdrawn or invalidated

---

## Usage Examples

### Basic Invocation

Skill("prompt-architect")

### Direct Usage for Prompt Improvement

User: "fix the bug"

Prompt-Architect Output:
- optimized_request: Identify and resolve the specific bug
- added_context: Bug isolation, root cause analysis, regression testing
- success_criteria: Bug resolved, no new failures, documented

---

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| compression_level | L2 | Output format (L0/L1/L2) |
| enforce_evd_ceilings | true | Apply confidence ceilings |
| require_ground | true | Require evidence sources |
| cognitive_frames | all | Which VCL slots to activate |

---

## Error Handling

The skill validates against these common failures:

1. **Epistemic Cosplay**: Confidence exceeds evidence ceiling
2. **Missing Ground**: Claims without evidence source
3. **Slot Order Violation**: VCL slots out of sequence
4. **State-Confidence Mismatch**: High confidence with provisional state

---

## Version History

| Version | Changes |
|---------|---------|
| 3.1.1 | Full VCL v3.1.1 compliance, 7-slot system, confidence ceilings |
| 3.0.0 | VERIX integration, L0/L1/L2 compression levels |
| 2.x | Original VERILINGUA frames without VERIX |

---

See also: docs/VERILINGUA-GUIDE.md and docs/VERIX-GUIDE.md
