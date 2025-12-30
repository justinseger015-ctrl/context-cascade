# Comprehensive Implementation Plan
## VERILINGUA x VERIX x DSPy x GlobalMOO Integration

**Branch**: `feature/veralingua-moo-integration`
**Version**: 2.0.0 (Full System Integration)

---

## System Components Available

### MCPs (Model Context Protocol Servers)
| MCP | Purpose | Use In This Project |
|-----|---------|---------------------|
| `memory-mcp` | Triple-layer persistence (KV, Graph, Events) | Store optimization state, Pareto points, mode configs |
| `memory-triple-layer` | Extended memory with vector DB | Semantic search for similar configs |
| `sequential-thinking` | Structured reasoning | Complex optimization decisions |
| `connascence-analyzer` | Code quality analysis | Quality gates for generated code |

### Agents (211 Total - Key Selections)
| Category | Agent | Use Case |
|----------|-------|----------|
| `delivery/backend` | `backend-dev` | Python core module implementation |
| `quality/analysis` | `code-analyzer` | Code quality validation |
| `quality/testing` | `tester` | Test suite generation |
| `research` | `researcher` | DSPy/GlobalMOO research |
| `orchestration/swarm` | `hierarchical-coordinator` | Multi-phase coordination |
| `platforms/ai-ml` | `automl-optimizer` | GlobalMOO integration |
| `foundry/core` | `base-template-generator` | Boilerplate generation |

### Skills (196 Total - Key Selections)
| Skill | Purpose |
|-------|---------|
| `feature-dev-complete` | 12-stage lifecycle for each module |
| `cascade-orchestrator` | Multi-skill coordination |
| `code-review-assistant` | Post-phase audits |
| `testing-quality` | Test generation |
| `functionality-audit` | Execution verification |
| `documentation` | API docs generation |

### Scripts Available
- `validate_skill.py` - Skill validation
- `test_generator.py` - Test generation
- `multi_agent_review.py` - Code review
- `workflow_executor.py` - Workflow execution
- `parallel_exec.py` - Parallel execution

---

## Architecture: Four-Phase Cascade with Ralph Loops

```
PHASE 0: FOUNDATION (Sequential)
    |
    +-> Ralph Loop: "Build core infrastructure"
    |   Promise: FOUNDATION_COMPLETE
    |   Max Iter: 20
    |
    +-> Audit: Connascence + Code Review
    |
    +-> Memory: Store in expertise/cognitive-architecture
    |
    v
PHASE 1: EVALUATION SYSTEM (Parallel)
    |
    +-> Ralph Loop: "Build evaluation metrics"
    |   Promise: EVAL_SYSTEM_COMPLETE
    |   Max Iter: 25
    |
    +-> [PARALLEL TASKS]:
    |   - Task("Metrics Dev", "Build metrics.py", "backend-dev")
    |   - Task("Grader Dev", "Build graders/", "backend-dev")
    |   - Task("Corpus Creator", "Build task corpus", "researcher")
    |   - Task("Tester", "Build test suite", "tester")
    |
    +-> Audit: Functionality + Theater Detection
    |
    +-> Memory: Store evaluation patterns
    |
    v
PHASE 2: OPTIMIZATION INTEGRATION (Sequential -> Parallel)
    |
    +-> Ralph Loop: "Integrate GlobalMOO + DSPy"
    |   Promise: OPTIMIZATION_COMPLETE
    |   Max Iter: 30
    |
    +-> [SEQUENTIAL FIRST]:
    |   - GlobalMOO client (needs API tested)
    |   - Verify connection with provided key
    |
    +-> [THEN PARALLEL]:
    |   - Task("DSPy Dev", "Build dspy_level2.py", "backend-dev")
    |   - Task("Cascade Dev", "Build cascade.py", "backend-dev")
    |   - Task("Mode Distiller", "Build distill_modes.py", "backend-dev")
    |
    +-> Audit: Integration + Performance
    |
    +-> Memory: Store optimization results
    |
    v
PHASE 3: COMMAND INTEGRATION (Parallel)
    |
    +-> Ralph Loop: "Integrate with Claude Code"
    |   Promise: INTEGRATION_COMPLETE
    |   Max Iter: 15
    |
    +-> [PARALLEL TASKS]:
    |   - Task("Command Dev", "Build /mode command", "backend-dev")
    |   - Task("Skill Creator", "Create cognitive-mode skill", "base-template-generator")
    |   - Task("Doc Writer", "Generate API docs", "docs-api-openapi")
    |
    +-> Final Audit: Full system review
    |
    +-> Memory: Store integration patterns
    |
    v
DEPLOY TO BRANCH -> TEST -> MERGE TO MAIN
```

