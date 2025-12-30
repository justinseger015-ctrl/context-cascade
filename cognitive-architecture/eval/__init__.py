"""
Evaluation module for cognitive architecture.

Provides metrics, graders, and validation utilities for measuring
prompt optimization outcomes across task_accuracy, token_efficiency,
edge_robustness, and epistemic_consistency dimensions.
"""

from .metrics import (
    EvaluationResult,
    MetricCalculator,
    length_normalize,
    format_compliance_penalty,
    aggregate_metrics,
)
from .edge_cases import (
    EdgeCaseType,
    EdgeCaseDetector,
    create_adversarial_task,
    detect_edge_case_type,
)
from .consistency import (
    ConsistencyChecker,
    ConsistencyViolation,
    check_epistemic_consistency,
    compute_coherence_score,
)

__all__ = [
    # Metrics
    "EvaluationResult",
    "MetricCalculator",
    "length_normalize",
    "format_compliance_penalty",
    "aggregate_metrics",
    # Edge Cases
    "EdgeCaseType",
    "EdgeCaseDetector",
    "create_adversarial_task",
    "detect_edge_case_type",
    # Consistency
    "ConsistencyChecker",
    "ConsistencyViolation",
    "check_epistemic_consistency",
    "compute_coherence_score",
]
