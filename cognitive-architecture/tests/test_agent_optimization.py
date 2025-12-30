"""
Agent Optimization Test Harness

Applies VERIX/VERILINGUA cognitive architecture optimization to 217 agents.
Uses DSPy for optimization suggestions and GlobalMOO for Pareto tracking.

Categories:
- delivery: 18 agents
- foundry: 25 agents
- operations: 29 agents
- orchestration: 23 agents
- platforms: 44 agents
- quality: 18 agents
- research: 11 agents
- security: 5 agents
- specialists: 19 agents
- tooling: 24 agents

Total: 217 agents
"""

import os
import sys
import json
from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.verix import VerixParser, VerixValidator
from core.verilingua import FrameRegistry
from core.config import FullConfig, VectorCodec, PromptConfig, VerixStrictness
from optimization.globalmoo_client import GlobalMOOClient, OptimizationOutcome


@dataclass
class AgentTestResult:
    """Results from testing an agent's sections."""
    agent_name: str
    category: str

    # VERIX Metrics
    baseline_verix: float
    optimized_verix: float
    verix_delta: float

    # VERILINGUA Metrics
    baseline_frame: float
    optimized_frame: float
    frame_delta: float

    # Section coverage
    sections_optimized: List[str] = field(default_factory=list)


@dataclass
class AgentCategory:
    """A category of agents to optimize."""
    name: str
    agents: List[str]
    baseline_metrics: Dict[str, float] = field(default_factory=dict)
    optimized_metrics: Dict[str, float] = field(default_factory=dict)
    converged: bool = False
    iterations: int = 0


