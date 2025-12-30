"""
Slash commands for VERILINGUA x VERIX cognitive architecture.

Available commands:
- /mode: Select or list cognitive modes
- /eval: Evaluate task against metrics
- /optimize: Run GlobalMOO optimization
- /pareto: Display Pareto frontier
- /frame: Configure VERILINGUA frames
- /verix: Apply VERIX epistemic notation
"""

from .mode import mode_command
from .eval import eval_command
from .optimize import optimize_command
from .pareto import pareto_command
from .frame import frame_command
from .verix import verix_command

__all__ = [
    "mode_command",
    "eval_command",
    "optimize_command",
    "pareto_command",
    "frame_command",
    "verix_command",
]
