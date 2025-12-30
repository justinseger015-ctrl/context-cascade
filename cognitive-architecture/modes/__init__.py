"""
Modes module for cognitive architecture.

Provides named configuration modes and automatic selection
based on task characteristics.

Modes:
- strict: Maximum epistemic consistency
- balanced: Good tradeoff across all objectives
- efficient: Optimized for token efficiency
- robust: Optimized for edge case handling
- minimal: Lightweight with few frames
"""

from .library import (
    Mode,
    ModeLibrary,
    get_mode,
    list_modes,
    get_mode_config,
    BUILTIN_MODES,
)
from .selector import (
    ModeSelector,
    TaskContext,
    select_mode,
    recommend_modes,
)

__all__ = [
    # Library
    "Mode",
    "ModeLibrary",
    "get_mode",
    "list_modes",
    "get_mode_config",
    "BUILTIN_MODES",
    # Selector
    "ModeSelector",
    "TaskContext",
    "select_mode",
    "recommend_modes",
]