---

## Detailed Phase Breakdown

### PHASE 0: Foundation (Week 1, Days 1-3)

**Ralph Loop Configuration**:
```yaml
session_id: phase-0-foundation
completion_promise: "FOUNDATION_COMPLETE"
max_iterations: 20
quality_gate: true
```

**Sequential Tasks** (must complete in order):

| # | Task | Agent | Skill | Output |
|---|------|-------|-------|--------|
| 1 | Config Dataclasses | `backend-dev` | `feature-dev-complete` | `core/config.py` |
| 2 | VectorCodec | `backend-dev` | `feature-dev-complete` | `core/config.py` (extend) |
| 3 | VERIX Parser | `backend-dev` | `feature-dev-complete` | `core/verix.py` |
| 4 | Frame Registry | `backend-dev` | `feature-dev-complete` | `core/verilingua.py` |
| 5 | PromptBuilder | `backend-dev` | `feature-dev-complete` | `core/prompt_builder.py` |

**Post-Phase Audit**:
```bash
# Run after all tasks complete
Skill("code-review-assistant")  # Multi-agent review
Skill("functionality-audit")     # Verify code executes
Skill("connascence-quality-gate") # No God objects, clean code
```

**Memory Operations**:
```javascript
// Store expertise for future sessions
kv_store.set_json('expertise:cognitive-architecture:foundation', {
    WHO: 'hierarchical-coordinator',
    WHEN: timestamp,
    PROJECT: 'cognitive-architecture',
    WHY: 'phase-completion',
    files: ['core/config.py', 'core/verix.py', 'core/verilingua.py', 'core/prompt_builder.py'],
    patterns: {
        config_vector: 'VectorCodec pattern',
        frame_registry: 'Protocol-based frames',
        verix_parser: 'Regex + structured extraction'
    }
});

// Build knowledge graph
graph.add_relationship('phase:foundation', 'produces', 'module:core');
graph.add_relationship('module:config', 'used_by', 'module:prompt_builder');
```

---

### PHASE 1: Evaluation System (Week 1, Days 4-5 + Week 2, Days 1-2)

**Ralph Loop Configuration**:
```yaml
session_id: phase-1-evaluation
completion_promise: "EVAL_SYSTEM_COMPLETE"
max_iterations: 25
quality_gate: true
```

**Parallel Tasks** (spawn in single message):

```javascript
[Single Message - Golden Rule]:
  Task("Metrics Developer",
       "Build eval/metrics.py with: task_accuracy, token_efficiency, edge_robustness, epistemic_consistency. Use dataclasses. Include anti-gaming normalization.",
       "backend-dev")

  Task("Deterministic Grader Dev",
       "Build eval/graders/deterministic.py with: format_compliance, token_count, latency_measure, regex_checks. Must be 100% reproducible.",
       "backend-dev")

  Task("LLM Judge Dev",
       "Build eval/graders/llm_judge.py with: rubric_scoring, calibration_check. Use Claude API. Include caching.",
       "backend-dev")

  Task("Corpus Researcher",
       "Create tasks/core_corpus.jsonl (50 tasks), tasks/edge_corpus.jsonl (20 adversarial), tasks/holdout.jsonl (30 never-optimize). Diverse task types.",
       "researcher")

  Task("Test Developer",
       "Build comprehensive test suite for eval/ module. pytest fixtures, mocking, 90%+ coverage target.",
       "tester")

  TodoWrite({ todos: [
    {content: "Build metrics.py", status: "in_progress", activeForm: "Building metrics"},
    {content: "Build deterministic graders", status: "pending", activeForm: "Building graders"},
    {content: "Build LLM judge", status: "pending", activeForm: "Building LLM judge"},
    {content: "Create task corpora", status: "pending", activeForm: "Creating corpora"},
    {content: "Write test suite", status: "pending", activeForm: "Writing tests"},
    {content: "Run post-phase audit", status: "pending", activeForm: "Running audit"}
  ]})
```

