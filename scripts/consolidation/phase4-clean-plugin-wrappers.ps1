# Phase 4: Remove When-X-Use-Y Routing Wrappers from Plugin
# These are now handled by COMMANDS_INDEX.yaml
# Run with: powershell -ExecutionPolicy Bypass -File phase4-clean-plugin-wrappers.ps1

$PluginDir = "C:\Users\17175\claude-code-plugins\context-cascade"
$SkillsDir = Join-Path $PluginDir "skills"
$BackupDir = "$env:USERPROFILE\.claude\plugin-wrappers-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== Phase 4: Remove Routing Wrappers from Plugin ===" -ForegroundColor Cyan
Write-Host ""

# Find all when-*-use-* directories
$WrapperDirs = Get-ChildItem -Path $SkillsDir -Recurse -Directory |
    Where-Object { $_.Name -match "when-.*-use-" }

Write-Host "Found $($WrapperDirs.Count) routing wrapper skill folders" -ForegroundColor Yellow
Write-Host ""

if ($WrapperDirs.Count -eq 0) {
    Write-Host "No wrapper folders found. Exiting." -ForegroundColor Green
    exit
}

# Create backup directory
Write-Host "Creating backup at: $BackupDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

# Backup and delete each wrapper
$DeletedCount = 0
foreach ($dir in $WrapperDirs) {
    # Create relative backup path
    $RelPath = $dir.FullName.Replace($SkillsDir, "").TrimStart("\")
    $BackupPath = Join-Path $BackupDir $RelPath

    # Create parent directory in backup
    $BackupParent = Split-Path $BackupPath -Parent
    if (-not (Test-Path $BackupParent)) {
        New-Item -ItemType Directory -Path $BackupParent -Force | Out-Null
    }

    # Copy to backup
    Copy-Item -Path $dir.FullName -Destination $BackupPath -Recurse -Force

    # Delete original
    Remove-Item -Path $dir.FullName -Recurse -Force
    Write-Host "DELETED: $($dir.Name)" -ForegroundColor Green
    $DeletedCount++
}

Write-Host ""
Write-Host "=== Phase 4 Complete ===" -ForegroundColor Cyan
Write-Host "Deleted $DeletedCount routing wrapper folders from plugin" -ForegroundColor Green
Write-Host ""

# Regenerate skill index
Write-Host "Regenerating skill-index.json..." -ForegroundColor Yellow
$IndexScript = Join-Path $PluginDir "scripts\skill-index\generate-index.js"

if (Test-Path $IndexScript) {
    Push-Location $PluginDir
    node $IndexScript
    Pop-Location
    Write-Host "skill-index.json regenerated" -ForegroundColor Green
} else {
    Write-Host "WARNING: generate-index.js not found - run manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To rollback: Copy-Item -Path '$BackupDir\*' -Destination '$SkillsDir' -Recurse"
