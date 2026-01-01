#!/usr/bin/env python3
"""
Real Task Evaluator for VVV Dogfooding

This module actually executes the 50-task corpus against skills
using LLM evaluation (Claude-as-Judge pattern).

This is the REAL evaluator - not just static analysis.

Usage:
    from evals.real_evaluator import RealTaskEvaluator
    evaluator = RealTaskEvaluator("prompt-architect")
    results = evaluator.run_evaluation()
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)

# Try to import anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


@dataclass
class TaskResult:
    """Result of evaluating a single task."""
    task_id: str
    difficulty: str
    category: str
    input_text: str
    skill_output: str
    success_criteria: str

    # Evaluation scores (0-1)
    intent_accuracy: float = 0.0
    constraint_coverage: float = 0.0
    output_quality: float = 0.0
    verix_compliance: float = 0.0
    l2_purity: float = 0.0

    # Overall
    passed: bool = False
    judge_reasoning: str = ""
    execution_time_ms: int = 0


@dataclass
class EvaluationResult:
    """Aggregate evaluation results."""
    skill_name: str
    version: str
    timestamp: str
    total_tasks: int
    passed_tasks: int

    # Per-category scores
    easy_score: float = 0.0
    medium_score: float = 0.0
    hard_score: float = 0.0

    # Per-dimension scores
    intent_accuracy: float = 0.0
    constraint_coverage: float = 0.0
    output_quality: float = 0.0
    verix_compliance: float = 0.0
    l2_purity: float = 0.0

    # Overall
    overall_score: float = 0.0
    task_results: List[TaskResult] = field(default_factory=list)


class RealTaskEvaluator:
    """
    Evaluator that actually runs tasks through skills and scores outputs.

    Uses Claude-as-Judge pattern for evaluation:
    1. Load task from corpus
    2. Execute skill with task input
    3. Have Claude evaluate output against success criteria
    4. Aggregate scores
    """

    CORPUS_DIR = Path(__file__).parent / "corpus"
    RESULTS_DIR = Path(__file__).parent.parent / "storage" / "eval_results"
    SKILLS_DIR = Path(__file__).parent.parent.parent / "skills" / "foundry"

    def __init__(self, skill_name: str, model: str = "claude-sonnet-4-20250514"):
        """
        Initialize evaluator.

        Args:
            skill_name: One of "prompt-architect", "agent-creator", "skill-forge"
            model: Claude model to use for evaluation (default: claude-sonnet-4-20250514)
        """
        self.skill_name = skill_name
        self.model = model
        self.corpus = self._load_corpus()
        self.skill_content = self._load_skill()

        if ANTHROPIC_AVAILABLE:
            # Get API key from environment
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if api_key and not api_key.startswith("${"):
                self.client = anthropic.Anthropic(api_key=api_key)
            else:
                self.client = None
                print("[WARNING] ANTHROPIC_API_KEY not set - using mock evaluation")
        else:
            self.client = None
            print("[WARNING] Anthropic SDK not available - using mock evaluation")

        self.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    def _load_corpus(self) -> Dict:
        """Load the task corpus for this skill."""
        corpus_file = self.CORPUS_DIR / f"{self.skill_name}-corpus.json"
        if not corpus_file.exists():
            raise FileNotFoundError(f"Corpus not found: {corpus_file}")

        with open(corpus_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_skill(self) -> str:
        """Load the skill definition."""
        skill_file = self.SKILLS_DIR / self.skill_name / "SKILL.md"
        if not skill_file.exists():
            raise FileNotFoundError(f"Skill not found: {skill_file}")

        return skill_file.read_text(encoding="utf-8")

    def _execute_skill(self, task_input: str) -> str:
        """
        Execute the skill with given input.

        Uses Claude to simulate skill execution by providing
        the skill definition and asking it to process the input.
        """
        if not self.client:
            return f"[MOCK] Processed: {task_input[:50]}..."

        prompt = f"""You are executing the {self.skill_name} skill.

Here is the skill definition:
<skill>
{self.skill_content[:8000]}  # Truncate if too long
</skill>

Now execute this skill with the following input:
<input>
{task_input}
</input>

