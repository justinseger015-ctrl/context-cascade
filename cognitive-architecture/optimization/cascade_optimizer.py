"""
Cascade Optimizer - Full Context Cascade LEVEL Optimization.

THIS MODULE: Optimizes across cascade LEVELS (commands, agents, skills, playbooks).
DIFFERENT FROM: cascade.py which runs Three-MOO PHASES (A, B, C).

Applies DSPy x GlobalMOO optimization across the entire Context Cascade:
  Commands (127) -> Agents (216) -> Skills (196) -> Playbooks (30)

TWO-LAYER ARCHITECTURE:
  Layer 1 (Language Evolution): Optimizes VERIX/VERILINGUA patterns themselves
  Layer 2 (Prompt Expression): Optimizes how language is used in prompts/messages

The cascade optimization:
1. Collect execution feedback from all cascade levels
2. Layer 1 evolves the language based on patterns
3. Layer 2 optimizes prompts using evolved language
4. GlobalMOO finds Pareto-optimal configurations
5. Distill into named modes (Audit, Speed, Research, etc.)
6. Apply modes to future executions

Key Classes:
- CascadeOptimizer: Main orchestrator
- CascadeLevel: Enum of levels (COMMAND, AGENT, SKILL, PLAYBOOK)
- OptimizationCycleResult: Result of optimization cycle
"""

import os
import sys
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from enum import Enum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, FrameworkConfig, PromptConfig, VerixStrictness
from optimization.globalmoo_client import (
    GlobalMOOClient, OptimizationOutcome, ParetoPoint,
    Objective, ObjectiveDirection
)
from optimization.language_evolution import (
    LanguageEvolutionOptimizer, create_language_evolver
)
from optimization.skill_execution_tracker import (
    SkillExecutionTracker, ExecutionType, ExecutionRecord,
    get_tracker, track_skill_start, track_skill_end
)
from optimization.task_prompt_optimizer import (
    TaskPromptOptimizer, TaskResult, OptimizedTaskPrompt
)


class CascadeLevel(Enum):
    """Levels in the Context Cascade."""
    COMMAND = "command"
    AGENT = "agent"
    SKILL = "skill"
    PLAYBOOK = "playbook"


@dataclass
class CascadeLevelStats:
    """Statistics for a cascade level."""
    level: CascadeLevel
    total_executions: int = 0
    successful_executions: int = 0
    avg_verix_compliance: float = 0.0
    optimal_config: Optional[FullConfig] = None

    @property
    def success_rate(self) -> float:
        if self.total_executions == 0:
            return 0.0
        return self.successful_executions / self.total_executions


@dataclass
class OptimizationCycleResult:
    """Result of a full optimization cycle."""
    cycle_number: int
    timestamp: float = field(default_factory=time.time)

    # Layer 1 results
    language_evolution_version: int = 0
    patterns_evolved: int = 0
    frames_optimized: int = 0

    # Layer 2 results
    prompts_optimized: int = 0
    cache_hit_rate: float = 0.0

    # Cascade results
    cascade_stats: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Pareto frontier
    pareto_points: int = 0
    named_modes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cycle_number": self.cycle_number,
            "timestamp": self.timestamp,
            "language_evolution_version": self.language_evolution_version,
            "patterns_evolved": self.patterns_evolved,
            "frames_optimized": self.frames_optimized,
            "prompts_optimized": self.prompts_optimized,
            "cache_hit_rate": self.cache_hit_rate,
            "cascade_stats": self.cascade_stats,
            "pareto_points": self.pareto_points,
            "named_modes": self.named_modes,
        }


