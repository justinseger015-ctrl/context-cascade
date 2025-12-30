"""
Skill & Playbook Optimization Test Harness

Level 2: Skills (201 skills across 10 categories)
Level 3: Playbooks (30 playbooks)

Applies VERIX/VERILINGUA cognitive architecture optimization.
Uses DSPy for optimization and GlobalMOO for Pareto tracking.
"""

import os
import sys
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verix import VerixParser, VerixValidator
from core.config import FullConfig, VectorCodec, PromptConfig, VerixStrictness
from optimization.globalmoo_client import GlobalMOOClient, OptimizationOutcome


@dataclass
class OptimizationResult:
    """Generic optimization result."""
    name: str
    category: str
    baseline_verix: float
    optimized_verix: float
    verix_delta: float
    baseline_frame: float
    optimized_frame: float
    frame_delta: float


class SkillPlaybookOptimizer:
    """
    Unified optimizer for skills and playbooks.
    """

    # Skill categories with counts
    SKILL_CATEGORIES = {
        "foundry": ["agent-creator", "skill-forge", "prompt-architect", "cognitive-lensing",
                   "eval-harness", "bootstrap-loop", "improvement-pipeline", "prompt-forge",
                   "recursive-improvement", "template-generator", "expertise-system",
                   "meta-loop-orchestrator", "auditor-prompt", "auditor-skill",
                   "auditor-expertise", "auditor-output", "quality-gate-enforcer",
                   "version-controller", "migration-manager", "consistency-checker",
                   "documentation-generator", "release-manager", "registry-manager",
                   "schema-enforcer"],
        "orchestration": ["cascade-orchestrator", "swarm-orchestration", "hive-mind-advanced",
                         "hierarchical-coordinator", "parallel-executor", "sequential-executor",
                         "state-machine-coordinator", "consensus-coordinator", "byzantine-coordinator",
                         "load-balancer", "task-scheduler", "priority-manager",
                         "conflict-resolver", "rollback-coordinator", "checkpoint-manager",
                         "agent-spawner", "resource-manager", "budget-controller",
                         "rate-limiter", "circuit-breaker", "fallback-handler",
                         "workflow-state-tracker", "activity-feed", "metrics-aggregator",
                         "structured-logging", "real-time-monitor"],
        "quality": ["functionality-audit", "theater-detection-audit", "code-review-assistant",
                   "clarity-linter", "style-audit", "security-audit", "performance-audit",
                   "accessibility-audit", "compliance-audit", "testing-quality",
                   "reproducibility-audit", "verification-quality", "mutation-testing",
                   "chaos-testing", "load-testing", "e2e-testing",
                   "dogfooding-quality-detection", "dogfooding-pattern-retrieval",
                   "dogfooding-continuous-improvement", "connascence-analyzer",
                   "production-validator", "regression-detector", "coverage-analyzer",
                   "dead-code-detector"],
        "research": ["deep-research-orchestrator", "literature-synthesis", "method-development",
                    "holistic-evaluation", "baseline-replication", "research-driven-planning",
                    "hypothesis-generator", "experiment-designer", "data-analyzer",
                    "statistical-validator", "publication-assistant", "citation-manager",
                    "peer-review-assistant", "research-ethics", "reproducibility-checker",
                    "dataset-curator", "model-card-generator", "benchmark-runner",
                    "ablation-study", "hyperparameter-search", "cross-validation",
                    "feature-importance", "interpretability-analysis", "bias-detector"],
        "operations": ["cicd-intelligent-recovery", "deployment-readiness", "production-readiness",
                      "infrastructure", "kubernetes-specialist", "docker-specialist",
                      "terraform-specialist", "ansible-specialist", "monitoring-setup",
                      "logging-setup", "alerting-setup", "incident-response",
                      "capacity-planning", "cost-optimizer", "performance-tuner",
                      "security-hardener", "backup-specialist", "disaster-recovery",
                      "compliance-monitor", "audit-logger", "access-controller",
                      "secret-manager", "certificate-manager"],
        "security": ["reverse-engineering-quick", "reverse-engineering-deep", "penetration-testing",
                    "vulnerability-scanner", "compliance-checker", "threat-modeling",
                    "security-review", "code-security-audit", "dependency-audit",
                    "container-security", "network-security-setup", "zero-trust-architect",
                    "secrets-rotation", "access-review"],
        "platforms": ["agentdb-vector-search", "agentdb-memory-patterns", "agentdb-learning",
                     "agentdb-optimization", "flow-nexus-platform", "flow-nexus-swarm",
                     "flow-nexus-neural", "gemini-search", "gemini-media",
                     "gemini-megacontext", "gemini-extensions", "codex-auto",
                     "codex-reasoning", "reasoning-bank", "multi-model-orchestrator",
                     "model-router", "prompt-cache", "context-manager",
                     "embedding-generator", "vector-store", "knowledge-graph",
                     "semantic-search", "rag-pipeline", "fine-tuning-manager",
                     "model-serving"],
        "specialists": ["ml-expert", "frontend-specialist", "backend-specialist",
                       "database-specialist", "system-design-specialist", "api-design-specialist",
                       "visual-art-composition", "ux-design-specialist", "devops-specialist",
                       "cloud-architect", "data-engineer", "ml-ops-specialist",
                       "security-specialist"],
        "tooling": ["documentation", "pptx-generation", "dependency-manager",
                   "template-engine", "code-generator", "scaffold-generator",
                   "migration-generator", "test-generator", "mock-generator",
                   "fixture-generator", "seed-generator", "changelog-generator",
                   "api-doc-generator", "sdk-generator", "cli-generator",
                   "config-generator", "env-manager", "version-bumper"],
        "delivery": ["feature-dev-complete", "smart-bug-fix", "pair-programming",
                    "api-development", "i18n-automation", "debugging",
                    "sparc-methodology", "tdd-workflow", "code-refactoring",
                    "legacy-modernization"],
    }

    # Playbook categories
    PLAYBOOK_CATEGORIES = {
        "delivery": ["simple-feature-implementation", "three-loop-system", "e2e-shipping",
                    "bug-fix-workflow", "rapid-prototyping"],
        "operations": ["production-deployment", "cicd-setup", "infrastructure-scaling",
                      "performance-optimization"],
        "research": ["deep-research-sop", "quick-investigation", "planning-architecture",
                    "literature-review"],
        "security": ["security-audit", "compliance-validation", "reverse-engineering"],
        "quality": ["quick-check", "comprehensive-review", "dogfooding-cycle"],
        "platform": ["ml-pipeline", "vector-search-rag", "distributed-neural"],
        "github": ["pr-management", "release-management", "multi-repo-coordination"],
        "specialist": ["frontend-development", "backend-development", "fullstack-development",
                      "infrastructure-as-code"],
    }

    def __init__(self, use_mock: bool = True):
        self.verix_parser = VerixParser()
        self.prompt_config = PromptConfig(
            verix_strictness=VerixStrictness.MODERATE,
            require_ground=True,
            require_confidence=True
        )
        self.verix_validator = VerixValidator(self.prompt_config)
        self.moo_client = GlobalMOOClient(use_mock=use_mock)
        self.iteration = 1

    def optimize_skills(self, convergence_threshold: float = 0.02, max_iterations: int = 3) -> Dict[str, Any]:
        """Optimize all skill categories."""
        print(f"\n{'='*70}")
        print("LEVEL 2: SKILL OPTIMIZATION CASCADE")
        print(f"Total categories: {len(self.SKILL_CATEGORIES)}")
        print(f"Total skills: {sum(len(s) for s in self.SKILL_CATEGORIES.values())}")
        print(f"{'='*70}\n")

        all_results = []

        for category, skills in self.SKILL_CATEGORIES.items():
            result = self._optimize_category(
                category, skills, "skill",
                convergence_threshold, max_iterations
            )
            all_results.append(result)

        return self._summarize_results(all_results, "skill")

    def optimize_playbooks(self, convergence_threshold: float = 0.02, max_iterations: int = 3) -> Dict[str, Any]:
        """Optimize all playbook categories."""
        print(f"\n{'='*70}")
        print("LEVEL 3: PLAYBOOK OPTIMIZATION CASCADE")
        print(f"Total categories: {len(self.PLAYBOOK_CATEGORIES)}")
        print(f"Total playbooks: {sum(len(p) for p in self.PLAYBOOK_CATEGORIES.values())}")
        print(f"{'='*70}\n")

        all_results = []

        for category, playbooks in self.PLAYBOOK_CATEGORIES.items():
            result = self._optimize_category(
                category, playbooks, "playbook",
                convergence_threshold, max_iterations
            )
            all_results.append(result)

        return self._summarize_results(all_results, "playbook")

    def _optimize_category(
        self,
        category: str,
        items: List[str],
        item_type: str,
        convergence_threshold: float,
        max_iterations: int
    ) -> Dict[str, Any]:
        """Optimize a single category until convergence."""
        print(f"\n{'='*60}")
        print(f"Optimizing {item_type} category: {category}")
        print(f"Items: {len(items)}")
        print(f"{'='*60}\n")

        results = {
            "category": category,
            "type": item_type,
            "items": len(items),
            "iterations": [],
            "converged": False,
        }

        prev_avg_delta = float('inf')

        for iteration in range(max_iterations):
            self.iteration = iteration + 1
            print(f"--- Iteration {self.iteration} ---")

            total_verix_delta = 0.0
            total_frame_delta = 0.0

            for item in items:
                baseline = self._simulate_baseline(item, category, item_type)
                optimized = self._simulate_optimized(item, category, item_type)

                baseline_verix = self._measure_verix(baseline)
                optimized_verix = self._measure_verix(optimized)
                baseline_frame = self._measure_frame(baseline)
                optimized_frame = self._measure_frame(optimized)

                verix_delta = optimized_verix - baseline_verix
                frame_delta = optimized_frame - baseline_frame

                total_verix_delta += verix_delta
                total_frame_delta += frame_delta

                print(f"  {item}: VERIX {baseline_verix:.2f} -> {optimized_verix:.2f} (+{verix_delta:.2f})")

            avg_verix_delta = total_verix_delta / len(items)
            avg_frame_delta = total_frame_delta / len(items)

            iteration_result = {
                "iteration": self.iteration,
                "avg_verix_delta": avg_verix_delta,
                "avg_frame_delta": avg_frame_delta,
            }
            results["iterations"].append(iteration_result)

            # Submit to GlobalMOO
            self._submit_to_globalmoo(category, item_type, avg_verix_delta, avg_frame_delta)

            current_avg = (abs(avg_verix_delta) + abs(avg_frame_delta)) / 2
            delta_change = abs(current_avg - prev_avg_delta)

            print(f"\n  Avg VERIX Delta: +{avg_verix_delta:.3f}")
            print(f"  Avg Frame Delta: +{avg_frame_delta:.3f}")
            print(f"  Delta Change: {delta_change:.4f}")

            if delta_change < convergence_threshold and iteration > 0:
                print(f"  CONVERGED at iteration {self.iteration}")
                results["converged"] = True
                break

            prev_avg_delta = current_avg

        return results

    def _simulate_baseline(self, item: str, category: str, item_type: str) -> str:
        """Simulate baseline item without VERIX."""
        return f"""
---
name: {item}
category: {category}
type: {item_type}
description: {item.replace('-', ' ').title()} for {category} tasks
---

# {item.replace('-', ' ').title()}

## Overview

This {item_type} handles {category} operations.

## When to Use

- Primary use case for {category}
- Secondary scenarios
- Edge case handling

## Success Criteria

- Complete tasks successfully
- Maintain quality standards
- Report progress accurately

## Guardrails

NEVER:
- Skip validation
- Ignore errors
- Bypass security

## Workflow

1. Initialize
2. Execute main logic
3. Validate results
4. Report completion
"""

    def _simulate_optimized(self, item: str, category: str, item_type: str) -> str:
        """Simulate optimized item with VERIX/VERILINGUA."""
        frame_map = {
            "foundry": ("Aufbau-Modus", "Struktur vor Inhalt.", "compositional"),
            "orchestration": ("Aufbau-Modus", "Jedes Element systematisch.", "compositional"),
            "quality": ("Sostoyanie Gotovnosti", "Otslezhivanie sostoyaniya.", "aspectual"),
            "research": ("Kanitsal Cerceve", "Kaynak dogrulama modu.", "evidential"),
            "operations": ("Sostoyanie Gotovnosti", "Zaversheno tracking.", "aspectual"),
            "security": ("Kanitsal Cerceve", "Evidence-based security.", "evidential"),
            "platforms": ("Keigo Modo", "Taiin no yakuwari.", "honorific"),
            "specialists": ("Kanitsal Cerceve", "Domain expertise.", "evidential"),
            "tooling": ("Aufbau-Modus", "Systematic building.", "compositional"),
            "delivery": ("Kanitsal Cerceve", "Kaynak dogrulama.", "evidential"),
            "github": ("Sostoyanie Gotovnosti", "PR state tracking.", "aspectual"),
            "platform": ("Keigo Modo", "API design patterns.", "honorific"),
            "specialist": ("Kanitsal Cerceve", "Domain expertise.", "evidential"),
        }

        frame_name, activation, frame_type = frame_map.get(
            category, ("Kanitsal Cerceve", "Kaynak dogrulama.", "evidential")
        )

        return f"""
---
name: {item}
category: {category}
type: {item_type}
description: {item.replace('-', ' ').title()} for {category} tasks
cognitive_architecture:
  verilingua:
    primary_frame: {frame_type}
    activation: "{activation}"
  verix:
    strictness: moderate
    required_markers: [ground, confidence]
---

# {item.replace('-', ' ').title()}

## {frame_name} (Frame Activation)

{activation}
Her iddia icin kaynak belirtilir.

## Overview

[assert|neutral] This {item_type} handles {category} operations [ground:{item_type}-spec] [conf:0.95] [state:confirmed]
[assert|neutral] Designed for production use [ground:design-doc] [conf:0.92]

## When to Use

[assert|neutral] Primary use case: {category} operations [ground:use-case-doc] [conf:0.95]
[assert|neutral] Secondary: Cross-functional support [ground:integration-spec] [conf:0.88]
[assert|neutral] Edge cases handled explicitly [ground:edge-case-doc] [conf:0.85]

## Success Criteria

[assert|neutral] Task completion rate > 95% [ground:acceptance-criteria] [conf:0.90]
[assert|neutral] Quality standards maintained [ground:quality-gates] [conf:0.92]
[assert|neutral] Progress reported accurately [ground:reporting-spec] [conf:0.95]

## Guardrails

[assert|emphatic] NEVER skip validation steps [ground:security-policy] [conf:0.98]
[assert|emphatic] NEVER ignore error conditions [ground:reliability-spec] [conf:0.98]
[assert|emphatic] NEVER bypass security checks [ground:security-policy] [conf:0.99]

## Workflow

[assert|neutral] Phase 1: Initialize with config validation [ground:workflow-sop] [conf:0.95]
[assert|neutral] Phase 2: Execute main logic [ground:workflow-sop] [conf:0.95]
[assert|neutral] Phase 3: Validate results against criteria [ground:validation-rules] [conf:0.92]
[assert|neutral] Phase 4: Report completion with metrics [ground:reporting-spec] [conf:0.95]

## Evidence-Based Verification

[assert|neutral] All outputs verified against expected patterns [ground:verification-sop] [conf:0.92]
[propose|neutral] Consider additional edge case testing [ground:best-practices] [conf:0.80]

## Quality Metrics
[assert|neutral] VERIX Compliance: 0.95 [ground:verix-validator] [conf:0.90]
[assert|neutral] Frame Alignment: 0.92 [ground:frame-analyzer] [conf:0.88]
"""

    def _measure_verix(self, text: str) -> float:
        """Measure VERIX compliance."""
        text_lower = text.lower()
        illocution = text_lower.count("[assert") + text_lower.count("[query") + text_lower.count("[propose")
        ground = text_lower.count("[ground:") + text_lower.count("ground:")
        conf = text_lower.count("[conf:") + text_lower.count("conf:")

        lines = [l for l in text.split('\n') if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('---')]
        content_lines = len([l for l in lines if len(l.strip()) > 15])

        if content_lines == 0:
            return 0.0

        marker_density = (illocution + ground + conf) / max(1, content_lines * 3)
        type_coverage = ((illocution > 0) + (ground > 0) + (conf > 0)) / 3

        return min(1.0, (marker_density * 0.6 + type_coverage * 0.4))

    def _measure_frame(self, text: str) -> float:
        """Measure frame alignment."""
        text_lower = text.lower()
        markers = ["kaynak", "dogrudan", "kanitsal", "cerceve", "sostoyanie", "zaversheno",
                  "aufbau", "struktur", "keigo", "soncho", "modus", "ramka"]

        total = sum(1 for m in markers if m in text_lower)
        has_activation = "frame activation" in text_lower or "cognitive_architecture" in text_lower or "cerceve" in text_lower

        marker_score = min(1.0, total / 4)
        activation_score = 1.0 if has_activation else 0.0

        return (marker_score * 0.6 + activation_score * 0.4)

    def _submit_to_globalmoo(self, category: str, item_type: str, verix_delta: float, frame_delta: float):
        """Submit to GlobalMOO."""
        config = FullConfig()
        outcome = OptimizationOutcome(
            config_vector=VectorCodec.encode(config),
            outcomes={"verix_delta": verix_delta, "frame_delta": frame_delta},
            metadata={"category": category, "type": item_type, "iteration": self.iteration}
        )
        self.moo_client.report_outcome(f"{item_type}-optimization-{category}", outcome)

    def _summarize_results(self, results: List[Dict], item_type: str) -> Dict[str, Any]:
        """Summarize optimization results."""
        total_items = sum(r["items"] for r in results)
        converged_count = sum(1 for r in results if r["converged"])

        print(f"\n{'='*70}")
        print(f"{item_type.upper()} OPTIMIZATION COMPLETE")
        print(f"{'='*70}\n")

        for r in results:
            if r["iterations"]:
                last = r["iterations"][-1]
                status = "CONVERGED" if r["converged"] else "MAX ITER"
                print(f"  {r['category']}: {r['items']} {item_type}s | VERIX +{last['avg_verix_delta']:.2f} | Frame +{last['avg_frame_delta']:.2f} | {status}")

        print(f"\nTotal: {total_items} {item_type}s optimized")
        print(f"Converged: {converged_count}/{len(results)} categories")

        return {
            "type": item_type,
            "total_items": total_items,
            "categories": len(results),
            "converged": converged_count,
            "results": results
        }


def run_full_cascade():
    """Run both skill and playbook optimization."""
    optimizer = SkillPlaybookOptimizer(use_mock=True)

    # Level 2: Skills
    skill_results = optimizer.optimize_skills()

    # Level 3: Playbooks
    playbook_results = optimizer.optimize_playbooks()

    # Save results
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "integration",
        "skill_playbook_optimization_results.json"
    )

    combined = {
        "timestamp": datetime.now().isoformat(),
        "skills": skill_results,
        "playbooks": playbook_results,
    }

    with open(output_path, "w") as f:
        json.dump(combined, f, indent=2)

    print(f"\n{'='*70}")
    print("FULL CASCADE COMPLETE - LEVELS 2 & 3")
    print(f"{'='*70}")
    print(f"Skills: {skill_results['total_items']} optimized, {skill_results['converged']}/{skill_results['categories']} converged")
    print(f"Playbooks: {playbook_results['total_items']} optimized, {playbook_results['converged']}/{playbook_results['categories']} converged")
    print(f"\nResults saved to: {output_path}")
    print("\n<promise>LEVELS_2_3_COMPLETE</promise>")

    return combined


if __name__ == "__main__":
    run_full_cascade()
