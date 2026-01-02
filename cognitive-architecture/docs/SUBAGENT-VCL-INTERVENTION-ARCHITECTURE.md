# Subagent VCL Intervention Architecture

## Current Flow (Plain English Prompts)

```
USER REQUEST
     |
     v
+------------------------+
| Phase 1: Intent        |  Skill("intent-analyzer")
| Analysis               |  -> { intent, constraints }
+------------------------+
     |
     v
+------------------------+
| Phase 2: Prompt        |  Skill("prompt-architect")
| Optimization           |  -> { optimized_request }
+------------------------+
     |
     v
+------------------------+
| Phase 3: Planning      |  Skill("planner")
|                        |  -> { tasks: [...] }
+------------------------+
     |
     v
+------------------------+
| Phase 4: Agent         |  Skill("agent-selector")
| Selection              |  -> { selected_agent, capabilities }
+------------------------+
     |
     v
+------------------------+
| Phase 5: Execution     |  Task("Agent", "PROMPT", "type")
|                        |        ^
+------------------------+        |
     |                      INTERVENTION POINT #1
     |                      (currently plain English)
     v
+------------------------+
| Agent Receives:        |
| - agent.md definition  | <-- Already VERIX-annotated
| - PROMPT from Task()   | <-- NOT VCL-ified yet
+------------------------+
     |
     v
+------------------------+
| Agent Executes         |
| (no telemetry capture) | <-- INTERVENTION POINT #2
+------------------------+
```

## Future Flow (VCL-ified Prompts + Telemetry)

```
USER REQUEST
     |
     v
+------------------------+
| Phase 1: Intent        |
| Analysis               |
+------------------------+
     |
     v
+------------------------+
| Phase 2: Prompt        |
| Optimization           |
+------------------------+
     |
     v
+------------------------+
| Phase 3: Planning      |
+------------------------+
     |
     v
+---------------------------+
| Phase 4: Agent Selection  |
| + VCL Frame Config        | <-- NEW: agent-selector returns VCL config
+---------------------------+
     |
     |  { selected_agent, capabilities,
     |    vcl_config: { frames, verix_strictness, compression } }
     v
+---------------------------+
| VCL Prompt Compiler       | <-- NEW COMPONENT
|                           |
| Inputs:                   |
|   - Task description      |
|   - VCL config            |
|   - Agent capabilities    |
|                           |
| Outputs:                  |
|   - VCLPrompt object      |
|   - Prompt version ID     |
+---------------------------+
     |
     v
+---------------------------+
| Phase 5: Execution        |
| Task("Agent",             |
|   VCLPrompt.to_string(),  | <-- VCL-formatted prompt
|   "type")                 |
+---------------------------+
     |
     |  +---------------------------+
     +->| RMIS Telemetry Harness    | <-- Captures execution
        | on_eval_complete(...)     |
        +---------------------------+
              |
              v
        +---------------------------+
        | Language Evolution        |
        | Two-Stage Optimizer       |
        | DSPy Layers               |
        +---------------------------+
              |
              v
        +---------------------------+
        | IMPROVED VCL PROMPTS      |
        | (next iteration)          |
        +---------------------------+
```

## Three Intervention Points

### 1. Task() Prompt Parameter (CRITICAL)

**Current:**
```javascript
Task("Backend Dev", "Build REST API for user authentication", "backend-dev")
                    ^-- plain English, no structure
```

**Future:**
```javascript
Task("Backend Dev", VCLPrompt({
  version: "v1.2.3",
  intent: "api_implementation",
  frames: ["evidential", "compositional"],
  verix: "[direct|neutral] Implement REST API for user authentication with JWT tokens [ground:task-spec] [conf:0.95]",
  constraints: ["REST", "JWT", "PostgreSQL"],
  output: "L2"
}).compile(), "backend-dev")
```

### 2. Agent-Selector Output Enhancement

**Current agent-selector output:**
```json
{
  "selected_agent": "dev-backend-api",
  "capabilities": ["Express.js", "REST", "JWT"],
  "confidence": 0.95
}
```

**Enhanced output with VCL config:**
```json
{
  "selected_agent": "dev-backend-api",
  "capabilities": ["Express.js", "REST", "JWT"],
  "confidence": 0.95,
  "vcl_config": {
    "recommended_frames": ["evidential", "compositional"],
    "verix_strictness": "MODERATE",
    "compression_level": "L2",
    "illocution": "direct",
    "grounding_required": true
  }
}
```

### 3. Execution Telemetry Capture

**Current:** No capture
**Future:** Every Task() call triggers telemetry:

```python
# Automatic capture via hook or wrapper
harness.on_eval_complete(
    loop="PRODUCTION",
    skill=agent_type,
    task_id=f"{pipeline}_{task_id}",
    iteration=execution_count,
    passed=task_success,
    output=agent_output,
    metrics={
        "vcl_version": prompt.version,
        "prompt_hash": hash(prompt),
        "latency_ms": execution_time,
    }
)
```

## Implementation Hooks

### Option A: Claude Code Hook (Recommended)

Create a `pre-task-vcl-compiler` hook:

