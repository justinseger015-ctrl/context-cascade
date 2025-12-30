#!/usr/bin/env node
/**
 * Ralph Loop Stop Hook (Enhanced v3.0)
 *
 * Enhanced stop hook for Ralph Wiggum persistence loops.
 * Integrates with RalphSessionManager for:
 * - Cross-context handoff via Memory MCP
 * - Checkpoint after each phase
 * - Automatic monitoring triggers
 *
 * Hook Mechanism (from YouTube "How to Make Claude Code Run in an Endless Loop"):
 * - Runs when Claude tries to end session
 * - Exit code 0 = allow exit
 * - Exit code 2 = block exit and re-inject prompt
 * - Checks completion promise in output
 * - Tracks iteration count with max limit
 *
 * @version 3.0.0
 */

const fs = require('fs');
const path = require('path');

// Import session manager
let sessionManager;
try {
  sessionManager = require('./ralph-session-manager.js');
} catch (err) {
  console.error('[RalphStopHook] Session manager not available:', err.message);
  process.exit(0);
}

const { manager, RalphPhase, STATE_FILE } = sessionManager;

/**
 * Main hook execution
 */
async function main() {
  // Read Claude's output from stdin
  let claudeOutput = '';
  try {
    claudeOutput = fs.readFileSync(0, 'utf8');
  } catch (err) {
    // No stdin available
  }

  // Load active session
  const session = manager.loadActiveSession();

  if (!session) {
    // No active loop, allow normal exit
    console.error('[RalphStopHook] No active session, allowing exit');
    process.exit(0);
  }

  if (session.status !== 'running') {
    console.error(`[RalphStopHook] Session status is ${session.status}, allowing exit`);
    process.exit(0);
  }

  // Check for completion promise
  if (session.completion_promise) {
    const promisePattern = new RegExp(`<promise>${escapeRegex(session.completion_promise)}</promise>`);
    if (promisePattern.test(claudeOutput)) {
      console.error(`[RalphStopHook] Completion promise found: ${session.completion_promise}`);

      // Mark session complete
      await manager.completeSession(session, true);

      printCompletionBanner(session);
      process.exit(0);
    }
  }

  // Increment iteration
  session.iteration++;
  manager.log(`Iteration ${session.iteration} of ${session.max_iterations}`);

  // Check max iterations
  if (session.iteration >= session.max_iterations) {
    console.error('[RalphStopHook] Max iterations reached');

    session.status = 'failed';
    session.error_history.push({
      error: 'MAX_ITERATIONS_REACHED',
      iteration: session.iteration,
      timestamp: new Date().toISOString()
    });

    await manager.completeSession(session, false);

    printMaxIterationsBanner(session);
    process.exit(0);
  }

  // Check for phase-specific completion signals
  const phaseResult = checkPhaseCompletion(claudeOutput, session);
  if (phaseResult.advance) {
    session.advancePhase();
    await manager.checkpoint(session, phaseResult.note);
    console.error(`[RalphStopHook] Advanced to phase ${session.getPhaseName()}`);
  }

  // Update auditor results if present
  updateAuditorResults(claudeOutput, session);

  // Save updated state
  manager.saveToFile(session);
  await manager.checkpoint(session, `Iteration ${session.iteration}`);

  // Re-inject prompt
  printContinuationBanner(session);
  outputPrompt(session);

  // Exit code 2 blocks exit and re-triggers
  process.exit(2);
}

/**
 * Check for phase-specific completion signals
 */
function checkPhaseCompletion(output, session) {
  const phaseSignals = {
    [RalphPhase.PREPARE]: ['EXPERTISE_LOADED', 'PREPARATION_COMPLETE'],
    [RalphPhase.AUDIT]: ['ALL_AUDITS_PASSED', 'AUDIT_COMPLETE'],
    [RalphPhase.EXECUTE]: ['EXECUTION_COMPLETE', session.completion_promise],
    [RalphPhase.TEST]: ['TESTS_PASSED', 'EVAL_COMPLETE'],
    [RalphPhase.COMPARE]: ['COMPARISON_DONE', 'ACCEPT', 'REJECT'],
    [RalphPhase.COMMIT]: ['COMMIT_COMPLETE', 'COMMITTED'],
    [RalphPhase.MONITOR]: ['MONITORING_COMPLETE', 'DAY_7_COMPLETE']
  };

  const signals = phaseSignals[session.phase] || [];

  for (const signal of signals) {
    if (signal && output.includes(signal)) {
      return { advance: true, note: `Phase signal: ${signal}` };
    }
  }

  return { advance: false };
}

/**
 * Update auditor results from output
 */
function updateAuditorResults(output, session) {
  const auditors = ['prompt', 'skill', 'expertise', 'output'];

  for (const auditor of auditors) {
    // Look for auditor result patterns
    const passPattern = new RegExp(`${auditor}[-_]?auditor.*pass`, 'i');
    const failPattern = new RegExp(`${auditor}[-_]?auditor.*fail`, 'i');
    const scorePattern = new RegExp(`${auditor}[-_]?auditor.*score[:\\s]*(\\d+\\.?\\d*)`, 'i');

    if (passPattern.test(output)) {
      session.auditor_results[auditor].status = 'passed';
    } else if (failPattern.test(output)) {
      session.auditor_results[auditor].status = 'failed';
    }

    const scoreMatch = output.match(scorePattern);
    if (scoreMatch) {
      session.auditor_results[auditor].score = parseFloat(scoreMatch[1]);
    }
  }
}

/**
 * Output the continuation prompt
 */
function outputPrompt(session) {
  console.log(`
ORIGINAL TASK:
---
${session.target_file ? `Target: ${session.target_file}` : ''}
${session.foundry_skill ? `Skill: ${session.foundry_skill}` : ''}
${session.prompt || 'Continue working on the task.'}
---

Current Phase: ${session.getPhaseName()}
Progress: ${session.getProgress().toFixed(1)}%

Continue working on this task. Check files for your previous progress.
If tests exist, run them and fix any failures.
If blocked, document what's preventing progress.
`);

  if (session.completion_promise) {
    console.log(`To complete, output exactly: <promise>${session.completion_promise}</promise>\n`);
  }
}

function printContinuationBanner(session) {
  console.log(`
==========================================
   RALPH LOOP: ITERATION ${session.iteration} of ${session.max_iterations}
==========================================

Phase: ${session.getPhaseName()} | Progress: ${session.getProgress().toFixed(1)}%
Session: ${session.session_id}

The loop continues. Previous work persists in files.
Review your progress and continue working toward completion.
`);
}

function printCompletionBanner(session) {
  console.log(`
==========================================
   RALPH LOOP: TASK COMPLETE!
==========================================

Completion promise verified: ${session.completion_promise}
Total iterations: ${session.iteration}
Final phase: ${session.getPhaseName()}
Session: ${session.session_id}

Session state saved for future reference.
`);
}

function printMaxIterationsBanner(session) {
  console.log(`
==========================================
   RALPH LOOP: MAX ITERATIONS REACHED
==========================================

Completed ${session.max_iterations} iterations without completion promise.
Last phase: ${session.getPhaseName()}
Progress: ${session.getProgress().toFixed(1)}%
Session: ${session.session_id}

Loop has been deactivated. Session state preserved.
Consider:
1. Reviewing the task requirements
2. Breaking the task into smaller steps
3. Increasing max_iterations if needed
`);
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Run
main().catch(err => {
  console.error('[RalphStopHook] Error:', err.message);
  process.exit(0);
});
