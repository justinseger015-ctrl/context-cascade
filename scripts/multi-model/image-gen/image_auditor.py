"""
Image Auditor - Automated quality validation for generated images.
Uses vision model to evaluate against a rubric based on visual-art-composition framework.

Integrates with Ralph Loop for iterative refinement until quality threshold met.
"""

import os
import base64
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum

# Try to import anthropic for Claude vision
try:
    import anthropic
    CLAUDE_AVAILABLE = True
except ImportError:
    CLAUDE_AVAILABLE = False

# Try to import openai for GPT-4V
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AuditSeverity(Enum):
    """Severity levels for audit findings."""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    CRITICAL = "critical"


@dataclass
class AuditFinding:
    """Single audit finding."""
    category: str
    severity: AuditSeverity
    message: str
    suggestion: Optional[str] = None


@dataclass
class AuditResult:
    """Complete audit result for an image."""
    passed: bool
    score: float  # 0.0 to 1.0
    findings: List[AuditFinding] = field(default_factory=list)
    prompt_feedback: Optional[str] = None  # Specific prompt improvements
    regenerate_prompt: Optional[str] = None  # Complete regeneration prompt if failed

    def to_dict(self) -> Dict:
        return {
            "passed": self.passed,
            "score": self.score,
            "findings": [
                {
                    "category": f.category,
                    "severity": f.severity.value,
                    "message": f.message,
                    "suggestion": f.suggestion
                }
                for f in self.findings
            ],
            "prompt_feedback": self.prompt_feedback,
            "regenerate_prompt": self.regenerate_prompt
        }


# Audit rubric based on visual-art-composition framework
AUDIT_RUBRIC = """
# Image Quality Audit Rubric

Evaluate the image against these criteria. For each, provide a score (0-10) and specific feedback.

## 1. TEXT ARTIFACTS (Critical - Auto-Fail if present)
- Are there ANY visible text, letters, numbers, or symbols that look like text?
- Are there garbled/distorted text-like artifacts?
- Score 0 if ANY text artifacts present, 10 if completely clean

## 2. CONCEPT ALIGNMENT (Weight: 30%)
- Does the image communicate the intended concept/message?
- Is the visual metaphor clear and appropriate?
- Would a viewer understand the intended meaning?

## 3. PROFESSIONAL QUALITY (Weight: 25%)
- Is this suitable for a professional LinkedIn banner?
- Is the composition balanced and visually appealing?
- Are there any obvious AI artifacts (weird hands, floating objects, impossible geometry)?

## 4. COLOR PALETTE (Weight: 15%)
- Does the color scheme match the intended palette from the prompt?
- Are colors harmonious and professional?
- Is there appropriate contrast for readability as a banner?

## 5. AESTHETIC COHERENCE (Weight: 15%)
- Do all elements work together as a unified composition?
- Is there a clear focal point?
- Does negative space enhance rather than detract?

## 6. TECHNICAL QUALITY (Weight: 15%)
- Is the resolution appropriate (no pixelation)?
- Are edges clean (no aliasing issues)?
- Is lighting consistent throughout?

## Output Format (JSON):
{
  "text_artifacts": {"score": 0-10, "found": true/false, "details": "..."},
  "concept_alignment": {"score": 0-10, "feedback": "..."},
  "professional_quality": {"score": 0-10, "feedback": "..."},
  "color_palette": {"score": 0-10, "feedback": "..."},
  "aesthetic_coherence": {"score": 0-10, "feedback": "..."},
  "technical_quality": {"score": 0-10, "feedback": "..."},
  "overall_pass": true/false,
  "overall_score": 0-100,
  "regeneration_suggestions": "Specific prompt changes if score < 70"
}
"""


