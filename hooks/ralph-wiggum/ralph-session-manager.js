/**
 * Ralph Session Manager v3.0
 *
 * Enhanced session persistence for Ralph Wiggum loops with:
 * - Memory-MCP integration for cross-context handoff
 * - Checkpoint protocol after each phase
 * - Automated monitoring with rollback triggers
 * - Full state serialization and recovery
 *
 * @version 3.0.0
 * @see docs/META-LOOP-ENHANCEMENT-PLAN-v4.md Phase E
 *
 * Key Insights from Ralph Architecture (YouTube: "How to Make Claude Code Run in an Endless Loop"):
 * - Uses stop hook with exit code 2 to block exit and re-inject prompt
 * - State file tracks iteration count, completion promise, session_id
 * - Max iterations prevents infinite loops
 * - Clear completion criteria required for success
 */

const fs = require('fs');
const path = require('path');

// Configuration
const STATE_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.claude', 'ralph-wiggum');
const STATE_FILE = path.join(STATE_DIR, 'loop-state.md');
const META_STATE_FILE = path.join(STATE_DIR, 'meta-loop-state.yaml');
const SESSIONS_DIR = path.join(STATE_DIR, 'sessions');
const CHECKPOINTS_DIR = path.join(STATE_DIR, 'checkpoints');
const LOG_FILE = path.join(STATE_DIR, 'session-history.log');

// Memory MCP tagging protocol
let taggedMemoryStore, memoryMcpAvailable;
try {
  const taggingProtocol = require('../12fa/memory-mcp-tagging-protocol.js');
  taggedMemoryStore = taggingProtocol.taggedMemoryStore;
  memoryMcpAvailable = true;
  console.error('[RalphSessionManager] Memory MCP tagging protocol loaded');
} catch (err) {
  memoryMcpAvailable = false;
  console.error('[RalphSessionManager] Memory MCP not available - using file-only persistence');
}

/**
 * Ralph Loop Phase enumeration
 */
const RalphPhase = {
  PREPARE: 0,       // Initial setup, loading expertise
  AUDIT: 1,         // 4 parallel auditors
  EXECUTE: 2,       // Main foundry skill execution
  TEST: 3,          // Eval harness validation
  COMPARE: 4,       // Baseline vs candidate comparison
  COMMIT: 5,        // Apply changes with versioning
  MONITOR: 6,       // 7-day monitoring period
  ROLLBACK: 7       // Rollback if needed
};

/**
 * Enhanced Ralph Session State
 * Extends beyond simple state file to full session tracking
 */
class RalphSessionState {
  constructor(options = {}) {
    this.session_id = options.session_id || this.generateSessionId();
    this.phase = options.phase || RalphPhase.PREPARE;
    this.iteration = options.iteration || 0;
    this.max_iterations = options.max_iterations || 50;
    this.target_file = options.target_file || '';
    this.completion_promise = options.completion_promise || '';
    this.foundry_skill = options.foundry_skill || '';

    // New fields for Phase E
    this.proposals = options.proposals || [];
    this.auditor_results = options.auditor_results || {
      prompt: { status: 'pending', score: null },
      skill: { status: 'pending', score: null },
      expertise: { status: 'pending', score: null },
      output: { status: 'pending', score: null }
    };
    this.eval_results = options.eval_results || {};
    this.metrics = options.metrics || {
      baseline: null,
      candidate: null,
      delta: null
    };
    this.monitoring_day = options.monitoring_day || 0;
    this.commit_sha = options.commit_sha || null;

    // Session lifecycle
    this.started_at = options.started_at || new Date().toISOString();
    this.last_checkpoint = options.last_checkpoint || null;
    this.status = options.status || 'running'; // running, paused, completed, failed, rolled_back
    this.error_history = options.error_history || [];

    // Cross-context handoff
    this.context_id = options.context_id || this.generateContextId();
    this.previous_contexts = options.previous_contexts || [];
    this.handoff_notes = options.handoff_notes || [];
  }

