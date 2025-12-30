# Finance Specialists

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



**Category**: specialists/finance
**Agent Count**: 3
**Added**: 2025-11-26

This directory contains specialized agents for quantitative finance, risk management, and market data integration.

## Available Agents

| Agent | File | Specialization |
|-------|------|----------------|
| Quant Analyst | `quant-analyst.md` | Quantitative trading, signal calibration, backtesting |
| Risk Manager | `risk-manager.md` | Risk quantification, VaR, compliance, kill switch |
| Market Data Specialist | `market-data-specialist.md` | Real-time data feeds, Alpaca API, WebSocket streaming |

## Use Cases

### ISS-017: AI/Compliance Engines Return Fake Values

Use **quant-analyst** and **risk-manager** together:

```
Task("Quant Analyst", "Audit AI signal generators for proper calibration. Calculate Brier scores and generate calibration curves for all prediction models.", "quant-analyst")

Task("Risk Manager", "Validate risk engine calculations are real. Audit VaR, drawdown, and P(ruin) calculations against expected values.", "risk-manager")
```

### ISS-020: Real-Time Data Feeds Are Mock/Placeholder

Use **market-data-specialist**:

```
Task("Market Data Specialist", "Replace mock data generators with real Alpaca API integration. Implement WebSocket streaming for live quotes and trades.", "market-data-specialist")
```

## Integration Points

These agents integrate with existing agents:
- **soc-compliance-auditor**: Regulatory compliance
- **compliance-validation-agent**: Data privacy
- **kafka-streaming-agent**: Data streaming architecture
- **model-monitoring-agent**: Production monitoring
- **model-evaluation-agent**: Model validation

## Source Attribution

Based on agents from:
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- [alpacahq/alpaca-mcp-server](https://github.com/alpacahq/alpaca-mcp-server)



---

## AGENT-SPECIFIC IMPROVEMENTS

### Role Clarity
- **Frontend Developer**: Build production-ready React/Vue components with accessibility and performance
- **Backend Developer**: Implement scalable APIs with security, validation, and comprehensive testing
- **SPARC Architect**: Design system architecture following SPARC methodology (Specification, Pseudocode, Architecture, Refinement, Completion)
- **Business Analyst**: Translate stakeholder requirements into technical specifications and user stories
- **Finance Specialist**: Analyze market data, manage risk, and optimize trading strategies

### Success Criteria
- [assert|neutral] *Tests Passing**: 100% of tests must pass before completion (unit, integration, E2E) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Code Reviewed**: All code changes must pass peer review and automated quality checks [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Documentation Complete**: All public APIs, components, and modules must have comprehensive documentation [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Security Validated**: Security scanning (SAST, DAST) must pass with no critical vulnerabilities [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Performance Benchmarked**: Performance metrics must meet or exceed defined SLAs [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases
- **Legacy Code**: Handle outdated dependencies, deprecated APIs, and undocumented behavior carefully
- **Version Conflicts**: Resolve dependency version mismatches using lock files and compatibility matrices
- **Unclear Requirements**: Request clarification from stakeholders before implementation begins
- **Integration Failures**: Have rollback strategies and circuit breakers for third-party service failures
- **Data Migration**: Validate data integrity before and after schema changes

### Guardrails
- [assert|emphatic] NEVER: ship without tests**: All code changes require >=80% test coverage [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: skip code review**: All PRs require approval from at least one team member [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: commit secrets**: Use environment variables and secret managers (never hardcode credentials) [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: ignore linter warnings**: Fix all ESLint/Prettier/TypeScript errors before committing [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: break backward compatibility**: Use deprecation notices and versioning for breaking changes [ground:policy] [conf:0.98] [state:confirmed]

### Failure Recovery
- **Document blockers**: Log all impediments in issue tracker with severity and impact assessment
- **Request clarification**: Escalate to stakeholders when requirements are ambiguous or contradictory
- **Escalate technical debt**: Flag architectural issues that require senior engineer intervention
- **Rollback strategy**: Maintain ability to revert changes within 5 minutes for production issues
- **Post-mortem analysis**: Conduct blameless retrospectives after incidents to prevent recurrence

### Evidence-Based Verification
- **Verify via tests**: Run test suite (npm test, pytest, cargo test) and confirm 100% pass rate
- **Verify via linter**: Run linter (npm run lint, flake8, clippy) and confirm zero errors
- **Verify via type checker**: Run type checker (tsc --noEmit, mypy, cargo check) and confirm zero errors
- **Verify via build**: Run production build (npm run build, cargo build --release) and confirm success
- **Verify via deployment**: Deploy to staging environment and run smoke tests before production

---

Adapted and enhanced for the ruv-sparc-three-loop-system plugin format.


---
*Promise: `<promise>README_VERIX_COMPLIANT</promise>`*
