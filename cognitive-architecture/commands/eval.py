"""
/eval command - Evaluate tasks against cognitive architecture metrics.

Usage:
    /eval "<task>" "<response>"      - Evaluate response against task
    /eval --corpus <path>            - Run evaluation on corpus
    /eval --metrics                  - Show metric definitions
    /eval --graders                  - List available graders
"""

import os
import sys
import json
from typing import Optional, Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval.metrics import (
    EvaluationResult,
    MetricCalculator,
    length_normalize,
    format_compliance_penalty,
)
from eval.edge_cases import EdgeCaseType, EdgeCaseDetector
from eval.consistency import ConsistencyChecker


def format_metrics() -> str:
    """Format metric definitions."""
    return """
Evaluation Metrics:

1. task_accuracy (0.0 - 1.0)
   - Measures correctness of response content
   - Graded by deterministic + LLM judge
   - Anti-gaming: Length normalization applied

2. token_efficiency (0.0 - 1.0)
   - Measures tokens used vs target
   - Formula: 1 - abs(actual - target) / max(actual, target)
   - Anti-gaming: Format compliance penalty

3. edge_robustness (0.0 - 1.0)
   - Measures handling of adversarial/edge cases
   - Categories: injection, ambiguous, contradictory, etc.
   - Anti-gaming: No score if edge case not triggered

4. epistemic_consistency (0.0 - 1.0)
   - Measures VERIX compliance
   - Checks: grounding, confidence, consistency
   - Anti-gaming: Requires claim validation
"""


def format_graders() -> str:
    """Format available graders."""
    return """
Available Graders:

Deterministic Graders:
  - FormatGrader: JSON, markdown, code block compliance
  - TokenGrader: Token count efficiency
  - LatencyGrader: Response time measurement
  - RegexGrader: Pattern matching validation
  - VERIXGrader: Epistemic notation compliance
  - VERILINGUAGrader: Cognitive frame usage

LLM Judge Graders:
  - RubricGrader: Multi-criteria rubric evaluation
  - CouncilGrader: 3-model council (Claude + Gemini + Codex)

Edge Case Graders:
  - InjectionGrader: Prompt injection resistance
  - AmbiguityGrader: Ambiguous input handling
  - ContradictionGrader: Contradictory claim handling
"""


