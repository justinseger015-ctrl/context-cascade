"""
LLM-based graders for subjective quality assessment.

Uses Claude (or other models via council) to evaluate responses
against rubrics for qualities that can't be measured deterministically.

Features:
- RubricGrader: Evaluate against multi-dimensional rubric
- Cross-model council: Claude + Gemini + Codex consensus
- Self-referential grading: Evaluate prompts about prompting
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Callable
from enum import Enum
import json
import os
import sys

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.config import FullConfig


class JudgeModel(Enum):
    """Available judge models for council."""
    CLAUDE = "claude"
    GEMINI = "gemini"
    CODEX = "codex"


@dataclass
class RubricCriterion:
    """A single criterion in a rubric."""

    name: str
    description: str
    weight: float = 1.0
    levels: Dict[int, str] = field(default_factory=dict)  # score -> description

    def __post_init__(self):
        if not self.levels:
            # Default 4-point scale
            self.levels = {
                0: f"No {self.name.lower()} present",
                1: f"Minimal {self.name.lower()}",
                2: f"Adequate {self.name.lower()}",
                3: f"Good {self.name.lower()}",
                4: f"Excellent {self.name.lower()}",
            }

    def to_prompt_text(self) -> str:
        """Convert to text for LLM prompt."""
        lines = [f"**{self.name}** (weight: {self.weight})"]
        lines.append(f"Description: {self.description}")
        lines.append("Scoring levels:")
        for score, desc in sorted(self.levels.items()):
            lines.append(f"  {score}: {desc}")
        return "\n".join(lines)


@dataclass
class JudgingResult:
    """Result of LLM judging."""

    score: float  # Normalized to [0.0, 1.0]
    criterion_scores: Dict[str, float]
    reasoning: str
    judge_model: str
    raw_response: str = ""
    confidence: float = 0.8

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "score": self.score,
            "criterion_scores": self.criterion_scores,
            "reasoning": self.reasoning,
            "judge_model": self.judge_model,
            "confidence": self.confidence,
        }


class RubricGrader:
    """
    Grade responses against a rubric using LLM judge.

    Supports single-model or council-based evaluation.
    """

    # Default rubric for cognitive architecture
    DEFAULT_CRITERIA = [
        RubricCriterion(
            name="Epistemic Clarity",
            description="Claims are clearly sourced with appropriate confidence levels",
            weight=1.5,
        ),
        RubricCriterion(
            name="Cognitive Frame Activation",
            description="Response uses cognitive frames appropriately for the task",
            weight=1.0,
        ),
        RubricCriterion(
            name="Task Completion",
            description="Response fully addresses the task requirements",
            weight=1.5,
        ),
        RubricCriterion(
            name="Coherence",
            description="Response is internally consistent and well-structured",
            weight=1.0,
        ),
    ]

    def __init__(
        self,
        criteria: Optional[List[RubricCriterion]] = None,
        use_council: bool = False,
        council_models: Optional[List[JudgeModel]] = None,
    ):
        """
        Initialize rubric grader.

        Args:
            criteria: List of rubric criteria (None = use defaults)
            use_council: Whether to use multi-model council
            council_models: Models for council (default: all three)
        """
        self.criteria = criteria or self.DEFAULT_CRITERIA
        self.use_council = use_council
        self.council_models = council_models or list(JudgeModel)

        # Normalize weights
        total_weight = sum(c.weight for c in self.criteria)
        for c in self.criteria:
            c.weight = c.weight / total_weight

    def grade(
        self,
        response: str,
        task: Dict[str, Any],
        expected: Optional[Any] = None,
    ) -> JudgingResult:
        """
        Grade a response using LLM judge.

        Args:
            response: Model's response to evaluate
            task: Original task definition
            expected: Expected output or criteria (optional)

        Returns:
            JudgingResult with scores and reasoning
        """
        if self.use_council:
            return self._grade_with_council(response, task, expected)
        else:
            return self._grade_single(response, task, expected, JudgeModel.CLAUDE)

    def _grade_single(
        self,
        response: str,
        task: Dict[str, Any],
        expected: Optional[Any],
        model: JudgeModel,
    ) -> JudgingResult:
        """Grade using a single model."""
        prompt = self._build_judge_prompt(response, task, expected)

        # For now, return mock result (real implementation would call API)
        # This allows testing without API calls
        return self._mock_judge(response, task, model)

    def _grade_with_council(
        self,
        response: str,
        task: Dict[str, Any],
        expected: Optional[Any],
    ) -> JudgingResult:
        """
        Grade using multi-model council.

        Aggregates scores from Claude, Gemini, and Codex for cross-model
        compatibility and bias reduction.
        """
        results = []

        for model in self.council_models:
            result = self._grade_single(response, task, expected, model)
            results.append(result)

        # Aggregate scores
        aggregated = self._aggregate_council_results(results)
        return aggregated

    def _aggregate_council_results(
        self,
        results: List[JudgingResult],
    ) -> JudgingResult:
        """Aggregate council results with consensus weighting."""
        if not results:
            return JudgingResult(
                score=0.0,
                criterion_scores={},
                reasoning="No council results",
                judge_model="council",
            )

        # Calculate mean scores
        n = len(results)
        mean_score = sum(r.score for r in results) / n

        # Aggregate criterion scores
        all_criteria = set()
        for r in results:
            all_criteria.update(r.criterion_scores.keys())

        criterion_scores = {}
        for criterion in all_criteria:
            scores = [r.criterion_scores.get(criterion, 0.0) for r in results]
            criterion_scores[criterion] = sum(scores) / len(scores)

        # Calculate confidence based on agreement
        score_variance = sum((r.score - mean_score) ** 2 for r in results) / n
        confidence = max(0.5, 1.0 - score_variance * 2)

        # Combine reasoning
        reasoning_parts = [f"[{r.judge_model}] {r.reasoning}" for r in results]
        combined_reasoning = "\n\n".join(reasoning_parts)

        return JudgingResult(
            score=mean_score,
            criterion_scores=criterion_scores,
            reasoning=combined_reasoning,
            judge_model="council",
            confidence=confidence,
        )

    def _build_judge_prompt(
        self,
        response: str,
        task: Dict[str, Any],
        expected: Optional[Any],
    ) -> str:
        """Build the prompt for the LLM judge."""
        rubric_text = "\n\n".join(c.to_prompt_text() for c in self.criteria)

        task_text = task.get("task", task.get("description", "Unknown task"))

        prompt = f"""You are an expert evaluator for AI responses. Evaluate the following response against the rubric.

