"""
Skill Execution Tracker - Track and optimize skill/command/playbook executions.

Every execution of a VERIX/VERILINGUA skill is a learning opportunity:
1. Execute skill with current config
2. Measure outcome (success, VERIX compliance, efficiency)
3. Report to GlobalMOO
4. Learn better configs over time
5. Apply learned configs to future executions

This creates a CONTINUOUS IMPROVEMENT LOOP that runs inside Claude Code.
"""

import os
import sys
import json
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Callable
from pathlib import Path
from enum import Enum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, FrameworkConfig, PromptConfig, VerixStrictness
from core.verix import VerixParser, VerixValidator
from optimization.globalmoo_client import (
    GlobalMOOClient, OptimizationOutcome, ParetoPoint,
    Objective, ObjectiveDirection
)


class ExecutionType(Enum):
    """Type of execution being tracked."""
    SKILL = "skill"
    COMMAND = "command"
    PLAYBOOK = "playbook"
    AGENT = "agent"


@dataclass
class ExecutionRecord:
    """Record of a skill/command/playbook execution."""
    execution_id: str
    execution_type: ExecutionType
    name: str  # Skill/command/playbook name
    config_vector: List[float]

    # Inputs
    input_description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)

    # Outputs
    success: bool = True
    output: str = ""
    error: Optional[str] = None

    # Metrics
    verix_claims_found: int = 0
    verix_compliance: float = 0.0
    frame_activations_used: List[str] = field(default_factory=list)
    iterations: int = 1
    duration_ms: float = 0.0

    # Metadata
    timestamp: float = field(default_factory=time.time)
    parent_execution_id: Optional[str] = None  # For nested executions

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "execution_type": self.execution_type.value,
            "name": self.name,
            "config_vector": self.config_vector,
            "input_description": self.input_description,
            "success": self.success,
            "verix_claims_found": self.verix_claims_found,
            "verix_compliance": self.verix_compliance,
            "frame_activations_used": self.frame_activations_used,
            "iterations": self.iterations,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp,
            "error": self.error,
        }

    def to_outcome_metrics(self) -> Dict[str, float]:
        """Convert to GlobalMOO outcome format."""
        return {
            "task_accuracy": 1.0 if self.success else 0.0,
            "token_efficiency": max(0.0, 1.0 - (len(self.output) / 20000)),
            "edge_robustness": 1.0 / max(1, self.iterations),
            "epistemic_consistency": self.verix_compliance,
        }


@dataclass
class SkillConfig:
    """Configuration for a specific skill/command/playbook."""
    name: str
    execution_type: ExecutionType
    optimal_config: FullConfig
    execution_count: int = 0
    success_count: int = 0
    avg_compliance: float = 0.0
    last_updated: float = field(default_factory=time.time)

    def success_rate(self) -> float:
        if self.execution_count == 0:
            return 0.0
        return self.success_count / self.execution_count


