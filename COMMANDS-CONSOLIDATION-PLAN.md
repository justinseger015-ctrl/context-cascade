# Context Cascade Commands Consolidation Plan

**Created:** 2026-01-03
**Status:** PLANNING
**Goal:** Reduce context consumption from ~710 command files to ~50 core commands + 1 routing manifest

---

## Current State Analysis

### Token Consumption (Observed)

| Component | File Count | Avg Tokens | Total Tokens |
|-----------|-----------|------------|--------------|
| Commands (top-level) | 260 | ~500 | ~130k |
| Skills (commands/skills/) | 233 | ~700 | ~163k |
| Agents (commands/agents/) | 217 | ~3k | ~651k |
| **TOTAL** | **710** | - | **~944k tokens** |

### Identified Problems

#### Problem 1: Exact Duplicates (100+ files)

These pairs are IDENTICAL content with different names:

| Short Name | Long Duplicate | Action |
|------------|----------------|--------|
| `build-feature.md` | `delivery-essential-commands-build-feature.md` | DELETE long |
| `fix-bug.md` | `delivery-essential-commands-fix-bug.md` | DELETE long |
| `debug.md` | `delivery-sparc-debug.md` | DELETE long |
| `review-pr.md` | `delivery-essential-commands-review-pr.md` | DELETE long |
| `quick-check.md` | `delivery-essential-commands-quick-check.md` | DELETE long |
| `smoke-test.md` | `delivery-essential-commands-smoke-test.md` | DELETE long |
| `e2e-test.md` | `delivery-essential-commands-e2e-test.md` | DELETE long |
| `sparc.md` | `delivery-sparc-sparc.md` | DELETE long |
| `tdd.md` | `delivery-sparc-tdd.md` | DELETE long |
| `tester.md` | `delivery-sparc-tester.md` | DELETE long |
| `reviewer.md` | `delivery-sparc-reviewer.md` | DELETE long |
| `documenter.md` | `delivery-sparc-documenter.md` | DELETE long |
| `researcher.md` | `delivery-sparc-researcher.md` | DELETE long |
| `analyzer.md` | `delivery-sparc-analyzer.md` | DELETE long |
| `architect.md` | `delivery-sparc-architect.md` | DELETE long |
| `devops.md` | `delivery-sparc-devops.md` | DELETE long |
| `deployment.md` | `delivery-workflows-deployment.md` | DELETE long |
| `development.md` | `delivery-workflows-development.md` | DELETE long |
| `testing.md` | `delivery-workflows-testing.md` | DELETE long |

#### Problem 2: When-X-Use-Y Routing Wrappers (60 files)

These should be YAML index entries, not full skill files:

```
skill-delivery-when-fixing-complex-bug-use-smart-bug-fix.md
skill-delivery-when-debugging-code-use-debugging-assistant.md
skill-delivery-when-developing-complete-feature-use-feature-dev-complete.md
... (60 total)
```

**Each wrapper = ~700 tokens. Total = ~42k tokens wasted.**

Should become 60 lines in a single YAML file:

```yaml
# Instead of 60 files, 1 file:
routing:
  "fixing complex bug": smart-bug-fix
  "debugging code": debugging-assistant
  "developing complete feature": feature-dev-complete
```

#### Problem 3: Agents/Skills as Slash Commands (450 files)

Agents and skills are registered as slash commands but should load ON-DEMAND:

```
commands/skills/skill-*.md (233 files)
commands/agents/agent-*.md (217 files)
```

These should NOT be registered as commands. They should:
1. Live in the plugin directory (already do)
2. Be discovered via SKILL-INDEX.md and AGENT-REGISTRY.md (already exist)
3. Load only when invoked via `Task()` or `Skill()`

#### Problem 4: Double-Prefix Naming (30+ files)

Redundant prefixes inflate command names:

| Current Name | Consolidated Name |
|--------------|-------------------|
| `orchestration-hive-mind-hive-mind-consensus.md` | `hive-mind-consensus.md` |
| `orchestration-hive-mind-hive-mind-sessions.md` | `hive-mind-sessions.md` |
| `operations-memory-memory-search.md` | `memory-search.md` |
| `operations-memory-memory-persist.md` | `memory-persist.md` |
| `orchestration-swarm-swarm-spawn.md` | `swarm-spawn.md` |
| `orchestration-swarm-swarm-status.md` | `swarm-status.md` |

---

## Target Architecture

### Tier 1: Core Commands (~30 files, ~15k tokens)

User-facing slash commands that remain as individual files:

```
~/.claude/commands/
  sparc.md
  build-feature.md
  fix-bug.md
  debug.md
  review-pr.md
  quick-check.md
  tdd.md
  deploy.md
  research.md
  ... (~30 total)
```

### Tier 2: Routing Manifest (1 file, ~3k tokens)

Single YAML file for all intent-to-skill routing:

```yaml
# ~/.claude/commands/COMMANDS_INDEX.yaml
version: "1.0"
generated: "2026-01-03"

# Core commands - these exist as individual .md files
core_commands:
  - sparc
  - build-feature
  - fix-bug
  - debug
  - review-pr
  - quick-check
  - tdd
  - deploy
  - research

# Intent routing - when user says X, invoke skill Y
intent_routing:
  bug_fixing:
    triggers: ["fix bug", "debug", "broken", "error", "not working"]
    skill: smart-bug-fix
    agents: [debugger, coder, tester]

  feature_development:
    triggers: ["build feature", "implement", "add functionality"]
    skill: feature-dev-complete
    agents: [planner, coder, tester, reviewer]

  code_review:
    triggers: ["review code", "PR review", "pull request"]
    skill: code-review-assistant
    agents: [reviewer, security-auditor]

  research:
    triggers: ["research", "investigate", "explore"]
    skill: deep-research-orchestrator
    agents: [researcher, synthesizer]

# Category shortcuts - expand to skill lists
categories:
  delivery: [feature-dev-complete, smart-bug-fix, api-docs, testing-framework]
  quality: [code-review-assistant, functionality-audit, theater-detection]
  research: [deep-research-orchestrator, literature-synthesis, baseline-replication]
  operations: [production-readiness, cicd-intelligent-recovery, cloud-platforms]
```

