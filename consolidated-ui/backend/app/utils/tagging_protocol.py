"""
Memory MCP Tagging Protocol
WHO/WHEN/PROJECT/WHY metadata for all memory_store operations

Implements mandatory tagging as per CLAUDE.md specification:
- WHO (agent_id, user_id, agent_category, capabilities)
- WHEN (ISO timestamp, Unix timestamp, readable format)
- PROJECT (project_id, project_name, task_id)
- WHY (intent: implementation/bugfix/refactor/testing/documentation/analysis/planning/research)
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, Literal
from enum import Enum
import uuid


class Intent(str, Enum):
    """Intent categories for Memory MCP operations"""
    IMPLEMENTATION = "implementation"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ANALYSIS = "analysis"
    PLANNING = "planning"
    RESEARCH = "research"


class AgentCategory(str, Enum):
    """Agent categories for WHO tagging"""
    CORE_DEVELOPMENT = "core-development"
    TESTING_VALIDATION = "testing-validation"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DOCUMENTATION = "documentation"
    SWARM_COORDINATION = "swarm-coordination"
    PERFORMANCE = "performance"
    SECURITY = "security"
    RESEARCH = "research"


class TaggingProtocol:
    """
    Memory MCP Tagging Protocol Implementation

    Automatically generates WHO/WHEN/PROJECT/WHY metadata for all memory operations.
    Ensures compliance with CLAUDE.md tagging requirements.
    """

    def __init__(
        self,
        agent_id: str,
        agent_category: AgentCategory,
        capabilities: list[str],
        project_id: str,
        project_name: str
    ):
        """
        Initialize tagging protocol for an agent

        Args:
            agent_id: Unique agent identifier
            agent_category: Agent category from AgentCategory enum
            capabilities: List of agent capabilities
            project_id: Project identifier
            project_name: Human-readable project name
        """
        self.agent_id = agent_id
        self.agent_category = agent_category
        self.capabilities = capabilities
        self.project_id = project_id
        self.project_name = project_name

    def generate_tags(
        self,
        intent: Intent,
        user_id: Optional[str] = None,
        task_id: Optional[str] = None,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate complete WHO/WHEN/PROJECT/WHY tags

        Args:
            intent: Intent category (implementation, bugfix, etc.)
            user_id: Optional user identifier
            task_id: Optional task identifier
            additional_metadata: Optional additional metadata to include

        Returns:
            Complete metadata dictionary with all required tags
        """
        now = datetime.now(timezone.utc)

        tags = {
            # WHO - Agent and user identification
            "who": {
                "agent_id": self.agent_id,
                "agent_category": self.agent_category.value,
                "capabilities": self.capabilities,
                "user_id": user_id or "system"
            },

            # WHEN - Temporal information
            "when": {
                "iso_timestamp": now.isoformat(),
                "unix_timestamp": int(now.timestamp()),
                "readable": now.strftime("%Y-%m-%d %H:%M:%S UTC")
            },

            # PROJECT - Project and task context
            "project": {
                "project_id": self.project_id,
                "project_name": self.project_name,
                "task_id": task_id or f"auto-{uuid.uuid4().hex[:8]}"
            },

            # WHY - Intent and purpose
            "why": {
                "intent": intent.value,
                "description": self._get_intent_description(intent)
            }
        }

        # Add any additional metadata
        if additional_metadata:
            tags["additional"] = additional_metadata

        return tags

    def _get_intent_description(self, intent: Intent) -> str:
        """Get human-readable description of intent"""
        descriptions = {
            Intent.IMPLEMENTATION: "Implementing new feature or functionality",
            Intent.BUGFIX: "Fixing bugs or errors in existing code",
            Intent.REFACTOR: "Refactoring code for better quality or performance",
            Intent.TESTING: "Writing or executing tests",
            Intent.DOCUMENTATION: "Creating or updating documentation",
            Intent.ANALYSIS: "Analyzing code, performance, or system behavior",
            Intent.PLANNING: "Planning architecture or approach",
            Intent.RESEARCH: "Researching solutions or best practices"
        }
        return descriptions.get(intent, "Unknown intent")

    def create_memory_store_payload(
        self,
        content: str,
        intent: Intent,
        user_id: Optional[str] = None,
        task_id: Optional[str] = None,
        additional_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create complete memory_store payload with tags

        Args:
            content: Content to store in memory
            intent: Intent category
            user_id: Optional user identifier
            task_id: Optional task identifier
            additional_metadata: Optional additional metadata

        Returns:
            Complete payload for memory_store operation
        """
        tags = self.generate_tags(intent, user_id, task_id, additional_metadata)

        return {
            "content": content,
            "metadata": tags,
            "timestamp": tags["when"]["unix_timestamp"]
        }


def create_backend_dev_tagger(
    project_id: str = "ruv-sparc-ui-dashboard",
    project_name: str = "RUV SPARC UI Dashboard"
) -> TaggingProtocol:
    """
    Create tagging protocol for backend development agent

    Args:
        project_id: Project identifier
        project_name: Human-readable project name

    Returns:
        TaggingProtocol instance configured for backend development
    """
    return TaggingProtocol(
        agent_id="backend-dev",
        agent_category=AgentCategory.BACKEND,
        capabilities=[
            "REST API development",
            "FastAPI",
            "PostgreSQL",
            "Redis",
            "Circuit breaker patterns",
            "Memory MCP integration"
        ],
        project_id=project_id,
        project_name=project_name
    )


# Example usage for P2_T4
if __name__ == "__main__":
    # Create tagger for this task
    tagger = create_backend_dev_tagger()

    # Generate tags for implementation intent
    payload = tagger.create_memory_store_payload(
        content="Implemented Memory MCP client with circuit breaker",
        intent=Intent.IMPLEMENTATION,
        task_id="P2_T4",
        additional_metadata={
            "features": ["circuit_breaker", "fallback_mode", "tagging_protocol"],
            "dependencies": ["P1_T5", "P2_T1"],
            "deliverables": [
                "memory_mcp_client.py",
                "tagging_protocol.py",
                "fallback_mode_tests.py",
                "vector_search_api.py"
            ]
        }
    )

    print("Generated Memory MCP payload:")
    import json
    print(json.dumps(payload, indent=2))
