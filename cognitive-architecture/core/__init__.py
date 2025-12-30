"""
Core module for cognitive architecture.

Contains:
- config: Configuration dataclasses and VectorCodec
- verix: VERIX epistemic notation parser and validator
- verilingua: 7 cognitive frames from natural language distinctions
- prompt_builder: THIN WAIST contract for prompt construction
- runtime: Claude client wrapper
"""

from .config import FullConfig, FrameworkConfig, PromptConfig, VectorCodec
from .verix import VerixClaim, VerixParser, VerixValidator
from .verilingua import CognitiveFrame, FrameRegistry

__all__ = [
    "FullConfig",
    "FrameworkConfig",
    "PromptConfig",
    "VectorCodec",
    "VerixClaim",
    "VerixParser",
    "VerixValidator",
    "CognitiveFrame",
    "FrameRegistry",
]
