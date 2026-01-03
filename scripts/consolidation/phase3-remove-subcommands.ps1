# Phase 3: Remove Skills and Agents from Commands Registration
# These should be loaded on-demand, not registered as slash commands
# Run with: powershell -ExecutionPolicy Bypass -File phase3-remove-subcommands.ps1

$CommandsDir = "$env:USERPROFILE\.claude\commands"
$SkillsDir = Join-Path $CommandsDir "skills"
$AgentsDir = Join-Path $CommandsDir "agents"
$BackupDir = "$env:USERPROFILE\.claude\commands-subcommands-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== Phase 3: Remove Skills/Agents from Commands Registration ===" -ForegroundColor Cyan
Write-Host ""

# Count files to be removed
$SkillCount = 0
$AgentCount = 0

if (Test-Path $SkillsDir) {
    $SkillCount = (Get-ChildItem $SkillsDir -Filter "*.md" -ErrorAction SilentlyContinue).Count
}
if (Test-Path $AgentsDir) {
    $AgentCount = (Get-ChildItem $AgentsDir -Filter "*.md" -ErrorAction SilentlyContinue).Count
}

Write-Host "Found $SkillCount skill files and $AgentCount agent files to remove" -ForegroundColor Yellow
Write-Host ""

if (($SkillCount + $AgentCount) -eq 0) {
    Write-Host "No files to remove. Exiting." -ForegroundColor Yellow
    exit
}

# Create backup
Write-Host "Creating backup at: $BackupDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

if (Test-Path $SkillsDir) {
    Copy-Item -Path $SkillsDir -Destination (Join-Path $BackupDir "skills") -Recurse
    Write-Host "Backed up skills directory" -ForegroundColor Gray
}

if (Test-Path $AgentsDir) {
    Copy-Item -Path $AgentsDir -Destination (Join-Path $BackupDir "agents") -Recurse
    Write-Host "Backed up agents directory" -ForegroundColor Gray
}

Write-Host "Backup created successfully" -ForegroundColor Green
Write-Host ""

# Confirm before deletion
$Confirm = Read-Host "Delete $SkillCount skill files and $AgentCount agent files? (y/N)"

if ($Confirm -ne "y") {
    Write-Host "Cancelled. No files deleted." -ForegroundColor Yellow
    exit
}

# Delete directories
if (Test-Path $SkillsDir) {
    Remove-Item $SkillsDir -Recurse -Force
    Write-Host "DELETED: skills directory ($SkillCount files)" -ForegroundColor Green
}

if (Test-Path $AgentsDir) {
    Remove-Item $AgentsDir -Recurse -Force
    Write-Host "DELETED: agents directory ($AgentCount files)" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Phase 3 Complete ===" -ForegroundColor Cyan
Write-Host "Removed $($SkillCount + $AgentCount) files from commands registration" -ForegroundColor Green
Write-Host ""
Write-Host "Skills and agents are now loaded on-demand from:" -ForegroundColor Cyan
Write-Host "  - context-cascade/discovery/SKILL-INDEX.md" -ForegroundColor White
Write-Host "  - context-cascade/discovery/AGENT-REGISTRY.md" -ForegroundColor White
Write-Host ""
Write-Host "To rollback: Copy-Item -Path '$BackupDir\*' -Destination '$CommandsDir' -Recurse"