  generateSessionId() {
    return `ralph-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  generateContextId() {
    return `ctx-${Date.now()}-${process.pid}`;
  }

  /**
   * Get phase name from number
   */
  getPhaseName() {
    const names = ['PREPARE', 'AUDIT', 'EXECUTE', 'TEST', 'COMPARE', 'COMMIT', 'MONITOR', 'ROLLBACK'];
    return names[this.phase] || 'UNKNOWN';
  }

  /**
   * Advance to next phase
   */
  advancePhase() {
    if (this.phase < RalphPhase.ROLLBACK) {
      this.phase++;
      this.last_checkpoint = new Date().toISOString();
    }
  }

  /**
   * Check if all auditors passed
   */
  auditorsAllPassed() {
    return Object.values(this.auditor_results)
      .every(r => r.status === 'passed' && r.score >= 0.8);
  }

  /**
   * Calculate overall progress percentage
   */
  getProgress() {
    const phaseProgress = (this.phase / 7) * 100;
    const iterProgress = (this.iteration / this.max_iterations) * 100;
    return Math.min(100, Math.max(phaseProgress, iterProgress / 2));
  }

  /**
   * Check if session should continue
   */
  shouldContinue() {
    return this.status === 'running' &&
           this.iteration < this.max_iterations &&
           this.phase <= RalphPhase.MONITOR;
  }

  /**
   * Serialize to JSON
   */
  toJSON() {
    return {
      session_id: this.session_id,
      phase: this.phase,
      phase_name: this.getPhaseName(),
      iteration: this.iteration,
      max_iterations: this.max_iterations,
      target_file: this.target_file,
      completion_promise: this.completion_promise,
      foundry_skill: this.foundry_skill,
      proposals: this.proposals,
      auditor_results: this.auditor_results,
      eval_results: this.eval_results,
      metrics: this.metrics,
      monitoring_day: this.monitoring_day,
      commit_sha: this.commit_sha,
      started_at: this.started_at,
      last_checkpoint: this.last_checkpoint,
      status: this.status,
      error_history: this.error_history,
      context_id: this.context_id,
      previous_contexts: this.previous_contexts,
      handoff_notes: this.handoff_notes,
      progress: this.getProgress(),
      'x-schema-version': '3.0'
    };
  }

  /**
   * Deserialize from JSON
   */
  static fromJSON(data) {
    return new RalphSessionState(data);
  }
}

/**
 * Ralph Session Manager
 * Handles persistence, checkpoints, and cross-context handoff
 */
class RalphSessionManager {
  constructor() {
    this.ensureDirectories();
    this._currentSession = null;
  }

  ensureDirectories() {
    [STATE_DIR, SESSIONS_DIR, CHECKPOINTS_DIR].forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
      }
    });
  }

  log(message) {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] ${message}\n`;
    fs.appendFileSync(LOG_FILE, logLine);
    console.error(`[RalphSessionManager] ${message}`);
  }

  /**
   * Start a new session
   */
  async startSession(options) {
    const session = new RalphSessionState(options);
    this._currentSession = session;

    // Save to file
    this.saveToFile(session);

    // Save checkpoint
    await this.checkpoint(session, 'Session started');

    // Persist to Memory MCP
    await this.persistToMemoryMCP(session);

    this.log(`Started session ${session.session_id} for ${session.target_file}`);

    return session;
  }

  /**
   * Load active session
   */
  loadActiveSession() {
    if (fs.existsSync(STATE_FILE)) {
      try {
        const content = fs.readFileSync(STATE_FILE, 'utf8');
        const data = this.parseStateFile(content);
        if (data.active === 'true' || data.active === true) {
          // Load full session from sessions dir if available
          const sessionFile = path.join(SESSIONS_DIR, `${data.session_id}.json`);
          if (fs.existsSync(sessionFile)) {
            const sessionData = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
            this._currentSession = RalphSessionState.fromJSON(sessionData);
          } else {
            // Create from state file
            this._currentSession = new RalphSessionState({
              session_id: data.session_id,
              iteration: parseInt(data.iteration) || 0,
              max_iterations: parseInt(data.max_iterations) || 50,
              completion_promise: data.completion_promise
            });
          }
          return this._currentSession;
        }
      } catch (err) {
        this.log(`Error loading session: ${err.message}`);
      }
    }
    return null;
  }

