"""
Task Prompt Optimizer v3.0 - Optimize Claude Code's Task() calls to subagents.

This is the REAL runtime prompt optimization:
- Claude Code spawns agents via Task()
- Those Task() descriptions ARE prompts
- This optimizer applies VERIX/VERILINGUA/GlobalMOO to those prompts

The optimization loop:
1. Receive task description + agent type
2. Apply config vector (frame activation, VERIX requirements)
3. Build optimized prompt using PromptBuilder patterns
4. Track agent success/failure
5. Report outcomes to GlobalMOO
6. Learn better config vectors over time

v3.0: Uses x- prefixed custom fields for Anthropic compliance
"""

import os
import sys
import json
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from enum import Enum

# Add parent for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, FrameworkConfig, PromptConfig, VerixStrictness
from core.prompt_builder import PromptBuilder
from core.verix import VerixParser, VerixValidator
from optimization.globalmoo_client import (
    GlobalMOOClient, OptimizationOutcome, ParetoPoint,
    create_cognitive_project, Objective, ObjectiveDirection
)
from optimization.dspy_level2 import DSPyLevel2Optimizer, CompiledPrompt


class AgentCategory(Enum):
    """Agent categories with optimal frame configurations."""
    DELIVERY = "delivery"
    QUALITY = "quality"
    RESEARCH = "research"
    ORCHESTRATION = "orchestration"
    SECURITY = "security"
    PLATFORMS = "platforms"
    SPECIALISTS = "specialists"
    TOOLING = "tooling"
    FOUNDRY = "foundry"
    OPERATIONS = "operations"


# Optimal frame configurations per agent category
CATEGORY_FRAME_CONFIGS = {
    AgentCategory.DELIVERY: FrameworkConfig(
        evidential=True,   # Need to track evidence for deliverables
        aspectual=True,    # Track completion status
        morphological=False,
        compositional=True,  # Build complex from simple
        honorific=False,
        classifier=False,
        spatial=False,
    ),
    AgentCategory.QUALITY: FrameworkConfig(
        evidential=True,   # Critical for audit trails
        aspectual=True,    # Track ongoing vs complete
        morphological=True,  # Semantic decomposition
        compositional=False,
        honorific=False,
        classifier=True,   # Categorize issues
        spatial=False,
    ),
    AgentCategory.RESEARCH: FrameworkConfig(
        evidential=True,   # Source verification essential
        aspectual=True,    # Track research progress
        morphological=True,  # Deep semantic analysis
        compositional=True,  # Build theories from parts
        honorific=False,
        classifier=True,   # Categorize findings
        spatial=False,
    ),
    AgentCategory.ORCHESTRATION: FrameworkConfig(
        evidential=True,
        aspectual=True,    # Track task states
        morphological=False,
        compositional=True,  # Compose workflows
        honorific=True,    # Calibrate to audiences
        classifier=False,
        spatial=True,      # Navigate task space
    ),
    AgentCategory.SECURITY: FrameworkConfig(
        evidential=True,   # Evidence for vulnerabilities
        aspectual=True,
        morphological=True,
        compositional=False,
        honorific=False,
        classifier=True,   # Categorize threats
        spatial=True,      # Map attack surfaces
    ),
    # Default for others
    AgentCategory.PLATFORMS: FrameworkConfig(evidential=True, aspectual=True),
    AgentCategory.SPECIALISTS: FrameworkConfig(evidential=True, aspectual=True),
    AgentCategory.TOOLING: FrameworkConfig(evidential=True, aspectual=True),
    AgentCategory.FOUNDRY: FrameworkConfig(evidential=True, aspectual=True, compositional=True),
    AgentCategory.OPERATIONS: FrameworkConfig(evidential=True, aspectual=True),
}


