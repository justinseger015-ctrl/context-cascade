"""
Monthly Analyzer for DSPy Level 1.

Orchestrates the monthly structural evolution analysis:
1. Load telemetry from Memory MCP (last 30 days)
2. Run failure classification
3. Compute impact correlations
4. Run ablation on removal candidates
5. Generate evolution proposals
6. Store proposals for human review

Schedule: First Sunday of each month at 00:00 UTC

Part of the DSPy Level 1 monthly structural evolution system.
"""

import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
import calendar

# Import sibling modules
from .failure_classifier import (
    FailureClassifier,
    FailureCategory,
    FailureType,
    create_failure_classifier,
)
from .impact_analyzer import (
    ImpactAnalyzer,
    ImpactFactor,
    AblationResult,
    create_impact_analyzer,
)
from .memory_mcp_integration import (
    TelemetryAggregatorWithMCP,
    create_telemetry_aggregator_with_mcp,
)
from .dspy_level1 import (
    TelemetryAggregator,
    EvolutionProposal,
    ProposalType,
    ProposalStatus,
)


@dataclass
class MonthlyAnalysisResult:
    """Result of a monthly analysis run."""
    analysis_id: str
    run_date: str
    telemetry_summary: Dict[str, Any]
    failure_summary: Dict[str, Any]
    impact_summary: Dict[str, Any]
    proposals: List[EvolutionProposal]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "analysis_id": self.analysis_id,
            "run_date": self.run_date,
            "telemetry_summary": self.telemetry_summary,
            "failure_summary": self.failure_summary,
            "impact_summary": self.impact_summary,
            "proposals": [p.to_dict() for p in self.proposals],
            "recommendations": self.recommendations,
        }