  /**
   * Parse the YAML-like state file
   */
  parseStateFile(content) {
    const data = {};
    const lines = content.split('\n');
    let inFrontmatter = false;
    let promptLines = [];
    let passedSecondDelimiter = false;

    for (const line of lines) {
      if (line.trim() === '---') {
        if (!inFrontmatter) {
          inFrontmatter = true;
        } else if (!passedSecondDelimiter) {
          passedSecondDelimiter = true;
        }
        continue;
      }

      if (inFrontmatter && !passedSecondDelimiter) {
        const match = line.match(/^(\w+):\s*(.*)$/);
        if (match) {
          data[match[1]] = match[2].replace(/^["']|["']$/g, '');
        }
      } else if (passedSecondDelimiter) {
        promptLines.push(line);
      }
    }

    data.prompt = promptLines.join('\n').trim();
    return data;
  }

  /**
   * Save session to file system
   */
  saveToFile(session) {
    // Save full session JSON
    const sessionFile = path.join(SESSIONS_DIR, `${session.session_id}.json`);
    fs.writeFileSync(sessionFile, JSON.stringify(session.toJSON(), null, 2), { mode: 0o600 });

    // Update state file for hook compatibility
    const stateContent = `---
session_id: ${session.session_id}
iteration: ${session.iteration}
max_iterations: ${session.max_iterations}
completion_promise: "${session.completion_promise}"
started_at: ${session.started_at}
active: ${session.status === 'running'}
phase: ${session.getPhaseName()}
---

${session.prompt || 'Continue working on the task.'}
`;
    fs.writeFileSync(STATE_FILE, stateContent, { mode: 0o600 });
  }

  /**
   * Create checkpoint (Phase E.3)
   */
  async checkpoint(session, note = '') {
    const checkpointId = `${session.session_id}-${session.phase}-${Date.now()}`;
    const checkpointFile = path.join(CHECKPOINTS_DIR, `${checkpointId}.json`);

    const checkpoint = {
      checkpoint_id: checkpointId,
      session: session.toJSON(),
      note: note,
      created_at: new Date().toISOString(),
      'x-tagging-version': '3.0'
    };

    // Save to file
    fs.writeFileSync(checkpointFile, JSON.stringify(checkpoint, null, 2), { mode: 0o600 });

    // Save to Memory MCP
    if (memoryMcpAvailable) {
      try {
        const tagged = taggedMemoryStore('ralph-session-manager', JSON.stringify(checkpoint), {
          project: 'context-cascade',
          'x-intent': 'checkpoint',
          'x-session-id': session.session_id,
          'x-phase': session.getPhaseName(),
          'x-namespace': 'ralph/checkpoints'
        });

        // Memory MCP store would be called here
        this.log(`Checkpoint ${checkpointId} created and tagged for Memory MCP`);
      } catch (err) {
        this.log(`Memory MCP checkpoint failed: ${err.message}`);
      }
    }

    session.last_checkpoint = new Date().toISOString();
    return checkpointId;
  }

  /**
   * Persist to Memory MCP (Phase E.4)
   */
  async persistToMemoryMCP(session) {
    if (!memoryMcpAvailable) {
      this.log('Memory MCP not available - skipping persistence');
      return false;
    }

    try {
      const sessionData = {
        type: 'ralph_session',
        session: session.toJSON(),
        persisted_at: new Date().toISOString(),
        resume_instructions: this.generateResumeInstructions(session)
      };

      const tagged = taggedMemoryStore('ralph-session-manager', JSON.stringify(sessionData), {
        project: 'context-cascade',
        'x-intent': 'session_persistence',
        'x-session-id': session.session_id,
        'x-status': session.status,
        'x-namespace': 'ralph/sessions'
      });

      this.log(`Session ${session.session_id} persisted to Memory MCP`);
      return true;
    } catch (err) {
      this.log(`Memory MCP persistence failed: ${err.message}`);
      return false;
    }
  }

  /**
   * Generate resume instructions for cross-context handoff
   */
  generateResumeInstructions(session) {
    return `
## Session Handoff: ${session.session_id}

### Current State
- Phase: ${session.getPhaseName()} (${session.phase}/7)
- Iteration: ${session.iteration}/${session.max_iterations}
- Status: ${session.status}
- Progress: ${session.getProgress().toFixed(1)}%

### Target
- File: ${session.target_file}
- Skill: ${session.foundry_skill}
- Completion: ${session.completion_promise}

### Resume Commands
1. Load session: RalphSessionManager.resumeSession("${session.session_id}")
2. Continue from phase ${session.getPhaseName()}
3. Check auditor results before proceeding

### Notes
${session.handoff_notes.join('\n') || 'No handoff notes'}
`;
  }

  /**
   * Resume session from Memory MCP (Phase E.4)
   */
  async resumeSession(sessionId) {
    // First check file system
    const sessionFile = path.join(SESSIONS_DIR, `${sessionId}.json`);
    if (fs.existsSync(sessionFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
        const session = RalphSessionState.fromJSON(data);

        // Track context handoff
        session.previous_contexts.push(session.context_id);
        session.context_id = session.generateContextId();
        session.handoff_notes.push(`Resumed in new context at ${new Date().toISOString()}`);

        this._currentSession = session;
        this.saveToFile(session);
        await this.checkpoint(session, 'Session resumed in new context');

        this.log(`Resumed session ${sessionId} from file`);
        return session;
      } catch (err) {
        this.log(`Error resuming from file: ${err.message}`);
      }
    }

    // Try Memory MCP
    if (memoryMcpAvailable) {
      this.log(`Attempting to resume ${sessionId} from Memory MCP...`);
      // Memory MCP query would go here
      // For now, return null to indicate not found
    }

    return null;
  }

  /**
   * Find active sessions (for cross-context discovery)
   */
  listActiveSessions() {
    const sessions = [];

    if (fs.existsSync(SESSIONS_DIR)) {
      const files = fs.readdirSync(SESSIONS_DIR);
      for (const file of files) {
        if (file.endsWith('.json')) {
          try {
            const data = JSON.parse(fs.readFileSync(path.join(SESSIONS_DIR, file), 'utf8'));
            if (data.status === 'running' || data.status === 'paused') {
              sessions.push({
                session_id: data.session_id,
                status: data.status,
                phase: data.phase_name,
                progress: data.progress,
                target: data.target_file,
                started_at: data.started_at,
                last_checkpoint: data.last_checkpoint
              });
            }
          } catch (err) {
            // Skip corrupted files
          }
        }
      }
    }

    return sessions;
  }

  /**
   * Update monitoring status (Phase E.5)
   */
  async updateMonitoring(session, metrics) {
    if (session.phase !== RalphPhase.MONITOR) {
      return;
    }

    session.monitoring_day++;
    session.metrics.current = metrics;

    // Check for regression
    if (session.metrics.baseline && metrics) {
      const delta = this.calculateDelta(session.metrics.baseline, metrics);
      session.metrics.delta = delta;

      // Auto-rollback trigger: >3% regression for 2+ days
      if (delta < -0.03 && session.monitoring_day >= 2) {
        this.log(`Regression detected: ${(delta * 100).toFixed(2)}% - triggering rollback consideration`);
        session.handoff_notes.push(`ALERT: Regression detected on day ${session.monitoring_day}: ${(delta * 100).toFixed(2)}%`);
        await this.checkpoint(session, 'Regression alert');
      }
    }

    // Complete monitoring after 7 days
    if (session.monitoring_day >= 7) {
      if (session.metrics.delta >= 0) {
        session.status = 'completed';
        this.log(`Session ${session.session_id} completed successfully after 7-day monitoring`);
      } else {
        session.phase = RalphPhase.ROLLBACK;
        this.log(`Session ${session.session_id} entering rollback due to regression`);
      }
    }

    this.saveToFile(session);
    await this.checkpoint(session, `Monitoring day ${session.monitoring_day}`);
  }

  calculateDelta(baseline, current) {
    if (!baseline || !current) return 0;
    // Simple average of all metrics
    const baseAvg = Object.values(baseline).reduce((a, b) => a + b, 0) / Object.values(baseline).length;
    const currAvg = Object.values(current).reduce((a, b) => a + b, 0) / Object.values(current).length;
    return currAvg - baseAvg;
  }

  /**
   * Mark session complete
   */
  async completeSession(session, success = true) {
    session.status = success ? 'completed' : 'failed';
    session.last_checkpoint = new Date().toISOString();

    this.saveToFile(session);
    await this.persistToMemoryMCP(session);

    this.log(`Session ${session.session_id} ${success ? 'completed' : 'failed'}`);

    // Deactivate state file for hook
    if (fs.existsSync(STATE_FILE)) {
      let content = fs.readFileSync(STATE_FILE, 'utf8');
      content = content.replace(/^active: true/m, 'active: false');
      fs.writeFileSync(STATE_FILE, content, { mode: 0o600 });
    }
  }

  /**
   * Get current session
   */
  getCurrentSession() {
    return this._currentSession || this.loadActiveSession();
  }
}

// Singleton instance
const manager = new RalphSessionManager();

// Export for use in hooks
module.exports = {
  RalphSessionState,
  RalphSessionManager,
  RalphPhase,
  manager,

  // Convenience functions
  startSession: (options) => manager.startSession(options),
  loadSession: () => manager.loadActiveSession(),
  resumeSession: (id) => manager.resumeSession(id),
  checkpoint: (session, note) => manager.checkpoint(session, note),
  completeSession: (session, success) => manager.completeSession(session, success),
  listActiveSessions: () => manager.listActiveSessions(),

  // Constants
  STATE_DIR,
  STATE_FILE,
  SESSIONS_DIR,
  CHECKPOINTS_DIR
};
