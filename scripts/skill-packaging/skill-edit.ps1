# skill-edit.ps1 - Edit packaged .skill files
# Usage: .\skill-edit.ps1 -Action <unpack|pack|edit> -SkillPath <path> [-EditPath <path>]
#
# Actions:
#   unpack - Extract .skill to folder for editing
#   pack   - Package folder back to .skill
#   edit   - Open folder for editing (unpacks, waits for user, then packs)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("unpack", "pack", "edit")]
    [string]$Action,

    [Parameter(Mandatory=$true)]
    [string]$SkillPath,

    [string]$EditPath = "",

    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Resolve paths
$SkillPath = Resolve-Path $SkillPath -ErrorAction SilentlyContinue
if (-not $SkillPath -and $Action -ne "pack") {
    Write-Error "Skill file not found: $SkillPath"
    exit 1
}

# Default edit path is skill name without extension + "-edit"
if (-not $EditPath) {
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($SkillPath)
    $parentDir = [System.IO.Path]::GetDirectoryName($SkillPath)
    $EditPath = Join-Path $parentDir "$baseName-edit"
}

function Unpack-Skill {
    param([string]$Source, [string]$Destination)

    Write-Host "Unpacking skill: $Source" -ForegroundColor Cyan

    if (Test-Path $Destination) {
        if ($Force) {
            Remove-Item -Path $Destination -Recurse -Force
        } else {
            Write-Error "Edit folder already exists: $Destination. Use -Force to overwrite."
            exit 1
        }
    }

    # Create temp zip copy (since .skill is just a renamed .zip)
    $tempZip = [System.IO.Path]::GetTempFileName() + ".zip"
    Copy-Item -Path $Source -Destination $tempZip

    # Extract
    Expand-Archive -Path $tempZip -DestinationPath $Destination -Force
    Remove-Item -Path $tempZip

    Write-Host "Unpacked to: $Destination" -ForegroundColor Green
    return $Destination
}

function Pack-Skill {
    param([string]$Source, [string]$Destination)

    Write-Host "Packing skill: $Source -> $Destination" -ForegroundColor Cyan

    if (-not (Test-Path $Source)) {
        Write-Error "Source folder not found: $Source"
        exit 1
    }

    # Remove existing .skill file if exists
    if (Test-Path $Destination) {
        if ($Force) {
            Remove-Item -Path $Destination -Force
        } else {
            Write-Error "Skill file already exists: $Destination. Use -Force to overwrite."
            exit 1
        }
    }

    # Create temp zip
    $tempZip = [System.IO.Path]::GetTempFileName()
    Remove-Item $tempZip  # Remove the temp file, we just want the path
    $tempZip = $tempZip + ".zip"

    # Compress folder contents (not the folder itself)
    Compress-Archive -Path "$Source\*" -DestinationPath $tempZip -Force

    # Rename to .skill
    Move-Item -Path $tempZip -Destination $Destination -Force

    Write-Host "Packed skill: $Destination" -ForegroundColor Green

    # Calculate size
    $size = (Get-Item $Destination).Length
    $sizeKB = [math]::Round($size / 1024, 1)
    Write-Host "Size: ${sizeKB} KB" -ForegroundColor Gray

    return $Destination
}

function Edit-Skill {
    param([string]$SkillFile)

    # Unpack
    $editFolder = Unpack-Skill -Source $SkillFile -Destination $EditPath

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "Skill unpacked for editing at:" -ForegroundColor Yellow
    Write-Host "  $editFolder" -ForegroundColor White
    Write-Host ""
    Write-Host "Edit the files, then press ENTER to repack." -ForegroundColor Yellow
    Write-Host "Press Ctrl+C to cancel (changes will remain unpacked)." -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""

    # Wait for user
    Read-Host "Press ENTER when done editing"

    # Repack
    Pack-Skill -Source $editFolder -Destination $SkillFile

    # Cleanup edit folder
    Write-Host "Cleaning up edit folder..." -ForegroundColor Gray
    Remove-Item -Path $editFolder -Recurse -Force

    Write-Host "Done!" -ForegroundColor Green
}

# Main execution
switch ($Action) {
    "unpack" {
        Unpack-Skill -Source $SkillPath -Destination $EditPath
    }
    "pack" {
        # For pack, SkillPath is the source folder, EditPath is the destination .skill
        if (-not $EditPath -or $EditPath -eq "") {
            $EditPath = $SkillPath -replace "-edit$", ""
            $EditPath = $EditPath + ".skill"
        }
        Pack-Skill -Source $SkillPath -Destination $EditPath
    }
    "edit" {
        Edit-Skill -SkillFile $SkillPath
    }
}
