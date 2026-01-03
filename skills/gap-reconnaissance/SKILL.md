# Gap Reconnaissance Skill

## Metadata
- **Name**: gap-reconnaissance
- **Version**: 1.0.0
- **Category**: research
- **Triggers**: ["gap analysis", "find solution", "reconnaissance", "research github", "what framework", "what library"]
- **Priority**: HIGH

## Purpose

Systematic process for identifying gaps in a project, researching solutions, extracting reusable patterns, and creating integration guides - then cleaning up to minimize storage.

## The 7-Phase Process

```
+-----------------------------------------------------------------------+
|                    GAP RECONNAISSANCE WORKFLOW                         |
+-----------------------------------------------------------------------+
|                                                                        |
|  PHASE 1: GAP IDENTIFICATION                                           |
|  +------------------------------------------------------------------+  |
|  | - Analyze project architecture docs                              |  |
|  | - Identify missing components (100% gaps)                        |  |
|  | - Determine criticality (P0/P1/P2)                               |  |
|  | - Document gap with clear requirements                           |  |
|  +------------------------------------------------------------------+  |
|                              |                                         |
|                              v                                         |
|  PHASE 2: TECHNICAL CRITERIA                                           |
|  +------------------------------------------------------------------+  |
|  | - Define minimum viable solution                                 |  |
|  | - Check tech stack compatibility                                 |  |
|  |   - Language match (Python/Rust/TypeScript)                      |  |
|  |   - Deployment match (Docker/K8s/serverless)                     |  |
|  |   - Integration points (APIs, data formats)                      |  |
|  | - Estimate integration effort                                    |  |
|  | - Define success metrics                                         |  |
|  +------------------------------------------------------------------+  |
|                              |                                         |
|                              v                                         |
|  PHASE 3: GITHUB RESEARCH                                              |
|  +------------------------------------------------------------------+  |
|  | - WebSearch for "[gap] framework 2025 github code"               |  |
|  | - WebSearch for "[gap] paper 2025 arxiv implementation"          |  |
|  | - Filter by:                                                     |  |
|  |   - Stars (>1k preferred)                                        |  |
|  |   - Last commit (<6 months)                                      |  |
|  |   - License (Apache/MIT)                                         |  |
|  |   - Production vs research                                       |  |
|  | - Create candidate shortlist (3-5 repos)                         |  |
|  +------------------------------------------------------------------+  |
|                              |                                         |
|                              v                                         |
|  PHASE 4: RECONNAISSANCE DOWNLOAD                                      |
|  +------------------------------------------------------------------+  |
|  | - git clone --depth 1 [repo] ~/reconnaissance/[name]             |  |
|  | - Check size: du -sh                                             |  |
|  | - Explore structure: ls -la, find *.py                           |  |
|  | - Read README.md for architecture                                |  |
|  | - Identify core algorithm locations                              |  |
|  +------------------------------------------------------------------+  |
|                              |                                         |
|                              v                                         |
|  PHASE 5: DEEP DIVE EXTRACTION                                         |
|  +------------------------------------------------------------------+  |
|  | - Read core algorithm files                                      |  |
|  | - Understand patterns and interfaces                             |  |
|  | - Map to project integration points                              |  |
|  | - Identify what to KEEP vs DELETE                                |  |
|  | - Extract ONLY essential code                                    |  |
|  +------------------------------------------------------------------+  |
|                              |                                         |
|                              v                                         |
|  PHASE 6: GUIDE CREATION                                               |
|  +------------------------------------------------------------------+  |
|  | - Create MANIFEST.md with:                                       |  |
|  |   - Executive summary                                            |  |
|  |   - Algorithm inventory                                          |  |
|  |   - Integration architecture                                     |  |
|  |   - Effort estimates                                             |  |
|  |   - What to use / What to skip                                   |  |
|  | - Create comparison charts if multiple sources                   |  |
|  | - Update project architecture docs                               |  |
|  +------------------------------------------------------------------+  |
|                              |                                         |
|                              v                                         |
|  PHASE 7: CLEANUP                                                      |
|  +------------------------------------------------------------------+  |
|  | - Delete .git/ (largest space consumer)                          |  |
|  | - Delete docs/, examples/, tests/ (reference README)             |  |
|  | - Delete algorithms NOT needed (keep only essentials)            |  |
|  | - Target: <200KB per repo                                        |  |
|  | - Verify: find . -name "*.py" shows only essentials              |  |
|  +------------------------------------------------------------------+  |
|                                                                        |
+-----------------------------------------------------------------------+
```

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `gap_description` | YES | What capability is missing |
| `project_path` | YES | Path to project with gap |
| `tech_stack` | YES | Languages, frameworks, deployment |
| `priority` | NO | P0/P1/P2 (default: P1) |
| `max_repos` | NO | Max repos to analyze (default: 3) |

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| `MANIFEST.md` | `reconnaissance/[repo]/` | Integration guide |
| `*-COMPARISON-CHART.md` | `reconnaissance/` | Multi-source comparison |
| `*-RESEARCH-*.md` | `reconnaissance/` | Paper analysis |
| Cleaned repo | `reconnaissance/[repo]/` | Essential code only |
| Architecture update | Project docs | Gap now documented |

