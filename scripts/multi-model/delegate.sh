#!/usr/bin/env bash
# delegate.sh - Drop-in wrapper to invoke Codex CLI or Gemini CLI reliably from Claude Code
#
# CRITICAL: This wrapper solves the PATH mismatch problem where Claude Code
# runs in a non-interactive shell that can't find your installed binaries.
#
# Goals:
#  - Hard-check PATH (no reinstall attempts)
#  - Capture stdout/stderr cleanly to files + echo a stable summary
#  - Prevent reinstall loops (fail fast if binary missing)
#  - Optionally force `codex exec --json` for deterministic parsing (JSONL)
#
# Usage:
#   ./delegate.sh codex  "Prompt text here"              [--json] [--model MODEL] [--cwd /path] [--outdir /path]
#   ./delegate.sh gemini "Prompt text here"              [--cwd /path] [--outdir /path] [--args "...extra flags..."]
#   ./delegate.sh codex  --raw "codex --help"            [--cwd ...] [--outdir ...]
#   ./delegate.sh gemini --raw "gemini /help"            [--cwd ...] [--outdir ...]
#
# Exit codes:
#  0  success
#  10 binary missing
#  11 bad usage
#  12 command failed (non-zero)
#  13 install attempt blocked

set -euo pipefail

SELF="$(basename "$0")"

usage() {
  cat <<'EOF'
delegate.sh - invoke Codex or Gemini in a deterministic, Claude-friendly way.

USAGE
  delegate.sh codex  "PROMPT" [--json] [--model NAME] [--yolo] [--full-auto] [--cwd PATH] [--outdir PATH] [--timeout SEC]
  delegate.sh gemini "PROMPT" [--all-files] [--cwd PATH] [--outdir PATH] [--timeout SEC] [--args "EXTRA FLAGS"]
  delegate.sh codex  --raw "SHELL_COMMAND" [--cwd PATH] [--outdir PATH] [--timeout SEC]
  delegate.sh gemini --raw "SHELL_COMMAND" [--cwd PATH] [--outdir PATH] [--timeout SEC]

OPTIONS
  --json            (codex only) force: codex exec --json "PROMPT"
  --model NAME      (codex only) set model (e.g., gpt-5.2-codex)
  --yolo            (codex only) bypass approvals and sandbox
  --full-auto       (codex only) autonomous mode with workspace write
  --all-files       (gemini only) analyze entire codebase with 1M context
  --cwd PATH        run command in this directory (default: current)
  --outdir PATH     directory for logs (default: ./.delegate-logs)
  --timeout SEC     optional timeout (default: none)
  --args "..."      (gemini only) extra flags passed to gemini
  --raw "..."       run the exact shell command (still with PATH hard-check)

EXAMPLES
  # Codex: fix tests autonomously
  delegate.sh codex "Fix all failing tests" --full-auto

  # Codex: get JSON output for parsing
  delegate.sh codex "List all API endpoints" --json

  # Gemini: analyze entire codebase
  delegate.sh gemini "Map the full architecture" --all-files

  # Gemini: research with Google Search grounding
  delegate.sh gemini "What are React 19 best practices?"
EOF
}

# ---- defaults
MODE=""
PROMPT=""
RAW_CMD=""
FORCE_JSON="0"
MODEL=""
YOLO_FLAG=""
FULL_AUTO_FLAG=""
ALL_FILES_FLAG=""
CWD="$(pwd)"
OUTDIR="$(pwd)/.delegate-logs"
TIMEOUT=""
EXTRA_ARGS=""

# ---- parse
if [[ $# -lt 2 ]]; then usage; exit 11; fi
MODE="$1"; shift

if [[ "$1" == "--raw" ]]; then
  shift
  [[ $# -ge 1 ]] || { echo "ERROR: --raw requires a command string" >&2; exit 11; }
  RAW_CMD="$1"; shift
else
  PROMPT="$1"; shift
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) FORCE_JSON="1"; shift ;;
    --model) MODEL="${2:-}"; shift 2 ;;
    --yolo) YOLO_FLAG="--yolo"; shift ;;
    --full-auto) FULL_AUTO_FLAG="--full-auto"; shift ;;
    --all-files) ALL_FILES_FLAG="--all-files"; shift ;;
    --cwd) CWD="${2:-}"; shift 2 ;;
    --outdir) OUTDIR="${2:-}"; shift 2 ;;
    --timeout) TIMEOUT="${2:-}"; shift 2 ;;
    --args) EXTRA_ARGS="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "ERROR: Unknown arg: $1" >&2; usage; exit 11 ;;
  esac
done

if [[ "$MODE" != "codex" && "$MODE" != "gemini" ]]; then
  echo "ERROR: First arg must be 'codex' or 'gemini'" >&2
  exit 11
fi

# ---- helpers
ts() { date -u +"%Y%m%dT%H%M%SZ"; }
rand() { LC_ALL=C tr -dc 'a-z0-9' </dev/urandom 2>/dev/null | head -c 8 || echo "$(date +%s)"; }

RUN_ID="$(ts)_$(rand)"
mkdir -p "$OUTDIR"

STDOUT_FILE="$OUTDIR/${MODE}_${RUN_ID}.stdout"
STDERR_FILE="$OUTDIR/${MODE}_${RUN_ID}.stderr"
META_FILE="$OUTDIR/${MODE}_${RUN_ID}.meta.json"

