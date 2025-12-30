"""
Real Task Evaluator v3.0 - Execute actual tasks and measure real outcomes.

Replaces synthetic objective functions with real LLM execution and grading.

This is the KEY component that closes the optimization loop:
  Config -> Prompt -> LLM Execution -> Response -> Grading -> Telemetry -> MOO

v3.0: Uses x- prefixed custom fields for Anthropic compliance.
      Telemetry storage automatically uses v3.0 format via ExecutionTelemetry.
"""

import os
import sys
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from abc import ABC, abstractmethod

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, FrameworkConfig, PromptConfig
from core.prompt_builder import PromptBuilder
from core.verilingua import score_all_frames, aggregate_frame_score
from core.verix import VerixParser, VerixValidator
from optimization.telemetry_schema import ExecutionTelemetry, TelemetryStore


@dataclass
class Task:
    """A task to evaluate."""
    prompt: str
    task_type: str = "general"
    expected_output: Optional[str] = None
    grading_rubric: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None

    def prompt_hash(self) -> str:
        """Hash the prompt for deduplication."""
        return hashlib.md5(self.prompt.encode()).hexdigest()[:12]


@dataclass
class ExecutionResult:
    """Result of executing a task with a config."""
    response: str
    tokens_used: int
    latency_ms: int
    success: bool
    error: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class EvaluationResult:
    """Complete evaluation result with all metrics."""
    task: Task
    config: FullConfig
    execution: ExecutionResult

    # Objective scores (0.0 - 1.0, higher is better)
    task_accuracy: float = 0.0
    token_efficiency: float = 0.0
    frame_compliance: float = 0.0
    verix_compliance: float = 0.0

    # Detailed breakdowns
    frame_scores: Dict[str, float] = field(default_factory=dict)
    verix_claims_count: int = 0
    verix_grounded_claims: int = 0

    def to_objectives(self) -> Dict[str, float]:
        """Get objectives dict for MOO."""
        return {
            "task_accuracy": self.task_accuracy,
            "token_efficiency": self.token_efficiency,
            "frame_compliance": self.frame_compliance,
            "verix_compliance": self.verix_compliance,
        }

    def to_telemetry(self) -> ExecutionTelemetry:
        """Convert to telemetry record for storage."""
        return ExecutionTelemetry(
            config_vector=VectorCodec.encode(self.config),
            active_frames=[
                name for name, active in [
                    ("evidential", self.config.framework.evidential),
                    ("aspectual", self.config.framework.aspectual),
                    ("morphological", self.config.framework.morphological),
                    ("compositional", self.config.framework.compositional),
                    ("honorific", self.config.framework.honorific),
                    ("classifier", self.config.framework.classifier),
                    ("spatial", self.config.framework.spatial),
                ] if active
            ],
            verix_strictness=self.config.prompt.verix_strictness.value,
            task_type=self.task.task_type,
            task_prompt_hash=self.task.prompt_hash(),
            task_prompt_length=len(self.task.prompt),
            response_tokens=self.execution.tokens_used,
            response_length=len(self.execution.response),
            latency_ms=self.execution.latency_ms,
            frame_scores=self.frame_scores,
            aggregate_frame_score=self.frame_compliance,
            verix_claims_count=self.verix_claims_count,
            verix_grounded_claims=self.verix_grounded_claims,
            verix_compliance_score=self.verix_compliance,
            task_success=self.execution.success,
            error_occurred=self.execution.error is not None,
            error_message=self.execution.error,
        )


class LLMRuntime(ABC):
    """Abstract base for LLM execution."""

    @abstractmethod
    def execute(self, prompt: str) -> ExecutionResult:
        """Execute a prompt and return result."""
        pass