class MonthlyAnalyzer:
    """
    Orchestrates monthly structural evolution analysis.

    Combines failure classification, impact analysis, and proposal generation
    to produce monthly improvement recommendations.
    """

    # Thresholds for proposal generation
    LOW_ACCURACY_THRESHOLD = 0.6        # Generate disable proposal if below
    HIGH_FAILURE_RATE_THRESHOLD = 0.1   # Flag if failure rate exceeds
    ABLATION_IMPROVEMENT_THRESHOLD = 0.05  # Generate removal proposal if delta >

    def __init__(
        self,
        telemetry: Optional[TelemetryAggregatorWithMCP] = None,
        failure_classifier: Optional[FailureClassifier] = None,
        impact_analyzer: Optional[ImpactAnalyzer] = None,
        proposals_dir: Optional[Path] = None,
    ):
        """
        Initialize monthly analyzer.

        Args:
            telemetry: Telemetry aggregator with MCP support
            failure_classifier: Failure classifier instance
            impact_analyzer: Impact analyzer instance
            proposals_dir: Directory for storing proposals
        """
        self.telemetry = telemetry or create_telemetry_aggregator_with_mcp()
        self.failure_classifier = failure_classifier or create_failure_classifier()
        self.impact_analyzer = impact_analyzer or create_impact_analyzer()

        if proposals_dir is None:
            proposals_dir = Path(__file__).parent.parent / "storage" / "monthly-proposals"

        self.proposals_dir = Path(proposals_dir)
        self.proposals_dir.mkdir(parents=True, exist_ok=True)

        self._proposal_counter = 0
        self._last_analysis: Optional[MonthlyAnalysisResult] = None

    def should_run(self) -> bool:
        """
        Check if monthly analysis should run now.

        Runs on first Sunday of each month.
        """
        now = datetime.utcnow()

        # Get first Sunday of current month
        cal = calendar.Calendar()
        month_days = cal.monthdayscalendar(now.year, now.month)

        first_sunday = None
        for week in month_days:
            if week[6] != 0:  # Sunday is index 6
                first_sunday = week[6]
                break

        if first_sunday is None:
            return False

        # Check if today is the first Sunday
        is_first_sunday = now.day == first_sunday

        # Check if we haven't already run this month
        last_run_file = self.proposals_dir / f"last-run-{now.year}-{now.month:02d}.json"
        already_ran = last_run_file.exists()

        return is_first_sunday and not already_ran

    def run_analysis(
        self,
        days: int = 30,
        evaluation_fn: Optional[Callable[[List[float]], Dict[str, float]]] = None,
        force: bool = False,
    ) -> MonthlyAnalysisResult:
        """
        Run monthly structural evolution analysis.

        Args:
            days: Number of days to analyze
            evaluation_fn: Optional evaluation function for ablation
            force: Run even if not scheduled

        Returns:
            Analysis result with proposals
        """
        if not force and not self.should_run():
            if self._last_analysis:
                return self._last_analysis
            raise RuntimeError("Monthly analysis not scheduled. Use force=True to override.")

        analysis_id = f"monthly-{int(time.time())}"
        run_date = datetime.utcnow().isoformat()

        # Step 1: Load and aggregate historical telemetry
        telemetry_summary = self._load_telemetry(days)

        # Step 2: Run failure classification
        failure_summary = self._classify_failures()

        # Step 3: Compute impact correlations
        impact_summary = self._analyze_impact()

        # Step 4: Run ablation if evaluation function provided
        if evaluation_fn:
            self._run_ablation(evaluation_fn)

        # Step 5: Generate proposals
        proposals = self._generate_proposals(failure_summary, impact_summary)

        # Step 6: Generate recommendations
        recommendations = self._generate_recommendations(
            failure_summary, impact_summary, proposals
        )

        # Create result
        result = MonthlyAnalysisResult(
            analysis_id=analysis_id,
            run_date=run_date,
            telemetry_summary=telemetry_summary,
            failure_summary=failure_summary,
            impact_summary=impact_summary,
            proposals=proposals,
            recommendations=recommendations,
        )

        # Store result
        self._store_result(result)
        self._last_analysis = result

        return result

    def _load_telemetry(self, days: int) -> Dict[str, Any]:
        """Load and summarize telemetry data."""
        # Load from Memory MCP
        historical = self.telemetry.aggregate_historical(days=days)

        # Set telemetry for impact analyzer
        self.impact_analyzer.set_telemetry(self.telemetry.base)

        return {
            "days_analyzed": days,
            "snapshots_found": historical.get("snapshots_found", 0),
            "total_points": historical.get("total_points", 0),
            "clusters_found": len(historical.get("by_cluster", {})),
            "frames_analyzed": len(historical.get("by_frame", {})),
            "time_range": historical.get("time_range", {}),
        }

    def _classify_failures(self) -> Dict[str, Any]:
        """Run failure classification on telemetry."""
        points = self.telemetry.get_points()

        # Clear previous failures
        self.failure_classifier.clear()

        # Classify each point
        for point in points:
            self.failure_classifier.classify_outcome(
                config_vector=point.config_vector,
                outcomes=point.outcomes,
                output_metadata=point.metadata,
                task_type=point.task_type,
            )

        # Find patterns
        patterns = self.failure_classifier.find_patterns(min_correlation=0.3)

        # Get summary
        summary = self.failure_classifier.get_summary()
        summary["patterns"] = [p.to_dict() for p in patterns]

        return summary

    def _analyze_impact(self) -> Dict[str, Any]:
        """Compute impact correlations."""
        try:
            self.impact_analyzer.compute_correlations(min_samples=50)

            high_impact = self.impact_analyzer.get_high_impact_variables()
            removal_candidates = self.impact_analyzer.get_removal_candidates()

            return {
                "high_impact_count": len(high_impact),
                "high_impact_factors": [f.to_dict() for f in high_impact[:10]],
                "removal_candidates": removal_candidates,
                "correlation_matrix_computed": True,
            }

        except ValueError as e:
            # Not enough samples
            return {
                "high_impact_count": 0,
                "high_impact_factors": [],
                "removal_candidates": [],
                "correlation_matrix_computed": False,
                "error": str(e),
            }

    def _run_ablation(
        self,
        evaluation_fn: Callable[[List[float]], Dict[str, float]],
    ) -> None:
        """Run ablation analysis on removal candidates."""
        candidates = self.impact_analyzer.get_removal_candidates()

        if candidates:
            # Get indices of candidates
            candidate_indices = [
                i for i, name in enumerate(self.impact_analyzer.CONFIG_DIMENSIONS)
                if name in candidates
            ]

            self.impact_analyzer.run_ablation_analysis(
                candidates=candidate_indices,
                evaluation_fn=evaluation_fn,
                n_trials=10,
            )

    def _generate_proposals(
        self,
        failure_summary: Dict[str, Any],
        impact_summary: Dict[str, Any],
    ) -> List[EvolutionProposal]:
        """Generate evolution proposals based on analysis."""
        proposals = []

        # Proposal Type 1: Disable low-impact frames
        for candidate in impact_summary.get("removal_candidates", []):
            if candidate.endswith("_frame"):
                proposals.append(self._create_disable_frame_proposal(candidate))

        # Proposal Type 2: Address high failure categories
        failure_rates = failure_summary.get("by_category", {})
        total_failures = failure_summary.get("total_failures", 0)

        if total_failures > 0:
            for category, count in failure_rates.items():
                rate = count / total_failures
                if rate > self.HIGH_FAILURE_RATE_THRESHOLD:
                    proposals.append(self._create_fix_failure_proposal(category, rate))

        # Proposal Type 3: Optimize high-impact variables
        for factor_dict in impact_summary.get("high_impact_factors", [])[:3]:
            proposals.append(self._create_optimization_proposal(factor_dict))

        # Proposal Type 4: Based on ablation results
        for result in self.impact_analyzer.get_ablation_results():
            if result.recommendation == "remove":
                proposals.append(self._create_removal_proposal(result))

        return proposals

    def _create_disable_frame_proposal(self, frame_name: str) -> EvolutionProposal:
        """Create proposal to disable a low-impact frame."""
        self._proposal_counter += 1

        return EvolutionProposal(
            proposal_id=f"L1-MONTHLY-{self._proposal_counter:04d}",
            proposal_type=ProposalType.FRAME_ACTIVATION,
            description=f"Disable {frame_name} frame by default",
            rationale="Ablation analysis shows minimal impact on all outcome metrics",
            changes={
                "frame": frame_name,
                "default_enabled": False,
            },
            expected_impact={
                "token_efficiency": 0.02,
                "latency_score": 0.01,
            },
        )

    def _create_fix_failure_proposal(
        self,
        category: str,
        failure_rate: float,
    ) -> EvolutionProposal:
        """Create proposal to address a high failure category."""
        self._proposal_counter += 1

        # Map categories to fixes
        fixes = {
            "epistemic": {
                "description": "Increase VERIX strictness to reduce epistemic failures",
                "changes": {"verix_strictness": 2},
                "expected_impact": {"epistemic_consistency": 0.05},
            },
            "structural": {
                "description": "Enable mandatory frame validation",
                "changes": {"require_frame_validation": True},
                "expected_impact": {"verix_format_valid": 0.03},
            },
            "performance": {
                "description": "Adjust compression level for efficiency",
                "changes": {"compression_level": 2},
                "expected_impact": {"token_efficiency": 0.05},
            },
            "domain": {
                "description": "Enable domain-specific validation frames",
                "changes": {"enable_domain_validation": True},
                "expected_impact": {"factual_accuracy": 0.03},
            },
        }

        fix = fixes.get(category, {
            "description": f"Address {category} failures",
            "changes": {},
            "expected_impact": {},
        })

        return EvolutionProposal(
            proposal_id=f"L1-MONTHLY-{self._proposal_counter:04d}",
            proposal_type=ProposalType.VERIX_ADJUSTMENT,
            description=fix["description"],
            rationale=f"{category} failures represent {failure_rate:.1%} of total failures",
            changes=fix["changes"],
            expected_impact=fix["expected_impact"],
        )

    def _create_optimization_proposal(
        self,
        factor_dict: Dict[str, Any],
    ) -> EvolutionProposal:
        """Create proposal to optimize a high-impact variable."""
        self._proposal_counter += 1

        config_name = factor_dict.get("config_name", "unknown")
        outcome_name = factor_dict.get("outcome_name", "unknown")
        correlation = factor_dict.get("correlation", 0)

        direction = "increase" if correlation > 0 else "decrease"

        return EvolutionProposal(
            proposal_id=f"L1-MONTHLY-{self._proposal_counter:04d}",
            proposal_type=ProposalType.FRAME_ACTIVATION,
            description=f"Consider {direction} of {config_name}",
            rationale=f"Strong correlation (r={correlation:.3f}) with {outcome_name}",
            changes={
                "config": config_name,
                "direction": direction,
                "correlation": correlation,
            },
            expected_impact={
                outcome_name: abs(correlation) * 0.1,
            },
        )

    def _create_removal_proposal(
        self,
        result: AblationResult,
    ) -> EvolutionProposal:
        """Create proposal based on ablation result."""
        self._proposal_counter += 1

        return EvolutionProposal(
            proposal_id=f"L1-MONTHLY-{self._proposal_counter:04d}",
            proposal_type=ProposalType.FRAME_ACTIVATION,
            description=f"Remove {result.config_name} from default configuration",
            rationale=f"Ablation shows +{result.delta:.3f} improvement when disabled",
            changes={
                "config": result.config_name,
                "enabled": False,
            },
            expected_impact={
                "composite_score": result.delta,
            },
        )

    def _generate_recommendations(
        self,
        failure_summary: Dict[str, Any],
        impact_summary: Dict[str, Any],
        proposals: List[EvolutionProposal],
    ) -> List[str]:
        """Generate human-readable recommendations."""
        recommendations = []

        # Recommendation 1: Overall health assessment
        total_failures = failure_summary.get("total_failures", 0)
        avg_severity = failure_summary.get("avg_severity", 0)

        if total_failures > 100:
            recommendations.append(
                f"High failure count ({total_failures}) detected. "
                f"Average severity: {avg_severity:.2f}. "
                "Consider reviewing the proposed structural changes."
            )
        elif total_failures > 0:
            recommendations.append(
                f"Moderate failure count ({total_failures}) with avg severity {avg_severity:.2f}. "
                "System is generally healthy."
            )
        else:
            recommendations.append(
                "No failures detected in the analysis period. System is healthy."
            )

        # Recommendation 2: Priority proposals
        if proposals:
            recommendations.append(
                f"Generated {len(proposals)} evolution proposals. "
                "Review proposals in order of expected impact."
            )
        else:
            recommendations.append(
                "No structural changes recommended at this time."
            )

        # Recommendation 3: Data coverage
        if not impact_summary.get("correlation_matrix_computed", False):
            recommendations.append(
                "Insufficient data for correlation analysis. "
                "Collect more telemetry before next monthly analysis."
            )

        # Recommendation 4: Removal candidates
        removal_candidates = impact_summary.get("removal_candidates", [])
        if removal_candidates:
            recommendations.append(
                f"Consider removing: {', '.join(removal_candidates)}. "
                "These dimensions show minimal impact on outcomes."
            )

        return recommendations

    def _store_result(self, result: MonthlyAnalysisResult) -> None:
        """Store analysis result to disk."""
        # Save full result
        result_path = self.proposals_dir / f"{result.analysis_id}.json"
        with open(result_path, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

        # Mark as run this month
        now = datetime.utcnow()
        last_run_path = self.proposals_dir / f"last-run-{now.year}-{now.month:02d}.json"
        with open(last_run_path, "w") as f:
            json.dump({
                "analysis_id": result.analysis_id,
                "run_date": result.run_date,
                "proposal_count": len(result.proposals),
            }, f, indent=2)

        # Save proposals separately for easy access
        proposals_path = self.proposals_dir / f"proposals-{now.year}-{now.month:02d}.json"
        with open(proposals_path, "w") as f:
            json.dump(
                [p.to_dict() for p in result.proposals],
                f,
                indent=2,
            )

    def get_last_analysis(self) -> Optional[MonthlyAnalysisResult]:
        """Get the last analysis result."""
        return self._last_analysis

    def load_proposals(self, year: int, month: int) -> List[EvolutionProposal]:
        """Load proposals for a specific month."""
        proposals_path = self.proposals_dir / f"proposals-{year}-{month:02d}.json"

        if not proposals_path.exists():
            return []

        with open(proposals_path) as f:
            data = json.load(f)
            return [EvolutionProposal.from_dict(p) for p in data]

    def generate_report(self) -> str:
        """Generate a human-readable report of the last analysis."""
        if self._last_analysis is None:
            return "No analysis has been run yet."

        result = self._last_analysis
        lines = [
            "# Monthly Structural Evolution Report",
            f"**Analysis ID**: {result.analysis_id}",
            f"**Run Date**: {result.run_date}",
            "",
            "## Telemetry Summary",
        ]

        for key, value in result.telemetry_summary.items():
            lines.append(f"- {key}: {value}")

        lines.extend([
            "",
            "## Failure Summary",
            f"- Total failures: {result.failure_summary.get('total_failures', 0)}",
            f"- Average severity: {result.failure_summary.get('avg_severity', 0):.2f}",
        ])

        by_category = result.failure_summary.get("by_category", {})
        if by_category:
            lines.append("- By category:")
            for cat, count in by_category.items():
                lines.append(f"  - {cat}: {count}")

        lines.extend([
            "",
            "## Impact Summary",
            f"- High-impact factors: {result.impact_summary.get('high_impact_count', 0)}",
            f"- Removal candidates: {', '.join(result.impact_summary.get('removal_candidates', [])) or 'None'}",
        ])

        lines.extend([
            "",
            "## Proposals",
        ])

        for i, proposal in enumerate(result.proposals, 1):
            lines.append(f"{i}. [{proposal.proposal_type.value}] {proposal.description}")
            lines.append(f"   Rationale: {proposal.rationale}")

        lines.extend([
            "",
            "## Recommendations",
        ])

        for i, rec in enumerate(result.recommendations, 1):
            lines.append(f"{i}. {rec}")

        return "\n".join(lines)


# Factory function
def create_monthly_analyzer(
    proposals_dir: Optional[Path] = None,
) -> MonthlyAnalyzer:
    """Create a MonthlyAnalyzer instance with default components."""
    return MonthlyAnalyzer(proposals_dir=proposals_dir)
