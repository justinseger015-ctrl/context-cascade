#!/usr/bin/env python3
"""
Multi-Model Evaluator - Alternates between Claude, Gemini, and Codex
Adapted from life-os-dashboard cli-bridge pattern
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# API Keys
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


@dataclass
class TaskResult:
    task_id: str
    difficulty: str
    category: str
    input_text: str
    skill_output: str
    success_criteria: str
    model_used: str = ""
    intent_accuracy: float = 0.0
    constraint_coverage: float = 0.0
    output_quality: float = 0.0
    verix_compliance: float = 0.0
    l2_purity: float = 0.0
    passed: bool = False
    judge_reasoning: str = ""
    execution_time_ms: int = 0


@dataclass
class EvaluationResult:
    skill_name: str
    version: str
    timestamp: str
    total_tasks: int
    passed_tasks: int
    models_used: List[str] = field(default_factory=list)
    task_results: List[TaskResult] = field(default_factory=list)

    @property
    def pass_rate(self):
        return self.passed_tasks / self.total_tasks if self.total_tasks > 0 else 0


class MultiModelClient:
    """Client that can use Claude CLI, Gemini API, or OpenAI/Codex API"""

    PROVIDERS = ["claude", "gemini", "codex"]

    def __init__(self):
        self._claude_available = None
        self._gemini_client = None
        self._openai_client = None
        self._current_index = 0

    def _check_claude_cli(self) -> bool:
        if self._claude_available is None:
            try:
                result = subprocess.run(
                    ["claude", "--version"],
                    capture_output=True, text=True, timeout=10, shell=True
                )
                self._claude_available = result.returncode == 0
            except:
                self._claude_available = False
        return self._claude_available

    def _get_gemini(self):
        if self._gemini_client is None and GOOGLE_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=GOOGLE_API_KEY)
                self._gemini_client = genai.GenerativeModel("gemini-1.5-flash")
            except ImportError:
                print("[WARN] google-generativeai not installed")
        return self._gemini_client

    def _get_openai(self):
        if self._openai_client is None and OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self._openai_client = OpenAI(api_key=OPENAI_API_KEY)
            except ImportError:
                print("[WARN] openai package not installed")
        return self._openai_client

    def get_available_providers(self) -> List[str]:
        available = []
        if self._check_claude_cli():
            available.append("claude")
        if self._get_gemini():
            available.append("gemini")
        if self._get_openai():
            available.append("codex")
        return available

    def get_next_provider(self) -> str:
        """Round-robin through available providers"""
        available = self.get_available_providers()
        if not available:
            raise ValueError("No AI providers available")
        provider = available[self._current_index % len(available)]
        self._current_index += 1
        return provider

    def send_message(self, prompt: str, provider: Optional[str] = None) -> Dict[str, Any]:
        """Send message to specified or next provider"""
        if provider is None:
            provider = self.get_next_provider()

        start_time = time.time()

        if provider == "claude":
            return self._send_claude(prompt, start_time)
        elif provider == "gemini":
            return self._send_gemini(prompt, start_time)
        elif provider == "codex":
            return self._send_codex(prompt, start_time)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _send_claude(self, prompt: str, start_time: float) -> Dict[str, Any]:
        cmd = ["claude", "--print", "--output-format", "text"]
        result = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True,
            timeout=300, shell=True
        )
        execution_time_ms = int((time.time() - start_time) * 1000)

        if result.returncode != 0:
            raise ValueError(f"Claude CLI error: {result.stderr}")

        return {
            "response": result.stdout.strip(),
            "model": "claude-cli",
            "provider": "claude",
            "execution_time_ms": execution_time_ms
        }

    def _send_gemini(self, prompt: str, start_time: float) -> Dict[str, Any]:
        model = self._get_gemini()
        if not model:
            raise ValueError("Gemini not available")

        response = model.generate_content(prompt)
        execution_time_ms = int((time.time() - start_time) * 1000)

        return {
            "response": response.text,
            "model": "gemini-1.5-flash",
            "provider": "gemini",
            "execution_time_ms": execution_time_ms
        }

    def _send_codex(self, prompt: str, start_time: float) -> Dict[str, Any]:
        client = self._get_openai()
        if not client:
            raise ValueError("OpenAI/Codex not available")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        execution_time_ms = int((time.time() - start_time) * 1000)

        return {
            "response": response.choices[0].message.content,
            "model": "gpt-4o-mini",
            "provider": "codex",
            "execution_time_ms": execution_time_ms
        }


class MultiModelEvaluator:
    """Evaluator that alternates between multiple AI providers"""

    CORPUS_DIR = Path(__file__).parent / "corpus"
    RESULTS_DIR = Path(__file__).parent.parent / "storage" / "eval_results"
    SKILLS_DIR = Path(__file__).parent.parent.parent / "skills" / "foundry"

    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.corpus = self._load_corpus()
        self.skill_content = self._load_skill()
        self.client = MultiModelClient()
        self.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

        available = self.client.get_available_providers()
        print(f"[MULTI] Available providers: {available}")
        if not available:
            raise ValueError("No AI providers available")

    def _load_corpus(self) -> Dict:
        corpus_file = self.CORPUS_DIR / f"{self.skill_name}-corpus.json"
        if not corpus_file.exists():
            raise FileNotFoundError(f"Corpus not found: {corpus_file}")
        with open(corpus_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_skill(self) -> str:
        skill_file = self.SKILLS_DIR / self.skill_name / "SKILL.md"
        if not skill_file.exists():
            raise FileNotFoundError(f"Skill not found: {skill_file}")
        return skill_file.read_text(encoding="utf-8")

    def _execute_skill(self, task_input: str) -> tuple:
        """Execute skill and return (output, provider_used)"""
        prompt = f"""You are executing the {self.skill_name} skill.

