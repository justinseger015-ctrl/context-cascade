"""
PromptBuilder - THE THIN WAIST CONTRACT

This class implements the stable contract that NEVER changes:
    build(task, task_type) -> (system_prompt, user_prompt)

All optimization happens AROUND this contract, not inside it.
DSPy Level 2 caches compiled prompts keyed by cluster_key.
GlobalMOO optimizes configurations that feed into this builder.

THE CONTRACT:
- Input: task (str), task_type (str)
- Output: (system_prompt, user_prompt) tuple
- This signature NEVER changes
- All other code wraps around this contract
"""

from typing import Tuple, List, Optional
from dataclasses import dataclass

from .config import FullConfig, VectorCodec, CompressionLevel
from .verix import VerixValidator, VerixStrictness
from .verilingua import FrameRegistry, CognitiveFrame, get_combined_activation_instruction


# Task type definitions with base instructions
TASK_TYPE_INSTRUCTIONS = {
    "reasoning": """
You are a precise reasoning assistant. Your responses should:
- Break down complex problems into clear steps
- Show your reasoning chain explicitly
- Validate each step before proceeding
- Acknowledge uncertainty when present
""",

    "coding": """
You are a code assistant. Your responses should:
- Provide working, tested code
- Follow best practices and style guidelines
- Include comments for complex logic
- Consider edge cases and error handling
""",

    "analysis": """
You are an analytical assistant. Your responses should:
- Examine data/information systematically
- Identify patterns and anomalies
- Provide evidence-based conclusions
- Consider alternative interpretations
""",

    "creative": """
You are a creative assistant. Your responses should:
- Generate novel and original content
- Consider multiple creative angles
- Balance creativity with relevance
- Iterate on ideas when helpful
""",

    "conversational": """
You are a helpful conversational assistant. Your responses should:
- Be clear and accessible
- Anticipate follow-up questions
- Provide context when helpful
- Maintain appropriate tone
""",

    "default": """
You are a helpful assistant. Your responses should be:
- Accurate and well-reasoned
- Clear and well-organized
- Appropriately detailed
- Honest about limitations
""",
}


@dataclass
class PromptComponents:
    """
    Internal structure for prompt components.

    Used to organize the parts before assembly.
    """
    base_instruction: str
    frame_activations: str
    verix_requirements: str
    output_format: str
    task_content: str


