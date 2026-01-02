You are the Prompt Architect skill analyzing your own failures.

CURRENT SKILL.md (first 2500 chars):
```
---
name: prompt-architect
description: Meta-loop skill for prompt optimization using VERILINGUA VCL + VERIX v3.1.1
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.1.1
x-category: foundry
x-vcl-compliance: v3.1.1
x-cognitive-frames: [HON, MOR, COM, CLS, EVD, ASP, SPC]
---

<!-- =========================================================================
     PROMPT ARCHITECT v3.1.1 :: VERILINGUA VCL + VERIX COMPLIANT

     VCL 7-Slot System: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC
     Default Output: L2 English (human-facing)
     Immutable Rules: EVD >= 1, ASP >= 1
     ========================================================================= -->

---
<!-- S0 META-IDENTITY -->
---

[define|neutral] SKILL := {
  name: "prompt-architect",
  category: "foundry",
  version: "3.1.1",
  layer: L2,
  vcl_compliance: "v3.1.1"
} [ground:given] [conf:0.95] [state:confirmed]

[define|neutral] COGNITIVE_FRAME := {
  frame: "Compositional",
  source: "German",
  force: "Build from primitives?"
} [ground:cognitive-science] [conf:0.85] [state:confirmed]

---
<!-- S1 VCL 7-SLOT SYSTEM REFERENCE -->
---

[define|neutral] VCL_SLOT_ORDER := {
  order: ["HON", "MOR", "COM", "CLS", "EVD", "ASP", "SPC"],
  rule: "Slots MUST appear in this order when present",
  enforcement: "E1"
} [ground:vcl-spec-v3.1.1] [conf:0.90] [state:confirmed]

[define|neutral] VCL_SLOT_HON := {
  name: "Honorific",
  source: "Japanese keigo",
  purpose: "Audience register selection",
  values: ["teineigo", "sonkeigo", "kenjougo"],
  weight: 0.08,
  enforcement: 0
} [ground:vcl-spec-v3.1.1] [conf:0.90] [state:confirmed]

[define|neutral] VCL_SLOT_MOR := {
  name: "Morphological",
  source: "Arabic trilateral roots",
  purpose: "Semantic decomposition into root components",
  notation: "root:X-Y-Z",
  weight: 0.10,
  enforcement: 0
} [ground:vcl-spec-v3.1.1] [conf:0.90] [state:confirmed]

[define|neutral] VCL_SLOT_COM := {
  name: "Compositional",
  source: "German compounding",
  purpose: "Build concepts from primitives",
  notation: "Concept+From+Parts",
  weight: 0.10,
  enforcement: 0
} [ground:vcl-spec-v3.1.1] [conf:0.90] [state:confirmed]

[define|neutral] VCL_SLOT_CLS := {
  name: "Classifier",
  source: "Chinese classifiers",
  purpose: "Semantic typing and counting",
  notation: "type_specifier",
  weight: 0.08,
  enforcement: 0
} [ground:vcl-spec-v3.1.1] [conf:0.90] [state:confirmed]

[define|neutral] VCL_SLOT_EVD := {
  name: "Evidential",
  
```

FAILURE ANALYSIS:
- Total failures: 11
- Pattern summary: {"timeout": 3, "domain_specific": 2, "epistemic_calibration": 2, "incomplete_output": 1, "wrong_language": 2}

TOP FAILURES:
[
  {
    "id": "PA-017",
    "category": "prompt_optimization",
    "issue": "The skill execution failed due to a CLI timeout after 5 minutes, producing no usable output. The task required creating a diagnostic prompt for test failures, but nothing was generated. Intent was not"
  },
  {
    "id": "PA-020",
    "category": "prompt_optimization",
    "issue": "The skill failed to address the success criteria which explicitly requires 'idiomatic Go patterns'. The output is generic and language-agnostic, mentioning TypeScript, Python, and Rust but never Go. W"
  },
  {
    "id": "PA-021",
    "category": "prompt_optimization",
    "issue": "The skill failed to execute due to a timeout error. No actual output was produced, so intent accuracy, constraint coverage, output quality, and VERIX compliance cannot be evaluated and receive 0.0 sco"
  },
  {
    "id": "PA-023",
    "category": "prompt_optimization",
    "issue": "The skill correctly identified that 'add caching' is ambiguous and needs clarification, which shows good intent recognition. However, the success criteria specifically states 'Converts caching into sp"
  },
  {
    "id": "PA-024",
    "category": "prompt_optimization",
    "issue": "The success criteria explicitly requires transforming 'accessibility' into a WCAG compliance checklist, but the skill output only mentions WCAG as one of four options (Option D) and provides no actual"
  },
  {
    "id": "PA-025",
    "category": "prompt_optimization",
    "issue": "The success criteria explicitly requires 'Creates incremental TypeScript migration plan', but the skill output pivoted to Python type hints instead. While the skill correctly identified the codebase i"
  },
  {
    "id": "PA-027",
    "category": "prompt_optimization",
    "issue": "The skill correctly identified that 'add authentication' is vague and needs clarification - this is good prompt architect behavior. However, the success criteria specified 'Converts auth into complete"
  },
  {
    "id": "PA-039",
    "category": "anti_pattern_detection",
    "issue": "The skill partially identified the anti-pattern nature of 'connection per request' by noting it's 'generally considered an anti-pattern' with valid reasons (overhead, resource exhaustion, performance)"
  }
]

Based on these failures, propose ONE specific improvement to add to SKILL.md.

The improvement should:
1. Address the root cause of at least 2+ failures
2. Be a new rule, constraint, or pattern
3. Be concise and actionable
4. Use VERIX format for internal documentation

Output ONLY the improvement text (no explanation):

Example format:
### Domain-Specific Context Rule
[assert|emphatic] When success criteria mention a specific technology (Go, Django, WCAG, TypeScript), the output MUST explicitly address that technology's idioms and patterns. [ground:witnessed:eval-failures-PA-020-023-024-025] [conf:0.90]

- If criteria mentions "Go", include Go-specific patterns (error wrapping with %w, errors.Is/As)
- If criteria mentions "Django", include Django-specific solutions (cache framework, decorators)
- If criteria mentions "WCAG", provide actual compliance checklist with specific criteria
- If criteria mentions "TypeScript", address type-safe migration patterns
