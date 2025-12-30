# Phase C & D Detailed Implementation Specification

## Executive Summary

This document provides detailed implementation plans for the remaining META-LOOP phases:
- **Phase C**: DSPy Level 1 - Failure classification, impact analysis, monthly proposals
- **Phase D**: GlobalMOO Enhancement - Two-stage optimization, holdout validation

---

## PHASE C: DSPy Level 1 Integration

### C.1 Current State Analysis

**Existing Code** (`cognitive-architecture/optimization/dspy_level1.py`):
- TelemetryAggregator: Records config vectors + outcomes
- DSPyLevel1Analyzer: Basic frame/VERIX/compression analysis
- EvolutionProposal: Proposal dataclass

**GAPS to Fill**:
1. FailureClassifier (12 failure types)
2. ImpactAnalyzer (correlation matrix 14x11)
3. Memory MCP integration for telemetry
4. Monthly scheduling mechanism

---

### C.2 Failure Classifier Implementation

**Location**: `cognitive-architecture/optimization/failure_classifier.py`

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

class FailureCategory(Enum):
    """Top-level failure categories."""
    EPISTEMIC = "epistemic"
    STRUCTURAL = "structural"
    PERFORMANCE = "performance"
    DOMAIN = "domain"

class FailureType(Enum):
    """Specific failure types (12 total)."""

    # EPISTEMIC (4 types) - Confidence/evidence issues
    OVERCONFIDENCE = "overconfidence"         # Stated confidence > actual accuracy
    UNDERCONFIDENCE = "underconfidence"       # Stated confidence < actual accuracy
    GROUNDING_FAILURE = "grounding_failure"   # Claims without evidence
    INCONSISTENCY = "inconsistency"           # Self-contradicting statements

    # STRUCTURAL (3 types) - VCL/VERIX issues
    FRAME_IGNORED = "frame_ignored"           # Required frame not activated
    VERIX_VIOLATION = "verix_violation"       # VERIX format error
    FOCUS_DRIFT = "focus_drift"               # Wandered from task

    # PERFORMANCE (3 types) - Efficiency issues
    VERBOSITY = "verbosity"                   # Excessive tokens
    TERSENESS = "terseness"                   # Insufficient detail
    LATENCY = "latency"                       # Too slow (timeout risk)

    # DOMAIN (2 types) - Factual errors
    MATH_ERROR = "math_error"                 # Calculation mistake
    FACTUAL_ERROR = "factual_error"           # Wrong fact stated

@dataclass
class FailureInstance:
    """A classified failure instance."""
    failure_type: FailureType
    category: FailureCategory
    severity: float  # 0.0 = minor, 1.0 = critical
    config_vector: List[float]
    task_type: str
    description: str
    evidence: Dict[str, any]
    timestamp: float

@dataclass
class FailurePattern:
    """A pattern of correlated failures."""
    failure_types: List[FailureType]
    correlation: float
    config_signature: str  # Which config dimensions correlate
    frequency: float       # How often this pattern occurs
    remediation: str       # Suggested fix

