#!/bin/bash
# Post-Task Hook: Memory Store Reminder
# Fires after Task() to remind agents to store results

cat << 'MEMORY_STORE'
!! MEMORY-MCP: POST-TASK STORE !!

AFTER completing this task, STORE in memory:

IF task found issues:
  kv.set_json("findings:{agent}:{severity}:{id}", {
    "WHO": "{agent-type}:{id}",
    "WHEN": datetime.now().isoformat(),
    "PROJECT": "{project}",
    "WHY": "analysis",
    ...finding details...
  })

IF task applied fixes:
  kv.set_json("fixes:{agent}:{finding-id}", {
    "WHO": "{agent-type}:{id}",
    "WHEN": datetime.now().isoformat(),
    "PROJECT": "{project}",
    "WHY": "bugfix",
    ...fix details...
  })
  graph.add_relationship("fix:{id}", "resolves", "finding:{id}")

IF task made decisions:
  kv.set_json("decisions:{project}:{decision-id}", {
    "WHO": "{agent-type}:{id}",
    "WHEN": datetime.now().isoformat(),
    "PROJECT": "{project}",
    "WHY": "planning",
    ...decision rationale...
  })

IF task learned something new:
  kv.set_json("expertise:{domain}:{topic}", {
    "WHO": "{agent-type}:{id}",
    "WHEN": datetime.now().isoformat(),
    "PROJECT": "{project}",
    "WHY": "documentation",
    ...knowledge...
  })

ALWAYS: Use WHO/WHEN/PROJECT/WHY tags!
MEMORY_STORE
