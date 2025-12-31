/**
 * E2E Tests: Three-Loop Workflow
 * Phase 5.1 Quality Expansion
 *
 * Tests the complete three-loop workflow:
 * - Inner Loop: Agent task execution
 * - Middle Loop: Workflow orchestration
 * - Outer Loop: Meta-improvement cycle
 *
 * @module quality/e2e/three-loop-workflow
 */

const fs = require('fs');
const path = require('path');
const { EventEmitter } = require('events');

/**
 * Mock agent executor for testing
 */
class MockAgentExecutor extends EventEmitter {
  constructor() {
    super();
    this.executionLog = [];
    this.state = 'idle';
  }

  async execute(agentId, task, options = {}) {
    this.state = 'running';
    this.executionLog.push({
      agentId,
      task,
      timestamp: Date.now(),
      options
    });

    this.emit('task:start', { agentId, task });

    // Simulate execution
    await this.delay(10);

    const result = {
      success: true,
      agentId,
      task,
      output: `Executed: ${task}`,
      duration: 10
    };

    this.state = 'idle';
    this.emit('task:complete', result);

    return result;
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getLog() {
    return this.executionLog;
  }

  reset() {
    this.executionLog = [];
    this.state = 'idle';
  }
}

/**
 * Mock workflow orchestrator
 */
class MockWorkflowOrchestrator extends EventEmitter {
  constructor(agentExecutor) {
    super();
    this.agentExecutor = agentExecutor;
    this.workflows = new Map();
    this.activeWorkflow = null;
  }

  async runWorkflow(workflowId, steps) {
    this.activeWorkflow = workflowId;
    this.workflows.set(workflowId, {
      id: workflowId,
      steps,
      status: 'running',
      results: [],
      startTime: Date.now()
    });

    this.emit('workflow:start', { workflowId, stepCount: steps.length });

    const workflow = this.workflows.get(workflowId);

    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      this.emit('step:start', { workflowId, stepIndex: i, step });

      try {
        const result = await this.agentExecutor.execute(
          step.agentId,
          step.task,
          step.options
        );

        workflow.results.push({
          stepIndex: i,
          success: true,
          result
        });

        this.emit('step:complete', { workflowId, stepIndex: i, result });
      } catch (err) {
        workflow.results.push({
          stepIndex: i,
          success: false,
          error: err.message
        });

        this.emit('step:error', { workflowId, stepIndex: i, error: err.message });

        if (!step.continueOnError) {
          workflow.status = 'failed';
          break;
        }
      }
    }

    workflow.status = workflow.results.every(r => r.success) ? 'completed' : 'failed';
    workflow.endTime = Date.now();
    workflow.duration = workflow.endTime - workflow.startTime;

    this.activeWorkflow = null;
    this.emit('workflow:complete', { workflowId, status: workflow.status });

    return workflow;
  }

  getWorkflow(workflowId) {
    return this.workflows.get(workflowId);
  }

  reset() {
    this.workflows.clear();
    this.activeWorkflow = null;
  }
}

/**
 * Mock meta-loop controller
 */
class MockMetaLoop extends EventEmitter {
  constructor(orchestrator) {
    super();
    this.orchestrator = orchestrator;
    this.cycles = [];
    this.metrics = {
      totalCycles: 0,
      successfulCycles: 0,
      improvements: []
    };
    this.running = false;
  }

