# Phase 1: Delete Exact Duplicate Commands
# This script removes long-prefix duplicates, keeping short names
# Run with: powershell -ExecutionPolicy Bypass -File phase1-delete-duplicates.ps1

$CommandsDir = "$env:USERPROFILE\.claude\commands"
$BackupDir = "$env:USERPROFILE\.claude\commands-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== Phase 1: Delete Exact Duplicate Commands ===" -ForegroundColor Cyan
Write-Host ""

# Create backup first
Write-Host "Creating backup at: $BackupDir" -ForegroundColor Yellow
Copy-Item -Path $CommandsDir -Destination $BackupDir -Recurse
Write-Host "Backup created successfully" -ForegroundColor Green
Write-Host ""

# Duplicates mapping: [keep-name] -> [delete-names]
$Duplicates = @{
    # delivery-essential-commands duplicates
    "build-feature.md" = @("delivery-essential-commands-build-feature.md")
    "fix-bug.md" = @("delivery-essential-commands-fix-bug.md")
    "review-pr.md" = @("delivery-essential-commands-review-pr.md")
    "quick-check.md" = @("delivery-essential-commands-quick-check.md")
    "smoke-test.md" = @("delivery-essential-commands-smoke-test.md")
    "e2e-test.md" = @("delivery-essential-commands-e2e-test.md")

    # delivery-sparc duplicates
    "sparc.md" = @("delivery-sparc-sparc.md")
    "debug.md" = @("delivery-sparc-debug.md", "delivery-sparc-debugger.md")
    "tdd.md" = @("delivery-sparc-tdd.md")
    "tester.md" = @("delivery-sparc-tester.md")
    "reviewer.md" = @("delivery-sparc-reviewer.md")
    "documenter.md" = @("delivery-sparc-documenter.md")
    "researcher.md" = @("delivery-sparc-researcher.md")
    "analyzer.md" = @("delivery-sparc-analyzer.md")
    "architect.md" = @("delivery-sparc-architect.md")
    "devops.md" = @("delivery-sparc-devops.md")
    "code.md" = @("delivery-sparc-code.md", "delivery-sparc-coder.md")
    "optimizer.md" = @("delivery-sparc-optimizer.md")

    # delivery-workflows duplicates
    "deployment.md" = @("delivery-workflows-deployment.md")
    "development.md" = @("delivery-workflows-development.md")
    "testing.md" = @("delivery-workflows-testing.md")

    # Other category duplicates
    "auto-agent.md" = @("operations-automation-auto-agent.md")
    "smart-spawn.md" = @("operations-automation-smart-spawn.md")
    "mcp.md" = @("delivery-sparc-mcp.md")
    "improve.md" = @("foundry-recursive-improvement-run-improvement-cycle.md")
    "expertise-create.md" = @("foundry-expertise-expertise-create.md")
}

$DeletedCount = 0
$SkippedCount = 0

foreach ($keep in $Duplicates.Keys) {
    $keepPath = Join-Path $CommandsDir $keep

    # Verify the keeper file exists
    if (-not (Test-Path $keepPath)) {
        Write-Host "WARNING: Keeper file not found: $keep" -ForegroundColor Yellow
        continue
    }

    foreach ($delete in $Duplicates[$keep]) {
        $deletePath = Join-Path $CommandsDir $delete

        if (Test-Path $deletePath) {
            Remove-Item $deletePath -Force
            Write-Host "DELETED: $delete (keeping: $keep)" -ForegroundColor Green
            $DeletedCount++
        } else {
            $SkippedCount++
        }
    }
}

Write-Host ""
Write-Host "=== Phase 1 Complete ===" -ForegroundColor Cyan
Write-Host "Deleted: $DeletedCount files" -ForegroundColor Green
Write-Host "Skipped (not found): $SkippedCount files" -ForegroundColor Yellow
Write-Host ""
Write-Host "To rollback: Copy-Item -Path '$BackupDir' -Destination '$CommandsDir' -Recurse -Force"
