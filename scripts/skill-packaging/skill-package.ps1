# skill-package.ps1 - Package a skill folder into a .skill file
# Usage: .\skill-package.ps1 -SkillFolder <path> [-OutputPath <path>] [-PackagedDir <path>]
#
# This script packages a skill folder into a .skill file (zip renamed)
# and optionally copies it to the packaged/ directory.

param(
    [Parameter(Mandatory=$true)]
    [string]$SkillFolder,

    [string]$OutputPath = "",

    [string]$PackagedDir = "",

    [switch]$Force,

    [switch]$CopyToPackaged
)

$ErrorActionPreference = "Stop"

# Resolve skill folder
if (-not (Test-Path $SkillFolder)) {
    Write-Error "Skill folder not found: $SkillFolder"
    exit 1
}

$SkillFolder = Resolve-Path $SkillFolder

# Get skill name from folder
$skillName = Split-Path $SkillFolder -Leaf

# Validate SKILL.md exists
$skillMd = Join-Path $SkillFolder "SKILL.md"
if (-not (Test-Path $skillMd)) {
    Write-Error "SKILL.md not found in: $SkillFolder"
    exit 1
}

# Default output path
if (-not $OutputPath) {
    $parentDir = Split-Path $SkillFolder -Parent
    $OutputPath = Join-Path $parentDir "$skillName.skill"
}

# Default packaged directory
if (-not $PackagedDir) {
    # Find skills/packaged relative to skill location
    $searchPath = $SkillFolder
    while ($searchPath -and -not (Test-Path (Join-Path $searchPath "packaged"))) {
        $searchPath = Split-Path $searchPath -Parent
        if ($searchPath -match "skills$") {
            $PackagedDir = Join-Path $searchPath "packaged"
            break
        }
    }
    if (-not $PackagedDir) {
        $PackagedDir = Join-Path (Split-Path $SkillFolder -Parent) "packaged"
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Packaging Skill: $skillName" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Validate required structure
Write-Host "Validating skill structure..." -ForegroundColor Gray
$requiredFiles = @("SKILL.md")
$recommendedDirs = @("examples", "tests")
$optionalDirs = @("references", "resources")

$valid = $true
foreach ($file in $requiredFiles) {
    $path = Join-Path $SkillFolder $file
    if (Test-Path $path) {
        Write-Host "  [OK] $file" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $file" -ForegroundColor Red
        $valid = $false
    }
}

foreach ($dir in $recommendedDirs) {
    $path = Join-Path $SkillFolder $dir
    if (Test-Path $path) {
        $count = (Get-ChildItem $path -File -Recurse).Count
        Write-Host "  [OK] $dir/ ($count files)" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] $dir/ (recommended)" -ForegroundColor Yellow
    }
}

foreach ($dir in $optionalDirs) {
    $path = Join-Path $SkillFolder $dir
    if (Test-Path $path) {
        $count = (Get-ChildItem $path -File -Recurse).Count
        Write-Host "  [OK] $dir/ ($count files)" -ForegroundColor Green
    }
}

if (-not $valid) {
    Write-Error "Skill validation failed. Missing required files."
    exit 1
}

Write-Host ""

# Remove existing .skill file if exists
if (Test-Path $OutputPath) {
    if ($Force) {
        Remove-Item -Path $OutputPath -Force
        Write-Host "Removed existing: $OutputPath" -ForegroundColor Gray
    } else {
        Write-Error "Skill file already exists: $OutputPath. Use -Force to overwrite."
        exit 1
    }
}

# Create temp zip
$tempZip = [System.IO.Path]::GetTempFileName()
Remove-Item $tempZip
$tempZip = $tempZip + ".zip"

Write-Host "Creating package..." -ForegroundColor Gray

# Compress folder contents
Compress-Archive -Path "$SkillFolder\*" -DestinationPath $tempZip -Force

# Rename to .skill
Move-Item -Path $tempZip -Destination $OutputPath -Force

# Get file info
$fileInfo = Get-Item $OutputPath
$sizeKB = [math]::Round($fileInfo.Length / 1024, 1)

Write-Host ""
Write-Host "Packaged: $OutputPath" -ForegroundColor Green
Write-Host "Size: ${sizeKB} KB" -ForegroundColor Gray

# Copy to packaged directory if requested
if ($CopyToPackaged) {
    if (-not (Test-Path $PackagedDir)) {
        New-Item -ItemType Directory -Path $PackagedDir -Force | Out-Null
    }

    $packagedPath = Join-Path $PackagedDir "$skillName.skill"
    Copy-Item -Path $OutputPath -Destination $packagedPath -Force
    Write-Host "Copied to: $packagedPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green

# Return info
return @{
    SkillName = $skillName
    OutputPath = $OutputPath
    SizeKB = $sizeKB
}