**Post-Phase Audit**:
```javascript
// Parallel audits
[Single Message]:
  Skill("functionality-audit")      // Verify all evaluators work
  Skill("theater-detection-audit")  // No fake/placeholder code
  Skill("testing-quality")          // Validate test coverage
```

**Memory Operations**:
```javascript
// Store evaluation patterns
kv_store.set_json('expertise:cognitive-architecture:evaluation', {
    WHO: 'hierarchical-coordinator',
    WHEN: timestamp,
    PROJECT: 'cognitive-architecture',
    WHY: 'phase-completion',
    metrics: ['task_accuracy', 'token_efficiency', 'edge_robustness', 'epistemic_consistency'],
    anti_gaming: ['length_normalization', 'format_as_submetric'],
    corpus_stats: {
        core: 50,
        edge: 20,
        holdout: 30
    }
});

// Track evaluation relationships
graph.add_relationship('phase:evaluation', 'produces', 'module:eval');
graph.add_relationship('module:metrics', 'validates', 'module:core');
```

---

### PHASE 2: Optimization Integration (Week 2, Days 3-5)

**Ralph Loop Configuration**:
```yaml
session_id: phase-2-optimization
completion_promise: "OPTIMIZATION_COMPLETE"
max_iterations: 30
quality_gate: true
```

**Sequential First** (GlobalMOO must work before parallel):

```javascript
// Step 1: Verify GlobalMOO connection
Task("GlobalMOO Integrator",
     "Build optimization/globalmoo_client.py. Test connection with API key. Implement: create_model, create_project, load_cases, suggest_inverse. Handle errors gracefully.",
     "backend-dev")

// Wait for completion, then verify
// Run: python -c "from optimization.globalmoo_client import Client; c = Client(); print(c.test_connection())"
```

**Then Parallel** (after GlobalMOO verified):

```javascript
[Single Message - Golden Rule]:
  Task("DSPy Developer",
       "Build optimization/dspy_level2.py. Implement: cluster_key generation, FrameActivatedReasoning signature, CognitiveModule, prompt caching per cluster. Use MIPROv2 optimizer.",
       "backend-dev")

  Task("Cascade Developer",
       "Build optimization/cascade.py. Implement Three-MOO Cascade: Phase A (structure), Phase B (edge discovery), Phase C (production frontier). Orchestrate GlobalMOO calls.",
       "backend-dev")

  Task("Mode Distiller",
       "Build optimization/distill_modes.py. Implement: Pareto clustering, representative selection, mode naming (Audit/Speed/Research/Math/Synthesis). Output YAML.",
       "backend-dev")

  Task("Level 1 Developer",
       "Build optimization/dspy_level1.py. Implement: aggregate telemetry analysis, structural change proposals, PR generation. Monthly cadence.",
       "backend-dev")

  TodoWrite({ todos: [
    {content: "Verify GlobalMOO connection", status: "completed", activeForm: "Verified"},
    {content: "Build DSPy Level 2", status: "in_progress", activeForm: "Building DSPy"},
    {content: "Build Three-MOO Cascade", status: "pending", activeForm: "Building cascade"},
    {content: "Build mode distiller", status: "pending", activeForm: "Building distiller"},
    {content: "Build DSPy Level 1", status: "pending", activeForm: "Building Level 1"},
    {content: "Integration testing", status: "pending", activeForm: "Testing integration"}
  ]})
```

**Post-Phase Audit**:
```javascript
[Single Message]:
  Skill("functionality-audit")     // End-to-end optimization works
  Skill("code-review-assistant")   // Security review (API keys)
  Skill("performance-analysis")    // Latency acceptable
```