class FailureClassifier:
    """
    Classifies failures from evaluation outcomes.

    Uses heuristics to detect failure types from:
    - Outcome metrics (accuracy, confidence, etc.)
    - Output analysis (length, structure, etc.)
    - Config vector correlation
    """

    # Thresholds for detection
    OVERCONFIDENCE_THRESHOLD = 0.15  # |stated_conf - actual_acc| > 0.15
    VERBOSITY_RATIO = 2.0            # tokens > 2x expected
    TERSENESS_RATIO = 0.3            # tokens < 0.3x expected

    def __init__(self, telemetry: TelemetryAggregator):
        self.telemetry = telemetry
        self._failures: List[FailureInstance] = []

    def classify_outcome(
        self,
        config_vector: List[float],
        outcomes: Dict[str, float],
        output_metadata: Dict[str, any],
        task_type: str,
    ) -> List[FailureInstance]:
        """
        Classify failures in a single evaluation outcome.

        Args:
            config_vector: The configuration used
            outcomes: Measured outcomes (accuracy, efficiency, etc.)
            output_metadata: Additional info (token_count, confidence_stated, etc.)
            task_type: Type of task evaluated

        Returns:
            List of detected failures
        """
        failures = []

        # Check EPISTEMIC failures
        failures.extend(self._check_epistemic(config_vector, outcomes, output_metadata, task_type))

        # Check STRUCTURAL failures
        failures.extend(self._check_structural(config_vector, outcomes, output_metadata, task_type))

        # Check PERFORMANCE failures
        failures.extend(self._check_performance(config_vector, outcomes, output_metadata, task_type))

        # Check DOMAIN failures
        failures.extend(self._check_domain(config_vector, outcomes, output_metadata, task_type))

        self._failures.extend(failures)
        return failures

    def _check_epistemic(self, config, outcomes, metadata, task) -> List[FailureInstance]:
        """Check for epistemic failures."""
        failures = []

        # Overconfidence
        stated_conf = metadata.get('confidence_stated', 0.5)
        actual_acc = outcomes.get('task_accuracy', 0.5)
        if stated_conf - actual_acc > self.OVERCONFIDENCE_THRESHOLD:
            failures.append(FailureInstance(
                failure_type=FailureType.OVERCONFIDENCE,
                category=FailureCategory.EPISTEMIC,
                severity=(stated_conf - actual_acc) / 0.5,
                config_vector=config,
                task_type=task,
                description=f"Stated {stated_conf:.2f} but achieved {actual_acc:.2f}",
                evidence={'stated': stated_conf, 'actual': actual_acc},
                timestamp=time.time()
            ))

        # Underconfidence
        if actual_acc - stated_conf > self.OVERCONFIDENCE_THRESHOLD:
            failures.append(FailureInstance(
                failure_type=FailureType.UNDERCONFIDENCE,
                category=FailureCategory.EPISTEMIC,
                severity=(actual_acc - stated_conf) / 0.5,
                config_vector=config,
                task_type=task,
                description=f"Stated {stated_conf:.2f} but achieved {actual_acc:.2f}",
                evidence={'stated': stated_conf, 'actual': actual_acc},
                timestamp=time.time()
            ))

        # Grounding failure
        grounding_score = outcomes.get('grounding_score', 1.0)
        if grounding_score < 0.5:
            failures.append(FailureInstance(
                failure_type=FailureType.GROUNDING_FAILURE,
                category=FailureCategory.EPISTEMIC,
                severity=1.0 - grounding_score,
                config_vector=config,
                task_type=task,
                description=f"Low grounding score: {grounding_score:.2f}",
                evidence={'grounding_score': grounding_score},
                timestamp=time.time()
            ))

        # Inconsistency
        consistency = outcomes.get('epistemic_consistency', 1.0)
        if consistency < 0.7:
            failures.append(FailureInstance(
                failure_type=FailureType.INCONSISTENCY,
                category=FailureCategory.EPISTEMIC,
                severity=1.0 - consistency,
                config_vector=config,
                task_type=task,
                description=f"Inconsistent statements: {consistency:.2f}",
                evidence={'consistency': consistency},
                timestamp=time.time()
            ))

        return failures

    def _check_structural(self, config, outcomes, metadata, task) -> List[FailureInstance]:
        """Check for structural VCL/VERIX failures."""
        failures = []

        # Frame ignored
        frames_expected = metadata.get('frames_expected', [])
        frames_used = metadata.get('frames_used', [])
        ignored = set(frames_expected) - set(frames_used)
        if ignored:
            failures.append(FailureInstance(
                failure_type=FailureType.FRAME_IGNORED,
                category=FailureCategory.STRUCTURAL,
                severity=len(ignored) / max(1, len(frames_expected)),
                config_vector=config,
                task_type=task,
                description=f"Ignored frames: {ignored}",
                evidence={'ignored': list(ignored)},
                timestamp=time.time()
            ))

        # VERIX violation
        verix_valid = outcomes.get('verix_format_valid', 1.0)
        if verix_valid < 0.8:
            failures.append(FailureInstance(
                failure_type=FailureType.VERIX_VIOLATION,
                category=FailureCategory.STRUCTURAL,
                severity=1.0 - verix_valid,
                config_vector=config,
                task_type=task,
                description=f"VERIX format errors: {1-verix_valid:.0%}",
                evidence={'verix_valid': verix_valid},
                timestamp=time.time()
            ))

        # Focus drift
        relevance = outcomes.get('task_relevance', 1.0)
        if relevance < 0.7:
            failures.append(FailureInstance(
                failure_type=FailureType.FOCUS_DRIFT,
                category=FailureCategory.STRUCTURAL,
                severity=1.0 - relevance,
                config_vector=config,
                task_type=task,
                description=f"Output drifted from task: {relevance:.2f}",
                evidence={'relevance': relevance},
                timestamp=time.time()
            ))

        return failures

    def _check_performance(self, config, outcomes, metadata, task) -> List[FailureInstance]:
        """Check for performance failures."""
        failures = []

        token_count = metadata.get('token_count', 0)
        expected_tokens = metadata.get('expected_tokens', 500)

        # Verbosity
        if token_count > expected_tokens * self.VERBOSITY_RATIO:
            failures.append(FailureInstance(
                failure_type=FailureType.VERBOSITY,
                category=FailureCategory.PERFORMANCE,
                severity=min(1.0, (token_count / expected_tokens - 1) / 3),
                config_vector=config,
                task_type=task,
                description=f"Excessive tokens: {token_count} (expected {expected_tokens})",
                evidence={'actual': token_count, 'expected': expected_tokens},
                timestamp=time.time()
            ))

        # Terseness
        if token_count < expected_tokens * self.TERSENESS_RATIO:
            failures.append(FailureInstance(
                failure_type=FailureType.TERSENESS,
                category=FailureCategory.PERFORMANCE,
                severity=min(1.0, 1 - token_count / (expected_tokens * self.TERSENESS_RATIO)),
                config_vector=config,
                task_type=task,
                description=f"Too brief: {token_count} (expected {expected_tokens})",
                evidence={'actual': token_count, 'expected': expected_tokens},
                timestamp=time.time()
            ))

        # Latency (if tracked)
        latency_ms = metadata.get('latency_ms', 0)
        latency_limit = metadata.get('latency_limit_ms', 30000)
        if latency_ms > latency_limit * 0.8:
            failures.append(FailureInstance(
                failure_type=FailureType.LATENCY,
                category=FailureCategory.PERFORMANCE,
                severity=min(1.0, latency_ms / latency_limit),
                config_vector=config,
                task_type=task,
                description=f"Near timeout: {latency_ms}ms (limit {latency_limit}ms)",
                evidence={'latency': latency_ms, 'limit': latency_limit},
                timestamp=time.time()
            ))

        return failures

    def _check_domain(self, config, outcomes, metadata, task) -> List[FailureInstance]:
        """Check for domain-specific failures."""
        failures = []

        # Math error (if applicable)
        math_accuracy = outcomes.get('math_accuracy', None)
        if math_accuracy is not None and math_accuracy < 0.9:
            failures.append(FailureInstance(
                failure_type=FailureType.MATH_ERROR,
                category=FailureCategory.DOMAIN,
                severity=1.0 - math_accuracy,
                config_vector=config,
                task_type=task,
                description=f"Math errors detected: {1-math_accuracy:.0%}",
                evidence={'math_accuracy': math_accuracy},
                timestamp=time.time()
            ))

        # Factual error
        factual_accuracy = outcomes.get('factual_accuracy', None)
        if factual_accuracy is not None and factual_accuracy < 0.9:
            failures.append(FailureInstance(
                failure_type=FailureType.FACTUAL_ERROR,
                category=FailureCategory.DOMAIN,
                severity=1.0 - factual_accuracy,
                config_vector=config,
                task_type=task,
                description=f"Factual errors detected: {1-factual_accuracy:.0%}",
                evidence={'factual_accuracy': factual_accuracy},
                timestamp=time.time()
            ))

        return failures

    def find_patterns(self, min_correlation: float = 0.3) -> List[FailurePattern]:
        """Find correlated failure patterns."""
        # Implementation: Cluster failures by config signature + failure type
        # Return patterns with correlation >= min_correlation
        pass

    def get_summary(self) -> Dict[str, any]:
        """Get failure summary statistics."""
        by_type = {}
        by_category = {}

        for f in self._failures:
            t = f.failure_type.value
            c = f.category.value

            by_type[t] = by_type.get(t, 0) + 1
            by_category[c] = by_category.get(c, 0) + 1

        return {
            'total_failures': len(self._failures),
            'by_type': by_type,
            'by_category': by_category,
            'avg_severity': sum(f.severity for f in self._failures) / max(1, len(self._failures))
        }
