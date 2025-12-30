"""
loopctl CLI entry point.

Usage:
    python -m loopctl ralph_iteration_complete --state <statefile> --loop-dir .loop
    python -m loopctl status --loop-dir .loop
    python -m loopctl reset --loop-dir .loop
"""

import argparse
import json
import sys
from pathlib import Path

from .core import ralph_iteration_complete, get_status, reset_loop


def main():
    parser = argparse.ArgumentParser(
        description="loopctl - Single Authority for Loop Control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Process Ralph iteration completion
    python -m loopctl ralph_iteration_complete --state .claude/ralph-loop.local.md --loop-dir .loop

    # Get current status
    python -m loopctl status --loop-dir .loop

    # Reset loop state
    python -m loopctl reset --loop-dir .loop
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # ralph_iteration_complete command
    ralph_parser = subparsers.add_parser(
        "ralph_iteration_complete",
        help="Process a Ralph iteration completion",
    )
    ralph_parser.add_argument(
        "--state",
        required=True,
        help="Path to Ralph state file",
    )
    ralph_parser.add_argument(
        "--loop-dir",
        required=True,
        help="Path to .loop/ directory",
    )
    ralph_parser.add_argument(
        "--output",
        help="Path to artifact output file",
    )
    ralph_parser.add_argument(
        "--iteration",
        type=int,
        help="Iteration number (reads from state if not provided)",
    )

    # status command
    status_parser = subparsers.add_parser(
        "status",
        help="Show current loop status",
    )
    status_parser.add_argument(
        "--loop-dir",
        required=True,
        help="Path to .loop/ directory",
    )

    # reset command
    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset loop state to defaults",
    )
    reset_parser.add_argument(
        "--loop-dir",
        required=True,
        help="Path to .loop/ directory",
    )

    args = parser.parse_args()

    if args.command == "ralph_iteration_complete":
        result = ralph_iteration_complete(
            state_path=args.state,
            loop_dir=args.loop_dir,
            output_path=args.output,
            iteration=args.iteration,
        )
        print(json.dumps(result))

    elif args.command == "status":
        result = get_status(args.loop_dir)
        print(json.dumps(result, indent=2))

    elif args.command == "reset":
        result = reset_loop(args.loop_dir)
        print(json.dumps(result, indent=2))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
