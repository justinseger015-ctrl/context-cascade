/**
 * Test Data Fixtures for E2E Tests
 */

export const testProjects = [
  {
    name: 'E2E Test Project 1',
    description: 'First test project for E2E workflows',
  },
  {
    name: 'E2E Test Project 2',
    description: 'Second test project for concurrent testing',
  },
];

export const testTasks = [
  {
    title: 'Test Task 1',
    description: 'First test task',
    skillName: 'test-skill-1',
    cronSchedule: '0 12 * * *',
    priority: 'high',
    params: {
      param1: 'value1',
      param2: 'value2',
    },
  },
  {
    title: 'Test Task 2',
    description: 'Second test task',
    skillName: 'test-skill-2',
    cronSchedule: '*/30 * * * *',
    priority: 'medium',
    params: {
      testMode: true,
    },
  },
];

export const testAgents = [
  {
    name: 'Test Researcher',
    type: 'researcher',
    capabilities: ['research', 'analysis', 'reporting'],
  },
  {
    name: 'Test Coder',
    type: 'coder',
    capabilities: ['coding', 'testing', 'debugging'],
  },
  {
    name: 'Test Reviewer',
    type: 'reviewer',
    capabilities: ['review', 'security', 'quality'],
  },
];

/**
 * Generate unique test data
 */
export function generateUniqueTestData(prefix: string = 'E2E') {
  const timestamp = Date.now();
  return {
    project: {
      name: `${prefix} Project ${timestamp}`,
      description: `Test project created at ${new Date().toISOString()}`,
    },
    task: {
      title: `${prefix} Task ${timestamp}`,
      description: `Test task created at ${new Date().toISOString()}`,
      skillName: `test-skill-${timestamp}`,
      cronSchedule: '0 0 * * *',
      priority: 'medium',
      params: { testId: timestamp },
    },
    agent: {
      name: `${prefix} Agent ${timestamp}`,
      type: 'coder',
      capabilities: ['test-capability-1', 'test-capability-2'],
    },
  };
}
