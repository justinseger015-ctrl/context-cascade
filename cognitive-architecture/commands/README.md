# Cognitive Architecture Commands

Slash commands for the VERILINGUA x VERIX x DSPy x GlobalMOO integration.

## Available Commands

| Command | Description |
|---------|-------------|
| `/mode` | Select or configure cognitive modes |
| `/eval` | Evaluate tasks against metrics |
| `/optimize` | Run GlobalMOO optimization |
| `/pareto` | Display and explore Pareto frontier |
| `/frame` | Configure VERILINGUA cognitive frames |
| `/verix` | Apply VERIX epistemic notation |

## /mode - Mode Selection

Select and configure cognitive modes for different task types.

```bash
/mode                    # List available modes
/mode <name>             # Select mode by name
/mode auto "<task>"      # Auto-select based on task
/mode info <name>        # Show mode details
/mode recommend "<task>" # Get top-3 recommendations
```

**Available Modes:**
- `strict` - Maximum epistemic consistency (research, legal, medical)
- `balanced` - Good tradeoff for general use (default)
- `efficient` - Optimized for token efficiency (high-volume APIs)
- `robust` - Edge case handling (security, adversarial)
- `minimal` - Lightweight with no frames (simple Q&A)

## /eval - Evaluation

Evaluate tasks against the 4 cognitive architecture metrics.

```bash
/eval "<task>" "<response>"  # Evaluate response
/eval --corpus <path>        # Evaluate corpus file
/eval --metrics              # Show metric definitions
/eval --graders              # List available graders
```

**Metrics:**
- `task_accuracy` - Correctness (0.0 - 1.0)
- `token_efficiency` - Tokens vs target (0.0 - 1.0)
- `edge_robustness` - Adversarial handling (0.0 - 1.0)
- `epistemic_consistency` - VERIX compliance (0.0 - 1.0)

## /optimize - GlobalMOO Optimization

Run multi-objective optimization using the Three-MOO Cascade.

```bash
/optimize               # Show optimization status
/optimize start         # Start optimization run
/optimize suggest       # Get configuration suggestions
/optimize report        # Get optimization report
/optimize phase <A|B|C> # Run specific cascade phase
```

**Cascade Phases:**
- Phase A: Framework structure optimization
- Phase B: Edge case discovery
- Phase C: Production frontier refinement

## /pareto - Pareto Frontier

Explore the Pareto frontier of optimal configurations.

```bash
/pareto                  # Display frontier
/pareto filter <metric>  # Filter by metric
/pareto export           # Export as JSON
/pareto distill          # Distill into named modes
/pareto visualize        # ASCII visualization
```

## /frame - VERILINGUA Frames

Configure the 7 cognitive frames from linguistic traditions.

```bash
/frame                    # List all frames
/frame <name>             # Show frame details
/frame enable <names>     # Enable frames (comma-separated)
/frame disable <names>    # Disable frames
/frame preset <name>      # Apply preset
```

**Frames:**
- `evidential` - Turkish -mis/-di ("How do you know?")
- `aspectual` - Russian pfv/ipfv ("Complete or ongoing?")
- `morphological` - Arabic trilateral roots (semantic decomposition)
- `compositional` - German compounding (primitives to compounds)
- `honorific` - Japanese keigo (audience calibration)
- `classifier` - Chinese measure words (object comparison)
- `spatial` - Guugu Yimithirr (absolute positioning)

**Presets:**
- `all` - All 7 frames
- `minimal` - No frames
- `research` - evidential + aspectual
- `coding` - compositional + spatial
- `documentation` - honorific + compositional
- `analysis` - evidential + aspectual + morphological
- `security` - evidential + spatial + classifier

## /verix - Epistemic Notation

Apply VERIX notation for epistemic consistency.

```bash
/verix                     # Show VERIX guide
/verix parse "<text>"      # Parse for VERIX elements
/verix validate "<claim>"  # Validate epistemic consistency
/verix annotate "<text>"   # Add VERIX annotations
/verix level <0|1|2>       # Set compression level
```

**VERIX Structure:**
```
STATEMENT := ILLOCUTION + AFFECT + CONTENT + GROUND + CONFIDENCE + STATE
```

**Compression Levels:**
- L0: AI-AI (Emoji shorthand, maximum compression)
- L1: AI+Human (Full annotation, balanced)
- L2: Human (Natural language, lossy)

## Integration

Commands integrate with:
- **modes/library.py** - Mode definitions and registry
- **modes/selector.py** - Automatic mode selection
- **eval/** - Metrics and graders
- **optimization/** - GlobalMOO and DSPy integration
- **core/verilingua.py** - Cognitive frames
- **core/verix.py** - Epistemic notation

## Usage from Python

```python
from commands.mode import mode_command
from commands.eval import eval_command
from commands.optimize import optimize_command

# Select mode
result = mode_command("auto", "security audit for API")
print(result["output"])

# Evaluate response
result = eval_command(
    task="Explain quantum computing",
    response="Quantum computing uses qubits..."
)
print(result["data"]["metrics"])

# Run optimization
result = optimize_command("start")
print(result["output"])
```