## Tech Stack Compatibility Checklist

```yaml
languages:
  python:
    compatible: [Python, Cython]
    maybe: [Rust via PyO3, C via ctypes]
    incompatible: [Java, Go, pure C++]

  rust:
    compatible: [Rust]
    maybe: [C via FFI, Python via PyO3]
    incompatible: [Python-only, JavaScript]

  typescript:
    compatible: [TypeScript, JavaScript]
    maybe: [Rust via WASM]
    incompatible: [Python, C++]

deployment:
  docker_compose:
    compatible: [Docker, docker-compose]
    maybe: [Kubernetes with adaptation]
    incompatible: [serverless, Lambda-only]

  kubernetes:
    compatible: [Helm, K8s manifests]
    maybe: [Docker with adaptation]
    incompatible: [Docker Compose only]

communication:
  rest_api:
    compatible: [REST, HTTP, gRPC]
    maybe: [GraphQL, WebSocket]
    incompatible: [proprietary protocols]
```

## Pre-Mortem Checklist

Before committing to a solution, verify:

```markdown
- [ ] Does project ACTUALLY need this? (check existing code first)
- [ ] Does solution match tech stack?
- [ ] Is solution production-ready or research-only?
- [ ] What's the minimum viable extraction?
- [ ] What can we DELETE after extraction?
- [ ] Are there simpler alternatives?
```

## Example Invocation

```
User: "fog-compute needs federated learning for training and inference"

Claude executes:
1. GAP: FL training + inference missing (100% gap per architecture doc)
2. CRITERIA: Python, Docker, integrate with NSGA-II scheduler
3. RESEARCH: WebSearch "federated learning framework 2025 github"
4. DOWNLOAD: Clone FATE-LLM, PFLlib
5. EXTRACT: Keep FedKSeed, InferDPT, SCAFFOLD, FedDBE
6. GUIDE: Create MANIFEST.md, comparison chart
7. CLEANUP: 9.5MB -> 126KB, 197MB -> 124KB
```

## Success Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Repo size reduction | >90% | Keep only essentials |
| Integration effort documented | <1 week | Clear roadmap |
| Tech stack match | 100% | No incompatible solutions |
| Cleanup verified | <200KB/repo | Storage efficiency |

## Anti-Patterns

| Anti-Pattern | Why Bad | Instead |
|--------------|---------|---------|
| Clone entire repo and keep | Wastes storage, clutters | Extract only what's needed |
| Skip pre-mortem | Miss tech stack issues | Always verify compatibility |
| No MANIFEST.md | Knowledge lost | Document integration path |
| Keep .git folder | 80%+ of size | Always delete .git |
| Research without downloading | Superficial understanding | Clone and read code |

## Related Skills

- `literature-synthesis` - For paper-heavy research
- `codebase-archaeology` - For understanding existing code
- `integration-architect` - For designing integration

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-03 | Initial extraction from FL reconnaissance session |
