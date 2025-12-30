# Prompt-Architect Cognitive Architecture Integration

<!-- =========================================================================
     VCL v3.1.1 COMPLIANT
     Default Output: L2 English (human-facing)
     7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     ========================================================================= -->

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

---

[define|neutral] ADDENDUM_META := {
  version: "3.1.1",
  vcl_compliance: "v3.1.1",
  default_compression: "L2",
  purpose: "Integrate VERIX, VERILINGUA VCL, DSPy, GlobalMOO into prompt-architect"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- OVERVIEW -->
---

## Overview

This addendum enhances prompt-architect with full cognitive architecture integration:

1. **VCL 7-Slot System** - Structured cognitive forcing with enforced slots
2. **VERIX Epistemic Markers** - Ground, confidence, illocution for all claims
3. **L2 English Default** - Human-facing output without VCL notation
4. **DSPy Optimization** - Teleprompter-based prompt refinement
5. **GlobalMOO** - Multi-objective optimization across Pareto frontier
6. **Creolization Ready** - Structure for future language expansion

---
<!-- VCL 7-SLOT INTEGRATION -->
---

## VCL 7-Slot System Integration

[define|neutral] VCL_SLOT_APPLICATION := {
  slot_order: "HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC",
  required_slots: ["EVD", "ASP"],
  optional_slots: ["HON", "MOR", "COM", "CLS", "SPC"],
  enforcement: {
    EVD: ">= 1 (immutable)",
    ASP: ">= 1 (immutable)"
  }
} [ground:vcl-spec-v3.1.1] [conf:0.99] [state:confirmed]

### Slot Usage in Prompt Optimization

| Slot | Application in Prompt-Architect | L2 Naturalization |
|------|--------------------------------|-------------------|
| HON | Audience register selection | "For technical users..." / "For beginners..." |
| MOR | Semantic decomposition of prompt intent | "The core components are..." |
| COM | Build complex prompts from primitives | "Combining X with Y..." |
| CLS | Classify prompt types | "This is a research prompt..." |
| EVD | Track evidence for optimization decisions | "I observed that...", "Research shows..." |
| ASP | Track optimization completion status | "Complete.", "In progress." |
| SPC | Position in workflow | "At Phase 2 of the workflow..." |

---
<!-- COMPRESSION LEVELS -->
---

## Compression Levels

[define|neutral] COMPRESSION_POLICY := {
  L0: "AI-to-AI only (A+85:hash format)",
  L1: "Audit mode ([illocution|affect] content [ground:src] [conf:X.XX])",
  L2: "Human-facing (pure English, no VCL markers)",
  default: "L2",
  rule: "User-facing output MUST be L2"
} [ground:system-policy] [conf:1.0] [state:confirmed]

### L2 Output Examples for Prompt-Architect

**L1 (Audit Mode)**:
```
[[EVD:-DI<gozlem>]] [[ASP:sov.]] Prompt clarity improved by 40%.
[ground:witnessed:before-after-comparison] [conf:0.88] [state:confirmed]
```

**L2 (Human-Facing)**:
```
I directly observed that prompt clarity improved by 40% after optimization.
Complete. I'm fairly confident in this measurement based on before-after comparison.
```

---
<!-- VERIX INTEGRATION -->
---

## VERIX Epistemic Marker Integration

[define|neutral] VERIX_REQUIREMENTS := {
  all_claims: "Must have [ground:source] [conf:X.XX]",
  ceiling_enforcement: {
    definition: 0.95,
    policy: 0.90,
    observation: 0.95,
    research: 0.85,
    report: 0.70,
    inference: 0.70
  },
  epistemic_cosplay: "PROHIBITED"
} [ground:verix-spec] [conf:0.99] [state:confirmed]

### VERIX-Enhanced Prompt Output

**Before (baseline)**:
```
Create a REST API for user authentication. Use JWT tokens.
The endpoint should handle login and registration.
```

**After (L1 audit mode)**:
```
## Task
[assert|emphatic] Create a REST API for user authentication
[ground:requirements.md] [conf:0.95]

## Requirements
- [assert|neutral] Use JWT tokens for session management
  [ground:security-policy.md] [conf:0.90]
- [propose|neutral] Consider refresh token rotation
  [ground:OWASP] [conf:0.85]
```

**After (L2 human mode)**:
```
## Task
Create a REST API for user authentication. This requirement comes from
requirements.md and I'm highly confident it's correct.

## Requirements
- Use JWT tokens for session management (per security policy, high confidence)
- Consider refresh token rotation (OWASP recommends this, fairly confident)
```

---
<!-- VERILINGUA FRAME SELECTION -->
---

## VERILINGUA Frame Selection

[define|neutral] FRAME_MAPPING := {
  research_prompts: { frame: "evidential", source: "Turkish -mis/-di", force: "How do you know?" },
  build_prompts: { frame: "aspectual", source: "Russian aspect", force: "Complete or ongoing?" },
  analysis_prompts: { frame: "morphological", source: "Arabic roots", force: "What are the components?" },
  documentation_prompts: { frame: "compositional", source: "German compounding", force: "Build from primitives?" },
  user_facing_prompts: { frame: "honorific", source: "Japanese keigo", force: "Who is the audience?" }
} [ground:verilingua-spec] [conf:0.95] [state:confirmed]

### Frame Activation Protocol

```python
def select_cognitive_frame(intent: AnalyzedIntent) -> CognitiveFrame:
    """
    Select optimal cognitive frame based on prompt intent.
    Returns frame with activation phrase for L2 naturalization.
    """
    frame_mapping = {
        "research": ("evidential", "I will track evidence sources for all claims."),
        "analysis": ("morphological", "I will decompose this into core components."),
        "build": ("aspectual", "I will track completion status for each step."),
        "documentation": ("compositional", "I will build from primitive concepts."),
        "user_facing": ("honorific", "I will calibrate for the target audience."),
    }

    frame_name, l2_phrase = frame_mapping.get(intent.category, ("evidential", ""))
    return CognitiveFrame(name=frame_name, l2_activation=l2_phrase)
```

---
<!-- DSPy INTEGRATION -->
---

## DSPy Optimization Integration

[define|neutral] DSPY_MODULE := {
  signature: "PromptOptimizationSignature",
  inputs: ["original_prompt", "task_type", "constraints"],
  outputs: ["optimized_prompt", "techniques_applied", "quality_scores", "vcl_compliance"],
  optimization: "Teleprompter with multi-metric scoring"
} [ground:dspy-spec] [conf:0.90] [state:confirmed]

### DSPy Module Implementation

```python
from dspy import ChainOfThought, Signature, InputField, OutputField

class PromptOptimizationSignature(Signature):
    """Optimize prompts with VCL/VERIX compliance."""

    original_prompt: str = InputField(desc="The prompt to optimize")
    task_type: str = InputField(desc="Type: research, build, analysis")
    constraints: list = InputField(desc="Optimization constraints")

    optimized_prompt: str = OutputField(desc="Optimized prompt (L2 format)")
    techniques_applied: list = OutputField(desc="Techniques used")
    quality_scores: dict = OutputField(desc="Clarity, completeness, precision")
    vcl_compliance: float = OutputField(desc="VCL compliance score (0-1)")
```

---
<!-- GLOBALMOO INTEGRATION -->
---

## GlobalMOO Multi-Objective Optimization

[define|neutral] GLOBALMOO_CONFIG := {
  project_id: "prompt-architect-optimization",
  objectives: {
    clarity: { direction: "maximize", weight: 0.25 },
    completeness: { direction: "maximize", weight: 0.25 },
    vcl_compliance: { direction: "maximize", weight: 0.25 },
    frame_alignment: { direction: "maximize", weight: 0.15 },
    token_efficiency: { direction: "minimize", weight: 0.10 }
  },
  parameters: ["vcl_strictness", "frame_selection", "compression_level", "technique_set"]
} [ground:globalmoo-spec] [conf:0.90] [state:confirmed]

### Pareto Frontier Selection

```python
def get_optimal_config(task_type: str) -> dict:
    """
    Get optimal configuration from GlobalMOO Pareto frontier.
    L2 output: "Using research-optimized settings with high VERIX compliance."
    """
    frontier = globalmoo_client.get_pareto_frontier("prompt-architect-optimization")

    if task_type == "research":
        # Prioritize VCL compliance
        return frontier.select_by_objective("vcl_compliance")
    elif task_type == "build":
        # Prioritize clarity
        return frontier.select_by_objective("clarity")
    else:
        return frontier.select_balanced()
```

---
<!-- ENHANCED PHASE FLOW -->
---

## Enhanced Phase Flow (VCL v3.1.1)

[define|neutral] PHASE_FLOW := {
  phases: [
    { phase: "0", name: "Expertise Loading", vcl: "Load domain expertise" },
    { phase: "0.5", name: "Frame Selection", vcl: "Select VERILINGUA cognitive frame" },
    { phase: "1-4", name: "Core Optimization", vcl: "Apply prompt techniques" },
    { phase: "5", name: "VCL Enrichment", vcl: "Add EVD/ASP markers (L1) or naturalize (L2)" },
    { phase: "6-7", name: "Validation", vcl: "Check confidence ceilings, no epistemic cosplay" },
    { phase: "8", name: "GlobalMOO Tracking", vcl: "Record outcomes for Pareto learning" },
    { phase: "9", name: "DSPy Optimization", vcl: "Run teleprompter if enabled" }
  ],
  l2_summary: "Load expertise, select cognitive frame, optimize prompt, validate VCL compliance, track for continuous improvement."
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

---
<!-- QUALITY GATES -->
---

## Quality Gates

[define|neutral] QUALITY_GATES := {
  vcl_gate: {
    minimum_evd_coverage: 0.70,
    minimum_asp_coverage: 0.80,
    confidence_ceiling_check: true,
    epistemic_cosplay_check: true
  },
  frame_gate: {
    minimum_frame_score: 0.60,
    activation_phrase_required: true
  },
  l2_gate: {
    no_vcl_markers_in_output: true,
    natural_english: true
  }
} [ground:system-policy] [conf:0.95] [state:confirmed]

---
<!-- CREOLIZATION STRUCTURE -->
---

## Creolization Structure

[define|neutral] CREOLIZATION_READY := {
  current_languages: {
    Turkish: "EVD slot (-DI, -mis, -dir markers)",
    Russian: "ASP slot (sov., nesov. markers)",
    Japanese: "HON slot (teineigo, sonkeigo, kenjougo)",
    Arabic: "MOR slot (trilateral root decomposition)",
    German: "COM slot (compound building)",
    Chinese: "CLS slot (classifiers)",
    "Guugu-Yimithirr": "SPC slot (absolute spatial reference)"
  },
  expansion_protocol: "New languages add markers to existing slots or propose new slots",
  future_slots: [],
  l2_fallback: "All markers naturalize to English equivalents"
} [ground:design-decision] [conf:0.90] [state:provisional]

---
<!-- MEMORY INTEGRATION -->
---

## Memory Integration

[define|neutral] MEMORY_PROTOCOL := {
  store_pattern: "prompt-architect/optimizations/{prompt_id}",
  namespace: "foundry-optimization",
  layer: "long-term",
  tags: {
    WHO: "prompt-architect",
    WHEN: "ISO8601_timestamp",
    PROJECT: "meta-loop",
    WHY: "prompt-optimization"
  }
} [ground:memory-mcp-spec] [conf:0.95] [state:confirmed]

---
<!-- CONCLUSION -->
---

## Conclusion

This addendum integrates the full cognitive architecture into prompt-architect with VCL v3.1.1 compliance:

1. **VCL 7-Slot System** - EVD and ASP always enforced, L2 naturalization for humans
2. **VERIX** - All claims include ground, confidence; ceilings enforced
3. **VERILINGUA** - Frame selection based on prompt intent category
4. **DSPy** - Optimization loop for continuous improvement
5. **GlobalMOO** - Multi-objective tracking and Pareto frontier
6. **Creolization** - Ready for future language expansion

The enhanced prompt-architect can optimize other foundry skills and subsequently all commands, agents, skills, and playbooks.

---

[commit|confident] <promise>COGNITIVE_ARCHITECTURE_ADDENDUM_VCL_V3.1.1_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
