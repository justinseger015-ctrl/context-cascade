"""
/mode command - Select or configure cognitive modes.

Usage:
    /mode                    - List available modes
    /mode <name>             - Select mode by name
    /mode auto "<task>"      - Auto-select based on task
    /mode info <name>        - Show mode details
    /mode recommend "<task>" - Get top-3 recommendations
"""

import os
import sys
from typing import List, Optional, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modes.library import (
    Mode,
    ModeLibrary,
    get_mode,
    list_modes,
    get_mode_config,
    BUILTIN_MODES,
)
from modes.selector import (
    ModeSelector,
    TaskContext,
    select_mode,
    recommend_modes,
    ModeRecommendation,
)


def format_mode_summary(mode: Mode) -> str:
    """Format mode for display."""
    lines = [
        f"  {mode.name} ({mode.mode_type.value})",
        f"    {mode.description}",
    ]
    if mode.tags:
        lines.append(f"    Tags: {', '.join(mode.tags)}")
    return "\n".join(lines)


def format_mode_detail(mode: Mode) -> str:
    """Format detailed mode info."""
    lines = [
        f"Mode: {mode.name}",
        f"Type: {mode.mode_type.value}",
        f"Description: {mode.description}",
        "",
        "Configuration:",
        "  Framework:",
    ]

    # Framework settings
    fw = mode.config.framework
    for field in ["evidential", "aspectual", "morphological", "compositional",
                  "honorific", "classifier", "spatial"]:
        value = getattr(fw, field)
        lines.append(f"    {field}: {value}")

    lines.append("  Prompt:")
    pr = mode.config.prompt
    lines.append(f"    verix_strictness: {pr.verix_strictness.value}")
    lines.append(f"    compression_level: {pr.compression_level.value}")
    lines.append(f"    require_ground: {pr.require_ground}")
    lines.append(f"    require_confidence: {pr.require_confidence}")

    if mode.use_cases:
        lines.append("")
        lines.append("Use Cases:")
        for use_case in mode.use_cases:
            lines.append(f"  - {use_case}")

    if mode.expected_metrics:
        lines.append("")
        lines.append("Expected Metrics:")
        for metric, value in mode.expected_metrics.items():
            lines.append(f"  {metric}: {value:.2f}")

    return "\n".join(lines)


def format_recommendation(rec: ModeRecommendation) -> str:
    """Format recommendation for display."""
    lines = [
        f"  {rec.mode.name} (score: {rec.score:.2f})",
    ]
    for reason in rec.reasons:
        lines.append(f"    + {reason}")
    return "\n".join(lines)


def mode_command(
    action: Optional[str] = None,
    target: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute /mode command.

    Args:
        action: Command action (list, select, auto, info, recommend)
        target: Target for action (mode name or task description)

    Returns:
        Command result with mode information
    """
    result = {
        "command": "/mode",
        "success": True,
        "output": "",
        "data": None,
    }

    # Default: list modes
    if action is None:
        mode_names = list_modes()
        lines = ["Available Cognitive Modes:", ""]
        for name in mode_names:
            mode = get_mode(name)
            if mode:
                lines.append(format_mode_summary(mode))
        lines.append("")
        lines.append("Usage:")
        lines.append('  /mode <name>             - Select mode')
        lines.append('  /mode auto "<task>"      - Auto-select')
        lines.append('  /mode recommend "<task>" - Get recommendations')
        result["output"] = "\n".join(lines)
        result["data"] = {"modes": mode_names}
        return result

    # Info: show mode details
    if action == "info":
        if not target:
            result["success"] = False
            result["output"] = "Error: Mode name required. Usage: /mode info <name>"
            return result

        mode = get_mode(target)
        if not mode:
            result["success"] = False
            result["output"] = f"Error: Mode '{target}' not found"
            return result

        result["output"] = format_mode_detail(mode)
        result["data"] = {"mode": mode.to_dict()}
        return result

    # Auto: auto-select based on task
    if action == "auto":
        if not target:
            result["success"] = False
            result["output"] = "Error: Task required. Usage: /mode auto \"<task>\""
            return result

        mode = select_mode(target)
        result["output"] = f"Auto-selected mode: {mode.name}\n\n{format_mode_detail(mode)}"
        result["data"] = {"selected": mode.name, "mode": mode.to_dict()}
        return result

    # Recommend: get top-3 recommendations
    if action == "recommend":
        if not target:
            result["success"] = False
            result["output"] = "Error: Task required. Usage: /mode recommend \"<task>\""
            return result

        recs = recommend_modes(target, top_k=3)
        lines = [f"Mode Recommendations for: \"{target}\"", ""]
        for i, rec in enumerate(recs, 1):
            lines.append(f"{i}. {format_recommendation(rec)}")
        result["output"] = "\n".join(lines)
        result["data"] = {"recommendations": [r.to_dict() for r in recs]}
        return result

    # Select: select mode by name
    mode = get_mode(action)
    if mode:
        result["output"] = f"Selected mode: {action}\n\n{format_mode_detail(mode)}"
        result["data"] = {"selected": action, "mode": mode.to_dict()}
        return result

    # Unknown action
    result["success"] = False
    result["output"] = f"Unknown action or mode: '{action}'\nUse /mode to list available modes."
    return result


if __name__ == "__main__":
    import json

    # Demo
    print("=== /mode ===")
    r = mode_command()
    print(r["output"])

    print("\n=== /mode info balanced ===")
    r = mode_command("info", "balanced")
    print(r["output"])

    print("\n=== /mode auto \"security audit\" ===")
    r = mode_command("auto", "security audit for production API")
    print(r["output"])

    print("\n=== /mode recommend \"quick translation\" ===")
    r = mode_command("recommend", "quick translation task")
    print(r["output"])
