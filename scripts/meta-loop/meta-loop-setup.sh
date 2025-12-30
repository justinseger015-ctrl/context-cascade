#!/bin/bash
# meta-loop-setup.sh
# PURPOSE: Initialize a Meta Loop cycle with sequential Ralph phases
#
# IMPORTANT: Ralph loops are SEQUENTIAL, not parallel!
# The Stop hook (quality-gate-stop-hook.sh) uses a SINGLE state file.
# This script manages the meta-loop state and starts Ralph loops for each phase.
#
# Usage: bash meta-loop-setup.sh start "<task>" --target "<file>" --foundry "<skill>"
#        bash meta-loop-setup.sh phase "<phase_name>" "<prompt>" --promise "<text>"
#        bash meta-loop-setup.sh status
#        bash meta-loop-setup.sh cancel

set -euo pipefail

# Directories
RALPH_DIR="${HOME}/.claude/ralph-wiggum"
META_DIR="${RALPH_DIR}/meta-loop"
RALPH_STATE="${RALPH_DIR}/loop-state.md"
META_STATE="${META_DIR}/state.yaml"
SESSIONS_DIR="${META_DIR}/sessions"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[META-LOOP]${NC} $1"; }
log_success() { echo -e "${GREEN}[META-LOOP]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[META-LOOP]${NC} $1"; }
log_error() { echo -e "${RED}[META-LOOP]${NC} $1"; }
log_phase() { echo -e "${CYAN}[PHASE]${NC} $1"; }

# Ensure directories exist
mkdir -p "$RALPH_DIR" "$META_DIR" "$SESSIONS_DIR"

# Generate session ID
generate_session_id() {
    echo "meta-$(date +%Y%m%d-%H%M%S)-$$"
}

# ============================================================
# COMMAND: start
# Initialize a new meta loop
# ============================================================
cmd_start() {
    local task=""
    local target=""
    local foundry=""
    local max_iterations=30

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --target) target="$2"; shift 2 ;;
            --foundry) foundry="$2"; shift 2 ;;
            --max-iterations) max_iterations="$2"; shift 2 ;;
            *)
                if [[ -z "$task" ]]; then
                    task="$1"
                fi
                shift
                ;;
        esac
    done

    # Validate
    if [[ -z "$task" ]] || [[ -z "$target" ]] || [[ -z "$foundry" ]]; then
        log_error "Usage: $0 start \"<task>\" --target <file> --foundry <skill>"
        log_error "Foundry must be: agent-creator, skill-forge, or prompt-forge"
        exit 1
    fi

    if [[ ! "$foundry" =~ ^(agent-creator|skill-forge|prompt-forge)$ ]]; then
        log_error "Invalid foundry: $foundry"
        log_error "Must be: agent-creator, skill-forge, or prompt-forge"
        exit 1
    fi

    local session_id=$(generate_session_id)

    # Create meta loop state
    cat > "$META_STATE" << EOF
---
session_id: $session_id
active: true
started_at: $(date -Iseconds 2>/dev/null || date +%Y-%m-%dT%H:%M:%S)
task: "$task"
target: "$target"
foundry_skill: $foundry
max_iterations_per_phase: $max_iterations

# Sequential phases (Ralph loops run ONE AT A TIME)
phases:
  - name: EXECUTE
    status: pending
    promise: ${foundry^^}_PROPOSAL_READY
    max_iter: 30
  - name: IMPLEMENT
    status: pending
    promise: CHANGES_APPLIED
    max_iter: 20
  - name: AUDIT
    status: pending
    promise: ALL_AUDITS_PASS
    max_iter: 15
  - name: EVAL
    status: pending
    promise: EVAL_HARNESS_PASS
    max_iter: 50
  - name: MONITOR
    status: pending
    promise: MONITOR_COMPLETE
    max_iter: 7

current_phase: EXECUTE
current_phase_iteration: 0

# Metrics
metrics:
  baseline: null
  candidate: null
  verdict: null

# Auditor results (run as Task agents, not Ralph loops)
auditors:
  prompt: pending
  skill: pending
  expertise: pending
  output: pending