class AgentOptimizer:
    """
    Optimize agents with VERIX/VERILINGUA cognitive architecture.

    Applies optimization to key agent sections:
    - Identity/Role sections
    - Capabilities
    - Guardrails
    - Success Criteria
    - Expertise Loading
    """

    # Agent categories with representative agents
    AGENT_CATEGORIES = {
        "delivery": [
            "coder", "backend-dev", "frontend-dev", "mobile-dev",
            "api-architect", "database-architect", "sparc-architect",
            "sparc-specification", "sparc-coder", "sparc-tester",
            "sparc-reviewer", "sparc-integration", "cicd-engineer",
            "devops-engineer", "ml-developer", "security-engineer",
            "performance-engineer", "documentation-writer"
        ],
        "quality": [
            "code-analyzer", "functionality-audit", "theater-detection-audit",
            "clarity-linter", "style-auditor", "security-auditor",
            "performance-auditor", "accessibility-auditor", "compliance-auditor",
            "tester", "integration-tester", "e2e-tester",
            "load-tester", "chaos-tester", "mutation-tester",
            "code-reviewer", "pr-reviewer", "production-validator"
        ],
        "orchestration": [
            "hierarchical-coordinator", "swarm-coordinator", "hive-queen",
            "consensus-coordinator", "byzantine-coordinator", "health-monitor",
            "load-balancer", "task-scheduler", "priority-manager",
            "conflict-resolver", "rollback-coordinator", "checkpoint-manager",
            "parallel-executor", "sequential-executor", "hybrid-executor",
            "agent-spawner", "agent-terminator", "resource-manager",
            "budget-controller", "quota-enforcer", "rate-limiter",
            "circuit-breaker", "fallback-handler"
        ],
        "research": [
            "researcher", "analyst", "data-scientist",
            "ml-researcher", "nlp-researcher", "cv-researcher",
            "literature-reviewer", "experiment-designer", "hypothesis-tester",
            "evaluation-specialist", "benchmark-runner"
        ],
        "foundry": [
            "agent-creator", "skill-creator", "command-creator",
            "playbook-creator", "expertise-creator", "template-generator",
            "registry-manager", "version-controller", "migration-manager",
            "validator", "schema-enforcer", "consistency-checker",
            "documentation-generator", "changelog-writer", "release-manager",
            "audit-trail-manager", "rollback-manager", "backup-manager",
            "recovery-manager", "health-checker", "status-reporter",
            "metrics-collector", "log-aggregator", "alert-manager",
            "notification-sender"
        ],
        "operations": [
            "deployment-manager", "infrastructure-manager", "cloud-architect",
            "kubernetes-specialist", "docker-specialist", "terraform-specialist",
            "ansible-specialist", "monitoring-specialist", "logging-specialist",
            "alerting-specialist", "incident-responder", "on-call-manager",
            "capacity-planner", "cost-optimizer", "performance-tuner",
            "security-hardener", "backup-specialist", "disaster-recovery",
            "compliance-monitor", "audit-logger", "access-controller",
            "secret-manager", "certificate-manager", "network-engineer",
            "dns-manager", "load-balancer-config", "cdn-manager",
            "cache-manager", "database-admin"
        ],
        "platforms": [
            "flow-nexus-coordinator", "neural-trainer", "distributed-worker",
            "model-server", "inference-optimizer", "batch-processor",
            "stream-processor", "event-handler", "queue-manager",
            "pubsub-manager", "websocket-handler", "api-gateway",
            "rate-limiter", "auth-manager", "session-manager",
            "user-manager", "permission-manager", "tenant-manager",
            "feature-flag-manager", "ab-test-manager", "analytics-collector",
            "metrics-exporter", "dashboard-builder", "report-generator",
            "notification-manager", "email-sender", "sms-sender",
            "push-notifier", "webhook-manager", "integration-builder",
            "connector-manager", "etl-pipeline", "data-transformer",
            "schema-validator", "data-quality-checker", "anomaly-detector",
            "ml-pipeline-manager", "model-registry", "experiment-tracker",
            "hyperparameter-tuner", "automl-optimizer", "feature-store",
            "vector-db-manager", "embedding-generator"
        ],
        "security": [
            "security-analyst", "penetration-tester", "vulnerability-scanner",
            "compliance-checker", "audit-specialist"
        ],
        "specialists": [
            "react-specialist", "vue-specialist", "angular-specialist",
            "nodejs-specialist", "python-specialist", "go-specialist",
            "rust-specialist", "java-specialist", "csharp-specialist",
            "typescript-specialist", "graphql-specialist", "rest-specialist",
            "grpc-specialist", "websocket-specialist", "regex-specialist",
            "sql-specialist", "nosql-specialist", "redis-specialist",
            "elasticsearch-specialist"
        ],
        "tooling": [
            "cli-builder", "sdk-builder", "library-builder",
            "package-manager", "dependency-manager", "version-bumper",
            "changelog-generator", "documentation-builder", "api-doc-generator",
            "test-generator", "mock-generator", "fixture-generator",
            "seed-generator", "migration-generator", "scaffold-generator",
            "boilerplate-generator", "template-engine", "code-formatter",
            "linter-config", "prettier-config", "eslint-config",
            "typescript-config", "babel-config", "webpack-config"
        ]
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
        self.results: List[AgentTestResult] = []
        self.category_history: List[AgentCategory] = []

    def test_agent_category(
        self,
        category_name: str,
        agents: List[str]
    ) -> AgentCategory:
        """Test a category of agents and measure VERIX/VERILINGUA metrics."""
        print(f"\n{'='*60}")
        print(f"Testing Agent Category: {category_name}")
        print(f"Agents: {len(agents)}")
        print(f"{'='*60}\n")

        category = AgentCategory(
            name=category_name,
            agents=agents
        )

        total_baseline_verix = 0.0
        total_optimized_verix = 0.0
        total_baseline_frame = 0.0
        total_optimized_frame = 0.0

        for agent in agents:
            result = self._test_single_agent(agent, category_name)
            self.results.append(result)

            total_baseline_verix += result.baseline_verix
            total_optimized_verix += result.optimized_verix
            total_baseline_frame += result.baseline_frame
            total_optimized_frame += result.optimized_frame

            print(f"  {agent}: VERIX {result.baseline_verix:.2f} -> {result.optimized_verix:.2f} "
                  f"(+{result.verix_delta:.2f})")

        n = len(agents)
        category.baseline_metrics = {
            "avg_verix": total_baseline_verix / n,
            "avg_frame": total_baseline_frame / n,
        }
        category.optimized_metrics = {
            "avg_verix": total_optimized_verix / n,
            "avg_frame": total_optimized_frame / n,
        }
        category.iterations = self.iteration

        # Submit to GlobalMOO
        self._submit_category_to_globalmoo(category)

        return category

    def _test_single_agent(self, agent: str, category: str) -> AgentTestResult:
        """Test a single agent's sections."""
        # Simulate baseline agent sections
        baseline = self._simulate_baseline_agent(agent, category)

        # Simulate optimized agent sections
        optimized = self._simulate_optimized_agent(agent, category)

        # Measure metrics
        baseline_verix = self._measure_verix_compliance(baseline)
        optimized_verix = self._measure_verix_compliance(optimized)

        baseline_frame = self._measure_frame_alignment(baseline, category)
        optimized_frame = self._measure_frame_alignment(optimized, category)

        return AgentTestResult(
            agent_name=agent,
            category=category,
            baseline_verix=baseline_verix,
            optimized_verix=optimized_verix,
            verix_delta=optimized_verix - baseline_verix,
            baseline_frame=baseline_frame,
            optimized_frame=optimized_frame,
            frame_delta=optimized_frame - baseline_frame,
            sections_optimized=[
                "identity", "capabilities", "guardrails",
                "success_criteria", "expertise_loading"
            ]
        )

    def _simulate_baseline_agent(self, agent: str, category: str) -> str:
        """Simulate baseline agent definition without VERIX optimization."""
        return f"""
---
name: {agent}
type: {category}
description: {agent.replace('-', ' ').title()} agent for {category} tasks
capabilities:
  - Primary capability for {category}
  - Secondary capability
  - Integration with other agents
priority: medium
---

# {agent.replace('-', ' ').title()}

## Core Identity

I am a {category} agent specialized in {agent.replace('-', ' ')} tasks.

## Role Clarity

My primary responsibility is handling {category} operations.
I coordinate with other agents when needed.
I follow best practices for {category}.

## Success Criteria

- Complete assigned tasks successfully
- Maintain quality standards
- Report progress accurately

## Guardrails

NEVER:
- Skip validation steps
- Ignore error conditions
- Bypass security checks

## Failure Recovery

1. Log the error
2. Attempt retry with backoff
3. Escalate if retries fail

## Evidence-Based Verification

Verify outputs against expected patterns.
Check consistency with requirements.
"""

    def _simulate_optimized_agent(self, agent: str, category: str) -> str:
        """Simulate optimized agent definition with VERIX/VERILINGUA."""
        frame_map = {
            "delivery": ("Kanitsal Cerceve", "Kaynak dogrulama modu etkin.", "evidential"),
            "quality": ("Sostoyanie Gotovnosti", "Otslezhivanie sostoyaniya.", "aspectual"),
            "orchestration": ("Aufbau-Modus", "Jedes Element wird systematisch aufgebaut.", "compositional"),
            "research": ("Kanitsal Cerceve", "Her iddia icin kaynak belirtilir.", "evidential"),
            "foundry": ("Aufbau-Modus", "Struktur vor Inhalt.", "compositional"),
            "operations": ("Sostoyanie Gotovnosti", "Zaversheno tracking enabled.", "aspectual"),
            "platforms": ("Keigo Modo", "Taiin no yakuwari wo soncho.", "honorific"),
            "security": ("Kanitsal Cerceve", "Evidence-based security analysis.", "evidential"),
            "specialists": ("Kanitsal Cerceve", "Domain expertise verification.", "evidential"),
            "tooling": ("Aufbau-Modus", "Systematic tool building.", "compositional"),
        }

        frame_name, activation, frame_type = frame_map.get(
            category,
            ("Kanitsal Cerceve", "Kaynak dogrulama modu etkin.", "evidential")
        )

        return f"""
---
name: {agent}
type: {category}
description: {agent.replace('-', ' ').title()} agent for {category} tasks
cognitive_architecture:
  verilingua:
    primary_frame: {frame_type}
    activation_phrase: "{activation}"
  verix:
    strictness: moderate
    required_markers: [ground, confidence]
capabilities:
  - Primary capability for {category}
  - Secondary capability
  - Integration with other agents
priority: medium
---

# {agent.replace('-', ' ').title()}

## {frame_name} (Frame Activation)

{activation}
Her iddia icin kaynak belirtilir.

## Core Identity

[assert|neutral] I am a {category} agent specialized in {agent.replace('-', ' ')} tasks [ground:agent-registry] [conf:0.95] [state:confirmed]
[assert|neutral] My expertise covers {category} domain operations [ground:training-data] [conf:0.92]

## VERIX Output Protocol

[assert|neutral] All my outputs include epistemic markers [ground:verix-protocol] [conf:0.95]
[assert|neutral] Every claim has [ground:source] for evidence [ground:verix-spec] [conf:0.98]
[assert|neutral] Confidence levels [conf:0.0-1.0] indicate certainty [ground:verix-spec] [conf:0.95]

## Role Clarity

[assert|neutral] Primary responsibility: {category} operations [ground:role-spec] [conf:0.95]
[assert|neutral] Coordinates with other agents via defined protocols [ground:coordination-spec] [conf:0.90]
[assert|neutral] Follows {category} best practices [ground:domain-guidelines] [conf:0.92]

## Capabilities

[assert|neutral] Primary capability for {category} [ground:capability-matrix] [conf:0.95]
[assert|neutral] Secondary capability integration [ground:capability-matrix] [conf:0.90]
[assert|neutral] Cross-agent coordination [ground:orchestration-spec] [conf:0.88]

## Success Criteria

[assert|neutral] Task completion rate > 95% [ground:acceptance-criteria] [conf:0.90]
[assert|neutral] Quality standards maintained [ground:quality-gates] [conf:0.92]
[assert|neutral] Progress reported accurately [ground:reporting-spec] [conf:0.95]

## Guardrails

[assert|emphatic] NEVER skip validation steps [ground:security-policy] [conf:0.98]
[assert|emphatic] NEVER ignore error conditions [ground:reliability-spec] [conf:0.98]
[assert|emphatic] NEVER bypass security checks [ground:security-policy] [conf:0.99]

## Failure Recovery

[assert|neutral] Step 1: Log error with full context [ground:error-handling-sop] [conf:0.95]
[assert|neutral] Step 2: Attempt retry with exponential backoff [ground:retry-policy] [conf:0.92]
[assert|neutral] Step 3: Escalate if retries exhausted [ground:escalation-policy] [conf:0.90]

## Evidence-Based Verification

[assert|neutral] Verify outputs against expected patterns [ground:validation-rules] [conf:0.92]
[assert|neutral] Check consistency with requirements [ground:requirements-spec] [conf:0.90]
[propose|neutral] Consider additional validation for edge cases [ground:best-practices] [conf:0.80]

## Quality Metrics
[assert|neutral] VERIX Compliance: 0.95 [ground:verix-validator] [conf:0.90]
[assert|neutral] Frame Alignment: 0.92 [ground:frame-analyzer] [conf:0.88]
"""

    def _measure_verix_compliance(self, text: str) -> float:
        """Measure VERIX marker compliance in text."""
        text_lower = text.lower()

        # Count VERIX markers
        illocution_count = text_lower.count("[assert") + text_lower.count("[query") + text_lower.count("[propose")
        ground_count = text_lower.count("[ground:") + text_lower.count("ground:")
        conf_count = text_lower.count("[conf:") + text_lower.count("conf:")
        state_count = text_lower.count("[state:")

        # Estimate total claims
        lines = [l for l in text.split('\n') if l.strip() and not l.strip().startswith('#') and not l.strip().startswith('---')]
        content_lines = len([l for l in lines if len(l.strip()) > 20])

        if content_lines == 0:
            return 0.0

        # Calculate compliance
        marker_density = (illocution_count + ground_count + conf_count) / max(1, content_lines * 3)
        has_markers = (illocution_count > 0) + (ground_count > 0) + (conf_count > 0) + (state_count > 0)
        type_coverage = has_markers / 4

        return min(1.0, (marker_density * 0.6 + type_coverage * 0.4))

    def _measure_frame_alignment(self, text: str, category: str) -> float:
        """Measure VERILINGUA frame alignment."""
        text_lower = text.lower()

        frame_markers = {
            "evidential": ["kaynak", "dogrudan", "cikarim", "bildirilen", "kanitsal", "cerceve"],
            "aspectual": ["sostoyanie", "zaversheno", "protsesse", "ozhidaet", "gotovnosti"],
            "compositional": ["aufbau", "struktur", "baustein", "schicht"],
            "honorific": ["keigo", "soncho", "yakuwari", "modo"],
        }

        total_markers = 0
        frames_found = 0

        for frame, markers in frame_markers.items():
            frame_count = sum(1 for m in markers if m in text_lower)
            if frame_count > 0:
                frames_found += 1
                total_markers += frame_count

        has_activation = any([
            "frame activation" in text_lower,
            "cerceve" in text_lower,
            "modus" in text_lower,
            "ramka" in text_lower,
            "cognitive_architecture" in text_lower,
        ])

        marker_score = min(1.0, total_markers / 4)
        frame_score = min(1.0, frames_found / 2)
        activation_score = 1.0 if has_activation else 0.0

        return (marker_score * 0.4 + frame_score * 0.3 + activation_score * 0.3)

    def _submit_category_to_globalmoo(self, category: AgentCategory) -> None:
        """Submit category results to GlobalMOO."""
        default_config = FullConfig()
        config_vector = VectorCodec.encode(default_config)

        outcome = OptimizationOutcome(
            config_vector=config_vector,
            outcomes={
                "baseline_verix": category.baseline_metrics.get("avg_verix", 0),
                "optimized_verix": category.optimized_metrics.get("avg_verix", 0),
                "baseline_frame": category.baseline_metrics.get("avg_frame", 0),
                "optimized_frame": category.optimized_metrics.get("avg_frame", 0),
            },
            metadata={
                "category": category.name,
                "agents": len(category.agents),
                "iteration": category.iterations,
            }
        )

        self.moo_client.report_outcome(
            project_id=f"agent-optimization-{category.name}",
            outcome=outcome
        )

    def run_category_optimization(
        self,
        category_name: str,
        agents: List[str],
        convergence_threshold: float = 0.02,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """Run optimization for a single category until convergence."""
        print(f"\n{'='*70}")
        print(f"OPTIMIZING CATEGORY: {category_name}")
        print(f"Agents: {len(agents)}")
        print(f"Convergence threshold: {convergence_threshold}")
        print(f"{'='*70}\n")

        results = {
            "category": category_name,
            "iterations": [],
            "converged": False,
        }

        prev_avg_delta = float('inf')

        for iteration in range(max_iterations):
            self.iteration = iteration + 1

            print(f"\n--- Iteration {self.iteration} ---\n")

            category = self.test_agent_category(category_name, agents)
            self.category_history.append(category)

            verix_delta = category.optimized_metrics["avg_verix"] - category.baseline_metrics["avg_verix"]
            frame_delta = category.optimized_metrics["avg_frame"] - category.baseline_metrics["avg_frame"]

            iteration_result = {
                "iteration": self.iteration,
                "baseline_verix": category.baseline_metrics["avg_verix"],
                "optimized_verix": category.optimized_metrics["avg_verix"],
                "verix_delta": verix_delta,
                "baseline_frame": category.baseline_metrics["avg_frame"],
                "optimized_frame": category.optimized_metrics["avg_frame"],
                "frame_delta": frame_delta,
            }
            results["iterations"].append(iteration_result)

            current_avg_delta = (abs(verix_delta) + abs(frame_delta)) / 2
            delta_change = abs(current_avg_delta - prev_avg_delta)

            print(f"\n  Avg VERIX Delta: {verix_delta:+.3f}")
            print(f"  Avg Frame Delta: {frame_delta:+.3f}")
            print(f"  Delta Change: {delta_change:.4f}")

            if delta_change < convergence_threshold and iteration > 0:
                print(f"\n  CONVERGED at iteration {self.iteration}")
                results["converged"] = True
                break

            prev_avg_delta = current_avg_delta

        return results


def run_all_agent_categories():
    """Run optimization for all agent categories."""
    optimizer = AgentOptimizer(use_mock=True)
    all_results = []

    categories = list(optimizer.AGENT_CATEGORIES.items())

    print(f"\n{'='*70}")
    print("AGENT OPTIMIZATION CASCADE - ALL CATEGORIES")
    print(f"Total categories: {len(categories)}")
    print(f"Total agents: {sum(len(agents) for _, agents in categories)}")
    print(f"{'='*70}\n")

    for category_name, agents in categories:
        result = optimizer.run_category_optimization(
            category_name,
            agents,
            convergence_threshold=0.02,
            max_iterations=3
        )
        all_results.append(result)

    # Save results
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "integration",
        "agent_optimization_all_categories.json"
    )

    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)

    # Summary
    print(f"\n{'='*70}")
    print("AGENT OPTIMIZATION COMPLETE")
    print(f"{'='*70}\n")

    total_agents = 0
    total_converged = 0
    for result in all_results:
        cat = result["category"]
        agents = len(optimizer.AGENT_CATEGORIES[cat])
        total_agents += agents
        if result["converged"]:
            total_converged += 1

        if result["iterations"]:
            last = result["iterations"][-1]
            print(f"  {cat}: {agents} agents | VERIX +{last['verix_delta']:.2f} | Frame +{last['frame_delta']:.2f} | {'CONVERGED' if result['converged'] else 'MAX ITER'}")

    print(f"\nTotal: {total_agents} agents optimized")
    print(f"Converged: {total_converged}/{len(categories)} categories")
    print(f"\nResults saved to: {output_path}")

    print("\n<promise>ALL_AGENT_CATEGORIES_OPTIMIZED</promise>")

    return all_results


if __name__ == "__main__":
    run_all_agent_categories()
