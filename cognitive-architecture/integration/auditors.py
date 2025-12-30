"""
VERIX-Speaking Auditors for the Integration.

Each auditor MUST emit strict JSON with VERIX claims.
Claims follow VCL v3.1.1 spec with confidence ceilings.

Auditor Orthogonality (MECE):
| Auditor   | Question                                    | Primary Frame              |
|-----------|---------------------------------------------|----------------------------|
| Skill     | Does it demonstrate the intended capability?| Compositional + Classifier |
| Prompt    | Did compilation/config behave as intended?  | Evidential                 |
| Expertise | Is domain reasoning sound for audience?     | Honorific                  |
| Output    | Does it meet acceptance criteria?           | Classifier + Spatial       |

Output Format (REQUIRED):
{
  "auditor_type": "skill|prompt|expertise|output",
  "verix": {
    "illocution": "assert|recommend|warn|reject",
    "affect": "confident|uncertain|concerned"
  },
  "claims": [
    "[assert|concerned] Task accuracy below threshold [ground:harness_accuracy=0.65] [conf:0.95] [state:flagged]"
  ],
  "vcl": {
    "evd_type": "observation|research|report|inference",
    "asp_type": "sov|nesov",
    "confidence_ceiling": 0.95
  },
  "would_change_if": [
    "harness_accuracy >= 0.75",
    "capability_indicators present"
  ],
  "action_class": "TUNE_VECTOR|CHANGE_MODE|EDIT_PROMPTBUILDER|CODE_FIX|TEST_ADD|ACCEPT|REJECT",
  "confidence": 0.85,
  "grounds": ["harness:task_accuracy=0.65", "artifact:length=1234"]
}

VCL Confidence Ceilings (ENFORCED):
  - definition: 0.95
  - policy: 0.90
  - observation: 0.95
  - research: 0.85
  - report: 0.70
  - inference: 0.70
"""

import os
import sys
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from enum import Enum

# Add parent paths for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import VCL validator for compliance checking
try:
    from core.vcl_validator import (
        VCLValidator,
        VCLConfig,
        EVDType,
        ASPType,
        CONFIDENCE_CEILINGS,
        CompressionLevel as VCLCompressionLevel,
    )
    VCL_AVAILABLE = True
except ImportError:
    VCL_AVAILABLE = False


class Illocution(Enum):
    """VERIX illocution types."""
    ASSERT = "assert"
    RECOMMEND = "recommend"
    WARN = "warn"
    REJECT = "reject"


class Affect(Enum):
    """VERIX affect types."""
    CONFIDENT = "confident"
    UNCERTAIN = "uncertain"
    CONCERNED = "concerned"


class ActionClass(Enum):
    """What action the auditor recommends."""
    TUNE_VECTOR = "TUNE_VECTOR"
    CHANGE_MODE = "CHANGE_MODE"
    EDIT_PROMPTBUILDER = "EDIT_PROMPTBUILDER"
    CODE_FIX = "CODE_FIX"
    TEST_ADD = "TEST_ADD"
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


@dataclass
class AuditorResult:
    """Standard output format for all auditors with VCL compliance."""
    auditor_type: str
    verix: Dict[str, str]
    claims: List[str]
    would_change_if: List[str]
    action_class: str
    confidence: float
    grounds: List[str]
    # VCL v3.1.1 fields
    vcl: Dict[str, Any] = field(default_factory=lambda: {
        "evd_type": "observation",
        "asp_type": "sov",
        "confidence_ceiling": 0.95,
    })

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def enforce_confidence_ceiling(self) -> "AuditorResult":
        """Enforce VCL confidence ceiling based on EVD type."""
        evd_type = self.vcl.get("evd_type", "inference")
        ceiling = self.vcl.get("confidence_ceiling", 0.70)

        # Map EVD type to ceiling if VCL available
        if VCL_AVAILABLE:
            evd_map = {
                "observation": CONFIDENCE_CEILINGS.get(EVDType.OBSERVATION, 0.95),
                "research": CONFIDENCE_CEILINGS.get(EVDType.RESEARCH, 0.85),
                "report": CONFIDENCE_CEILINGS.get(EVDType.REPORT, 0.70),
                "inference": CONFIDENCE_CEILINGS.get(EVDType.INFERENCE, 0.70),
                "definition": CONFIDENCE_CEILINGS.get(EVDType.DEFINITION, 0.95),
                "policy": CONFIDENCE_CEILINGS.get(EVDType.POLICY, 0.90),
            }
            ceiling = evd_map.get(evd_type, 0.70)

        # Cap confidence at ceiling
        if self.confidence > ceiling:
            self.confidence = ceiling
            self.vcl["confidence_capped"] = True

        self.vcl["confidence_ceiling"] = ceiling
        return self


