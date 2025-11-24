/**
 * E2E Workflow 3: Agent Activity → Real-time Feed → Workflow Graph
 * P4_T7 - Integration Testing
 *
 * Test Flow:
 * 1. Spawn 3 agents via hooks
 * 2. Verify real-time activity feed updates
 * 3. Verify workflow graph shows agent dependencies
 * 4. Test WebSocket real-time event streaming
 * 5. Verify agent status transitions
 *
 * Target: <5% failure rate
 */

import { test, expect, Page } from '@playwright/test';
import { WebSocketHelper } from '../helpers/websocket-helper';
import { AgentActivityPage } from '../pages/AgentActivityPage';
import { WorkflowGraphPage } from '../pages/WorkflowGraphPage';
import { ApiHelper } from '../helpers/api-helper';

test.describe('Workflow 3: Agent Activity and Real-time Monitoring', () => {
  let wsHelper: WebSocketHelper;
  let activityPage: AgentActivityPage;
  let graphPage: WorkflowGraphPage;
  let apiHelper: ApiHelper;
  let agentIds: string[] = [];

  test.beforeEach(async ({ page }) => {
    wsHelper = new WebSocketHelper(page);
    activityPage = new AgentActivityPage(page);
    graphPage = new WorkflowGraphPage(page);
    apiHelper = new ApiHelper(page);

    // Connect WebSocket
    await wsHelper.connect();
  });

  test.afterEach(async () => {
    // Cleanup agents
    for (const agentId of agentIds) {
      await apiHelper.delete(`/api/agents/${agentId}`);
    }
    agentIds = [];

    await wsHelper.disconnect();
  });

  test('should spawn agents, monitor activity, and visualize workflow', async ({ page }) => {
    // Step 1: Spawn 3 agents via hooks
    await activityPage.goto();

    // Set up WebSocket listeners for agent events
    const agentEvents: any[] = [];
    await wsHelper.onMessage('agent_spawned', (data) => {
      agentEvents.push({ type: 'spawned', ...data });
    });
    await wsHelper.onMessage('agent_status_update', (data) => {
      agentEvents.push({ type: 'status_update', ...data });
    });
    await wsHelper.onMessage('agent_activity', (data) => {
      agentEvents.push({ type: 'activity', ...data });
    });

    // Define agent configurations
    const agents = [
      {
        name: 'Research Agent',
        type: 'researcher',
        capabilities: ['web-search', 'data-analysis', 'report-generation'],
        dependencies: [],
      },
      {
        name: 'Coder Agent',
        type: 'coder',
        capabilities: ['code-generation', 'testing', 'debugging'],
        dependencies: ['researcher'], // Depends on research agent
      },
      {
        name: 'Reviewer Agent',
        type: 'reviewer',
        capabilities: ['code-review', 'security-audit', 'quality-check'],
        dependencies: ['coder'], // Depends on coder agent
      },
    ];

    // Spawn agents one by one
    for (const agentConfig of agents) {
      await activityPage.clickSpawnAgent();

      const agentForm = page.locator('[data-testid="agent-spawn-form"]');
      await expect(agentForm).toBeVisible({ timeout: 2000 });

      await agentForm.locator('[name="name"]').fill(agentConfig.name);
      await agentForm.locator('[name="type"]').selectOption(agentConfig.type);

      // Add capabilities
      for (const capability of agentConfig.capabilities) {
        await agentForm.locator('[data-testid="add-capability"]').click();
        const capabilityInput = agentForm.locator('[data-capability]:last-child input');
        await capabilityInput.fill(capability);
      }

      // Add dependencies
      for (const dependency of agentConfig.dependencies) {
        const dependencySelect = agentForm.locator('[name="dependencies"]');
        await dependencySelect.selectOption({ label: dependency });
      }

      await agentForm.locator('[data-testid="spawn-agent-submit"]').click();

      // Wait for agent spawned event
      await wsHelper.waitForMessage('agent_spawned', {
        name: agentConfig.name,
      }, 5000);

      // Extract agent ID from response
      const spawnedEvent = agentEvents.find(
        e => e.type === 'spawned' && e.name === agentConfig.name
      );
      expect(spawnedEvent).toBeTruthy();
      agentIds.push(spawnedEvent.agent_id);

      await page.waitForTimeout(500); // Allow UI to update
    }

    expect(agentIds.length).toBe(3);

    // Step 2: Verify real-time activity feed updates
    await page.waitForLoadState('networkidle');

    // Verify all agents appear in activity feed
    for (const agentId of agentIds) {
      const agentFeedItem = page.locator(`[data-agent-id="${agentId}"]`);
      await expect(agentFeedItem).toBeVisible({ timeout: 3000 });
    }

    // Verify feed shows spawn events
    for (const agent of agents) {
      const spawnEvent = page.locator('[data-event-type="agent_spawned"]', {
        has: page.locator(`text="${agent.name}"`),
      });
      await expect(spawnEvent.first()).toBeVisible({ timeout: 3000 });
    }

    // Trigger agent activity
    const researchAgentId = agentIds[0];
    await apiHelper.post(`/api/agents/${researchAgentId}/execute`, {
      task: 'Research best practices for E2E testing',
    });

    // Wait for activity event
    await wsHelper.waitForMessage('agent_activity', {
      agent_id: researchAgentId,
    }, 10000);

    // Verify activity appears in feed
    const activityEvent = page.locator('[data-event-type="agent_activity"]', {
      has: page.locator(`[data-agent-id="${researchAgentId}"]`),
    });
    await expect(activityEvent.first()).toBeVisible({ timeout: 3000 });

    // Verify timestamp is recent
    const timestamp = await activityEvent.first().locator('[data-testid="event-timestamp"]').textContent();
    expect(timestamp).toBeTruthy();

    const eventTime = new Date(timestamp!);
    const now = new Date();
    const timeDiff = Math.abs(now.getTime() - eventTime.getTime());
    expect(timeDiff).toBeLessThan(60000); // Within last minute

    // Step 3: Verify workflow graph shows agent dependencies
    await graphPage.goto();
    await page.waitForLoadState('networkidle');

    // Verify all agents appear as nodes in graph
    for (let i = 0; i < agents.length; i++) {
      const agentNode = page.locator(`[data-graph-node-id="${agentIds[i]}"]`);
      await expect(agentNode).toBeVisible({ timeout: 5000 });

      // Verify node shows agent name
      await expect(agentNode).toContainText(agents[i].name);

      // Verify node shows agent type
      await expect(agentNode).toHaveAttribute('data-agent-type', agents[i].type);
    }

    // Verify dependency edges
    // Research Agent → Coder Agent
    const edge1 = page.locator(`[data-edge-from="${agentIds[0]}"][data-edge-to="${agentIds[1]}"]`);
    await expect(edge1).toBeVisible({ timeout: 3000 });

    // Coder Agent → Reviewer Agent
    const edge2 = page.locator(`[data-edge-from="${agentIds[1]}"][data-edge-to="${agentIds[2]}"]`);
    await expect(edge2).toBeVisible({ timeout: 3000 });

    // Verify graph layout
    // Research Agent should be leftmost (no dependencies)
    // Reviewer Agent should be rightmost (depends on others)
    const researchNodeBox = await page.locator(`[data-graph-node-id="${agentIds[0]}"]`).boundingBox();
    const reviewerNodeBox = await page.locator(`[data-graph-node-id="${agentIds[2]}"]`).boundingBox();

    expect(researchNodeBox).toBeTruthy();
    expect(reviewerNodeBox).toBeTruthy();
    expect(researchNodeBox!.x).toBeLessThan(reviewerNodeBox!.x);

    // Step 4: Test interactive graph features
    // Click on node to show details
    const coderNode = page.locator(`[data-graph-node-id="${agentIds[1]}"]`);
    await coderNode.click();

    const nodeDetails = page.locator('[data-testid="node-details-panel"]');
    await expect(nodeDetails).toBeVisible({ timeout: 2000 });

    // Verify details panel shows agent info
    await expect(nodeDetails).toContainText('Coder Agent');
    await expect(nodeDetails).toContainText('coder');

    // Verify capabilities are listed
    for (const capability of agents[1].capabilities) {
      await expect(nodeDetails).toContainText(capability);
    }

    // Verify dependencies are listed
    await expect(nodeDetails).toContainText('researcher');

    // Test zoom controls
    const zoomInButton = page.locator('[data-testid="graph-zoom-in"]');
    await zoomInButton.click();
    await page.waitForTimeout(300);

    const zoomOutButton = page.locator('[data-testid="graph-zoom-out"]');
    await zoomOutButton.click();
    await page.waitForTimeout(300);

    // Test pan (drag graph)
    const graphContainer = page.locator('[data-testid="workflow-graph-container"]');
    const containerBox = await graphContainer.boundingBox();

    if (containerBox) {
      await page.mouse.move(containerBox.x + 100, containerBox.y + 100);
      await page.mouse.down();
      await page.mouse.move(containerBox.x + 200, containerBox.y + 200, { steps: 10 });
      await page.mouse.up();
    }

    // Verify graph still shows all nodes after pan
    for (const agentId of agentIds) {
      const agentNode = page.locator(`[data-graph-node-id="${agentId}"]`);
      await expect(agentNode).toBeVisible();
    }

    // Step 5: Test agent status transitions and real-time updates
    // Change agent status
    await apiHelper.patch(`/api/agents/${agentIds[1]}`, {
      status: 'busy',
    });

    // Wait for status update event
    await wsHelper.waitForMessage('agent_status_update', {
      agent_id: agentIds[1],
      status: 'busy',
    }, 5000);

    // Verify graph node reflects new status
    const busyNode = page.locator(`[data-graph-node-id="${agentIds[1]}"]`);
    await expect(busyNode).toHaveAttribute('data-status', 'busy', { timeout: 3000 });

    // Verify activity feed shows status change
    await activityPage.goto();
    const statusEvent = page.locator('[data-event-type="agent_status_update"]', {
      has: page.locator(`[data-agent-id="${agentIds[1]}"]`),
    });
    await expect(statusEvent.first()).toBeVisible({ timeout: 3000 });
    await expect(statusEvent.first()).toContainText('busy');
  });

  test('should handle agent failures and cleanup', async ({ page }) => {
    // Spawn agent that will fail
    await activityPage.goto();

    await wsHelper.onMessage('agent_error', (data) => {
      console.log('Agent error:', data);
    });

    await activityPage.clickSpawnAgent();

    const agentForm = page.locator('[data-testid="agent-spawn-form"]');
    await agentForm.locator('[name="name"]').fill('Failing Agent');
    await agentForm.locator('[name="type"]').selectOption('tester');

    // Add invalid capability to trigger error
    await agentForm.locator('[data-testid="add-capability"]').click();
    const capabilityInput = agentForm.locator('[data-capability]:last-child input');
    await capabilityInput.fill('invalid-capability-trigger-error');

    await agentForm.locator('[data-testid="spawn-agent-submit"]').click();

    // Wait for error event
    const errorReceived = await wsHelper.waitForMessage('agent_error', {
      name: 'Failing Agent',
    }, 5000).catch(() => null);

    // Verify error appears in activity feed
    if (errorReceived) {
      const errorEvent = page.locator('[data-event-type="agent_error"]');
      await expect(errorEvent.first()).toBeVisible({ timeout: 3000 });
      await expect(errorEvent.first()).toContainText('error');
    }

    // Verify error notification
    const errorNotification = page.locator('[data-testid="error-notification"]');
    await expect(errorNotification).toBeVisible({ timeout: 3000 });
  });

  test('should support accessibility for agent monitoring', async ({ page }) => {
    // Spawn agent via keyboard
    await activityPage.goto();

    await page.keyboard.press('Tab'); // Focus spawn button
    await page.keyboard.press('Enter');

    const agentForm = page.locator('[data-testid="agent-spawn-form"]');
    await expect(agentForm).toBeVisible();

    // Tab through form fields
    await page.keyboard.press('Tab'); // Name field
    await page.keyboard.type('Accessible Agent');

    await page.keyboard.press('Tab'); // Type select
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('Enter');

    await page.keyboard.press('Tab'); // Submit button
    await page.keyboard.press('Enter');

    // Verify agent spawned
    await wsHelper.waitForMessage('agent_spawned', {
      name: 'Accessible Agent',
    }, 5000);

    // Navigate activity feed with keyboard
    const firstFeedItem = page.locator('[data-event-type]:first-child');
    await firstFeedItem.focus();

    await page.keyboard.press('ArrowDown'); // Next item
    await page.keyboard.press('ArrowUp'); // Previous item

    // Open details with Enter
    await page.keyboard.press('Enter');

    const details = page.locator('[data-testid="event-details"]');
    await expect(details).toBeVisible({ timeout: 2000 });

    // Navigate graph with keyboard
    await graphPage.goto();

    const graphContainer = page.locator('[data-testid="workflow-graph-container"]');
    await graphContainer.focus();

    // Use arrow keys to navigate
    await page.keyboard.press('ArrowRight'); // Next node
    await page.keyboard.press('ArrowLeft'); // Previous node

    // Use Enter to select node
    await page.keyboard.press('Enter');

    const nodeDetails = page.locator('[data-testid="node-details-panel"]');
    await expect(nodeDetails).toBeVisible({ timeout: 2000 });
  });
});
