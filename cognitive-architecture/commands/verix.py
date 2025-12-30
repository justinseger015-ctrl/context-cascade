"""
/verix command - Apply VERIX epistemic notation.

Usage:
    /verix                     - Show VERIX guide
    /verix parse "<text>"      - Parse text for VERIX elements
    /verix validate "<claim>"  - Validate epistemic consistency
    /verix annotate "<text>"   - Add VERIX annotations
    /verix level <0|1|2>       - Set compression level
"""

import os
import sys
import re
from typing import Optional, Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verix import (
    VerixClaim,
    VerixParser,
    Illocution,
    Affect,
    State,
)
from core.config import CompressionLevel


def format_verix_guide() -> str:
    """Format VERIX notation guide."""
    return """
VERIX - Epistemic Notation System
==================================

Structure:
  STATEMENT := ILLOCUTION + AFFECT + CONTENT + GROUND + CONFIDENCE + STATE

Components:

1. ILLOCUTION (What type of claim?)
   [assert|...]  - Factual claim
   [query|...]   - Question
   [propose|...] - Suggestion
   [commit|...]  - Promise

2. AFFECT (Emotional register)
   @high    - Strong conviction
   @neutral - Objective stance
   @low     - Hedged/tentative

3. CONTENT
   The actual claim or statement

4. GROUND (Evidence basis)
   [ground: direct observation]
   [ground: expert testimony]
   [ground: inference from X]

5. CONFIDENCE (Certainty level)
   [conf:95]  - High confidence (90-100%)
   [conf:75]  - Medium confidence (50-89%)
   [conf:30]  - Low confidence (0-49%)

6. STATE (Epistemic status)
   [state: VERIFIED]    - Confirmed true
   [state: TENTATIVE]   - Provisional
   [state: SPECULATIVE] - Unverified

Compression Levels:
  L0: AI-AI   (Emoji shorthand)
  L1: AI+Human (Annotated format)
  L2: Human   (Natural language, lossy)

Examples:
  L0: [A|@n|Python is dynamically typed|o|95|V]
  L1: [assert|@neutral|Python is dynamically typed|ground:documentation|conf:95|VERIFIED]
  L2: Python is dynamically typed (well-established fact).
"""


def parse_text_for_verix(text: str) -> Dict[str, Any]:
    """Parse text to extract VERIX-relevant elements."""
    result = {
        "claims": [],
        "hedges": [],
        "grounds": [],
        "confidence_markers": [],
    }

    # Find claims (sentences with assertions)
    sentences = re.split(r'[.!?]+', text)
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        # Detect hedges
        hedge_patterns = [
            r'\bprobably\b', r'\bmight\b', r'\bcould\b', r'\bperhaps\b',
            r'\bseems?\b', r'\bappears?\b', r'\blikely\b', r'\bpossibly\b',
        ]
        hedges = []
        for pattern in hedge_patterns:
            if re.search(pattern, sent, re.IGNORECASE):
                hedges.append(pattern.replace(r'\b', ''))

        # Detect confidence markers
        conf_patterns = [
            (r'\bcertainly\b', 95),
            (r'\bdefinitely\b', 95),
            (r'\bprobably\b', 70),
            (r'\blikely\b', 70),
            (r'\bpossibly\b', 40),
            (r'\bmaybe\b', 40),
            (r'\buncertain\b', 30),
        ]
        for pattern, conf in conf_patterns:
            if re.search(pattern, sent, re.IGNORECASE):
                result["confidence_markers"].append({
                    "marker": pattern.replace(r'\b', ''),
                    "implied_confidence": conf,
                })

        # Detect grounds
        ground_patterns = [
            r'according to (\w+)',
            r'based on (\w+)',
            r'research shows',
            r'studies indicate',
            r'evidence suggests',
        ]
        for pattern in ground_patterns:
            match = re.search(pattern, sent, re.IGNORECASE)
            if match:
                result["grounds"].append({
                    "pattern": pattern,
                    "match": match.group(0),
                })

        result["claims"].append({
            "text": sent,
            "hedges": hedges,
            "is_grounded": len(result["grounds"]) > 0,
        })

    result["hedges"] = list(set(h for c in result["claims"] for h in c["hedges"]))
    return result