Here is the skill definition:
<skill>
{self.skill_content[:6000]}
</skill>

Now execute this skill with the following input:
<input>
{task_input}
</input>

Provide the skill's output following its defined behavior and format."""

        result = self.client.send_message(prompt)
        return result["response"], result["provider"]

    def _judge_output(self, task: Dict, skill_output: str) -> Dict[str, Any]:
        """Use next provider to judge output"""
        judge_prompt = f"""You are evaluating a skill's output. Score each dimension from 0.0 to 1.0.

TASK:
- ID: {task['id']}
- Category: {task['category']}
- Input: {task['input'][:500]}
- Success Criteria: {task['success_criteria']}

SKILL OUTPUT:
{skill_output[:1500]}

EXPECTED (if available):
- Intent: {task.get('expected_intent', 'N/A')}
- Constraints: {task.get('expected_constraints', [])}

Score these dimensions (0.0 to 1.0):
1. intent_accuracy: Did the skill correctly identify/handle the intent?
2. constraint_coverage: Were all relevant constraints addressed?
3. output_quality: Is the output well-structured and useful?
4. verix_compliance: Does output follow epistemic standards (confidence, evidence)?
5. l2_purity: Is output in pure English without internal markup?

Respond in JSON format ONLY:
{{
  "intent_accuracy": 0.0,
  "constraint_coverage": 0.0,
  "output_quality": 0.0,
  "verix_compliance": 0.0,
  "l2_purity": 0.0,
  "passed": true,
  "reasoning": "Brief explanation"
}}"""

        result = self.client.send_message(judge_prompt)
        text = result["response"]

        # Parse JSON from response
        start = text.find('{')
        end = text.rfind('}') + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except:
                pass

        return {
            "intent_accuracy": 0.0,
            "constraint_coverage": 0.0,
            "output_quality": 0.0,
            "verix_compliance": 0.0,
            "l2_purity": 0.0,
            "passed": False,
            "reasoning": "Failed to parse judge response"
        }

    def run_evaluation(self, max_tasks: int = 50) -> EvaluationResult:
        """Run evaluation alternating between providers"""
        tasks = self.corpus.get("tasks", [])[:max_tasks]
        results = []
        models_used = set()

        print(f"\n{'='*60}")
        print(f"MULTI-MODEL EVALUATION: {self.skill_name}")
        print(f"Tasks: {len(tasks)} | Providers: {self.client.get_available_providers()}")
        print(f"{'='*60}\n")

        for i, task in enumerate(tasks):
            task_id = task.get("id", f"T-{i+1}")
            start_time = time.time()

            try:
                # Execute skill
                skill_output, exec_provider = self._execute_skill(task["input"])
                models_used.add(exec_provider)

                # Judge output (will use next provider)
                scores = self._judge_output(task, skill_output)

                execution_time_ms = int((time.time() - start_time) * 1000)

                result = TaskResult(
                    task_id=task_id,
                    difficulty=task.get("difficulty", "unknown"),
                    category=task.get("category", "unknown"),
                    input_text=task["input"],
                    skill_output=skill_output[:500],
                    success_criteria=task.get("success_criteria", ""),
                    model_used=exec_provider,
                    intent_accuracy=scores.get("intent_accuracy", 0),
                    constraint_coverage=scores.get("constraint_coverage", 0),
                    output_quality=scores.get("output_quality", 0),
                    verix_compliance=scores.get("verix_compliance", 0),
                    l2_purity=scores.get("l2_purity", 0),
                    passed=scores.get("passed", False),
                    judge_reasoning=scores.get("reasoning", ""),
                    execution_time_ms=execution_time_ms
                )

                status = "PASS" if result.passed else "FAIL"
                print(f"[{i+1}/{len(tasks)}] {task_id} ({exec_provider})... {status} ({execution_time_ms}ms)")

            except Exception as e:
                result = TaskResult(
                    task_id=task_id,
                    difficulty=task.get("difficulty", "unknown"),
                    category=task.get("category", "unknown"),
                    input_text=task["input"],
                    skill_output="",
                    success_criteria=task.get("success_criteria", ""),
                    model_used="error",
                    passed=False,
                    judge_reasoning=f"Error: {str(e)}"
                )
                print(f"[{i+1}/{len(tasks)}] {task_id}... ERROR: {e}")

            results.append(result)

        passed = sum(1 for r in results if r.passed)

        eval_result = EvaluationResult(
            skill_name=self.skill_name,
            version=self.corpus.get("version", "unknown"),
            timestamp=datetime.now().isoformat(),
            total_tasks=len(results),
            passed_tasks=passed,
            models_used=list(models_used),
            task_results=results
        )

        # Save results
        output_file = self.RESULTS_DIR / f"{self.skill_name}-multi-eval-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(asdict(eval_result), f, indent=2, default=str)

        print(f"\nResults saved: {output_file}")
        return eval_result

    def print_summary(self, result: EvaluationResult):
        print(f"\n{'='*60}")
        print(f"SUMMARY: {result.skill_name}")
        print(f"{'='*60}")
        print(f"Pass Rate: {result.pass_rate:.1%} ({result.passed_tasks}/{result.total_tasks})")
        print(f"Models Used: {', '.join(result.models_used)}")

        # Group by category
        by_category = {}
        for tr in result.task_results:
            cat = tr.category
            if cat not in by_category:
                by_category[cat] = {"pass": 0, "fail": 0}
            if tr.passed:
                by_category[cat]["pass"] += 1
            else:
                by_category[cat]["fail"] += 1

        print(f"\nBy Category:")
        for cat, counts in by_category.items():
            total = counts["pass"] + counts["fail"]
            rate = counts["pass"] / total if total > 0 else 0
            print(f"  {cat}: {rate:.0%} ({counts['pass']}/{total})")

        # Show failures
        failures = [tr for tr in result.task_results if not tr.passed]
        if failures:
            print(f"\nFailures ({len(failures)}):")
            for tr in failures[:10]:
                print(f"  {tr.task_id} ({tr.model_used}): {tr.judge_reasoning[:80]}")


if __name__ == "__main__":
    skill = sys.argv[1] if len(sys.argv) > 1 else "prompt-architect"
    max_tasks = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    evaluator = MultiModelEvaluator(skill)
    result = evaluator.run_evaluation(max_tasks=max_tasks)
    evaluator.print_summary(result)
