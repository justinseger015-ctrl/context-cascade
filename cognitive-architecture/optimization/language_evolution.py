"""
Language Evolution Optimizer (DSPy Level 1)

This is the META-LEVEL optimization that evolves the VERIX/VERILINGUA
language itself based on patterns found in execution outcomes.

Cadence: Daily/Weekly (slow)
Scope: Language constructs themselves

What gets optimized:
1. VERIX notation patterns - Which patterns correlate with success?
2. VERILINGUA frame effectiveness - Which frames work for which contexts?
3. Frame combinations - Which frame sets perform best together?
4. Illocution usage - Which speech acts work in which contexts?

The optimization loop:
1. Collect execution outcomes from SkillExecutionTracker
2. Analyze patterns: success vs failure correlations
3. Use GlobalMOO to find Pareto-optimal language configurations
4. Evolve language definitions for next cycle
5. Propagate changes to Layer 2 (PromptExpressionOptimizer)
"""

import os
import sys
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, FrameworkConfig, PromptConfig, VerixStrictness
from core.verix import VerixParser, VerixValidator, VerixClaim
from optimization.globalmoo_client import (
    GlobalMOOClient, OptimizationOutcome, ParetoPoint,
    Objective, ObjectiveDirection
)


@dataclass
class LanguagePattern:
    """A pattern in VERIX/VERILINGUA usage."""
    pattern_type: str  # 'verix_notation', 'frame_activation', 'illocution', 'combination'
    pattern_value: str
    occurrence_count: int = 0
    success_count: int = 0
    avg_compliance: float = 0.0
    contexts: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        if self.occurrence_count == 0:
            return 0.0
        return self.success_count / self.occurrence_count

    @property
    def effectiveness_score(self) -> float:
        """Combined score of success rate and compliance."""
        return self.success_rate * 0.6 + self.avg_compliance * 0.4


@dataclass
class FrameEffectiveness:
    """Effectiveness of a cognitive frame in different contexts."""
    frame_name: str
    total_uses: int = 0
    success_uses: int = 0
    avg_compliance: float = 0.0

    # Per-context effectiveness
    context_effectiveness: Dict[str, float] = field(default_factory=dict)

    @property
    def overall_effectiveness(self) -> float:
        if self.total_uses == 0:
            return 0.0
        success_rate = self.success_uses / self.total_uses
        return success_rate * 0.5 + self.avg_compliance * 0.5


@dataclass
class LanguageEvolutionState:
    """Current state of language evolution."""
    version: int = 1
    last_evolution: float = field(default_factory=time.time)

    # Evolved patterns
    optimal_verix_patterns: List[str] = field(default_factory=list)
    optimal_frame_combinations: List[List[str]] = field(default_factory=list)
    context_frame_mapping: Dict[str, List[str]] = field(default_factory=dict)

    # Illocution effectiveness by context
    illocution_context_scores: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "last_evolution": self.last_evolution,
            "optimal_verix_patterns": self.optimal_verix_patterns,
            "optimal_frame_combinations": self.optimal_frame_combinations,
            "context_frame_mapping": self.context_frame_mapping,
            "illocution_context_scores": self.illocution_context_scores,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LanguageEvolutionState":
        return cls(
            version=data.get("version", 1),
            last_evolution=data.get("last_evolution", time.time()),
            optimal_verix_patterns=data.get("optimal_verix_patterns", []),
            optimal_frame_combinations=data.get("optimal_frame_combinations", []),
            context_frame_mapping=data.get("context_frame_mapping", {}),
            illocution_context_scores=data.get("illocution_context_scores", {}),
        )