class CascadeOptimizer:
    """
    Full Context Cascade Optimizer.

    Coordinates:
    - Layer 1: LanguageEvolutionOptimizer (evolves language patterns)
    - Layer 2: TaskPromptOptimizer (optimizes prompt expressions)
    - SkillExecutionTracker (collects feedback from all levels)
    - GlobalMOO (finds Pareto-optimal configurations)
    """

    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        use_mock_moo: bool = True,
    ):
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage" / "cascade_optimizer"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize Layer 1: Language Evolution
        self.language_evolver = LanguageEvolutionOptimizer(
            storage_dir=self.storage_dir / "language_evolution",
            use_mock_moo=use_mock_moo,
        )
        self.language_evolver.setup_project()

        # Initialize Layer 2: Task Prompt Optimization
        self.prompt_optimizer = TaskPromptOptimizer(
            storage_dir=self.storage_dir / "prompt_optimization",
            use_mock_moo=use_mock_moo,
        )
        self.prompt_optimizer.setup_project()

        # Initialize execution tracker
        self.tracker = SkillExecutionTracker(
            storage_dir=self.storage_dir / "execution_tracker",
            use_mock_moo=use_mock_moo,
        )
        self.tracker.setup_project()

        # Master GlobalMOO for overall optimization
        self.moo = GlobalMOOClient(use_mock=use_mock_moo)
        self._project_id: Optional[str] = None

        # Cascade level stats
        self.level_stats: Dict[CascadeLevel, CascadeLevelStats] = {
            level: CascadeLevelStats(level=level)
            for level in CascadeLevel
        }

        # Storage files
        self.modes_file = self.storage_dir / "named_modes.json"
        self.history_file = self.storage_dir / "optimization_history.jsonl"

        # Cycle counter
        self._cycle_count = 0

        # Load existing modes
        self._named_modes: Dict[str, FullConfig] = self._load_modes()

    def setup_project(self, name: str = "cascade-optimizer") -> str:
        """Setup master GlobalMOO project."""
        model_id = self.moo.create_model(
            name=f"{name}-model",
            description="Full Context Cascade optimization: Commands -> Agents -> Skills -> Playbooks",
            input_dimensions=VectorCodec.VECTOR_SIZE,
        )

        self._project_id = self.moo.create_project(
            model_id=model_id,
            name=name,
            objectives=[
                Objective("cascade_accuracy", ObjectiveDirection.MAXIMIZE, threshold=0.9),
                Objective("language_coherence", ObjectiveDirection.MAXIMIZE),
                Objective("prompt_efficiency", ObjectiveDirection.MAXIMIZE),
                Objective("cross_level_consistency", ObjectiveDirection.MAXIMIZE),
            ],
        )

        return self._project_id

    # ============================================
    # Execution Tracking (Feedback Collection)
    # ============================================

    def start_execution(
        self,
        level: CascadeLevel,
        name: str,
        description: str = "",
        parent_id: Optional[str] = None,
    ) -> str:
        """
        Start tracking an execution at any cascade level.

        This is called BEFORE executing a command/agent/skill/playbook.
        """
        # Map cascade level to execution type
        exec_type = {
            CascadeLevel.COMMAND: ExecutionType.COMMAND,
            CascadeLevel.AGENT: ExecutionType.AGENT,
            CascadeLevel.SKILL: ExecutionType.SKILL,
            CascadeLevel.PLAYBOOK: ExecutionType.PLAYBOOK,
        }[level]

        return self.tracker.start_execution(
            execution_type=exec_type,
            name=name,
            input_description=description,
            parent_id=parent_id,
        )

    def end_execution(
        self,
        execution_id: str,
        success: bool,
        output: str = "",
        error: Optional[str] = None,
    ) -> ExecutionRecord:
        """
        End tracking an execution and process feedback.

        This is called AFTER executing a command/agent/skill/playbook.
        The output is analyzed for VERIX patterns and fed to both layers.
        """
        record = self.tracker.end_execution(
            execution_id=execution_id,
            success=success,
            output=output,
            error=error,
        )

        # Feed to Layer 1: Language Evolution
        self.language_evolver.analyze_execution(
            output=output,
            context=record.name,
            success=success,
            config_vector=record.config_vector,
        )

        # Update level stats
        level = self._exec_type_to_cascade_level(record.execution_type)
        stats = self.level_stats[level]
        stats.total_executions += 1
        if success:
            stats.successful_executions += 1

        alpha = 0.3
        stats.avg_verix_compliance = (
            alpha * record.verix_compliance +
            (1 - alpha) * stats.avg_verix_compliance
        )

        return record

    def _exec_type_to_cascade_level(self, exec_type: ExecutionType) -> CascadeLevel:
        """Convert ExecutionType to CascadeLevel."""
        return {
            ExecutionType.COMMAND: CascadeLevel.COMMAND,
            ExecutionType.AGENT: CascadeLevel.AGENT,
            ExecutionType.SKILL: CascadeLevel.SKILL,
            ExecutionType.PLAYBOOK: CascadeLevel.PLAYBOOK,
        }[exec_type]

    # ============================================
    # Prompt Optimization (Layer 2)
    # ============================================

    def optimize_prompt(
        self,
        level: CascadeLevel,
        name: str,
        description: str,
    ) -> OptimizedTaskPrompt:
        """
        Optimize a prompt for any cascade level.

        Uses:
        - Layer 1 recommendations (evolved language patterns)
        - Layer 2 caching (compiled prompt templates)
        - GlobalMOO suggestions (optimal config vectors)
        """
        # Get Layer 1 recommendations
        recommended_frames = self.language_evolver.get_recommended_frames(name)
        recommended_illocution = self.language_evolver.get_recommended_illocution(name)

        # Get optimized prompt from Layer 2
        optimized = self.prompt_optimizer.optimize_task_prompt(
            description=description,
            agent_type=name,  # Using name as agent type for consistency
            task_type=level.value,
        )

        # Enhance with Layer 1 recommendations
        enhanced_description = self._enhance_with_language_patterns(
            description=optimized.optimized_prompt,
            recommended_frames=recommended_frames,
            recommended_illocution=recommended_illocution,
        )

        return OptimizedTaskPrompt(
            original_description=description,
            optimized_prompt=enhanced_description,
            agent_type=name,
            config_vector=optimized.config_vector,
            cluster_key=optimized.cluster_key,
            frame_activations=optimized.frame_activations,
            verix_requirements=optimized.verix_requirements,
        )

    def _enhance_with_language_patterns(
        self,
        description: str,
        recommended_frames: List[str],
        recommended_illocution: str,
    ) -> str:
        """Enhance prompt with Layer 1 language patterns."""
        # Add recommended frames if not already present
        frame_section = ""
        if recommended_frames:
            frame_section = f"\n## Recommended Cognitive Frames\n"
            frame_section += f"Activate: {', '.join(recommended_frames)}\n"

        # Add illocution guidance
        illocution_section = f"\n## Communication Style\n"
        illocution_section += f"Primary illocution: {recommended_illocution}\n"

        return description + frame_section + illocution_section

    # ============================================
    # Optimization Cycle
    # ============================================

    def run_optimization_cycle(self) -> OptimizationCycleResult:
        """
        Run a full optimization cycle.

        This should be run periodically (daily/weekly) to:
        1. Evolve language patterns (Layer 1)
        2. Update prompt templates (Layer 2)
        3. Compute Pareto frontier
        4. Distill named modes
        """
        self._cycle_count += 1
        result = OptimizationCycleResult(cycle_number=self._cycle_count)

        # Layer 1: Evolve language
        evolution_report = self.language_evolver.evolve()
        result.language_evolution_version = evolution_report.get("version", 0)
        result.patterns_evolved = len(evolution_report.get("optimal_verix_patterns", []))
        result.frames_optimized = len(self.language_evolver.frame_effectiveness)

        # Layer 2: Update prompt cache stats
        l2_stats = self.prompt_optimizer.l2_cache.stats()
        result.cache_hit_rate = l2_stats.get("hit_rate", 0.0)
        result.prompts_optimized = l2_stats.get("compile_count", 0)

        # Cascade stats
        for level, stats in self.level_stats.items():
            result.cascade_stats[level.value] = {
                "total_executions": stats.total_executions,
                "success_rate": stats.success_rate,
                "avg_compliance": stats.avg_verix_compliance,
            }

        # Report to master GlobalMOO
        self._report_cycle_to_moo(result)

        # Compute Pareto frontier
        pareto = self.moo.get_pareto_frontier(self._project_id) if self._project_id else []
        result.pareto_points = len(pareto)

        # Distill named modes
        modes = self._distill_named_modes(pareto)
        result.named_modes = list(modes.keys())
        self._named_modes = modes
        self._save_modes(modes)

        # Log to history
        with open(self.history_file, "a") as f:
            f.write(json.dumps(result.to_dict()) + "\n")

        return result

    def _report_cycle_to_moo(self, result: OptimizationCycleResult) -> None:
        """Report optimization cycle to master GlobalMOO."""
        if not self._project_id:
            return

        # Calculate metrics
        total_execs = sum(s.total_executions for s in self.level_stats.values())
        total_success = sum(s.successful_executions for s in self.level_stats.values())

        cascade_accuracy = total_success / total_execs if total_execs > 0 else 0.0
        language_coherence = result.patterns_evolved / 20.0  # Normalize
        prompt_efficiency = result.cache_hit_rate

        # Cross-level consistency: variance in success rates
        success_rates = [s.success_rate for s in self.level_stats.values()]
        if success_rates:
            mean_rate = sum(success_rates) / len(success_rates)
            variance = sum((r - mean_rate) ** 2 for r in success_rates) / len(success_rates)
            cross_level_consistency = 1.0 - min(1.0, variance)
        else:
            cross_level_consistency = 0.0

        outcome = OptimizationOutcome(
            config_vector=VectorCodec.encode(FullConfig()),
            outcomes={
                "cascade_accuracy": cascade_accuracy,
                "language_coherence": min(1.0, language_coherence),
                "prompt_efficiency": prompt_efficiency,
                "cross_level_consistency": cross_level_consistency,
            },
            metadata={"cycle": result.cycle_number},
        )

        self.moo.report_outcome(self._project_id, outcome)

    def _distill_named_modes(self, pareto: List[ParetoPoint]) -> Dict[str, FullConfig]:
        """Distill Pareto frontier into named modes."""
        modes = {}

        # Default modes (when no Pareto data)
        modes["standard"] = FullConfig()

        modes["audit"] = FullConfig(
            framework=FrameworkConfig(
                evidential=True, aspectual=True, morphological=True,
            ),
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.STRICT,
                require_ground=True,
                require_confidence=True,
            ),
        )

        modes["speed"] = FullConfig(
            framework=FrameworkConfig(evidential=True),
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.RELAXED,
                require_ground=False,
                require_confidence=False,
            ),
        )

        modes["research"] = FullConfig(
            framework=FrameworkConfig(
                evidential=True, aspectual=True, morphological=True,
                compositional=True, classifier=True,
            ),
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.MODERATE,
                require_ground=True,
                require_confidence=True,
            ),
        )

        modes["synthesis"] = FullConfig(
            framework=FrameworkConfig(
                evidential=True, compositional=True, honorific=True,
            ),
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.MODERATE,
            ),
        )

        # Override with Pareto-optimal if available
        if pareto:
            # Audit: max language_coherence
            audit_point = max(
                pareto,
                key=lambda p: p.outcomes.get("language_coherence", 0),
            )
            modes["audit"] = audit_point.to_config()

            # Speed: max prompt_efficiency
            speed_point = max(
                pareto,
                key=lambda p: p.outcomes.get("prompt_efficiency", 0),
            )
            modes["speed"] = speed_point.to_config()

            # Research: max cascade_accuracy
            research_point = max(
                pareto,
                key=lambda p: p.outcomes.get("cascade_accuracy", 0),
            )
            modes["research"] = research_point.to_config()

            # Standard: balanced
            standard_point = max(
                pareto,
                key=lambda p: sum(p.outcomes.values()) / len(p.outcomes),
            )
            modes["standard"] = standard_point.to_config()

        return modes

    def _save_modes(self, modes: Dict[str, FullConfig]) -> None:
        """Save named modes to file."""
        data = {}
        for name, config in modes.items():
            data[name] = {
                "config_vector": VectorCodec.encode(config),
                "cluster_key": VectorCodec.cluster_key(config),
                "summary": config.summary(),
                "active_frames": config.framework.active_frames(),
                "verix_strictness": config.prompt.verix_strictness.name,
            }

        with open(self.modes_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_modes(self) -> Dict[str, FullConfig]:
        """Load named modes from file."""
        if not self.modes_file.exists():
            return {}

        try:
            with open(self.modes_file) as f:
                data = json.load(f)

            return {
                name: VectorCodec.decode(mode_data["config_vector"])
                for name, mode_data in data.items()
            }
        except Exception:
            return {}

    def get_mode(self, mode_name: str) -> FullConfig:
        """Get a named mode configuration."""
        if mode_name in self._named_modes:
            return self._named_modes[mode_name]
        return FullConfig()  # Default

    def list_modes(self) -> Dict[str, str]:
        """List available modes with summaries."""
        return {
            name: config.summary()
            for name, config in self._named_modes.items()
        }

    def stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        return {
            "cycle_count": self._cycle_count,
            "cascade_levels": {
                level.value: {
                    "executions": stats.total_executions,
                    "success_rate": stats.success_rate,
                    "avg_compliance": stats.avg_verix_compliance,
                }
                for level, stats in self.level_stats.items()
            },
            "language_evolution": self.language_evolver.stats(),
            "prompt_optimization": self.prompt_optimizer.stats(),
            "execution_tracking": self.tracker.stats(),
            "named_modes": list(self._named_modes.keys()),
        }


# Global cascade optimizer instance
_cascade_optimizer: Optional[CascadeOptimizer] = None


def get_cascade_optimizer() -> CascadeOptimizer:
    """Get or create global cascade optimizer."""
    global _cascade_optimizer
    if _cascade_optimizer is None:
        _cascade_optimizer = CascadeOptimizer()
        _cascade_optimizer.setup_project()
    return _cascade_optimizer


# Convenience functions
def track_cascade_start(
    level: str,
    name: str,
    description: str = "",
) -> str:
    """Start tracking a cascade execution."""
    cascade_level = CascadeLevel(level)
    return get_cascade_optimizer().start_execution(
        level=cascade_level,
        name=name,
        description=description,
    )


def track_cascade_end(
    execution_id: str,
    success: bool,
    output: str = "",
) -> None:
    """End tracking a cascade execution."""
    get_cascade_optimizer().end_execution(
        execution_id=execution_id,
        success=success,
        output=output,
    )


def optimize_cascade_prompt(
    level: str,
    name: str,
    description: str,
) -> str:
    """Get optimized prompt for cascade execution."""
    cascade_level = CascadeLevel(level)
    optimized = get_cascade_optimizer().optimize_prompt(
        level=cascade_level,
        name=name,
        description=description,
    )
    return optimized.optimized_prompt


# Demo
if __name__ == "__main__":
    print("Cascade Optimizer - Full Context Cascade Demo")
    print("=" * 60)

    optimizer = get_cascade_optimizer()

    # Simulate cascade executions
    cascade_executions = [
        # Commands
        (CascadeLevel.COMMAND, "sparc-coder", True,
         "[assert|neutral] Code generated [conf:0.9]"),
        (CascadeLevel.COMMAND, "sparc-architect", True,
         "[commit|positive] Architecture designed [conf:0.85]"),

        # Agents
        (CascadeLevel.AGENT, "backend-dev", True,
         "[assert|neutral] API implemented [conf:0.88]"),
        (CascadeLevel.AGENT, "researcher", True,
         "[query|uncertain] Need more data [conf:0.7]"),
        (CascadeLevel.AGENT, "code-analyzer", False,
         "Error: Analysis failed"),

        # Skills
        (CascadeLevel.SKILL, "feature-dev-complete", True,
         "[commit|positive] Feature complete [conf:0.92]"),
        (CascadeLevel.SKILL, "smart-bug-fix", True,
         "[assert|neutral] Bug fixed [conf:0.85]"),
        (CascadeLevel.SKILL, "code-review-assistant", True,
         "[assert|negative] Issues found [conf:0.9]"),

        # Playbooks
        (CascadeLevel.PLAYBOOK, "three-loop-system", True,
         "[complete] Full development cycle done"),
        (CascadeLevel.PLAYBOOK, "deep-research-sop", True,
         "[assert|neutral] Research completed [conf:0.88]"),
    ]

    print("\n--- Simulating Cascade Executions ---")
    for level, name, success, output in cascade_executions:
        exec_id = optimizer.start_execution(level, name, f"Testing {name}")
        time.sleep(0.05)
        optimizer.end_execution(exec_id, success, output)
        print(f"  {level.value}/{name}: {'OK' if success else 'FAIL'}")

    # Run optimization cycle
    print("\n--- Running Optimization Cycle ---")
    result = optimizer.run_optimization_cycle()
    print(f"Cycle: {result.cycle_number}")
    print(f"Language Evolution v{result.language_evolution_version}")
    print(f"Patterns evolved: {result.patterns_evolved}")
    print(f"Pareto points: {result.pareto_points}")
    print(f"Named modes: {result.named_modes}")

    # Show cascade stats
    print("\n--- Cascade Stats ---")
    for level_name, stats in result.cascade_stats.items():
        print(f"  {level_name}: "
              f"execs={stats['total_executions']}, "
              f"success={stats['success_rate']:.1%}, "
              f"compliance={stats['avg_compliance']:.2f}")

    # Show named modes
    print("\n--- Named Modes ---")
    for name, summary in optimizer.list_modes().items():
        print(f"  {name}: {summary}")

    # Demo prompt optimization
    print("\n--- Optimized Prompts ---")
    for level in [CascadeLevel.SKILL, CascadeLevel.AGENT]:
        prompt = optimize_cascade_prompt(
            level.value,
            "backend-dev",
            "Build a REST API for user authentication"
        )
        print(f"\n{level.value} prompt preview:")
        print(prompt[:400] + "...")

    # Full stats
    print("\n--- Full Stats ---")
    stats = optimizer.stats()
    print(f"Cycles: {stats['cycle_count']}")
    print(f"Modes: {stats['named_modes']}")
    print(f"Language patterns: {stats['language_evolution'].get('patterns_discovered', 0)}")
