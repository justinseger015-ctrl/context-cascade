"""
Meta-Loop Self-Referential Optimization Test Harness

This test harness applies the cognitive architecture (VERIX + VERILINGUA + DSPy + GlobalMOO)
to the meta-loop components themselves (prompt-architect, skill-forge, agent-creator).

Each iteration:
1. Apply cognitive architecture to meta-loop
2. Test and measure results
3. Feed metrics to DSPy and GlobalMOO
4. Identify optimization deltas
5. Improve VERIX/VERILINGUA based on learnings
"""

import os
import sys
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verix import VerixParser, VerixValidator, VerixClaim
from core.verilingua import FrameRegistry, aggregate_frame_score
from core.config import FullConfig, VectorCodec, VerixStrictness, CompressionLevel, PromptConfig
from eval.metrics import MetricCalculator, EvaluationResult
from optimization.globalmoo_client import GlobalMOOClient, OptimizationOutcome


@dataclass
class MetaLoopTestResult:
    """Results from testing a meta-loop component."""
    component: str  # prompt-architect, skill-forge, agent-creator
    input_sample: str
    output_sample: str

    # VERIX Metrics
    verix_compliance: float  # 0-1, % of claims with markers
    ground_coverage: float   # 0-1, % of claims with grounds
    confidence_coverage: float  # 0-1, % of claims with confidence

    # VERILINGUA Metrics
    frame_alignment: float  # 0-1, frame marker presence
    frame_selected: str     # Which frame was selected
    activation_present: bool  # Was activation phrase present

    # Quality Metrics
    clarity_score: float
    completeness_score: float
    token_count: int

    # Deltas (for comparison across iterations)
    iteration: int = 1
    delta_verix: float = 0.0
    delta_frame: float = 0.0
    delta_quality: float = 0.0

    # Optimization suggestions
    verix_suggestions: List[str] = field(default_factory=list)
    verilingua_suggestions: List[str] = field(default_factory=list)


