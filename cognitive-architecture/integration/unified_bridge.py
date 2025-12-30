"""
UnifiedBridge - The Single Integration Gateway

This is the ONLY component that translates loop state/telemetry into
VectorCodec configs. All config changes flow through this gate.

INVARIANTS ENFORCED:
1. Thin waist contract preserved (uses PromptBuilder without changing it)
2. Frozen eval harness is authoritative (reads eval_report.json only)
3. Bridge is the only writer of runtime_config.json
4. Events are append-only to events.jsonl

Data Flow (Goodhart-Resistant):
    Ralph (artifact) -> Harness (grades) -> eval_report.json (truth)
                                                  |
                                            Bridge (reads)
                                                  |
                                        runtime_config.json (control)
                                                  |
                                       PromptBuilder (compiles)
                                                  |
                                          Ralph (next iteration)
"""

import os
import sys
import json
import uuid
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

# Add parent paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import FullConfig, VectorCodec, FrameworkConfig, PromptConfig, VerixStrictness, CompressionLevel
from core.prompt_builder import PromptBuilder
from core.vcl_validator import (
    VCLValidator,
    VCLConfig,
    ValidationResult as VCLValidationResult,
    L2Naturalizer,
    EVDType,
    ASPType,
    CompressionLevel as VCLCompressionLevel,
    enforce_safety_bounds as vcl_enforce_safety_bounds,
    compute_cluster_signature,
    CONFIDENCE_CEILINGS,
)
from modes.selector import ModeSelector, TaskContext
from modes.library import ModeLibrary


class DecisionIntent(Enum):
    """What the bridge intends to do with this iteration."""
    CONTINUE = "continue"       # Keep iterating with tuned config
    EXPLOIT = "exploit"         # Use best known config
    EXPLORE = "explore"         # Try new config variation
    HALT = "halt"               # Stop loop (regression or max iter)
    ESCALATE = "escalate"       # Requires human review


class Plane(Enum):
    """The five MECE planes of the architecture."""
    EXECUTION = "execution"       # Claude runtime, Ralph loop
    COGNITION = "cognition"       # VERILINGUA, VERIX, PromptBuilder
    OPTIMIZATION = "optimization" # GlobalMOO, PyMOO, mode distillation
    GOVERNANCE = "governance"     # 8-phase orchestrator, rollback
    EVIDENCE = "evidence"         # Frozen eval harness


class Timescale(Enum):
    """Nested timescales for optimization."""
    MICRO = "micro"   # Ralph iterations (minutes)
    MESO = "meso"     # MOO optimization (hours/days)
    MACRO = "macro"   # Meta-loop evolution (days/weeks)


@dataclass
class UnifiedEvent:
    """
    A single event in the append-only event spine.

    Every iteration appends one event to events.jsonl.
    """
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    task_id: str = ""
    plane: str = "execution"
    timescale: str = "micro"
    iteration: int = 0
    git_head: Optional[str] = None

    # Configuration state
    config: Dict[str, Any] = field(default_factory=dict)

    # Metrics (from harness only)
    metrics: Dict[str, float] = field(default_factory=dict)

    # Decision
    decision: str = "continue"
    reason: str = ""

    # VERIX-style grounds
    grounds: str = ""

    def to_jsonl(self) -> str:
        """Convert to JSON line for append."""
        return json.dumps(asdict(self), separators=(",", ":"))

    @classmethod
    def from_jsonl(cls, line: str) -> "UnifiedEvent":
        """Parse from JSON line."""
        return cls(**json.loads(line))


@dataclass
class BridgeInput:
    """Input to the bridge from loop state."""
    iteration: int
    artifact_path: Optional[str]
    eval_report: Dict[str, Any]
    history: List[Dict[str, Any]]
    policy: Dict[str, Any]
    task_metadata: Dict[str, Any]
    current_config: Dict[str, Any]


