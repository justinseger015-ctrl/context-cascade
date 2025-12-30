"""
VERILINGUA x VERIX x DSPy x GlobalMOO Cognitive Architecture

A self-improving prompt optimization system that combines:
- VERILINGUA: 7 cognitive frames from natural language distinctions
- VERIX: Epistemic notation for claim validation
- DSPy: Programmatic prompt optimization
- GlobalMOO: Multi-objective Pareto optimization

Thin Waist Contracts (NEVER CHANGE):
- PromptBuilder.build(task, task_type) -> (system_prompt, user_prompt)
- evaluate(config_vector) -> outcomes_vector
"""

__version__ = "0.1.0"
__author__ = "Context Cascade Team"

from .core.config import FullConfig, FrameworkConfig, PromptConfig, VectorCodec
from .core.prompt_builder import PromptBuilder

__all__ = [
    "FullConfig",
    "FrameworkConfig",
    "PromptConfig",
    "VectorCodec",
    "PromptBuilder",
]
