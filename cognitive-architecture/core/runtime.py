"""
Runtime - Claude client wrapper for executing prompts.

This module provides the execution layer that:
1. Takes prompts from PromptBuilder
2. Sends them to Claude API
3. Returns structured responses
4. Tracks token usage and latency

The runtime wraps the Anthropic SDK but could be swapped
for other providers without changing the rest of the system.
"""

import os
import time
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from .config import FullConfig
from .prompt_builder import PromptBuilder
from .verix import VerixParser, VerixClaim, VerixValidator


@dataclass
class ExecutionMetrics:
    """
    Metrics from a single prompt execution.

    Tracks token usage, latency, and cost for analysis
    and optimization feedback.
    """
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    model: str = ""
    timestamp: str = ""

    # Estimated cost in USD (approximate)
    input_cost_per_1k: float = 0.003  # Claude 3 Sonnet default
    output_cost_per_1k: float = 0.015

    @property
    def estimated_cost(self) -> float:
        """Calculate estimated cost in USD."""
        input_cost = (self.input_tokens / 1000) * self.input_cost_per_1k
        output_cost = (self.output_tokens / 1000) * self.output_cost_per_1k
        return input_cost + output_cost

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "latency_ms": self.latency_ms,
            "model": self.model,
            "timestamp": self.timestamp,
            "estimated_cost_usd": self.estimated_cost,
        }


@dataclass
class ExecutionResult:
    """
    Result from prompt execution.

    Contains the response text, parsed claims (if VERIX formatted),
    and execution metrics.
    """
    response: str
    claims: List[VerixClaim] = field(default_factory=list)
    metrics: ExecutionMetrics = field(default_factory=ExecutionMetrics)
    success: bool = True
    error: Optional[str] = None

    # Validation results
    is_valid: bool = True
    violations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "response": self.response[:500] + "..." if len(self.response) > 500 else self.response,
            "claims_count": len(self.claims),
            "metrics": self.metrics.to_dict(),
            "success": self.success,
            "error": self.error,
            "is_valid": self.is_valid,
            "violations": self.violations,
        }