@dataclass
class BridgeOutput:
    """Output from bridge decision."""
    decision_intent: DecisionIntent
    mode: str
    vector14: List[float]
    verix: Dict[str, Any]
    frames: Dict[str, bool]
    reasons: List[str]
    human_gates_triggered: List[str] = field(default_factory=list)


class UnifiedBridge:
    """
    The ONLY place where loop state influences prompt generation.

    This bridge:
    1. Reads current runtime_config (or defaults to balanced mode)
    2. Requests prompt generation via PromptBuilder (thin waist unchanged)
    3. Submits artifacts to eval harness (read-only usage)
    4. Ingests eval_report metrics into optimization components
    5. Asks Governance to decide accept/reject/rollback/continue
    6. If approved, writes updated runtime_config.json
    7. Appends UnifiedEvent to events.jsonl (always)
    8. Validates output artifacts against VCL compliance requirements

    VCL Integration:
    - Uses VCLValidator to check output compliance
    - Enforces immutable safety bounds (EVD >= 1, ASP >= 1)
    - Tracks VCL compliance score in events
    - Supports L0/L1/L2 compression levels
    """

    def __init__(self, loop_dir: Path):
        """
        Initialize bridge with loop directory.

        Args:
            loop_dir: Path to .loop/ directory containing contract files
        """
        self.loop_dir = Path(loop_dir)
        self.config_path = self.loop_dir / "runtime_config.json"
        self.eval_path = self.loop_dir / "eval_report.json"
        self.events_path = self.loop_dir / "events.jsonl"
        self.policy_path = self.loop_dir / "policy.json"
        self.history_path = self.loop_dir / "history.json"
        self.moo_state_path = self.loop_dir / "moo_state.json"

        # Load mode library for selection
        self.mode_library = ModeLibrary()
        self.mode_selector = ModeSelector(self.mode_library)

        # Initialize VCL validator
        self.vcl_validator = VCLValidator()
        self.l2_naturalizer = L2Naturalizer()

    def load_runtime_config(self) -> Dict[str, Any]:
        """Load current runtime configuration."""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())
        return self._default_config()

    def load_policy(self) -> Dict[str, Any]:
        """Load governance policy."""
        if self.policy_path.exists():
            return json.loads(self.policy_path.read_text())
        return {"regression_threshold": 0.03, "max_iterations": 50}

    def load_eval_report(self) -> Dict[str, Any]:
        """Load evaluation report (harness output only)."""
        if self.eval_path.exists():
            return json.loads(self.eval_path.read_text())
        return {"metrics": {}, "harness_version": "unknown"}

    def load_history(self) -> List[Dict[str, Any]]:
        """Load iteration history."""
        if self.history_path.exists():
            data = json.loads(self.history_path.read_text())
            return data.get("iterations", [])
        return []

    def propose_next_config(self, bridge_input: BridgeInput) -> BridgeOutput:
        """
        Propose next configuration based on loop state.

        This is the core decision logic that respects all invariants.

        Args:
            bridge_input: Current loop state

        Returns:
            BridgeOutput with next configuration
        """
        # SECURITY: Validate no model-reported metrics
        for entry in bridge_input.history:
            if "model_reported_metrics" in entry:
                raise ValueError("INVARIANT VIOLATION: model-reported metrics in history!")

        reasons = []
        human_gates = []

        # 1. Check regression
        if self._check_regression(bridge_input):
            return BridgeOutput(
                decision_intent=DecisionIntent.HALT,
                mode=bridge_input.current_config.get("mode", "balanced"),
                vector14=bridge_input.current_config.get("vector14", [0]*14),
                verix=bridge_input.current_config.get("verix", {}),
                frames=bridge_input.current_config.get("frames", {}),
                reasons=["HALT: Regression detected above threshold"],
            )

        # 2. Check max iterations
        max_iter = bridge_input.policy.get("max_iterations", 50)
        if bridge_input.iteration >= max_iter:
            return BridgeOutput(
                decision_intent=DecisionIntent.HALT,
                mode=bridge_input.current_config.get("mode", "balanced"),
                vector14=bridge_input.current_config.get("vector14", [0]*14),
                verix=bridge_input.current_config.get("verix", {}),
                frames=bridge_input.current_config.get("frames", {}),
                reasons=[f"HALT: Max iterations ({max_iter}) reached"],
            )

        # 3. Check human gates
        human_gates = self._check_human_gates(bridge_input)
        if human_gates:
            return BridgeOutput(
                decision_intent=DecisionIntent.ESCALATE,
                mode=bridge_input.current_config.get("mode", "balanced"),
                vector14=bridge_input.current_config.get("vector14", [0]*14),
                verix=bridge_input.current_config.get("verix", {}),
                frames=bridge_input.current_config.get("frames", {}),
                reasons=[f"ESCALATE: Human gates triggered: {human_gates}"],
                human_gates_triggered=human_gates,
            )

        # 4. Decide explore vs exploit
        intent = self._select_intent(bridge_input)
        reasons.append(f"Intent: {intent.value}")

        # 5. Generate next config
        config = self._generate_config(intent, bridge_input)

        # 6. Enforce immutable bounds
        config = self._enforce_policy(config, bridge_input.policy)
        reasons.append("Policy bounds enforced")

        return config

    def _check_regression(self, bridge_input: BridgeInput) -> bool:
        """Check if current score shows regression above threshold."""
        threshold = bridge_input.policy.get("regression_threshold", 0.03)
        current = bridge_input.eval_report.get("metrics", {}).get("overall", 0)
        previous = bridge_input.current_config.get("previous_harness_score", 0)

        if previous > 0 and current > 0:
            delta = previous - current
            return delta > threshold
        return False

    def _check_human_gates(self, bridge_input: BridgeInput) -> List[str]:
        """Check which human gates are triggered."""
        gates = []
        policy_gates = bridge_input.policy.get("human_gates", {})

        # Threshold crossing gate
        crossing = policy_gates.get("threshold_crossing", {})
        delta_threshold = crossing.get("delta_threshold", 0.10)
        current = bridge_input.eval_report.get("metrics", {}).get("overall", 0)
        previous = bridge_input.current_config.get("previous_harness_score", 0)

        if previous > 0 and abs(current - previous) > delta_threshold:
            gates.append("threshold_crossing")

        return gates

    def _select_intent(self, bridge_input: BridgeInput) -> DecisionIntent:
        """Select explore vs exploit based on history."""
        history = bridge_input.history

        if len(history) < 5:
            return DecisionIntent.EXPLORE

        # Check recent trend
        recent_scores = [h.get("overall", 0) for h in history[-5:]]
        if all(s >= 0.8 for s in recent_scores):
            return DecisionIntent.EXPLOIT

        # Check oscillation
        if len(set(recent_scores)) <= 2:
            return DecisionIntent.EXPLORE  # Break out of oscillation

        return DecisionIntent.CONTINUE

    def _generate_config(self, intent: DecisionIntent, bridge_input: BridgeInput) -> BridgeOutput:
        """Generate next configuration based on intent."""
        current = bridge_input.current_config
        task_meta = bridge_input.task_metadata

        if intent == DecisionIntent.EXPLOIT:
            # Use best known config
            return BridgeOutput(
                decision_intent=intent,
                mode=current.get("mode", "balanced"),
                vector14=current.get("vector14", [0]*14),
                verix=current.get("verix", {}),
                frames=current.get("frames", {}),
                reasons=["Exploiting best known configuration"],
            )

        # For EXPLORE or CONTINUE, use mode selector
        task_desc = task_meta.get("task_description", "")
        context = TaskContext.from_task(task_desc)
        selected_mode = self.mode_selector.select(context)

        # Convert mode to config
        config = selected_mode.config
        vector14 = VectorCodec.encode(config)

        return BridgeOutput(
            decision_intent=intent,
            mode=selected_mode.name,
            vector14=vector14,
            verix={
                "strictness": config.prompt.verix_strictness.name,
                "compression": config.prompt.compression_level.name,
                "require_ground": config.prompt.require_ground,
                "require_confidence": config.prompt.require_confidence,
            },
            frames={
                "evidential": config.framework.evidential,
                "aspectual": config.framework.aspectual,
                "morphological": config.framework.morphological,
                "compositional": config.framework.compositional,
                "honorific": config.framework.honorific,
                "classifier": config.framework.classifier,
                "spatial": config.framework.spatial,
            },
            reasons=[f"Selected mode '{selected_mode.name}' for task context"],
        )

    def _enforce_policy(self, config: BridgeOutput, policy: Dict[str, Any]) -> BridgeOutput:
        """Enforce immutable bounds from policy."""
        immutable = policy.get("immutable_bounds", {})

        # Ensure evidential frame meets minimum
        evidential_min = immutable.get("evidential_min", 0.3)
        if config.vector14[0] < evidential_min:
            config.vector14[0] = evidential_min
            config.frames["evidential"] = True
            config.reasons.append(f"Enforced evidential_min={evidential_min}")

        # Ensure require_ground meets minimum
        ground_min = immutable.get("require_ground_min", 0.5)
        if config.vector14[9] < ground_min:
            config.vector14[9] = ground_min
            config.verix["require_ground"] = True
            config.reasons.append(f"Enforced require_ground_min={ground_min}")

        return config

    def write_config(self, config: BridgeOutput, iteration: int, prev_score: float) -> None:
        """
        Write updated configuration to runtime_config.json.

        This is the ONLY way to update cognition plane configuration.
        Includes VCL slots with immutable safety bounds enforced.
        """
        # Build VCL slots with enforced safety bounds
        vcl_slots = {
            "HON": {"enforcement": 1, "level": "teineigo"},
            "MOR": {"enforcement": 1, "active": config.frames.get("morphological", False)},
            "COM": {"enforcement": 1, "active": config.frames.get("compositional", False)},
            "CLS": {"enforcement": 0, "active": config.frames.get("classifier", False)},
            "EVD": {"enforcement": max(1, 2), "type": "observation"},  # IMMUTABLE >= 1
            "ASP": {"enforcement": max(1, 2), "type": "sov"},          # IMMUTABLE >= 1
            "SPC": {"enforcement": 0, "active": config.frames.get("spatial", False)},
        }

        output = {
            "_comment": "CONTROL INPUT - Written ONLY by UnifiedBridge",
            "_schema_version": "2.0.0",  # Bumped for VCL integration
            "mode": config.mode,
            "vector14": config.vector14,
            "verix": config.verix,
            "frames": config.frames,
            "vcl_slots": vcl_slots,
            "confidence_ceilings": {
                "definition": 0.95,
                "policy": 0.90,
                "observation": 0.95,
                "research": 0.85,
                "report": 0.70,
                "inference": 0.70,
            },
            "iteration": iteration,
            "previous_harness_score": prev_score,
            "exploration_mode": config.decision_intent.value,
            "updated_at": datetime.now().isoformat(),
        }

        # Apply VCL safety bounds before writing
        output = vcl_enforce_safety_bounds(output)
        self.config_path.write_text(json.dumps(output, indent=2))

    def append_event(self, event: UnifiedEvent) -> None:
        """
        Append event to events.jsonl (append-only).

        This is how we maintain the audit trail.
        """
        with open(self.events_path, "a") as f:
            f.write(event.to_jsonl() + "\n")

    def update_history(self, iteration: int, metrics: Dict[str, float]) -> None:
        """Update iteration history with harness metrics only."""
        history_data = {"_comment": "ITERATION HISTORY - Harness metrics only", "iterations": []}

        if self.history_path.exists():
            history_data = json.loads(self.history_path.read_text())

        history_data["iterations"].append({
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
        })

        self.history_path.write_text(json.dumps(history_data, indent=2))

    # =========================================================================
    # VCL VALIDATION METHODS
    # =========================================================================

    def validate_artifact_vcl(self, artifact: str) -> VCLValidationResult:
        """
        Validate artifact against VCL compliance requirements.

        Uses current runtime_config to determine VCL settings.

        Args:
            artifact: The artifact text to validate

        Returns:
            VCLValidationResult with all check details
        """
        vcl_config = self.get_vcl_config()
        return self.vcl_validator.validate(artifact, vcl_config)

    def get_vcl_config(self) -> VCLConfig:
        """
        Build VCLConfig from current runtime_config.

        Maps runtime_config VCL settings to VCLConfig dataclass.
        Always enforces immutable safety bounds (EVD >= 1, ASP >= 1).
        """
        runtime_config = self.load_runtime_config()
        vcl_slots = runtime_config.get("vcl_slots", {})
        verix_data = runtime_config.get("verix", {})

        # Map compression level
        compression_map = {
            "L0": VCLCompressionLevel.L0_INTERNAL,
            "L0_INTERNAL": VCLCompressionLevel.L0_INTERNAL,
            "L1": VCLCompressionLevel.L1_AUDIT,
            "L1_AUDIT": VCLCompressionLevel.L1_AUDIT,
            "L2": VCLCompressionLevel.L2_HUMAN,
            "L2_HUMAN": VCLCompressionLevel.L2_HUMAN,
        }
        compression = compression_map.get(
            verix_data.get("compression", "L2"),
            VCLCompressionLevel.L2_HUMAN
        )

        # Build VCLConfig
        config = VCLConfig(
            hon_enforcement=vcl_slots.get("HON", {}).get("enforcement", 1),
            mor_enforcement=vcl_slots.get("MOR", {}).get("enforcement", 1),
            com_enforcement=vcl_slots.get("COM", {}).get("enforcement", 1),
            cls_enforcement=vcl_slots.get("CLS", {}).get("enforcement", 0),
            evd_enforcement=vcl_slots.get("EVD", {}).get("enforcement", 2),
            asp_enforcement=vcl_slots.get("ASP", {}).get("enforcement", 2),
            spc_enforcement=vcl_slots.get("SPC", {}).get("enforcement", 0),
            compression=compression,
            require_ground=verix_data.get("require_ground", True),
            require_confidence=verix_data.get("require_confidence", True),
        )

        # ALWAYS enforce immutable safety bounds
        config.enforce_safety_bounds()
        return config

    def naturalize_output(self, artifact: str) -> str:
        """
        Convert artifact to L2 natural English.

        This is the DEFAULT for human-facing output.

        Args:
            artifact: Text with potential VCL notation

        Returns:
            Pure English text
        """
        return self.l2_naturalizer.naturalize(artifact)

    def get_confidence_ceiling(self, evd_type: str) -> float:
        """
        Get confidence ceiling for an EVD type.

        Args:
            evd_type: Evidence type string (observation, research, etc.)

        Returns:
            Maximum confidence value allowed
        """
        evd_map = {
            "observation": EVDType.OBSERVATION,
            "research": EVDType.RESEARCH,
            "report": EVDType.REPORT,
            "inference": EVDType.INFERENCE,
            "definition": EVDType.DEFINITION,
            "policy": EVDType.POLICY,
        }
        evd_enum = evd_map.get(evd_type.lower())
        if evd_enum:
            return CONFIDENCE_CEILINGS.get(evd_enum, 0.70)
        return 0.70  # Default to inference ceiling (most restrictive)

    def compute_vcl_cluster_key(self) -> str:
        """
        Compute VCL cluster signature for DSPy caching.

        This ensures cache isolation across VCL configurations.
        """
        vcl_config = self.get_vcl_config()
        return compute_cluster_signature(vcl_config)

    def _default_config(self) -> Dict[str, Any]:
        """Return default balanced configuration with VCL slots."""
        return {
            "mode": "balanced",
            "vector14": [1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0],
            "verix": {
                "strictness": "MODERATE",
                "compression": "L2",  # L2 is DEFAULT for human-facing output
                "require_ground": True,
                "require_confidence": True,
            },
            "frames": {
                "evidential": True,
                "aspectual": True,
                "morphological": False,
                "compositional": False,
                "honorific": False,
                "classifier": False,
                "spatial": False,
            },
            # VCL 7-slot configuration (order: HON -> MOR -> COM -> CLS -> EVD -> ASP -> SPC)
            "vcl_slots": {
                "HON": {"enforcement": 1, "level": "teineigo"},
                "MOR": {"enforcement": 1, "active": False},
                "COM": {"enforcement": 1, "active": False},
                "CLS": {"enforcement": 0, "active": False},
                "EVD": {"enforcement": 2, "type": "observation"},  # IMMUTABLE >= 1
                "ASP": {"enforcement": 2, "type": "sov"},          # IMMUTABLE >= 1
                "SPC": {"enforcement": 0, "active": False},
            },
            # Confidence ceilings by EVD type
            "confidence_ceilings": {
                "definition": 0.95,
                "policy": 0.90,
                "observation": 0.95,
                "research": 0.85,
                "report": 0.70,
                "inference": 0.70,
            },
            "iteration": 0,
            "previous_harness_score": 0.0,
            "exploration_mode": "explore",
        }

    def get_prompt_builder(self) -> PromptBuilder:
        """
        Get PromptBuilder configured from current runtime_config.

        This uses the thin waist contract WITHOUT changing it.
        """
        config_data = self.load_runtime_config()

        # Build FullConfig from runtime_config
        frames_data = config_data.get("frames", {})
        verix_data = config_data.get("verix", {})

        framework = FrameworkConfig(
            evidential=frames_data.get("evidential", True),
            aspectual=frames_data.get("aspectual", True),
            morphological=frames_data.get("morphological", False),
            compositional=frames_data.get("compositional", False),
            honorific=frames_data.get("honorific", False),
            classifier=frames_data.get("classifier", False),
            spatial=frames_data.get("spatial", False),
        )

        # Map strictness string to enum
        strictness_map = {
            "RELAXED": VerixStrictness.RELAXED,
            "MODERATE": VerixStrictness.MODERATE,
            "STRICT": VerixStrictness.STRICT,
        }
        strictness = strictness_map.get(
            verix_data.get("strictness", "MODERATE"),
            VerixStrictness.MODERATE
        )

        # Map compression string to enum
        compression_map = {
            "L0": CompressionLevel.L0_AI_AI,
            "L0_AI_AI": CompressionLevel.L0_AI_AI,
            "L1": CompressionLevel.L1_AI_HUMAN,
            "L1_AI_HUMAN": CompressionLevel.L1_AI_HUMAN,
            "L2": CompressionLevel.L2_HUMAN,
            "L2_HUMAN": CompressionLevel.L2_HUMAN,
        }
        compression = compression_map.get(
            verix_data.get("compression", "L1"),
            CompressionLevel.L1_AI_HUMAN
        )

        prompt_config = PromptConfig(
            verix_strictness=strictness,
            compression_level=compression,
            require_ground=verix_data.get("require_ground", True),
            require_confidence=verix_data.get("require_confidence", True),
        )

        full_config = FullConfig(framework=framework, prompt=prompt_config)

        # Return builder using thin waist contract
        return PromptBuilder(full_config)


def compute_cache_key(task: str, config: Dict[str, Any]) -> str:
    """
    Compute cache key that includes hash of runtime_config.

    This ensures DSPy caching doesn't pollute across configs.
    """
    config_hash = hashlib.sha256(
        json.dumps({
            "vector14": config.get("vector14", []),
            "frames": config.get("frames", {}),
            "verix": config.get("verix", {}),
        }, sort_keys=True).encode()
    ).hexdigest()[:16]

    task_hash = hashlib.sha256(task.encode()).hexdigest()[:16]
    return f"{task_hash}_{config_hash}"