class MockRuntime(LLMRuntime):
    """Mock runtime for testing without API calls."""

    def __init__(self, response_generator: Optional[Callable[[str], str]] = None):
        """Initialize with optional custom response generator."""
        self.response_generator = response_generator or self._default_response

    def _default_response(self, prompt: str) -> str:
        """Generate a mock response with VERIX markers."""
        return f"""
[witnessed] I analyzed the provided prompt directly.
[complete] Here is my response to the task.

[assert|neutral] The task has been processed [conf:0.85] [state:confirmed]
[inferred] Based on the prompt structure, this appears to be a {len(prompt) % 3}-step task.

Response generated for prompt of length {len(prompt)} characters.
"""

    def execute(self, prompt: str) -> ExecutionResult:
        """Execute with mock response."""
        start = time.time()
        response = self.response_generator(prompt)
        latency = int((time.time() - start) * 1000)

        return ExecutionResult(
            response=response,
            tokens_used=len(response.split()),
            latency_ms=latency,
            success=True,
        )


class AnthropicRuntime(LLMRuntime):
    """Real Anthropic API runtime."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-haiku-20240307"):
        """Initialize with API key and model."""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None

    @property
    def client(self):
        """Lazy-init Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("anthropic package required. Install with: pip install anthropic")
        return self._client

    def execute(self, prompt: str) -> ExecutionResult:
        """Execute via Anthropic API."""
        start = time.time()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )

            latency = int((time.time() - start) * 1000)
            text = response.content[0].text
            tokens = response.usage.output_tokens

            return ExecutionResult(
                response=text,
                tokens_used=tokens,
                latency_ms=latency,
                success=True,
                raw_response=response,
            )
        except Exception as e:
            return ExecutionResult(
                response="",
                tokens_used=0,
                latency_ms=int((time.time() - start) * 1000),
                success=False,
                error=str(e),
            )


class TaskGrader:
    """Grade task outputs for accuracy."""

    def __init__(self):
        """Initialize grader."""
        pass

    def grade_accuracy(
        self,
        task: Task,
        response: str,
        execution: ExecutionResult
    ) -> float:
        """
        Grade task accuracy (0.0 - 1.0).

        Uses multiple signals:
        1. If expected_output provided, compare similarity
        2. Check response coherence (not empty, reasonable length)
        3. Check for error indicators
        """
        if not execution.success:
            return 0.0

        if not response or len(response) < 10:
            return 0.1  # Minimal response

        score = 0.5  # Base score for non-empty response

        # Length appropriateness
        prompt_len = len(task.prompt)
        response_len = len(response)
        if response_len >= prompt_len * 0.5:  # Response is substantial
            score += 0.2

        # Check for error patterns
        error_patterns = ["I cannot", "I'm unable", "error", "failed"]
        if not any(p.lower() in response.lower() for p in error_patterns):
            score += 0.1

        # If expected output, check similarity
        if task.expected_output:
            similarity = self._compute_similarity(response, task.expected_output)
            score = 0.3 + (0.7 * similarity)

        return min(1.0, score)

    def _compute_similarity(self, response: str, expected: str) -> float:
        """Compute text similarity (simple word overlap)."""
        response_words = set(response.lower().split())
        expected_words = set(expected.lower().split())

        if not expected_words:
            return 0.5

        overlap = len(response_words & expected_words)
        return overlap / len(expected_words)