class BaseAuditor:
    """Base class for all auditors."""

    auditor_type: str = "base"

    def audit(
        self,
        artifact: str,
        eval_report: Dict[str, Any],
        runtime_config: Dict[str, Any],
    ) -> AuditorResult:
        """
        Audit an artifact and return structured result.

        Args:
            artifact: The artifact content to audit
            eval_report: Harness evaluation report
            runtime_config: Current configuration

        Returns:
            AuditorResult with VERIX claims
        """
        raise NotImplementedError


class SkillAuditor(BaseAuditor):
    """
    Skill Auditor - Does it demonstrate the intended capability?

    Primary Frame: Compositional + Classifier
    """

    auditor_type = "skill"

    def audit(
        self,
        artifact: str,
        eval_report: Dict[str, Any],
        runtime_config: Dict[str, Any],
    ) -> AuditorResult:
        metrics = eval_report.get("metrics", {})
        accuracy = metrics.get("task_accuracy", 0.0)

        claims = []
        grounds = []
        would_change_if = []

        # Check task accuracy
        if accuracy >= 0.8:
            claims.append(
                f"[assert|confident] Task demonstrates intended capability [ground:harness_accuracy={accuracy:.2f}] [conf:0.95] [state:confirmed]"
            )
            action = ActionClass.ACCEPT
            illocution = Illocution.ASSERT
            affect = Affect.CONFIDENT
        elif accuracy >= 0.6:
            claims.append(
                f"[assert|uncertain] Task partially demonstrates capability [ground:harness_accuracy={accuracy:.2f}] [conf:0.70] [state:provisional]"
            )
            would_change_if.append(f"harness_accuracy >= 0.80")
            action = ActionClass.TUNE_VECTOR
            illocution = Illocution.RECOMMEND
            affect = Affect.UNCERTAIN
        else:
            claims.append(
                f"[assert|concerned] Task fails to demonstrate capability [ground:harness_accuracy={accuracy:.2f}] [conf:0.90] [state:flagged]"
            )
            would_change_if.append(f"harness_accuracy >= 0.60")
            action = ActionClass.REJECT
            illocution = Illocution.REJECT
            affect = Affect.CONCERNED

        grounds.append(f"harness:task_accuracy={accuracy:.2f}")
        grounds.append(f"artifact:length={len(artifact)}")

        result = AuditorResult(
            auditor_type=self.auditor_type,
            verix={"illocution": illocution.value, "affect": affect.value},
            claims=claims,
            would_change_if=would_change_if,
            action_class=action.value,
            confidence=accuracy if accuracy > 0 else 0.5,
            grounds=grounds,
            # VCL: Skill auditor uses observation EVD (harness metrics are observed)
            vcl={
                "evd_type": "observation",
                "asp_type": "sov" if action == ActionClass.ACCEPT else "nesov",
                "confidence_ceiling": 0.95,
            },
        )
        return result.enforce_confidence_ceiling()