```

---

### C.3 Impact Analyzer Implementation

**Location**: `cognitive-architecture/optimization/impact_analyzer.py`

```python
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

@dataclass
class ImpactFactor:
    """Impact of a config dimension on an outcome."""
    config_index: int
    config_name: str
    outcome_name: str
    correlation: float      # Pearson correlation [-1, 1]
    significance: float     # p-value
    is_high_impact: bool    # |correlation| >= 0.3
    is_candidate_removal: bool  # |correlation| < 0.1

@dataclass
class AblationResult:
    """Result of ablating (removing) a config dimension."""
    config_index: int
    config_name: str
    baseline_score: float
    ablated_score: float
    delta: float
    recommendation: str  # 'keep', 'remove', 'investigate'

class ImpactAnalyzer:
    """
    Analyzes correlations between 14 config dimensions and 11 outcome metrics.

    Produces:
    - Correlation matrix (14 x 11)
    - High-impact variables (|r| >= 0.3)
    - Low-impact removal candidates (|r| < 0.1)
    - Ablation analysis for top candidates
    """

    CONFIG_DIMENSIONS = [
        'evidential_frame', 'aspectual_frame', 'morphological_frame',
        'compositional_frame', 'honorific_frame', 'classifier_frame',
        'spatial_frame', 'verix_strictness', 'compression_level',
        'require_ground', 'require_confidence', 'reserved_11',
        'reserved_12', 'reserved_13'
    ]

    OUTCOME_METRICS = [
        'task_accuracy', 'token_efficiency', 'edge_robustness',
        'epistemic_consistency', 'grounding_score', 'verix_format_valid',
        'task_relevance', 'math_accuracy', 'factual_accuracy',
        'calibration_error', 'latency_score'
    ]

    HIGH_IMPACT_THRESHOLD = 0.3
    LOW_IMPACT_THRESHOLD = 0.1

    def __init__(self, telemetry: TelemetryAggregator):
        self.telemetry = telemetry
        self._correlation_matrix: Optional[np.ndarray] = None
        self._impact_factors: List[ImpactFactor] = []

    def compute_correlations(self, min_samples: int = 100) -> np.ndarray:
        """
        Compute correlation matrix between configs and outcomes.

        Returns:
            14 x 11 correlation matrix
        """
        points = self.telemetry.get_points()

        if len(points) < min_samples:
            raise ValueError(f"Need {min_samples} samples, have {len(points)}")

        # Build arrays
        config_data = np.array([p.config_vector for p in points])
        outcome_data = np.array([
            [p.outcomes.get(m, np.nan) for m in self.OUTCOME_METRICS]
            for p in points
        ])

        # Compute correlations
        n_configs = len(self.CONFIG_DIMENSIONS)
        n_outcomes = len(self.OUTCOME_METRICS)
        correlations = np.zeros((n_configs, n_outcomes))

        for i in range(n_configs):
            for j in range(n_outcomes):
                # Filter NaN values
                mask = ~np.isnan(outcome_data[:, j])
                if mask.sum() < 10:
                    continue

                x = config_data[mask, i]
                y = outcome_data[mask, j]

                # Pearson correlation
                if np.std(x) > 0 and np.std(y) > 0:
                    correlations[i, j] = np.corrcoef(x, y)[0, 1]

        self._correlation_matrix = correlations
        self._extract_impact_factors()

        return correlations

    def _extract_impact_factors(self):
        """Extract impact factors from correlation matrix."""
        self._impact_factors = []

        for i, config_name in enumerate(self.CONFIG_DIMENSIONS):
            for j, outcome_name in enumerate(self.OUTCOME_METRICS):
                r = self._correlation_matrix[i, j]

                if np.isnan(r):
                    continue

                factor = ImpactFactor(
                    config_index=i,
                    config_name=config_name,
                    outcome_name=outcome_name,
                    correlation=r,
                    significance=0.0,  # TODO: compute p-value
                    is_high_impact=abs(r) >= self.HIGH_IMPACT_THRESHOLD,
                    is_candidate_removal=abs(r) < self.LOW_IMPACT_THRESHOLD
                )
                self._impact_factors.append(factor)

    def get_high_impact_variables(self) -> List[ImpactFactor]:
        """Get variables with |correlation| >= 0.3."""
        return [f for f in self._impact_factors if f.is_high_impact]

    def get_removal_candidates(self) -> List[str]:
        """Get config dimensions that could potentially be removed."""
        # A dimension is a removal candidate if ALL its outcome correlations are low
        candidate_counts = {}

        for f in self._impact_factors:
            if f.is_candidate_removal:
                candidate_counts[f.config_name] = candidate_counts.get(f.config_name, 0) + 1

        # Only return if ALL outcomes show low impact
        n_outcomes = len(self.OUTCOME_METRICS)
        return [name for name, count in candidate_counts.items() if count >= n_outcomes * 0.8]

    def run_ablation_analysis(
        self,
        candidates: List[int],
        evaluation_fn,
        n_trials: int = 10,
    ) -> List[AblationResult]:
        """
        Run ablation analysis on candidate dimensions.

        Args:
            candidates: Config indices to ablate
            evaluation_fn: Function(config_vector) -> outcomes
            n_trials: Number of trials per ablation

        Returns:
            Ablation results for each candidate
        """
        results = []

        # Get baseline configs from Pareto frontier
        baseline_configs = self._get_baseline_configs()

        for idx in candidates:
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

            baseline_avg = np.mean(baseline_scores)
            ablated_avg = np.mean(ablated_scores)
            delta = ablated_avg - baseline_avg

            # Recommendation
            if delta > 0.05:
                rec = 'remove'  # Removing improves score
            elif delta < -0.05:
                rec = 'keep'    # Removing hurts score
            else:
                rec = 'investigate'  # Marginal impact

            results.append(AblationResult(
                config_index=idx,
                config_name=name,
                baseline_score=baseline_avg,
                ablated_score=ablated_avg,
                delta=delta,
                recommendation=rec
            ))

        return results

    def _get_baseline_configs(self) -> List[List[float]]:
        """Get baseline configs for ablation."""
        # Use recent high-performing configs
        points = self.telemetry.get_points()
        ranked = sorted(
            points,
            key=lambda p: p.outcomes.get('task_accuracy', 0),
            reverse=True
        )
        return [p.config_vector for p in ranked[:20]]

    def _composite_score(self, outcomes: Dict[str, float]) -> float:
        """Compute composite score from outcomes."""
        weights = {
            'task_accuracy': 0.3,
            'token_efficiency': 0.2,
            'epistemic_consistency': 0.2,
            'edge_robustness': 0.15,
            'grounding_score': 0.15,
        }
        score = sum(outcomes.get(k, 0) * w for k, w in weights.items())
        return score

    def generate_report(self) -> str:
        """Generate human-readable impact analysis report."""
        report = ["# Impact Analysis Report\n"]

        # High impact
        report.append("## High-Impact Variables (|r| >= 0.3)\n")
        high_impact = self.get_high_impact_variables()
        for f in sorted(high_impact, key=lambda x: -abs(x.correlation)):
            report.append(f"- {f.config_name} -> {f.outcome_name}: r={f.correlation:.3f}\n")

        # Removal candidates
        report.append("\n## Removal Candidates (|r| < 0.1 for all outcomes)\n")
        candidates = self.get_removal_candidates()
        for c in candidates:
            report.append(f"- {c}\n")

        return "".join(report)
