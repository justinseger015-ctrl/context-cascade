"""
/frame command - Configure VERILINGUA cognitive frames.

Usage:
    /frame                    - List all frames
    /frame <name>             - Show frame details
    /frame enable <names>     - Enable frames
    /frame disable <names>    - Disable frames
    /frame preset <name>      - Apply frame preset
"""

import os
import sys
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verilingua import FrameRegistry


@dataclass
class Frame:
    """Simple frame representation for command output."""
    name: str
    source_language: str
    cognitive_force: str
    markers: List[str]
    examples: List[str]
    description: str


def _build_frame_info() -> Dict[str, Frame]:
    """Build frame info from FrameRegistry."""
    frame_info = {}
    for name, frame in FrameRegistry.get_all().items():
        markers = frame.compliance_markers() if hasattr(frame, 'compliance_markers') else []
        examples = []
        # Extract examples from activation instruction
        instruction = frame.activation_instruction() if hasattr(frame, 'activation_instruction') else ""
        # Find lines that look like examples (start with quotes or contain markers)
        for line in instruction.split('\n'):
            if line.strip().startswith('"') or any(m in line for m in markers):
                examples.append(line.strip())

        frame_info[name] = Frame(
            name=name,
            source_language=frame.linguistic_source if hasattr(frame, 'linguistic_source') else "Unknown",
            cognitive_force=frame.cognitive_force if hasattr(frame, 'cognitive_force') else "",
            markers=markers,
            examples=examples[:3],  # First 3 examples
            description=f"Cognitive frame from {frame.linguistic_source}" if hasattr(frame, 'linguistic_source') else "",
        )
    return frame_info


FRAME_REGISTRY = _build_frame_info()


FRAME_PRESETS = {
    "all": ["evidential", "aspectual", "morphological", "compositional",
            "honorific", "classifier", "spatial"],
    "minimal": [],
    "research": ["evidential", "aspectual"],
    "coding": ["compositional", "spatial"],
    "documentation": ["honorific", "compositional"],
    "analysis": ["evidential", "aspectual", "morphological"],
    "security": ["evidential", "spatial", "classifier"],
}


def format_frame_list() -> str:
    """Format list of all frames."""
    lines = [
        "VERILINGUA Cognitive Frames",
        "=" * 50,
        "",
    ]

    for name, frame in FRAME_REGISTRY.items():
        lines.append(f"{name.upper()}")
        lines.append(f"  Source: {frame.source_language}")
        lines.append(f"  Force: {frame.cognitive_force}")
        lines.append(f"  Markers: {', '.join(frame.markers[:3])}...")
        lines.append("")

    lines.append("Presets:")
    for preset, frames in FRAME_PRESETS.items():
        lines.append(f"  {preset}: {', '.join(frames) if frames else '(none)'}")

    return "\n".join(lines)


def format_frame_detail(frame: Frame) -> str:
    """Format detailed frame info."""
    lines = [
        f"Frame: {frame.name.upper()}",
        "=" * 40,
        f"Source Language: {frame.source_language}",
        f"Cognitive Force: {frame.cognitive_force}",
        "",
        "Markers:",
    ]

    for marker in frame.markers:
        lines.append(f"  - {marker}")

    lines.append("")
    lines.append("Examples:")
    for example in frame.examples:
        lines.append(f"  {example}")

    lines.append("")
    lines.append("Description:")
    lines.append(f"  {frame.description}")

    return "\n".join(lines)


def frame_command(
    action: Optional[str] = None,
    target: Optional[str] = None,
    frames: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Execute /frame command.

    Args:
        action: Command action (enable, disable, preset, or frame name)
        target: Target for action (preset name or frame list)
        frames: List of frames to enable/disable

    Returns:
        Command result with frame configuration
    """
    result = {
        "command": "/frame",
        "success": True,
        "output": "",
        "data": None,
    }

    # Default: list all frames
    if action is None:
        result["output"] = format_frame_list()
        result["data"] = {
            "frames": list(FRAME_REGISTRY.keys()),
            "presets": FRAME_PRESETS,
        }
        return result

    # Check if action is a frame name
    if action.lower() in FRAME_REGISTRY:
        frame = FRAME_REGISTRY[action.lower()]
        result["output"] = format_frame_detail(frame)
        result["data"] = {
            "frame": {
                "name": frame.name,
                "source_language": frame.source_language,
                "cognitive_force": frame.cognitive_force,
                "markers": frame.markers,
                "examples": frame.examples,
            }
        }
        return result

    # Enable: enable frames
    if action == "enable":
        if not target:
            result["success"] = False
            result["output"] = "Error: Specify frames to enable. Usage: /frame enable evidential,aspectual"
            return result

        frame_list = [f.strip().lower() for f in target.split(",")]
        valid_frames = [f for f in frame_list if f in FRAME_REGISTRY]
        invalid_frames = [f for f in frame_list if f not in FRAME_REGISTRY]

        lines = ["Frame Configuration Updated:", ""]
        if valid_frames:
            lines.append(f"Enabled: {', '.join(valid_frames)}")
        if invalid_frames:
            lines.append(f"Unknown frames (ignored): {', '.join(invalid_frames)}")

        result["output"] = "\n".join(lines)
        result["data"] = {"enabled": valid_frames, "invalid": invalid_frames}
        return result

    # Disable: disable frames
    if action == "disable":
        if not target:
            result["success"] = False
            result["output"] = "Error: Specify frames to disable. Usage: /frame disable morphological"
            return result

        frame_list = [f.strip().lower() for f in target.split(",")]
        valid_frames = [f for f in frame_list if f in FRAME_REGISTRY]

        lines = ["Frame Configuration Updated:", ""]
        if valid_frames:
            lines.append(f"Disabled: {', '.join(valid_frames)}")

        result["output"] = "\n".join(lines)
        result["data"] = {"disabled": valid_frames}
        return result

    # Preset: apply frame preset
    if action == "preset":
        if not target or target.lower() not in FRAME_PRESETS:
            available = ", ".join(FRAME_PRESETS.keys())
            result["success"] = False
            result["output"] = f"Error: Unknown preset. Available: {available}"
            return result

        preset_name = target.lower()
        preset_frames = FRAME_PRESETS[preset_name]

        lines = [
            f"Applied preset: {preset_name}",
            "",
            f"Active frames: {', '.join(preset_frames) if preset_frames else '(none)'}",
        ]

        result["output"] = "\n".join(lines)
        result["data"] = {"preset": preset_name, "frames": preset_frames}
        return result

    # Unknown action
    result["success"] = False
    result["output"] = f"""
Unknown action: '{action}'

/frame - Configure VERILINGUA cognitive frames

Usage:
  /frame                    - List all frames
  /frame <name>             - Show frame details
  /frame enable <names>     - Enable frames (comma-separated)
  /frame disable <names>    - Disable frames
  /frame preset <name>      - Apply preset (all, minimal, research, etc.)

Available frames: {', '.join(FRAME_REGISTRY.keys())}
"""
    return result


if __name__ == "__main__":
    # Demo
    print("=== /frame ===")
    r = frame_command()
    print(r["output"])

    print("\n=== /frame evidential ===")
    r = frame_command("evidential")
    print(r["output"])

    print("\n=== /frame preset research ===")
    r = frame_command("preset", "research")
    print(r["output"])

    print("\n=== /frame enable aspectual,classifier ===")
    r = frame_command("enable", "aspectual,classifier")
    print(r["output"])
