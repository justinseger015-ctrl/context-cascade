# Skill Format Migration Plan: Anthropic Official Compliance

## Executive Summary

**Current State**: 196 skills using custom format with x- extensions
**Target State**: Anthropic official skill format with progressive disclosure
**Risk Level**: HIGH - 50+ downstream components affected

---

## Key Findings

### Official Anthropic Format (from documentation)

```yaml
---
name: skill-name                    # REQUIRED, kebab-case, max 64 chars
description: What it does...        # REQUIRED, max 1024 chars, trigger keywords
allowed-tools: Read, Bash, Grep     # OPTIONAL, comma-separated
model: claude-opus-4-5-20251101     # OPTIONAL, specific model
---
```

**Critical Rules:**
1. Directory name MUST match `name` field exactly
2. Only 4 official fields allowed in frontmatter
3. Skills use progressive disclosure (SKILL.md + reference.md)
4. Keep SKILL.md under 500 lines

### Current Format Gaps

| Gap | Severity | Affected Skills | Impact |
|-----|----------|-----------------|--------|
| Directory-name mismatch | CRITICAL | ~40 skills (20%) | Breaks discovery |
| Non-official x- fields | HIGH | 196 skills (100%) | Not portable |
| VERIX in descriptions | MEDIUM | 196 skills (100%) | Parsing issues |
| Conditional naming (when-X-use-Y) | HIGH | ~40 skills | Breaks spec |
| Missing model field | LOW | 196 skills (100%) | Suboptimal |

### Downstream Components (50+ files)

**Tier 1 - Direct Parsers (MUST update):**
- scripts/migration/validate-all.js
- scripts/validate-all-skills.py
- skills/foundry/skill-forge/resources/scripts/validate_skill.py
- scripts/skill-packager.py
- scripts/migration/migrate-skills.js

**Tier 2 - Index/Registry (MUST update):**
- skills-packaged/SKILLS-INDEX.json
- agents/foundry/registry/registry.json (x-skills references)
- .claude-plugin/plugin.json

**Tier 3 - Execution Path (MUST verify):**
- playbooks/docs/SKILL-PLAYBOOK.md
- cognitive-architecture/tests/test_skill_playbook_optimization.py
- consolidated-ui/backend/app/utils/memory_mcp_client.py

**Tier 4 - Hook System (MUST verify):**
- hooks/12fa/ (permission/budget tracking)

---

## Migration Strategy

### Option A: Full Anthropic Compliance (RECOMMENDED)

**Approach**: Strip all custom metadata, use only official fields

**Pros:**
- Full compatibility with Anthropic ecosystem
- Skills work with official Claude Code marketplace
- Simpler, cleaner format

**Cons:**
- Lose x-version, x-category, x-tags metadata
- Need external system for categorization
- VERIX epistemic notation removed from descriptions

### Option B: Hybrid Compliance

**Approach**: Official fields + x- extensions (current state)

**Pros:**
- Keeps custom metadata
- Already implemented

**Cons:**
- Not officially portable
- May break with future Anthropic updates
- Non-standard

### Option C: Sidecar Metadata

**Approach**: Official SKILL.md + separate metadata.json

**Pros:**
- Full Anthropic compliance in SKILL.md
- Preserves all custom metadata
- Best of both worlds

**Cons:**
- More files to manage
- Need to update all parsers for dual-file pattern

---

## Recommended Plan: Option C (Sidecar Metadata)

### Phase 1: Directory Normalization (Week 1)

**Task 1.1**: Rename conditional directories
```
BEFORE: when-debugging-code-use-debugging-assistant/
AFTER:  debugging-assistant/

BEFORE: when-creating-pipelines-use-pipeline-creator/
AFTER:  pipeline-creator/
```

**Task 1.2**: Ensure name field matches directory
- Audit all 196 skills
- Fix name field to match directory (kebab-case)
- Update all references

### Phase 2: Frontmatter Standardization (Week 2)

**Task 2.1**: Create metadata.json sidecar files
```
skill-name/
  SKILL.md           # Official format only
  metadata.json      # Custom extensions
  reference.md       # Supporting docs (if needed)
```

**Task 2.2**: metadata.json schema
```json
{
  "version": "1.0.0",
  "category": "delivery",
  "tags": ["coding", "debugging"],
  "author": "ruv",
  "verix": {
    "description": "[assert|neutral] ... [ground:...] [conf:0.95]"
  },
  "mcp_servers": {
    "required": ["memory-mcp"],
    "optional": ["sequential-thinking"]
  },
  "triggers": ["debug", "fix bug", "troubleshoot"]
}
```

**Task 2.3**: Update SKILL.md frontmatter
- Remove x-version, x-category, x-tags, x-author, x-mcp_servers
- Keep only: name, description, allowed-tools, model
- Move VERIX notation from description to metadata.json

### Phase 3: Parser Updates (Week 3)

**Task 3.1**: Update validate-all.js
- Add metadata.json parsing support
- Validate official fields separately
- Report on sidecar compliance

