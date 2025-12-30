"""
Integration module for Cognitive Architecture + Meta-Loop + Ralph Wiggum.

This module implements the UnifiedBridge that connects:
- Cognitive Architecture (frames, VERIX, modes, MOO)
- Meta-Loop (auditors, eval harness, improvement pipeline)
- Ralph Wiggum (iteration motor)

The integration respects these INVARIANTS:
1. Thin waist contract is sacred (PromptBuilder.build signature)
2. Evidence plane is constitutionally protected (frozen eval harness)
3. Ralph is executor, not governor (doesn't decide goodness)
4. Bridge is the only cross-plane mutation gate
5. Event log is append-only and replayable
6. Timescale isolation (micro < meso < macro)
"""

from .unified_bridge import (
    UnifiedBridge,
    BridgeInput,
    BridgeOutput,
    DecisionIntent,
    UnifiedEvent,
)

__all__ = [
    "UnifiedBridge",
    "BridgeInput",
    "BridgeOutput",
    "DecisionIntent",
    "UnifiedEvent",
]
