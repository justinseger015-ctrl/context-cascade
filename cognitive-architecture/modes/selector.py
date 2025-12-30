"""
Automatic mode selection based on task characteristics.

Analyzes task context to recommend the most appropriate mode.
"""

import os
import sys
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modes.library import Mode, ModeLibrary, ModeType, BUILTIN_MODES


class TaskDomain(Enum):
    """Domain categories for tasks."""
    CODING = "coding"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    SUPPORT = "support"
    SECURITY = "security"
    DOCUMENTATION = "documentation"
    GENERAL = "general"


class TaskComplexity(Enum):
    """Complexity levels for tasks."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"


class ConstraintType(Enum):
    """Types of constraints on task execution."""
    SPEED = "speed"
    ACCURACY = "accuracy"
    COST = "cost"
    SAFETY = "safety"


@dataclass
class TaskContext:
    """Context for a task to inform mode selection."""

    task_description: str
    domain: Optional[TaskDomain] = None
    complexity: Optional[TaskComplexity] = None
    constraints: List[ConstraintType] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_task(cls, task: str, **kwargs) -> "TaskContext":
        """Create context from task description."""
        context = cls(task_description=task, **kwargs)
        context._infer_from_description()
        return context

    def _infer_from_description(self) -> None:
        """Infer domain and complexity from description."""
        desc_lower = self.task_description.lower()

        # Infer domain
        if self.domain is None:
            self.domain = self._infer_domain(desc_lower)

        # Infer complexity
        if self.complexity is None:
            self.complexity = self._infer_complexity(desc_lower)

        # Infer constraints
        if not self.constraints:
            self.constraints = self._infer_constraints(desc_lower)

    def _infer_domain(self, desc: str) -> TaskDomain:
        """Infer domain from description."""
        domain_keywords = {
            TaskDomain.CODING: [
                "code", "function", "class", "api", "debug", "implement",
                "program", "script", "variable", "syntax", "compile"
            ],
            TaskDomain.RESEARCH: [
                "research", "study", "paper", "literature", "hypothesis",
                "experiment", "data", "analysis", "finding", "methodology"
            ],
            TaskDomain.ANALYSIS: [
                "analyze", "review", "audit", "examine", "evaluate",
                "assess", "investigate", "diagnose", "inspect"
            ],
            TaskDomain.CREATIVE: [
                "write", "create", "design", "generate", "compose",
                "story", "content", "creative", "novel", "imagine"
            ],
            TaskDomain.SUPPORT: [
                "help", "support", "assist", "explain", "clarify",
                "how to", "what is", "question", "answer"
            ],
            TaskDomain.SECURITY: [
                "security", "vulnerability", "threat", "attack", "protect",
                "encrypt", "auth", "permission", "access", "compliance"
            ],
            TaskDomain.DOCUMENTATION: [
                "document", "readme", "guide", "manual", "specification",
                "api doc", "reference", "tutorial"
            ],
        }

        for domain, keywords in domain_keywords.items():
            if any(kw in desc for kw in keywords):
                return domain

        return TaskDomain.GENERAL

    def _infer_complexity(self, desc: str) -> TaskComplexity:
        """Infer complexity from description."""
        # Simple indicators
        simple_patterns = [
            r"simple", r"quick", r"basic", r"just", r"only",
            r"single", r"one", r"brief"
        ]
        if any(re.search(p, desc) for p in simple_patterns):
            return TaskComplexity.SIMPLE

        # Complex indicators
        complex_patterns = [
            r"complex", r"comprehensive", r"detailed", r"thorough",
            r"multi", r"all", r"every", r"complete", r"full"
        ]
        if any(re.search(p, desc) for p in complex_patterns):
            return TaskComplexity.COMPLEX

        # Default to moderate
        return TaskComplexity.MODERATE

    def _infer_constraints(self, desc: str) -> List[ConstraintType]:
        """Infer constraints from description."""
        constraints = []

        if any(w in desc for w in ["fast", "quick", "immediately", "urgent", "asap"]):
            constraints.append(ConstraintType.SPEED)

        if any(w in desc for w in ["accurate", "precise", "correct", "exact", "rigorous"]):
            constraints.append(ConstraintType.ACCURACY)

        if any(w in desc for w in ["cheap", "efficient", "minimal", "budget", "cost"]):
            constraints.append(ConstraintType.COST)

        if any(w in desc for w in ["safe", "secure", "careful", "sensitive", "compliant"]):
            constraints.append(ConstraintType.SAFETY)

        return constraints


@dataclass
class ModeRecommendation:
    """A mode recommendation with score and reasoning."""

    mode: Mode
    score: float  # 0.0 - 1.0
    reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mode_name": self.mode.name,
            "score": self.score,
            "reasons": self.reasons,
        }


class ModeSelector:
    """Select optimal mode based on task context."""

    # Mapping from domain to preferred mode types
    DOMAIN_MODE_AFFINITY: Dict[TaskDomain, List[ModeType]] = {
        TaskDomain.CODING: [ModeType.BALANCED, ModeType.ROBUST],
        TaskDomain.RESEARCH: [ModeType.STRICT, ModeType.BALANCED],
        TaskDomain.ANALYSIS: [ModeType.STRICT, ModeType.BALANCED],
        TaskDomain.CREATIVE: [ModeType.BALANCED, ModeType.MINIMAL],
        TaskDomain.SUPPORT: [ModeType.BALANCED, ModeType.EFFICIENT],
        TaskDomain.SECURITY: [ModeType.STRICT, ModeType.ROBUST],
        TaskDomain.DOCUMENTATION: [ModeType.BALANCED, ModeType.EFFICIENT],
        TaskDomain.GENERAL: [ModeType.BALANCED],
    }

    # Mapping from constraints to preferred mode types
    CONSTRAINT_MODE_AFFINITY: Dict[ConstraintType, List[ModeType]] = {
        ConstraintType.SPEED: [ModeType.EFFICIENT, ModeType.MINIMAL],
        ConstraintType.ACCURACY: [ModeType.STRICT, ModeType.BALANCED],
        ConstraintType.COST: [ModeType.EFFICIENT, ModeType.MINIMAL],
        ConstraintType.SAFETY: [ModeType.ROBUST, ModeType.STRICT],
    }

    # Complexity adjustments
    COMPLEXITY_ADJUSTMENTS: Dict[TaskComplexity, Dict[ModeType, float]] = {
        TaskComplexity.SIMPLE: {
            ModeType.MINIMAL: 0.2,
            ModeType.EFFICIENT: 0.1,
            ModeType.STRICT: -0.2,
        },
        TaskComplexity.MODERATE: {
            ModeType.BALANCED: 0.1,
        },
        TaskComplexity.COMPLEX: {
            ModeType.STRICT: 0.2,
            ModeType.BALANCED: 0.1,
            ModeType.MINIMAL: -0.2,
        },
    }

    def __init__(self, library: Optional[ModeLibrary] = None):
        """
        Initialize selector.

        Args:
            library: Mode library to select from
        """
        self.library = library or ModeLibrary()

    def select(self, context: TaskContext) -> Mode:
        """
        Select best mode for context.

        Args:
            context: Task context

        Returns:
            Selected mode
        """
        recommendations = self.recommend(context, top_k=1)
        if recommendations:
            return recommendations[0].mode

        # Fallback to balanced
        return self.library.get("balanced") or list(BUILTIN_MODES.values())[0]

    def recommend(
        self,
        context: TaskContext,
        top_k: int = 3,
    ) -> List[ModeRecommendation]:
        """
        Get top-k mode recommendations for context.

        Args:
            context: Task context
            top_k: Number of recommendations to return

        Returns:
            List of recommendations sorted by score
        """
        recommendations = []

        for mode in self.library._modes.values():
            score, reasons = self._score_mode(mode, context)
            recommendations.append(ModeRecommendation(
                mode=mode,
                score=score,
                reasons=reasons,
            ))

        # Sort by score descending
        recommendations.sort(key=lambda r: r.score, reverse=True)

        return recommendations[:top_k]

    def _score_mode(
        self,
        mode: Mode,
        context: TaskContext,
    ) -> Tuple[float, List[str]]:
        """Score a mode for the given context."""
        score = 0.5  # Base score
        reasons = []

        # Domain affinity
        if context.domain:
            preferred = self.DOMAIN_MODE_AFFINITY.get(context.domain, [])
            if mode.mode_type in preferred:
                bonus = 0.2 if mode.mode_type == preferred[0] else 0.1
                score += bonus
                reasons.append(f"Good fit for {context.domain.value} domain")

        # Constraint affinity
        for constraint in context.constraints:
            preferred = self.CONSTRAINT_MODE_AFFINITY.get(constraint, [])
            if mode.mode_type in preferred:
                bonus = 0.15 if mode.mode_type == preferred[0] else 0.08
                score += bonus
                reasons.append(f"Satisfies {constraint.value} constraint")

        # Complexity adjustment
        if context.complexity:
            adjustments = self.COMPLEXITY_ADJUSTMENTS.get(context.complexity, {})
            adjustment = adjustments.get(mode.mode_type, 0.0)
            score += adjustment
            if adjustment > 0:
                reasons.append(f"Appropriate for {context.complexity.value} tasks")

        # Tag matching
        for tag in context.tags:
            if tag.lower() in [t.lower() for t in mode.tags]:
                score += 0.1
                reasons.append(f"Matches tag: {tag}")

        # Clamp score
        score = max(0.0, min(1.0, score))

        return score, reasons


# Convenience functions

_default_selector = ModeSelector()


def select_mode(task: str, **kwargs) -> Mode:
    """
    Select mode for a task description.

    Args:
        task: Task description
        **kwargs: Additional context parameters

    Returns:
        Selected mode
    """
    context = TaskContext.from_task(task, **kwargs)
    return _default_selector.select(context)


def recommend_modes(task: str, top_k: int = 3, **kwargs) -> List[ModeRecommendation]:
    """
    Get mode recommendations for a task.

    Args:
        task: Task description
        top_k: Number of recommendations
        **kwargs: Additional context parameters

    Returns:
        List of recommendations
    """
    context = TaskContext.from_task(task, **kwargs)
    return _default_selector.recommend(context, top_k)