class RealTaskEvaluator:
    """
    Evaluates tasks with actual LLM execution.

    This is the production evaluator that:
    1. Builds prompts using PromptBuilder with cognitive frames
    2. Executes via LLM runtime (mock or real)
    3. Scores responses against frames and VERIX
    4. Returns complete EvaluationResult for MOO
    """

    def __init__(
        self,
        runtime: Optional[LLMRuntime] = None,
        store_telemetry: bool = True,
    ):
        """
        Initialize evaluator.

        Args:
            runtime: LLM runtime to use (defaults to MockRuntime)
            store_telemetry: Whether to store telemetry records
        """
        self.runtime = runtime or MockRuntime()
        self.grader = TaskGrader()
        self.store_telemetry = store_telemetry
        self.telemetry_store = TelemetryStore() if store_telemetry else None

    def evaluate(self, config: FullConfig, task: Task) -> EvaluationResult:
        """
        Evaluate a single task with a configuration.

        Args:
            config: Full configuration (frames + VERIX settings)
            task: Task to evaluate

        Returns:
            Complete EvaluationResult with all metrics
        """
        # 1. Build prompt with config
        builder = PromptBuilder(config)
        prompt_parts = builder.build(task.prompt, task.task_type)

        # Handle tuple return from builder
        if isinstance(prompt_parts, tuple):
            full_prompt = "\n".join(prompt_parts)
        else:
            full_prompt = prompt_parts

        # 2. Execute via runtime
        execution = self.runtime.execute(full_prompt)

        # 3. Score frame compliance
        frame_scores = {}
        frame_compliance = 0.0

        if execution.success and execution.response:
            frame_scores = score_all_frames(execution.response, config.framework)
            frame_compliance = aggregate_frame_score(execution.response, config.framework)

        # 4. Score VERIX compliance
        verix_compliance = 0.0
        verix_claims_count = 0
        verix_grounded = 0

        if execution.success and execution.response:
            parser = VerixParser(config.prompt)
            claims = parser.parse(execution.response)
            verix_claims_count = len(claims)
            verix_grounded = sum(1 for c in claims if c.ground)

            validator = VerixValidator(config.prompt)
            verix_compliance = validator.compliance_score(claims)

        # 5. Grade accuracy
        task_accuracy = self.grader.grade_accuracy(task, execution.response, execution)

        # 6. Compute token efficiency (inverse of tokens used, normalized)
        # Higher is better: 1.0 = minimal tokens, 0.0 = max tokens
        max_expected_tokens = 500  # Baseline expectation
        token_efficiency = max(0.0, 1.0 - (execution.tokens_used / max_expected_tokens))
        token_efficiency = min(1.0, token_efficiency)

        # 7. Build result
        result = EvaluationResult(
            task=task,
            config=config,
            execution=execution,
            task_accuracy=task_accuracy,
            token_efficiency=token_efficiency,
            frame_compliance=frame_compliance,
            verix_compliance=verix_compliance,
            frame_scores=frame_scores,
            verix_claims_count=verix_claims_count,
            verix_grounded_claims=verix_grounded,
        )

        # 8. Store telemetry
        if self.store_telemetry and self.telemetry_store:
            telemetry = result.to_telemetry()
            self.telemetry_store.store(telemetry)

        return result

    def evaluate_batch(
        self,
        config: FullConfig,
        tasks: List[Task]
    ) -> List[EvaluationResult]:
        """Evaluate multiple tasks with same config."""
        return [self.evaluate(config, task) for task in tasks]

    def compare_configs(
        self,
        configs: List[FullConfig],
        tasks: List[Task]
    ) -> Dict[str, List[EvaluationResult]]:
        """Compare multiple configs across same task set."""
        results = {}
        for i, config in enumerate(configs):
            config_key = f"config_{i}"
            results[config_key] = self.evaluate_batch(config, tasks)
        return results


# Factory functions
def create_evaluator(
    use_real_api: bool = False,
    api_key: Optional[str] = None,
    store_telemetry: bool = True,
) -> RealTaskEvaluator:
    """
    Create an evaluator instance.

    Args:
        use_real_api: Whether to use real Anthropic API
        api_key: API key (defaults to env var)
        store_telemetry: Whether to store telemetry
    """
    if use_real_api:
        runtime = AnthropicRuntime(api_key=api_key)
    else:
        runtime = MockRuntime()

    return RealTaskEvaluator(runtime=runtime, store_telemetry=store_telemetry)


def create_mock_evaluator() -> RealTaskEvaluator:
    """Create evaluator with mock runtime (for testing)."""
    return RealTaskEvaluator(runtime=MockRuntime(), store_telemetry=False)