class LanguageEvolutionOptimizer:
    """
    DSPy Level 1: Evolve the VERIX/VERILINGUA language itself.

    Analyzes execution patterns to find:
    - Which VERIX patterns work best
    - Which frame combinations are most effective
    - Which illocutions work in which contexts
    - How to evolve the language for better outcomes
    """

    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        use_mock_moo: bool = True,
    ):
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage" / "language_evolution"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.moo = GlobalMOOClient(use_mock=use_mock_moo)
        self.verix_parser = VerixParser(PromptConfig())

        # Storage files
        self.state_file = self.storage_dir / "evolution_state.json"
        self.patterns_file = self.storage_dir / "discovered_patterns.json"
        self.history_file = self.storage_dir / "evolution_history.jsonl"

        # In-memory state
        self.state = self._load_state()
        self.patterns: Dict[str, LanguagePattern] = {}
        self.frame_effectiveness: Dict[str, FrameEffectiveness] = {}

        # GlobalMOO project
        self._project_id: Optional[str] = None

    def setup_project(self, name: str = "language-evolution") -> str:
        """Setup GlobalMOO project for language optimization."""
        model_id = self.moo.create_model(
            name=f"{name}-model",
            description="Evolve VERIX/VERILINGUA language patterns",
            input_dimensions=VectorCodec.VECTOR_SIZE,
        )

        self._project_id = self.moo.create_project(
            model_id=model_id,
            name=name,
            objectives=[
                Objective("pattern_effectiveness", ObjectiveDirection.MAXIMIZE),
                Objective("frame_synergy", ObjectiveDirection.MAXIMIZE),
                Objective("context_fit", ObjectiveDirection.MAXIMIZE),
                Objective("language_economy", ObjectiveDirection.MAXIMIZE),  # Simpler = better
            ],
        )

        return self._project_id

    def analyze_execution(
        self,
        output: str,
        context: str,
        success: bool,
        config_vector: List[float],
    ) -> None:
        """
        Analyze a single execution for language patterns.

        Args:
            output: The output text containing VERIX claims
            context: Execution context (skill name, type, etc.)
            success: Whether execution succeeded
            config_vector: Configuration used
        """
        # Parse VERIX claims
        claims = self.verix_parser.parse(output)

        # Extract patterns
        self._extract_verix_patterns(claims, context, success)

        # Track frame effectiveness
        config = VectorCodec.decode(config_vector)
        self._track_frame_effectiveness(config.framework.active_frames(), context, success)

        # Track illocution usage
        self._track_illocution_usage(claims, context, success)

    def _extract_verix_patterns(
        self,
        claims: List[VerixClaim],
        context: str,
        success: bool,
    ) -> None:
        """Extract and track VERIX notation patterns."""
        for claim in claims:
            # Pattern: illocution|affect combination
            pattern_key = f"{claim.illocution}|{claim.affect}"

            if pattern_key not in self.patterns:
                self.patterns[pattern_key] = LanguagePattern(
                    pattern_type="verix_notation",
                    pattern_value=pattern_key,
                )

            pattern = self.patterns[pattern_key]
            pattern.occurrence_count += 1
            if success:
                pattern.success_count += 1
            if context not in pattern.contexts:
                pattern.contexts.append(context)

            # Track confidence levels if present
            if claim.confidence is not None:
                alpha = 0.3
                pattern.avg_compliance = (
                    alpha * claim.confidence +
                    (1 - alpha) * pattern.avg_compliance
                )

    def _track_frame_effectiveness(
        self,
        active_frames: List[str],
        context: str,
        success: bool,
    ) -> None:
        """Track effectiveness of frame activations."""
        for frame in active_frames:
            if frame not in self.frame_effectiveness:
                self.frame_effectiveness[frame] = FrameEffectiveness(frame_name=frame)

            eff = self.frame_effectiveness[frame]
            eff.total_uses += 1
            if success:
                eff.success_uses += 1

            # Update context-specific effectiveness
            if context not in eff.context_effectiveness:
                eff.context_effectiveness[context] = 0.0

            alpha = 0.3
            current = eff.context_effectiveness[context]
            eff.context_effectiveness[context] = (
                alpha * (1.0 if success else 0.0) +
                (1 - alpha) * current
            )

        # Track frame combinations
        if len(active_frames) > 1:
            combo_key = "+".join(sorted(active_frames))
            if combo_key not in self.patterns:
                self.patterns[combo_key] = LanguagePattern(
                    pattern_type="combination",
                    pattern_value=combo_key,
                )

            pattern = self.patterns[combo_key]
            pattern.occurrence_count += 1
            if success:
                pattern.success_count += 1
            if context not in pattern.contexts:
                pattern.contexts.append(context)

    def _track_illocution_usage(
        self,
        claims: List[VerixClaim],
        context: str,
        success: bool,
    ) -> None:
        """Track which illocutions work in which contexts."""
        for claim in claims:
            illocution = claim.illocution

            if illocution not in self.state.illocution_context_scores:
                self.state.illocution_context_scores[illocution] = {}

            if context not in self.state.illocution_context_scores[illocution]:
                self.state.illocution_context_scores[illocution][context] = 0.5

            # Update score
            alpha = 0.2
            current = self.state.illocution_context_scores[illocution][context]
            self.state.illocution_context_scores[illocution][context] = (
                alpha * (1.0 if success else 0.0) +
                (1 - alpha) * current
            )

    def evolve(self) -> Dict[str, Any]:
        """
        Run language evolution cycle.

        Analyzes collected patterns and evolves language definitions.

        Returns:
            Evolution report
        """
        report = {
            "version": self.state.version,
            "patterns_analyzed": len(self.patterns),
            "frames_tracked": len(self.frame_effectiveness),
            "evolutions": [],
        }

        # Find optimal VERIX patterns
        verix_patterns = [
            p for p in self.patterns.values()
            if p.pattern_type == "verix_notation" and p.occurrence_count >= 5
        ]
        verix_patterns.sort(key=lambda p: p.effectiveness_score, reverse=True)

        self.state.optimal_verix_patterns = [
            p.pattern_value for p in verix_patterns[:10]
        ]
        report["optimal_verix_patterns"] = self.state.optimal_verix_patterns

        # Find optimal frame combinations
        combo_patterns = [
            p for p in self.patterns.values()
            if p.pattern_type == "combination" and p.occurrence_count >= 3
        ]
        combo_patterns.sort(key=lambda p: p.effectiveness_score, reverse=True)

        self.state.optimal_frame_combinations = [
            p.pattern_value.split("+") for p in combo_patterns[:5]
        ]
        report["optimal_frame_combinations"] = self.state.optimal_frame_combinations

        # Build context -> frame mapping
        context_frames: Dict[str, Dict[str, float]] = defaultdict(dict)
        for frame, eff in self.frame_effectiveness.items():
            for context, score in eff.context_effectiveness.items():
                if score > 0.6:  # Only include effective mappings
                    context_frames[context][frame] = score

        self.state.context_frame_mapping = {
            ctx: sorted(frames.keys(), key=lambda f: frames[f], reverse=True)[:3]
            for ctx, frames in context_frames.items()
        }
        report["context_frame_mapping"] = self.state.context_frame_mapping

        # Report to GlobalMOO
        self._report_evolution_to_moo(report)

        # Increment version
        self.state.version += 1
        self.state.last_evolution = time.time()

        # Save state
        self._save_state()
        self._save_patterns()

        # Log to history
        with open(self.history_file, "a") as f:
            f.write(json.dumps({
                "version": self.state.version,
                "timestamp": self.state.last_evolution,
                "report": report,
            }) + "\n")

        return report

    def _report_evolution_to_moo(self, report: Dict[str, Any]) -> None:
        """Report evolution results to GlobalMOO."""
        if not self._project_id:
            return

        # Calculate evolution metrics
        pattern_effectiveness = 0.0
        if self.state.optimal_verix_patterns:
            patterns = [
                self.patterns.get(p)
                for p in self.state.optimal_verix_patterns
                if p in self.patterns
            ]
            if patterns:
                pattern_effectiveness = sum(
                    p.effectiveness_score for p in patterns if p
                ) / len(patterns)

        frame_synergy = 0.0
        if self.state.optimal_frame_combinations:
            combos = [
                self.patterns.get("+".join(sorted(c)))
                for c in self.state.optimal_frame_combinations
            ]
            if combos:
                frame_synergy = sum(
                    p.effectiveness_score for p in combos if p
                ) / len(combos)

        context_fit = len(self.state.context_frame_mapping) / 20.0  # Normalize
        language_economy = 1.0 - (len(self.state.optimal_verix_patterns) / 20.0)

        outcome = OptimizationOutcome(
            config_vector=VectorCodec.encode(FullConfig()),
            outcomes={
                "pattern_effectiveness": pattern_effectiveness,
                "frame_synergy": frame_synergy,
                "context_fit": min(1.0, context_fit),
                "language_economy": max(0.0, language_economy),
            },
            metadata={"version": self.state.version},
        )

        self.moo.report_outcome(self._project_id, outcome)

    def get_recommended_frames(self, context: str) -> List[str]:
        """Get recommended frames for a context."""
        if context in self.state.context_frame_mapping:
            return self.state.context_frame_mapping[context]

        # Fall back to most effective frames overall
        sorted_frames = sorted(
            self.frame_effectiveness.values(),
            key=lambda f: f.overall_effectiveness,
            reverse=True,
        )
        return [f.frame_name for f in sorted_frames[:3]]

    def get_recommended_illocution(self, context: str) -> str:
        """Get recommended illocution for a context."""
        best_illocution = "assert"
        best_score = 0.0

        for illocution, contexts in self.state.illocution_context_scores.items():
            if context in contexts and contexts[context] > best_score:
                best_score = contexts[context]
                best_illocution = illocution

        return best_illocution

    def _save_state(self) -> None:
        """Save evolution state."""
        with open(self.state_file, "w") as f:
            json.dump(self.state.to_dict(), f, indent=2)

    def _load_state(self) -> LanguageEvolutionState:
        """Load evolution state."""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    return LanguageEvolutionState.from_dict(json.load(f))
            except Exception:
                pass
        return LanguageEvolutionState()

    def _save_patterns(self) -> None:
        """Save discovered patterns."""
        data = {}
        for key, pattern in self.patterns.items():
            data[key] = {
                "pattern_type": pattern.pattern_type,
                "pattern_value": pattern.pattern_value,
                "occurrence_count": pattern.occurrence_count,
                "success_count": pattern.success_count,
                "avg_compliance": pattern.avg_compliance,
                "contexts": pattern.contexts,
                "effectiveness_score": pattern.effectiveness_score,
            }

        with open(self.patterns_file, "w") as f:
            json.dump(data, f, indent=2)

    def stats(self) -> Dict[str, Any]:
        """Get evolution statistics."""
        return {
            "version": self.state.version,
            "last_evolution": self.state.last_evolution,
            "patterns_discovered": len(self.patterns),
            "frames_tracked": len(self.frame_effectiveness),
            "optimal_verix_patterns": len(self.state.optimal_verix_patterns),
            "optimal_frame_combinations": len(self.state.optimal_frame_combinations),
            "context_mappings": len(self.state.context_frame_mapping),
            "illocution_contexts": sum(
                len(contexts)
                for contexts in self.state.illocution_context_scores.values()
            ),
        }


