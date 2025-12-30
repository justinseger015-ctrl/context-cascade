"""
Impact Analyzer for DSPy Level 1.

Analyzes correlations between 14 config dimensions and 11 outcome metrics.
Produces:
- Correlation matrix (14 x 11)
- High-impact variables (|r| >= 0.3)
- Low-impact removal candidates (|r| < 0.1)
- Ablation analysis for top candidates

Part of the DSPy Level 1 monthly structural evolution system.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Callable
from pathlib import Path

# Try to import numpy, fallback to pure Python if not available
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None


@dataclass
class ImpactFactor:
    """Impact of a config dimension on an outcome."""
    config_index: int
    config_name: str
    outcome_name: str
    correlation: float              # Pearson correlation [-1, 1]
    significance: float             # p-value (0 if not computed)
    is_high_impact: bool            # |correlation| >= 0.3
    is_candidate_removal: bool      # |correlation| < 0.1

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "config_index": self.config_index,
            "config_name": self.config_name,
            "outcome_name": self.outcome_name,
            "correlation": self.correlation,
            "significance": self.significance,
            "is_high_impact": self.is_high_impact,
            "is_candidate_removal": self.is_candidate_removal,
        }


@dataclass
class AblationResult:
    """Result of ablating (removing) a config dimension."""
    config_index: int
    config_name: str
    baseline_score: float
    ablated_score: float
    delta: float
    recommendation: str  # 'keep', 'remove', 'investigate'

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "config_index": self.config_index,
            "config_name": self.config_name,
            "baseline_score": self.baseline_score,
            "ablated_score": self.ablated_score,
            "delta": self.delta,
            "recommendation": self.recommendation,
        }


class ImpactAnalyzer:
    """
    Analyzes correlations between 14 config dimensions and 11 outcome metrics.

    Produces:
    - Correlation matrix (14 x 11)
    - High-impact variables (|r| >= 0.3)
    - Low-impact removal candidates (|r| < 0.1)
    - Ablation analysis for top candidates
    """

    # Configuration dimension names (14 total)
    CONFIG_DIMENSIONS = [
        "evidential_frame",      # 0
        "aspectual_frame",       # 1
        "morphological_frame",   # 2
        "compositional_frame",   # 3
        "honorific_frame",       # 4
        "classifier_frame",      # 5
        "spatial_frame",         # 6
        "verix_strictness",      # 7
        "compression_level",     # 8
        "require_ground",        # 9
        "require_confidence",    # 10
        "reserved_11",           # 11
        "reserved_12",           # 12
        "reserved_13",           # 13
    ]

    # Outcome metric names (11 total)
    OUTCOME_METRICS = [
        "task_accuracy",
        "token_efficiency",
        "edge_robustness",
        "epistemic_consistency",
        "grounding_score",
        "verix_format_valid",
        "task_relevance",
        "math_accuracy",
        "factual_accuracy",
        "calibration_error",
        "latency_score",
    ]

    # Thresholds
    HIGH_IMPACT_THRESHOLD = 0.3     # |r| >= 0.3 is high impact
    LOW_IMPACT_THRESHOLD = 0.1      # |r| < 0.1 is candidate for removal

    def __init__(self, telemetry=None):
        """
        Initialize impact analyzer.

        Args:
            telemetry: TelemetryAggregator instance (optional)
        """
        self.telemetry = telemetry
        self._correlation_matrix: Optional[List[List[float]]] = None
        self._impact_factors: List[ImpactFactor] = []
        self._ablation_results: List[AblationResult] = []

    def set_telemetry(self, telemetry) -> None:
        """Set or update the telemetry aggregator."""
        self.telemetry = telemetry

    def compute_correlations(self, min_samples: int = 100) -> List[List[float]]:
        """
        Compute correlation matrix between configs and outcomes.

        Args:
            min_samples: Minimum samples required for analysis

        Returns:
            14 x 11 correlation matrix (list of lists)

        Raises:
            ValueError: If insufficient samples
        """
        if self.telemetry is None:
            raise ValueError("Telemetry aggregator not set")

        points = self.telemetry.get_points()

        if len(points) < min_samples:
            raise ValueError(f"Need {min_samples} samples, have {len(points)}")

        n_configs = len(self.CONFIG_DIMENSIONS)
        n_outcomes = len(self.OUTCOME_METRICS)

        if NUMPY_AVAILABLE:
            return self._compute_correlations_numpy(points, n_configs, n_outcomes)
        else:
            return self._compute_correlations_pure(points, n_configs, n_outcomes)

    def _compute_correlations_numpy(
        self,
        points: List,
        n_configs: int,
        n_outcomes: int,
    ) -> List[List[float]]:
        """Compute correlations using numpy."""
        # Build arrays
        config_data = np.array([p.config_vector[:n_configs] for p in points])
        outcome_data = np.array([
            [p.outcomes.get(m, float('nan')) for m in self.OUTCOME_METRICS]
            for p in points
        ])

        correlations = np.zeros((n_configs, n_outcomes))

        for i in range(n_configs):
            for j in range(n_outcomes):
                # Filter NaN values
                mask = ~np.isnan(outcome_data[:, j])
                if mask.sum() < 10:
                    correlations[i, j] = 0.0
                    continue

                x = config_data[mask, i]
                y = outcome_data[mask, j]

                # Pearson correlation
                if np.std(x) > 0 and np.std(y) > 0:
                    correlations[i, j] = np.corrcoef(x, y)[0, 1]
                else:
                    correlations[i, j] = 0.0

        self._correlation_matrix = correlations.tolist()
        self._extract_impact_factors()

        return self._correlation_matrix

    def _compute_correlations_pure(
        self,
        points: List,
        n_configs: int,
        n_outcomes: int,
    ) -> List[List[float]]:
        """Compute correlations using pure Python."""
        correlations = [[0.0] * n_outcomes for _ in range(n_configs)]

        for i in range(n_configs):
            for j in range(n_outcomes):
                metric_name = self.OUTCOME_METRICS[j]

                # Get valid pairs
                pairs = []
                for p in points:
                    if len(p.config_vector) > i:
                        x = p.config_vector[i]
                        y = p.outcomes.get(metric_name)
                        if y is not None:
                            pairs.append((x, y))

                if len(pairs) < 10:
                    continue

                correlations[i][j] = self._pearson_correlation(pairs)

        self._correlation_matrix = correlations
        self._extract_impact_factors()

        return self._correlation_matrix

    def _pearson_correlation(self, pairs: List[Tuple[float, float]]) -> float:
        """Compute Pearson correlation coefficient."""
        n = len(pairs)
        if n < 2:
            return 0.0

        # Means
        mean_x = sum(p[0] for p in pairs) / n
        mean_y = sum(p[1] for p in pairs) / n

        # Variances and covariance
        var_x = sum((p[0] - mean_x) ** 2 for p in pairs)
        var_y = sum((p[1] - mean_y) ** 2 for p in pairs)
        cov = sum((p[0] - mean_x) * (p[1] - mean_y) for p in pairs)

        # Correlation
        if var_x <= 0 or var_y <= 0:
            return 0.0

        return cov / ((var_x ** 0.5) * (var_y ** 0.5))

    def _extract_impact_factors(self) -> None:
        """Extract impact factors from correlation matrix."""
        self._impact_factors = []

        if self._correlation_matrix is None:
            return

        for i, config_name in enumerate(self.CONFIG_DIMENSIONS):
            for j, outcome_name in enumerate(self.OUTCOME_METRICS):
                r = self._correlation_matrix[i][j]

                # Skip invalid correlations
                if r != r:  # NaN check
                    continue

                factor = ImpactFactor(
                    config_index=i,
                    config_name=config_name,
                    outcome_name=outcome_name,
                    correlation=r,
                    significance=0.0,  # TODO: compute p-value
                    is_high_impact=abs(r) >= self.HIGH_IMPACT_THRESHOLD,
                    is_candidate_removal=abs(r) < self.LOW_IMPACT_THRESHOLD,
                )
                self._impact_factors.append(factor)

    def get_high_impact_variables(self) -> List[ImpactFactor]:
        """
        Get variables with |correlation| >= 0.3.

        Returns:
            List of high-impact factors sorted by absolute correlation
        """
        high_impact = [f for f in self._impact_factors if f.is_high_impact]
        return sorted(high_impact, key=lambda f: -abs(f.correlation))

    def get_removal_candidates(self) -> List[str]:
        """
        Get config dimensions that could potentially be removed.

        A dimension is a removal candidate if ALL its outcome correlations
        are below the LOW_IMPACT_THRESHOLD.

        Returns:
            List of config dimension names
        """
        # Count low-impact correlations per config dimension
        candidate_counts: Dict[str, int] = {}

        for f in self._impact_factors:
            if f.is_candidate_removal:
                candidate_counts[f.config_name] = candidate_counts.get(f.config_name, 0) + 1

        # Only return if ALL outcomes show low impact (at least 80%)
        n_outcomes = len(self.OUTCOME_METRICS)
        threshold = int(n_outcomes * 0.8)

        return [
            name for name, count in candidate_counts.items()
            if count >= threshold
        ]

    def run_ablation_analysis(
        self,
        candidates: List[int],
        evaluation_fn: Callable[[List[float]], Dict[str, float]],
        n_trials: int = 10,
    ) -> List[AblationResult]:
        """
        Run ablation analysis on candidate dimensions.

        Tests the impact of setting each candidate dimension to 0.

        Args:
            candidates: Config indices to ablate
            evaluation_fn: Function(config_vector) -> outcomes dict
            n_trials: Number of trials per ablation

        Returns:
            Ablation results for each candidate
        """
        results = []

        # Get baseline configs from telemetry
        baseline_configs = self._get_baseline_configs()

        if not baseline_configs:
            return results

        for idx in candidates:
            if idx >= len(self.CONFIG_DIMENSIONS):
                continue

            name = self.CONFIG_DIMENSIONS[idx]

            baseline_scores = []
            ablated_scores = []

            for config in baseline_configs[:n_trials]:
                # Baseline evaluation
                outcomes = evaluation_fn(config)
                baseline_scores.append(self._composite_score(outcomes))

                # Ablated evaluation (set dimension to 0)
                ablated_config = config.copy()
                ablated_config[idx] = 0.0
                ablated_outcomes = evaluation_fn(ablated_config)
                ablated_scores.append(self._composite_score(ablated_outcomes))

            if not baseline_scores:
                continue

            baseline_avg = sum(baseline_scores) / len(baseline_scores)
            ablated_avg = sum(ablated_scores) / len(ablated_scores)
            delta = ablated_avg - baseline_avg

            # Recommendation based on delta
            if delta > 0.05:
                recommendation = "remove"    # Removing improves score
            elif delta < -0.05:
                recommendation = "keep"      # Removing hurts score
            else:
                recommendation = "investigate"  # Marginal impact

            result = AblationResult(
                config_index=idx,
                config_name=name,
                baseline_score=baseline_avg,
                ablated_score=ablated_avg,
                delta=delta,
                recommendation=recommendation,
            )
            results.append(result)

        self._ablation_results = results
        return results

    def _get_baseline_configs(self) -> List[List[float]]:
        """Get baseline configs for ablation from telemetry."""
        if self.telemetry is None:
            return []

        points = self.telemetry.get_points()

        # Sort by task accuracy (high to low)
        ranked = sorted(
            points,
            key=lambda p: p.outcomes.get("task_accuracy", 0),
            reverse=True,
        )

        return [p.config_vector for p in ranked[:20]]

    def _composite_score(self, outcomes: Dict[str, float]) -> float:
        """
        Compute composite score from outcomes.

        Weighted average of key metrics.
        """
        weights = {
            "task_accuracy": 0.30,
            "token_efficiency": 0.20,
            "epistemic_consistency": 0.20,
            "edge_robustness": 0.15,
            "grounding_score": 0.15,
        }

        score = 0.0
        for metric, weight in weights.items():
            score += outcomes.get(metric, 0.0) * weight

        return score

    def get_correlation_matrix(self) -> Optional[List[List[float]]]:
        """Get the computed correlation matrix."""
        return self._correlation_matrix

    def get_impact_factors(self) -> List[ImpactFactor]:
        """Get all impact factors."""
        return self._impact_factors

    def get_ablation_results(self) -> List[AblationResult]:
        """Get ablation analysis results."""
        return self._ablation_results

    def generate_report(self) -> str:
        """Generate human-readable impact analysis report."""
        lines = ["# Impact Analysis Report", ""]

        # High impact section
        lines.append("## High-Impact Variables (|r| >= 0.3)")
        lines.append("")
        high_impact = self.get_high_impact_variables()
        if high_impact:
            for f in high_impact[:10]:  # Top 10
                lines.append(f"- {f.config_name} -> {f.outcome_name}: r={f.correlation:.3f}")
        else:
            lines.append("- No high-impact variables found")
        lines.append("")

        # Removal candidates section
        lines.append("## Removal Candidates (|r| < 0.1 for all outcomes)")
        lines.append("")
        candidates = self.get_removal_candidates()
        if candidates:
            for c in candidates:
                lines.append(f"- {c}")
        else:
            lines.append("- No removal candidates found")
        lines.append("")

        # Ablation results section
        if self._ablation_results:
            lines.append("## Ablation Analysis Results")
            lines.append("")
            for r in self._ablation_results:
                lines.append(
                    f"- {r.config_name}: baseline={r.baseline_score:.3f}, "
                    f"ablated={r.ablated_score:.3f}, delta={r.delta:+.3f} "
                    f"-> {r.recommendation.upper()}"
                )
            lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Total impact factors analyzed: {len(self._impact_factors)}")
        lines.append(f"- High-impact factors: {len(high_impact)}")
        lines.append(f"- Removal candidates: {len(candidates)}")
        lines.append(f"- Ablation tests run: {len(self._ablation_results)}")

        return "\n".join(lines)

    def save_report(self, filepath: Path) -> None:
        """Save report to file."""
        report = self.generate_report()
        with open(filepath, "w") as f:
            f.write(report)

    def save_results(self, filepath: Path) -> None:
        """Save results as JSON."""
        data = {
            "correlation_matrix": self._correlation_matrix,
            "impact_factors": [f.to_dict() for f in self._impact_factors],
            "ablation_results": [r.to_dict() for r in self._ablation_results],
            "high_impact_count": len(self.get_high_impact_variables()),
            "removal_candidates": self.get_removal_candidates(),
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)


# Factory function
def create_impact_analyzer(telemetry=None) -> ImpactAnalyzer:
    """Create an ImpactAnalyzer instance."""
    return ImpactAnalyzer(telemetry=telemetry)
