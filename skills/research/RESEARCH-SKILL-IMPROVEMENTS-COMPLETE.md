# Research Skill Prompt Improvements - Completion Report

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Summary

Successfully applied SKILL-SPECIFIC prompt improvements to ALL 14 research skills.

## Improvements Applied

Each research skill now includes a comprehensive "SKILL-SPECIFIC GUIDANCE" section with:

1. **When to Use This Skill** - Research-specific triggers and contexts
2. **When NOT to Use This Skill** - Anti-patterns and exclusions
3. **Success Criteria** - Measurable outcomes and deliverables
4. **Edge Cases & Limitations** - Failure modes and constraints
5. **Critical Guardrails** - Research ethics and methodology requirements
6. **Evidence-Based Validation** - Verification techniques

## Files Modified (14 total)

### Core Research Skills
- literature-synthesis/SKILL.md
- baseline-replication/SKILL.md
- researcher/SKILL.md
- method-development/SKILL.md
- deep-research-orchestrator/SKILL.md

### Intent & Planning Skills
- intent-analyzer/SKILL.md
- interactive-planner/SKILL.md
- research-driven-planning/SKILL.md

### Idea Generation & Writing Skills
- rapid-idea-generator/SKILL.md
- rapid-manuscript-drafter/SKILL.md

### Visualization & Publication Skills
- research-gap-visualizer/SKILL.md
- visual-asset-generator/SKILL.md
- research-publication/SKILL.md

### Specialized Tools
- specialized-tools/when-gathering-requirements-use-interactive-planner/SKILL.md

## Technical Details

**Location**: `C:/Users/17175/claude-code-plugins/ruv-sparc-three-loop-system/skills/research`

**Insertion Point**: After opening YAML delimiter (`---`) at line 3, before YAML frontmatter (`name:` field)

**Backup Location**: `.backup-complete-20251215-220149/` (contains original unmodified files)

**Script Used**: `apply-all-improvements.py` (Python-based for cross-platform compatibility)

## Verification

```bash
# Total files processed
find . -name "SKILL.md" -type f | wc -l
# Output: 14

# All files have improvements
find . -name "SKILL.md" -type f -exec grep -l "## SKILL-SPECIFIC GUIDANCE" {} \; | wc -l
# Output: 14

# Check specific file structure
head -60 literature-synthesis/SKILL.md
# Shows: ---
#        ## SKILL-SPECIFIC GUIDANCE
#        ### When to Use This Skill
#        ...
#        ---
#        name: literature-synthesis
```

## Example: Literature Synthesis

### Before
```yaml
---
name: literature-synthesis
description: Systematic literature review and synthesis...
version: 1.0.0
```

### After
```yaml
---

## SKILL-SPECIFIC GUIDANCE

### When to Use This Skill
- Academic research requiring systematic literature review (PRISMA-compliant)
- SOTA analysis for Deep Research SOP Phase 1
- Identifying research gaps and opportunities for novel methods
- Preparing related work sections for academic papers
- Validating novelty claims with 50+ peer-reviewed sources

### When NOT to Use This Skill
- Quick fact-checking or single-paper summaries (use researcher skill)
- Non-academic contexts (industry reports, blog posts)
- When <50 papers are sufficient
- Time-constrained projects (<1 week turnaround)

### Success Criteria
- [assert|neutral] Minimum 50 papers reviewed (Quality Gate 1) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] PRISMA flow diagram generated [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] SOTA benchmarks extracted and tabulated [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Research gaps identified with 3+ citations [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] BibTeX database with complete metadata [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] All claims cross-referenced with 2+ independent sources [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases & Limitations
- Paywalled papers: institutional access, contact authors, preprints
- Conflicting results: report both sides, analyze methodology
- Rapidly evolving fields: expand to arXiv, track citations
- Limited dataset access: document limitation, suggest alternatives
- Outdated SOTA: verify publication dates, check newer methods

### Critical Guardrails
- NEVER claim research gaps without systematic evidence (show search strategy)
- ALWAYS document inclusion/exclusion criteria before screening
- NEVER cherry-pick papers (report contradictory evidence)
- ALWAYS verify publication venue tier (h-index, acceptance rates)
- NEVER skip quality assessment (CASP checklist)

### Evidence-Based Validation
- Validate search reproducibility: rerun queries, verify counts
- Cross-validate SOTA benchmarks: Papers with Code, leaderboards
- Verify citation accuracy: match title/author/year
- Test research gap validity: search for contradictory evidence
- Confirm PRISMA compliance: official checklist, 27 items

---
name: literature-synthesis
description: Systematic literature review and synthesis...
version: 1.0.0
```

## Key Features Per Skill

### Literature Synthesis
- When to use: Academic research, SOTA analysis, research gaps, academic papers, novelty validation
- Success criteria: 50+ papers, PRISMA diagram, SOTA benchmarks, 3+ citations per gap
- Guardrails: Never claim gaps without evidence, never cherry-pick, always verify venue tier

### Baseline Replication
- When to use: ML baseline validation, reproducibility challenges, SOTA verification, Quality Gate 1
- Success criteria: +/-1% accuracy, 3+ Docker reproductions, 47+ hyperparameters documented
- Guardrails: Never claim reproduction without t-test, never skip random seeds, always verify SHA256

### Researcher
- When to use: Multi-source investigation (3-5+ sources), credibility scoring >85%, knowledge base building
- Success criteria: 90%+ credibility score, 3+ independent sources, contradictory evidence reported
- Guardrails: Never cite without scoring, never accept <70% credibility, always distinguish facts from opinions