---
EOF

    log_success "Meta Loop initialized!"
    echo ""
    echo "=========================================="
    echo "   META LOOP: $session_id"
    echo "=========================================="
    echo ""
    echo "Task:    $task"
    echo "Target:  $target"
    echo "Foundry: $foundry"
    echo ""
    echo "Phases (SEQUENTIAL - one Ralph loop at a time):"
    echo "  1. EXECUTE   -> Generate proposal"
    echo "  2. IMPLEMENT -> Apply changes"
    echo "  3. AUDIT     -> Run 4 auditor agents (parallel Tasks)"
    echo "  4. EVAL      -> Eval harness validation"
    echo "  5. MONITOR   -> 7-day watch"
    echo ""
    echo "Starting EXECUTE phase..."
    echo ""

    # Start first Ralph loop for EXECUTE phase
    cmd_phase "EXECUTE" "$(get_execute_prompt "$task" "$target" "$foundry")" --promise "${foundry^^}_PROPOSAL_READY"
}

# ============================================================
# COMMAND: phase
# Start a Ralph loop for a specific phase
# ============================================================
cmd_phase() {
    local phase_name="$1"
    local prompt="$2"
    local promise=""
    local max_iter=30

    shift 2

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --promise) promise="$2"; shift 2 ;;
            --max-iter) max_iter="$2"; shift 2 ;;
            *) shift ;;
        esac
    done

    if [[ -z "$promise" ]]; then
        log_error "Phase requires --promise"
        exit 1
    fi

    log_phase "Starting phase: $phase_name"
    log_info "Promise: $promise"
    log_info "Max iterations: $max_iter"

    # Update meta state
    if [[ -f "$META_STATE" ]]; then
        if [[ "$(uname -s)" == "Darwin" ]]; then
            sed -i '' "s/^current_phase:.*/current_phase: $phase_name/" "$META_STATE"
            sed -i '' "s/^current_phase_iteration:.*/current_phase_iteration: 0/" "$META_STATE"
        else
            sed -i "s/^current_phase:.*/current_phase: $phase_name/" "$META_STATE"
            sed -i "s/^current_phase_iteration:.*/current_phase_iteration: 0/" "$META_STATE"
        fi
    fi

    # Create Ralph state file (this is what the Stop hook reads)
    cat > "$RALPH_STATE" << EOF
---
session_id: ${phase_name}-$(date +%Y%m%d-%H%M%S)
iteration: 0
max_iterations: $max_iter
completion_promise: "$promise"
started_at: $(date -Iseconds 2>/dev/null || date +%Y-%m-%dT%H:%M:%S)
active: true
quality_gate: true
meta_loop_phase: $phase_name
---

$prompt
EOF

    echo ""
    echo "=========================================="
    echo "   RALPH LOOP: Phase $phase_name"
    echo "=========================================="
    echo ""
    echo "Promise: <promise>$promise</promise>"
    echo "Max iterations: $max_iter"
    echo ""
    echo "The Stop hook will now manage this loop."
    echo "Work on the task. Output the promise when complete."
    echo ""
}

# ============================================================
# Generate phase-specific prompts
# ============================================================
get_execute_prompt() {
    local task="$1"
    local target="$2"
    local foundry="$3"

    case "$foundry" in
        "agent-creator")
            cat << EOF
META LOOP PHASE: EXECUTE (Agent Creator)
Task: $task
Target: $target

Execute agent-creator methodology:

Phase 0: Load domain expertise from .claude/expertise/
Phase 0.5: Select cognitive frame (evidential/aspectual/hierarchical)
Phase 1: Analysis & Intent Decoding (30-60 min)
Phase 2: Meta-Cognitive Extraction (30-45 min)
Phase 3: Architecture Design (45-60 min)
Phase 4: Technical Enhancement (60-90 min)

Generate a complete improvement proposal with:
- Changes needed
- Rationale for each change
- Predicted improvement metrics

Output <promise>AGENT-CREATOR_PROPOSAL_READY</promise> when proposal is complete.
EOF
            ;;
        "skill-forge")
            cat << EOF
META LOOP PHASE: EXECUTE (Skill Forge)
Task: $task
Target: $target

Execute skill-forge methodology:

Phase 0: Schema Definition (if complex)
Phase 0.5: Cognitive Frame Design
Phase 1: Intent Archaeology + Chain-of-Verification
Phase 2: Use Case Crystallization
Phase 3: Structural Architecture
Phase 4: Metadata Engineering
Phase 5: Instruction Crafting + COV
Phase 6: Resource Development
Phase 7: Validation + Adversarial Testing
Phase 8: Metrics Tracking

