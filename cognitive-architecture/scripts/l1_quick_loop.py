#!/usr/bin/env python3
"""
L1 Quick Loop - Uses existing baseline results to drive improvement.

This is a simpler version that:
1. Loads baseline results from JSON
2. Analyzes failures
3. Proposes and applies improvements
4. Runs targeted re-eval on failures only (faster)
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
COGNITIVE_DIR = SCRIPT_DIR.parent
STORAGE_DIR = COGNITIVE_DIR / "storage" / "eval_results"
SKILLS_DIR = COGNITIVE_DIR.parent / "skills" / "foundry"
PA_SKILL_PATH = SKILLS_DIR / "prompt-architect" / "SKILL.md"
L1_STORAGE = COGNITIVE_DIR / "storage" / "l1_loop"

# Ensure storage exists
L1_STORAGE.mkdir(parents=True, exist_ok=True)

def load_baseline():
    """Load the most recent baseline eval results."""
    results = sorted(STORAGE_DIR.glob("prompt-architect-cli-eval-*.json"))
    if not results:
        print("[ERROR] No baseline results found!")
        sys.exit(1)

    latest = results[-1]
    print(f"Loading baseline: {latest.name}")

    with open(latest) as f:
        return json.load(f)

def analyze_failures(baseline):
    """Analyze failure patterns."""
    failures = []

    for task in baseline.get("task_results", []):
        if not task.get("passed", True):
            failures.append({
                "id": task["task_id"],
                "category": task.get("category", "unknown"),
                "difficulty": task.get("difficulty", "unknown"),
                "reasoning": task.get("reasoning", "")[:500],
            })

    # Group by category
    by_category = {}
    for f in failures:
        cat = f["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(f)

    return failures, by_category

def print_failure_analysis(failures, by_category):
    """Print failure analysis."""
    print(f"\n{'='*70}")
    print(f"FAILURE ANALYSIS ({len(failures)} failures)")
    print("=" * 70)

    print("\nBy Category:")
    for cat, items in by_category.items():
        print(f"  {cat}: {len(items)} failures")
        for item in items:
            print(f"    - {item['id']} ({item['difficulty']})")

    print("\nCommon Issues:")
    # Extract common patterns from reasoning
    patterns = {
        "timeout": 0,
        "domain_specific": 0,
        "epistemic_calibration": 0,
        "incomplete_output": 0,
        "wrong_language": 0,
    }

    for f in failures:
        reasoning = f["reasoning"].lower()
        if "timeout" in reasoning or "crash" in reasoning:
            patterns["timeout"] += 1
        if "django" in reasoning or "go-specific" in reasoning or "wcag" in reasoning:
            patterns["domain_specific"] += 1
        if "confidence" in reasoning or "ceiling" in reasoning:
            patterns["epistemic_calibration"] += 1
        if "truncated" in reasoning:
            patterns["incomplete_output"] += 1
        if "typescript" in reasoning and "python" in reasoning:
            patterns["wrong_language"] += 1

    for pattern, count in patterns.items():
        if count > 0:
            print(f"  {pattern}: {count}")

    return patterns

def generate_improvement_prompt(failures, patterns, skill_content):
    """Generate a prompt for PA to improve itself."""
    failure_summary = json.dumps([{
        "id": f["id"],
        "category": f["category"],
        "issue": f["reasoning"][:200]
    } for f in failures[:8]], indent=2)

    prompt = f"""You are the Prompt Architect skill analyzing your own failures.

CURRENT SKILL.md (first 2500 chars):
```
{skill_content[:2500]}
```

FAILURE ANALYSIS:
- Total failures: {len(failures)}
- Pattern summary: {json.dumps(patterns)}

TOP FAILURES:
{failure_summary}

Based on these failures, propose ONE specific improvement to add to SKILL.md.

The improvement should:
1. Address the root cause of at least 2+ failures
2. Be a new rule, constraint, or pattern
3. Be concise and actionable
4. Use VERIX format for internal documentation

Output ONLY the improvement text (no explanation):

Example format:
### Domain-Specific Context Rule
[assert|emphatic] When success criteria mention a specific technology (Go, Django, WCAG, TypeScript), the output MUST explicitly address that technology's idioms and patterns. [ground:witnessed:eval-failures-PA-020-023-024-025] [conf:0.90]

- If criteria mentions "Go", include Go-specific patterns (error wrapping with %w, errors.Is/As)
- If criteria mentions "Django", include Django-specific solutions (cache framework, decorators)
- If criteria mentions "WCAG", provide actual compliance checklist with specific criteria
- If criteria mentions "TypeScript", address type-safe migration patterns
"""
    return prompt

def save_improvement(iteration, improvement, pass_rate_before, pass_rate_after):
    """Save improvement record."""
    record = {
        "iteration": iteration,
        "timestamp": datetime.now().isoformat(),
        "improvement": improvement,
        "pass_rate_before": pass_rate_before,
        "pass_rate_after": pass_rate_after,
        "delta": pass_rate_after - pass_rate_before,
    }

    history_file = L1_STORAGE / "improvement_history.jsonl"
    with open(history_file, "a") as f:
        f.write(json.dumps(record) + "\n")

    print(f"Saved to: {history_file}")

def main():
    print("=" * 70)
    print("L1 QUICK LOOP - Prompt Architect Self-Improvement")
    print("=" * 70)

    # 1. Load baseline
    baseline = load_baseline()
    pass_rate = baseline["overall_score"]
    print(f"\nBaseline pass rate: {pass_rate:.1%}")

    # 2. Analyze failures
    failures, by_category = analyze_failures(baseline)
    patterns = print_failure_analysis(failures, by_category)

    # 3. Read current skill
    skill_content = PA_SKILL_PATH.read_text(encoding="utf-8")
    print(f"\nCurrent SKILL.md size: {len(skill_content)} chars")

    # 4. Generate improvement prompt
    prompt = generate_improvement_prompt(failures, patterns, skill_content)

    # 5. Save prompt for manual execution
    prompt_file = L1_STORAGE / "l1_improvement_prompt.md"
    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)

    print(f"\n{'='*70}")
    print("IMPROVEMENT PROMPT SAVED")
    print("=" * 70)
    print(f"File: {prompt_file}")
    print(f"\nTo generate improvement, run:")
    print(f'  claude --print < "{prompt_file}"')
    print(f"\nThen apply the improvement to:")
    print(f"  {PA_SKILL_PATH}")

    # Also output the prompt to stdout for easy copying
    print(f"\n{'='*70}")
    print("PROMPT CONTENT:")
    print("=" * 70)
    print(prompt)

if __name__ == "__main__":
    main()