class PromptAuditor(BaseAuditor):
    """
    Prompt Auditor - Did compilation/config behave as intended?

    Primary Frame: Evidential
    """

    auditor_type = "prompt"

    def audit(
        self,
        artifact: str,
        eval_report: Dict[str, Any],
        runtime_config: Dict[str, Any],
    ) -> AuditorResult:
        metrics = eval_report.get("metrics", {})
        efficiency = metrics.get("token_efficiency", 0.0)

        claims = []
        grounds = []
        would_change_if = []

        # Check token efficiency as proxy for prompt effectiveness
        mode = runtime_config.get("mode", "unknown")
        frames = runtime_config.get("frames", {})
        active_frames = [k for k, v in frames.items() if v]

        if efficiency >= 0.7:
            claims.append(
                f"[assert|confident] Prompt compilation efficient for mode '{mode}' [ground:harness_efficiency={efficiency:.2f}] [conf:0.90] [state:confirmed]"
            )
            action = ActionClass.ACCEPT
            illocution = Illocution.ASSERT
            affect = Affect.CONFIDENT
        else:
            claims.append(
                f"[assert|concerned] Prompt compilation inefficient [ground:harness_efficiency={efficiency:.2f}] [conf:0.85] [state:flagged]"
            )
            would_change_if.append("harness_efficiency >= 0.70")
            would_change_if.append("fewer frames active")
            action = ActionClass.TUNE_VECTOR
            illocution = Illocution.WARN
            affect = Affect.CONCERNED

        grounds.append(f"harness:token_efficiency={efficiency:.2f}")
        grounds.append(f"config:mode={mode}")
        grounds.append(f"config:active_frames={active_frames}")

        result = AuditorResult(
            auditor_type=self.auditor_type,
            verix={"illocution": illocution.value, "affect": affect.value},
            claims=claims,
            would_change_if=would_change_if,
            action_class=action.value,
            confidence=efficiency if efficiency > 0 else 0.5,
            grounds=grounds,
            # VCL: Prompt auditor uses observation EVD (efficiency is observed)
            vcl={
                "evd_type": "observation",
                "asp_type": "sov" if action == ActionClass.ACCEPT else "nesov",
                "confidence_ceiling": 0.95,
            },
        )
        return result.enforce_confidence_ceiling()


class ExpertiseAuditor(BaseAuditor):
    """
    Expertise Auditor - Is domain reasoning sound for audience?

    Primary Frame: Honorific
    """

    auditor_type = "expertise"

    def audit(
        self,
        artifact: str,
        eval_report: Dict[str, Any],
        runtime_config: Dict[str, Any],
    ) -> AuditorResult:
        metrics = eval_report.get("metrics", {})
        robustness = metrics.get("edge_robustness", 0.0)

        claims = []
        grounds = []
        would_change_if = []

        # Check robustness as proxy for domain expertise application
        if robustness >= 0.75:
            claims.append(
                f"[assert|confident] Domain reasoning handles edge cases [ground:harness_robustness={robustness:.2f}] [conf:0.88] [state:confirmed]"
            )
            action = ActionClass.ACCEPT
            illocution = Illocution.ASSERT
            affect = Affect.CONFIDENT
        elif robustness >= 0.5:
            claims.append(
                f"[assert|uncertain] Domain reasoning partially robust [ground:harness_robustness={robustness:.2f}] [conf:0.70] [state:provisional]"
            )
            would_change_if.append("harness_robustness >= 0.75")
            action = ActionClass.TUNE_VECTOR
            illocution = Illocution.RECOMMEND
            affect = Affect.UNCERTAIN
        else:
            claims.append(
                f"[assert|concerned] Domain reasoning fragile at edges [ground:harness_robustness={robustness:.2f}] [conf:0.85] [state:flagged]"
            )
            would_change_if.append("harness_robustness >= 0.50")
            action = ActionClass.CODE_FIX
            illocution = Illocution.WARN
            affect = Affect.CONCERNED

        grounds.append(f"harness:edge_robustness={robustness:.2f}")

        result = AuditorResult(
            auditor_type=self.auditor_type,
            verix={"illocution": illocution.value, "affect": affect.value},
            claims=claims,
            would_change_if=would_change_if,
            action_class=action.value,
            confidence=robustness if robustness > 0 else 0.5,
            grounds=grounds,
            # VCL: Expertise auditor uses inference EVD (reasoning quality is inferred)
            vcl={
                "evd_type": "inference",
                "asp_type": "sov" if action == ActionClass.ACCEPT else "nesov",
                "confidence_ceiling": 0.70,  # Inference ceiling
            },
        )
        return result.enforce_confidence_ceiling()


