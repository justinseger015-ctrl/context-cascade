#!/bin/bash
# Pre-Task Hook: Memory Check Reminder
# Fires before Task() to remind agents to check memory

cat << 'MEMORY_REMINDER'
!! MEMORY-MCP: PRE-TASK CHECK !!

BEFORE starting this task, CHECK MEMORY for:
  1. Prior work on this topic: kv.list_keys("findings:{domain}:")
  2. Known issues: kv.list_keys("findings:*:high:")
  3. Fix patterns: graph.get_subgraph("{pattern}", depth=2)
  4. Previous decisions: kv.list_keys("decisions:{project}:")

QUERY PATTERNS:
  - "What was done before?" -> Check KV store
  - "Are there related issues?" -> Query graph relationships
  - "What patterns worked?" -> Search expertise namespace

REMEMBER: Agents share memory. Check what others have stored.
MEMORY_REMINDER
