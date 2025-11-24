"""
Utils package for RUV SPARC UI Dashboard

Provides:
- Memory MCP client with circuit breaker
- WHO/WHEN/PROJECT/WHY tagging protocol
- Vector search API
- Fallback mechanisms
"""

from .memory_mcp_client import MemoryMCPClient, create_memory_mcp_client
from .tagging_protocol import TaggingProtocol, Intent, AgentCategory, create_backend_dev_tagger
from .vector_search_api import router as memory_router

__all__ = [
    "MemoryMCPClient",
    "create_memory_mcp_client",
    "TaggingProtocol",
    "Intent",
    "AgentCategory",
    "create_backend_dev_tagger",
    "memory_router"
]
