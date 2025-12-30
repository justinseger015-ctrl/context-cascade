# Prompt Architect - Recursive Improvement Addendum

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
  purpose: "Connect prompt-architect to Recursive Self-Improvement System"
} [ground:manifest] [conf:1.0] [state:confirmed]

---
<!-- PURPOSE -->
---

## Purpose

This addendum connects **prompt-architect** (Phase 2 in 5-phase workflow) with the **Recursive Self-Improvement System**.

---
<!-- DISTINCTION -->
---

## Distinction: prompt-architect vs prompt-forge

[define|neutral] SKILL_DISTINCTION := {
  prompt_architect: {
    purpose: "Optimize USER prompts for better AI responses",
    target: "User-provided prompts",
    scope: "Single-use optimization",
    output: "Improved user prompt (L2 English)",
    gate: "None (direct use)"
  },
  prompt_forge: {
    purpose: "Self-improve SYSTEM prompts and skills",
    target: "Internal skills, agents, expertise",
    scope: "Recursive improvement loop",
    output: "Proposals + diffs + eval results",
    gate: "Frozen eval harness"
  }
} [ground:architecture-design] [conf:0.95] [state:confirmed]

| Aspect | prompt-architect | prompt-forge |
|--------|------------------|--------------|
| **Purpose** | Optimize USER prompts | Self-improve SYSTEM prompts |
| **Target** | User-provided prompts | Internal skills, agents |
| **Scope** | Single-use optimization | Recursive improvement loop |
| **Output** | Improved prompt (L2) | Proposals + diffs + eval |
| **Gate** | None (direct use) | Frozen eval harness |

---
<!-- ROUTING LOGIC -->
---

## When to Use Which

