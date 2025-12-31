#!/bin/bash
# Memory Trigger Patterns
# Reference for when to READ vs WRITE memory

cat << 'TRIGGERS'
!! MEMORY-MCP: TRIGGER PATTERNS !!

=== WHEN TO READ MEMORY ===

TASK START:
  - Check "expertise:{domain}:" for domain knowledge
  - Check "findings:*:" for known issues
  - Check "fixes:*:" for proven solutions

ERROR ENCOUNTERED:
  - Search "findings:*:high:" for similar errors
  - Query graph for error -> fix paths

BEFORE CODING:
  - Check "expertise:patterns:" for established patterns
  - Search for similar implementations

ARCHITECTURAL DECISION:
  - Check "decisions:{project}:" for precedents
  - Query graph for architectural relationships

=== WHEN TO WRITE MEMORY ===

TASK COMPLETE (success):
  - Store in "agents:{category}:{type}:{project}:{timestamp}"
  - Add to graph if created entities/relationships

ISSUE FOUND:
  - Store in "findings:{agent}:{severity}:{id}"
  - Link to fix patterns in graph

BUG FIXED:
  - Store in "fixes:{agent}:{finding-id}"
  - Update finding status
  - Add graph: fix --resolves--> finding

DECISION MADE:
  - Store in "decisions:{project}:{id}"
  - Include rationale and alternatives considered

KNOWLEDGE GAINED:
  - Store in "expertise:{domain}:{topic}"
  - Build graph relationships

=== TERMINAL COMMANDS ===

# Quick memory check
python -c "
import sys; sys.path.insert(0, r'D:\\Projects\\memory-mcp-triple-system')
from src.stores.kv_store import KVStore
kv = KVStore(r'C:\\Users\\17175\\.claude\\memory-mcp-data\\agent_kv.db')
print('Keys:', kv.list_keys(''))
kv.close()
"

# Query graph
python -c "
import sys; sys.path.insert(0, r'D:\\Projects\\memory-mcp-triple-system')
from src.services.graph_service import GraphService
g = GraphService(data_dir=r'C:\\Users\\17175\\.claude\\memory-mcp-data')
g.load_graph()
print(f'Nodes: {g.get_node_count()}, Edges: {g.get_edge_count()}')
"
TRIGGERS