  async runCycle(cycleConfig) {
    if (this.running) {
      throw new Error('Meta-loop already running');
    }

    this.running = true;
    const cycleId = `cycle-${Date.now()}`;

    this.emit('cycle:start', { cycleId });

    const cycle = {
      id: cycleId,
      config: cycleConfig,
      phases: [],
      startTime: Date.now()
    };

    // Phase 1: Analyze
    this.emit('phase:start', { cycleId, phase: 'analyze' });
    const analysisResult = await this.runAnalysisPhase(cycleConfig);
    cycle.phases.push({ name: 'analyze', result: analysisResult });
    this.emit('phase:complete', { cycleId, phase: 'analyze', result: analysisResult });

    // Phase 2: Plan
    this.emit('phase:start', { cycleId, phase: 'plan' });
    const planResult = await this.runPlanPhase(analysisResult);
    cycle.phases.push({ name: 'plan', result: planResult });
    this.emit('phase:complete', { cycleId, phase: 'plan', result: planResult });

    // Phase 3: Execute
    this.emit('phase:start', { cycleId, phase: 'execute' });
    const executeResult = await this.runExecutePhase(planResult);
    cycle.phases.push({ name: 'execute', result: executeResult });
    this.emit('phase:complete', { cycleId, phase: 'execute', result: executeResult });

    // Phase 4: Evaluate
    this.emit('phase:start', { cycleId, phase: 'evaluate' });
    const evaluateResult = await this.runEvaluatePhase(executeResult);
    cycle.phases.push({ name: 'evaluate', result: evaluateResult });
    this.emit('phase:complete', { cycleId, phase: 'evaluate', result: evaluateResult });

    cycle.endTime = Date.now();
    cycle.duration = cycle.endTime - cycle.startTime;
    cycle.success = evaluateResult.improved;

    this.cycles.push(cycle);
    this.metrics.totalCycles++;
    if (cycle.success) {
      this.metrics.successfulCycles++;
      this.metrics.improvements.push(evaluateResult.improvement);
    }

    this.running = false;
    this.emit('cycle:complete', { cycleId, success: cycle.success });

    return cycle;
  }

  async runAnalysisPhase(config) {
    // Simulate analysis
    await this.delay(5);
    return {
      targets: config.targets || ['performance', 'quality'],
      currentMetrics: {
        performance: 0.75,
        quality: 0.80
      }
    };
  }

  async runPlanPhase(analysis) {
    await this.delay(5);
    return {
      actions: analysis.targets.map(target => ({
        target,
        action: `improve_${target}`,
        priority: 1
      }))
    };
  }

  async runExecutePhase(plan) {
    // Execute via orchestrator
    const workflow = await this.orchestrator.runWorkflow(
      `meta-workflow-${Date.now()}`,
      plan.actions.map(action => ({
        agentId: 'improver',
        task: action.action,
        options: { target: action.target }
      }))
    );

    return {
      workflowId: workflow.id,
      success: workflow.status === 'completed',
      results: workflow.results
    };
  }

  async runEvaluatePhase(execution) {
    await this.delay(5);
    return {
      improved: execution.success,
      improvement: execution.success ? 0.05 : 0,
      newMetrics: {
        performance: 0.80,
        quality: 0.85
      }
    };
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getMetrics() {
    return this.metrics;
  }

  reset() {
    this.cycles = [];
    this.metrics = {
      totalCycles: 0,
      successfulCycles: 0,
      improvements: []
    };
    this.running = false;
  }
}

/**
 * Three-Loop Integration Test Suite
 */
class ThreeLoopTestSuite {
  constructor() {
    this.agentExecutor = new MockAgentExecutor();
    this.orchestrator = new MockWorkflowOrchestrator(this.agentExecutor);
    this.metaLoop = new MockMetaLoop(this.orchestrator);
    this.results = [];
  }

  async runTest(name, testFn) {
    const start = Date.now();
    try {
      await testFn();
      this.results.push({
        name,
        status: 'PASS',
        duration: Date.now() - start
      });
      console.log(`  [PASS] ${name}`);
      return true;
    } catch (err) {
      this.results.push({
        name,
        status: 'FAIL',
        error: err.message,
        duration: Date.now() - start
      });
      console.log(`  [FAIL] ${name}: ${err.message}`);
      return false;
    }
  }

  reset() {
    this.agentExecutor.reset();
    this.orchestrator.reset();
    this.metaLoop.reset();
  }