```

---

### C.4 Memory MCP Integration

**Location**: Update `dspy_level1.py` with Memory MCP support

```python
# Add to TelemetryAggregator

async def persist_to_memory_mcp(self):
    """Persist telemetry to Memory MCP for cross-session aggregation."""
    from hooks.12fa.memory_mcp_tagging_protocol import taggedMemoryStore

    aggregate = {
        'timestamp': time.time(),
        'point_count': len(self._points),
        'by_cluster': self.aggregate_by_cluster(),
        'by_frame': self.aggregate_by_frame(),
        'x-schema-version': '1.0'
    }

    await taggedMemoryStore('dspy-level1', json.dumps(aggregate), {
        'project': 'context-cascade',
        'x-intent': 'telemetry_aggregate',
        'x-namespace': 'dspy/telemetry/aggregate'
    })

async def load_from_memory_mcp(self):
    """Load historical telemetry from Memory MCP."""
    # Query Memory MCP for dspy/telemetry/* entries
    # Merge with local telemetry
    pass
```

---

### C.5 Monthly Scheduling

**Location**: `cognitive-architecture/optimization/monthly_analyzer.py`

```python
class MonthlyAnalyzer:
    """
    Runs monthly structural evolution analysis.

    Schedule: First Sunday of each month at 00:00 UTC
    """

    def __init__(
        self,
        telemetry: TelemetryAggregator,
        failure_classifier: FailureClassifier,
        impact_analyzer: ImpactAnalyzer,
        proposals_dir: Path,
    ):
        self.telemetry = telemetry
        self.failure_classifier = failure_classifier
        self.impact_analyzer = impact_analyzer
        self.proposals_dir = proposals_dir

    def run_monthly_analysis(self) -> List[EvolutionProposal]:
        """
        Execute monthly analysis pipeline.

        Steps:
        1. Load telemetry from Memory MCP (last 30 days)
        2. Run failure classification
        3. Compute impact correlations
        4. Run ablation on removal candidates
        5. Generate evolution proposals
        6. Store proposals for human review
        """
        proposals = []

        # 1. Load telemetry
        self.telemetry.load_from_memory_mcp()

        # 2. Failure classification
        failures = self.failure_classifier.get_summary()

        # 3. Impact analysis
        correlations = self.impact_analyzer.compute_correlations()
        high_impact = self.impact_analyzer.get_high_impact_variables()
        removal_candidates = self.impact_analyzer.get_removal_candidates()

        # 4. Generate proposals based on findings
        # Proposal type 1: Disable low-impact frames
        for candidate in removal_candidates:
            if candidate.endswith('_frame'):
                proposals.append(self._create_disable_frame_proposal(candidate))

        # Proposal type 2: Adjust based on failure patterns
        if failures['by_category'].get('epistemic', 0) > 0.1:
            proposals.append(self._create_epistemic_fix_proposal(failures))

        # Proposal type 3: Optimize high-impact variables
        for factor in high_impact[:3]:  # Top 3
            proposals.append(self._create_optimization_proposal(factor))

        # 5. Store proposals
        self._store_proposals(proposals)

        return proposals

    def _create_disable_frame_proposal(self, frame_name: str) -> EvolutionProposal:
        """Create proposal to disable a low-impact frame."""
        return EvolutionProposal(
            proposal_id=f"L1-MONTHLY-{int(time.time())}",
            proposal_type=ProposalType.FRAME_ACTIVATION,
            description=f"Disable {frame_name} by default",
            rationale=f"Ablation shows minimal impact on all outcomes",
            changes={'frame': frame_name, 'default_enabled': False},
            expected_impact={'token_efficiency': 0.02},
        )

    def _store_proposals(self, proposals: List[EvolutionProposal]):
        """Store proposals to file and Memory MCP."""
        filepath = self.proposals_dir / f"monthly-{time.strftime('%Y-%m')}.json"
        with open(filepath, 'w') as f:
            json.dump([p.to_dict() for p in proposals], f, indent=2)