# Factory function
def create_language_evolver(
    storage_dir: Optional[Path] = None,
    use_mock_moo: bool = True,
) -> LanguageEvolutionOptimizer:
    """Create and setup language evolution optimizer."""
    evolver = LanguageEvolutionOptimizer(
        storage_dir=storage_dir,
        use_mock_moo=use_mock_moo,
    )
    evolver.setup_project()
    return evolver


if __name__ == "__main__":
    print("Language Evolution Optimizer - Demo")
    print("=" * 50)

    evolver = create_language_evolver()

    # Simulate execution analyses
    test_outputs = [
        ("[assert|neutral] API design complete [conf:0.9]", "backend-dev", True),
        ("[query|uncertain] What is the error? [conf:0.5]", "debugger", True),
        ("[commit|positive] Will implement feature [conf:0.85]", "coder", True),
        ("[assert|negative] Test failed [conf:0.95]", "tester", False),
        ("[express|neutral] Uncertain about approach", "researcher", True),
    ]

    for output, context, success in test_outputs:
        evolver.analyze_execution(
            output=output,
            context=context,
            success=success,
            config_vector=VectorCodec.encode(FullConfig()),
        )

    # Run evolution
    print("\n--- Running Evolution Cycle ---")
    report = evolver.evolve()
    print(f"Version: {report['version']}")
    print(f"Patterns analyzed: {report['patterns_analyzed']}")
    print(f"Optimal VERIX patterns: {report.get('optimal_verix_patterns', [])}")

    # Get recommendations
    print("\n--- Recommendations ---")
    for context in ["backend-dev", "researcher", "tester"]:
        frames = evolver.get_recommended_frames(context)
        illocution = evolver.get_recommended_illocution(context)
        print(f"  {context}: frames={frames}, illocution={illocution}")

    # Stats
    print("\n--- Stats ---")
    for key, value in evolver.stats().items():
        print(f"  {key}: {value}")
