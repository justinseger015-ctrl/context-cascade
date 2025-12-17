

## When to Use This Skill

- **Tool Usage**: When you need to execute specific tools, lookup reference materials, or run automation pipelines
- **Reference Lookup**: When you need to access documented patterns, best practices, or technical specifications
- **Automation Needs**: When you need to run standardized workflows or pipeline processes

## When NOT to Use This Skill

- **Manual Processes**: Avoid when manual intervention is more appropriate than automated tools
- **Non-Standard Tools**: Do not use when tools are deprecated, unsupported, or outside standard toolkit

## Success Criteria

- **Tool Executed Correctly**: Verify tool runs without errors and produces expected output
- **Reference Accurate**: Confirm reference material is current and applicable
- **Pipeline Complete**: Ensure automation pipeline completes all stages successfully

## Edge Cases

- **Tool Unavailable**: Handle scenarios where required tool is not installed or accessible
- **Outdated References**: Detect when reference material is obsolete or superseded
- **Pipeline Failures**: Recover gracefully from mid-pipeline failures with clear error messages

## Guardrails

- **NEVER use deprecated tools**: Always verify tool versions and support status before execution
- **ALWAYS verify outputs**: Validate tool outputs match expected format and content
- **ALWAYS check health**: Run tool health checks before critical operations

## Evidence-Based Validation

- **Tool Health Checks**: Execute diagnostic commands to verify tool functionality before use
- **Output Validation**: Compare actual outputs against expected schemas or patterns
- **Pipeline Monitoring**: Track pipeline execution metrics and success rates

# Phase 2: Pilot Skills Selection
You are executing a multi-stage workflow with defined phase gates. Follow the prescribed sequence rigorously. Validate completion criteria at each stage before advancing. Maintain state consistency across phases. Document decision points and branching logic clearly.
You are executing a multi-stage workflow with defined phase gates. Follow the prescribed sequence rigorously. Validate completion criteria at each stage before advancing. Maintain state consistency across phases. Document decision points and branching logic clearly.

**Date**: 2025-11-02
**Purpose**: Select 10 diverse skills to test enhancement pipeline velocity and quality

## Selection Criteria

### Diversity Dimensions
1. **Complexity**: Simple utility → Complex orchestration
2. **Domain**: Development, Testing, Documentation, Infrastructure, Research
3. **Agent Usage**: Pure LLM → Multi-agent coordination
4. **Current State**: 1 file only → Partial structure
5. **Target Tier**: Bronze → Gold (mix of targets)

## Pilot Skills Selected (10)

### 1. **base-template-generator** (Domain: Code Generation)
- **Current**: Incomplete (skill.md only)
- **Target**: Bronze tier (3 files)
- **Complexity**: Low - Simple boilerplate generation
- **Rationale**: Tests basic enhancement for utility skills

### 2. **debugging** (Domain: Development)
- **Current**: Incomplete (skill.md only)
- **Target**: Silver tier (7+ files)
- **Complexity**: Medium - Systematic debugging methodology
- **Rationale**: Common use case, moderately complex

### 3. **code-analyzer** (Domain: Development)
- **Current**: Incomplete (skill.md only)
- **Target**: Gold tier (12+ files)
- **Complexity**: Medium-High - Static analysis + agent coordination
- **Rationale**: Tests integration with Connascence MCP tools

### 4. **api-docs** (Domain: Documentation)
- **Current**: Incomplete (skill.md only)
- **Target**: Silver tier (7+ files)
- **Complexity**: Medium - OpenAPI spec generation
- **Rationale**: Documentation skill, template-heavy

### 5. **cicd-engineer** (Domain: Infrastructure)
- **Current**: Incomplete (skill.md only)
- **Target**: Gold tier (12+ files)
- **Complexity**: High - CI/CD pipeline orchestration
- **Rationale**: Infrastructure skill, multi-platform integration

### 6. **micro-skill-creator** (Domain: Meta)
- **Current**: Incomplete (skill.md only)
- **Target**: Silver tier (7+ files)
- **Complexity**: Medium - Skill creation for atomic skills
- **Rationale**: Meta skill (creates other skills), tests dogfooding

### 7. **researcher** (Domain: Research)
- **Current**: Incomplete (skill.md only)
- **Target**: Silver tier (7+ files)
- **Complexity**: Medium - Information gathering + synthesis
- **Rationale**: Research domain, Gemini integration

### 8. **tester** (Domain: Testing)
- **Current**: Incomplete (skill.md only)
- **Target**: Gold tier (12+ files)
- **Complexity**: Medium-High - Test generation + execution
- **Rationale**: Testing domain, high automation potential

### 9. **reviewer** (Domain: Quality)
- **Current**: Incomplete (skill.md only)
- **Target**: Silver tier (7+ files)
- **Complexity**: Medium - Code review patterns
- **Rationale**: Quality domain, agent-powered analysis

### 10. **prompt-architect** (Domain: AI Engineering)
- **Current**: Incomplete (skill.md only)
- **Target**: Bronze tier (3 files)
- **Complexity**: Low-Medium - Prompt optimization
- **Rationale**: AI engineering domain, simple use case

## Diversity Matrix

| Skill | Complexity | Domain | Target Tier | Agent Type | Special Features |
|-------|-----------|--------|-------------|------------|------------------|
| base-template-generator | Low | Code Gen | Bronze | Single | Boilerplate |
| debugging | Medium | Dev | Silver | Single | Systematic |
| code-analyzer | Med-High | Dev | Gold | Multi | MCP Integration |
| api-docs | Medium | Docs | Silver | Single | Templates |
| cicd-engineer | High | Infra | Gold | Multi | Multi-platform |
| micro-skill-creator | Medium | Meta | Silver | Single | Dogfooding |
| researcher | Medium | Research | Silver | Single | Gemini |
| tester | Med-High | Testing | Gold | Multi | Automation |
| reviewer | Medium | Quality | Silver | Multi | Analysis |
| prompt-architect | Low-Med | AI Eng | Bronze | Single | Optimization |

## Target Distribution

- **Bronze** (3 files): 2 skills (20%)
- **Silver** (7+ files): 5 skills (50%)
- **Gold** (12+ files): 3 skills (30%)

## Expected Outcomes

### Velocity Metrics
- **Bronze**: 2-3 hours per skill
- **Silver**: 3-4 hours per skill
- **Gold**: 4-5 hours per skill
- **Total estimated**: 35-40 hours with 4-agent parallelization

### Quality Metrics
- **Audit score**: ≥85% for all skills
- **GO decision**: 100% pass rate
- **MECE compliance**: 100%

### Learning Objectives
1. Validate Bronze/Silver/Gold tier distinctions
2. Test pipeline on diverse domains
3. Measure actual velocity vs estimates
4. Identify pain points and bottlenecks
5. Refine automation scripts
6. Test meta skill integration (micro-skill-creator)
7. Validate MCP tool integration (code-analyzer)

## Success Criteria

- ✅ All 10 skills enhanced successfully
- ✅ All 10 skills pass audit (≥85%)
- ✅ Average enhancement time ≤ 4 hours per skill
- ✅ Pipeline refinements identified and documented
- ✅ Quality maintained (no regression from functionality-audit)

## Next Steps

1. Generate enhancement plans for all 10 skills
2. Execute parallel enhancements (batches of 5)
3. Audit all enhanced skills
4. Measure metrics and compare to estimates
5. Document findings and refinements
6. Proceed to Phase 3 (batch enhancement of 246 remaining skills)
