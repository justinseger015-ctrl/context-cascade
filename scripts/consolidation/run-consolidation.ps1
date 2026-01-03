# Master Consolidation Script
# Runs all phases with confirmation between each
# Run with: powershell -ExecutionPolicy Bypass -File run-consolidation.ps1

param(
    [switch]$Phase1Only,
    [switch]$Phase2Only,
    [switch]$Phase3Only,
    [switch]$DryRun,
    [switch]$Force
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CommandsDir = "$env:USERPROFILE\.claude\commands"

Write-Host @"
============================================================
     CONTEXT CASCADE COMMANDS CONSOLIDATION
============================================================

This script will consolidate your commands directory from:
  ~710 files (~944k tokens) -> ~165 files (~232k tokens)

Phases:
  1. Delete exact duplicates (35 files, 17k tokens saved)
  2. Convert routing wrappers to index (60 files, 40k tokens saved)
  3. Remove skills/agents from commands (450 files, 650k tokens saved)

Current state:
"@ -ForegroundColor Cyan

# Count current files
$TopLevelCount = (Get-ChildItem $CommandsDir -Filter "*.md" -ErrorAction SilentlyContinue).Count
$SkillsCount = 0
$AgentsCount = 0

if (Test-Path "$CommandsDir\skills") {
    $SkillsCount = (Get-ChildItem "$CommandsDir\skills" -Filter "*.md" -ErrorAction SilentlyContinue).Count
}
if (Test-Path "$CommandsDir\agents") {
    $AgentsCount = (Get-ChildItem "$CommandsDir\agents" -Filter "*.md" -ErrorAction SilentlyContinue).Count
}

Write-Host "  Top-level commands: $TopLevelCount" -ForegroundColor White
Write-Host "  Skills (commands/skills/): $SkillsCount" -ForegroundColor White
Write-Host "  Agents (commands/agents/): $AgentsCount" -ForegroundColor White
Write-Host "  TOTAL: $($TopLevelCount + $SkillsCount + $AgentsCount)" -ForegroundColor Yellow
Write-Host ""

if ($DryRun) {
    Write-Host "[DRY RUN MODE - No changes will be made]" -ForegroundColor Magenta
    Write-Host ""
}

# Phase 1
if (-not $Phase2Only -and -not $Phase3Only) {
    Write-Host "=== PHASE 1: Delete Exact Duplicates ===" -ForegroundColor Cyan

    if (-not $Force) {
        $confirm = Read-Host "Run Phase 1? (y/N)"
        if ($confirm -ne "y") {
            Write-Host "Phase 1 skipped" -ForegroundColor Yellow
        } else {
            if ($DryRun) {
                Write-Host "[DRY RUN] Would run: phase1-delete-duplicates.ps1" -ForegroundColor Magenta
            } else {
                & "$ScriptDir\phase1-delete-duplicates.ps1"
            }
        }
    } else {
        if ($DryRun) {
            Write-Host "[DRY RUN] Would run: phase1-delete-duplicates.ps1" -ForegroundColor Magenta
        } else {
            & "$ScriptDir\phase1-delete-duplicates.ps1"
        }
    }
    Write-Host ""
}

# Phase 2
if (-not $Phase1Only -and -not $Phase3Only) {
    Write-Host "=== PHASE 2: Convert Routing Wrappers ===" -ForegroundColor Cyan

    if (-not $Force) {
        $confirm = Read-Host "Run Phase 2? (y/N)"
        if ($confirm -ne "y") {
            Write-Host "Phase 2 skipped" -ForegroundColor Yellow
        } else {
            if ($DryRun) {
                Write-Host "[DRY RUN] Would run: phase2-extract-routing.ps1" -ForegroundColor Magenta
            } else {
                & "$ScriptDir\phase2-extract-routing.ps1"
            }
        }
    } else {
        if ($DryRun) {
            Write-Host "[DRY RUN] Would run: phase2-extract-routing.ps1" -ForegroundColor Magenta
        } else {
            & "$ScriptDir\phase2-extract-routing.ps1"
        }
    }
    Write-Host ""
}

# Phase 3
if (-not $Phase1Only -and -not $Phase2Only) {
    Write-Host "=== PHASE 3: Remove Skills/Agents from Commands ===" -ForegroundColor Cyan
    Write-Host "WARNING: This is the biggest change - removes 450+ files" -ForegroundColor Red
    Write-Host "Skills and agents will still work via on-demand loading" -ForegroundColor Yellow
    Write-Host ""

    if (-not $Force) {
        $confirm = Read-Host "Run Phase 3? (y/N)"
        if ($confirm -ne "y") {
            Write-Host "Phase 3 skipped" -ForegroundColor Yellow
        } else {
            if ($DryRun) {
                Write-Host "[DRY RUN] Would run: phase3-remove-subcommands.ps1" -ForegroundColor Magenta
            } else {
                & "$ScriptDir\phase3-remove-subcommands.ps1"
            }
        }
    } else {
        if ($DryRun) {
            Write-Host "[DRY RUN] Would run: phase3-remove-subcommands.ps1" -ForegroundColor Magenta
        } else {
            & "$ScriptDir\phase3-remove-subcommands.ps1"
        }
    }
    Write-Host ""
}

# Final count
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "CONSOLIDATION COMPLETE" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

$FinalTopLevel = (Get-ChildItem $CommandsDir -Filter "*.md" -ErrorAction SilentlyContinue).Count
$FinalSkills = 0
$FinalAgents = 0

if (Test-Path "$CommandsDir\skills") {
    $FinalSkills = (Get-ChildItem "$CommandsDir\skills" -Filter "*.md" -ErrorAction SilentlyContinue).Count
}
if (Test-Path "$CommandsDir\agents") {
    $FinalAgents = (Get-ChildItem "$CommandsDir\agents" -Filter "*.md" -ErrorAction SilentlyContinue).Count
}

$Before = $TopLevelCount + $SkillsCount + $AgentsCount
$After = $FinalTopLevel + $FinalSkills + $FinalAgents
$Saved = $Before - $After

Write-Host ""
Write-Host "Before: $Before files" -ForegroundColor White
Write-Host "After:  $After files" -ForegroundColor Green
Write-Host "Saved:  $Saved files (~$([math]::Round($Saved * 0.7))k tokens estimated)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backups created in: $env:USERPROFILE\.claude\" -ForegroundColor Yellow
