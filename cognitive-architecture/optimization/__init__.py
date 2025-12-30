"""
Optimization module for cognitive architecture.

Provides GlobalMOO integration, DSPy prompt optimization,
and Three-MOO cascade orchestration for multi-objective
prompt configuration optimization.

TWO-LAYER ARCHITECTURE:
- Layer 1 (Language Evolution): Optimizes VERIX/VERILINGUA patterns themselves
- Layer 2 (Prompt Expression): Optimizes how language is used in prompts

Components:
- globalmoo_client: GlobalMOO API wrapper
- dspy_level2: Per-cluster prompt caching (minutes/hours)
- dspy_level1: Monthly structural evolution
- cascade: Three-phase MOO orchestration
- distill_modes: Pareto frontier -> named modes

RUNTIME OPTIMIZATION (NEW):
- task_prompt_optimizer: Optimize Task() prompts for subagents
- skill_execution_tracker: Track skill/command/playbook executions
- language_evolution: Layer 1 - evolve language patterns
- cascade_optimizer: Full Context Cascade optimization
"""

from .globalmoo_client import (
    GlobalMOOClient,
    OptimizationOutcome,
    OptimizationProject,
    ParetoPoint,
)
from .dspy_level2 import (
    DSPyLevel2Optimizer,
    ClusterCache,
    CompiledPrompt,
)
from .dspy_level1 import (
    DSPyLevel1Analyzer,
    EvolutionProposal,
    TelemetryAggregator,
)
from .cascade import (
    ThreeMOOCascade,
    CascadePhase,
    CascadeResult,
)
from .distill_modes import (
    ModeDistiller,
    NamedMode,
    ModeLibrary,
)

# Runtime optimization (new)
from .task_prompt_optimizer import (
    TaskPromptOptimizer,
    TaskResult,
    OptimizedTaskPrompt,
    create_task_optimizer,
)
from .skill_execution_tracker import (
    SkillExecutionTracker,
    ExecutionType,
    ExecutionRecord,
    get_tracker,
    track_skill_start,
    track_skill_end,
    track_command_start,
    track_command_end,
    track_playbook_start,
    track_playbook_end,
)
from .language_evolution import (
    LanguageEvolutionOptimizer,
    LanguagePattern,
    LanguageEvolutionState,
    create_language_evolver,
)
from .cascade_optimizer import (
    CascadeOptimizer,
    CascadeLevel,
    CascadeLevelStats,
    OptimizationCycleResult,
    get_cascade_optimizer,
    track_cascade_start,
    track_cascade_end,
    optimize_cascade_prompt,
)

# Phase D: Two-Stage Optimizer and Holdout Validation
from .two_stage_optimizer import (
    TwoStageOptimizer,
    CognitiveOptProblem,
)
from .holdout_validator import (
    HoldoutValidator,
    ValidationResult,
    ValidationHistory,
    create_holdout_validator,
)

__all__ = [
    # GlobalMOO
    "GlobalMOOClient",
    "OptimizationOutcome",
    "OptimizationProject",
    "ParetoPoint",
    # DSPy L2
    "DSPyLevel2Optimizer",
    "ClusterCache",
    "CompiledPrompt",
    # DSPy L1
    "DSPyLevel1Analyzer",
    "EvolutionProposal",
    "TelemetryAggregator",
    # Cascade
    "ThreeMOOCascade",
    "CascadePhase",
    "CascadeResult",
    # Modes
    "ModeDistiller",
    "NamedMode",
    "ModeLibrary",
    # Task Prompt Optimizer
    "TaskPromptOptimizer",
    "TaskResult",
    "OptimizedTaskPrompt",
    "create_task_optimizer",
    # Skill Execution Tracker
    "SkillExecutionTracker",
    "ExecutionType",
    "ExecutionRecord",
    "get_tracker",
    "track_skill_start",
    "track_skill_end",
    "track_command_start",
    "track_command_end",
    "track_playbook_start",
    "track_playbook_end",
    # Language Evolution
    "LanguageEvolutionOptimizer",
    "LanguagePattern",
    "LanguageEvolutionState",
    "create_language_evolver",
    # Cascade Optimizer
    "CascadeOptimizer",
    "CascadeLevel",
    "CascadeLevelStats",
    "OptimizationCycleResult",
    "get_cascade_optimizer",
    "track_cascade_start",
    "track_cascade_end",
    "optimize_cascade_prompt",
    # Two-Stage Optimizer
    "TwoStageOptimizer",
    "CognitiveOptProblem",
    # Holdout Validator
    "HoldoutValidator",
    "ValidationResult",
    "ValidationHistory",
    "create_holdout_validator",
]