class ImageAuditor:
    """Audit generated images against quality rubric."""

    def __init__(self, vision_provider: str = "auto"):
        """
        Initialize auditor with vision provider.

        Args:
            vision_provider: "claude", "openai", or "auto" (tries claude first)
        """
        self.provider = vision_provider
        self._claude_client = None
        self._openai_client = None

        if vision_provider == "auto":
            if CLAUDE_AVAILABLE and os.environ.get("ANTHROPIC_API_KEY"):
                self.provider = "claude"
            elif OPENAI_AVAILABLE and os.environ.get("OPENAI_API_KEY"):
                self.provider = "openai"
            else:
                raise ValueError("No vision provider available. Set ANTHROPIC_API_KEY or OPENAI_API_KEY")

    def _get_claude_client(self):
        if self._claude_client is None:
            self._claude_client = anthropic.Anthropic()
        return self._claude_client

    def _get_openai_client(self):
        if self._openai_client is None:
            self._openai_client = OpenAI()
        return self._openai_client

    def _encode_image(self, image_path: Path) -> Tuple[str, str]:
        """Encode image to base64 and determine media type."""
        suffix = image_path.suffix.lower()
        media_type = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp"
        }.get(suffix, "image/png")

        with open(image_path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")

        return data, media_type

    def _build_audit_prompt(self, original_prompt: str, intended_concept: str) -> str:
        """Build the audit prompt with context."""
        return f"""You are an expert image quality auditor using the visual-art-composition framework.

## Original Generation Prompt:
{original_prompt}

## Intended Concept/Message:
{intended_concept}

{AUDIT_RUBRIC}

Analyze the image and provide your evaluation in the JSON format specified above.
Be strict about text artifacts - ANY visible text is an automatic fail.
Be constructive with regeneration suggestions if the score is below 70."""

    def audit(
        self,
        image_path: Path,
        original_prompt: str,
        intended_concept: str,
        pass_threshold: float = 0.7
    ) -> AuditResult:
        """
        Audit an image against the quality rubric.

        Args:
            image_path: Path to the generated image
            original_prompt: The prompt used to generate the image
            intended_concept: What the image should communicate
            pass_threshold: Minimum score (0-1) to pass (default 0.7 = 70%)

        Returns:
            AuditResult with pass/fail, score, findings, and feedback
        """
        image_path = Path(image_path)
        if not image_path.exists():
            return AuditResult(
                passed=False,
                score=0.0,
                findings=[AuditFinding(
                    category="file",
                    severity=AuditSeverity.CRITICAL,
                    message=f"Image file not found: {image_path}"
                )]
            )

        # Encode image
        image_data, media_type = self._encode_image(image_path)

        # Build prompt
        audit_prompt = self._build_audit_prompt(original_prompt, intended_concept)

        # Call vision model
        if self.provider == "claude":
            response = self._audit_with_claude(image_data, media_type, audit_prompt)
        else:
            response = self._audit_with_openai(image_data, media_type, audit_prompt)

        # Parse response
        return self._parse_audit_response(response, pass_threshold, original_prompt)

    def _audit_with_claude(self, image_data: str, media_type: str, prompt: str) -> str:
        """Run audit using Claude vision."""
        client = self._get_claude_client()

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        return message.content[0].text

    def _audit_with_openai(self, image_data: str, media_type: str, prompt: str) -> str:
        """Run audit using GPT-4 Vision."""
        client = self._get_openai_client()

        response = client.chat.completions.create(
            model="gpt-4o",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{image_data}"
                            }
                        }
                    ]
                }
            ]
        )

        return response.choices[0].message.content

    def _parse_audit_response(
        self,
        response: str,
        pass_threshold: float,
        original_prompt: str
    ) -> AuditResult:
        """Parse the vision model's audit response."""
        findings = []

        # Try to extract JSON from response
        try:
            # Find JSON block in response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback: try to parse as unstructured
            return AuditResult(
                passed=False,
                score=0.5,
                findings=[AuditFinding(
                    category="parse_error",
                    severity=AuditSeverity.WARNING,
                    message=f"Could not parse audit response: {e}",
                    suggestion="Re-run audit"
                )],
                prompt_feedback=response[:500]
            )

        # Check text artifacts (critical)
        text_data = data.get("text_artifacts", {})
        if text_data.get("found", False) or text_data.get("score", 10) < 5:
            findings.append(AuditFinding(
                category="text_artifacts",
                severity=AuditSeverity.CRITICAL,
                message=text_data.get("details", "Text artifacts detected"),
                suggestion="Add 'NO TEXT, NO WORDS, NO LETTERS' to prompt"
            ))

        # Process other categories
        categories = [
            ("concept_alignment", 0.30),
            ("professional_quality", 0.25),
            ("color_palette", 0.15),
            ("aesthetic_coherence", 0.15),
            ("technical_quality", 0.15)
        ]

        weighted_score = 0.0
        for category, weight in categories:
            cat_data = data.get(category, {})
            score = cat_data.get("score", 5) / 10.0
            weighted_score += score * weight

            if score < 0.6:
                severity = AuditSeverity.FAIL if score < 0.4 else AuditSeverity.WARNING
                findings.append(AuditFinding(
                    category=category,
                    severity=severity,
                    message=cat_data.get("feedback", f"Low score in {category}"),
                    suggestion=None
                ))

        # Text artifacts override (auto-fail)
        if text_data.get("found", False):
            weighted_score = min(weighted_score, 0.3)

        overall_score = data.get("overall_score", weighted_score * 100) / 100.0
        passed = overall_score >= pass_threshold and not text_data.get("found", False)

        # Build regeneration prompt if failed
        regenerate_prompt = None
        if not passed:
            suggestions = data.get("regeneration_suggestions", "")
            if suggestions:
                # Enhance original prompt with suggestions
                regenerate_prompt = f"{original_prompt}\n\nIMPROVEMENTS: {suggestions}\n\nCRITICAL: NO TEXT, NO WORDS, NO LETTERS, NO SYMBOLS."

        return AuditResult(
            passed=passed,
            score=overall_score,
            findings=findings,
            prompt_feedback=data.get("regeneration_suggestions"),
            regenerate_prompt=regenerate_prompt
        )