### Tier 3: Skills (On-Demand, Plugin Directory)

Skills remain in plugin, loaded only when selected:

```
context-cascade/skills/
  delivery/
    feature-dev-complete/skill.md
    smart-bug-fix/skill.md
  quality/
    code-review-assistant/skill.md
  ...
```

Discovered via `discovery/SKILL-INDEX.md` (already exists).

### Tier 4: Agents (On-Demand, Plugin Directory)

Agents remain in plugin, loaded only when skill invokes:

```
context-cascade/agents/
  delivery/*.md
  quality/*.md
  ...
```

Discovered via `discovery/AGENT-REGISTRY.md` (already exists).

---

## Implementation Phases

### Phase 1: Delete Exact Duplicates

**Script:** `scripts/consolidation/phase1-delete-duplicates.sh`

```bash
#!/bin/bash
COMMANDS_DIR="$HOME/.claude/commands"

# Exact duplicates to delete (long-prefix versions)
DUPLICATES=(
  "delivery-essential-commands-build-feature.md"
  "delivery-essential-commands-fix-bug.md"
  "delivery-essential-commands-review-pr.md"
  "delivery-essential-commands-quick-check.md"
  "delivery-essential-commands-smoke-test.md"
  "delivery-essential-commands-e2e-test.md"
  "delivery-essential-commands-deploy-check.md"
  "delivery-essential-commands-integration-test.md"
  "delivery-essential-commands-load-test.md"
  "delivery-essential-commands-regression-test.md"
  "delivery-sparc-sparc.md"
  "delivery-sparc-debug.md"
  "delivery-sparc-debugger.md"
  "delivery-sparc-tdd.md"
  "delivery-sparc-tester.md"
  "delivery-sparc-reviewer.md"
  "delivery-sparc-documenter.md"
  "delivery-sparc-researcher.md"
  "delivery-sparc-analyzer.md"
  "delivery-sparc-architect.md"
  "delivery-sparc-devops.md"
  "delivery-sparc-coder.md"
  "delivery-sparc-code.md"
  "delivery-sparc-optimizer.md"
  "delivery-workflows-deployment.md"
  "delivery-workflows-development.md"
  "delivery-workflows-testing.md"
)

for file in "${DUPLICATES[@]}"; do
  if [[ -f "$COMMANDS_DIR/$file" ]]; then
    echo "Deleting duplicate: $file"
    rm "$COMMANDS_DIR/$file"
  fi
done

echo "Phase 1 complete: Deleted ${#DUPLICATES[@]} duplicate files"
```

**Impact:** ~35 files deleted, ~17k tokens saved

### Phase 2: Convert When-X-Use-Y to Index

**Script:** `scripts/consolidation/phase2-convert-routing.sh`

1. Parse all `when-*-use-*.md` files
2. Extract trigger phrases and target skills
3. Generate `COMMANDS_INDEX.yaml`
4. Delete the 60 wrapper files

**Impact:** 60 files -> 1 file, ~40k tokens saved

### Phase 3: Remove Skills/Agents from Commands

**Script:** `scripts/consolidation/phase3-remove-subcommands.sh`

```bash
#!/bin/bash
# Remove skills and agents directories from commands
rm -rf "$HOME/.claude/commands/skills"
rm -rf "$HOME/.claude/commands/agents"
```

**Impact:** 450 files deleted, ~650k tokens saved

### Phase 4: Flatten Double-Prefix Names

**Script:** `scripts/consolidation/phase4-flatten-names.sh`

Rename remaining commands to remove redundant prefixes.

**Impact:** Cleaner naming, minor token savings

---

## Estimated Impact

| Phase | Files Removed | Tokens Saved |
|-------|---------------|--------------|
| Phase 1: Duplicates | ~35 | ~17k |
| Phase 2: Routing Wrappers | ~60 | ~40k |
| Phase 3: Skills/Agents | ~450 | ~650k |
| Phase 4: Naming Cleanup | 0 | ~5k |
| **TOTAL** | **~545** | **~712k tokens** |

### Before vs After

| Metric | Before | After | Reduction |
|--------|--------|-------|-----------|
| Total Files | 710 | ~165 | 77% |
| Context Tokens | ~944k | ~232k | 75% |
| Slash Commands | 710 | ~30 | 96% |

---

## Rollback Plan

Before execution, backup current state:

```bash
# Create timestamped backup
BACKUP_DIR="$HOME/.claude/commands-backup-$(date +%Y%m%d-%H%M%S)"
cp -r "$HOME/.claude/commands" "$BACKUP_DIR"
```

---

## Validation Checklist

- [ ] Core commands still invocable (sparc, build-feature, etc.)
- [ ] Skill routing works via COMMANDS_INDEX.yaml
- [ ] Agent invocation works via Task()
- [ ] No "command not found" errors
- [ ] Context consumption reduced (check /mcp output)

---

## Next Steps

1. Review this plan
2. Run Phase 1 (safest, clear duplicates)
3. Test thoroughly
4. Proceed to Phase 2-4

**Recommendation:** Start with Phase 1 only, validate, then continue.