class PromptBuilder:
    """
    Build prompts with cognitive frame activation and VERIX requirements.

    This is the THIN WAIST - the contract that NEVER changes.
    DSPy Level 2 caches compiled prompts keyed by cluster_key.

    The build() method signature is FROZEN:
        build(task: str, task_type: str) -> Tuple[str, str]

    All optimization happens by:
    1. Changing the FullConfig passed to __init__
    2. Caching compiled prompts by cluster_key
    3. NOT by changing this class's interface
    """

    def __init__(self, config: FullConfig):
        """
        Initialize builder with configuration.

        Args:
            config: FullConfig specifying frames and VERIX settings
        """
        self.config = config
        self.active_frames = FrameRegistry.get_active(config.framework)
        self.verix_validator = VerixValidator(config.prompt)
        self._cluster_key = VectorCodec.cluster_key(config)

    def build(self, task: str, task_type: str) -> Tuple[str, str]:
        """
        THE CONTRACT - NEVER CHANGES

        Build system and user prompts for the given task.

        Args:
            task: The specific task description
            task_type: Category of task (reasoning, coding, analysis, etc.)

        Returns:
            (system_prompt, user_prompt) tuple
        """
        # Gather components
        components = PromptComponents(
            base_instruction=self._base_instruction(task_type),
            frame_activations=self._frame_activations(),
            verix_requirements=self._verix_requirements(),
            output_format=self._output_format(),
            task_content=task,
        )

        # Assemble prompts
        system_prompt = self._assemble_system_prompt(components)
        user_prompt = self._assemble_user_prompt(components)

        return system_prompt, user_prompt

    def cluster_key(self) -> str:
        """
        Return cluster key for DSPy Level 2 caching.

        Prompts with the same cluster key share cached artifacts.
        """
        return self._cluster_key

    def _base_instruction(self, task_type: str) -> str:
        """
        Get task-type specific base instruction.

        Args:
            task_type: Category of task

        Returns:
            Base instruction string
        """
        normalized_type = task_type.lower().strip()
        return TASK_TYPE_INSTRUCTIONS.get(
            normalized_type,
            TASK_TYPE_INSTRUCTIONS["default"]
        )

    def _frame_activations(self) -> str:
        """
        Build frame activation instructions.

        Returns:
            Combined activation instructions for all active frames
        """
        return get_combined_activation_instruction(self.config.framework)

    def _verix_requirements(self) -> str:
        """
        Build VERIX compliance requirements based on config.

        Returns:
            VERIX requirement instructions
        """
        strictness = self.config.prompt.verix_strictness
        compression = self.config.prompt.compression_level
        require_ground = self.config.prompt.require_ground
        require_confidence = self.config.prompt.require_confidence

        parts = ["# VERIX EPISTEMIC NOTATION REQUIREMENTS", ""]

        # Strictness level instructions
        if strictness == VerixStrictness.STRICT:
            parts.append("""
## STRICT VERIX MODE

You MUST format all claims using full VERIX notation:
[illocution|affect] content [ground:evidence] [conf:N.NN] [state:status]

Required fields:
- illocution: assert, query, direct, commit, or express
- affect: neutral, positive, negative, or uncertain
- content: the actual claim
- ground: source/evidence for the claim
- confidence: numeric 0.00-1.00
- state: provisional, confirmed, or retracted

Example:
[assert|neutral] The function handles null input correctly [ground:traced code path] [conf:0.95] [state:confirmed]
""")
        elif strictness == VerixStrictness.MODERATE:
            parts.append("""
## MODERATE VERIX MODE

Format significant claims using VERIX notation:
[illocution|affect] content [conf:N.NN]

Required fields:
- illocution: assert, query, direct, commit, or express
- affect: neutral, positive, negative, or uncertain
- confidence: numeric 0.00-1.00

Optional but encouraged: ground, state

Example:
[assert|neutral] The race condition occurs in the mutex lock [conf:0.85]
""")
        else:  # RELAXED
            parts.append("""
## RELAXED VERIX MODE

Use VERIX notation for key claims where confidence matters:
[illocution|affect] content

The minimal format marks speech act and stance.
Include confidence when uncertain: [conf:N.NN]

Example:
[assert|uncertain] The bug might be in the event handler [conf:0.60]
""")

        # Ground requirements
        if require_ground:
            parts.append("""
## EVIDENCE REQUIREMENT

All factual claims MUST include evidence/source:
- [ground:code_analysis] - from reading/tracing code
- [ground:documentation] - from official docs
- [ground:user_input] - from user's message
- [ground:inference] - from logical deduction
- [ground:assumption] - explicit assumption (state confidence)
""")

        # Confidence requirements
        if require_confidence:
            parts.append("""
## CONFIDENCE REQUIREMENT

Include confidence values [conf:N.NN] for:
- Uncertain claims (< 0.7 confidence)
- Inferences or assumptions
- Claims about future behavior
- Debugging hypotheses
""")

        # Compression level
        parts.append(f"""
## OUTPUT FORMAT

Compression Level: {compression.name}
""")

        if compression == CompressionLevel.L0_AI_AI:
            parts.append("""
Use compact L0 format for machine processing:
A.85:claim content (Assert, Neutral, 85% confidence)
?.60:question content (Query, Uncertain, 60%)
!+90:instruction (Direct, Positive, 90%)
""")
        elif compression == CompressionLevel.L1_AI_HUMAN:
            parts.append("""
Use annotated L1 format for human inspection:
[assert|neutral] claim content [ground:source] [conf:0.85] [state:confirmed]
""")
        else:  # L2_HUMAN
            parts.append("""
Use natural L2 format for end users:
Write in natural language, but maintain epistemic honesty.
Express uncertainty naturally: "I believe...", "It appears...", "Based on..."
""")

        return "\n".join(parts)

    def _output_format(self) -> str:
        """
        Build output format instructions.

        Returns:
            Output format requirements
        """
        active_frame_names = [f.name for f in self.active_frames]
        frame_list = ", ".join(active_frame_names) if active_frame_names else "none"

        return f"""
# OUTPUT REQUIREMENTS

Active Frames: [{frame_list}]
VERIX Strictness: {self.config.prompt.verix_strictness.name}
Compression: {self.config.prompt.compression_level.name}

Your response MUST:
1. Follow all active cognitive frame requirements
2. Use appropriate VERIX notation for claims
3. Mark evidence sources explicitly
4. Include confidence where relevant
"""

    def _assemble_system_prompt(self, components: PromptComponents) -> str:
        """
        Assemble final system prompt from components.

        Args:
            components: PromptComponents with all parts

        Returns:
            Complete system prompt string
        """
        sections = [
            components.base_instruction.strip(),
            "",
            components.frame_activations.strip() if components.frame_activations else "",
            "",
            components.verix_requirements.strip(),
            "",
            components.output_format.strip(),
        ]

        # Filter empty sections and join
        return "\n".join(s for s in sections if s)

    def _assemble_user_prompt(self, components: PromptComponents) -> str:
        """
        Assemble final user prompt from components.

        Args:
            components: PromptComponents with task content

        Returns:
            Complete user prompt string
        """
        return f"""
# TASK

{components.task_content}

---

Respond following all active cognitive frames and VERIX notation requirements.
"""


