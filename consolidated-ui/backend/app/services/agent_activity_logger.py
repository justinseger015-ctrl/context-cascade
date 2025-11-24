"""
Agent Activity Logger
Logs agent activity to PostgreSQL + Memory MCP with WebSocket broadcasting
Implements circuit breaker pattern for Memory MCP resilience
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.agent import AgentCRUD
from app.crud.execution_result import ExecutionResultCRUD
from app.utils.memory_mcp_client import MemoryMCPClient
from app.utils.tagging_protocol import Intent
from app.websocket.connection_manager import connection_manager
from app.websocket.message_types import WSMessage, MessageType

logger = logging.getLogger(__name__)


class AgentActivityLogger:
    """
    Agent activity logger with triple-redundancy storage:
    1. PostgreSQL (execution_results table)
    2. Memory MCP (with WHO/WHEN/PROJECT/WHY tagging)
    3. Redis cache (via Memory MCP client)

    Features:
    - Circuit breaker for Memory MCP queries
    - WebSocket broadcasting to all connected clients
    - Automatic agent status updates
    - Execution metrics calculation
    """

    def __init__(
        self,
        db_session: AsyncSession,
        memory_client: Optional[MemoryMCPClient] = None
    ):
        """
        Initialize activity logger

        Args:
            db_session: SQLAlchemy async session
            memory_client: Memory MCP client with circuit breaker
        """
        self.db_session = db_session
        self.memory_client = memory_client
        self.agent_crud = AgentCRUD(db_session)
        self.execution_crud = ExecutionResultCRUD(db_session)

    async def log_activity(
        self,
        agent_id: int,
        task_id: int,
        status: str,
        output: Optional[str] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Log agent activity across all storage systems and broadcast via WebSocket

        Args:
            agent_id: Agent ID
            task_id: Task ID being executed
            status: Execution status (running, success, failed, timeout)
            output: Execution output
            error: Error message if failed
            duration_ms: Execution duration in milliseconds
            user_id: User ID for audit logging
            ip_address: IP address for audit logging

        Returns:
            Dictionary with storage and broadcast status
        """
        now = datetime.utcnow()

        # Step 1: Update agent status and last_active_at
        agent_status = self._map_execution_status_to_agent_status(status)
        await self.agent_crud.update_activity(agent_id, status=agent_status)

        logger.info(
            f"Agent activity: agent_id={agent_id}, task_id={task_id}, "
            f"status={status}, duration={duration_ms}ms"
        )

        # Step 2: Store in PostgreSQL execution_results
        execution_data = {
            "task_id": task_id,
            "started_at": now if status == "running" else now,
            "ended_at": now if status != "running" else None,
            "status": status,
            "output_text": output,
            "error_text": error,
        }

        # Calculate duration if not provided
        if status != "running" and duration_ms is None and execution_data.get("ended_at"):
            delta = execution_data["ended_at"] - execution_data["started_at"]
            duration_ms = int(delta.total_seconds() * 1000)

        execution_result = await self.execution_crud.create(
            **execution_data,
            user_id=user_id,
            ip_address=ip_address
        )

        stored_in_memory = False
        memory_error = None

        # Step 3: Store in Memory MCP (with circuit breaker)
        if self.memory_client:
            try:
                content = self._create_memory_content(
                    agent_id=agent_id,
                    task_id=task_id,
                    status=status,
                    output=output,
                    error=error,
                    duration_ms=duration_ms
                )

                intent = self._determine_intent_from_status(status)

                memory_result = await self.memory_client.store(
                    content=content,
                    intent=intent,
                    user_id=user_id or "system",
                    task_id=str(task_id),
                    additional_metadata={
                        "agent_id": agent_id,
                        "execution_result_id": execution_result.id,
                        "status": status,
                        "duration_ms": duration_ms
                    }
                )

                stored_in_memory = memory_result.get("status") == "success"

                logger.info(
                    f"Memory MCP storage: status={memory_result.get('status')}, "
                    f"storage={memory_result.get('storage')}"
                )

            except Exception as e:
                memory_error = str(e)
                logger.warning(f"Failed to store in Memory MCP: {e}")
                # Continue execution - PostgreSQL storage succeeded

        # Step 4: Broadcast via WebSocket to all connected clients
        broadcasted = await self._broadcast_activity_update(
            agent_id=agent_id,
            task_id=task_id,
            status=status,
            output=output,
            error=error,
            duration_ms=duration_ms
        )

        # Commit database transaction
        await self.db_session.commit()

        return {
            "status": "success",
            "agent_id": agent_id,
            "task_id": task_id,
            "execution_result_id": execution_result.id,
            "stored_in_postgresql": True,
            "stored_in_memory_mcp": stored_in_memory,
            "broadcasted_via_websocket": broadcasted,
            "memory_mcp_error": memory_error,
            "timestamp": now.isoformat()
        }

    async def _broadcast_activity_update(
        self,
        agent_id: int,
        task_id: int,
        status: str,
        output: Optional[str] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None
    ) -> bool:
        """
        Broadcast agent activity update to all connected WebSocket clients

        Args:
            agent_id: Agent ID
            task_id: Task ID
            status: Execution status
            output: Execution output (truncated for WebSocket)
            error: Error message (truncated for WebSocket)
            duration_ms: Execution duration

        Returns:
            True if broadcast successful, False otherwise
        """
        try:
            # Create WebSocket message
            message = WSMessage(
                type=MessageType.AGENT_ACTIVITY_UPDATE,
                data={
                    "agent_id": agent_id,
                    "task_id": task_id,
                    "status": status,
                    "output": self._truncate_text(output, max_length=1000),
                    "error": self._truncate_text(error, max_length=500),
                    "duration_ms": duration_ms,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )

            # Broadcast to all connected clients
            await connection_manager.broadcast(message)

            logger.debug(f"Broadcasted agent activity update: agent_id={agent_id}, task_id={task_id}")

            return True

        except Exception as e:
            logger.error(f"Failed to broadcast activity update: {e}")
            return False

    def _map_execution_status_to_agent_status(self, execution_status: str) -> str:
        """
        Map execution status to agent status

        Args:
            execution_status: Execution status (running, success, failed, timeout)

        Returns:
            Agent status (active, idle, busy, error)
        """
        mapping = {
            "running": "busy",
            "success": "idle",
            "failed": "error",
            "timeout": "error",
            "cancelled": "idle"
        }
        return mapping.get(execution_status, "idle")

    def _determine_intent_from_status(self, status: str) -> Intent:
        """
        Determine Memory MCP intent from execution status

        Args:
            status: Execution status

        Returns:
            Intent enum value
        """
        if status == "success":
            return Intent.IMPLEMENTATION
        elif status in ["failed", "timeout"]:
            return Intent.BUGFIX
        elif status == "running":
            return Intent.TESTING
        else:
            return Intent.ANALYSIS

    def _create_memory_content(
        self,
        agent_id: int,
        task_id: int,
        status: str,
        output: Optional[str] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None
    ) -> str:
        """
        Create structured content for Memory MCP storage

        Args:
            agent_id: Agent ID
            task_id: Task ID
            status: Execution status
            output: Execution output
            error: Error message
            duration_ms: Duration in milliseconds

        Returns:
            Formatted content string
        """
        parts = [
            f"Agent {agent_id} executed task {task_id}",
            f"Status: {status}",
        ]

        if duration_ms is not None:
            parts.append(f"Duration: {duration_ms}ms")

        if output:
            # Truncate output for storage
            truncated_output = self._truncate_text(output, max_length=2000)
            parts.append(f"Output: {truncated_output}")

        if error:
            # Truncate error for storage
            truncated_error = self._truncate_text(error, max_length=1000)
            parts.append(f"Error: {truncated_error}")

        return " | ".join(parts)

    @staticmethod
    def _truncate_text(text: Optional[str], max_length: int = 1000) -> Optional[str]:
        """
        Truncate text to maximum length with ellipsis

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            Truncated text or None
        """
        if not text:
            return None

        if len(text) <= max_length:
            return text

        return text[:max_length - 3] + "..."
