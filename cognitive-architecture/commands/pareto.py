"""
/pareto command - Display and explore Pareto frontier.

Usage:
    /pareto                    - Display current Pareto frontier
    /pareto filter <metric>    - Filter by metric dominance
    /pareto export             - Export frontier as JSON
    /pareto distill            - Distill into named modes
    /pareto visualize          - ASCII visualization
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from optimization.globalmoo_client import ParetoPoint
from optimization.distill_modes import ModeDistiller, NamedMode, ModeCategory
from core.config import VectorCodec


def pareto_point_to_dict(p: ParetoPoint) -> dict:
    """Convert ParetoPoint to dict."""
    return {
        "config_vector": p.config_vector,
        "outcomes": p.outcomes,
        "dominance_rank": p.dominance_rank,
        "crowding_distance": p.crowding_distance,
    }


def create_sample_pareto() -> List[ParetoPoint]:
    """Create sample Pareto points for demo."""
    return [
        ParetoPoint(
            config_vector=[1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 0, 0, 0],
            outcomes={
                "task_accuracy": 0.95,
                "token_efficiency": 0.55,
                "edge_robustness": 0.90,
                "epistemic_consistency": 0.98,
            },
        ),
        ParetoPoint(
            config_vector=[1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            outcomes={
                "task_accuracy": 0.82,
                "token_efficiency": 0.80,
                "edge_robustness": 0.70,
                "epistemic_consistency": 0.85,
            },
        ),
        ParetoPoint(
            config_vector=[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            outcomes={
                "task_accuracy": 0.72,
                "token_efficiency": 0.95,
                "edge_robustness": 0.60,
                "epistemic_consistency": 0.70,
            },
        ),
        ParetoPoint(
            config_vector=[1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
            outcomes={
                "task_accuracy": 0.85,
                "token_efficiency": 0.72,
                "edge_robustness": 0.92,
                "epistemic_consistency": 0.88,
            },
        ),
        ParetoPoint(
            config_vector=[0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
            outcomes={
                "task_accuracy": 0.68,
                "token_efficiency": 0.98,
                "edge_robustness": 0.55,
                "epistemic_consistency": 0.50,
            },
        ),
    ]


def format_pareto_table(points: List[ParetoPoint]) -> str:
    """Format Pareto points as table."""
    lines = [
        "Pareto Frontier",
        "-" * 70,
        "  #  | Accuracy | Efficiency | Robustness | Epistemic | Frames",
        "-" * 70,
    ]

    for i, point in enumerate(points, 1):
        o = point.outcomes
        config = VectorCodec.decode(point.config_vector)
        frames = sum([
            config.framework.evidential,
            config.framework.aspectual,
            config.framework.morphological,
            config.framework.compositional,
            config.framework.honorific,
            config.framework.classifier,
            config.framework.spatial,
        ])
        lines.append(
            f"  {i:2} |   {o.get('task_accuracy', 0):.2f}   |"
            f"    {o.get('token_efficiency', 0):.2f}    |"
            f"    {o.get('edge_robustness', 0):.2f}    |"
            f"   {o.get('epistemic_consistency', 0):.2f}   |"
            f"   {frames}/7"
        )

    lines.append("-" * 70)
    return "\n".join(lines)


def format_ascii_visualization(points: List[ParetoPoint]) -> str:
    """Create ASCII scatter plot of accuracy vs efficiency."""
    lines = [
        "Pareto Frontier: Accuracy vs Efficiency",
        "",
        "Accuracy",
        "1.0 |",
    ]

    # Create 10x20 grid
    grid = [[" " for _ in range(21)] for _ in range(11)]

    for i, point in enumerate(points):
        acc = point.outcomes.get("task_accuracy", 0)
        eff = point.outcomes.get("token_efficiency", 0)
        row = 10 - int(acc * 10)
        col = int(eff * 20)
        row = max(0, min(10, row))
        col = max(0, min(20, col))
        grid[row][col] = str(i + 1)

    for r in range(11):
        y_val = 1.0 - r * 0.1
        row_str = "".join(grid[r])
        if r == 10:
            lines.append(f"0.0 +{'='*21}")
        else:
            lines.append(f"{y_val:.1f} |{row_str}|")

    lines.append("    0.0" + " " * 8 + "0.5" + " " * 8 + "1.0")
    lines.append("                    Efficiency")
    lines.append("")
    lines.append("Points: " + ", ".join(f"{i+1}" for i in range(len(points))))

    return "\n".join(lines)


def pareto_command(
    action: Optional[str] = None,
    metric: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute /pareto command.

    Args:
        action: Command action (filter, export, distill, visualize)
        metric: Metric to filter by

    Returns:
        Command result with Pareto data
    """
    result = {
        "command": "/pareto",
        "success": True,
        "output": "",
        "data": None,
    }

    # Get current Pareto points (sample for demo)
    points = create_sample_pareto()

    # Default: show Pareto frontier
    if action is None:
        result["output"] = format_pareto_table(points)
        result["data"] = {
            "count": len(points),
            "points": [pareto_point_to_dict(p) for p in points],
        }
        return result

    # Filter: filter by metric dominance
    if action == "filter":
        valid_metrics = ["task_accuracy", "token_efficiency", "edge_robustness", "epistemic_consistency"]

        if not metric or metric not in valid_metrics:
            result["success"] = False
            result["output"] = f"Error: Specify metric: {', '.join(valid_metrics)}"
            return result

        # Sort by metric
        sorted_points = sorted(
            points,
            key=lambda p: p.outcomes.get(metric, 0),
            reverse=True,
        )

        lines = [f"Pareto Frontier sorted by {metric}:", ""]
        for i, point in enumerate(sorted_points, 1):
            o = point.outcomes
            lines.append(f"  {i}. {metric}: {o.get(metric, 0):.3f}")

        result["output"] = "\n".join(lines)
        result["data"] = {
            "metric": metric,
            "sorted_points": [pareto_point_to_dict(p) for p in sorted_points],
        }
        return result

    # Export: export as JSON
    if action == "export":
        export_data = {
            "pareto_frontier": [pareto_point_to_dict(p) for p in points],
            "count": len(points),
            "metrics": ["task_accuracy", "token_efficiency", "edge_robustness", "epistemic_consistency"],
        }

        result["output"] = json.dumps(export_data, indent=2)
        result["data"] = export_data
        return result

    # Distill: distill into named modes
    if action == "distill":
        distiller = ModeDistiller()
        modes = distiller.distill(points, include_defaults=True)

        lines = ["Distilled Modes:", ""]
        for mode in modes:
            exp = mode.expected_outcomes
            lines.append(f"  {mode.name} ({mode.category.value})")
            lines.append(f"    acc={exp.get('task_accuracy', 0):.2f} "
                         f"eff={exp.get('token_efficiency', 0):.2f} "
                         f"rob={exp.get('edge_robustness', 0):.2f}")

        result["output"] = "\n".join(lines)
        result["data"] = {"modes": [m.to_dict() for m in modes]}
        return result

    # Visualize: ASCII visualization
    if action == "visualize":
        result["output"] = format_ascii_visualization(points)
        result["data"] = {"count": len(points)}
        return result

    # Unknown action
    result["success"] = False
    result["output"] = f"""
Unknown action: '{action}'

/pareto - Explore Pareto frontier

Usage:
  /pareto                    - Display frontier
  /pareto filter <metric>    - Filter by metric
  /pareto export             - Export as JSON
  /pareto distill            - Distill into modes
  /pareto visualize          - ASCII visualization
"""
    return result


if __name__ == "__main__":
    # Demo
    print("=== /pareto ===")
    r = pareto_command()
    print(r["output"])

    print("\n=== /pareto filter task_accuracy ===")
    r = pareto_command("filter", "task_accuracy")
    print(r["output"])

    print("\n=== /pareto visualize ===")
    r = pareto_command("visualize")
    print(r["output"])

    print("\n=== /pareto distill ===")
    r = pareto_command("distill")
    print(r["output"])