class SkillExecutionTracker:
    """
    Track and optimize skill/command/playbook executions.

    Maintains:
    - Execution history for learning
    - Per-skill optimal configurations
    - GlobalMOO project for optimization
    - VERIX compliance analysis
    """

    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        use_mock_moo: bool = True,
    ):
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage" / "execution_tracker"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.moo = GlobalMOOClient(use_mock=use_mock_moo)
        self.verix_parser = VerixParser(PromptConfig())
        self.verix_validator = VerixValidator(PromptConfig())

        # Storage files
        self.history_file = self.storage_dir / "execution_history.jsonl"
        self.configs_file = self.storage_dir / "skill_configs.json"
        self.pareto_file = self.storage_dir / "pareto_frontier.json"

        # In-memory state
        self._skill_configs: Dict[str, SkillConfig] = {}
        self._active_executions: Dict[str, ExecutionRecord] = {}

        # GlobalMOO project
        self._project_id: Optional[str] = None

        # Load existing configs
        self._load_configs()

    def setup_project(self, name: str = "skill-execution-optimizer") -> str:
        """Setup GlobalMOO project."""
        model_id = self.moo.create_model(
            name=f"{name}-model",
            description="Optimize skill/command/playbook executions",
            input_dimensions=VectorCodec.VECTOR_SIZE,
        )

        self._project_id = self.moo.create_project(
            model_id=model_id,
            name=name,
            objectives=[
                Objective("task_accuracy", ObjectiveDirection.MAXIMIZE, threshold=0.95),
                Objective("token_efficiency", ObjectiveDirection.MAXIMIZE),
                Objective("edge_robustness", ObjectiveDirection.MAXIMIZE),
                Objective("epistemic_consistency", ObjectiveDirection.MAXIMIZE),
            ],
        )

        return self._project_id

    def start_execution(
        self,
        execution_type: ExecutionType,
        name: str,
        input_description: str = "",
        parameters: Optional[Dict[str, Any]] = None,
        parent_id: Optional[str] = None,
    ) -> str:
        """
        Start tracking an execution.

        Call this BEFORE executing a skill/command/playbook.

        Returns:
            execution_id to use for end_execution
        """
        # Generate execution ID
        execution_id = f"{execution_type.value}-{name}-{int(time.time() * 1000)}"

        # Get optimal config for this skill
        config = self.get_optimal_config(execution_type, name)

        # Create record
        record = ExecutionRecord(
            execution_id=execution_id,
            execution_type=execution_type,
            name=name,
            config_vector=VectorCodec.encode(config),
            input_description=input_description,
            parameters=parameters or {},
            frame_activations_used=config.framework.active_frames(),
            parent_execution_id=parent_id,
        )

        self._active_executions[execution_id] = record
        return execution_id

    def end_execution(
        self,
        execution_id: str,
        success: bool,
        output: str = "",
        error: Optional[str] = None,
        iterations: int = 1,
    ) -> ExecutionRecord:
        """
        End tracking an execution and record results.

        Call this AFTER executing a skill/command/playbook.

        Returns:
            Completed ExecutionRecord
        """
        if execution_id not in self._active_executions:
            raise ValueError(f"Unknown execution_id: {execution_id}")

        record = self._active_executions.pop(execution_id)

        # Update record
        record.success = success
        record.output = output
        record.error = error
        record.iterations = iterations
        record.duration_ms = (time.time() - record.timestamp) * 1000

        # Analyze VERIX compliance in output
        claims = self.verix_parser.parse(output)
        record.verix_claims_found = len(claims)
        if claims:
            record.verix_compliance = self.verix_validator.compliance_score(claims)

        # Save to history
        self._save_execution(record)

        # Update skill config
        self._update_skill_config(record)

        # Report to GlobalMOO
        self._report_to_moo(record)

        return record

    def get_optimal_config(
        self,
        execution_type: ExecutionType,
        name: str,
    ) -> FullConfig:
        """
        Get optimal configuration for a skill/command/playbook.

        Uses learned configuration if available, otherwise defaults.
        """
        key = f"{execution_type.value}:{name}"

        if key in self._skill_configs:
            return self._skill_configs[key].optimal_config

        # Try GlobalMOO suggestion
        if self._project_id and self.moo._mock_cases:
            try:
                target = {
                    "task_accuracy": 0.95,
                    "token_efficiency": 0.8,
                    "edge_robustness": 0.9,
                    "epistemic_consistency": 0.85,
                }
                suggestions = self.moo.suggest_inverse(self._project_id, target, 1)
                if suggestions:
                    return VectorCodec.decode(suggestions[0])
            except Exception:
                pass

        # Default config based on execution type
        return self._default_config(execution_type, name)

    def _default_config(self, execution_type: ExecutionType, name: str) -> FullConfig:
        """Get default config based on execution type and name."""
        name_lower = name.lower()

        # Determine appropriate frames
        if execution_type == ExecutionType.SKILL:
            if any(kw in name_lower for kw in ["research", "analysis", "audit"]):
                framework = FrameworkConfig(
                    evidential=True, aspectual=True, morphological=True,
                    compositional=True, classifier=True,
                )
                strictness = VerixStrictness.STRICT
            elif any(kw in name_lower for kw in ["dev", "code", "implement"]):
                framework = FrameworkConfig(
                    evidential=True, aspectual=True, compositional=True,
                )
                strictness = VerixStrictness.MODERATE
            else:
                framework = FrameworkConfig(evidential=True, aspectual=True)
                strictness = VerixStrictness.MODERATE

        elif execution_type == ExecutionType.COMMAND:
            framework = FrameworkConfig(evidential=True, aspectual=True)
            strictness = VerixStrictness.MODERATE

        elif execution_type == ExecutionType.PLAYBOOK:
            # Playbooks are comprehensive
            framework = FrameworkConfig(
                evidential=True, aspectual=True, compositional=True,
            )
            strictness = VerixStrictness.MODERATE

        else:  # AGENT
            framework = FrameworkConfig(evidential=True, aspectual=True)
            strictness = VerixStrictness.MODERATE

        return FullConfig(
            framework=framework,
            prompt=PromptConfig(
                verix_strictness=strictness,
                require_ground=True,
                require_confidence=True,
            ),
        )

    def _save_execution(self, record: ExecutionRecord) -> None:
        """Save execution to history file."""
        with open(self.history_file, "a") as f:
            f.write(json.dumps(record.to_dict()) + "\n")

    def _update_skill_config(self, record: ExecutionRecord) -> None:
        """Update skill configuration based on execution result."""
        key = f"{record.execution_type.value}:{record.name}"

        if key not in self._skill_configs:
            self._skill_configs[key] = SkillConfig(
                name=record.name,
                execution_type=record.execution_type,
                optimal_config=VectorCodec.decode(record.config_vector),
            )

        config = self._skill_configs[key]
        config.execution_count += 1
        if record.success:
            config.success_count += 1

        # Update rolling average compliance
        alpha = 0.3  # Exponential moving average factor
        config.avg_compliance = (
            alpha * record.verix_compliance +
            (1 - alpha) * config.avg_compliance
        )
        config.last_updated = time.time()

        # Save configs
        self._save_configs()

    def _report_to_moo(self, record: ExecutionRecord) -> None:
        """Report execution outcome to GlobalMOO."""
        if not self._project_id:
            return

        outcome = OptimizationOutcome(
            config_vector=record.config_vector,
            outcomes=record.to_outcome_metrics(),
            metadata={
                "execution_type": record.execution_type.value,
                "name": record.name,
                "execution_id": record.execution_id,
            },
        )

        self.moo.report_outcome(self._project_id, outcome)

    def _save_configs(self) -> None:
        """Save skill configs to file."""
        data = {}
        for key, config in self._skill_configs.items():
            data[key] = {
                "name": config.name,
                "execution_type": config.execution_type.value,
                "optimal_config_vector": VectorCodec.encode(config.optimal_config),
                "execution_count": config.execution_count,
                "success_count": config.success_count,
                "avg_compliance": config.avg_compliance,
                "last_updated": config.last_updated,
            }

        with open(self.configs_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load_configs(self) -> None:
        """Load skill configs from file."""
        if not self.configs_file.exists():
            return

        try:
            with open(self.configs_file) as f:
                data = json.load(f)

            for key, config_data in data.items():
                self._skill_configs[key] = SkillConfig(
                    name=config_data["name"],
                    execution_type=ExecutionType(config_data["execution_type"]),
                    optimal_config=VectorCodec.decode(config_data["optimal_config_vector"]),
                    execution_count=config_data["execution_count"],
                    success_count=config_data["success_count"],
                    avg_compliance=config_data["avg_compliance"],
                    last_updated=config_data["last_updated"],
                )
        except Exception:
            pass

    def get_pareto_frontier(self) -> List[ParetoPoint]:
        """Get current Pareto frontier."""
        if self._project_id:
            return self.moo.get_pareto_frontier(self._project_id)
        return []

    def distill_modes(self) -> Dict[str, FullConfig]:
        """Distill Pareto frontier into named modes."""
        pareto = self.get_pareto_frontier()

        modes = {
            "standard": FullConfig(),
            "audit": FullConfig(
                framework=FrameworkConfig(evidential=True, aspectual=True, morphological=True),
                prompt=PromptConfig(verix_strictness=VerixStrictness.STRICT),
            ),
            "speed": FullConfig(
                framework=FrameworkConfig(evidential=True),
                prompt=PromptConfig(verix_strictness=VerixStrictness.RELAXED),
            ),
            "research": FullConfig(
                framework=FrameworkConfig(
                    evidential=True, aspectual=True, morphological=True,
                    compositional=True, classifier=True,
                ),
                prompt=PromptConfig(verix_strictness=VerixStrictness.MODERATE),
            ),
        }

        if pareto:
            # Override with Pareto-optimal configs
            modes["audit"] = max(
                pareto, key=lambda p: p.outcomes.get("epistemic_consistency", 0)
            ).to_config()

            modes["speed"] = max(
                pareto, key=lambda p: p.outcomes.get("token_efficiency", 0)
            ).to_config()

            modes["standard"] = max(
                pareto, key=lambda p: sum(p.outcomes.values()) / len(p.outcomes)
            ).to_config()

        return modes

    def stats(self) -> Dict[str, Any]:
        """Get tracker statistics."""
        total_executions = sum(c.execution_count for c in self._skill_configs.values())
        total_success = sum(c.success_count for c in self._skill_configs.values())

        by_type = {}
        for config in self._skill_configs.values():
            t = config.execution_type.value
            if t not in by_type:
                by_type[t] = {"count": 0, "success": 0}
            by_type[t]["count"] += config.execution_count
            by_type[t]["success"] += config.success_count

        return {
            "tracked_skills": len(self._skill_configs),
            "total_executions": total_executions,
            "overall_success_rate": total_success / total_executions if total_executions > 0 else 0,
            "by_type": by_type,
            "pareto_points": len(self.get_pareto_frontier()),
            "active_executions": len(self._active_executions),
        }

    def get_skill_stats(self, execution_type: ExecutionType, name: str) -> Optional[Dict[str, Any]]:
        """Get stats for a specific skill."""
        key = f"{execution_type.value}:{name}"
        if key not in self._skill_configs:
            return None

        config = self._skill_configs[key]
        return {
            "name": config.name,
            "execution_count": config.execution_count,
            "success_rate": config.success_rate(),
            "avg_compliance": config.avg_compliance,
            "active_frames": config.optimal_config.framework.active_frames(),
            "verix_strictness": config.optimal_config.prompt.verix_strictness.name,
        }

    def get_top_performing(self, n: int = 10) -> List[Dict[str, Any]]:
        """Get top N performing skills by success rate and compliance."""
        scored = []
        for key, config in self._skill_configs.items():
            if config.execution_count >= 3:  # Minimum executions
                score = config.success_rate() * 0.6 + config.avg_compliance * 0.4
                scored.append((score, key, config))

        scored.sort(reverse=True)

        return [
            {
                "key": key,
                "name": config.name,
                "type": config.execution_type.value,
                "score": score,
                "success_rate": config.success_rate(),
                "avg_compliance": config.avg_compliance,
                "executions": config.execution_count,
            }
            for score, key, config in scored[:n]
        ]


# Global tracker instance
_tracker: Optional[SkillExecutionTracker] = None


def get_tracker() -> SkillExecutionTracker:
    """Get or create global tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = SkillExecutionTracker()
        _tracker.setup_project()
    return _tracker


# Convenience functions for tracking
def track_skill_start(name: str, description: str = "", **params) -> str:
    """Start tracking a skill execution."""
    return get_tracker().start_execution(
        ExecutionType.SKILL, name, description, params
    )


def track_skill_end(execution_id: str, success: bool, output: str = "", error: str = None) -> None:
    """End tracking a skill execution."""
    get_tracker().end_execution(execution_id, success, output, error)


def track_command_start(name: str, description: str = "", **params) -> str:
    """Start tracking a command execution."""
    return get_tracker().start_execution(
        ExecutionType.COMMAND, name, description, params
    )


def track_command_end(execution_id: str, success: bool, output: str = "", error: str = None) -> None:
    """End tracking a command execution."""
    get_tracker().end_execution(execution_id, success, output, error)


def track_playbook_start(name: str, description: str = "", **params) -> str:
    """Start tracking a playbook execution."""
    return get_tracker().start_execution(
        ExecutionType.PLAYBOOK, name, description, params
    )


def track_playbook_end(execution_id: str, success: bool, output: str = "", error: str = None) -> None:
    """End tracking a playbook execution."""
    get_tracker().end_execution(execution_id, success, output, error)


# Example usage
if __name__ == "__main__":
    print("Skill Execution Tracker - Demo")
    print("=" * 50)

    tracker = get_tracker()

    # Simulate some skill executions
    test_skills = [
        ("intent-analyzer", True, "[assert|neutral] User wants to build API [conf:0.92]"),
        ("prompt-architect", True, "[assert|positive] Optimized prompt ready [conf:0.88]"),
        ("code-review-assistant", True, "[assert|neutral] No critical issues [conf:0.85]"),
        ("smart-bug-fix", False, "Error: Could not reproduce"),
        ("feature-dev-complete", True, "[commit|neutral] Feature implemented [conf:0.90]"),
    ]

    for name, success, output in test_skills:
        print(f"\nExecuting skill: {name}")
        exec_id = track_skill_start(name, f"Testing {name}")
        time.sleep(0.1)  # Simulate execution
        track_skill_end(exec_id, success, output)

        stats = tracker.get_skill_stats(ExecutionType.SKILL, name)
        if stats:
            print(f"  Success rate: {stats['success_rate']:.1%}")
            print(f"  VERIX compliance: {stats['avg_compliance']:.2f}")

    # Show overall stats
    print("\n--- Overall Stats ---")
    for key, value in tracker.stats().items():
        print(f"  {key}: {value}")

    # Show top performing
    print("\n--- Top Performing Skills ---")
    for skill in tracker.get_top_performing(5):
        print(f"  {skill['name']}: score={skill['score']:.2f}, "
              f"success={skill['success_rate']:.1%}, compliance={skill['avg_compliance']:.2f}")

    # Distill modes
    print("\n--- Distilled Modes ---")
    modes = tracker.distill_modes()
    for name, config in modes.items():
        print(f"  {name}: {config.summary()}")