Provide the skill's output following its defined behavior and format."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"[ERROR] Skill execution failed: {e}"

    def _judge_output(self, task: Dict, skill_output: str) -> Dict[str, Any]:
        """
        Use Claude to judge the skill output against success criteria.

        Returns scores for each dimension and overall pass/fail.
        """
        if not self.client:
            # Mock scoring for testing
            return {
                "intent_accuracy": 0.8,
                "constraint_coverage": 0.75,
                "output_quality": 0.85,
                "verix_compliance": 0.9,
                "l2_purity": 1.0,
                "passed": True,
                "reasoning": "[MOCK] Evaluation passed"
            }

        judge_prompt = f"""You are evaluating a skill's output. Score each dimension from 0.0 to 1.0.

TASK:
- ID: {task['id']}
- Category: {task['category']}
- Input: {task['input']}
- Success Criteria: {task['success_criteria']}

SKILL OUTPUT:
{skill_output}

EXPECTED (if available):
- Intent: {task.get('expected_intent', 'N/A')}
- Constraints: {task.get('expected_constraints', [])}

Score these dimensions (0.0 to 1.0):
1. intent_accuracy: Did the skill correctly identify/handle the intent?
2. constraint_coverage: Were all relevant constraints addressed?
3. output_quality: Is the output well-structured and useful?
4. verix_compliance: Does output follow VERIX epistemic standards (claims grounded)?
5. l2_purity: Is output in pure English without VCL markers?

Respond in JSON format:
{{
  "intent_accuracy": 0.0-1.0,
  "constraint_coverage": 0.0-1.0,
  "output_quality": 0.0-1.0,
  "verix_compliance": 0.0-1.0,
  "l2_purity": 0.0-1.0,
  "passed": true/false,
  "reasoning": "Brief explanation"
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": judge_prompt}]
            )

            # Parse JSON from response
            text = response.content[0].text
            # Find JSON in response
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])

            return {
                "intent_accuracy": 0.5,
                "constraint_coverage": 0.5,
                "output_quality": 0.5,
                "verix_compliance": 0.5,
                "l2_purity": 0.5,
                "passed": False,
                "reasoning": "Failed to parse judge response"
            }

        except Exception as e:
            return {
                "intent_accuracy": 0.0,
                "constraint_coverage": 0.0,
                "output_quality": 0.0,
                "verix_compliance": 0.0,
                "l2_purity": 0.0,
                "passed": False,
                "reasoning": f"Judge error: {e}"
            }

    def evaluate_task(self, task: Dict) -> TaskResult:
        """Evaluate a single task."""
        start_time = time.time()

        # Execute skill
        skill_output = self._execute_skill(task['input'])

        # Judge output
        scores = self._judge_output(task, skill_output)

        execution_time = int((time.time() - start_time) * 1000)

        return TaskResult(
            task_id=task['id'],
            difficulty=task['difficulty'],
            category=task['category'],
            input_text=task['input'],
            skill_output=skill_output[:500],  # Truncate for storage
            success_criteria=task['success_criteria'],
            intent_accuracy=scores.get('intent_accuracy', 0),
            constraint_coverage=scores.get('constraint_coverage', 0),
            output_quality=scores.get('output_quality', 0),
            verix_compliance=scores.get('verix_compliance', 0),
            l2_purity=scores.get('l2_purity', 0),
            passed=scores.get('passed', False),
            judge_reasoning=scores.get('reasoning', ''),
            execution_time_ms=execution_time,
        )

    def run_evaluation(
        self,
        task_ids: Optional[List[str]] = None,
        difficulty_filter: Optional[str] = None,
        max_tasks: Optional[int] = None,
    ) -> EvaluationResult:
        """
        Run evaluation on corpus.

        Args:
            task_ids: Specific task IDs to run (None = all)
            difficulty_filter: "easy", "medium", "hard" (None = all)
            max_tasks: Maximum number of tasks to run (None = all)

        Returns:
            EvaluationResult with aggregate scores
        """
        tasks = self.corpus['tasks']

        # Filter by difficulty
        if difficulty_filter:
            tasks = [t for t in tasks if t['difficulty'] == difficulty_filter]

        # Filter by task IDs
        if task_ids:
            tasks = [t for t in tasks if t['id'] in task_ids]

        # Limit tasks
        if max_tasks:
            tasks = tasks[:max_tasks]

        print(f"\n{'='*60}")
        print(f"REAL EVALUATION: {self.skill_name}")
        print(f"Tasks to evaluate: {len(tasks)}")
        print(f"{'='*60}\n")

        results: List[TaskResult] = []

        for i, task in enumerate(tasks, 1):
            print(f"[{i}/{len(tasks)}] Evaluating {task['id']}...", end=" ")
            result = self.evaluate_task(task)
            results.append(result)
            status = "PASS" if result.passed else "FAIL"
            print(f"{status} ({result.execution_time_ms}ms)")

        # Aggregate scores
        passed_count = sum(1 for r in results if r.passed)

        easy_results = [r for r in results if r.difficulty == 'easy']
        medium_results = [r for r in results if r.difficulty == 'medium']
        hard_results = [r for r in results if r.difficulty == 'hard']

        def avg_score(results_list: List[TaskResult], attr: str) -> float:
            if not results_list:
                return 0.0
            return sum(getattr(r, attr) for r in results_list) / len(results_list)

        eval_result = EvaluationResult(
            skill_name=self.skill_name,
            version=self.corpus.get('version', 'unknown'),
            timestamp=datetime.now(timezone.utc).isoformat(),
            total_tasks=len(results),
            passed_tasks=passed_count,

            easy_score=avg_score(easy_results, 'output_quality') if easy_results else 0,
            medium_score=avg_score(medium_results, 'output_quality') if medium_results else 0,
            hard_score=avg_score(hard_results, 'output_quality') if hard_results else 0,

            intent_accuracy=avg_score(results, 'intent_accuracy'),
            constraint_coverage=avg_score(results, 'constraint_coverage'),
            output_quality=avg_score(results, 'output_quality'),
            verix_compliance=avg_score(results, 'verix_compliance'),
            l2_purity=avg_score(results, 'l2_purity'),

            overall_score=passed_count / len(results) if results else 0,
            task_results=results,
        )

        # Save results
        self._save_results(eval_result)

        return eval_result

    def _save_results(self, result: EvaluationResult):
        """Save evaluation results to file."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{self.skill_name}-eval-{timestamp}.json"
        filepath = self.RESULTS_DIR / filename

        # Convert to dict for JSON serialization
        result_dict = {
            "skill_name": result.skill_name,
            "version": result.version,
            "timestamp": result.timestamp,
            "total_tasks": result.total_tasks,
            "passed_tasks": result.passed_tasks,
            "easy_score": result.easy_score,
            "medium_score": result.medium_score,
            "hard_score": result.hard_score,
            "intent_accuracy": result.intent_accuracy,
            "constraint_coverage": result.constraint_coverage,
            "output_quality": result.output_quality,
            "verix_compliance": result.verix_compliance,
            "l2_purity": result.l2_purity,
            "overall_score": result.overall_score,
            "task_results": [
                {
                    "task_id": r.task_id,
                    "difficulty": r.difficulty,
                    "category": r.category,
                    "passed": r.passed,
                    "intent_accuracy": r.intent_accuracy,
                    "output_quality": r.output_quality,
                    "execution_time_ms": r.execution_time_ms,
                    "reasoning": r.judge_reasoning,
                }
                for r in result.task_results
            ]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2)

        print(f"\nResults saved: {filepath}")

    def print_summary(self, result: EvaluationResult):
        """Print evaluation summary."""
        print(f"\n{'='*60}")
        print(f"EVALUATION SUMMARY: {result.skill_name}")
        print(f"{'='*60}")
        print(f"Total Tasks: {result.total_tasks}")
        print(f"Passed: {result.passed_tasks} ({result.overall_score:.1%})")
        print(f"\nBy Difficulty:")
        print(f"  Easy: {result.easy_score:.1%}")
        print(f"  Medium: {result.medium_score:.1%}")
        print(f"  Hard: {result.hard_score:.1%}")
        print(f"\nBy Dimension:")
        print(f"  Intent Accuracy: {result.intent_accuracy:.1%}")
        print(f"  Constraint Coverage: {result.constraint_coverage:.1%}")
        print(f"  Output Quality: {result.output_quality:.1%}")
        print(f"  VERIX Compliance: {result.verix_compliance:.1%}")
        print(f"  L2 Purity: {result.l2_purity:.1%}")
        print(f"\nOverall Score: {result.overall_score:.1%}")


def main():
    """Run evaluation from command line."""
    import argparse

    parser = argparse.ArgumentParser(description="Run real task evaluation")
    parser.add_argument("skill", choices=["prompt-architect", "agent-creator", "skill-forge"])
    parser.add_argument("--max-tasks", type=int, default=None, help="Max tasks to run")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default=None)

    args = parser.parse_args()

    evaluator = RealTaskEvaluator(args.skill)
    result = evaluator.run_evaluation(
        difficulty_filter=args.difficulty,
        max_tasks=args.max_tasks,
    )
    evaluator.print_summary(result)


if __name__ == "__main__":
    main()