```

---

## PHASE D: GlobalMOO Enhancement

### D.1 Current State Analysis

**Existing Code** (`cognitive-architecture/optimization/globalmoo_client.py`):
- GlobalMOOClient with 5D cognitive project
- TwoTierBounds for IMMUTABLE/MUTABLE separation
- ThrashingDetector for oscillation recovery
- Pareto frontier extraction

**GAPS to Fill**:
1. TwoStageOptimizer (GlobalMOO 5D -> PyMOO 14D)
2. HoldoutValidator (20% holdout, overfitting detection)
3. Enhanced mode distillation (task-specific modes)
4. Three-phase cascade (structure, edge, production)

---

### D.2 Two-Stage Optimizer Implementation

**Location**: `cognitive-architecture/optimization/two_stage_optimizer.py`

```python
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np

# PyMOO imports (optional dependency)
try:
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.core.problem import ElementwiseProblem
    from pymoo.optimize import minimize
    PYMOO_AVAILABLE = True
except ImportError:
    PYMOO_AVAILABLE = False

@dataclass
class OptimizationResult:
    """Result of two-stage optimization."""
    pareto_5d: List[ParetoPoint]      # Stage 1 results (5D)
    pareto_14d: List[ParetoPoint]     # Stage 2 results (14D)
    best_configs: List[FullConfig]    # Final recommended configs
    convergence_history: List[float]  # Optimization progress
    stage1_iterations: int
    stage2_generations: int

class TwoStageOptimizer:
    """
    Two-stage optimization: GlobalMOO (5D) -> PyMOO (14D).

    Stage 1: GlobalMOO cloud-based coarse search in 5D space
             (evidential, aspectual, verix, compression, ground)

    Stage 2: PyMOO NSGA-II local refinement in full 14D space
             Uses Stage 1 results as seeds
    """

    # 5D to 14D mapping
    DIM_5D_TO_14D = {
        0: 0,   # evidential_frame
        1: 1,   # aspectual_frame
        2: 7,   # verix_strictness
        3: 8,   # compression_level
        4: 9,   # require_ground
    }

    def __init__(
        self,
        globalmoo_client: GlobalMOOClient,
        evaluation_fn,
        holdout_validator: Optional['HoldoutValidator'] = None,
    ):
        """
        Args:
            globalmoo_client: GlobalMOO client instance
            evaluation_fn: Function(config_vector) -> outcomes
            holdout_validator: Optional holdout validation
        """
        self.globalmoo = globalmoo_client
        self.evaluate = evaluation_fn
        self.holdout = holdout_validator

    def optimize(
        self,
        seed_configs: List[FullConfig],
        stage1_iterations: int = 100,
        stage2_generations: int = 50,
        stage2_population: int = 100,
    ) -> OptimizationResult:
        """
        Run two-stage optimization.

        Args:
            seed_configs: Initial seed configurations
            stage1_iterations: GlobalMOO iterations
            stage2_generations: PyMOO generations
            stage2_population: PyMOO population size

        Returns:
            OptimizationResult with Pareto frontiers from both stages
        """
        convergence = []

        # Stage 1: GlobalMOO 5D
        pareto_5d = self._run_stage1(seed_configs, stage1_iterations)
        convergence.append(self._measure_hypervolume(pareto_5d))

        # Stage 2: PyMOO 14D (seeded from Stage 1)
        seeds_14d = self._expand_to_14d(pareto_5d)
        pareto_14d = self._run_stage2(seeds_14d, stage2_generations, stage2_population)
        convergence.append(self._measure_hypervolume(pareto_14d))

        # Holdout validation if available
        if self.holdout:
            validation_result = self.holdout.validate(pareto_14d)
            if not validation_result.passed:
                print(f"WARNING: Holdout validation failed: {validation_result.reason}")

        # Extract best configs
        best_configs = self._select_best_configs(pareto_14d)

        return OptimizationResult(
            pareto_5d=pareto_5d,
            pareto_14d=pareto_14d,
            best_configs=best_configs,
            convergence_history=convergence,
            stage1_iterations=stage1_iterations,
            stage2_generations=stage2_generations,
        )

    def _run_stage1(
        self,
        seed_configs: List[FullConfig],
        iterations: int,
    ) -> List[ParetoPoint]:
        """Run GlobalMOO 5D exploration."""
        project_id = self.globalmoo.project_id

        # Convert seeds to 5D
        seeds_5d = [self._compress_to_5d(VectorCodec.encode(c)) for c in seed_configs]

        # Load seeds
        cases = [
            OptimizationOutcome(
                config_vector=s,
                outcomes=self.evaluate(self._expand_to_14d_single(s))
            )
            for s in seeds_5d
        ]
        self.globalmoo.load_cases(project_id, cases)

        # Optimization loop
        for i in range(iterations):
            # Get suggestions
            target = {'task_accuracy': 0.95, 'token_efficiency': 0.85}
            suggestions = self.globalmoo.suggest_inverse(project_id, target)

            # Evaluate and report
            for suggestion in suggestions:
                config_14d = self._expand_to_14d_single(suggestion)
                outcomes = self.evaluate(config_14d)
                self.globalmoo.report_outcome(
                    project_id,
                    OptimizationOutcome(config_vector=suggestion, outcomes=outcomes)
                )

        return self.globalmoo.get_pareto_frontier(project_id)

    def _run_stage2(
        self,
        seeds: List[List[float]],
        generations: int,
        population_size: int,
    ) -> List[ParetoPoint]:
        """Run PyMOO NSGA-II 14D refinement."""
        if not PYMOO_AVAILABLE:
            print("PyMOO not available, skipping Stage 2")
            return []

        # Define problem
        problem = CognitiveOptProblem(
            n_var=14,
            n_obj=4,  # accuracy, efficiency, robustness, consistency
            evaluation_fn=self.evaluate,
        )

        # Create algorithm with seed population
        algorithm = NSGA2(
            pop_size=population_size,
            sampling=np.array(seeds[:population_size]),
        )

        # Run optimization
        result = minimize(
            problem,
            algorithm,
            ('n_gen', generations),
            verbose=True,
        )

        # Convert to ParetoPoints
        pareto_14d = []
        for x, f in zip(result.X, result.F):
            pareto_14d.append(ParetoPoint(
                config_vector=list(x),
                outcomes={
                    'task_accuracy': -f[0],  # PyMOO minimizes
                    'token_efficiency': -f[1],
                    'edge_robustness': -f[2],
                    'epistemic_consistency': -f[3],
                },
            ))

        return pareto_14d

    def _compress_to_5d(self, config_14d: List[float]) -> List[float]:
        """Compress 14D config to 5D for GlobalMOO."""
        return [config_14d[idx] for idx in sorted(self.DIM_5D_TO_14D.values())]

    def _expand_to_14d(self, pareto_5d: List[ParetoPoint]) -> List[List[float]]:
        """Expand 5D Pareto points to 14D seeds."""
        return [self._expand_to_14d_single(p.config_vector) for p in pareto_5d]

    def _expand_to_14d_single(self, config_5d: List[float]) -> List[float]:
        """Expand single 5D config to 14D."""
        # Start with default
        config_14d = VectorCodec.encode(FullConfig())

        # Apply 5D values
        for i5, i14 in self.DIM_5D_TO_14D.items():
            if i5 < len(config_5d):
                config_14d[i14] = config_5d[i5]

        return config_14d

    def _measure_hypervolume(self, pareto: List[ParetoPoint]) -> float:
        """Measure hypervolume indicator of Pareto frontier."""
        # Simplified: sum of outcome values
        if not pareto:
            return 0.0
        return sum(
            sum(p.outcomes.values()) for p in pareto
        ) / len(pareto)

    def _select_best_configs(self, pareto: List[ParetoPoint]) -> List[FullConfig]:
        """Select best configs from Pareto frontier."""
        # Sort by composite score
        ranked = sorted(
            pareto,
            key=lambda p: sum(p.outcomes.values()),
            reverse=True
        )
        return [VectorCodec.decode(p.config_vector) for p in ranked[:5]]