class PromptBuilderFactory:
    """
    Factory for creating PromptBuilder instances with common configurations.

    Provides convenient factory methods for standard use cases.
    """

    @staticmethod
    def default() -> PromptBuilder:
        """Create builder with default configuration."""
        return PromptBuilder(FullConfig())

    @staticmethod
    def minimal() -> PromptBuilder:
        """Create builder with minimal frame activation."""
        from .config import MINIMAL_CONFIG
        return PromptBuilder(MINIMAL_CONFIG)

    @staticmethod
    def strict() -> PromptBuilder:
        """Create builder with all frames and strict VERIX."""
        from .config import STRICT_CONFIG
        return PromptBuilder(STRICT_CONFIG)

    @staticmethod
    def from_vector(vector: List[float]) -> PromptBuilder:
        """
        Create builder from configuration vector.

        Used by GlobalMOO to test candidate configurations.

        Args:
            vector: 14-dimensional configuration vector

        Returns:
            PromptBuilder with decoded configuration
        """
        config = VectorCodec.decode(vector)
        return PromptBuilder(config)

    @staticmethod
    def for_task_type(task_type: str) -> PromptBuilder:
        """
        Create builder optimized for a specific task type.

        Adjusts default frames based on task type.

        Args:
            task_type: Category of task

        Returns:
            PromptBuilder with task-appropriate configuration
        """
        from .config import FrameworkConfig, PromptConfig, VerixStrictness

        # Task-specific frame configurations
        task_frames = {
            "reasoning": FrameworkConfig(
                evidential=True,
                aspectual=True,
                morphological=True,
                compositional=True,
                honorific=False,
                classifier=False,
                spatial=False,
            ),
            "coding": FrameworkConfig(
                evidential=True,
                aspectual=True,
                morphological=False,
                compositional=False,
                honorific=False,
                classifier=True,
                spatial=True,
            ),
            "analysis": FrameworkConfig(
                evidential=True,
                aspectual=True,
                morphological=True,
                compositional=False,
                honorific=False,
                classifier=True,
                spatial=False,
            ),
            "creative": FrameworkConfig(
                evidential=False,
                aspectual=False,
                morphological=False,
                compositional=True,
                honorific=True,
                classifier=False,
                spatial=False,
            ),
            "conversational": FrameworkConfig(
                evidential=False,
                aspectual=False,
                morphological=False,
                compositional=False,
                honorific=True,
                classifier=False,
                spatial=False,
            ),
        }

        framework = task_frames.get(
            task_type.lower(),
            FrameworkConfig()  # default
        )

        config = FullConfig(
            framework=framework,
            prompt=PromptConfig(
                verix_strictness=VerixStrictness.MODERATE,
            ),
        )

        return PromptBuilder(config)


def build_prompt(
    task: str,
    task_type: str = "default",
    config: Optional[FullConfig] = None,
) -> Tuple[str, str]:
    """
    Convenience function to build prompts without instantiating builder.

    This is a shortcut for simple use cases. For repeated builds with
    the same config, instantiate PromptBuilder directly.

    Args:
        task: The task description
        task_type: Category of task
        config: Optional configuration (uses default if not provided)

    Returns:
        (system_prompt, user_prompt) tuple
    """
    builder = PromptBuilder(config or FullConfig())
    return builder.build(task, task_type)
