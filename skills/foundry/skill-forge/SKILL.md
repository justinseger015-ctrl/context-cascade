---
name: skill-forge
description: Meta-skill for producing production-grade skills with complete structure, validation, and self-improvement loops.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.1
x-category: foundry
x-last-reflection: 2026-01-05T00:00:00Z
x-reflection-count: 1
x-vcl-compliance: v3.1.1
x-cognitive-frames: [HON, MOR, COM, CLS, EVD, ASP, SPC]
---

### L1 Improvement
- Re-sequenced the forge SOP into Skill Forge required sections with explicit guardrails, hooks, and validation gates surfaced earlier.
- Preserved adversarial validation and dogfooding requirements while adding prompt-architect ceiling discipline across outputs.

## STANDARD OPERATING PROCEDURE

### Purpose
Create or upgrade skills so they ship with full directory structure, SKILL.md content, examples, tests, references, and validation evidence.

### Trigger Conditions
- Positive: "create skill", "optimize skill", "adversarial validation", "skill improvement".
- Negative/reroute: micro-skill creation (micro-skill-creator), agent design (agent-creator/agent-creation), prompt-only tuning (prompt-architect/prompt-forge).

### Guardrails
- Structure-first: always produce SKILL.md plus examples/ and tests/; prefer resources/ and references/.
- Adversarial validation is mandatory (boundary, failure, chain-of-verification); do not declare done without evidence.
- Self-application required: run dogfooding loop until improvement delta < 2% or risks documented.
- Enforce confidence ceilings in outputs; English-only user-facing content.
- Hooks latency targets: pre_hook_target_ms 20 (max 100); post_hook_target_ms 100 (max 1000).

### Execution Phases
1. **Requirements Analysis**: Parse requested skill, domain, constraints, and success criteria; check reuse options.
2. **Structure Design**: Lay out directories and placeholders per required sections; log any deviations.
3. **Skill Definition**: Author SKILL.md with frontmatter, SOP, guardrails, integrations, IO contracts, and anti-patterns.
4. **Adversarial Validation**: Run boundary/failure/COV checks; capture evidence and metrics.
5. **Dogfooding Loop**: Apply skill-forge to itself or the target skill; iterate until convergence threshold or timebox.
6. **Packaging & Delivery**: Package skill as .skill file and deliver:
   ```
   # Package new skill:
   powershell scripts/skill-packaging/skill-package.ps1 -SkillFolder <path> -CopyToPackaged -Force

   # Edit existing .skill:
   powershell scripts/skill-packaging/skill-edit.ps1 -Action edit -SkillPath <path>.skill
   ```
   - Validate SKILL.md exists with required sections
   - Package folder contents as .zip, rename to .skill
   - Copy to skills/packaged/ directory
   - Verify package size and contents
   - Record delivery notes with confidence ceilings

### Pattern Recognition
- Greenfield skill → prioritize purpose, triggers, and contracts before details.
- Legacy skill migration → map to required sections and fill gaps with TODOs + owners.
- High-risk domain → expand adversarial probes and safety guardrails.

### Advanced Techniques
- Use checklists from REQUIRED-SECTIONS.md to ensure tier coverage.
- Apply contrastive examples to define scope and refusal boundaries.
- Capture MCP tagging (WHO=skill-forge-{session}, WHY=skill-execution) for traceability.

### Common Anti-Patterns
- Missing required sections (overview, workflows, integrations, closure).
- Skipping validation or omitting confidence ceilings.
- Generic cross-skill notes without actionable coordination.

### Practical Guidelines
- Keep instructions concise but complete; link to references for depth.
- Prefer deterministic output schemas for examples/tests.
- Document open risks and next steps when timeboxed.

### Cross-Skill Coordination
- Upstream: prompt-architect for clarity; cognitive-lensing for alternative framings.
- Parallel: meta-tools for supporting utilities; base-template-generator for scaffolds when code is included.
- Downstream: agent-creator/agent-selector for routing; recursive-improvement for ongoing tuning.

### MCP Requirements
- Memory/vector search recommended for pattern reuse; tag WHO=skill-forge-{session}, WHY=skill-execution.
- Record hooks/performance expectations in outputs.

### Input/Output Contracts
```yaml
inputs:
  skill_name: string  # required
  category: string  # required
  domain: string  # optional domain focus
  constraints: list[string]  # optional constraints and policies
outputs:
  skill_folder: directory  # skills/{category}/{skill_name}/
  skill_artifacts:
    - SKILL.md           # required - main skill definition
    - readme.md          # recommended - quick start guide
    - examples/*.md      # required - usage examples
    - tests/*.md         # required - validation tests
    - references/*.md    # optional - methodology docs
    - resources/*        # optional - templates, scripts
  skill_package: file    # {skill_name}.skill in skills/packaged/
  validation_report: file  # adversarial and COV results
  delivery_notes: summary  # packaging summary, risks, and next steps
```

### Recursive Improvement
- Self-apply: `skill_forge.improve(skill_forge)`; log iterations and stop at <2% delta or explicit risk acceptance.

### Examples
- Forge a security-audit skill with dependency review tests and refusal policy.
- Upgrade an orchestration skill to include cross-skill coordination and MCP requirements.

### Troubleshooting
- Missing sections → consult REQUIRED-SECTIONS.md and add content/TODO with owner.
- Validation gaps → create or update tests before delivery; document any deferrals.
- Convergence slow → tighten hypotheses and focus on highest-risk gaps.

### Completion Verification
- [ ] Required directories present (SKILL.md, examples/, tests/)
- [ ] SKILL.md includes all tiers (frontmatter, SOP, integrations, closure)
- [ ] Adversarial validation executed with evidence and ceilings
- [ ] Dogfooding loop run or explicitly deferred with rationale
- [ ] **Skill packaged as .skill file** using skill-package.ps1
- [ ] **Package copied to skills/packaged/** directory
- [ ] Delivery notes include risks, hooks, and MCP tags

### Skill Editing Workflow
To update an existing .skill file:
```powershell
# 1. Unpack for editing
.\scripts\skill-packaging\skill-edit.ps1 -Action unpack -SkillPath skills/packaged/myskill.skill

# 2. Edit files in myskill-edit/ folder

# 3. Repack
.\scripts\skill-packaging\skill-edit.ps1 -Action pack -SkillPath myskill-edit -EditPath skills/packaged/myskill.skill -Force
```

Or use interactive mode:
```powershell
.\scripts\skill-packaging\skill-edit.ps1 -Action edit -SkillPath skills/packaged/myskill.skill
```

---

## LEARNED PATTERNS

### Medium Confidence [conf:0.75]
- Include .skill packaging as explicit final step in skill creation workflow [ground:user-directive:2026-01-05]
  - Context: User expects packaged output, not just source files
  - Action: Always run skill-package.ps1 before declaring skill complete

### Low Confidence [conf:0.55]
- TodoWrite tracking throughout multi-file creation improves workflow visibility [ground:observation:2026-01-05]
  - Context: No corrections received during 8-task tracked workflow
  - Action: Use TodoWrite for all multi-step skill creation sessions

---

Confidence: 0.75 (ceiling: inference 0.70) - Skill Forge SOP updated with .skill packaging workflow.
