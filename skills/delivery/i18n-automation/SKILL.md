---
name: i18n-automation
description: Automate internationalization and localization with safe key management, locale plumbing, and validated translations.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
model: sonnet
x-version: 3.2.0
x-category: delivery
x-vcl-compliance: v3.1.1
x-cognitive-frames:
  - HON
  - MOR
  - COM
  - CLS
  - EVD
  - ASP
  - SPC
---


## STANDARD OPERATING PROCEDURE

### Purpose
Enable reliable multi-lingual delivery by externalizing strings, wiring locale infrastructure, and validating translations.

### Trigger Conditions
- **Positive:** adding new locales, fixing missing translations, setting up i18n libraries, RTL enablement, pluralization issues.
- **Negative:** content-only rewrites without code changes (route to `documentation`).

### Guardrails
- **Structure-first:** maintain `examples/`, `tests/`, `resources/`, `references/`.
- **Constraint extraction:** HARD (locales, privacy/PII rules, release windows), SOFT (copy tone), INFERRED (fallback order, locale negotiation) — confirm inferred.
- **Confidence ceilings:** `{inference/report:0.70, research:0.85, observation/definition:0.95}` for locale behavior and translation claims.
- **Safety:** never hardcode secrets/PII in translations; keep placeholders intact.
- **Validation:** syntax-check translation files; test RTL, plural rules, and formatting boundaries.

### Execution Phases
1. **Assessment & Plan**
   - Identify target locales, libraries, file formats, and delivery constraints.
   - Inventory untranslated strings; design key namespaces.
2. **Implementation**
   - Externalize strings; add interpolation context; implement locale detection + fallback.
   - Wire date/number formatting and RTL toggles; store snippets in `examples/`.
3. **Translation Workflow**
   - Prepare source files; protect placeholders; integrate vendor pipelines if applicable.
   - Record guidance and glossaries in `references/`.
4. **Validation**
   - Run lint/schema checks on locale files; test pluralization + ICU messages.
   - Exercise UI in each locale (including RTL); capture artifacts in `resources/`.
5. **Release & Monitor**
   - Add regression tests in `tests/`; document rollout/rollback.
   - Summarize coverage, risks, and **Confidence: X.XX (ceiling: TYPE Y.YY)**.

### Output Format
- Constraints (HARD/SOFT/INFERRED) with confirmation status.
- Key namespaces, locale settings, and validation results.
- Deployment/rollback notes and evidence references.
- Confidence statement with ceiling.

### Validation Checklist
- [ ] Strings externalized; keys namespaced; placeholders preserved.
- [ ] Locale detection + fallback verified; RTL support tested when relevant.
- [ ] Pluralization and formatting checked with boundary values.
- [ ] Lint/schema checks run; tests captured in `tests/`.
- [ ] Sources and advisories stored in `references/`; artifacts in `resources/`.

### MCP / Memory Tags
- Namespace: `skills/delivery/i18n-automation/{project}/{locale}`
- Tags: `WHO=i18n-automation-{session}`, `WHY=skill-execution`, `WHAT=localization`

Confidence: 0.70 (ceiling: inference 0.70) - SOP integrates skill-forge structure-first and prompt-architect constraint/ceiling discipline.
