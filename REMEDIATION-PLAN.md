# COGNITIVE ARCHITECTURE REMEDIATION PLAN

## Executive Summary

Based on the Codex audit of the Cognitive Architecture Meta-Loop + Memory MCP Integration,
this plan addresses 7 critical gaps to bring the context-cascade plugin to full operational status.

---

## GAP PRIORITIZATION MATRIX

| Priority | Gap | Impact | Effort | ROI |
|----------|-----|--------|--------|-----|
| P0 | Skill Trigger Matching Pipeline | CRITICAL | Medium | HIGH |
| P0 | VERILINGUA Frame Weight Policy | CRITICAL | Low | HIGH |
| P1 | Memory MCP Integration (unstub) | HIGH | Medium | HIGH |
| P1 | Named Modes Runtime Selector | HIGH | Medium | HIGH |
| P2 | VERIX-VERILINGUA Bidirectional Bridge | MEDIUM | Medium | MEDIUM |
| P2 | Ralph Persistence to Session Manager | MEDIUM | Low | MEDIUM |
| P3 | Telemetry-Driven Mode Steering | LOW | High | LOW |

---

## P0: CRITICAL FIXES (Week 1)

### FIX-1: Skill Trigger Matching Pipeline

**Problem**: 199 skills define TRIGGER_POSITIVE patterns, but no matcher reads them.

**Files to Create/Modify**:
```
cognitive-architecture/skills/trigger_matcher.py      [NEW]
cognitive-architecture/skills/skill_index.json        [NEW]
hooks/enforcement/user-prompt-submit.sh               [MODIFY]
hooks/enforcement/pre-skill-invoke.sh                 [MODIFY]
```

**Implementation Steps**:

1. **Create skill-index.json generator** (`scripts/build-skill-index.py`):
   ```python
   # Scan all SKILL.md files for TRIGGER_POSITIVE
   # Output: {"keyword": ["skill1", "skill2"], ...}
   ```

2. **Create trigger_matcher.py**:
   ```python
   class SkillTriggerMatcher:
       def __init__(self, index_path: str):
           self.index = load_json(index_path)

       def match(self, prompt: str, threshold: float = 0.6) -> List[SkillMatch]:
           # Fuzzy match prompt against TRIGGER_POSITIVE keywords
           # Return ranked list of matching skills
   ```

3. **Modify user-prompt-submit.sh**:
   ```bash
   # Add skill trigger matching
   MATCHES=$(python -c "from trigger_matcher import match; print(match('$PROMPT'))")
   if [ -n "$MATCHES" ]; then
       export SUGGESTED_SKILLS="$MATCHES"
   fi
   ```

4. **Modify pre-skill-invoke.sh**:
   ```bash
   # Accept injected matches from user-prompt-submit
   if [ -n "$SUGGESTED_SKILLS" ]; then
       # Validate skill exists in registry
       # Allow invocation if matched
   fi
   ```

**Acceptance Criteria**:
- [ ] `skill_index.json` generated with all 199 skill triggers
- [ ] `trigger_matcher.py` returns ranked matches for test prompts
- [ ] Hook chain activates skills based on prompt content

---

### FIX-2: VERILINGUA Frame Weight Policy

**Problem**: Frames use boolean toggles only, no numeric weights or evidential minimum.

**Files to Modify**:
```
cognitive-architecture/core/verilingua.py             [MODIFY]
cognitive-architecture/core/config.py                 [MODIFY]
```

**Implementation Steps**:

1. **Add FRAME_WEIGHTS constant** to `verilingua.py`:
   ```python
   FRAME_WEIGHTS = {
       "evidential": 0.95,    # Always high - evidence is foundational
       "aspectual": 0.80,
       "illocutionary": 0.75,
       "modal": 0.70,
       "specificity": 0.65,
       "comparative": 0.60,
       "honorific": 0.50,
   }

   EVIDENTIAL_MINIMUM = 0.30  # Floor for evidential frame activation
   ```