### Method Development
- When to use: Novel ML methods after baseline replication, ablation studies (5+ required), hyperparameter optimization
- Success criteria: p < 0.05, Cohen's d >= 0.5, 95% CIs, Bonferroni correction, power >= 0.8
- Guardrails: Never claim novelty without ablations, never cherry-pick results, always report effect sizes

### Deep Research Orchestrator
- When to use: Complete research lifecycle (Pipelines A-I), multi-month projects, NeurIPS/ICML submissions
- Success criteria: 3 Quality Gates passed, 50+ papers, baseline +/-1%, 6+ evaluation dimensions
- Guardrails: Never skip Quality Gates, never claim production without Gate 3, always coordinate ethics review

### Intent Analyzer
- When to use: Ambiguous requests, multi-step workflows, first principles decomposition, Socratic questioning
- Success criteria: 85%+ confidence, explicit/implicit constraints identified, user confirms optimized request
- Guardrails: Never proceed <80% confidence, never assume technical level, always distinguish constraints

### Interactive Planner
- When to use: Requirements gathering, architecture decisions, feature planning, reducing assumptions
- Success criteria: 5-10 multi-select questions answered, all critical choices captured, plan reflects selections
- Guardrails: Never assume technical choices, never overwhelm with >15 questions, always confirm selections

### Research-Driven Planning
- When to use: Complex features requiring research, high-risk projects, 5x pre-mortem cycles, >97% accuracy
- Success criteria: 3-5+ sources analyzed, 5 pre-mortem cycles, 3+ agent consensus, >97% plan accuracy
- Guardrails: Never skip research phase, always execute 5 pre-mortem cycles, never proceed without consensus

### Rapid Idea Generator
- When to use: Brainstorming research directions, 10+ novel hypotheses, grant proposals, creative problem-solving
- Success criteria: 10+ distinct ideas, testable hypotheses, feasibility assessment, citations to literature
- Guardrails: Never generate without research gaps, never claim novelty without verification, always assess feasibility

### Rapid Manuscript Drafter
- When to use: NeurIPS/ICML/CVPR papers, Deep Research SOP completion, reproducibility reports, grant proposals
- Success criteria: Complete manuscript (all sections), cited claims, proper formatting, reproducibility section
- Guardrails: Never submit uncited claims, never fabricate results, always include reproducibility, always verify template

### Research Gap Visualizer
- When to use: Visualizing research gaps, 2D/3D plots, heatmaps, publication-ready figures, trend analysis
- Success criteria: 300+ DPI figures, clear labels, colorblind-friendly, gap areas highlighted, source data included
- Guardrails: Never use misleading visualizations, always use colorblind palettes, never omit labels, always provide source data

### Research Publication
- When to use: NeurIPS/ICML/CVPR submissions, peer review management, camera-ready versions, artifact archiving
- Success criteria: Paper submitted with all files, reproducibility package published, reviewer responses drafted
- Guardrails: Never ignore reviewer comments, always publish reproducibility packages, never violate anonymity, always archive with DOIs

### Visual Asset Generator
- When to use: Publication-ready figures, architecture diagrams, workflow visualizations, infographics, experimental plots
- Success criteria: 300+ DPI vector formats, clear labels, colorblind-friendly palettes, consistent style, source files included
- Guardrails: Never use raster formats for diagrams, always include captions, never use default matplotlib colors, always provide source code

### When-Gathering-Requirements-Use-Interactive-Planner
- When to use: Triggering interactive-planner, auto-invoking multi-select questions, comprehensive requirements collection
- Success criteria: Interactive-planner successfully invoked, 5-10 questions presented, all critical choices captured
- Guardrails: Never invoke if already active (avoid recursion), never force questions if user has clear requirements, always respect user preference

## Impact

- **Clarity**: Each skill now has clear triggers for when to use vs when NOT to use
- **Quality**: Success criteria provide measurable outcomes for skill execution
- **Safety**: Guardrails prevent common research ethics violations and methodological errors
- **Validation**: Evidence-based validation techniques ensure reproducibility and rigor

## Files Created

1. `apply-all-improvements.py` - Main improvement applicator (Python, cross-platform)
2. `apply-skill-improvements.sh` - Original Bash/sed implementation (deprecated due to Windows compatibility)
3. `RESEARCH-SKILL-IMPROVEMENTS-COMPLETE.md` - This completion report

## Rollback Instructions

If changes need to be reverted:

```bash
# Option 1: Restore from backup
cd C:/Users/17175/claude-code-plugins/ruv-sparc-three-loop-system/skills/research
cp .backup-complete-20251215-220149/*.md */SKILL.md

# Option 2: Restore from git
cd C:/Users/17175/claude-code-plugins/ruv-sparc-three-loop-system
git restore skills/research/**/SKILL.md
```

## Date Completed

December 15, 2025 at 22:01:49

## Total Processing Time

- Script development: ~15 minutes
- Backup creation: ~30 seconds
- Improvements application: ~5 seconds
- Verification: ~2 minutes
- Total: ~18 minutes

**Status**: COMPLETE - All 14 research skills updated successfully with comprehensive prompt improvements.


---
*Promise: `<promise>RESEARCH_SKILL_IMPROVEMENTS_COMPLETE_VERIX_COMPLIANT</promise>`*
