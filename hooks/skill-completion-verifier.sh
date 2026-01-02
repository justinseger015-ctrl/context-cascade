#!/bin/bash
# skill-completion-verifier.sh
# PURPOSE: Verify skill execution follows CASCADE pattern
# HOOK TYPE: PostToolUse (runs after Write/Edit)
# UPDATED: 2026-01-02 - Added cascade discovery references
#
# This hook verifies the CASCADE execution pattern:
#   Skill (SOP) -> Task (spawn agent) -> TodoWrite (track)

cat << 'EOF'

!! CASCADE COMPLETION CHECK !!
============================================================

Post-execution verification for CASCADE architecture:

CHECKLIST:
  [ ] Skill SOP was loaded and followed
  [ ] Agent(s) spawned via Task() from registry
  [ ] TodoWrite() called with progress items
  [ ] Work delegated to agents (not done directly)

IF SKILL WAS INVOKED:
  - Agents MUST be spawned via Task()
  - Agent types from: discovery/AGENT-REGISTRY.md
  - Pattern: Task("desc", "prompt", "agent-type")

IF NO SKILL ACTIVE:
  - Consider: Does this task need a skill?
  - Check: discovery/SKILL-INDEX.md for matches
  - Route: Use 5-phase workflow

GOLDEN RULE: 1 MESSAGE = ALL PARALLEL Task() calls

============================================================
EOF

exit 0