2. **Modify FrameRegistry.get_combined_activation_instruction()**:
   ```python
   def get_combined_activation_instruction(self, task_type: str) -> str:
       active = self.config.active_frames()
       weighted = [(f, FRAME_WEIGHTS.get(f, 0.5)) for f in active]
       weighted.sort(key=lambda x: x[1], reverse=True)

       # Enforce evidential minimum
       if "evidential" in active:
           if FRAME_WEIGHTS["evidential"] < EVIDENTIAL_MINIMUM:
               raise FrameWeightViolation("Evidential below minimum")

       return self._build_instruction(weighted)
   ```

3. **Update FrameworkConfig** to support float weights:
   ```python
   @dataclass
   class FrameworkConfig:
       frame_weights: Dict[str, float] = field(default_factory=lambda: FRAME_WEIGHTS)
       evidential_minimum: float = 0.30
   ```

**Acceptance Criteria**:
- [ ] `FRAME_WEIGHTS` dict added with 7 frame weights
- [ ] `EVIDENTIAL_MINIMUM = 0.30` enforced
- [ ] Weight-based prioritization in activation instruction

---

## P1: HIGH PRIORITY FIXES (Week 2)

### FIX-3: Memory MCP Integration (Unstub)

**Problem**: `memory_mcp_integration.py` simulates interface, never calls real MCP.

**Files to Modify**:
```
cognitive-architecture/optimization/memory_mcp_integration.py   [MODIFY]
```

**Implementation Steps**:

1. **Replace stub with real MCP calls**:
   ```python
   async def _persist_to_mcp(self, key: str, data: dict) -> bool:
       if not self._check_mcp_availability():
           return self._fallback_to_file(key, data)

       # Real MCP call
       result = await self.mcp_client.memory_store(
           namespace="cognitive-architecture",
           key=key,
           value=json.dumps(data),
           metadata={"timestamp": datetime.now().isoformat()}
       )
       return result.success

   async def _load_from_mcp(self, key: str) -> Optional[dict]:
       if not self._check_mcp_availability():
           return self._fallback_from_file(key)

       # Real MCP call
       result = await self.mcp_client.vector_search(
           namespace="cognitive-architecture",
           query=key,
           limit=1
       )
       return result.matches[0].value if result.matches else None
   ```

2. **Add MCP client initialization**:
   ```python
   from memory_mcp import MemoryMCPClient

   class MemoryMCPTelemetryStore:
       def __init__(self, config: dict):
           self.mcp_client = MemoryMCPClient(
               endpoint=config.get("mcp_endpoint", "localhost:50051")
           )
   ```

**Acceptance Criteria**:
- [ ] `memory_store()` called for persistence
- [ ] `vector_search()` called for retrieval
- [ ] Graceful fallback to file when MCP unavailable

---

### FIX-4: Named Modes Runtime Selector

**Problem**: Modes defined in JSON but never applied at runtime.

**Files to Modify**:
```
cognitive-architecture/modes/selector.py              [MODIFY]
cognitive-architecture/core/prompt_builder.py         [MODIFY]
```

**Implementation Steps**:

1. **Wire ModeSelector into PromptBuilder**:
   ```python
   # In prompt_builder.py
   from modes.selector import ModeSelector

   class PromptBuilder:
       def __init__(self, config: FrameworkConfig):
           self.config = config
           self.mode_selector = ModeSelector()

       def build(self, task: str, task_type: str) -> Tuple[str, str]:
           # Determine optimal mode based on task context
           context = self._analyze_task(task, task_type)
           selected_mode = self.mode_selector.select(context)

           # Apply mode configuration
           self._apply_mode(selected_mode)

           # Continue with prompt building
           ...
   ```

2. **Implement mode application**:
   ```python
   def _apply_mode(self, mode: NamedMode):
       # Update config with mode settings
       self.config.update_from_mode(mode)

       # Log mode selection for telemetry
       self._log_mode_selection(mode)
   ```

**Acceptance Criteria**:
- [ ] `ModeSelector.select()` called during prompt building
- [ ] Mode configuration applied before frame activation
- [ ] Mode selection logged for telemetry

---

## P2: MEDIUM PRIORITY FIXES (Week 3)

### FIX-5: VERIX-VERILINGUA Bidirectional Bridge

**Problem**: Only PromptBuilder links them; unidirectional flow.