class CognitiveOptProblem(ElementwiseProblem):
    """PyMOO problem definition for cognitive architecture optimization."""

    def __init__(self, n_var, n_obj, evaluation_fn):
        super().__init__(
            n_var=n_var,
            n_obj=n_obj,
            n_constr=0,
            xl=np.zeros(n_var),
            xu=np.ones(n_var),
        )
        self.evaluate_config = evaluation_fn

    def _evaluate(self, x, out, *args, **kwargs):
        outcomes = self.evaluate_config(list(x))
        # PyMOO minimizes, so negate for maximization
        out["F"] = [
            -outcomes.get('task_accuracy', 0),
            -outcomes.get('token_efficiency', 0),
            -outcomes.get('edge_robustness', 0),
            -outcomes.get('epistemic_consistency', 0),
        ]
```

---

### D.3 Holdout Validator Implementation

**Location**: `cognitive-architecture/optimization/holdout_validator.py`

```python
from dataclasses import dataclass
from typing import List, Dict, Set
import random

@dataclass
class ValidationResult:
    """Result of holdout validation."""
    passed: bool
    training_score: float
    holdout_score: float
    gap: float              # training - holdout
    overfitting_detected: bool
    reason: str

class HoldoutValidator:
    """
    Holdout validation to detect overfitting.

    Reserves 20% of evaluation tasks that are NEVER exposed to the optimizer.
    Compares training vs holdout performance to detect overfitting.
    """

    HOLDOUT_RATIO = 0.20
    OVERFITTING_THRESHOLD = 0.20  # Flag if holdout degrades >20%

    def __init__(
        self,
        all_tasks: List[Dict],
        evaluation_fn,
        seed: int = 42,
    ):
        """
        Args:
            all_tasks: Complete set of evaluation tasks
            evaluation_fn: Function(config, task) -> outcome
            seed: Random seed for reproducibility
        """
        self.evaluation_fn = evaluation_fn

        # Split tasks into training and holdout
        random.seed(seed)
        shuffled = list(all_tasks)
        random.shuffle(shuffled)

        split_idx = int(len(shuffled) * (1 - self.HOLDOUT_RATIO))
        self.training_tasks = shuffled[:split_idx]
        self.holdout_tasks = shuffled[split_idx:]

        # Track which tasks are holdout (NEVER expose to optimizer)
        self.holdout_ids: Set[str] = {t.get('id', str(i)) for i, t in enumerate(self.holdout_tasks)}

    def is_holdout(self, task_id: str) -> bool:
        """Check if task is in holdout set."""
        return task_id in self.holdout_ids

    def get_training_tasks(self) -> List[Dict]:
        """Get training tasks (safe to use for optimization)."""
        return self.training_tasks

    def validate(self, configs: List[ParetoPoint]) -> ValidationResult:
        """
        Validate Pareto frontier against holdout tasks.

        CRITICAL: This is the ONLY place holdout tasks are evaluated.
        """
        if not configs:
            return ValidationResult(
                passed=False,
                training_score=0,
                holdout_score=0,
                gap=0,
                overfitting_detected=False,
                reason="No configs to validate"
            )

        # Evaluate on training tasks
        training_scores = []
        for config in configs:
            for task in self.training_tasks:
                outcome = self.evaluation_fn(config.config_vector, task)
                training_scores.append(outcome.get('task_accuracy', 0))

        training_avg = sum(training_scores) / len(training_scores) if training_scores else 0

        # Evaluate on holdout tasks
        holdout_scores = []
        for config in configs:
            for task in self.holdout_tasks:
                outcome = self.evaluation_fn(config.config_vector, task)
                holdout_scores.append(outcome.get('task_accuracy', 0))

        holdout_avg = sum(holdout_scores) / len(holdout_scores) if holdout_scores else 0

        # Compute gap
        gap = training_avg - holdout_avg

        # Check for overfitting
        overfitting = gap > self.OVERFITTING_THRESHOLD

        return ValidationResult(
            passed=not overfitting,
            training_score=training_avg,
            holdout_score=holdout_avg,
            gap=gap,
            overfitting_detected=overfitting,
            reason=f"Gap {gap:.2%}" + (" exceeds threshold" if overfitting else " within bounds")
        )
