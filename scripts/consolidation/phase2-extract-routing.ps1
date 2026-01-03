# Phase 2: Extract Routing from When-X-Use-Y Files
# Creates COMMANDS_INDEX.yaml from routing wrapper files
# Run with: powershell -ExecutionPolicy Bypass -File phase2-extract-routing.ps1

$SkillsDir = "$env:USERPROFILE\.claude\commands\skills"
$OutputFile = "$env:USERPROFILE\.claude\commands\COMMANDS_INDEX.yaml"
$BackupDir = "$env:USERPROFILE\.claude\commands\skills-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== Phase 2: Extract Routing from When-X-Use-Y Files ===" -ForegroundColor Cyan
Write-Host ""

# Find all when-X-use-Y files
$RoutingFiles = Get-ChildItem -Path $SkillsDir -Filter "*when-*-use-*.md" -ErrorAction SilentlyContinue

if ($RoutingFiles.Count -eq 0) {
    Write-Host "No when-X-use-Y routing files found. Exiting." -ForegroundColor Yellow
    exit
}

Write-Host "Found $($RoutingFiles.Count) routing wrapper files" -ForegroundColor Yellow
Write-Host ""

# Build routing index
$RoutingIndex = @{}

foreach ($file in $RoutingFiles) {
    # Parse filename: skill-category-when-TRIGGER-use-TARGET.md
    $name = $file.BaseName

    # Extract trigger and target from filename
    if ($name -match "when-(.+)-use-(.+)$") {
        $trigger = $Matches[1] -replace "-", " "
        $target = $Matches[2] -replace "-", " "

        # Determine category from prefix
        $category = "general"
        if ($name -match "^skill-(\w+)-when") {
            $category = $Matches[1]
        }

        if (-not $RoutingIndex.ContainsKey($category)) {
            $RoutingIndex[$category] = @()
        }

        $RoutingIndex[$category] += @{
            trigger = $trigger
            skill = $target
            source = $file.Name
        }
    }
}

# Generate YAML content
$YamlContent = @"
# COMMANDS_INDEX.yaml - Intent-to-Skill Routing Manifest
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
# This file replaces $($RoutingFiles.Count) individual routing wrapper files

version: "1.0"
generated: "$(Get-Date -Format 'yyyy-MM-dd')"

# Intent Routing Rules
# When user intent matches a trigger phrase, invoke the corresponding skill
intent_routing:
"@

foreach ($category in $RoutingIndex.Keys | Sort-Object) {
    $YamlContent += "`n  # Category: $category`n"
    $YamlContent += "  $category`:`n"

    foreach ($route in $RoutingIndex[$category]) {
        $YamlContent += "    - trigger: `"$($route.trigger)`"`n"
        $YamlContent += "      skill: `"$($route.skill)`"`n"
        $YamlContent += "      # source: $($route.source)`n"
    }
}

$YamlContent += @"

# Usage Notes:
# - This file is used by the skill-router-hook to match user intents
# - Triggers are matched as substrings (case-insensitive)
# - Multiple triggers can map to the same skill
# - The source comment shows which file this routing came from
"@

# Write YAML file
$YamlContent | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "Created routing manifest: $OutputFile" -ForegroundColor Green
Write-Host ""

# Backup and delete routing files
Write-Host "Creating backup of routing files at: $BackupDir" -ForegroundColor Yellow
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null

foreach ($file in $RoutingFiles) {
    Move-Item $file.FullName $BackupDir -Force
    Write-Host "Moved: $($file.Name)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Phase 2 Complete ===" -ForegroundColor Cyan
Write-Host "Created: COMMANDS_INDEX.yaml" -ForegroundColor Green
Write-Host "Moved $($RoutingFiles.Count) routing files to backup" -ForegroundColor Green
Write-Host ""
Write-Host "To rollback: Move-Item '$BackupDir\*' '$SkillsDir\'"