[define|neutral] ROUTING_DECISION := {
  user_prompt_optimization: "route(prompt-architect)",
  system_self_improvement: "route(prompt-forge)",
  l2_explanation: "If user wants better prompt output, use prompt-architect. If system wants to improve itself, use prompt-forge."
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

```
USER wants better prompt output
  -> Use prompt-architect (Phase 2)
  -> Optimizes their prompt
  -> Returns improved prompt (L2 English)

SYSTEM wants to improve itself
  -> Use prompt-forge (recursive improvement)
  -> Analyzes internal skills/prompts
  -> Generates proposals with VCL markers (L1)
  -> Tests against eval harness
  -> Commits if improved
```

---
<!-- INTEGRATION POINTS -->
---

## Integration Points

### prompt-architect as Improvement Target

[define|neutral] IMPROVEMENT_CYCLE := {
  target: "prompt-architect/SKILL.md",
  process: [
    { step: "prompt-auditor analyzes", checks: ["vcl_compliance", "technique_coverage", "l2_enforcement"] },
    { step: "prompt-forge generates proposals", areas: ["VCL slot coverage", "L2 naturalization"] },
    { step: "skill-forge applies proposals", output: "prompt-architect-v{N+1}" },
    { step: "eval-harness tests", benchmark: "prompt-generation-benchmark-v1" },
    { step: "If improved: commit" }
  ]
} [ground:recursive-improvement-spec] [conf:0.90] [state:confirmed]

### prompt-architect Informing prompt-forge

[define|neutral] TECHNIQUE_USAGE := {
  self_consistency: {
    in_prompt_architect: "Teaching users to apply",
    in_prompt_forge: "Applied when generating proposals"
  },
  program_of_thought: {
    in_prompt_architect: "Teaching users to structure",
    in_prompt_forge: "Used in improvement analysis"
  },
  plan_and_solve: {
    in_prompt_architect: "Teaching users to separate phases",
    in_prompt_forge: "Core of improvement cycle"
  }
} [ground:technique-mapping] [conf:0.90] [state:confirmed]

---
<!-- DUAL ROLE ARCHITECTURE -->
---

## Dual Role Architecture

[define|neutral] ARCHITECTURE_DIAGRAM := {
  user_flow: "User Request -> prompt-architect -> Optimized Prompt (L2)",
  system_flow: "Self-Improvement Request -> prompt-forge -> eval-harness -> Improved System",
  l2_summary: "Users get L2 English output; system improvement uses L1 for auditability."
} [ground:architecture-design] [conf:0.95] [state:confirmed]

```
                    +-------------------+
                    |   User Request    |
                    +-------------------+
                            |
                            v
                    +-------------------+
                    | Phase 2: prompt-  |
                    |     architect     |  <-- For USER prompts (L2 output)
                    +-------------------+
                            |
                            v
                    +-------------------+
                    | Optimized Prompt  |
                    |   (L2 English)    |
                    +-------------------+

                           ---

                    +-------------------+
                    | Self-Improvement  |
                    |     Request       |
                    +-------------------+
                            |
                            v
                    +-------------------+
                    |   prompt-forge    |  <-- For SYSTEM (L1 audit)
                    +-------------------+
                            |
                            v
                    +-------------------+
                    |   eval-harness    |
                    +-------------------+
                            |
                            v
                    +-------------------+
                    |  Improved System  |
                    +-------------------+
```

---
<!-- CROSS-POLLINATION -->
---

## Cross-Pollination

[define|neutral] CROSS_POLLINATION := {
  direction: "prompt-forge -> prompt-architect",
  mechanism: [
    "prompt-forge discovers effective technique",
    "Document in prompt-forge learnings (L1)",
    "prompt-auditor flags for prompt-architect update",
    "Run improvement cycle on prompt-architect",
    "Add technique to user-facing skill (L2 documentation)"
  ],
  example: {
    discovery: "Self-consistency with 3 perspectives optimal",
    current: "Consider multiple perspectives",
    proposed: "Consider exactly 3 perspectives: analytical, practical, contrarian",
    gate: "Must pass prompt-generation-benchmark-v1"
  }
} [ground:improvement-protocol] [conf:0.85] [state:confirmed]

---
<!-- SHARED TECHNIQUES -->
---

## Shared Techniques Reference

[define|neutral] TECHNIQUE_MATRIX := {
  techniques: ["self_consistency", "program_of_thought", "plan_and_solve", "few_shot", "chain_of_thought", "uncertainty_handling"],
  prompt_architect_role: "Teaching to users (L2 output)",
  prompt_forge_role: "Applied in proposal generation (L1 audit)"
} [ground:technique-mapping] [conf:0.90] [state:confirmed]

| Technique | In prompt-architect | In prompt-forge |
|-----------|---------------------|-----------------|
| Self-Consistency | Teaching to users (L2) | Applied in proposal generation (L1) |
| Program-of-Thought | Teaching to users (L2) | Applied in analysis (L1) |
| Plan-and-Solve | Teaching to users (L2) | Core cycle structure (L1) |
| Few-Shot | Teaching to users (L2) | Used in examples (L1) |
| Chain-of-Thought | Teaching to users (L2) | Applied in rationale (L1) |
| Uncertainty Handling | Should teach (L2) | CRITICAL for proposals (L1) |

---
<!-- VCL COMPLIANCE IN FEEDBACK LOOP -->
---

## VCL Compliance in Feedback Loop

[define|neutral] VCL_FEEDBACK := {
  prompt_architect_output: "L2 (pure English for users)",
  prompt_forge_output: "L1 (VCL markers for audit)",
  cross_pollination: "L1 discoveries naturalized to L2 for user docs",
  confidence_ceilings: "Enforced in both skills per EVD type"
} [ground:vcl-spec-v3.1.1] [conf:0.95] [state:confirmed]

```
prompt-architect (teaches techniques, L2 output)
       |
       v
Users apply techniques
       |
       v
prompt-forge improves prompt-architect (L1 audit)
       |
       v
Better technique teaching (L2)
       |
       v
Better user outcomes
       |
       v
(cycle continues)
```

---
<!-- MEMORY NAMESPACES -->
---

## Memory Namespaces

[define|neutral] MEMORY_NAMESPACES := {
  user_sessions: "prompt-architect/sessions/{id}",
  self_improvement: "prompt-forge/proposals/{id}",
  audits: "improvement/audits/prompt-architect",
  cycles: "improvement/cycles/prompt-architect",
  tagging: {
    WHO: "prompt-architect or prompt-forge",
    WHEN: "ISO8601_timestamp",
    PROJECT: "meta-loop",
    WHY: "optimization or improvement"
  }
} [ground:memory-mcp-spec] [conf:0.95] [state:confirmed]

---
<!-- USAGE IN 5-PHASE WORKFLOW -->
---

## Usage in 5-Phase Workflow

[define|neutral] WORKFLOW_INTEGRATION := {
  phase_1: "intent-analyzer detects: 'optimize my prompt' vs 'improve system'",
  phase_2_user: "prompt-architect for USER prompts (L2 output)",
  phase_2_system: "prompt-forge for SYSTEM prompts (L1 audit)",
  routing_key: "Intent determines which skill is invoked"
} [ground:workflow-spec] [conf:0.95] [state:confirmed]

```
Phase 1: intent-analyzer
  -> Detects: "optimize my prompt" vs "improve system"

Phase 2: prompt-architect (USER prompts)
  -> IF intent = "optimize my prompt"
  -> Apply evidence-based techniques
  -> Return improved prompt (L2 English)

Phase 2-ALT: prompt-forge (SYSTEM prompts)
  -> IF intent = "improve system"
  -> Analyze target skill/prompt
  -> Generate proposals (L1 audit)
  -> Gate through eval-harness
```

---
<!-- CREOLIZATION NOTE -->
---

## Creolization Note

[define|neutral] CREOLIZATION_APPLICATION := {
  current_state: "Turkish EVD markers in L1, Russian ASP markers in L1",
  l2_conversion: "All markers naturalized to English for user output",
  future_expansion: "New language markers can be added without breaking L2 output"
} [ground:design-decision] [conf:0.90] [state:provisional]

---

[define|neutral] VERSION := {
  version: "3.1.1",
  last_updated: "2025-12-30",
  vcl_compliance: "v3.1.1",
  key_insight: "prompt-architect teaches (L2), prompt-forge applies and improves the teacher (L1)"
} [ground:manifest] [conf:1.0] [state:confirmed]

---

[commit|confident] <promise>RECURSIVE_IMPROVEMENT_ADDENDUM_VCL_V3.1.1_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