**Memory Operations**:
```javascript
// Store optimization patterns
kv_store.set_json('expertise:cognitive-architecture:optimization', {
    WHO: 'hierarchical-coordinator',
    WHEN: timestamp,
    PROJECT: 'cognitive-architecture',
    WHY: 'phase-completion',
    components: {
        globalmoo: 'Client wrapper with inverse queries',
        dspy_l2: 'Cluster-based prompt caching',
        dspy_l1: 'Monthly evolution analysis',
        cascade: 'Three-phase MOO orchestration',
        modes: 'Pareto-derived presets'
    },
    api_config: {
        globalmoo_uri: 'https://api.globalmoo.ai/api',
        env_var: 'GLOBALMOO_API_KEY'
    }
});

// Build optimization graph
graph.add_relationship('phase:optimization', 'produces', 'module:optimization');
graph.add_relationship('module:globalmoo_client', 'calls', 'api:globalmoo');
graph.add_relationship('module:dspy_level2', 'produces', 'artifact:compiled_prompts');
graph.add_relationship('module:distill_modes', 'produces', 'artifact:mode_library');
```

---

### PHASE 3: Command Integration (Week 3, Days 1-3)

**Ralph Loop Configuration**:
```yaml
session_id: phase-3-integration
completion_promise: "INTEGRATION_COMPLETE"
max_iterations: 15
quality_gate: true
```

**Parallel Tasks**:

```javascript
[Single Message - Golden Rule]:
  Task("Command Developer",
       "Create commands for CLAUDE.md: /mode, /eval, /optimize, /pareto, /frame, /verix. Follow existing command patterns. Integration with PromptBuilder.",
       "backend-dev")

  Task("Skill Creator",
       "Create skills/cognitive-mode/SKILL.md. Frame selection skill. VERIX enforcement skill. Mode auto-selection skill. Follow skill-forge template.",
       "base-template-generator")

  Task("Hook Developer",
       "Create hooks for cognitive architecture: PreToolUse for frame injection, PostToolUse for VERIX validation, Stop for mode persistence.",
       "backend-dev")

  Task("Documentation Writer",
       "Generate comprehensive docs: API reference, integration guide, mode descriptions, troubleshooting. OpenAPI for external API.",
       "docs-api-openapi")

  TodoWrite({ todos: [
    {content: "Create Claude Code commands", status: "in_progress", activeForm: "Creating commands"},
    {content: "Create cognitive-mode skill", status: "pending", activeForm: "Creating skill"},
    {content: "Create integration hooks", status: "pending", activeForm: "Creating hooks"},
    {content: "Generate documentation", status: "pending", activeForm: "Generating docs"},
    {content: "Final integration test", status: "pending", activeForm: "Testing integration"}
  ]})
```

**Final Comprehensive Audit**:
```javascript
// Full system audit
[Single Message]:
  Skill("functionality-audit")      // All components work
  Skill("theater-detection-audit")  // No fake code
  Skill("code-review-assistant")    // Multi-agent review
  Skill("documentation")            // Docs complete
  Skill("connascence-quality-gate") // Code quality verified
```

**Memory Operations**:
```javascript
// Store complete integration
kv_store.set_json('expertise:cognitive-architecture:complete', {
    WHO: 'hierarchical-coordinator',
    WHEN: timestamp,
    PROJECT: 'cognitive-architecture',
    WHY: 'project-completion',
    modules: ['core', 'eval', 'optimization', 'modes'],
    commands: ['/mode', '/eval', '/optimize', '/pareto', '/frame', '/verix'],
    skills: ['cognitive-mode'],
    status: 'ready-for-merge'
});

// Final graph relationships
graph.add_relationship('phase:integration', 'completes', 'project:cognitive-architecture');
graph.add_relationship('project:cognitive-architecture', 'enhances', 'project:context-cascade');
```

---

## Execution Timeline

```
WEEK 1
======
Day 1-2: PHASE 0 Foundation (Sequential)
  - Ralph Loop: Build core/ modules
  - Audit: Code review + functionality

Day 3-5: PHASE 1 Evaluation (Parallel)
  - Ralph Loop: Build eval/ in parallel
  - Audit: Theater detection + testing quality

WEEK 2
======
Day 1-2: PHASE 1 cont'd
  - Complete evaluation system
  - Final Phase 1 audit

Day 3-5: PHASE 2 Optimization
  - Sequential: GlobalMOO client
  - Parallel: DSPy + Cascade + Modes
  - Audit: Performance + security

WEEK 3
======
Day 1-3: PHASE 3 Integration
  - Parallel: Commands + Skills + Hooks + Docs
  - Final comprehensive audit

Day 4-5: Testing & Merge
  - Full integration testing
  - Merge to main
```

