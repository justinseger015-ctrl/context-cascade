#!/bin/bash
# pre-task-spawn.sh
# Hook: PreToolUse on Task
# Purpose: Display agent registry reminder
#
# CRITICAL LIMITATION: This hook CANNOT inspect Task() parameters
# due to Claude Code hook constraints. We can only display reminders.

cat << 'EOF'

============================================================
!! TASK (AGENT SPAWN) DETECTED !!
============================================================

You are about to spawn an agent via Task().

CRITICAL: Agent type MUST be from registry!

AGENT REGISTRY: claude-code-plugins/context-cascade/agents/

VALID CATEGORIES (217 agents):

  1. DELIVERY (18 agents)
     - coder, backend-dev, frontend-dev, fullstack-dev
     - mobile-dev, devops-engineer, sre, release-engineer
     - api-developer, database-dev, integration-dev, etc.

  2. RESEARCH (11 agents)
     - researcher, analyst, data-scientist, ml-engineer
     - experiment-designer, paper-reader, etc.

  3. QUALITY (18 agents)
     - tester, qa-engineer, security-tester, load-tester
     - reviewer, code-analyzer, auditor, compliance-checker
     - theater-detection-audit, etc.

  4. ORCHESTRATION (21 agents)
     - hierarchical-coordinator, byzantine-coordinator
     - workflow-orchestrator, task-router, etc.

  5. FOUNDRY (15 agents)
     - agent-creator, skill-creator, prompt-engineer
     - template-generator, etc.

  6. OPERATIONS (12 agents)
     - cicd-engineer, monitoring-engineer, incident-responder
     - backup-manager, etc.

  7. PLATFORMS (8 agents)
     - platform-engineer, cloud-architect, kubernetes-expert
     - terraform-expert, etc.

  8. SECURITY (9 agents)
     - security-engineer, penetration-tester, crypto-expert
     - compliance-auditor, etc.

  9. SPECIALISTS (tech-specific, 50+ agents)
     - python-expert, javascript-expert, rust-expert
     - react-expert, vue-expert, etc.

 10. TOOLING (14 agents)
     - build-engineer, package-manager, dependency-analyzer
     - linter-configurator, etc.

FALLBACK AGENTS (if unsure):
  - coder (general coding)
  - researcher (research/analysis)
  - tester (testing)
  - reviewer (code review)

DOMAIN EXPERTISE CHECK:
  Before spawning agents, check if domain expertise exists:
  Location: .claude/expertise/{domain}.yaml

  If EXISTS:
    1. Run: /expertise-validate {domain}
    2. Load patterns and file locations
    3. Spawn agents with expertise context

  If NOT EXISTS:
    Agent will discover and create expertise during execution

AFTER SPAWNING:
  - Call TodoWrite() with 5-10 todos
  - Mark todos in_progress when starting
  - Mark completed immediately when done

PARALLEL SPAWN RULE:
  Spawn ALL independent agents in ONE message
  Do NOT spawn sequentially

LIMITATION WARNING:
  This hook CANNOT validate your agent type (hook constraint)
  Validation happens AFTER spawn via transcript parsing
  Please ensure agent type is from registry above

============================================================
EOF

# Always exit 0 (never block, can't validate params anyway)
exit 0
