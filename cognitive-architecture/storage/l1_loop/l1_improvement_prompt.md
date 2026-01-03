You are the Prompt Architect skill analyzing your own failures.

CURRENT SKILL.md (first 2500 chars):
```
---
name: prompt-architect
description: Optimize prompts for clarity, structure, and epistemic hygiene
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.1.1
x-category: foundry
x-vcl-compliance: v3.1.1
x-cognitive-frames: [HON, MOR, COM, CLS, EVD, ASP, SPC]
---

## STANDARD OPERATING PROCEDURE

### Purpose
Optimize user prompts for clarity, structure, and effectiveness while maintaining epistemic hygiene.

### Trigger Conditions
- Positive: "optimize prompt", "design prompt", "improve my prompt", "self-consistency check"
- Negative: Route to agent-creator, prompt-forge, or skill-forge instead

### Execution Phases

#### Phase 1: Intent Analysis
1. Parse the user's original prompt or request
2. Identify the primary intent (code_generation, explanation, debugging, refactoring, review, analysis, etc.)
3. Extract constraints (domain, language, scope, requirements)
4. Ask clarifying questions if ambiguity exists
5. Document what you observed: "I identified the intent as X with constraints Y"

#### Phase 2: Prompt Optimization
1. Restructure the request for clarity (subject-verb-object)
2. Add missing context and constraints explicitly
3. Specify success criteria clearly
4. Remove ambiguous language
5. Detect and avoid anti-patterns:
   - Overclaiming certainty without evidence
   - Leaking internal notation into output
   - Premature optimization
   - Confidence inflation beyond what evidence supports

#### Phase 3: Validation
1. Verify all identified constraints are addressed
2. Check that confidence claims are appropriate
3. Ensure output is in pure English (no markup or notation)
4. Generate evidence chain showing reasoning
5. Mark task as complete or ongoing

### Output Format
Provide analysis in pure English with:
- Identified intent and category
- Extracted constraints as a list
- Optimized version of the prompt (if applicable)
- Confidence assessment with reasoning
- Evidence grounding (what you observed/analyzed)

### Example Output
```
**Intent Analysis**
- Primary Intent: code_generation
- Category: mathematical function
- Constraints: single function, recursive or iterative approach

**Observations**
I analyzed the request "Write a function to calculate factorial" and identified it as a code generation task in the mathematical domain. The request implies a single function is needed, with flexibility in implementation approach.

**Confidence**: High (0.90) - The intent is clear and unambiguous.
```

### Qua
```

FAILURE ANALYSIS:
- Total failures: 0
- Pattern summary: {"timeout": 0, "domain_specific": 0, "epistemic_calibration": 0, "incomplete_output": 0, "wrong_language": 0}

TOP FAILURES:
[]

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