---

## Quality Gates (After Each Phase)

### Connascence Analyzer Checks
```yaml
quality_thresholds:
  god_objects: 0        # No classes with >15 methods
  parameter_bombs: 0    # No functions with >6 params
  cyclomatic_complexity: 10  # Max complexity per function
  deep_nesting: 4       # Max nesting levels
  long_functions: 50    # Max lines per function
  magic_literals: 0     # No hardcoded values
```

### Automated Checks
```bash
# Run after each phase
python -m pytest tests/ --cov=cognitive-architecture --cov-report=html
python -m pylint cognitive-architecture/ --min-score=8.0
python -m mypy cognitive-architecture/ --strict
```

### Human Review Gates
- **Phase 0**: Verify data structures match VERIX spec
- **Phase 1**: Validate evaluation metrics against research
- **Phase 2**: Test GlobalMOO integration with real API calls
- **Phase 3**: Review command UX with actual usage

---

## Memory Namespace Schema

```yaml
expertise/cognitive-architecture/:
  foundation:     # Phase 0 learnings
  evaluation:     # Phase 1 patterns
  optimization:   # Phase 2 configs
  complete:       # Final integration

findings/cognitive-architecture/:
  {severity}/{id}:  # Code quality issues found

decisions/cognitive-architecture/:
  {decision-id}:    # Architecture decisions made

swarm/cognitive-architecture/:
  {phase-id}:       # Swarm coordination state
```

---

## Rollback Strategy

Each phase creates a git tag before starting:

```bash
git tag phase-0-start
git tag phase-1-start
git tag phase-2-start
git tag phase-3-start
```

If a phase fails beyond max iterations:
1. Cancel Ralph loop
2. Archive state to memory
3. Rollback to previous tag
4. Analyze failure in memory
5. Retry with adjusted approach

---

## Success Criteria

| Metric | Target | How Measured |
|--------|--------|--------------|
| All phases complete | 4/4 | Ralph promises emitted |
| Test coverage | >85% | pytest-cov |
| Lint score | >8.0 | pylint |
| Type coverage | 100% | mypy |
| Zero critical issues | 0 | Connascence analyzer |
| GlobalMOO connected | TRUE | API ping test |
| Mode library generated | 5 modes | YAML file exists |
| Commands working | 6 commands | Manual verification |

---

## Files to Generate

```
cognitive-architecture/
  core/
    __init__.py
    config.py          # FrameworkConfig, PromptConfig, FullConfig, VectorCodec
    verix.py           # VerixClaim, VerixParser
    verilingua.py      # Frame protocol, 7 frame implementations
    prompt_builder.py  # PromptBuilder class
    runtime.py         # Claude client wrapper

  eval/
    __init__.py
    metrics.py         # Metric functions
    graders/
      __init__.py
      deterministic.py # Format, tokens, latency
      llm_judge.py     # Rubric scoring
    edge_cases.py      # Edge case detection
    consistency.py     # Epistemic consistency

  optimization/
    __init__.py
    globalmoo_client.py  # GlobalMOO SDK
    dspy_level2.py       # Prompt clustering
    dspy_level1.py       # Evolution analysis
    cascade.py           # Three-MOO orchestration
    distill_modes.py     # Pareto -> modes

  modes/
    __init__.py
    library.py           # Mode definitions
    selector.py          # Auto-selection
    modes.yaml           # Generated mode configs

  storage/
    logs/                # JSONL logs
    prompts/             # Cached prompts
    results/             # Optimization results

  tasks/
    core_corpus.jsonl    # 50 standard tasks
    edge_corpus.jsonl    # 20 adversarial tasks
    holdout.jsonl        # 30 regression tasks

  tests/
    test_config.py
    test_verix.py
    test_verilingua.py
    test_prompt_builder.py
    test_metrics.py
    test_graders.py
    test_globalmoo.py
    test_dspy.py
    test_cascade.py
    test_modes.py

  .env                   # API keys (gitignored)
  .env.template          # Template
  requirements.txt       # Dependencies
  pyproject.toml         # Project config
```

---

**Ready to Execute**: This plan uses the full Context Cascade system with Ralph loops, parallel agents, memory persistence, quality gates, and comprehensive auditing.