class OutputAuditor(BaseAuditor):
    """
    Output Auditor - Does it meet acceptance criteria?

    Primary Frame: Classifier + Spatial

    This auditor uses the ACCEPTANCE CHECKLIST as its rubric.
    """

    auditor_type = "output"

    def audit(
        self,
        artifact: str,
        eval_report: Dict[str, Any],
        runtime_config: Dict[str, Any],
    ) -> AuditorResult:
        metrics = eval_report.get("metrics", {})
        consistency = metrics.get("epistemic_consistency", 0.0)
        overall = metrics.get("overall", 0.0)

        claims = []
        grounds = []
        would_change_if = []

        # Check overall score against acceptance threshold
        acceptance_threshold = 0.75

        if overall >= acceptance_threshold:
            claims.append(
                f"[assert|confident] Output meets acceptance criteria [ground:harness_overall={overall:.2f}] [conf:0.92] [state:confirmed]"
            )
            claims.append(
                f"[assert|confident] Epistemic consistency maintained [ground:harness_consistency={consistency:.2f}] [conf:0.88] [state:confirmed]"
            )
            action = ActionClass.ACCEPT
            illocution = Illocution.ASSERT
            affect = Affect.CONFIDENT
        elif overall >= 0.5:
            claims.append(
                f"[assert|uncertain] Output approaches acceptance [ground:harness_overall={overall:.2f}] [conf:0.75] [state:provisional]"
            )
            would_change_if.append(f"harness_overall >= {acceptance_threshold}")
            action = ActionClass.TUNE_VECTOR
            illocution = Illocution.RECOMMEND
            affect = Affect.UNCERTAIN
        else:
            claims.append(
                f"[assert|concerned] Output fails acceptance criteria [ground:harness_overall={overall:.2f}] [conf:0.90] [state:flagged]"
            )
            would_change_if.append("harness_overall >= 0.50")
            action = ActionClass.REJECT
            illocution = Illocution.REJECT
            affect = Affect.CONCERNED

        grounds.append(f"harness:overall={overall:.2f}")
        grounds.append(f"harness:epistemic_consistency={consistency:.2f}")
        grounds.append(f"threshold:acceptance={acceptance_threshold}")

        result = AuditorResult(
            auditor_type=self.auditor_type,
            verix={"illocution": illocution.value, "affect": affect.value},
            claims=claims,
            would_change_if=would_change_if,
            action_class=action.value,
            confidence=overall if overall > 0 else 0.5,
            grounds=grounds,
            # VCL: Output auditor uses observation EVD (acceptance is observed from harness)
            vcl={
                "evd_type": "observation",
                "asp_type": "sov" if action == ActionClass.ACCEPT else "nesov",
                "confidence_ceiling": 0.95,
            },
        )
        return result.enforce_confidence_ceiling()