def eval_command(
    task: Optional[str] = None,
    response: Optional[str] = None,
    corpus: Optional[str] = None,
    show_metrics: bool = False,
    show_graders: bool = False,
) -> Dict[str, Any]:
    """
    Execute /eval command.

    Args:
        task: Task description to evaluate against
        response: Response to evaluate
        corpus: Path to JSONL corpus file
        show_metrics: Show metric definitions
        show_graders: Show available graders

    Returns:
        Command result with evaluation data
    """
    result = {
        "command": "/eval",
        "success": True,
        "output": "",
        "data": None,
    }

    # Show metrics
    if show_metrics:
        result["output"] = format_metrics()
        return result

    # Show graders
    if show_graders:
        result["output"] = format_graders()
        return result

    # Evaluate corpus
    if corpus:
        try:
            with open(corpus, "r", encoding="utf-8") as f:
                tasks = [json.loads(line) for line in f if line.strip()]

            calculator = MetricCalculator()
            results = []

            for t in tasks:
                task_str = t.get("task", "")
                expected = t.get("expected", "")
                resp = t.get("response", expected)  # Use expected as mock response

                eval_result = calculator.calculate(
                    task=task_str,
                    response=resp,
                    expected=expected,
                    token_count=len(resp.split()),
                )
                results.append({
                    "task_id": t.get("id", "unknown"),
                    "task_accuracy": eval_result.task_accuracy,
                    "token_efficiency": eval_result.token_efficiency,
                    "edge_robustness": eval_result.edge_robustness,
                    "epistemic_consistency": eval_result.epistemic_consistency,
                })

            # Aggregate
            avg = {
                "task_accuracy": sum(r["task_accuracy"] for r in results) / len(results),
                "token_efficiency": sum(r["token_efficiency"] for r in results) / len(results),
                "edge_robustness": sum(r["edge_robustness"] for r in results) / len(results),
                "epistemic_consistency": sum(r["epistemic_consistency"] for r in results) / len(results),
            }

            lines = [
                f"Corpus Evaluation: {corpus}",
                f"Tasks evaluated: {len(results)}",
                "",
                "Aggregate Metrics:",
                f"  task_accuracy: {avg['task_accuracy']:.3f}",
                f"  token_efficiency: {avg['token_efficiency']:.3f}",
                f"  edge_robustness: {avg['edge_robustness']:.3f}",
                f"  epistemic_consistency: {avg['epistemic_consistency']:.3f}",
            ]

            result["output"] = "\n".join(lines)
            result["data"] = {"aggregate": avg, "results": results}
            return result

        except FileNotFoundError:
            result["success"] = False
            result["output"] = f"Error: Corpus file not found: {corpus}"
            return result
        except json.JSONDecodeError as e:
            result["success"] = False
            result["output"] = f"Error: Invalid JSONL in corpus: {e}"
            return result

    # Evaluate single task/response
    if task and response:
        calculator = MetricCalculator()
        edge_detector = EdgeCaseDetector()
        consistency_checker = ConsistencyChecker()

        # Detect edge cases
        edge_types = edge_detector.detect(task)

        # Wrap string task in dict for MetricCalculator
        task_dict = {"id": "manual-eval", "task": task, "task_type": "general"}

        # Calculate metrics
        eval_result = calculator.calculate(
            task=task_dict,
            response=response,
            expected="",  # No expected for manual eval
            token_count=len(response.split()),
            edge_type=edge_types[0] if edge_types else None,
        )

        # Check consistency by parsing VERIX claims first
        from core.verix import VerixParser
        verix_parser = VerixParser()
        claims = verix_parser.parse(response)
        consistency_result = consistency_checker.check(claims)
        violations = consistency_result.violations

        lines = [
            "Evaluation Results:",
            "",
            f"Task: {task[:100]}{'...' if len(task) > 100 else ''}",
            f"Response length: {len(response)} chars, {len(response.split())} tokens",
            "",
            "Metrics:",
            f"  task_accuracy: {eval_result.task_accuracy:.3f}",
            f"  token_efficiency: {eval_result.token_efficiency:.3f}",
            f"  edge_robustness: {eval_result.edge_robustness:.3f}",
            f"  epistemic_consistency: {eval_result.epistemic_consistency:.3f}",
        ]

        if edge_types:
            lines.append("")
            lines.append(f"Edge cases detected: {', '.join(e.value for e in edge_types)}")

        if violations:
            lines.append("")
            lines.append(f"Consistency violations: {len(violations)}")
            for v in violations[:3]:  # Show first 3
                lines.append(f"  - {v.violation_type.value}: {v.description[:50]}")

        result["output"] = "\n".join(lines)
        result["data"] = {
            "metrics": {
                "task_accuracy": eval_result.task_accuracy,
                "token_efficiency": eval_result.token_efficiency,
                "edge_robustness": eval_result.edge_robustness,
                "epistemic_consistency": eval_result.epistemic_consistency,
            },
            "edge_cases": [e.value for e in edge_types],
            "violations": len(violations),
        }
        return result

    # No valid input
    result["output"] = """
/eval - Evaluate tasks against cognitive architecture metrics

Usage:
  /eval "<task>" "<response>"      - Evaluate response
  /eval --corpus <path>            - Evaluate corpus file
  /eval --metrics                  - Show metric definitions
  /eval --graders                  - List available graders

Example:
  /eval "Explain quantum computing" "Quantum computing uses qubits..."
"""
    return result


if __name__ == "__main__":
    # Demo
    print("=== /eval --metrics ===")
    r = eval_command(show_metrics=True)
    print(r["output"])

    print("\n=== /eval --graders ===")
    r = eval_command(show_graders=True)
    print(r["output"])

    print("\n=== /eval single ===")
    r = eval_command(
        task="Explain quantum computing in simple terms",
        response="Quantum computing uses quantum bits or qubits that can be 0 and 1 simultaneously."
    )
    print(r["output"])
