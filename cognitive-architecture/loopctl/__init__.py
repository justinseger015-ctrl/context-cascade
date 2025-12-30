"""
loopctl - Single Authority for Loop Control

This CLI is the single throat to choke for Ralph loop decisions.
The stop-hook calls loopctl, not the other way around.

Usage:
    python -m loopctl ralph_iteration_complete --state <statefile> --loop-dir .loop

Commands:
    ralph_iteration_complete  - Process a Ralph iteration completion
    status                    - Show current loop status
    reset                     - Reset loop state
"""

from .core import ralph_iteration_complete, get_status, reset_loop

__all__ = ["ralph_iteration_complete", "get_status", "reset_loop"]