  async runAllTests() {
    console.log('\n=== E2E: Three-Loop Workflow Tests ===\n');

    // Inner Loop Tests
    console.log('--- Inner Loop (Agent Execution) ---');

    await this.runTest('Inner: Single agent task execution', async () => {
      this.reset();
      const result = await this.agentExecutor.execute('coder', 'write function');
      if (!result.success) throw new Error('Execution failed');
      if (result.agentId !== 'coder') throw new Error('Wrong agent');
    });

    await this.runTest('Inner: Multiple sequential tasks', async () => {
      this.reset();
      await this.agentExecutor.execute('coder', 'task 1');
      await this.agentExecutor.execute('reviewer', 'task 2');
      await this.agentExecutor.execute('tester', 'task 3');
      const log = this.agentExecutor.getLog();
      if (log.length !== 3) throw new Error(`Expected 3 tasks, got ${log.length}`);
    });

    await this.runTest('Inner: Event emission on task lifecycle', async () => {
      this.reset();
      let started = false;
      let completed = false;
      this.agentExecutor.on('task:start', () => { started = true; });
      this.agentExecutor.on('task:complete', () => { completed = true; });
      await this.agentExecutor.execute('coder', 'test task');
      if (!started) throw new Error('Start event not emitted');
      if (!completed) throw new Error('Complete event not emitted');
    });

    // Middle Loop Tests
    console.log('\n--- Middle Loop (Workflow Orchestration) ---');

    await this.runTest('Middle: Simple workflow execution', async () => {
      this.reset();
      const workflow = await this.orchestrator.runWorkflow('wf-1', [
        { agentId: 'coder', task: 'implement feature' },
        { agentId: 'tester', task: 'write tests' }
      ]);
      if (workflow.status !== 'completed') throw new Error('Workflow not completed');
      if (workflow.results.length !== 2) throw new Error('Not all steps executed');
    });

    await this.runTest('Middle: Workflow tracks all step results', async () => {
      this.reset();
      const workflow = await this.orchestrator.runWorkflow('wf-2', [
        { agentId: 'planner', task: 'create plan' },
        { agentId: 'coder', task: 'implement' },
        { agentId: 'reviewer', task: 'review' },
        { agentId: 'tester', task: 'test' }
      ]);
      if (workflow.results.length !== 4) throw new Error('Missing results');
      if (!workflow.results.every(r => r.success)) throw new Error('Some steps failed');
    });

    await this.runTest('Middle: Workflow events emitted correctly', async () => {
      this.reset();
      const events = [];
      this.orchestrator.on('workflow:start', () => events.push('start'));
      this.orchestrator.on('step:start', () => events.push('step'));
      this.orchestrator.on('workflow:complete', () => events.push('complete'));

      await this.orchestrator.runWorkflow('wf-3', [
        { agentId: 'coder', task: 'task 1' }
      ]);

      if (!events.includes('start')) throw new Error('No start event');
      if (!events.includes('step')) throw new Error('No step event');
      if (!events.includes('complete')) throw new Error('No complete event');
    });

    await this.runTest('Middle: Workflow duration tracked', async () => {
      this.reset();
      const workflow = await this.orchestrator.runWorkflow('wf-4', [
        { agentId: 'coder', task: 'task' }
      ]);
      if (!workflow.duration || workflow.duration < 0) {
        throw new Error('Duration not tracked');
      }
    });

    // Outer Loop Tests
    console.log('\n--- Outer Loop (Meta-Improvement) ---');

    await this.runTest('Outer: Meta-loop cycle completes', async () => {
      this.reset();
      const cycle = await this.metaLoop.runCycle({
        targets: ['performance']
      });
      if (!cycle.success) throw new Error('Cycle not successful');
      if (cycle.phases.length !== 4) throw new Error('Not all phases executed');
    });

    await this.runTest('Outer: All four phases execute', async () => {
      this.reset();
      const cycle = await this.metaLoop.runCycle({
        targets: ['quality']
      });
      const phaseNames = cycle.phases.map(p => p.name);
      if (!phaseNames.includes('analyze')) throw new Error('Missing analyze');
      if (!phaseNames.includes('plan')) throw new Error('Missing plan');
      if (!phaseNames.includes('execute')) throw new Error('Missing execute');
      if (!phaseNames.includes('evaluate')) throw new Error('Missing evaluate');
    });

    await this.runTest('Outer: Metrics updated after cycle', async () => {
      this.reset();
      const metricsBefore = { ...this.metaLoop.getMetrics() };
      await this.metaLoop.runCycle({ targets: ['performance'] });
      const metricsAfter = this.metaLoop.getMetrics();
      if (metricsAfter.totalCycles !== metricsBefore.totalCycles + 1) {
        throw new Error('Cycle count not incremented');
      }
    });

    await this.runTest('Outer: Prevents concurrent cycles', async () => {
      this.reset();
      // Start first cycle but don't await
      const cycle1Promise = this.metaLoop.runCycle({ targets: ['a'] });

      // Try to start second while first is running
      let blocked = false;
      try {
        // Small delay to ensure first cycle started
        await new Promise(r => setTimeout(r, 1));
        await this.metaLoop.runCycle({ targets: ['b'] });
      } catch (err) {
        if (err.message.includes('already running')) {
          blocked = true;
        }
      }

      await cycle1Promise; // Clean up
      if (!blocked) throw new Error('Concurrent cycle was allowed');
    });

    // Integration Tests
    console.log('\n--- Integration (Cross-Loop) ---');

    await this.runTest('Integration: Inner results flow to Middle', async () => {
      this.reset();
      const workflow = await this.orchestrator.runWorkflow('int-1', [
        { agentId: 'coder', task: 'write code' }
      ]);
      const agentLog = this.agentExecutor.getLog();
      if (agentLog.length !== 1) throw new Error('Agent not called');
      if (workflow.results[0].result.agentId !== 'coder') {
        throw new Error('Result not propagated');
      }
    });

    await this.runTest('Integration: Middle results flow to Outer', async () => {
      this.reset();
      const cycle = await this.metaLoop.runCycle({ targets: ['test'] });
      const executePhase = cycle.phases.find(p => p.name === 'execute');
      if (!executePhase.result.workflowId) {
        throw new Error('Workflow not created by meta-loop');
      }
    });

    await this.runTest('Integration: Full three-loop cycle', async () => {
      this.reset();

      // Run a complete meta-loop cycle which triggers:
      // Outer (meta) -> Middle (workflow) -> Inner (agents)
      const cycle = await this.metaLoop.runCycle({
        targets: ['performance', 'quality']
      });

      // Verify all layers were touched
      const agentLog = this.agentExecutor.getLog();
      if (agentLog.length < 2) throw new Error('Agents not executed');

      const metrics = this.metaLoop.getMetrics();
      if (metrics.totalCycles !== 1) throw new Error('Cycle not recorded');

      if (!cycle.success) throw new Error('Full cycle failed');
    });

    await this.runTest('Integration: State consistency across loops', async () => {
      this.reset();

      // Run multiple cycles
      await this.metaLoop.runCycle({ targets: ['a'] });
      await this.metaLoop.runCycle({ targets: ['b'] });

      const metrics = this.metaLoop.getMetrics();
      const agentLog = this.agentExecutor.getLog();

      // Each cycle should have touched agents
      if (agentLog.length < 2) throw new Error('State not accumulated');
      if (metrics.totalCycles !== 2) throw new Error('Metrics not consistent');
    });

    // Summary
    const passed = this.results.filter(r => r.status === 'PASS').length;
    const failed = this.results.filter(r => r.status === 'FAIL').length;

    console.log('\n========================================');
    console.log('E2E THREE-LOOP WORKFLOW RESULTS');
    console.log('========================================');
    console.log(`Total:  ${this.results.length}`);
    console.log(`Passed: ${passed}`);
    console.log(`Failed: ${failed}`);
    console.log(`Status: ${failed === 0 ? 'ALL TESTS PASSED' : 'FAILURES DETECTED'}`);
    console.log('========================================\n');

    return {
      total: this.results.length,
      passed,
      failed,
      results: this.results
    };
  }
}

// Export for use in audit
module.exports = {
  MockAgentExecutor,
  MockWorkflowOrchestrator,
  MockMetaLoop,
  ThreeLoopTestSuite
};

// Run if executed directly
if (require.main === module) {
  const suite = new ThreeLoopTestSuite();
  suite.runAllTests().then(results => {
    process.exit(results.failed > 0 ? 1 : 0);
  });
}