**Implementation**:
- Add `FrameValidationBridge` class
- Feed VERIX validation results back into frame weights
- Create feedback loop for dynamic frame adjustment

### FIX-6: Ralph Persistence to Session Manager

**Problem**: Stop hook only updates local file, not session manager.

**Files to Modify**:
```
hooks/ralph-wiggum/ralph-loop-stop-hook.sh            [MODIFY]
```

**Implementation**:
```bash
# Add to ralph-loop-stop-hook.sh after line 109
# Persist to session manager
node "$CLAUDE_HOME/hooks/ralph-wiggum/ralph-session-manager.js" persist \
    --iteration "$ITERATION" \
    --state "$STATE_FILE" \
    --timestamp "$(date -Iseconds)"
```

---

## P3: LOW PRIORITY ENHANCEMENTS (Week 4+)

### FIX-7: Telemetry-Driven Mode Steering

**Problem**: Telemetry collected but doesn't steer runtime modes.

**Implementation**:
- Add telemetry analyzer to GlobalMOO client
- Create mode steering engine based on Pareto outcomes
- Wire telemetry into mode selector for dynamic adjustment

---

## EXECUTION PLAN

### Phase 1: Foundation (Days 1-3)
- [ ] Create `scripts/build-skill-index.py`
- [ ] Generate `skill_index.json`
- [ ] Add `FRAME_WEIGHTS` to verilingua.py
- [ ] Add `EVIDENTIAL_MINIMUM` enforcement

### Phase 2: Integration (Days 4-7)
- [ ] Create `trigger_matcher.py`
- [ ] Modify hook chain for skill matching
- [ ] Wire `ModeSelector` into `PromptBuilder`
- [ ] Unstub Memory MCP integration

### Phase 3: Persistence (Days 8-10)
- [ ] Update Ralph stop hook
- [ ] Add VERIX-VERILINGUA bridge
- [ ] Add telemetry feedback loop

### Phase 4: Validation (Days 11-14)
- [ ] Unit tests for all new components
- [ ] Integration tests for hook chain
- [ ] End-to-end test: prompt -> skill trigger -> execution

---

## CODEX TASK TEMPLATES

Use these to create Codex tasks for automated implementation:

### Task 1: Skill Trigger Pipeline
```
Implement a skill trigger matching pipeline for the context-cascade plugin.

1. Create scripts/build-skill-index.py that scans all SKILL.md files
   for TRIGGER_POSITIVE patterns and outputs skills/skill_index.json
2. Create cognitive-architecture/skills/trigger_matcher.py with:
   - SkillTriggerMatcher class
   - match(prompt, threshold) method returning List[SkillMatch]
   - Fuzzy matching using rapidfuzz or similar
3. Modify hooks/enforcement/user-prompt-submit.sh to call trigger_matcher
4. Modify hooks/enforcement/pre-skill-invoke.sh to accept matched skills

Test by running a prompt like "help me debug this API" and verify
debugging-related skills are suggested.
```

### Task 2: VERILINGUA Frame Weights
```
Add numeric frame weights and evidential minimum to VERILINGUA.

1. In cognitive-architecture/core/verilingua.py:
   - Add FRAME_WEIGHTS dict (evidential=0.95 down to honorific=0.50)
   - Add EVIDENTIAL_MINIMUM = 0.30
   - Modify get_combined_activation_instruction() to use weights

2. In cognitive-architecture/core/config.py:
   - Add frame_weights: Dict[str, float] to FrameworkConfig
   - Add evidential_minimum: float = 0.30

3. Add unit tests for weight enforcement
```

---

## SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| Skill trigger match rate | >80% | Test suite of 50 prompts |
| Frame weight compliance | 100% | Evidential never below 0.30 |
| Memory MCP call success | >95% | Telemetry logs |
| Mode selection accuracy | >70% | Task completion correlation |
| Ralph persistence success | 100% | Session recovery tests |

---

## DEPENDENCIES

- `rapidfuzz` for fuzzy matching (pip install rapidfuzz)
- `memory-mcp-client` for MCP integration
- Existing hook chain infrastructure

---

Generated: 2026-01-01
Author: Claude Code + Codex Audit
Repository: DNYoussef/context-cascade
