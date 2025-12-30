"""
Hooks integration for cognitive architecture.

Provides hooks that integrate with Claude Code's hook system for:
- Automatic mode selection on task start
- VERIX validation on response completion
- Frame compliance checking
"""

import os
import sys
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modes.selector import select_mode, TaskContext
from modes.library import get_mode, BUILTIN_MODES
from core.verilingua import FrameRegistry, aggregate_frame_score
from core.config import FullConfig, FrameworkConfig


def on_task_start(task_description: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Hook called when a new task starts.

    Auto-selects appropriate mode based on task description.

    Args:
        task_description: Description of the task
        metadata: Optional metadata (domain hints, constraints, etc.)

    Returns:
        Dict with selected mode and configuration
    """
    # Extract hints from metadata
    domain = None
    constraints = []

    if metadata:
        domain = metadata.get("domain")
        constraints = metadata.get("constraints", [])

    # Select mode
    mode = select_mode(task_description, domain=domain)

    return {
        "hook": "on_task_start",
        "mode_selected": mode.name,
        "mode_type": mode.mode_type.value,
        "config": {
            "framework": {
                "evidential": mode.config.framework.evidential,
                "aspectual": mode.config.framework.aspectual,
                "morphological": mode.config.framework.morphological,
                "compositional": mode.config.framework.compositional,
                "honorific": mode.config.framework.honorific,
                "classifier": mode.config.framework.classifier,
                "spatial": mode.config.framework.spatial,
            },
            "prompt": {
                "verix_strictness": mode.config.prompt.verix_strictness.value,
                "compression_level": mode.config.prompt.compression_level.value,
            },
        },
    }


def on_response_complete(
    response: str,
    mode_name: str = "balanced",
) -> Dict[str, Any]:
    """
    Hook called when response generation completes.

    Validates VERIX compliance and frame adherence.

    Args:
        response: The generated response
        mode_name: Name of the mode used

    Returns:
        Dict with validation results
    """
    mode = get_mode(mode_name)
    if not mode:
        mode = BUILTIN_MODES["balanced"]

    # Score frame compliance
    frame_score = aggregate_frame_score(response, mode.config.framework)

    # Check VERIX markers
    verix_markers = {
        "has_ground": "[ground:" in response.lower() or "ground:" in response.lower(),
        "has_confidence": "[conf:" in response.lower() or "conf:" in response.lower(),
        "has_illocution": any(m in response.lower() for m in ["[assert", "[query", "[propose"]),
    }

    # Calculate compliance score
    verix_score = sum(verix_markers.values()) / len(verix_markers)

    return {
        "hook": "on_response_complete",
        "frame_score": frame_score,
        "verix_score": verix_score,
        "verix_markers": verix_markers,
        "compliant": frame_score >= 0.5 and verix_score >= 0.3,
    }


def on_mode_switch(
    from_mode: str,
    to_mode: str,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Hook called when mode switches.

    Logs mode transitions for analysis.

    Args:
        from_mode: Previous mode name
        to_mode: New mode name
        reason: Optional reason for switch

    Returns:
        Dict with switch details
    """
    from_mode_obj = get_mode(from_mode)
    to_mode_obj = get_mode(to_mode)

    return {
        "hook": "on_mode_switch",
        "from_mode": from_mode,
        "to_mode": to_mode,
        "reason": reason,
        "from_type": from_mode_obj.mode_type.value if from_mode_obj else None,
        "to_type": to_mode_obj.mode_type.value if to_mode_obj else None,
    }


# Hook registry for external integration
HOOKS = {
    "on_task_start": on_task_start,
    "on_response_complete": on_response_complete,
    "on_mode_switch": on_mode_switch,
}


def get_hook(name: str):
    """Get hook function by name."""
    return HOOKS.get(name)


def list_hooks():
    """List all available hooks."""
    return list(HOOKS.keys())