class AuditorPanel:
    """
    Panel of all four auditors for consensus-based decisions.

    Implements auditor disagreement detection and consensus logic.
    Includes VCL v3.1.1 compliance validation.
    """

    def __init__(self):
        self.auditors = [
            SkillAuditor(),
            PromptAuditor(),
            ExpertiseAuditor(),
            OutputAuditor(),
        ]
        # Initialize VCL validator if available
        self.vcl_validator = VCLValidator() if VCL_AVAILABLE else None

    def audit_all(
        self,
        artifact: str,
        eval_report: Dict[str, Any],
        runtime_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run all auditors and aggregate results.

        Includes VCL compliance validation of artifact.

        Returns:
            Aggregated result with consensus analysis and VCL compliance
        """
        results = []
        for auditor in self.auditors:
            result = auditor.audit(artifact, eval_report, runtime_config)
            results.append(result.to_dict())

        # Analyze consensus
        actions = [r["action_class"] for r in results]
        accept_count = sum(1 for a in actions if a == "ACCEPT")
        reject_count = sum(1 for a in actions if a == "REJECT")

        # Determine consensus
        if reject_count >= 2:
            consensus = "REJECT"
            consensus_confidence = reject_count / len(actions)
        elif accept_count >= 3:
            consensus = "ACCEPT"
            consensus_confidence = accept_count / len(actions)
        else:
            consensus = "NEEDS_REVIEW"
            consensus_confidence = 0.5

        # Check for disagreement (triggers human gate)
        unique_actions = len(set(actions))
        disagreement = unique_actions >= 3

        # VCL compliance validation
        vcl_compliance = self._validate_vcl_compliance(artifact, runtime_config)

        return {
            "auditor_results": results,
            "consensus": {
                "decision": consensus,
                "confidence": consensus_confidence,
                "accept_count": accept_count,
                "reject_count": reject_count,
                "disagreement": disagreement,
                "unique_actions": unique_actions,
            },
            "vcl_compliance": vcl_compliance,
            "all_claims": [claim for r in results for claim in r["claims"]],
            "all_grounds": list(set(g for r in results for g in r["grounds"])),
        }

    def _validate_vcl_compliance(
        self,
        artifact: str,
        runtime_config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Validate artifact against VCL v3.1.1 requirements.

        Args:
            artifact: The artifact text to validate
            runtime_config: Current configuration

        Returns:
            VCL compliance result with score and violations
        """
        if not self.vcl_validator:
            return {
                "available": False,
                "score": 0.0,
                "violations": ["VCL validator not available"],
            }

        # Build VCL config from runtime_config
        vcl_slots = runtime_config.get("vcl_slots", {})
        verix_data = runtime_config.get("verix", {})

        compression_map = {
            "L0": VCLCompressionLevel.L0_INTERNAL,
            "L1": VCLCompressionLevel.L1_AUDIT,
            "L2": VCLCompressionLevel.L2_HUMAN,
        }
        compression = compression_map.get(
            verix_data.get("compression", "L2"),
            VCLCompressionLevel.L2_HUMAN
        )

        vcl_config = VCLConfig(
            evd_enforcement=vcl_slots.get("EVD", {}).get("enforcement", 2),
            asp_enforcement=vcl_slots.get("ASP", {}).get("enforcement", 2),
            compression=compression,
            require_ground=verix_data.get("require_ground", True),
            require_confidence=verix_data.get("require_confidence", True),
        )

        # Validate artifact
        result = self.vcl_validator.validate(artifact, vcl_config)

        return {
            "available": True,
            "passed": result.passed,
            "score": result.vcl_compliance_score,
            "checks": result.checks,
            "violations": result.violations,
        }


def run_auditor_panel(
    artifact_path: str,
    eval_report_path: str,
    runtime_config_path: str,
) -> Dict[str, Any]:
    """
    Convenience function to run auditor panel.

    Args:
        artifact_path: Path to artifact file
        eval_report_path: Path to eval_report.json
        runtime_config_path: Path to runtime_config.json

    Returns:
        Auditor panel results
    """
    from pathlib import Path
    import json

    artifact = Path(artifact_path).read_text(errors="ignore") if Path(artifact_path).exists() else ""
    eval_report = json.loads(Path(eval_report_path).read_text()) if Path(eval_report_path).exists() else {}
    runtime_config = json.loads(Path(runtime_config_path).read_text()) if Path(runtime_config_path).exists() else {}

    panel = AuditorPanel()
    return panel.audit_all(artifact, eval_report, runtime_config)