def validate_claim(claim: str) -> Dict[str, Any]:
    """Validate a claim for epistemic consistency."""
    validation = {
        "claim": claim,
        "issues": [],
        "suggestions": [],
        "score": 1.0,
    }

    # Check for ungrounded high confidence
    high_conf_patterns = [r'\bcertainly\b', r'\bdefinitely\b', r'\balways\b', r'\bnever\b']
    ground_patterns = [r'because\b', r'since\b', r'based on\b', r'according to\b']

    has_high_conf = any(re.search(p, claim, re.IGNORECASE) for p in high_conf_patterns)
    has_ground = any(re.search(p, claim, re.IGNORECASE) for p in ground_patterns)

    if has_high_conf and not has_ground:
        validation["issues"].append("High confidence without grounding")
        validation["suggestions"].append("Add evidence or source for claim")
        validation["score"] -= 0.3

    # Check for vague hedging
    vague_patterns = [r'\bkind of\b', r'\bsort of\b', r'\bsomewhat\b']
    if any(re.search(p, claim, re.IGNORECASE) for p in vague_patterns):
        validation["issues"].append("Vague hedging (non-quantified uncertainty)")
        validation["suggestions"].append("Use specific confidence markers (likely, probably)")
        validation["score"] -= 0.2

    # Check for absolute claims
    absolute_patterns = [r'\ball\b', r'\bnone\b', r'\bonly\b', r'\bimpossible\b']
    if any(re.search(p, claim, re.IGNORECASE) for p in absolute_patterns):
        validation["issues"].append("Absolute claim (may need qualification)")
        validation["suggestions"].append("Consider edge cases or exceptions")
        validation["score"] -= 0.1

    validation["score"] = max(0.0, validation["score"])
    return validation


def annotate_text(text: str, level: int = 1) -> str:
    """Add VERIX annotations to text."""
    sentences = re.split(r'([.!?]+)', text)
    annotated = []

    for i in range(0, len(sentences) - 1, 2):
        sent = sentences[i].strip()
        punct = sentences[i + 1] if i + 1 < len(sentences) else "."

        if not sent:
            continue

        # Determine illocution
        if "?" in punct:
            illocution = "query"
        elif any(w in sent.lower() for w in ["should", "could", "recommend"]):
            illocution = "propose"
        else:
            illocution = "assert"

        # Determine affect
        if any(w in sent.lower() for w in ["certainly", "definitely", "must"]):
            affect = "@high"
        elif any(w in sent.lower() for w in ["perhaps", "maybe", "might"]):
            affect = "@low"
        else:
            affect = "@neutral"

        # Determine confidence
        if any(w in sent.lower() for w in ["certainly", "definitely"]):
            conf = 95
        elif any(w in sent.lower() for w in ["probably", "likely"]):
            conf = 75
        elif any(w in sent.lower() for w in ["possibly", "maybe"]):
            conf = 40
        else:
            conf = 70

        # Format based on level
        if level == 0:
            # L0: Emoji shorthand
            i_short = illocution[0].upper()
            a_short = affect[1]
            annotated.append(f"[{i_short}|{a_short}|{sent}|{conf}]")
        elif level == 1:
            # L1: Full annotation
            annotated.append(f"[{illocution}|{affect}|{sent}|conf:{conf}]")
        else:
            # L2: Natural language
            conf_word = "certainly" if conf > 90 else "likely" if conf > 60 else "possibly"
            annotated.append(f"{sent} ({conf_word}){punct}")

    return " ".join(annotated)