def audit_and_regenerate_loop(
    generator,
    auditor: ImageAuditor,
    prompt: str,
    intended_concept: str,
    output_path: Path,
    config=None,
    max_iterations: int = 3,
    pass_threshold: float = 0.7
) -> Tuple[Path, AuditResult]:
    """
    Generate and audit images in a loop until quality threshold met.

    This is the "Ralph Wiggum Loop" integration - persistent iteration
    until the image passes audit.

    Args:
        generator: Image generator instance (from base.py)
        auditor: ImageAuditor instance
        prompt: Initial generation prompt
        intended_concept: What the image should communicate
        output_path: Where to save the final image
        config: ImageConfig for generation
        max_iterations: Maximum attempts before giving up
        pass_threshold: Minimum score to pass (0-1)

    Returns:
        Tuple of (final_image_path, final_audit_result)
    """
    current_prompt = prompt
    output_path = Path(output_path)

    for iteration in range(max_iterations):
        # Generate image
        iteration_path = output_path.with_stem(f"{output_path.stem}_iter{iteration+1}")
        print(f"\n[Iteration {iteration+1}/{max_iterations}] Generating image...")

        try:
            result = generator.generate(current_prompt, iteration_path, config)
            print(f"  Generated: {result.path} ({result.generation_time_seconds:.2f}s)")
        except Exception as e:
            print(f"  Generation failed: {e}")
            continue

        # Audit image
        print(f"  Auditing image...")
        audit_result = auditor.audit(
            iteration_path,
            current_prompt,
            intended_concept,
            pass_threshold
        )

        print(f"  Score: {audit_result.score:.1%} | Passed: {audit_result.passed}")

        if audit_result.passed:
            # Success! Rename to final path
            if iteration_path != output_path:
                iteration_path.rename(output_path)
            print(f"  SUCCESS: Image passed audit!")
            return output_path, audit_result

        # Print findings
        for finding in audit_result.findings:
            print(f"  [{finding.severity.value.upper()}] {finding.category}: {finding.message}")

        # Update prompt for next iteration
        if audit_result.regenerate_prompt:
            current_prompt = audit_result.regenerate_prompt
            print(f"  Updating prompt with feedback for next iteration...")

        # Cleanup failed iteration
        if iteration_path.exists() and iteration_path != output_path:
            iteration_path.unlink()

    # Max iterations reached without passing
    print(f"\n  FAILED: Max iterations ({max_iterations}) reached without passing audit.")
    return output_path, audit_result


# CLI integration
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Audit generated images against quality rubric")
    parser.add_argument("image", help="Path to image to audit")
    parser.add_argument("--prompt", "-p", required=True, help="Original generation prompt")
    parser.add_argument("--concept", "-c", required=True, help="Intended concept/message")
    parser.add_argument("--threshold", "-t", type=float, default=0.7, help="Pass threshold (0-1)")
    parser.add_argument("--provider", choices=["auto", "claude", "openai"], default="auto")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    auditor = ImageAuditor(vision_provider=args.provider)
    result = auditor.audit(
        Path(args.image),
        args.prompt,
        args.concept,
        args.threshold
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"AUDIT RESULT: {'PASSED' if result.passed else 'FAILED'}")
        print(f"Score: {result.score:.1%}")
        print(f"{'='*60}")

        if result.findings:
            print("\nFindings:")
            for f in result.findings:
                print(f"  [{f.severity.value.upper()}] {f.category}: {f.message}")
                if f.suggestion:
                    print(f"    Suggestion: {f.suggestion}")

        if result.prompt_feedback:
            print(f"\nFeedback: {result.prompt_feedback}")

        if result.regenerate_prompt:
            print(f"\nSuggested regeneration prompt:\n{result.regenerate_prompt[:500]}...")
