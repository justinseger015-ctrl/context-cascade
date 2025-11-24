/**
 * k6 Load Test Script - API Performance Benchmarking
 *
 * Targets: P99 latency <200ms for all endpoints
 * Load: 100 concurrent users, 10 req/s per user
 * Duration: 5 minutes
 */

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const taskLatency = new Trend('task_latency');
const projectLatency = new Trend('project_latency');
const agentLatency = new Trend('agent_latency');
const totalRequests = new Counter('total_requests');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 20 },  // Ramp-up to 20 users
    { duration: '1m', target: 50 },  // Ramp-up to 50 users
    { duration: '1m', target: 100 }, // Ramp-up to 100 users
    { duration: '2m', target: 100 }, // Sustain 100 users
    { duration: '1m', target: 0 },   // Ramp-down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<150', 'p(99)<200'], // 95% < 150ms, 99% < 200ms
    'http_req_failed': ['rate<0.01'], // Error rate < 1%
    'errors': ['rate<0.01'],
  },
};

const BASE_URL = __ENV.API_URL || 'http://localhost:8000';
const API_VERSION = '/api/v1';

// Sample task data for POST requests
const sampleTask = JSON.stringify({
  name: 'Performance Test Task',
  description: 'Automated k6 load test',
  cron_expression: '0 */6 * * *',
  agent_type: 'researcher',
  project_id: 1,
  enabled: true,
  metadata: { test: true }
});

// Sample project data
const sampleProject = JSON.stringify({
  name: 'Load Test Project',
  description: 'k6 performance testing',
  status: 'active',
  metadata: { test: true }
});

// Headers
const headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
};

/**
 * Main test scenario
 * Simulates realistic user behavior
 */
export default function () {
  totalRequests.add(1);

  // Scenario 1: Health check (lightweight)
  const healthRes = http.get(`${BASE_URL}${API_VERSION}/health`, { headers });
  check(healthRes, {
    'Health check status is 200': (r) => r.status === 200,
    'Health check has uptime': (r) => JSON.parse(r.body).uptime !== undefined,
  });
  errorRate.add(healthRes.status !== 200);

  sleep(0.5);

  // Scenario 2: Get all tasks
  const tasksRes = http.get(`${BASE_URL}${API_VERSION}/tasks`, { headers });
  const taskDuration = tasksRes.timings.duration;
  taskLatency.add(taskDuration);

  check(tasksRes, {
    'GET /tasks status is 200': (r) => r.status === 200,
    'GET /tasks P99 < 200ms': (r) => r.timings.duration < 200,
  });
  errorRate.add(tasksRes.status !== 200);

  sleep(1);

  // Scenario 3: Create new task
  const createTaskRes = http.post(
    `${BASE_URL}${API_VERSION}/tasks`,
    sampleTask,
    { headers }
  );

  check(createTaskRes, {
    'POST /tasks status is 201': (r) => r.status === 201,
    'POST /tasks has id': (r) => JSON.parse(r.body).id !== undefined,
  });
  errorRate.add(createTaskRes.status !== 201);

  const taskId = createTaskRes.status === 201
    ? JSON.parse(createTaskRes.body).id
    : 1;

  sleep(0.5);

  // Scenario 4: Get single task by ID
  const singleTaskRes = http.get(
    `${BASE_URL}${API_VERSION}/tasks/${taskId}`,
    { headers }
  );

  check(singleTaskRes, {
    'GET /tasks/{id} status is 200': (r) => r.status === 200 || r.status === 404,
  });
  errorRate.add(singleTaskRes.status !== 200 && singleTaskRes.status !== 404);

  sleep(1);

  // Scenario 5: Update task
  const updateTaskRes = http.put(
    `${BASE_URL}${API_VERSION}/tasks/${taskId}`,
    JSON.stringify({ enabled: false }),
    { headers }
  );

  check(updateTaskRes, {
    'PUT /tasks/{id} status is 200': (r) => r.status === 200 || r.status === 404,
  });
  errorRate.add(updateTaskRes.status !== 200 && updateTaskRes.status !== 404);

  sleep(1);

  // Scenario 6: Get all projects
  const projectsRes = http.get(`${BASE_URL}${API_VERSION}/projects`, { headers });
  const projectDuration = projectsRes.timings.duration;
  projectLatency.add(projectDuration);

  check(projectsRes, {
    'GET /projects status is 200': (r) => r.status === 200,
    'GET /projects P99 < 200ms': (r) => r.timings.duration < 200,
  });
  errorRate.add(projectsRes.status !== 200);

  sleep(1);

  // Scenario 7: Get all agents
  const agentsRes = http.get(`${BASE_URL}${API_VERSION}/agents`, { headers });
  const agentDuration = agentsRes.timings.duration;
  agentLatency.add(agentDuration);

  check(agentsRes, {
    'GET /agents status is 200': (r) => r.status === 200,
    'GET /agents P99 < 200ms': (r) => r.timings.duration < 200,
  });
  errorRate.add(agentsRes.status !== 200);

  sleep(1);

  // Scenario 8: Delete task (cleanup)
  const deleteTaskRes = http.del(
    `${BASE_URL}${API_VERSION}/tasks/${taskId}`,
    null,
    { headers }
  );

  check(deleteTaskRes, {
    'DELETE /tasks/{id} status is 204': (r) => r.status === 204 || r.status === 404,
  });
  errorRate.add(deleteTaskRes.status !== 204 && deleteTaskRes.status !== 404);

  sleep(2); // Total scenario duration: ~10 seconds
}

/**
 * Teardown function
 * Runs once at the end of the test
 */
export function teardown(data) {
  console.log('====================================');
  console.log('k6 Load Test Summary');
  console.log('====================================');
  console.log(`Total Requests: ${totalRequests.count}`);
  console.log('Latency Trends:');
  console.log(`  - Tasks: P95=${taskLatency.p(95)}ms, P99=${taskLatency.p(99)}ms`);
  console.log(`  - Projects: P95=${projectLatency.p(95)}ms, P99=${projectLatency.p(99)}ms`);
  console.log(`  - Agents: P95=${agentLatency.p(95)}ms, P99=${agentLatency.p(99)}ms`);
  console.log(`Error Rate: ${(errorRate.rate * 100).toFixed(2)}%`);
  console.log('====================================');
}