def verix_command(
    action: Optional[str] = None,
    text: Optional[str] = None,
    level: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Execute /verix command.

    Args:
        action: Command action (parse, validate, annotate, level)
        text: Text to process
        level: Compression level (0, 1, 2)

    Returns:
        Command result with VERIX data
    """
    result = {
        "command": "/verix",
        "success": True,
        "output": "",
        "data": None,
    }

    # Default: show guide
    if action is None:
        result["output"] = format_verix_guide()
        return result

    # Parse: parse text for VERIX elements
    if action == "parse":
        if not text:
            result["success"] = False
            result["output"] = 'Error: Text required. Usage: /verix parse "<text>"'
            return result

        parsed = parse_text_for_verix(text)

        lines = ["VERIX Parse Results:", ""]
        lines.append(f"Claims found: {len(parsed['claims'])}")
        lines.append(f"Hedges detected: {', '.join(parsed['hedges']) or '(none)'}")
        lines.append(f"Grounding phrases: {len(parsed['grounds'])}")
        lines.append("")

        if parsed["confidence_markers"]:
            lines.append("Confidence markers:")
            for marker in parsed["confidence_markers"]:
                lines.append(f"  - {marker['marker']} (implies ~{marker['implied_confidence']}%)")

        result["output"] = "\n".join(lines)
        result["data"] = parsed
        return result

    # Validate: validate epistemic consistency
    if action == "validate":
        if not text:
            result["success"] = False
            result["output"] = 'Error: Claim required. Usage: /verix validate "<claim>"'
            return result

        validation = validate_claim(text)

        lines = [
            "VERIX Validation:",
            f"Claim: {text}",
            f"Epistemic Score: {validation['score']:.2f}",
            "",
        ]

        if validation["issues"]:
            lines.append("Issues:")
            for issue in validation["issues"]:
                lines.append(f"  ! {issue}")
            lines.append("")
            lines.append("Suggestions:")
            for sugg in validation["suggestions"]:
                lines.append(f"  + {sugg}")
        else:
            lines.append("No epistemic issues detected.")

        result["output"] = "\n".join(lines)
        result["data"] = validation
        return result

    # Annotate: add VERIX annotations
    if action == "annotate":
        if not text:
            result["success"] = False
            result["output"] = 'Error: Text required. Usage: /verix annotate "<text>"'
            return result

        compression = level if level is not None else 1
        annotated = annotate_text(text, compression)

        level_names = {0: "L0 (AI-AI)", 1: "L1 (AI+Human)", 2: "L2 (Human)"}

        lines = [
            f"VERIX Annotated ({level_names.get(compression, 'L1')}):",
            "",
            annotated,
        ]

        result["output"] = "\n".join(lines)
        result["data"] = {"annotated": annotated, "level": compression}
        return result

    # Level: set compression level
    if action == "level":
        if level is None:
            try:
                level = int(text) if text else None
            except ValueError:
                level = None

        if level not in [0, 1, 2]:
            result["success"] = False
            result["output"] = "Error: Level must be 0, 1, or 2. Usage: /verix level 1"
            return result

        level_desc = {
            0: "L0: AI-AI (Emoji shorthand, maximum compression)",
            1: "L1: AI+Human (Full annotation, balanced)",
            2: "L2: Human (Natural language, lossy compression)",
        }

        result["output"] = f"VERIX compression level set to:\n  {level_desc[level]}"
        result["data"] = {"level": level}
        return result

    # Unknown action
    result["success"] = False
    result["output"] = f"""
Unknown action: '{action}'

/verix - Apply VERIX epistemic notation

Usage:
  /verix                     - Show VERIX guide
  /verix parse "<text>"      - Parse for VERIX elements
  /verix validate "<claim>"  - Validate epistemic consistency
  /verix annotate "<text>"   - Add VERIX annotations
  /verix level <0|1|2>       - Set compression level
"""
    return result


if __name__ == "__main__":
    # Demo
    print("=== /verix parse ===")
    r = verix_command("parse", "Python is probably the best language for data science. Research shows it has the largest ML ecosystem.")
    print(r["output"])

    print("\n=== /verix validate ===")
    r = verix_command("validate", "This will definitely work without any issues.")
    print(r["output"])

    print("\n=== /verix annotate (L1) ===")
    r = verix_command("annotate", "Python is probably the best choice. It might have some limitations.", 1)
    print(r["output"])

    print("\n=== /verix annotate (L0) ===")
    r = verix_command("annotate", "Python is probably the best choice.", 0)
    print(r["output"])