Generate a complete improvement proposal with:
- Specific changes to make
- COV validation of changes
- Adversarial testing considerations

Output <promise>SKILL-FORGE_PROPOSAL_READY</promise> when proposal is complete.
EOF
            ;;
        "prompt-forge")
            cat << EOF
META LOOP PHASE: EXECUTE (Prompt Forge)
Task: $task
Target: $target

Execute prompt-forge methodology:

Operation 1: Analyze current prompt structure
Operation 2: Generate improvement proposal
Operation 3: Apply evidence-based techniques
Operation 4: Generate diff showing changes
Operation 5: Self-verify improvements
Operation 6: Apply cognitive frame enhancement

Generate a complete improvement proposal with:
- Before/after for each change
- Rationale and technique used
- Predicted metric improvements

Output <promise>PROMPT-FORGE_PROPOSAL_READY</promise> when proposal is complete.
EOF
            ;;
    esac
}

# ============================================================
# COMMAND: status
# Show current meta loop status
# ============================================================
cmd_status() {
    if [[ ! -f "$META_STATE" ]]; then
        log_warning "No active meta loop"
        return
    fi

    echo ""
    echo "=========================================="
    echo "   META LOOP STATUS"
    echo "=========================================="
    echo ""

    # Extract values
    local session_id=$(grep "^session_id:" "$META_STATE" | head -1 | awk '{print $2}')
    local active=$(grep "^active:" "$META_STATE" | head -1 | awk '{print $2}')
    local phase=$(grep "^current_phase:" "$META_STATE" | head -1 | awk '{print $2}')
    local task=$(grep "^task:" "$META_STATE" | head -1 | sed 's/task: *//' | tr -d '"')

    echo "Session: $session_id"
    echo "Active:  $active"
    echo "Phase:   $phase"
    echo "Task:    $task"
    echo ""

    # Ralph loop status
    if [[ -f "$RALPH_STATE" ]]; then
        local ralph_active=$(grep "^active:" "$RALPH_STATE" | head -1 | awk '{print $2}')
        local iteration=$(grep "^iteration:" "$RALPH_STATE" | head -1 | awk '{print $2}')
        local max_iter=$(grep "^max_iterations:" "$RALPH_STATE" | head -1 | awk '{print $2}')
        local promise=$(grep "^completion_promise:" "$RALPH_STATE" | head -1 | sed 's/completion_promise: *//' | tr -d '"')

        echo "Ralph Loop:"
        echo "  Active:     $ralph_active"
        echo "  Iteration:  $iteration / $max_iter"
        echo "  Promise:    $promise"
    else
        echo "Ralph Loop: Not active"
    fi
    echo ""
}

# ============================================================
# COMMAND: cancel
# Cancel the meta loop
# ============================================================
cmd_cancel() {
    if [[ ! -f "$META_STATE" ]]; then
        log_warning "No active meta loop to cancel"
        return
    fi

    local session_id=$(grep "^session_id:" "$META_STATE" | head -1 | awk '{print $2}')

    # Deactivate meta state
    if [[ "$(uname -s)" == "Darwin" ]]; then
        sed -i '' 's/^active: true/active: false/' "$META_STATE"
    else
        sed -i 's/^active: true/active: false/' "$META_STATE"
    fi

    # Deactivate Ralph state if exists
    if [[ -f "$RALPH_STATE" ]]; then
        if [[ "$(uname -s)" == "Darwin" ]]; then
            sed -i '' 's/^active: true/active: false/' "$RALPH_STATE"
        else
            sed -i 's/^active: true/active: false/' "$RALPH_STATE"
        fi
    fi

    # Archive
    cp "$META_STATE" "$SESSIONS_DIR/${session_id}-cancelled.yaml"

    log_success "Meta loop cancelled: $session_id"
    echo ""
    echo "Session archived to: $SESSIONS_DIR/${session_id}-cancelled.yaml"
    echo ""
}

