/**
 * k6 WebSocket Benchmark - Real-time Performance Testing
 *
 * Targets: Message latency <100ms
 * Load: 1000 concurrent connections, 10 msg/s per connection
 * Duration: 5 minutes
 */

import ws from 'k6/ws';
import { check } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const messageLatency = new Trend('message_latency');
const connectionErrors = new Rate('connection_errors');
const messagesSent = new Counter('messages_sent');
const messagesReceived = new Counter('messages_received');

// Test configuration
export const options = {
  stages: [
    { duration: '1m', target: 100 },   // Ramp-up to 100 connections
    { duration: '1m', target: 500 },   // Ramp-up to 500 connections
    { duration: '1m', target: 1000 },  // Ramp-up to 1000 connections
    { duration: '2m', target: 1000 },  // Sustain 1000 connections
    { duration: '1m', target: 0 },     // Ramp-down
  ],
  thresholds: {
    'message_latency': ['p(95)<80', 'p(99)<100'], // 95% < 80ms, 99% < 100ms
    'connection_errors': ['rate<0.01'], // Error rate < 1%
  },
};

const WS_URL = __ENV.WS_URL || 'ws://localhost:8000/ws';

/**
 * Main WebSocket test scenario
 */
export default function () {
  const url = WS_URL;
  const params = { tags: { name: 'WebSocket Benchmark' } };

  const res = ws.connect(url, params, function (socket) {
    socket.on('open', () => {
      console.log('WebSocket connection established');

      // Send messages at 10 msg/s (every 100ms)
      let messageCount = 0;
      const maxMessages = 50; // Send 50 messages per VU (5 seconds worth)

      const interval = setInterval(() => {
        if (messageCount >= maxMessages) {
          clearInterval(interval);
          socket.close();
          return;
        }

        const sendTime = Date.now();
        const message = JSON.stringify({
          type: 'task_update',
          timestamp: sendTime,
          data: {
            task_id: Math.floor(Math.random() * 1000),
            status: 'running',
            progress: Math.random(),
          },
        });

        socket.send(message);
        messagesSent.add(1);
        messageCount++;

        // Track latency on response
        socket.on('message', (data) => {
          const receiveTime = Date.now();
          const latency = receiveTime - sendTime;
          messageLatency.add(latency);
          messagesReceived.add(1);

          check(data, {
            'Message received': (d) => d !== null && d !== undefined,
            'Latency < 100ms': () => latency < 100,
          });
        });
      }, 100); // 10 messages per second

      // Handle ping/pong for connection health
      socket.setInterval(() => {
        socket.ping();
      }, 30000); // Ping every 30 seconds
    });

    socket.on('error', (e) => {
      console.error('WebSocket error:', e);
      connectionErrors.add(1);
    });

    socket.on('close', () => {
      console.log('WebSocket connection closed');
    });

    // Keep connection alive for 10 seconds
    socket.setTimeout(() => {
      socket.close();
    }, 10000);
  });

  check(res, {
    'WebSocket connection successful': (r) => r && r.status === 101,
  });

  if (!res || res.status !== 101) {
    connectionErrors.add(1);
  }
}

/**
 * Teardown function
 */
export function teardown(data) {
  console.log('====================================');
  console.log('WebSocket Benchmark Summary');
  console.log('====================================');
  console.log(`Messages Sent: ${messagesSent.count}`);
  console.log(`Messages Received: ${messagesReceived.count}`);
  console.log(`Message Latency: P95=${messageLatency.p(95)}ms, P99=${messageLatency.p(99)}ms`);
  console.log(`Connection Error Rate: ${(connectionErrors.rate * 100).toFixed(2)}%`);
  console.log('====================================');
}