# Run via login shell for consistent PATH
run_login_shell() {
  local cmd="$1"
  if [[ -n "$TIMEOUT" ]]; then
    if command -v timeout >/dev/null 2>&1; then
      bash -lc "cd \"${CWD}\" && timeout ${TIMEOUT} ${cmd}"
    elif command -v gtimeout >/dev/null 2>&1; then
      bash -lc "cd \"${CWD}\" && gtimeout ${TIMEOUT} ${cmd}"
    else
      bash -lc "cd \"${CWD}\" && ${cmd}"
    fi
  else
    bash -lc "cd \"${CWD}\" && ${cmd}"
  fi
}

# CRITICAL: Hard-check that binary exists in login shell PATH
hard_check_binary() {
  local bin="$1"
  echo "[delegate] Checking for '$bin' in login shell PATH..."
  if ! bash -lc "command -v \"$bin\" >/dev/null 2>&1"; then
    echo "ERROR: '$bin' not found on PATH in login shell context." >&2
    echo "DEBUG: PATH=$(bash -lc 'echo $PATH' | head -c 500)" >&2
    echo "" >&2
    echo "SOLUTION: Install '$bin' manually. Do NOT let Claude install it." >&2
    echo "  For codex: npm install -g @openai/codex" >&2
    echo "  For gemini: npm install -g @google/gemini-cli" >&2
    exit 10
  fi
  echo "[delegate] Found: $(bash -lc "command -v \"$bin\"")"
  echo "[delegate] Version: $(bash -lc "$bin --version" 2>&1 | head -1)"
}

json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1" 2>/dev/null || \
  python -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1" 2>/dev/null || \
  echo "\"$1\""
}

# ---- CRITICAL: Prevent reinstall loops
if [[ -n "$RAW_CMD" ]]; then
  # Block any install/upgrade commands
  if echo "$RAW_CMD" | grep -qiE '(npm[[:space:]]+(install|i[[:space:]])|brew[[:space:]]+install|pip[[:space:]]+install|pnpm[[:space:]]+add|yarn[[:space:]]+add|curl[[:space:]].*\|[[:space:]]*bash|winget[[:space:]]+install)'; then
    echo "ERROR: Raw command appears to be an install/upgrade attempt; blocked by policy." >&2
    echo "REASON: CLIs are already installed. Claude should NEVER reinstall them." >&2
    exit 13
  fi
fi

# ---- hard-check binary exists
hard_check_binary "$MODE"

# ---- build command
CMD=""
if [[ -n "$RAW_CMD" ]]; then
  CMD="$RAW_CMD"
else
  if [[ "$MODE" == "codex" ]]; then
    # Build codex command
    CMD="codex"

    # Add model if specified
    [[ -n "$MODEL" ]] && CMD="$CMD --model $MODEL"

    # Add mode flags
    [[ -n "$YOLO_FLAG" ]] && CMD="$CMD $YOLO_FLAG"
    [[ -n "$FULL_AUTO_FLAG" ]] && CMD="$CMD $FULL_AUTO_FLAG"

    # For non-interactive use, prefer exec mode
    if [[ "$FORCE_JSON" == "1" ]]; then
      CMD="$CMD exec --json"
    else
      CMD="$CMD exec"
    fi

    # Add the prompt (properly escaped)
    CMD="$CMD $(printf "%q" "$PROMPT")"

  else
    # Gemini command
    CMD="gemini"

    # Add all-files flag if specified
    [[ -n "$ALL_FILES_FLAG" ]] && CMD="$CMD $ALL_FILES_FLAG"

    # Add extra args
    [[ -n "$EXTRA_ARGS" ]] && CMD="$CMD $EXTRA_ARGS"

    # For non-interactive, pipe the prompt
    # Using printf to handle special characters
    CMD="printf '%s' $(printf "%q" "$PROMPT") | $CMD"
  fi
fi

# ---- execute + capture
echo "[delegate] Executing: $CMD"
echo "[delegate] CWD: $CWD"
echo "[delegate] Run ID: $RUN_ID"
echo "---"

set +e
run_login_shell "$CMD" >"$STDOUT_FILE" 2>"$STDERR_FILE"
RC=$?
set -e

# ---- write metadata (JSON)
cat >"$META_FILE" <<EOF
{
  "run_id": "$RUN_ID",
  "mode": "$MODE",
  "cwd": "$CWD",
  "outdir": "$OUTDIR",
  "command": $(json_escape "$CMD"),
  "prompt": $(json_escape "${PROMPT:-}"),
  "raw_command": $(json_escape "${RAW_CMD:-}"),
  "stdout_file": "$(basename "$STDOUT_FILE")",
  "stderr_file": "$(basename "$STDERR_FILE")",
  "exit_code": $RC,
  "timestamp": "$(date -Iseconds)"
}
EOF

# ---- user-facing summary (stable and parseable)
echo ""
echo "DELEGATE_RUN_ID=$RUN_ID"
echo "DELEGATE_MODE=$MODE"
echo "DELEGATE_CWD=$CWD"
echo "DELEGATE_EXIT_CODE=$RC"
echo "DELEGATE_STDOUT_FILE=$STDOUT_FILE"
echo "DELEGATE_STDERR_FILE=$STDERR_FILE"
echo "DELEGATE_META_FILE=$META_FILE"

# Show output summary
echo ""
echo "--- STDOUT (first 100 lines) ---"
head -100 "$STDOUT_FILE" 2>/dev/null || echo "(empty)"

if [[ -s "$STDERR_FILE" ]]; then
  echo ""
  echo "--- STDERR ---"
  cat "$STDERR_FILE"
fi

# ---- fail if command failed (but logs are preserved)
if [[ $RC -ne 0 ]]; then
  echo ""
  echo "ERROR: '$MODE' invocation failed with exit code $RC" >&2
  echo "See full logs at: $STDOUT_FILE and $STDERR_FILE" >&2
  exit 12
fi

echo ""
echo "[delegate] SUCCESS"
exit 0