```

---

### D.4 Mode Distillation Enhancement

**Location**: `cognitive-architecture/optimization/mode_distiller.py`

```python
@dataclass
class DistilledMode:
    """A distilled named mode from the Pareto frontier."""
    name: str
    description: str
    config: FullConfig
    task_types: List[str]       # Which tasks this mode excels at
    primary_objective: str      # Which objective this mode optimizes
    accuracy: float
    efficiency: float
    created_from_pareto: bool

class ModeDistiller:
    """
    Enhanced mode distillation from Pareto frontier.

    Produces:
    - General modes (audit, speed, research, robust, balanced)
    - Task-specific modes (code, math, writing, analysis)
    - Dynamic modes created from optimization results
    """

    GENERAL_MODES = {
        'audit': {'accuracy': 0.96, 'efficiency': 0.76, 'primary': 'accuracy'},
        'speed': {'accuracy': 0.73, 'efficiency': 0.95, 'primary': 'efficiency'},
        'research': {'accuracy': 0.98, 'efficiency': 0.82, 'primary': 'accuracy'},
        'robust': {'accuracy': 0.96, 'efficiency': 0.77, 'primary': 'robustness'},
        'balanced': {'accuracy': 0.88, 'efficiency': 0.93, 'primary': 'balanced'},
    }

    TASK_SPECIFIC_MODES = {
        'code': {'task_types': ['coding', 'debugging', 'review']},
        'math': {'task_types': ['calculation', 'proof', 'analysis']},
        'writing': {'task_types': ['drafting', 'editing', 'formatting']},
        'analysis': {'task_types': ['research', 'synthesis', 'comparison']},
    }

    def distill_modes(
        self,
        pareto_frontier: List[ParetoPoint],
        task_performance: Dict[str, Dict[str, float]],  # task_type -> {config_hash: score}
    ) -> List[DistilledMode]:
        """
        Distill modes from Pareto frontier.

        Args:
            pareto_frontier: Optimization results
            task_performance: Performance by task type

        Returns:
            List of distilled modes
        """
        modes = []

        # Create general modes from frontier extremes
        modes.extend(self._create_general_modes(pareto_frontier))

        # Create task-specific modes
        modes.extend(self._create_task_modes(pareto_frontier, task_performance))

        return modes

    def _create_general_modes(self, pareto: List[ParetoPoint]) -> List[DistilledMode]:
        """Create general-purpose modes from Pareto extremes."""
        modes = []

        # Find accuracy-optimal
        accuracy_best = max(pareto, key=lambda p: p.outcomes.get('task_accuracy', 0))
        modes.append(DistilledMode(
            name='audit',
            description='Maximum accuracy for critical tasks',
            config=VectorCodec.decode(accuracy_best.config_vector),
            task_types=['audit', 'verification', 'critical'],
            primary_objective='task_accuracy',
            accuracy=accuracy_best.outcomes.get('task_accuracy', 0),
            efficiency=accuracy_best.outcomes.get('token_efficiency', 0),
            created_from_pareto=True
        ))

        # Find efficiency-optimal
        efficiency_best = max(pareto, key=lambda p: p.outcomes.get('token_efficiency', 0))
        modes.append(DistilledMode(
            name='speed',
            description='Maximum efficiency for quick responses',
            config=VectorCodec.decode(efficiency_best.config_vector),
            task_types=['quick', 'simple', 'routine'],
            primary_objective='token_efficiency',
            accuracy=efficiency_best.outcomes.get('task_accuracy', 0),
            efficiency=efficiency_best.outcomes.get('token_efficiency', 0),
            created_from_pareto=True
        ))

        # Find balanced
        balanced = max(
            pareto,
            key=lambda p: (
                p.outcomes.get('task_accuracy', 0) * 0.5 +
                p.outcomes.get('token_efficiency', 0) * 0.5
            )
        )
        modes.append(DistilledMode(
            name='balanced',
            description='Balanced accuracy and efficiency',
            config=VectorCodec.decode(balanced.config_vector),
            task_types=['general', 'default'],
            primary_objective='balanced',
            accuracy=balanced.outcomes.get('task_accuracy', 0),
            efficiency=balanced.outcomes.get('token_efficiency', 0),
            created_from_pareto=True
        ))

        return modes

    def _create_task_modes(
        self,
        pareto: List[ParetoPoint],
        task_performance: Dict[str, Dict[str, float]],
    ) -> List[DistilledMode]:
        """Create task-specific modes."""
        modes = []

        for mode_name, spec in self.TASK_SPECIFIC_MODES.items():
            task_types = spec['task_types']

            # Find config that performs best on these task types
            best_config = None
            best_score = 0

            for point in pareto:
                config_hash = VectorCodec.cluster_key(VectorCodec.decode(point.config_vector))

                # Average score across relevant task types
                scores = []
                for task_type in task_types:
                    if task_type in task_performance:
                        score = task_performance[task_type].get(config_hash, 0)
                        scores.append(score)

                if scores:
                    avg_score = sum(scores) / len(scores)
                    if avg_score > best_score:
                        best_score = avg_score
                        best_config = point

            if best_config:
                modes.append(DistilledMode(
                    name=mode_name,
                    description=f'Optimized for {", ".join(task_types)}',
                    config=VectorCodec.decode(best_config.config_vector),
                    task_types=task_types,
                    primary_objective=f'{mode_name}_tasks',
                    accuracy=best_config.outcomes.get('task_accuracy', 0),
                    efficiency=best_config.outcomes.get('token_efficiency', 0),
                    created_from_pareto=True
                ))

        return modes