```javascript
// hooks/pre-task-vcl-compiler.js
module.exports = {
  event: "pre_task_spawn",

  async handler({ taskDescription, agentType, context }) {
    // 1. Get VCL config from agent-selector cache
    const vclConfig = await getVCLConfig(agentType);

    // 2. Compile to VCL prompt
    const vclPrompt = new VCLPrompt({
      description: taskDescription,
      ...vclConfig
    });

    // 3. Return compiled prompt
    return {
      modifiedDescription: vclPrompt.compile(),
      metadata: {
        version: vclPrompt.version,
        prompt_hash: vclPrompt.hash(),
      }
    };
  }
};
```

### Option B: Wrapper Function

Modify how Task() is called in the 5-phase workflow:

```python
def vcl_task(agent_name: str, description: str, agent_type: str):
    """VCL-enhanced Task() wrapper."""

    # 1. Get agent capabilities
    agent_config = get_agent_config(agent_type)

    # 2. Compile VCL prompt
    vcl_prompt = VCLPrompt(
        intent=classify_intent(description),
        frames=agent_config.recommended_frames,
        verix=format_verix(description),
        constraints=extract_constraints(description),
    )

    # 3. Start telemetry
    task_id = generate_task_id()
    start_time = time.time()

    # 4. Execute
    result = Task(agent_name, vcl_prompt.compile(), agent_type)

    # 5. Capture telemetry
    harness.on_eval_complete(
        loop="PRODUCTION",
        skill=agent_type,
        task_id=task_id,
        passed=result.success,
        output=result.output,
        metrics={
            "vcl_version": vcl_prompt.version,
            "latency_ms": (time.time() - start_time) * 1000,
        }
    )

    return result
```

## VCL Prompt Schema (Detailed)

```python
@dataclass
class VCLPrompt:
    # Identity
    version: str                      # Semver for A/B tracking
    prompt_id: str                    # UUID for telemetry linkage

    # VCL Configuration
    intent_type: str                  # code_generation, debugging, etc.
    active_frames: List[str]          # evidential, aspectual, etc.
    verix_strictness: str             # RELAXED, MODERATE, STRICT
    compression_level: str            # L0, L1, L2

    # Content
    core_verix: str                   # [illocution|affect] statement [ground] [conf]
    constraints: List[str]            # Domain constraints
    success_criteria: List[str]       # How to judge success

    # Optimization hints
    grounding_required: bool = True
    confidence_floor: float = 0.8

    def compile(self) -> str:
        """Compile to executable prompt string."""
        return f"""<!-- VCL v{self.version} | {self.prompt_id} -->
[Context: {self.intent_type}]
[Frames: {', '.join(self.active_frames)}]
[Strictness: {self.verix_strictness}]

{self.core_verix}

[Constraints: {', '.join(self.constraints)}]
[Success: {', '.join(self.success_criteria)}]
[Output: {self.compression_level}]
"""

    def hash(self) -> str:
        """Content hash for dedup and A/B tracking."""
        import hashlib
        content = f"{self.intent_type}:{self.core_verix}:{':'.join(self.constraints)}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]
```

## Pipeline Integration Example

```python
# Daily content pipeline with VCL prompts
class ContentPipeline:
    def __init__(self):
        self.harness = create_rmis_harness()
        self.harness.start_loop("PIPELINE_CONTENT", "content-generation")

    def run_step(self, step_name: str, description: str, agent_type: str):
        # Get VCL config for this step
        vcl_config = self.get_step_config(step_name)

        # Compile prompt
        prompt = VCLPrompt(
            version=vcl_config["version"],
            prompt_id=str(uuid.uuid4()),
            intent_type=vcl_config["intent"],
            active_frames=vcl_config["frames"],
            verix_strictness=vcl_config["strictness"],
            compression_level="L2",
            core_verix=vcl_config["verix_template"].format(task=description),
            constraints=vcl_config["constraints"],
            success_criteria=vcl_config["success"],
        )

        # Execute with telemetry
        start = time.time()
        result = Task(step_name, prompt.compile(), agent_type)
        latency = (time.time() - start) * 1000

        # Capture
        self.harness.on_eval_complete(
            loop="PIPELINE_CONTENT",
            skill=agent_type,
            task_id=prompt.prompt_id,
            iteration=self.step_count,
            passed=result.success,
            output=result.output,
            metrics={
                "vcl_version": prompt.version,
                "prompt_hash": prompt.hash(),
                "latency_ms": latency,
            }
        )

        return result
```

## Data Flow Summary

```
+------------------+     +------------------+     +------------------+
| VCL Prompt       |     | Task Execution   |     | Telemetry        |
| Compilation      | --> | (Agent runs)     | --> | Capture          |
+------------------+     +------------------+     +------------------+
        ^                                                 |
        |                                                 v
        |                                     +------------------+
        |                                     | Language         |
        |                                     | Evolution        |
        |                                     +------------------+
        |                                                 |
        |                                                 v
        |                                     +------------------+
        |                                     | Pattern          |
        |                                     | Analysis         |
        |                                     +------------------+
        |                                                 |
        +<------------------------------------------------+
              Improved VCL configs for next iteration
```

## Next Steps

1. **Phase 1 (Now)**: Complete RMIS baseline with telemetry harness
2. **Phase 2**: Implement VCLPrompt class
3. **Phase 3**: Create pre-task hook for VCL compilation
4. **Phase 4**: Integrate with agent-selector for VCL config recommendations
5. **Phase 5**: Deploy to daily pipelines with A/B testing
