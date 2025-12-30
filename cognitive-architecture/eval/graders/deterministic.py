"""
Deterministic graders - 100% reproducible scoring.

Graders:
- FormatGrader: Check output format compliance
- TokenGrader: Count and score token usage
- LatencyGrader: Measure response time
- RegexGrader: Pattern matching for expected outputs
- CompositeGrader: Combine multiple graders

All graders return scores in [0.0, 1.0] range.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Callable
import re
import time


class Grader(ABC):
    """Base class for all graders."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return grader name."""
        pass

    @abstractmethod
    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """
        Grade a response.

        Args:
            response: Model's response text
            expected: Expected output or criteria
            metadata: Additional context (tokens, latency, etc.)

        Returns:
            Score in [0.0, 1.0]
        """
        pass

    def grade_with_details(
        self,
        response: str,
        expected: Any,
        metadata: Dict,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Grade with detailed breakdown.

        Returns:
            (score, details) tuple
        """
        score = self.grade(response, expected, metadata)
        return score, {"grader": self.name, "score": score}


class FormatGrader(Grader):
    """Grade format compliance."""

    def __init__(
        self,
        required_sections: Optional[List[str]] = None,
        required_markers: Optional[List[str]] = None,
        case_sensitive: bool = False,
    ):
        """
        Initialize format grader.

        Args:
            required_sections: Section headers that must be present
            required_markers: Markers/tags that must be present (e.g., VERIX markers)
            case_sensitive: Whether matching is case-sensitive
        """
        self.required_sections = required_sections or []
        self.required_markers = required_markers or []
        self.case_sensitive = case_sensitive

    @property
    def name(self) -> str:
        return "format"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade format compliance."""
        if not response:
            return 0.0

        check_response = response if self.case_sensitive else response.lower()

        section_score = 0.0
        if self.required_sections:
            sections_found = sum(
                1 for s in self.required_sections
                if (s if self.case_sensitive else s.lower()) in check_response
            )
            section_score = sections_found / len(self.required_sections)

        marker_score = 0.0
        if self.required_markers:
            markers_found = sum(
                1 for m in self.required_markers
                if (m if self.case_sensitive else m.lower()) in check_response
            )
            marker_score = markers_found / len(self.required_markers)

        # Combine scores
        if self.required_sections and self.required_markers:
            return (section_score + marker_score) / 2
        elif self.required_sections:
            return section_score
        elif self.required_markers:
            return marker_score
        else:
            return 1.0  # No requirements = pass

    def grade_with_details(
        self,
        response: str,
        expected: Any,
        metadata: Dict,
    ) -> Tuple[float, Dict[str, Any]]:
        score = self.grade(response, expected, metadata)
        check_response = response if self.case_sensitive else response.lower()

        missing_sections = [
            s for s in self.required_sections
            if (s if self.case_sensitive else s.lower()) not in check_response
        ]
        missing_markers = [
            m for m in self.required_markers
            if (m if self.case_sensitive else m.lower()) not in check_response
        ]

        return score, {
            "grader": self.name,
            "score": score,
            "missing_sections": missing_sections,
            "missing_markers": missing_markers,
        }


class TokenGrader(Grader):
    """Grade token efficiency."""

    def __init__(
        self,
        baseline_tokens: int = 500,
        penalty_factor: float = 0.5,
        min_tokens: int = 50,
    ):
        """
        Initialize token grader.

        Args:
            baseline_tokens: Expected baseline token count
            penalty_factor: Rate of penalty for exceeding baseline
            min_tokens: Minimum tokens expected (below = penalty)
        """
        self.baseline = baseline_tokens
        self.penalty_factor = penalty_factor
        self.min_tokens = min_tokens

    @property
    def name(self) -> str:
        return "token_efficiency"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade token efficiency."""
        # Get token count from metadata or estimate
        actual_tokens = metadata.get("token_count", self._estimate_tokens(response))

        if actual_tokens < self.min_tokens:
            # Too short - penalty
            return actual_tokens / self.min_tokens

        if actual_tokens <= self.baseline:
            return 1.0

        # Exponential decay for excess
        excess = (actual_tokens - self.baseline) / self.baseline
        return max(0.0, 1.0 - self.penalty_factor * excess)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count from text."""
        # Rough approximation: ~1.3 tokens per word
        words = len(text.split())
        return int(words * 1.3)

    def grade_with_details(
        self,
        response: str,
        expected: Any,
        metadata: Dict,
    ) -> Tuple[float, Dict[str, Any]]:
        score = self.grade(response, expected, metadata)
        actual_tokens = metadata.get("token_count", self._estimate_tokens(response))

        return score, {
            "grader": self.name,
            "score": score,
            "actual_tokens": actual_tokens,
            "baseline_tokens": self.baseline,
            "efficiency_ratio": actual_tokens / self.baseline if self.baseline > 0 else 0,
        }


class LatencyGrader(Grader):
    """Grade response latency."""

    def __init__(
        self,
        target_ms: int = 1000,
        max_ms: int = 5000,
    ):
        """
        Initialize latency grader.

        Args:
            target_ms: Target response time in ms (score=1.0)
            max_ms: Maximum acceptable time (score=0.0)
        """
        self.target_ms = target_ms
        self.max_ms = max_ms

    @property
    def name(self) -> str:
        return "latency"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade response latency."""
        latency_ms = metadata.get("latency_ms", 0)

        if latency_ms <= 0:
            return 1.0  # No latency data = assume good

        if latency_ms <= self.target_ms:
            return 1.0

        if latency_ms >= self.max_ms:
            return 0.0

        # Linear interpolation between target and max
        return 1.0 - (latency_ms - self.target_ms) / (self.max_ms - self.target_ms)

    def grade_with_details(
        self,
        response: str,
        expected: Any,
        metadata: Dict,
    ) -> Tuple[float, Dict[str, Any]]:
        score = self.grade(response, expected, metadata)
        latency_ms = metadata.get("latency_ms", 0)

        return score, {
            "grader": self.name,
            "score": score,
            "latency_ms": latency_ms,
            "target_ms": self.target_ms,
            "max_ms": self.max_ms,
        }


class RegexGrader(Grader):
    """Grade against regex patterns."""

    def __init__(
        self,
        patterns: List[str],
        all_required: bool = True,
        case_sensitive: bool = False,
    ):
        """
        Initialize regex grader.

        Args:
            patterns: List of regex patterns to match
            all_required: If True, all patterns must match for full score
            case_sensitive: Whether patterns are case-sensitive
        """
        flags = 0 if case_sensitive else re.IGNORECASE
        self.patterns = [re.compile(p, flags) for p in patterns]
        self.pattern_strings = patterns
        self.all_required = all_required

    @property
    def name(self) -> str:
        return "regex"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade against regex patterns."""
        if not response:
            return 0.0

        matches = [bool(p.search(response)) for p in self.patterns]
        match_count = sum(matches)

        if not self.patterns:
            return 1.0

        if self.all_required:
            return 1.0 if all(matches) else match_count / len(self.patterns)
        else:
            return match_count / len(self.patterns)

    def grade_with_details(
        self,
        response: str,
        expected: Any,
        metadata: Dict,
    ) -> Tuple[float, Dict[str, Any]]:
        score = self.grade(response, expected, metadata)
        matches = [(p, bool(pat.search(response))) for p, pat in zip(self.pattern_strings, self.patterns)]

        return score, {
            "grader": self.name,
            "score": score,
            "pattern_matches": {p: m for p, m in matches},
            "matched_count": sum(1 for _, m in matches if m),
            "total_patterns": len(self.patterns),
        }


class VERIXGrader(Grader):
    """Grade VERIX notation compliance."""

    # VERIX markers at different compression levels
    L1_MARKERS = [
        r"\[assert\|",
        r"\[query\|",
        r"\[direct\|",
        r"\[ground:",
        r"\[conf:\d",
    ]

    L0_MARKERS = [
        r"\{[AQDCE]\}",  # Illocution
        r"\{[+-~?]\}",   # Affect
        r"\{\d{3}\}",    # Confidence
    ]

    def __init__(self, compression_level: int = 1):
        """
        Initialize VERIX grader.

        Args:
            compression_level: 0=L0 (AI-AI), 1=L1 (AI+Human), 2=L2 (Human)
        """
        self.compression_level = compression_level
        markers = self.L0_MARKERS if compression_level == 0 else self.L1_MARKERS
        self.patterns = [re.compile(m, re.IGNORECASE) for m in markers]

    @property
    def name(self) -> str:
        return f"verix_l{self.compression_level}"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade VERIX compliance."""
        if not response:
            return 0.0

        matches = sum(1 for p in self.patterns if p.search(response))
        return matches / len(self.patterns) if self.patterns else 0.0


class VERILINGUAGrader(Grader):
    """Grade VERILINGUA frame activation."""

    FRAME_MARKERS = {
        "evidential": [r"\[witnessed\]", r"\[reported\]", r"\[inferred\]", r"\[assumed\]"],
        "aspectual": [r"\[complete\]", r"\[ongoing\]", r"\[habitual\]", r"\[attempted\]"],
        "morphological": [r"\[root:", r"\[pattern:", r"\[template:"],
        "compositional": [r"\[primitive:", r"\[compound:", r"\[decompose:"],
        "honorific": [r"\[audience:", r"\[register:", r"\[formality:"],
        "classifier": [r"\[type:", r"\[category:", r"\[class:"],
        "spatial": [r"\[path:", r"\[position:", r"\[direction:"],
    }

    def __init__(self, active_frames: Optional[List[str]] = None):
        """
        Initialize VERILINGUA grader.

        Args:
            active_frames: List of frame names to check (None = all)
        """
        self.active_frames = active_frames or list(self.FRAME_MARKERS.keys())
        self.patterns = {}
        for frame in self.active_frames:
            if frame in self.FRAME_MARKERS:
                self.patterns[frame] = [
                    re.compile(p, re.IGNORECASE)
                    for p in self.FRAME_MARKERS[frame]
                ]

    @property
    def name(self) -> str:
        return "verilingua"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade VERILINGUA frame activation."""
        if not response or not self.patterns:
            return 0.0

        frame_scores = []
        for frame, patterns in self.patterns.items():
            matches = sum(1 for p in patterns if p.search(response))
            frame_scores.append(matches / len(patterns) if patterns else 0.0)

        return sum(frame_scores) / len(frame_scores) if frame_scores else 0.0


class CompositeGrader(Grader):
    """Combine multiple graders with weights."""

    def __init__(
        self,
        graders: List[Tuple[Grader, float]],
        normalize_weights: bool = True,
    ):
        """
        Initialize composite grader.

        Args:
            graders: List of (grader, weight) tuples
            normalize_weights: Whether to normalize weights to sum to 1
        """
        self.graders = graders
        self.normalize_weights = normalize_weights

        if normalize_weights:
            total_weight = sum(w for _, w in graders)
            self.graders = [(g, w / total_weight) for g, w in graders]

    @property
    def name(self) -> str:
        return "composite"

    def grade(self, response: str, expected: Any, metadata: Dict) -> float:
        """Grade using weighted combination of graders."""
        total_score = 0.0

        for grader, weight in self.graders:
            score = grader.grade(response, expected, metadata)
            total_score += score * weight

        return total_score

    def grade_with_details(
        self,
        response: str,
        expected: Any,
        metadata: Dict,
    ) -> Tuple[float, Dict[str, Any]]:
        composite_score = 0.0
        component_scores = {}

        for grader, weight in self.graders:
            score, details = grader.grade_with_details(response, expected, metadata)
            composite_score += score * weight
            component_scores[grader.name] = {
                "score": score,
                "weight": weight,
                "weighted_score": score * weight,
                "details": details,
            }

        return composite_score, {
            "grader": self.name,
            "score": composite_score,
            "components": component_scores,
        }


# Factory functions

def create_cognitive_grader(
    verix_strictness: int = 1,
    active_frames: Optional[List[str]] = None,
    token_baseline: int = 500,
) -> CompositeGrader:
    """
    Create a composite grader for cognitive architecture evaluation.

    Args:
        verix_strictness: VERIX compression level (0, 1, or 2)
        active_frames: VERILINGUA frames to check
        token_baseline: Expected token count

    Returns:
        CompositeGrader configured for cognitive evaluation
    """
    graders = [
        (VERIXGrader(verix_strictness), 0.3),
        (VERILINGUAGrader(active_frames), 0.3),
        (TokenGrader(token_baseline), 0.2),
        (FormatGrader(
            required_markers=["[assert", "[ground:"],
        ), 0.2),
    ]

    return CompositeGrader(graders)


def create_meta_prompt_grader() -> CompositeGrader:
    """
    Create a grader for meta-prompt optimization tasks.

    Designed for evaluating prompts about prompting (self-referential).
    """
    graders = [
        (RegexGrader([
            r"(?:prompt|instruction|directive)",
            r"(?:optimize|improve|enhance)",
            r"(?:example|instance|case)",
        ], all_required=False), 0.3),
        (FormatGrader(
            required_sections=["## ", "Example", "Criteria"],
        ), 0.3),
        (TokenGrader(baseline_tokens=800), 0.2),
        (VERIXGrader(compression_level=1), 0.2),
    ]

    return CompositeGrader(graders)


def create_skill_grader() -> CompositeGrader:
    """
    Create a grader for skill creation/optimization tasks.
    """
    graders = [
        (RegexGrader([
            r"(?:skill|capability|competency)",
            r"(?:trigger|invoke|activate)",
            r"(?:workflow|pipeline|process)",
        ], all_required=False), 0.3),
        (FormatGrader(
            required_sections=["SKILL", "Usage", "Steps"],
        ), 0.3),
        (TokenGrader(baseline_tokens=1000), 0.2),
        (FormatGrader(
            required_markers=["```", "- "],
        ), 0.2),
    ]

    return CompositeGrader(graders)


def create_agent_grader() -> CompositeGrader:
    """
    Create a grader for agent creation/optimization tasks.
    """
    graders = [
        (RegexGrader([
            r"(?:agent|persona|role)",
            r"(?:capability|tool|action)",
            r"(?:context|scope|domain)",
        ], all_required=False), 0.3),
        (FormatGrader(
            required_sections=["Agent", "Capabilities", "Tools"],
        ), 0.3),
        (TokenGrader(baseline_tokens=600), 0.2),
        (VERIXGrader(compression_level=1), 0.2),
    ]

    return CompositeGrader(graders)
