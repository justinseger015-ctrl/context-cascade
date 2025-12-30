"""
/optimize command - Run GlobalMOO optimization.

Usage:
    /optimize                    - Show optimization status
    /optimize start              - Start new optimization run
    /optimize suggest <targets>  - Get suggestions for targets
    /optimize report             - Get optimization report
    /optimize phase <A|B|C>      - Run specific cascade phase
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.globalmoo_client import (
    GlobalMOOClient,
    OptimizationOutcome,
    ParetoPoint,
)
from optimization.cascade import ThreeMOOCascade, CascadePhase, CascadeResult
from optimization.distill_modes import ModeDistiller
from core.config import FullConfig, VectorCodec


def format_cascade_status(cascade: ThreeMOOCascade) -> str:
    """Format cascade status."""
    phase_names = {
        CascadePhase.PHASE_A: "A (Framework Structure)",
        CascadePhase.PHASE_B: "B (Edge Discovery)",
        CascadePhase.PHASE_C: "C (Production Frontier)",
    }

    # Get state from cascade (may be None if not started)
    state = getattr(cascade, '_state', None)
    current_phase = state.current_phase if state else None
    iteration_count = state.total_iterations if state else 0

    # Get pareto points from MOO client
    pareto_points = []
    if hasattr(cascade, 'moo') and cascade.moo:
        try:
            pareto_points = cascade.moo.get_pareto_frontier("cognitive-arch")
        except Exception:
            pass

    lines = [
        "Three-MOO Cascade Status:",
        f"  Current Phase: {phase_names.get(current_phase, 'Not started')}",
        f"  Iterations: {iteration_count}",
        f"  Pareto Points: {len(pareto_points)}",
        "",
        "Phase Objectives:",
        "  A: Optimize frame selection + VERIX strictness",
        "  B: Discover edge cases + expand config space",
        "  C: Refine Pareto frontier + distill modes",
    ]
    return "\n".join(lines)


def format_suggestions(suggestions: List[List[float]]) -> str:
    """Format optimization suggestions."""
    lines = ["Optimization Suggestions:", ""]

    for i, vec in enumerate(suggestions, 1):
        config = VectorCodec.decode(vec)
        frames_on = sum([
            config.framework.evidential,
            config.framework.aspectual,
            config.framework.morphological,
            config.framework.compositional,
            config.framework.honorific,
            config.framework.classifier,
            config.framework.spatial,
        ])
        lines.append(f"  {i}. Frames: {frames_on}/7, VERIX: {config.prompt.verix_strictness.value}")
        lines.append(f"     Compression: {config.prompt.compression_level.value}")

    return "\n".join(lines)


def format_pareto_points(points: List[ParetoPoint]) -> str:
    """Format Pareto points."""
    if not points:
        return "No Pareto points yet. Run /optimize start to begin."

    lines = ["Pareto Frontier Points:", ""]

    for i, point in enumerate(points[:10], 1):  # Show top 10
        o = point.outcomes
        lines.append(
            f"  {i}. acc={o.get('task_accuracy', 0):.2f} "
            f"eff={o.get('token_efficiency', 0):.2f} "
            f"rob={o.get('edge_robustness', 0):.2f} "
            f"epi={o.get('epistemic_consistency', 0):.2f}"
        )

    if len(points) > 10:
        lines.append(f"  ... and {len(points) - 10} more")

    return "\n".join(lines)


def optimize_command(
    action: Optional[str] = None,
    targets: Optional[Dict[str, float]] = None,
    phase: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute /optimize command.

    Args:
        action: Command action (start, suggest, report, phase)
        targets: Target outcomes for inverse suggestion
        phase: Specific phase to run (A, B, C)

    Returns:
        Command result with optimization data
    """
    result = {
        "command": "/optimize",
        "success": True,
        "output": "",
        "data": None,
    }

    # Initialize cascade (uses mock mode by default)
    cascade = ThreeMOOCascade()

    # Helper to get pareto points
    def get_pareto_points():
        try:
            return cascade.moo.get_pareto_frontier("cognitive-arch")
        except Exception:
            return []

    # Default: show status
    if action is None:
        state = getattr(cascade, '_state', None)
        result["output"] = format_cascade_status(cascade)
        result["data"] = {
            "phase": state.current_phase.value if state else None,
            "iterations": state.total_iterations if state else 0,
            "pareto_count": len(get_pareto_points()),
        }
        return result

    # Start: begin optimization run
    if action == "start":
        lines = [
            "Starting Three-MOO Cascade Optimization...",
            "",
            "Phase A: Framework Structure",
            "  - Optimizing frame selection",
            "  - Tuning VERIX strictness",
            "  - Establishing baseline metrics",
        ]

        # Run a few iterations (mock mode)
        cascade_results = cascade.run(max_iterations_per_phase=3)
        pareto_points = get_pareto_points()

        lines.append("")
        lines.append(f"Completed {len(cascade_results)} phases")
        lines.append(f"Pareto points found: {len(pareto_points)}")

        if pareto_points:
            lines.append("")
            lines.append("Best configuration:")
            best = max(pareto_points,
                       key=lambda p: p.outcomes.get("task_accuracy", 0))
            lines.append(f"  Accuracy: {best.outcomes.get('task_accuracy', 0):.3f}")
            lines.append(f"  Efficiency: {best.outcomes.get('token_efficiency', 0):.3f}")

        result["output"] = "\n".join(lines)
        result["data"] = {
            "iterations": len(cascade_results),
            "pareto_count": len(pareto_points),
        }
        return result

    # Suggest: get inverse suggestions
    if action == "suggest":
        if not targets:
            targets = {
                "task_accuracy": 0.85,
                "token_efficiency": 0.8,
                "edge_robustness": 0.75,
                "epistemic_consistency": 0.9,
            }

        # Use mock mode for suggestions
        client = GlobalMOOClient(use_mock=True)
        suggestions = client.suggest_inverse(
            project_id="cognitive-arch",
            target_outcomes=targets,
            num_suggestions=5,
        )

        result["output"] = format_suggestions(suggestions)
        result["data"] = {"suggestions": suggestions, "targets": targets}
        return result

    # Report: get optimization report
    if action == "report":
        pareto_points = get_pareto_points()
        state = getattr(cascade, '_state', None)
        lines = [
            "Optimization Report",
            "=" * 40,
            "",
            format_cascade_status(cascade),
            "",
            format_pareto_points(pareto_points),
        ]

        result["output"] = "\n".join(lines)
        result["data"] = {
            "phase": state.current_phase.value if state else None,
            "pareto_points": [p.to_dict() for p in pareto_points],
        }
        return result

    # Phase: run specific phase
    if action == "phase":
        phase_map = {
            "A": CascadePhase.PHASE_A,
            "B": CascadePhase.PHASE_B,
            "C": CascadePhase.PHASE_C,
        }

        if not phase or phase.upper() not in phase_map:
            result["success"] = False
            result["output"] = "Error: Specify phase A, B, or C. Usage: /optimize phase A"
            return result

        target_phase = phase_map[phase.upper()]

        lines = [
            f"Running Phase {phase.upper()}...",
            "",
        ]

        # Phase-specific descriptions
        phase_desc = {
            "A": "Optimizing framework structure (frame selection, VERIX strictness)",
            "B": "Discovering edge cases (adversarial corpus, failure modes)",
            "C": "Refining production frontier (Pareto points, named modes)",
        }
        lines.append(phase_desc[phase.upper()])

        # Run phase (full cascade for now - phases are sequential)
        cascade_results = cascade.run(max_iterations_per_phase=5)
        pareto_points = get_pareto_points()

        lines.append("")
        lines.append(f"Phase {phase.upper()} complete")
        lines.append(f"Phases completed: {len(cascade_results)}")
        lines.append(f"Pareto points: {len(pareto_points)}")

        result["output"] = "\n".join(lines)
        result["data"] = {
            "phase": phase.upper(),
            "iterations": len(cascade_results),
            "pareto_count": len(pareto_points),
        }
        return result

    # Unknown action
    result["success"] = False
    result["output"] = f"""
Unknown action: '{action}'

/optimize - Run GlobalMOO optimization

Usage:
  /optimize               - Show status
  /optimize start         - Start optimization run
  /optimize suggest       - Get config suggestions
  /optimize report        - Get optimization report
  /optimize phase <A|B|C> - Run specific cascade phase
"""
    return result


if __name__ == "__main__":
    # Demo
    print("=== /optimize ===")
    r = optimize_command()
    print(r["output"])

    print("\n=== /optimize start ===")
    r = optimize_command("start")
    print(r["output"])

    print("\n=== /optimize suggest ===")
    r = optimize_command("suggest")
    print(r["output"])

    print("\n=== /optimize report ===")
    r = optimize_command("report")
    print(r["output"])