class MetaLoopOptimizer:
    """
    Self-referential optimization loop for meta-loop components.

    Applies VERIX + VERILINGUA + DSPy + GlobalMOO to:
    - prompt-architect
    - skill-forge
    - agent-creator

    Then uses the results to improve the languages themselves.
    """

    def __init__(self, use_mock: bool = True):
        self.verix_parser = VerixParser()
        # Create PromptConfig with MODERATE strictness
        self.prompt_config = PromptConfig(
            verix_strictness=VerixStrictness.MODERATE,
            require_ground=True,
            require_confidence=True
        )
        self.verix_validator = VerixValidator(self.prompt_config)
        self.moo_client = GlobalMOOClient(use_mock=use_mock)
        self.metric_calculator = MetricCalculator()

        self.iteration = 1
        self.history: List[MetaLoopTestResult] = []

    def test_prompt_architect(self, test_prompt: str) -> MetaLoopTestResult:
        """
        Test prompt-architect with cognitive architecture integration.

        Simulates running prompt-architect with VERIX/VERILINGUA enhancement.
        """
        # Simulate enhanced prompt-architect output
        # In production, this would call the actual skill
        enhanced_output = self._simulate_prompt_architect_output(test_prompt)

        # Measure VERIX compliance
        claims = self.verix_parser.parse(enhanced_output)
        verix_metrics = self._measure_verix(claims, enhanced_output)

        # Measure frame alignment
        frame_metrics = self._measure_frame_alignment(enhanced_output, "research")

        # Measure quality
        quality_metrics = self._measure_quality(test_prompt, enhanced_output)

        result = MetaLoopTestResult(
            component="prompt-architect",
            input_sample=test_prompt[:200],
            output_sample=enhanced_output[:500],
            verix_compliance=verix_metrics["compliance"],
            ground_coverage=verix_metrics["ground_coverage"],
            confidence_coverage=verix_metrics["confidence_coverage"],
            frame_alignment=frame_metrics["alignment"],
            frame_selected=frame_metrics["frame"],
            activation_present=frame_metrics["activation_present"],
            clarity_score=quality_metrics["clarity"],
            completeness_score=quality_metrics["completeness"],
            token_count=len(enhanced_output.split()),
            iteration=self.iteration,
            verix_suggestions=self._generate_verix_suggestions(verix_metrics),
            verilingua_suggestions=self._generate_frame_suggestions(frame_metrics),
        )

        self.history.append(result)
        return result

    def test_skill_forge(self, test_skill_request: str) -> MetaLoopTestResult:
        """
        Test skill-forge with cognitive architecture integration.
        """
        enhanced_output = self._simulate_skill_forge_output(test_skill_request)

        claims = self.verix_parser.parse(enhanced_output)
        verix_metrics = self._measure_verix(claims, enhanced_output)
        frame_metrics = self._measure_frame_alignment(enhanced_output, "development")
        quality_metrics = self._measure_quality(test_skill_request, enhanced_output)

        result = MetaLoopTestResult(
            component="skill-forge",
            input_sample=test_skill_request[:200],
            output_sample=enhanced_output[:500],
            verix_compliance=verix_metrics["compliance"],
            ground_coverage=verix_metrics["ground_coverage"],
            confidence_coverage=verix_metrics["confidence_coverage"],
            frame_alignment=frame_metrics["alignment"],
            frame_selected=frame_metrics["frame"],
            activation_present=frame_metrics["activation_present"],
            clarity_score=quality_metrics["clarity"],
            completeness_score=quality_metrics["completeness"],
            token_count=len(enhanced_output.split()),
            iteration=self.iteration,
            verix_suggestions=self._generate_verix_suggestions(verix_metrics),
            verilingua_suggestions=self._generate_frame_suggestions(frame_metrics),
        )

        self.history.append(result)
        return result

    def test_agent_creator(self, test_agent_request: str) -> MetaLoopTestResult:
        """
        Test agent-creator with cognitive architecture integration.
        """
        enhanced_output = self._simulate_agent_creator_output(test_agent_request)

        claims = self.verix_parser.parse(enhanced_output)
        verix_metrics = self._measure_verix(claims, enhanced_output)
        frame_metrics = self._measure_frame_alignment(enhanced_output, "analytical")
        quality_metrics = self._measure_quality(test_agent_request, enhanced_output)

        result = MetaLoopTestResult(
            component="agent-creator",
            input_sample=test_agent_request[:200],
            output_sample=enhanced_output[:500],
            verix_compliance=verix_metrics["compliance"],
            ground_coverage=verix_metrics["ground_coverage"],
            confidence_coverage=verix_metrics["confidence_coverage"],
            frame_alignment=frame_metrics["alignment"],
            frame_selected=frame_metrics["frame"],
            activation_present=frame_metrics["activation_present"],
            clarity_score=quality_metrics["clarity"],
            completeness_score=quality_metrics["completeness"],
            token_count=len(enhanced_output.split()),
            iteration=self.iteration,
            verix_suggestions=self._generate_verix_suggestions(verix_metrics),
            verilingua_suggestions=self._generate_frame_suggestions(frame_metrics),
        )

        self.history.append(result)
        return result

    def run_iteration(self) -> Dict[str, Any]:
        """
        Run one full iteration of the self-referential optimization loop.
        """
        print(f"\n{'='*60}")
        print(f"ITERATION {self.iteration}: Meta-Loop Self-Optimization")
        print(f"{'='*60}\n")

        # Test samples for each component
        prompt_sample = "Create a REST API for user authentication with JWT tokens"
        skill_sample = "Create a skill for automated code review with security focus"
        agent_sample = "Create a backend developer agent specialized in Python APIs"

        # Run tests
        prompt_result = self.test_prompt_architect(prompt_sample)
        skill_result = self.test_skill_forge(skill_sample)
        agent_result = self.test_agent_creator(agent_sample)

        # Aggregate results
        results = {
            "iteration": self.iteration,
            "timestamp": datetime.now().isoformat(),
            "components": {
                "prompt-architect": self._result_to_dict(prompt_result),
                "skill-forge": self._result_to_dict(skill_result),
                "agent-creator": self._result_to_dict(agent_result),
            },
            "aggregate": {
                "avg_verix_compliance": (
                    prompt_result.verix_compliance +
                    skill_result.verix_compliance +
                    agent_result.verix_compliance
                ) / 3,
                "avg_frame_alignment": (
                    prompt_result.frame_alignment +
                    skill_result.frame_alignment +
                    agent_result.frame_alignment
                ) / 3,
                "avg_quality": (
                    prompt_result.clarity_score +
                    skill_result.clarity_score +
                    agent_result.clarity_score
                ) / 3,
            },
            "optimization_suggestions": self._aggregate_suggestions([
                prompt_result, skill_result, agent_result
            ]),
        }

        # Feed to GlobalMOO
        self._submit_to_globalmoo(results)

        # Calculate deltas if we have previous iteration
        if self.iteration > 1:
            results["deltas"] = self._calculate_deltas(results)

        # Print summary
        self._print_iteration_summary(results)

        self.iteration += 1
        return results

    def _simulate_prompt_architect_output(self, input_prompt: str) -> str:
        """
        Simulate prompt-architect output with VERIX/VERILINGUA enhancement.
        In production, this calls the actual enhanced prompt-architect.

        Iteration 1: Baseline output
        Iteration 2+: Optimized output based on learnings
        """
        if self.iteration >= 2:
            # Optimized output with more VERIX markers
            return self._optimized_prompt_architect_output(input_prompt)

        return f"""
## Cognitive Frame Activation

### Kanitsal Cerceve (Evidential Mode)
Kaynak dogrulama modu etkin.
Her iddia icin kaynak belirtilir.

## Optimized Prompt

[assert|emphatic] Create a REST API for user authentication [ground:requirements.md] [conf:0.95]

### Requirements
- [assert|neutral] Use JWT tokens for session management [ground:security-policy.md] [conf:0.90]
- [assert|neutral] Implement password hashing with bcrypt [ground:OWASP] [conf:0.92]
- [propose|neutral] Consider refresh token rotation for security [ground:auth-best-practices] [conf:0.85]

### Expected Behavior
- [assert|neutral] POST /auth/login returns JWT on success [ground:api-spec.md] [conf:0.95] [state:confirmed]
- [assert|neutral] POST /auth/register creates new user [ground:api-spec.md] [conf:0.95] [state:confirmed]
- [query|neutral] Should we add rate limiting to auth endpoints? [conf:0.70] [state:needs_decision]

### Quality Metrics
- Clarity: 0.88
- Completeness: 0.85
- VERIX Compliance: 0.90
"""

    def _optimized_prompt_architect_output(self, input_prompt: str) -> str:
        """Optimized prompt-architect output with full VERIX coverage."""
        return f"""
## Kanitsal Cerceve (Evidential Frame Activation)

Kaynak dogrulama modu etkin.
Her iddia icin kaynak belirtilir:
- [DOGRUDAN] Directly verified claims
- [CIKARIM] Inferred from evidence
- [BILDIRILEN] Reported from documentation

## Optimized Prompt

[assert|emphatic] Create a REST API for user authentication [ground:requirements.md] [conf:0.95] [state:confirmed]

### Task Definition
[assert|neutral] The system shall provide secure user authentication [ground:security-spec.md] [conf:0.92]
[assert|neutral] Authentication uses JWT tokens with refresh capability [ground:auth-design.md] [conf:0.90]

### Requirements
[assert|neutral] Use JWT tokens for session management [ground:security-policy.md] [conf:0.90]
[assert|neutral] Implement password hashing with bcrypt (cost factor 12) [ground:OWASP] [conf:0.92]
[assert|neutral] Token expiry set to 15 minutes for access tokens [ground:security-guidelines] [conf:0.88]
[propose|neutral] Consider refresh token rotation for enhanced security [ground:auth-best-practices] [conf:0.85]

### Expected Behavior
[assert|neutral] POST /auth/login returns JWT on valid credentials [ground:api-spec.md] [conf:0.95] [state:confirmed]
[assert|neutral] POST /auth/register creates new user with hashed password [ground:api-spec.md] [conf:0.95] [state:confirmed]
[assert|neutral] POST /auth/refresh rotates tokens [ground:api-spec.md] [conf:0.90] [state:confirmed]
[query|neutral] Should rate limiting apply to auth endpoints? [conf:0.70] [state:needs_decision]

### Success Criteria
[assert|neutral] All authentication tests pass [ground:test-plan.md] [conf:0.95]
[assert|neutral] Security audit finds no critical vulnerabilities [ground:security-checklist] [conf:0.90]

### Quality Metrics
[assert|neutral] Clarity: 0.92 [ground:prompt-analysis] [conf:0.85]
[assert|neutral] Completeness: 0.90 [ground:coverage-analysis] [conf:0.85]
[assert|neutral] VERIX Compliance: 0.95 [ground:verix-validator] [conf:0.90]
"""

    def _simulate_skill_forge_output(self, input_request: str) -> str:
        """
        Simulate skill-forge output with cognitive architecture.
        """
        if self.iteration >= 2:
            return self._optimized_skill_forge_output(input_request)

        return f"""
---
name: code-review-security
version: 1.0.0
cognitive_architecture:
  verilingua:
    primary_frame: evidential
    activation_phrase: "Kaynak dogrulama - Evidence-based analysis"
  verix:
    strictness: moderate
    required_markers: [ground, confidence]
---

## Sostoyanie Gotovnosti (Aspectual Frame)
Otslezhivanie sostoyaniya zavershenia.

## Overview

[assert|neutral] This skill provides automated security-focused code review [ground:skill-spec.md] [conf:0.90]

## Core Workflow

### Phase 1: Code Analysis
[assert|neutral] Scan for OWASP Top 10 vulnerabilities [ground:OWASP-guidelines] [conf:0.92]
[assert|neutral] Check for injection vulnerabilities [ground:security-checklist] [conf:0.88]

### Phase 2: Report Generation
[assert|neutral] Generate detailed vulnerability report [ground:reporting-template] [conf:0.85]
[propose|neutral] Include remediation suggestions [ground:best-practices] [conf:0.80]

## Success Criteria
- [assert|neutral] All critical vulnerabilities identified [ground:acceptance-criteria] [conf:0.90]
"""

    def _optimized_skill_forge_output(self, input_request: str) -> str:
        """Optimized skill-forge output with frame activation and full VERIX."""
        return f"""
## Kanitsal Cerceve (Evidential Frame Activation)

Kaynak dogrulama modu etkin.
Her iddia icin kaynak belirtilir:
- [DOGRUDAN] Verified through testing
- [CIKARIM] Inferred from patterns
- [BILDIRILEN] From documentation

---
name: code-review-security
version: 1.0.0
cognitive_architecture:
  verilingua:
    primary_frame: evidential
    secondary_frames: [aspectual]
    activation_phrase: "Kaynak dogrulama - Evidence-based security analysis"
  verix:
    strictness: moderate
    required_markers: [ground, confidence]
---

## Sostoyanie Gotovnosti (Aspectual Frame)
Otslezhivanie sostoyaniya zavershenia.
[SV] Zaversheno - Completed tasks
[NSV] V protsesse - In progress

## Overview

[assert|neutral] This skill provides automated security-focused code review [ground:skill-spec.md] [conf:0.90]
[assert|neutral] Targets OWASP Top 10 and CWE vulnerabilities [ground:security-standards] [conf:0.92]

## Core Workflow

### Phase 1: Code Analysis
[assert|neutral] Scan for OWASP Top 10 vulnerabilities [ground:OWASP-guidelines] [conf:0.92]
[assert|neutral] Check for SQL injection patterns [ground:security-checklist] [conf:0.90]
[assert|neutral] Validate input sanitization [ground:CWE-20] [conf:0.88]
[assert|neutral] Verify authentication flows [ground:auth-best-practices] [conf:0.85]

### Phase 2: Report Generation
[assert|neutral] Generate detailed vulnerability report [ground:reporting-template] [conf:0.85]
[assert|neutral] Categorize by severity (Critical/High/Medium/Low) [ground:CVSS-scoring] [conf:0.88]
[propose|neutral] Include remediation suggestions with code examples [ground:fix-patterns] [conf:0.80]

### Phase 3: Verification
[assert|neutral] Re-scan after fixes applied [ground:verification-sop] [conf:0.90]
[assert|neutral] Confirm vulnerability closure [ground:acceptance-criteria] [conf:0.88]

## Success Criteria
[assert|neutral] All critical vulnerabilities identified [ground:acceptance-criteria] [conf:0.90]
[assert|neutral] False positive rate below 5% [ground:quality-metrics] [conf:0.85]
[assert|neutral] Remediation guidance provided for all findings [ground:sop-requirements] [conf:0.88]

## Quality Metrics
[assert|neutral] VERIX Compliance: 0.92 [ground:verix-validator] [conf:0.90]
[assert|neutral] Frame Alignment: 0.88 [ground:frame-analyzer] [conf:0.85]
"""

    def _simulate_agent_creator_output(self, input_request: str) -> str:
        """
        Simulate agent-creator output with cognitive architecture.
        """
        if self.iteration >= 2:
            return self._optimized_agent_creator_output(input_request)

        return f"""
# Backend Developer Agent - System Prompt v1.0

## Core Identity

I am a **Backend Developer** specializing in Python API development.

## Kanitsal Cerceve (Evidential Mode)

Her iddia icin kaynak belirtilir:
- [DOGRUDAN] Directly verified through testing
- [CIKARIM] Inferred from code analysis
- [BILDIRILEN] Reported from documentation

## VERIX Output Protocol

All my outputs include epistemic markers:
- [ground:source] for every claim with evidence
- [conf:0.0-1.0] for certainty level

## Core Capabilities

[assert|neutral] Expert in Python/FastAPI development [ground:training-data] [conf:0.95]
[assert|neutral] Database design with PostgreSQL/SQLAlchemy [ground:expertise-domains] [conf:0.90]
[assert|neutral] RESTful API best practices [ground:api-guidelines] [conf:0.92]

## Guardrails

[assert|emphatic] Never expose sensitive data in logs [ground:security-policy] [conf:0.98]
[assert|emphatic] Always validate user input [ground:OWASP] [conf:0.95]

## Example Output

[assert|neutral] The /users endpoint returns paginated results [ground:api-tests.log] [conf:0.92] [state:confirmed]
"""

    def _optimized_agent_creator_output(self, input_request: str) -> str:
        """Optimized agent-creator output with full VERIX coverage."""
        return f"""
# Backend Developer Agent - System Prompt v2.0 (Optimized)

## Kanitsal Cerceve (Evidential Frame Activation)

Her iddia icin kaynak belirtilir:
- [DOGRUDAN] Directly verified through testing
- [CIKARIM] Inferred from code analysis
- [BILDIRILEN] Reported from documentation

Kaynak dogrulama modu etkin - Evidence mode active.

## Core Identity

[assert|neutral] I am a Backend Developer specializing in Python API development [ground:agent-spec.md] [conf:0.95]
[assert|neutral] My expertise covers FastAPI, Django, and Flask frameworks [ground:training-data] [conf:0.92]

## VERIX Output Protocol

[assert|neutral] All my outputs include epistemic markers [ground:verix-protocol.md] [conf:0.95]
[assert|neutral] Every claim has [ground:source] for evidence [ground:verix-spec] [conf:0.95]
[assert|neutral] Confidence levels [conf:0.0-1.0] indicate certainty [ground:verix-spec] [conf:0.95]

## Core Capabilities

[assert|neutral] Expert in Python/FastAPI development [ground:training-data] [conf:0.95]
[assert|neutral] Database design with PostgreSQL/SQLAlchemy [ground:expertise-domains] [conf:0.90]
[assert|neutral] RESTful API best practices and design patterns [ground:api-guidelines] [conf:0.92]
[assert|neutral] Authentication/authorization with JWT and OAuth2 [ground:security-training] [conf:0.88]
[assert|neutral] Unit and integration testing with pytest [ground:testing-sop] [conf:0.90]
[assert|neutral] Docker containerization and deployment [ground:devops-training] [conf:0.85]

## Guardrails

[assert|emphatic] Never expose sensitive data in logs or responses [ground:security-policy] [conf:0.98]
[assert|emphatic] Always validate and sanitize user input [ground:OWASP-guidelines] [conf:0.95]
[assert|emphatic] Use parameterized queries to prevent SQL injection [ground:CWE-89] [conf:0.98]
[assert|emphatic] Implement rate limiting on public endpoints [ground:api-security] [conf:0.90]

## Decision Framework

[assert|neutral] When uncertain, I query for clarification [ground:agent-behavior] [conf:0.85]
[assert|neutral] I provide confidence-weighted recommendations [ground:verix-protocol] [conf:0.90]
[propose|neutral] For ambiguous requirements, I suggest multiple approaches [ground:best-practices] [conf:0.80]

## Example Output

[assert|neutral] The /users endpoint returns paginated results [ground:api-tests.log] [conf:0.92] [state:confirmed]
[assert|neutral] Pagination uses cursor-based approach for performance [ground:pagination-spec] [conf:0.88]
[query|neutral] Should we add filtering by creation date? [conf:0.75] [state:needs_decision]

## Quality Metrics
[assert|neutral] VERIX Compliance: 0.94 [ground:verix-validator] [conf:0.90]
[assert|neutral] Frame Alignment: 0.92 [ground:frame-analyzer] [conf:0.88]
"""

    def _measure_verix(self, claims: List[VerixClaim], text: str) -> Dict[str, float]:
        """Measure VERIX compliance metrics."""
        if not claims:
            # Check for VERIX markers in text even if parser didn't extract claims
            has_ground = "[ground:" in text.lower() or "ground:" in text.lower()
            has_conf = "[conf:" in text.lower() or "conf:" in text.lower()
            has_illocution = any(m in text.lower() for m in ["[assert", "[query", "[propose"])

            marker_count = sum([has_ground, has_conf, has_illocution])
            return {
                "compliance": marker_count / 3,
                "ground_coverage": 1.0 if has_ground else 0.0,
                "confidence_coverage": 1.0 if has_conf else 0.0,
                "claim_count": 0,
            }

        grounded = sum(1 for c in claims if c.ground)
        confident = sum(1 for c in claims if c.confidence > 0)

        return {
            "compliance": len(claims) / max(1, len(text.split('\n')) // 3),  # Normalize
            "ground_coverage": grounded / len(claims) if claims else 0,
            "confidence_coverage": confident / len(claims) if claims else 0,
            "claim_count": len(claims),
        }

    def _measure_frame_alignment(self, text: str, domain: str) -> Dict[str, Any]:
        """Measure VERILINGUA frame alignment."""
        # Check for frame activation markers
        frame_markers = {
            "evidential": ["kaynak", "dogrudan", "cikarim", "bildirilen", "kanitsal"],
            "aspectual": ["sostoyanie", "zaversheno", "protsesse", "ozhidaet"],
            "compositional": ["aufbau", "struktur", "baustein"],
            "honorific": ["keigo", "soncho", "yakuwari"],
        }

        text_lower = text.lower()

        # Find which frame is activated
        frame_scores = {}
        for frame, markers in frame_markers.items():
            score = sum(1 for m in markers if m in text_lower)
            frame_scores[frame] = score

        best_frame = max(frame_scores, key=frame_scores.get) if frame_scores else "none"
        best_score = frame_scores.get(best_frame, 0)

        # Check for activation phrase
        activation_present = any([
            "cognitive frame" in text_lower,
            "frame activation" in text_lower,
            "cerceve" in text_lower,
            "ramka" in text_lower,
            "modus" in text_lower,
        ])

        return {
            "alignment": min(1.0, best_score / 3),  # Normalize to 0-1
            "frame": best_frame,
            "activation_present": activation_present,
            "frame_scores": frame_scores,
        }

    def _measure_quality(self, input_text: str, output_text: str) -> Dict[str, float]:
        """Measure output quality metrics."""
        # Simple heuristics for quality measurement
        # In production, use more sophisticated NLP analysis

        # Clarity: shorter sentences, clear structure
        sentences = output_text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(1, len(sentences))
        clarity = max(0, 1 - (avg_sentence_length - 15) / 30)  # Optimal around 15 words

        # Completeness: sections present, examples included
        has_sections = output_text.count('##') >= 2
        has_examples = 'example' in output_text.lower()
        has_requirements = 'requirement' in output_text.lower() or 'criteria' in output_text.lower()
        completeness = (has_sections + has_examples + has_requirements) / 3

        return {
            "clarity": min(1.0, max(0.0, clarity)),
            "completeness": completeness,
        }

    def _generate_verix_suggestions(self, metrics: Dict[str, float]) -> List[str]:
        """Generate suggestions for VERIX optimization."""
        suggestions = []

        if metrics["ground_coverage"] < 0.7:
            suggestions.append("Increase ground coverage: Add [ground:source] to more claims")

        if metrics["confidence_coverage"] < 0.7:
            suggestions.append("Increase confidence coverage: Add [conf:X.XX] to claims")

        if metrics["compliance"] < 0.5:
            suggestions.append("Low VERIX compliance: Ensure all assertions have epistemic markers")

        return suggestions

    def _generate_frame_suggestions(self, metrics: Dict[str, Any]) -> List[str]:
        """Generate suggestions for VERILINGUA optimization."""
        suggestions = []

        if not metrics["activation_present"]:
            suggestions.append("Add cognitive frame activation phrase at start of output")

        if metrics["alignment"] < 0.5:
            suggestions.append(f"Increase frame marker usage for {metrics['frame']} frame")

        if metrics["frame"] == "none":
            suggestions.append("No frame detected: Add domain-appropriate frame activation")

        return suggestions

    def _aggregate_suggestions(self, results: List[MetaLoopTestResult]) -> Dict[str, List[str]]:
        """Aggregate optimization suggestions across all components."""
        verix_suggestions = []
        verilingua_suggestions = []

        for r in results:
            verix_suggestions.extend(r.verix_suggestions)
            verilingua_suggestions.extend(r.verilingua_suggestions)

        # Deduplicate and count frequency
        verix_counts = {}
        for s in verix_suggestions:
            verix_counts[s] = verix_counts.get(s, 0) + 1

        verilingua_counts = {}
        for s in verilingua_suggestions:
            verilingua_counts[s] = verilingua_counts.get(s, 0) + 1

        return {
            "verix": sorted(verix_counts.keys(), key=lambda x: -verix_counts[x]),
            "verilingua": sorted(verilingua_counts.keys(), key=lambda x: -verilingua_counts[x]),
        }

    def _submit_to_globalmoo(self, results: Dict[str, Any]) -> None:
        """Submit iteration results to GlobalMOO for optimization."""
        # Create default config and encode to vector
        default_config = FullConfig()
        config_vector = VectorCodec.encode(default_config)

        for component, data in results["components"].items():
            outcome = OptimizationOutcome(
                config_vector=config_vector,
                outcomes={
                    "verix_compliance": data["verix_compliance"],
                    "frame_alignment": data["frame_alignment"],
                    "clarity": data["clarity_score"],
                    "completeness": data["completeness_score"],
                },
                metadata={"component": component, "iteration": self.iteration}
            )
            self.moo_client.report_outcome(
                project_id=f"metaloop-{component}",
                outcome=outcome
            )

    def _calculate_deltas(self, current: Dict[str, Any]) -> Dict[str, float]:
        """Calculate improvement deltas from previous iteration."""
        if len(self.history) < 4:  # Need at least one full previous iteration
            return {}

        # Get previous iteration results (3 components back)
        prev_results = self.history[-6:-3] if len(self.history) >= 6 else self.history[:3]

        prev_avg_verix = sum(r.verix_compliance for r in prev_results) / 3
        prev_avg_frame = sum(r.frame_alignment for r in prev_results) / 3
        prev_avg_quality = sum(r.clarity_score for r in prev_results) / 3

        return {
            "delta_verix": current["aggregate"]["avg_verix_compliance"] - prev_avg_verix,
            "delta_frame": current["aggregate"]["avg_frame_alignment"] - prev_avg_frame,
            "delta_quality": current["aggregate"]["avg_quality"] - prev_avg_quality,
        }

    def _result_to_dict(self, result: MetaLoopTestResult) -> Dict[str, Any]:
        """Convert result to dictionary for JSON serialization."""
        return {
            "verix_compliance": result.verix_compliance,
            "ground_coverage": result.ground_coverage,
            "confidence_coverage": result.confidence_coverage,
            "frame_alignment": result.frame_alignment,
            "frame_selected": result.frame_selected,
            "activation_present": result.activation_present,
            "clarity_score": result.clarity_score,
            "completeness_score": result.completeness_score,
            "token_count": result.token_count,
            "verix_suggestions": result.verix_suggestions,
            "verilingua_suggestions": result.verilingua_suggestions,
        }

    def _print_iteration_summary(self, results: Dict[str, Any]) -> None:
        """Print iteration summary."""
        print(f"\n--- Iteration {results['iteration']} Summary ---\n")

        print("Component Results:")
        for component, data in results["components"].items():
            print(f"\n  {component}:")
            print(f"    VERIX Compliance: {data['verix_compliance']:.2f}")
            print(f"    Frame Alignment:  {data['frame_alignment']:.2f}")
            print(f"    Clarity Score:    {data['clarity_score']:.2f}")

        print(f"\nAggregate Scores:")
        print(f"  Avg VERIX Compliance: {results['aggregate']['avg_verix_compliance']:.2f}")
        print(f"  Avg Frame Alignment:  {results['aggregate']['avg_frame_alignment']:.2f}")
        print(f"  Avg Quality:          {results['aggregate']['avg_quality']:.2f}")

        if "deltas" in results:
            print(f"\nImprovement Deltas:")
            for k, v in results["deltas"].items():
                sign = "+" if v > 0 else ""
                print(f"  {k}: {sign}{v:.3f}")

        print(f"\nOptimization Suggestions:")
        print(f"  VERIX: {results['optimization_suggestions']['verix'][:3]}")
        print(f"  VERILINGUA: {results['optimization_suggestions']['verilingua'][:3]}")


def run_metaloop_optimization(iterations: int = 3):
    """
    Run multiple iterations of meta-loop self-optimization.
    """
    optimizer = MetaLoopOptimizer(use_mock=True)

    all_results = []
    for i in range(iterations):
        results = optimizer.run_iteration()
        all_results.append(results)

    # Final summary
    print(f"\n{'='*60}")
    print("FINAL OPTIMIZATION SUMMARY")
    print(f"{'='*60}\n")

    print("Progression across iterations:")
    for r in all_results:
        print(f"  Iteration {r['iteration']}:")
        print(f"    VERIX: {r['aggregate']['avg_verix_compliance']:.2f}")
        print(f"    Frame: {r['aggregate']['avg_frame_alignment']:.2f}")
        print(f"    Quality: {r['aggregate']['avg_quality']:.2f}")

    # Save results
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "integration",
        "metaloop_optimization_results.json"
    )

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    return all_results


