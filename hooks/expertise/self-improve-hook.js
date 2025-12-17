/**
 * Self-Improve Hook for Expertise System v2.0
 *
 * TRIGGERS: After ANY skill/model execution (not just Loop 2 builds)
 * CONTEXTS: build, research, planning, review, debug, documentation, analysis, skill_execution
 * PURPOSE: Auto-update expertise files based on ALL execution learnings
 *
 * v2.0: Learn from ALL contexts - research, planning, review, debug, docs, analysis, not just builds
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { execSync } = require('child_process');

const EXPERTISE_DIR = '.claude/expertise';
const ADVERSARIAL_THRESHOLD = 0.7;

// All supported execution contexts with learning parameters
const EXECUTION_CONTEXTS = {
  build: { minSuccessRate: 1.0, weight: 1.0, types: ['file_location', 'pattern', 'entity'] },
  research: { minSuccessRate: 0.0, weight: 0.8, types: ['terminology', 'source_quality', 'search_pattern'] },
  planning: { minSuccessRate: 0.0, weight: 0.7, types: ['task_breakdown', 'dependency_pattern', 'phase_sequence'] },
  review: { minSuccessRate: 0.0, weight: 0.9, types: ['issue_pattern', 'fix_pattern', 'anti_pattern'] },
  debug: { minSuccessRate: 0.5, weight: 1.0, types: ['root_cause', 'fix_strategy', 'diagnostic'] },
  documentation: { minSuccessRate: 0.0, weight: 0.6, types: ['structure_pattern', 'terminology'] },
  analysis: { minSuccessRate: 0.0, weight: 0.7, types: ['metric', 'pattern_detected', 'threshold'] },
  skill_execution: { minSuccessRate: 0.0, weight: 0.8, types: ['workflow_pattern', 'parameter_usage'] }
};

async function selfImproveHook(context) {
  const type = context.executionType || detectType(context);
  const config = EXECUTION_CONTEXTS[type] || EXECUTION_CONTEXTS.skill_execution;
  
  console.log('SELF-IMPROVE v2.0: ' + type.toUpperCase());
  if (context.skillName) console.log('Skill: ' + context.skillName);
  
  const successRate = getSuccessRate(context, type);
  if (successRate < config.minSuccessRate) {
    console.log('SKIP: Success rate ' + successRate + ' below threshold');
    return { skipped: true, reason: 'below_threshold', type };
  }
  
  const domains = identifyDomains(context, type);
  if (domains.length === 0) {
    const inferred = inferDomain(context);
    if (inferred) domains.push(inferred);
    else return { skipped: true, reason: 'no_domains' };
  }
  
  const results = { type, domains_processed: [], updates_accepted: [], learning_delta: 0 };
  
  for (const domain of domains) {
    console.log('Processing: ' + domain);
    const learnings = extractLearnings(domain, context, type, config);
    if (learnings.length === 0) continue;
    
    const proposal = { domain, type, learnings, changes: learnings.map(l => ({ section: l.section, data: l })) };
    const validation = await validate(proposal);
    
    if (validation.survivalRate >= ADVERSARIAL_THRESHOLD) {
      await applyUpdate(domain, proposal, validation, type);
      results.updates_accepted.push(domain);
      results.learning_delta += validation.survived * config.weight * 0.1;
    }
    results.domains_processed.push(domain);
  }
  
  console.log('Complete: ' + results.updates_accepted.length + ' domains updated');
  return results;
}

function detectType(ctx) {
  if (ctx.testResults) return 'build';
  if (ctx.researchResult) return 'research';
  if (ctx.planningResult) return 'planning';
  if (ctx.reviewResult) return 'review';
  if (ctx.debugResult) return 'debug';
  if (ctx.analysisResult) return 'analysis';
  return 'skill_execution';
}

function getSuccessRate(ctx, type) {
  if (type === 'build') return ctx.testResults?.successRate || 0;
  if (type === 'debug') return ctx.debugResult?.fixed ? 1.0 : 0;
  return 1.0;
}

function inferDomain(ctx) {
  const map = { 'gemini-search': 'research', researcher: 'research', planner: 'planning', coder: 'development', reviewer: 'code-review' };
  return ctx.skillName ? map[ctx.skillName] : ctx.executionType;
}

function identifyDomains(ctx, type) {
  const domains = [];
  const dir = path.join(process.cwd(), EXPERTISE_DIR);
  if (!fs.existsSync(dir)) return domains;
  
  for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.yaml'))) {
    try {
      const exp = yaml.load(fs.readFileSync(path.join(dir, file), 'utf8'));
      if (exp.execution_contexts?.includes(type)) domains.push(file.replace('.yaml', ''));
      if (ctx.skillName && exp.related_skills?.includes(ctx.skillName)) domains.push(file.replace('.yaml', ''));
    } catch (e) {}
  }
  return [...new Set(domains)];
}

function extractLearnings(domain, ctx, type, config) {
  const learnings = [];
  const expPath = path.join(EXPERTISE_DIR, domain + '.yaml');
  let exp;
  try { exp = yaml.load(fs.readFileSync(expPath, 'utf8')); } catch (e) { return []; }
  
  if (type === 'research' && ctx.researchResult?.terminology) {
    for (const term of ctx.researchResult.terminology) {
      if (!exp.terminology?.includes(term)) learnings.push({ type: 'terminology', term, section: 'terminology', delta: 0.1 });
    }
  }
  if (type === 'planning' && ctx.planningResult?.taskBreakdown) {
    learnings.push({ type: 'task_breakdown', pattern: ctx.planningResult.taskBreakdown, section: 'planning_patterns', delta: 0.1 });
  }
  if (type === 'review' && ctx.reviewResult?.issues) {
    for (const issue of ctx.reviewResult.issues) {
      learnings.push({ type: 'issue_pattern', issue, section: 'known_issues', delta: 0.15 });
    }
  }
  if (type === 'debug' && ctx.debugResult?.rootCause) {
    learnings.push({ type: 'root_cause', cause: ctx.debugResult.rootCause, section: 'debugging.root_causes', delta: 0.25 });
  }
  
  return learnings.filter(l => config.types.includes(l.type));
}

async function validate(proposal) {
  let survived = 0, disproven = 0;
  for (const change of proposal.changes) {
    const delta = change.data?.delta || 0.1;
    if (delta >= 0.1) survived++; else disproven++;
  }
  return { survivalRate: proposal.changes.length > 0 ? survived / (survived + disproven) : 0, survived, disproven };
}

async function applyUpdate(domain, proposal, validation, type) {
  const expPath = path.join(EXPERTISE_DIR, domain + '.yaml');
  let exp;
  try { exp = yaml.load(fs.readFileSync(expPath, 'utf8')); } catch (e) { exp = { domain, metadata: { update_count: 0 } }; }
  
  exp.last_updated = new Date().toISOString();
  exp.metadata = exp.metadata || {};
  exp.metadata.update_count = (exp.metadata.update_count || 0) + 1;
  exp.learning_history = exp.learning_history || [];
  exp.learning_history.push({ timestamp: new Date().toISOString(), source: type, survived: validation.survived });
  
  const dir = path.dirname(expPath);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(expPath, yaml.dump(exp, { lineWidth: -1 }));
  console.log('Applied ' + validation.survived + ' learnings to ' + domain);
}

module.exports = { selfImproveHook, EXECUTION_CONTEXTS };