## Task
{task_text}

## Response to Evaluate
{response}

{"## Expected Output" + chr(10) + str(expected) if expected else ""}

## Evaluation Rubric
{rubric_text}

## Instructions
1. Evaluate the response against each criterion
2. Assign a score (0-4) for each criterion
3. Provide brief reasoning for each score
4. Calculate the weighted final score

## Output Format (JSON)
{{
    "criterion_scores": {{
        "criterion_name": {{"score": N, "reasoning": "..."}},
        ...
    }},
    "overall_reasoning": "...",
    "final_score": N.N
}}
"""
        return prompt

    def _mock_judge(
        self,
        response: str,
        task: Dict[str, Any],
        model: JudgeModel,
    ) -> JudgingResult:
        """
        Mock judge for testing without API calls.

        Uses heuristics to simulate LLM judgment.
        """
        scores = {}

        # Heuristic scoring based on response characteristics
        for criterion in self.criteria:
            score = self._heuristic_score(response, criterion)
            scores[criterion.name] = score

        # Calculate weighted average
        weighted_sum = sum(
            scores[c.name] * c.weight
            for c in self.criteria
        )

        # Normalize to [0, 1]
        max_score = 4.0  # Maximum per criterion
        normalized = weighted_sum / max_score

        return JudgingResult(
            score=normalized,
            criterion_scores={k: v / max_score for k, v in scores.items()},
            reasoning=f"Mock judgment based on heuristics (model: {model.value})",
            judge_model=model.value,
            confidence=0.6,  # Lower confidence for mock
        )

    def _heuristic_score(
        self,
        response: str,
        criterion: RubricCriterion,
    ) -> float:
        """Heuristic scoring for a criterion."""
        response_lower = response.lower()

        if "clarity" in criterion.name.lower():
            # Check for epistemic markers
            markers = ["[witnessed]", "[inferred]", "[assumed]", "[ground:", "[conf:"]
            count = sum(1 for m in markers if m in response_lower)
            return min(4.0, count * 1.5)

        elif "frame" in criterion.name.lower():
            # Check for cognitive frame markers
            frames = ["[complete]", "[ongoing]", "[type:", "[path:"]
            count = sum(1 for f in frames if f in response_lower)
            return min(4.0, count * 1.2)

        elif "task" in criterion.name.lower() or "completion" in criterion.name.lower():
            # Length and structure heuristic
            score = 2.0  # Base score
            if len(response) > 200:
                score += 0.5
            if len(response) > 500:
                score += 0.5
            if "```" in response or "1." in response:
                score += 0.5
            return min(4.0, score)

        elif "coherence" in criterion.name.lower():
            # Structure heuristic
            score = 2.5  # Base score
            if "##" in response:
                score += 0.5
            if response.count("\n\n") > 2:
                score += 0.5
            return min(4.0, score)

        else:
            # Default: medium score
            return 2.5


def create_rubric(criteria_configs: List[Dict[str, Any]]) -> List[RubricCriterion]:
    """
    Create rubric criteria from configuration.

    Args:
        criteria_configs: List of criterion configurations

    Returns:
        List of RubricCriterion objects
    """
    criteria = []
    for config in criteria_configs:
        criterion = RubricCriterion(
            name=config["name"],
            description=config["description"],
            weight=config.get("weight", 1.0),
            levels=config.get("levels", {}),
        )
        criteria.append(criterion)
    return criteria


# Specialized rubrics for meta-loop optimization

META_PROMPT_RUBRIC = [
    RubricCriterion(
        name="Prompt Structure",
        description="Clear structure with system/user separation and examples",
        weight=1.5,
    ),
    RubricCriterion(
        name="Instruction Clarity",
        description="Instructions are unambiguous and actionable",
        weight=1.5,
    ),
    RubricCriterion(
        name="Self-Reference Coherence",
        description="Meta-prompts correctly reference prompt optimization",
        weight=1.0,
    ),
    RubricCriterion(
        name="Example Quality",
        description="Examples demonstrate the desired behavior clearly",
        weight=1.0,
    ),
]

SKILL_CREATION_RUBRIC = [
    RubricCriterion(
        name="Skill Definition",
        description="Clear definition of skill scope and capabilities",
        weight=1.5,
    ),
    RubricCriterion(
        name="Trigger Clarity",
        description="Clear conditions for when skill should activate",
        weight=1.0,
    ),
    RubricCriterion(
        name="Workflow Steps",
        description="Well-defined sequential or parallel steps",
        weight=1.5,
    ),
    RubricCriterion(
        name="Output Specification",
        description="Clear expected outputs and success criteria",
        weight=1.0,
    ),
]

AGENT_CREATION_RUBRIC = [
    RubricCriterion(
        name="Agent Persona",
        description="Clear role definition and expertise boundaries",
        weight=1.5,
    ),
    RubricCriterion(
        name="Tool Access",
        description="Appropriate tool access and constraints defined",
        weight=1.0,
    ),
    RubricCriterion(
        name="Coordination",
        description="Clear protocols for multi-agent coordination",
        weight=1.0,
    ),
    RubricCriterion(
        name="Evaluation Criteria",
        description="Success metrics for agent performance",
        weight=1.5,
    ),
]

AUDIT_RUBRIC = [
    RubricCriterion(
        name="Coverage",
        description="Audit covers all relevant aspects",
        weight=1.5,
    ),
    RubricCriterion(
        name="Finding Clarity",
        description="Issues are clearly described with evidence",
        weight=1.5,
    ),
    RubricCriterion(
        name="Actionability",
        description="Recommendations are specific and implementable",
        weight=1.0,
    ),
    RubricCriterion(
        name="Priority Ranking",
        description="Issues are prioritized by severity/impact",
        weight=1.0,
    ),
]


def create_meta_prompt_grader() -> RubricGrader:
    """Create grader for prompt optimization tasks."""
    return RubricGrader(criteria=META_PROMPT_RUBRIC)


def create_skill_grader() -> RubricGrader:
    """Create grader for skill creation tasks."""
    return RubricGrader(criteria=SKILL_CREATION_RUBRIC)


def create_agent_grader() -> RubricGrader:
    """Create grader for agent creation tasks."""
    return RubricGrader(criteria=AGENT_CREATION_RUBRIC)


def create_audit_grader() -> RubricGrader:
    """Create grader for audit tasks."""
    return RubricGrader(criteria=AUDIT_RUBRIC)


def create_council_grader(rubric_type: str = "default") -> RubricGrader:
    """
    Create a council-based grader for cross-model evaluation.

    Args:
        rubric_type: Type of rubric (default, prompt, skill, agent, audit)

    Returns:
        RubricGrader configured for council evaluation
    """
    rubrics = {
        "default": None,  # Use default criteria
        "prompt": META_PROMPT_RUBRIC,
        "skill": SKILL_CREATION_RUBRIC,
        "agent": AGENT_CREATION_RUBRIC,
        "audit": AUDIT_RUBRIC,
    }

    criteria = rubrics.get(rubric_type)

    return RubricGrader(
        criteria=criteria,
        use_council=True,
        council_models=[JudgeModel.CLAUDE, JudgeModel.GEMINI, JudgeModel.CODEX],
    )