class ClaudeRuntime:
    """
    Claude API client wrapper for executing cognitive prompts.

    Handles:
    - API communication with Anthropic
    - Token counting and cost tracking
    - VERIX claim parsing from responses
    - Validation against configuration requirements
    """

    DEFAULT_MODEL = "claude-sonnet-4-20250514"
    DEFAULT_MAX_TOKENS = 4096

    def __init__(
        self,
        config: FullConfig,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize runtime with configuration.

        Args:
            config: FullConfig for prompt building and validation
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model to use (defaults to claude-sonnet-4-20250514)
            max_tokens: Max output tokens (defaults to 4096)
        """
        self.config = config
        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens or self.DEFAULT_MAX_TOKENS

        # Initialize components
        self.prompt_builder = PromptBuilder(config)
        self.verix_parser = VerixParser(config.prompt)
        self.verix_validator = VerixValidator(config.prompt)

        # Initialize API client
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self._client: Optional[Any] = None

        if HAS_ANTHROPIC and self._api_key:
            self._client = anthropic.Anthropic(api_key=self._api_key)

    @property
    def is_available(self) -> bool:
        """Check if runtime is ready to execute."""
        return HAS_ANTHROPIC and self._client is not None

    def execute(self, task: str, task_type: str = "default") -> ExecutionResult:
        """
        Execute a task and return structured result.

        This is the main entry point for running prompts.

        Args:
            task: Task description
            task_type: Category of task

        Returns:
            ExecutionResult with response, claims, metrics, and validation
        """
        # Build prompts
        system_prompt, user_prompt = self.prompt_builder.build(task, task_type)

        # Execute via API
        result = self._call_api(system_prompt, user_prompt)

        if not result.success:
            return result

        # Parse VERIX claims
        result.claims = self.verix_parser.parse(result.response)

        # Validate claims
        if result.claims:
            result.is_valid, result.violations = self.verix_validator.validate(result.claims)

        return result

    def execute_raw(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> ExecutionResult:
        """
        Execute with pre-built prompts (bypass PromptBuilder).

        Useful for testing or when prompts come from cache.

        Args:
            system_prompt: System prompt string
            user_prompt: User prompt string

        Returns:
            ExecutionResult
        """
        return self._call_api(system_prompt, user_prompt)

    def _call_api(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> ExecutionResult:
        """
        Make API call to Claude.

        Args:
            system_prompt: System prompt
            user_prompt: User prompt

        Returns:
            ExecutionResult with response and metrics
        """
        if not self.is_available:
            return ExecutionResult(
                response="",
                success=False,
                error="Anthropic client not available (missing API key or package)",
            )

        start_time = time.time()
        timestamp = datetime.now().isoformat()

        try:
            message = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
            )

            # Extract response
            response_text = ""
            for block in message.content:
                if hasattr(block, "text"):
                    response_text += block.text

            # Calculate metrics
            latency_ms = (time.time() - start_time) * 1000
            metrics = ExecutionMetrics(
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
                total_tokens=message.usage.input_tokens + message.usage.output_tokens,
                latency_ms=latency_ms,
                model=self.model,
                timestamp=timestamp,
            )

            return ExecutionResult(
                response=response_text,
                metrics=metrics,
                success=True,
            )

        except anthropic.APIError as e:
            return ExecutionResult(
                response="",
                success=False,
                error=f"API error: {e}",
                metrics=ExecutionMetrics(timestamp=timestamp),
            )
        except Exception as e:
            return ExecutionResult(
                response="",
                success=False,
                error=f"Unexpected error: {e}",
                metrics=ExecutionMetrics(timestamp=timestamp),
            )

    def validate_response(self, response: str) -> Tuple[bool, List[str]]:
        """
        Validate a response string against VERIX requirements.

        Args:
            response: Response text to validate

        Returns:
            (is_valid, list_of_violations)
        """
        claims = self.verix_parser.parse(response)
        if not claims:
            # No claims found - check if claims were expected
            if self.config.prompt.verix_strictness.value > 0:
                return False, ["No VERIX claims found in response"]
            return True, []

        return self.verix_validator.validate(claims)

    def get_prompt_preview(self, task: str, task_type: str = "default") -> Dict[str, str]:
        """
        Get a preview of the prompts that would be sent.

        Useful for debugging and optimization.

        Args:
            task: Task description
            task_type: Category of task

        Returns:
            Dict with system_prompt and user_prompt
        """
        system_prompt, user_prompt = self.prompt_builder.build(task, task_type)
        return {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "cluster_key": self.prompt_builder.cluster_key(),
            "model": self.model,
            "max_tokens": self.max_tokens,
        }


class MockRuntime:
    """
    Mock runtime for testing without API calls.

    Generates deterministic responses based on input,
    useful for unit tests and development.
    """

    def __init__(self, config: FullConfig):
        """Initialize mock runtime."""
        self.config = config
        self.prompt_builder = PromptBuilder(config)
        self.verix_parser = VerixParser(config.prompt)
        self.verix_validator = VerixValidator(config.prompt)
        self._call_count = 0

    @property
    def is_available(self) -> bool:
        """Mock is always available."""
        return True

    def execute(self, task: str, task_type: str = "default") -> ExecutionResult:
        """
        Execute with mock response.

        Generates a VERIX-formatted mock response based on the task.
        """
        self._call_count += 1

        # Build prompts (for consistency)
        system_prompt, user_prompt = self.prompt_builder.build(task, task_type)

        # Generate mock response with VERIX notation
        mock_response = self._generate_mock_response(task, task_type)

        # Simulate latency
        mock_metrics = ExecutionMetrics(
            input_tokens=len(system_prompt.split()) + len(user_prompt.split()),
            output_tokens=len(mock_response.split()),
            total_tokens=0,  # Will be calculated
            latency_ms=50.0 + (self._call_count * 10),  # Simulated latency
            model="mock-model",
            timestamp=datetime.now().isoformat(),
        )
        mock_metrics.total_tokens = mock_metrics.input_tokens + mock_metrics.output_tokens

        # Parse and validate
        claims = self.verix_parser.parse(mock_response)
        is_valid, violations = self.verix_validator.validate(claims) if claims else (True, [])

        return ExecutionResult(
            response=mock_response,
            claims=claims,
            metrics=mock_metrics,
            success=True,
            is_valid=is_valid,
            violations=violations,
        )

    def _generate_mock_response(self, task: str, task_type: str) -> str:
        """Generate a mock VERIX-formatted response."""
        # Extract key terms from task
        task_words = task.lower().split()[:5]
        topic = " ".join(task_words) if task_words else "the task"

        return f"""
[assert|neutral] I have analyzed {topic} [ground:task_analysis] [conf:0.85] [state:provisional]

[witnessed] The request involves {task_type} type work.
[inferred] Based on the task description, the following approach is recommended.

[complete] Mock analysis of the task has been completed.
[ongoing] Further refinement may be needed based on feedback.

[assert|positive] The mock response demonstrates VERIX notation compliance [conf:0.90] [state:confirmed]

Key findings:
1. [reported:mock_data] Finding one related to {topic}
2. [assumed:0.70] Finding two is an assumption
3. [witnessed] Finding three was directly observed in the mock

[commit|neutral] I will continue to provide VERIX-compliant responses [conf:0.95] [state:confirmed]
"""


def create_runtime(
    config: Optional[FullConfig] = None,
    use_mock: bool = False,
    **kwargs,
) -> ClaudeRuntime:
    """
    Factory function to create appropriate runtime.

    Args:
        config: Configuration (uses default if not provided)
        use_mock: If True, return MockRuntime instead
        **kwargs: Additional arguments passed to runtime constructor

    Returns:
        ClaudeRuntime or MockRuntime instance
    """
    cfg = config or FullConfig()

    if use_mock:
        return MockRuntime(cfg)

    return ClaudeRuntime(cfg, **kwargs)


# Evaluate contract - THE SECOND THIN WAIST CONTRACT
def evaluate(config_vector: List[float], tasks: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    THE SECOND THIN WAIST CONTRACT - Evaluate configuration vector.

    This function signature NEVER changes:
        evaluate(config_vector) -> outcomes_vector

    GlobalMOO calls this to evaluate candidate configurations.

    Args:
        config_vector: 14-dimensional configuration vector
        tasks: List of task dicts with 'task', 'task_type', 'expected' keys

    Returns:
        Dict with outcome metrics:
        - task_accuracy: 0.0-1.0
        - token_efficiency: 0.0-1.0 (lower tokens = higher efficiency)
        - edge_robustness: 0.0-1.0
        - epistemic_consistency: 0.0-1.0
    """
    from .config import VectorCodec

    # Decode config from vector
    config = VectorCodec.decode(config_vector)

    # Create runtime (mock for now, real API would be used in production)
    runtime = create_runtime(config, use_mock=True)

    # Initialize outcome accumulators
    total_accuracy = 0.0
    total_tokens = 0
    total_validity = 0.0
    task_count = len(tasks)

    if task_count == 0:
        return {
            "task_accuracy": 0.0,
            "token_efficiency": 0.0,
            "edge_robustness": 0.0,
            "epistemic_consistency": 0.0,
        }

    # Evaluate each task
    for task_data in tasks:
        task = task_data.get("task", "")
        task_type = task_data.get("task_type", "default")

        result = runtime.execute(task, task_type)

        if result.success:
            # Accuracy: based on VERIX validity
            total_accuracy += 1.0 if result.is_valid else 0.5
            total_tokens += result.metrics.total_tokens

            # Validity score
            if result.claims:
                compliance = runtime.verix_validator.compliance_score(result.claims)
                total_validity += compliance
            else:
                total_validity += 0.5  # Neutral if no claims

    # Calculate final outcomes
    avg_accuracy = total_accuracy / task_count
    avg_tokens = total_tokens / task_count if task_count > 0 else 1000

    # Token efficiency: normalize to 0-1 (lower tokens = higher score)
    # Assume baseline is 500 tokens, max is 2000
    token_efficiency = max(0.0, min(1.0, 1.0 - (avg_tokens - 200) / 1800))

    # Epistemic consistency from validation
    epistemic_consistency = total_validity / task_count

    # Edge robustness (simplified - would be more complex in production)
    edge_robustness = avg_accuracy * 0.8  # Proxy for now

    return {
        "task_accuracy": avg_accuracy,
        "token_efficiency": token_efficiency,
        "edge_robustness": edge_robustness,
        "epistemic_consistency": epistemic_consistency,
    }