**Task 3.2**: Update validate_skill.py
- Dual-file validation
- Cross-reference checks

**Task 3.3**: Update skill-packager.py
- Include metadata.json in .skill.zip
- Update manifest generation

**Task 3.4**: Update migrate-skills.js
- Transform existing x- fields to metadata.json
- Backup original files

### Phase 4: Index Regeneration (Week 4)

**Task 4.1**: Regenerate SKILLS-INDEX.json
- Update with new skill names
- Include metadata.json references

**Task 4.2**: Update registry.json
- Fix all x-skills references to new names
- Validate agent-skill mappings

**Task 4.3**: Update plugin.json
- Verify skills path still valid
- Update any hardcoded references

### Phase 5: Execution Path Verification (Week 5)

**Task 5.1**: Update playbook skill references
- Search/replace old skill names
- Verify execution chains

**Task 5.2**: Update test harnesses
- Fix SKILL_CATEGORIES dictionaries
- Update test fixtures

**Task 5.3**: Verify Memory MCP integration
- Ensure tagging protocol works with new names
- Test skill execution tracking

### Phase 6: Hook System Update (Week 6)

**Task 6.1**: Update permission hooks
- Verify skill name matching
- Test budget enforcement

**Task 6.2**: End-to-end testing
- Full workflow validation
- Performance benchmarking

---

## Premortem Analysis

### What Could Go Wrong?

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Skill name collisions** | MEDIUM | HIGH | Pre-audit all names, reserve namespace |
| **Broken playbook chains** | HIGH | HIGH | Comprehensive search/replace, testing |
| **Registry desync** | MEDIUM | HIGH | Automated validation script |
| **Memory MCP data loss** | LOW | CRITICAL | Backup before migration |
| **Performance regression** | LOW | MEDIUM | Benchmark before/after |
| **Incomplete parser updates** | MEDIUM | HIGH | Test suite for each parser |
| **VERIX notation loss** | HIGH | MEDIUM | Preserve in metadata.json |
| **Hook enforcement gaps** | MEDIUM | HIGH | E2E permission testing |

### Failure Modes

**Failure Mode 1: Silent Skill Discovery Failure**
- Symptom: Skills not matched to user requests
- Cause: Description keywords changed during migration
- Detection: Compare before/after skill matching rates
- Recovery: Restore from backup, fix descriptions

**Failure Mode 2: Cascading Reference Breaks**
- Symptom: Playbooks fail, agents can't find skills
- Cause: Renamed skills not updated everywhere
- Detection: Automated reference validation
- Recovery: Script to find/fix dangling references

**Failure Mode 3: Validation False Positives**
- Symptom: Valid skills marked invalid
- Cause: Parsers not updated for new format
- Detection: Manual spot checks
- Recovery: Update parser logic

**Failure Mode 4: ZIP Package Corruption**
- Symptom: skill-packager.py produces invalid .skill.zip
- Cause: metadata.json not included correctly
- Detection: Unzip and verify contents
- Recovery: Fix packager, regenerate all zips

---

## Rollback Plan

### Checkpoint Strategy

1. **Before Phase 1**: Full backup of skills/ directory
2. **Before Phase 3**: Backup all parser scripts
3. **Before Phase 4**: Backup index files
4. **Before Phase 6**: Full system snapshot

### Rollback Commands

```bash
# Restore skills directory
git checkout HEAD~1 -- skills/

# Restore all changes
git reset --hard HEAD~N

# Selective restore
git restore --source=backup-branch -- path/to/file
```

---

## Success Criteria

1. All 196 skills pass official format validation
2. Directory names match `name` fields (100%)
3. No x- fields in SKILL.md frontmatter
4. All metadata preserved in metadata.json sidecars
5. All playbook chains execute successfully
6. All agents can invoke their mapped skills
7. Memory MCP skill tracking functional
8. Hook enforcement working
9. SKILLS-INDEX.json accurate
10. skill-packager.py produces valid .skill.zip files

---

## Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Directory Normalization | 3-4 hours | None |
| Phase 2: Frontmatter Standardization | 6-8 hours | Phase 1 |
| Phase 3: Parser Updates | 4-6 hours | Phase 2 |
| Phase 4: Index Regeneration | 2-3 hours | Phase 3 |
| Phase 5: Execution Path Verification | 4-6 hours | Phase 4 |
| Phase 6: Hook System Update | 2-3 hours | Phase 5 |
| **Total** | **21-30 hours** | Sequential |

---

## Decision Required

Before proceeding, confirm:

1. **Option A, B, or C?** (Recommended: Option C - Sidecar Metadata)
2. **Preserve VERIX notation?** (Recommended: Yes, in metadata.json)
3. **Full rename or alias?** (Recommended: Full rename with reference updates)
4. **Phased or big-bang?** (Recommended: Phased with checkpoints)

---

*Generated: 2025-12-30*
*Status: AWAITING APPROVAL*
