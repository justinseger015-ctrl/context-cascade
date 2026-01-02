---
skill: gemini-extensions
description: Use Gemini’s extensions to integrate with Figma, Stripe, Postman, Shopify, and 60+ third-party services
tags: [gemini, extensions, figma, stripe, integrations, third-party]
version: 1.1.0
source: /skills/references/gemini-extensions.md
related-skills: [gemini-search, gemini-media, multi-model]
---

## Purpose
Bridge to third-party tools that Claude cannot access natively. This doc applies Prompt Architect discipline (clear intent, explicit constraints, optimized steps) and Skill Forge safeguards (structure-first, validation, confidence ceilings).

## When to Use
- Need design extraction (Figma), payment validation (Stripe), API testing (Postman), or ecommerce data (Shopify).
- Want unified access to additional observability/security extensions (Dynatrace, Elastic, Snyk, Harness).

## When Not to Use / Reroute
- Pure code execution without external integrations.
- Prompt-only improvements → `foundry/prompt-architect`.
- Skill authoring → `foundry/skill-forge`.

## Inputs (constraint extraction)
- **HARD**: Target extension, action, required credentials/tokens, permitted scopes.
- **SOFT**: Rate limits, sandbox vs production endpoints, output format (JSON/MD).
- **INFERRED**: Data retention requirements, PII handling rules — confirm before running.

## SOP
1. **Prepare**
   - Select extension and verify credentials; prefer sandbox/test modes.
   - Declare objective, scope, and output format in English.
2. **Execute**
   - Run the Gemini CLI call with the chosen extension and scoped query/action.
   - Capture response, pagination tokens, and any rate-limit headers.
3. **Validate & Hand Off**
   - Verify results against request intent; redact secrets and PII.
   - Summarize findings, cite endpoints/queries, and include next steps.

## Quality Gates
- Uses test keys/sandboxes unless production is explicitly approved.
- No secret leakage in outputs; paths and identifiers are redacted as needed.
- Confidence ceiling included; outputs in English only.

## Anti-Patterns
- Running in production by default.
- Issuing wide-scope queries without filters.
- Omitting audit trails (which extension, which action, when).
- Excluding confidence ceilings or file/endpoint references.

## Usage Examples
```bash
/gemini-extensions "Extract components from Figma frame 'Components/Buttons' and export design tokens"
/gemini-extensions "Run the 'User API' Postman collection against staging and summarize failures"
/gemini-extensions "Test Stripe payment intent creation with test card; report webhook events"
```

## Confidence
Confidence: 0.70 (ceiling: inference 0.70) — Follows Prompt Architect constraint clarity and Skill Forge validation; raise confidence after verifying extension credentials and sample calls.