@dataclass
class TaskResult:
    """Result from a Task() execution."""
    task_id: str
    agent_type: str
    success: bool
    output: str = ""
    error: Optional[str] = None
    iterations: int = 1
    duration_ms: float = 0.0
    verix_claims_found: int = 0
    verix_compliance: float = 0.0
    timestamp: float = field(default_factory=time.time)

    def to_outcome_metrics(self) -> Dict[str, float]:
        """Convert to GlobalMOO outcome metrics."""
        return {
            "task_accuracy": 1.0 if self.success else 0.0,
            "token_efficiency": max(0.0, 1.0 - (len(self.output) / 10000)),  # Normalize
            "edge_robustness": 1.0 / max(1, self.iterations),  # Fewer iterations = more robust
            "epistemic_consistency": self.verix_compliance,
        }


@dataclass
class OptimizedTaskPrompt:
    """An optimized task prompt with metadata."""
    original_description: str
    optimized_prompt: str
    agent_type: str
    config_vector: List[float]
    cluster_key: str
    frame_activations: List[str]
    verix_requirements: str
    compiled_at: float = field(default_factory=time.time)


class TaskPromptOptimizer:
    """
    Optimize Task() prompts using VERIX/VERILINGUA/GlobalMOO.

    This wraps the agent spawning process to:
    1. Apply optimal frame configurations based on agent type
    2. Add VERIX requirements to task descriptions
    3. Cache optimized prompts per cluster
    4. Track agent success/failure for GlobalMOO feedback
    """

    def __init__(
        self,
        storage_dir: Optional[Path] = None,
        use_mock_moo: bool = True,
    ):
        """
        Initialize optimizer.

        Args:
            storage_dir: Directory for caching and results
            use_mock_moo: Use mock GlobalMOO (local Pareto optimization)
        """
        if storage_dir is None:
            storage_dir = Path(__file__).parent.parent / "storage" / "task_optimizer"

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.moo = GlobalMOOClient(use_mock=use_mock_moo)
        self.l2_cache = DSPyLevel2Optimizer(
            cache_dir=self.storage_dir / "prompt_cache"
        )
        self.verix_parser = VerixParser(PromptConfig())
        self.verix_validator = VerixValidator(PromptConfig())

        # Results storage
        self.results_file = self.storage_dir / "task_results.jsonl"
        self.pareto_file = self.storage_dir / "pareto_frontier.json"

        # Project setup
        self._project_id: Optional[str] = None
        self._model_id: Optional[str] = None

        # Agent type to category mapping (will be populated)
        self._agent_category_map: Dict[str, AgentCategory] = {}

    def setup_project(self, name: str = "task-prompt-optimizer") -> str:
        """Setup GlobalMOO project for optimization."""
        self._model_id = self.moo.create_model(
            name=f"{name}-model",
            description="Optimize Claude Code Task() prompts with VERIX/VERILINGUA",
            input_dimensions=VectorCodec.VECTOR_SIZE,
        )

        self._project_id = self.moo.create_project(
            model_id=self._model_id,
            name=name,
            objectives=[
                Objective("task_accuracy", ObjectiveDirection.MAXIMIZE, threshold=0.95),
                Objective("token_efficiency", ObjectiveDirection.MAXIMIZE),
                Objective("edge_robustness", ObjectiveDirection.MAXIMIZE),
                Objective("epistemic_consistency", ObjectiveDirection.MAXIMIZE),
            ],
        )

        return self._project_id

    def get_agent_category(self, agent_type: str) -> AgentCategory:
        """
        Determine agent category from type.

        Maps agent types like 'backend-dev', 'researcher', etc. to categories.
        """
        # Check cache first
        if agent_type in self._agent_category_map:
            return self._agent_category_map[agent_type]

        # Infer from agent type name
        agent_lower = agent_type.lower()

        category_keywords = {
            AgentCategory.DELIVERY: ['dev', 'coder', 'backend', 'frontend', 'mobile', 'api'],
            AgentCategory.QUALITY: ['test', 'review', 'audit', 'validator', 'analyzer'],
            AgentCategory.RESEARCH: ['research', 'analyst', 'investigat', 'synthesis'],
            AgentCategory.ORCHESTRATION: ['orchestrat', 'coordinat', 'swarm', 'hive'],
            AgentCategory.SECURITY: ['security', 'pentest', 'vuln', 'compliance'],
            AgentCategory.PLATFORMS: ['cloud', 'kubernetes', 'docker', 'infra'],
            AgentCategory.SPECIALISTS: ['specialist', 'expert', 'ml', 'data'],
            AgentCategory.TOOLING: ['tool', 'cli', 'script'],
            AgentCategory.FOUNDRY: ['foundry', 'creator', 'forge'],
            AgentCategory.OPERATIONS: ['ops', 'deploy', 'monitor'],
        }

        for category, keywords in category_keywords.items():
            if any(kw in agent_lower for kw in keywords):
                self._agent_category_map[agent_type] = category
                return category

        # Default to delivery
        self._agent_category_map[agent_type] = AgentCategory.DELIVERY
        return AgentCategory.DELIVERY

    def get_optimal_config(self, agent_type: str, task_type: str = "default") -> FullConfig:
        """
        Get optimal configuration for agent type.

        Uses GlobalMOO suggestions if available, otherwise defaults.
        """
        category = self.get_agent_category(agent_type)
        framework = CATEGORY_FRAME_CONFIGS.get(
            category,
            FrameworkConfig(evidential=True, aspectual=True)
        )

        # Try to get GlobalMOO suggestion
        if self._project_id and self.moo._mock_cases:
            try:
                target = {
                    "task_accuracy": 0.95,
                    "token_efficiency": 0.8,
                    "edge_robustness": 0.9,
                    "epistemic_consistency": 0.85,
                }
                suggestions = self.moo.suggest_inverse(self._project_id, target, num_suggestions=1)
                if suggestions:
                    return VectorCodec.decode(suggestions[0])
            except Exception:
                pass

        # Default config with category-specific frames
        return FullConfig(
            framework=framework,
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.MODERATE,
                require_ground=True,
                require_confidence=True,
            ),
        )

    def optimize_task_prompt(
        self,
        description: str,
        agent_type: str,
        task_type: str = "default",
    ) -> OptimizedTaskPrompt:
        """
        Optimize a task description for an agent.

        Applies VERIX requirements and frame activation.

        Args:
            description: Original task description
            agent_type: Type of agent (e.g., 'backend-dev', 'researcher')
            task_type: Category of task

        Returns:
            OptimizedTaskPrompt with enhanced description
        """
        # Get optimal config for this agent
        config = self.get_optimal_config(agent_type, task_type)

        # Build prompt using PromptBuilder
        builder = PromptBuilder(config)
        system_prompt, user_prompt = builder.build(description, task_type)

        # Extract frame activations
        active_frames = config.framework.active_frames()

        # Build VERIX requirement block
        verix_block = self._build_verix_requirements(config)

        # Compose optimized prompt
        optimized = self._compose_optimized_prompt(
            description=description,
            agent_type=agent_type,
            active_frames=active_frames,
            verix_requirements=verix_block,
        )

        return OptimizedTaskPrompt(
            original_description=description,
            optimized_prompt=optimized,
            agent_type=agent_type,
            config_vector=VectorCodec.encode(config),
            cluster_key=builder.cluster_key(),
            frame_activations=active_frames,
            verix_requirements=verix_block,
        )

    def _build_verix_requirements(self, config: FullConfig) -> str:
        """Build VERIX requirements block for task prompt."""
        strictness = config.prompt.verix_strictness

        if strictness == VerixStrictness.STRICT:
            return """
## VERIX Requirements (STRICT)
Format ALL claims as: [illocution|affect] content [ground:source] [conf:N.NN] [state:status]
- Mark evidence sources explicitly
- Include confidence values for all assertions
- Track claim states (provisional/confirmed/retracted)
"""
        elif strictness == VerixStrictness.MODERATE:
            return """
## VERIX Requirements (MODERATE)
Format key claims as: [illocution|affect] content [conf:N.NN]
- Use assert/query/commit illocutions appropriately
- Include confidence for uncertain claims
- Ground important assertions with evidence
"""
        else:
            return """
## VERIX Requirements (RELAXED)
Mark uncertain claims with confidence when relevant.
Use epistemic markers for key assertions.
"""

    def _compose_optimized_prompt(
        self,
        description: str,
        agent_type: str,
        active_frames: List[str],
        verix_requirements: str,
    ) -> str:
        """Compose the optimized task prompt."""
        # Build frame activation section
        frame_section = ""
        if active_frames:
            frame_activations = []

            if "evidential" in active_frames:
                frame_activations.append(
                    "- **Evidential Frame**: Track how you know each fact "
                    "(witnessed/reported/inferred/assumed)"
                )
            if "aspectual" in active_frames:
                frame_activations.append(
                    "- **Aspectual Frame**: Mark task states as complete vs ongoing"
                )
            if "morphological" in active_frames:
                frame_activations.append(
                    "- **Morphological Frame**: Decompose complex concepts semantically"
                )
            if "compositional" in active_frames:
                frame_activations.append(
                    "- **Compositional Frame**: Build complex solutions from primitives"
                )
            if "honorific" in active_frames:
                frame_activations.append(
                    "- **Honorific Frame**: Calibrate response to audience expertise"
                )
            if "classifier" in active_frames:
                frame_activations.append(
                    "- **Classifier Frame**: Categorize and compare entities systematically"
                )
            if "spatial" in active_frames:
                frame_activations.append(
                    "- **Spatial Frame**: Use absolute positioning in problem space"
                )

            if frame_activations:
                frame_section = "## Cognitive Frames Active\n" + "\n".join(frame_activations) + "\n"

        # Compose full prompt
        return f"""# Task for {agent_type}

{frame_section}
{verix_requirements}

## Task Description

{description}

---
Apply all active cognitive frames and VERIX notation in your response.
Mark completion status and confidence levels for key deliverables.
"""

    def record_result(self, result: TaskResult) -> None:
        """
        Record task result for learning.

        Updates GlobalMOO with outcome metrics.

        v3.0: Uses x- prefixed custom fields for Anthropic compliance.
        """
        # Save to results file (v3.0 format with x- prefixed custom fields)
        with open(self.results_file, "a") as f:
            f.write(json.dumps({
                "task_id": result.task_id,
                "x-agent-type": result.agent_type,
                "success": result.success,
                "iterations": result.iterations,
                "duration_ms": result.duration_ms,
                "x-verix-compliance": result.verix_compliance,
                "timestamp": result.timestamp,
                "_schema_version": "3.0",
            }) + "\n")

        # Report to GlobalMOO if project exists
        if self._project_id:
            # Get the config vector used for this task
            config = self.get_optimal_config(result.agent_type)
            config_vector = VectorCodec.encode(config)

            outcome = OptimizationOutcome(
                config_vector=config_vector,
                outcomes=result.to_outcome_metrics(),
                metadata={
                    "x-agent-type": result.agent_type,
                    "x-task-id": result.task_id,
                    "_schema_version": "3.0",
                },
            )

            self.moo.report_outcome(self._project_id, outcome)

    def analyze_output(self, output: str) -> Tuple[int, float]:
        """
        Analyze agent output for VERIX compliance.

        Returns:
            (claims_found, compliance_score)
        """
        claims = self.verix_parser.parse(output)
        if not claims:
            return 0, 0.0

        compliance = self.verix_validator.compliance_score(claims)
        return len(claims), compliance

    def get_pareto_frontier(self) -> List[ParetoPoint]:
        """Get current Pareto frontier of optimal configurations."""
        if self._project_id:
            return self.moo.get_pareto_frontier(self._project_id)
        return []

    def distill_named_modes(self) -> Dict[str, FullConfig]:
        """
        Distill Pareto frontier into named modes.

        Creates practical modes like:
        - Audit: High epistemic consistency, strict VERIX
        - Speed: High token efficiency, relaxed VERIX
        - Research: All frames active, comprehensive
        - Standard: Balanced defaults
        """
        pareto = self.get_pareto_frontier()

        modes = {}

        if not pareto:
            # Default modes when no Pareto data
            modes["standard"] = FullConfig()
            modes["audit"] = FullConfig(
                framework=FrameworkConfig(evidential=True, aspectual=True, morphological=True),
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
            return modes

        # Find optimal points for each objective
        # Audit: max epistemic_consistency
        audit_point = max(pareto, key=lambda p: p.outcomes.get("epistemic_consistency", 0))
        modes["audit"] = audit_point.to_config()

        # Speed: max token_efficiency
        speed_point = max(pareto, key=lambda p: p.outcomes.get("token_efficiency", 0))
        modes["speed"] = speed_point.to_config()

        # Research: balanced with high accuracy
        research_point = max(pareto, key=lambda p: (
            p.outcomes.get("task_accuracy", 0) * 0.4 +
            p.outcomes.get("epistemic_consistency", 0) * 0.4 +
            p.outcomes.get("edge_robustness", 0) * 0.2
        ))
        modes["research"] = research_point.to_config()

        # Standard: most balanced
        standard_point = max(pareto, key=lambda p: sum(p.outcomes.values()) / len(p.outcomes))
        modes["standard"] = standard_point.to_config()

        return modes

    def save_modes(self, modes: Dict[str, FullConfig]) -> Path:
        """Save distilled modes to file."""
        modes_file = self.storage_dir / "named_modes.json"

        modes_data = {}
        for name, config in modes.items():
            modes_data[name] = {
                "config_vector": VectorCodec.encode(config),
                "cluster_key": VectorCodec.cluster_key(config),
                "summary": config.summary(),
                "active_frames": config.framework.active_frames(),
                "verix_strictness": config.prompt.verix_strictness.name,
            }

        with open(modes_file, "w") as f:
            json.dump(modes_data, f, indent=2)

        return modes_file

    def stats(self) -> Dict[str, Any]:
        """Get optimizer statistics."""
        results_count = 0
        success_count = 0

        if self.results_file.exists():
            with open(self.results_file) as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        results_count += 1
                        if data.get("success"):
                            success_count += 1
                    except:
                        pass

        return {
            "results_tracked": results_count,
            "success_rate": success_count / results_count if results_count > 0 else 0.0,
            "pareto_points": len(self.get_pareto_frontier()),
            "cache_stats": self.l2_cache.stats(),
            "project_id": self._project_id,
        }


# Factory function
def create_task_optimizer(
    storage_dir: Optional[Path] = None,
    use_mock_moo: bool = True,
) -> TaskPromptOptimizer:
    """Create and setup task prompt optimizer."""
    optimizer = TaskPromptOptimizer(
        storage_dir=storage_dir,
        use_mock_moo=use_mock_moo,
    )
    optimizer.setup_project()
    return optimizer


# Example usage and testing
if __name__ == "__main__":
    print("Task Prompt Optimizer - Demo")
    print("=" * 50)

    # Create optimizer
    optimizer = create_task_optimizer()
    print(f"Project ID: {optimizer._project_id}")

    # Test task optimization
    test_tasks = [
        ("backend-dev", "Build a REST API for user authentication with JWT tokens"),
        ("researcher", "Investigate best practices for error handling in async Python"),
        ("code-analyzer", "Audit the authentication module for security vulnerabilities"),
        ("orchestrator", "Coordinate a parallel implementation of the new feature"),
    ]

    for agent_type, description in test_tasks:
        print(f"\n--- Optimizing for {agent_type} ---")
        optimized = optimizer.optimize_task_prompt(description, agent_type)
        print(f"Cluster Key: {optimized.cluster_key}")
        print(f"Active Frames: {optimized.frame_activations}")
        print(f"Optimized Prompt Preview:")
        print(optimized.optimized_prompt[:500] + "...")

        # Simulate result
        result = TaskResult(
            task_id=f"test-{agent_type}",
            agent_type=agent_type,
            success=True,
            output="[assert|neutral] Task completed successfully [conf:0.9]",
            verix_claims_found=1,
            verix_compliance=0.85,
        )
        optimizer.record_result(result)

    # Distill modes
    print("\n--- Distilling Named Modes ---")
    modes = optimizer.distill_named_modes()
    for name, config in modes.items():
        print(f"  {name}: {config.summary()}")

    modes_file = optimizer.save_modes(modes)
    print(f"\nModes saved to: {modes_file}")

    # Stats
    print("\n--- Stats ---")
    stats = optimizer.stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
