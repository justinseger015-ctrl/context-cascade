"""
WebSocket Load Testing Script
Tests WebSocket with 45-50k concurrent connections
"""

import asyncio
import websockets
import json
import time
import statistics
from typing import List, Dict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketLoadTester:
    """Load tester for WebSocket connections"""

    def __init__(
        self,
        url: str,
        token: str,
        num_connections: int = 50000,
        connection_rate: int = 1000,  # Connections per second
        duration: int = 300,  # 5 minutes
    ):
        """
        Initialize load tester

        Args:
            url: WebSocket URL (ws:// or wss://)
            token: JWT authentication token
            num_connections: Total connections to create
            connection_rate: Connections to create per second
            duration: Test duration in seconds
        """
        self.url = url
        self.token = token
        self.num_connections = num_connections
        self.connection_rate = connection_rate
        self.duration = duration

        self.connections: List[websockets.WebSocketClientProtocol] = []
        self.connection_times: List[float] = []
        self.message_latencies: List[float] = []
        self.errors: List[str] = []

        self.connected_count = 0
        self.message_count = 0
        self.start_time = None

    async def create_connection(self, connection_id: int) -> bool:
        """
        Create a single WebSocket connection

        Args:
            connection_id: Connection identifier

        Returns:
            True if successful, False otherwise
        """
        try:
            start = time.time()

            # Build WebSocket URL with token
            ws_url = f"{self.url}?token={self.token}"

            # Connect
            ws = await websockets.connect(ws_url)

            connection_time = time.time() - start
            self.connection_times.append(connection_time)

            self.connections.append(ws)
            self.connected_count += 1

            # Start listening for messages
            asyncio.create_task(self.listen_for_messages(ws, connection_id))

            if self.connected_count % 1000 == 0:
                logger.info(f"Connected: {self.connected_count}/{self.num_connections}")

            return True

        except Exception as e:
            self.errors.append(f"Connection {connection_id} failed: {str(e)}")
            return False

    async def listen_for_messages(
        self,
        ws: websockets.WebSocketClientProtocol,
        connection_id: int
    ):
        """
        Listen for messages on a WebSocket connection

        Args:
            ws: WebSocket connection
            connection_id: Connection identifier
        """
        try:
            async for message in ws:
                try:
                    data = json.loads(message)
                    message_type = data.get("type")

                    # Respond to ping
                    if message_type == "ping":
                        pong = {
                            "type": "pong",
                            "event_id": f"pong_{connection_id}_{time.time()}",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        await ws.send(json.dumps(pong))

                    # Track message latency
                    if "timestamp" in data:
                        sent_time = datetime.fromisoformat(
                            data["timestamp"].replace("Z", "+00:00")
                        )
                        latency = (datetime.utcnow() - sent_time.replace(tzinfo=None)).total_seconds()
                        self.message_latencies.append(latency)

                    self.message_count += 1

                except json.JSONDecodeError:
                    pass

        except websockets.exceptions.ConnectionClosed:
            pass
        except Exception as e:
            self.errors.append(f"Listen error {connection_id}: {str(e)}")

    async def run_load_test(self):
        """Run the load test"""
        logger.info(f"Starting load test: {self.num_connections} connections")
        self.start_time = time.time()

        # Create connections at specified rate
        batch_size = self.connection_rate
        total_batches = (self.num_connections + batch_size - 1) // batch_size

        for batch in range(total_batches):
            batch_start = batch * batch_size
            batch_end = min((batch + 1) * batch_size, self.num_connections)

            # Create batch of connections concurrently
            tasks = [
                self.create_connection(i)
                for i in range(batch_start, batch_end)
            ]

            await asyncio.gather(*tasks, return_exceptions=True)

            # Wait 1 second between batches to maintain rate
            if batch < total_batches - 1:
                await asyncio.sleep(1)

        logger.info(f"All connections created: {self.connected_count}/{self.num_connections}")

        # Keep connections alive for duration
        logger.info(f"Maintaining connections for {self.duration} seconds...")
        await asyncio.sleep(self.duration)

        # Close all connections
        logger.info("Closing connections...")
        close_tasks = [ws.close() for ws in self.connections]
        await asyncio.gather(*close_tasks, return_exceptions=True)

        # Generate report
        self.generate_report()

    def generate_report(self):
        """Generate test report"""
        total_time = time.time() - self.start_time

        logger.info("\n" + "=" * 60)
        logger.info("LOAD TEST REPORT")
        logger.info("=" * 60)

        logger.info(f"\nConnections:")
        logger.info(f"  Total Attempted: {self.num_connections}")
        logger.info(f"  Successfully Connected: {self.connected_count}")
        logger.info(f"  Failed: {self.num_connections - self.connected_count}")
        logger.info(f"  Success Rate: {(self.connected_count / self.num_connections) * 100:.2f}%")

        if self.connection_times:
            logger.info(f"\nConnection Times:")
            logger.info(f"  Mean: {statistics.mean(self.connection_times):.3f}s")
            logger.info(f"  Median: {statistics.median(self.connection_times):.3f}s")
            logger.info(f"  Min: {min(self.connection_times):.3f}s")
            logger.info(f"  Max: {max(self.connection_times):.3f}s")
            logger.info(f"  StdDev: {statistics.stdev(self.connection_times):.3f}s")

        logger.info(f"\nMessages:")
        logger.info(f"  Total Received: {self.message_count}")
        logger.info(f"  Messages/Second: {self.message_count / total_time:.2f}")

        if self.message_latencies:
            logger.info(f"\nMessage Latencies:")
            logger.info(f"  Mean: {statistics.mean(self.message_latencies) * 1000:.2f}ms")
            logger.info(f"  Median: {statistics.median(self.message_latencies) * 1000:.2f}ms")
            logger.info(f"  Min: {min(self.message_latencies) * 1000:.2f}ms")
            logger.info(f"  Max: {max(self.message_latencies) * 1000:.2f}ms")

        logger.info(f"\nErrors:")
        logger.info(f"  Total Errors: {len(self.errors)}")
        if self.errors:
            logger.info(f"  Sample Errors:")
            for error in self.errors[:10]:  # Show first 10 errors
                logger.info(f"    - {error}")

        logger.info(f"\nTest Duration: {total_time:.2f}s")
        logger.info("=" * 60)


async def main():
    """Main entry point"""
    # Configuration
    WS_URL = "ws://localhost:8000/ws"  # Change to wss:// for production
    JWT_TOKEN = "your-test-jwt-token"  # Get from authentication

    # Test configurations
    TESTS = [
        {"connections": 1000, "rate": 500, "duration": 60, "name": "Small Load (1k)"},
        {"connections": 10000, "rate": 1000, "duration": 180, "name": "Medium Load (10k)"},
        {"connections": 50000, "rate": 1000, "duration": 300, "name": "Target Load (50k)"},
    ]

    for test_config in TESTS:
        logger.info(f"\n\nRunning test: {test_config['name']}")

        tester = WebSocketLoadTester(
            url=WS_URL,
            token=JWT_TOKEN,
            num_connections=test_config["connections"],
            connection_rate=test_config["rate"],
            duration=test_config["duration"],
        )

        await tester.run_load_test()

        # Wait between tests
        logger.info("\nWaiting 30s before next test...")
        await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())