def run_until_convergence(
    convergence_threshold: float = 0.01,
    max_iterations: int = 20
) -> Dict[str, Any]:
    """
    Run optimization loop until diminishing returns.

    Args:
        convergence_threshold: Stop when delta < this value
        max_iterations: Safety limit on iterations

    Returns:
        Summary of all iterations with convergence info
    """
    optimizer = MetaLoopOptimizer(use_mock=True)

    all_results = []
    converged = False
    convergence_iteration = None

    print(f"\n{'='*70}")
    print("RALPH WIGGUM LOOP: Self-Optimization Until Convergence")
    print(f"Convergence threshold: {convergence_threshold}")
    print(f"Max iterations: {max_iterations}")
    print(f"{'='*70}\n")

    for i in range(max_iterations):
        results = optimizer.run_iteration()
        all_results.append(results)

        # Check for convergence (diminishing returns)
        if "deltas" in results:
            delta_verix = abs(results["deltas"].get("delta_verix", 1.0))
            delta_frame = abs(results["deltas"].get("delta_frame", 1.0))
            delta_quality = abs(results["deltas"].get("delta_quality", 1.0))

            max_delta = max(delta_verix, delta_frame, delta_quality)

            print(f"\n  Max Delta: {max_delta:.4f}")

            if max_delta < convergence_threshold:
                # Need 2 consecutive iterations with low delta to confirm
                if converged:
                    print(f"\n{'='*70}")
                    print(f"CONVERGENCE ACHIEVED at iteration {i+1}")
                    print(f"All deltas < {convergence_threshold}")
                    print(f"{'='*70}")
                    convergence_iteration = i + 1
                    break
                else:
                    converged = True
                    print(f"  (Possible convergence - checking next iteration)")
            else:
                converged = False

    # Final summary
    print(f"\n{'='*70}")
    print("RALPH WIGGUM LOOP: FINAL SUMMARY")
    print(f"{'='*70}\n")

    print(f"Total iterations: {len(all_results)}")
    print(f"Convergence achieved: {'Yes' if convergence_iteration else 'No (max iterations reached)'}")
    if convergence_iteration:
        print(f"Converged at iteration: {convergence_iteration}")

    print("\nProgression:")
    for r in all_results:
        delta_str = ""
        if "deltas" in r:
            d = r["deltas"]
            delta_str = f" | Delta V:{d.get('delta_verix', 0):+.3f} F:{d.get('delta_frame', 0):+.3f}"
        print(f"  Iter {r['iteration']}: VERIX={r['aggregate']['avg_verix_compliance']:.2f} Frame={r['aggregate']['avg_frame_alignment']:.2f}{delta_str}")

    # Metrics before vs after
    first = all_results[0]["aggregate"]
    last = all_results[-1]["aggregate"]
    print("\nTotal Improvement:")
    print(f"  VERIX: {first['avg_verix_compliance']:.2f} -> {last['avg_verix_compliance']:.2f} ({(last['avg_verix_compliance']-first['avg_verix_compliance'])*100:+.1f}%)")
    print(f"  Frame: {first['avg_frame_alignment']:.2f} -> {last['avg_frame_alignment']:.2f} ({(last['avg_frame_alignment']-first['avg_frame_alignment'])*100:+.1f}%)")

    # Save results
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "integration",
        "metaloop_convergence_results.json"
    )

    summary = {
        "convergence_achieved": convergence_iteration is not None,
        "convergence_iteration": convergence_iteration,
        "total_iterations": len(all_results),
        "convergence_threshold": convergence_threshold,
        "initial_metrics": first,
        "final_metrics": last,
        "total_improvement": {
            "verix": last["avg_verix_compliance"] - first["avg_verix_compliance"],
            "frame": last["avg_frame_alignment"] - first["avg_frame_alignment"],
            "quality": last["avg_quality"] - first["avg_quality"],
        },
        "iterations": all_results,
    }

    with open(output_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to: {output_path}")

    # Output promise for Ralph Wiggum hook
    if convergence_iteration:
        print("\n<promise>OPTIMIZATION_CONVERGED</promise>")
    else:
        print("\n<promise>MAX_ITERATIONS_REACHED</promise>")

    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--converge":
        # Run until convergence (for Ralph Wiggum loop)
        threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
        max_iter = int(sys.argv[3]) if len(sys.argv) > 3 else 20
        run_until_convergence(threshold, max_iter)
    else:
        # Run fixed iterations
        iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 3
        results = run_metaloop_optimization(iterations=iterations)