# ============================================================
# COMMAND: next-phase
# Advance to next phase
# ============================================================
cmd_next_phase() {
    if [[ ! -f "$META_STATE" ]]; then
        log_error "No active meta loop"
        exit 1
    fi

    local current=$(grep "^current_phase:" "$META_STATE" | head -1 | awk '{print $2}')
    local task=$(grep "^task:" "$META_STATE" | head -1 | sed 's/task: *//' | tr -d '"')
    local target=$(grep "^target:" "$META_STATE" | head -1 | sed 's/target: *//' | tr -d '"')
    local foundry=$(grep "^foundry_skill:" "$META_STATE" | head -1 | awk '{print $2}')

    local next_phase=""
    local next_prompt=""
    local next_promise=""
    local next_max=30

    case "$current" in
        "EXECUTE")
            next_phase="IMPLEMENT"
            next_promise="CHANGES_APPLIED"
            next_max=20
            next_prompt="META LOOP PHASE: IMPLEMENT

Apply the improvement proposal to: $target

For each proposed change:
1. Locate exact position in file
2. Apply edit using Edit tool
3. Validate syntax/structure
4. Quick test if applicable

After all changes applied:
- Verify files saved
- Run quick validation

Output <promise>CHANGES_APPLIED</promise> when all edits are complete."
            ;;
        "IMPLEMENT")
            next_phase="AUDIT"
            next_promise="ALL_AUDITS_PASS"
            next_max=15
            next_prompt="META LOOP PHASE: AUDIT

Run 4 auditor validations on changes to: $target

Spawn these auditor agents in PARALLEL (single message):

Task(\"Prompt Auditor\", \"Audit instructions: clarity >= 0.8, completeness >= 0.8\", \"prompt-auditor\")
Task(\"Skill Auditor\", \"Audit structure: Tier 1-2 at 100%, YAML valid\", \"skill-auditor\")
Task(\"Expertise Auditor\", \"Verify domain accuracy: file locations, patterns\", \"expertise-auditor\")
Task(\"Output Auditor\", \"Validate output quality: format, metrics\", \"output-auditor\")

Wait for all auditors. If any fail, route issues back for fixes.

Output <promise>ALL_AUDITS_PASS</promise> when all 4 auditors pass."
            ;;
        "AUDIT")
            next_phase="EVAL"
            next_promise="EVAL_HARNESS_PASS"
            next_max=50
            next_prompt="META LOOP PHASE: EVAL

Run eval harness validation on: $target

1. Identify benchmark suite for this skill type
2. Run benchmark tests
3. Run regression tests
4. If any test fails:
   - Analyze failure
   - Generate fix
   - Apply fix
   - Re-run test

Requirements:
- All benchmarks PASS
- No regressions (0 failures)
- Metrics improved or unchanged

Output <promise>EVAL_HARNESS_PASS</promise> when all tests pass."
            ;;
        "EVAL")
            next_phase="COMPARE"
            log_phase "Moving to COMPARE (no Ralph loop)"
            log_info "Compare baseline vs candidate metrics"
            log_info "Decide: ACCEPT / REJECT / ESCALATE"
            return
            ;;
        *)
            log_warning "Unknown phase: $current"
            return
            ;;
    esac

    log_phase "Advancing: $current -> $next_phase"
    cmd_phase "$next_phase" "$next_prompt" --promise "$next_promise" --max-iter "$next_max"
}

# ============================================================
# Main entry point
# ============================================================
main() {
    local command="${1:-help}"
    shift || true

    case "$command" in
        start) cmd_start "$@" ;;
        phase) cmd_phase "$@" ;;
        status) cmd_status ;;
        cancel) cmd_cancel ;;
        next|next-phase) cmd_next_phase ;;
        help|--help|-h)
            echo "Meta Loop Setup Script"
            echo ""
            echo "Commands:"
            echo "  start \"<task>\" --target <file> --foundry <skill>"
            echo "  phase <name> \"<prompt>\" --promise <text>"
            echo "  status"
            echo "  cancel"
            echo "  next-phase"
            echo ""
            echo "Foundry skills: agent-creator, skill-forge, prompt-forge"
            echo ""
            echo "The meta loop uses SEQUENTIAL Ralph loops (one at a time)."
            echo "The Stop hook manages iteration via the state file."
            ;;
        *)
            log_error "Unknown command: $command"
            echo "Use '$0 help' for usage"
            exit 1
            ;;
    esac
}

main "$@"