```

---

### D.5 Three-Phase Cascade

**Location**: `cognitive-architecture/optimization/cascade_optimizer.py`

```python
@dataclass
class CascadePhase:
    """Configuration for a cascade phase."""
    name: str
    accuracy_weight: float
    efficiency_weight: float
    robustness_weight: float
    consistency_weight: float
    iterations: int

class CascadeOptimizer:
    """
    Three-phase cascade optimization.

    Phase A: Framework Structure (accuracy 60%, efficiency 40%)
             Focus: Get the basic framework right

    Phase B: Edge Discovery (accuracy 40%, robustness 60%)
             Focus: Find edge cases and robustness issues

    Phase C: Production Frontier (balanced weights)
             Focus: Final production-ready configurations
    """

    PHASES = [
        CascadePhase(
            name='A_structure',
            accuracy_weight=0.60,
            efficiency_weight=0.40,
            robustness_weight=0.00,
            consistency_weight=0.00,
            iterations=50
        ),
        CascadePhase(
            name='B_edge',
            accuracy_weight=0.40,
            efficiency_weight=0.00,
            robustness_weight=0.60,
            consistency_weight=0.00,
            iterations=50
        ),
        CascadePhase(
            name='C_production',
            accuracy_weight=0.25,
            efficiency_weight=0.25,
            robustness_weight=0.25,
            consistency_weight=0.25,
            iterations=100
        ),
    ]

    def __init__(self, two_stage_optimizer: TwoStageOptimizer):
        self.optimizer = two_stage_optimizer

    def run_cascade(
        self,
        seed_configs: List[FullConfig],
    ) -> Dict[str, OptimizationResult]:
        """
        Run three-phase cascade optimization.

        Each phase seeds from the previous phase's Pareto frontier.
        """
        results = {}
        current_seeds = seed_configs

        for phase in self.PHASES:
            print(f"\n=== Running Phase {phase.name} ===")
            print(f"Weights: acc={phase.accuracy_weight}, eff={phase.efficiency_weight}, "
                  f"rob={phase.robustness_weight}, con={phase.consistency_weight}")

            # Create weighted evaluation function
            def weighted_evaluate(config_vector):
                outcomes = self.optimizer.evaluate(config_vector)
                weighted = {
                    'task_accuracy': outcomes.get('task_accuracy', 0) * phase.accuracy_weight,
                    'token_efficiency': outcomes.get('token_efficiency', 0) * phase.efficiency_weight,
                    'edge_robustness': outcomes.get('edge_robustness', 0) * phase.robustness_weight,
                    'epistemic_consistency': outcomes.get('epistemic_consistency', 0) * phase.consistency_weight,
                }
                return weighted

            # Temporarily swap evaluation function
            original_eval = self.optimizer.evaluate
            self.optimizer.evaluate = weighted_evaluate

            try:
                result = self.optimizer.optimize(
                    current_seeds,
                    stage1_iterations=phase.iterations,
                    stage2_generations=phase.iterations // 2,
                )
                results[phase.name] = result

                # Seed next phase from this phase's results
                current_seeds = result.best_configs

            finally:
                self.optimizer.evaluate = original_eval

        return results
```

---

## Implementation Checklist

### Phase C Tasks

- [ ] Create `failure_classifier.py` with 12 failure types
- [ ] Create `impact_analyzer.py` with correlation matrix
- [ ] Add Memory MCP integration to TelemetryAggregator
- [ ] Create `monthly_analyzer.py` with scheduling
- [ ] Update `dspy_level1.py` to integrate new components
- [ ] Add tests for failure classification
- [ ] Add tests for impact analysis

### Phase D Tasks

- [ ] Create `two_stage_optimizer.py` with GlobalMOO -> PyMOO
- [ ] Create `holdout_validator.py` with 20% holdout
- [ ] Create `mode_distiller.py` with enhanced modes
- [ ] Create `cascade_optimizer.py` with three phases
- [ ] Add PyMOO as optional dependency
- [ ] Add tests for two-stage optimization
- [ ] Add tests for holdout validation

---

## Dependencies

### Phase C
- numpy (correlation computation)
- Memory MCP (telemetry persistence)

### Phase D
- pymoo (optional, for Stage 2)
- numpy (matrix operations)
- GlobalMOO API access

---

## Document Metadata

- **Version**: 1.0
- **Created**: 2025-12-30
- **Status**: Specification Complete
- **Owner**: Context Cascade Meta-Loop System

---

<promise>PHASE_C_D_SPECIFICATION_V1.0_COMPLETE</promise>
