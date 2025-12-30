# META-LOOP IMPROVEMENT MONITOR - SCHEDULED TASK SETUP
#
# Creates a Windows Scheduled Task that runs every 3 days
# to monitor improvement metrics and auto-trigger rollbacks
#
# Usage: .\setup-metaloop-monitor-schedule.ps1

$ErrorActionPreference = "Stop"

$TaskName = "MetaLoopImprovementMonitor"
$ScriptPath = Join-Path $PSScriptRoot "monitor-metaloop-improvements.js"
$LogPath = Join-Path $env:USERPROFILE ".claude\logs\metaloop-monitor.log"

# Ensure log directory exists
$LogDir = Split-Path $LogPath -Parent
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    Write-Host "[SETUP] Created log directory: $LogDir"
}

# Check if Node.js is available
$NodePath = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $NodePath) {
    Write-Error "Node.js not found in PATH. Please install Node.js first."
    exit 1
}

Write-Host @"

=== META-LOOP IMPROVEMENT MONITOR SETUP ===

Task Name:     $TaskName
Script:        $ScriptPath
Node:          $NodePath
Log:           $LogPath
Interval:      Every 3 days

"@

# Create the scheduled task action
$Action = New-ScheduledTaskAction `
    -Execute $NodePath `
    -Argument "`"$ScriptPath`" --check-all >> `"$LogPath`" 2>&1"

# Create trigger for every 3 days at midnight
$Trigger = New-ScheduledTaskTrigger `
    -Daily `
    -DaysInterval 3 `
    -At "00:00"

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# Register the task
try {
    # Remove existing task if present
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "[INFO] Removing existing task..."
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create new task
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Description "Meta-Loop Improvement Monitor - Runs every 3 days to check metrics and auto-rollback if needed" `
        | Out-Null

    Write-Host "[SUCCESS] Scheduled task created successfully!"
    Write-Host ""
    Write-Host "To verify:"
    Write-Host "  Get-ScheduledTask -TaskName '$TaskName' | Format-List"
    Write-Host ""
    Write-Host "To run immediately:"
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'"
    Write-Host ""
    Write-Host "To view logs:"
    Write-Host "  Get-Content '$LogPath' -Tail 50"
    Write-Host ""

} catch {
    Write-Error "Failed to create scheduled task: $_"
    exit 1
}

# Also create a Memory MCP initialization for baseline
$BaselineScript = @"
/**
 * Initialize baseline metrics in Memory MCP
 * Run once after improvements are applied
 */
const baseline = {
  commit_id: 'commit-metaloop-stack-20251228',
  created: new Date().toISOString(),
  metrics: {
    'skill-generation-benchmark-v1:skill-forge': 0.91,
    'prompt-generation-benchmark-v1:prompt-architect': 0.86,
    'cognitive-frame-benchmark-v1:agent-creator': 0.84,
    'expertise-generation-benchmark-v1:skill-auditor': 0.85
  },
  thresholds: {
    regression_threshold: 0.03,
    check_interval_days: 3,
    max_monitor_days: 14
  }
};

console.log('Baseline to store in Memory MCP:');
console.log(JSON.stringify(baseline, null, 2));

// Memory MCP store command:
// mcp__memory-mcp__memory_store({
//   text: JSON.stringify(baseline),
//   metadata: {
//     key: 'improvement/monitors/commit-metaloop-stack-20251228/baseline',
//     namespace: 'improvement',
//     layer: 'long-term',
//     tags: { WHO: 'setup-script', WHEN: baseline.created, PROJECT: 'meta-loop-stack', WHY: 'baseline' }
//   }
// })
"@

$BaselinePath = Join-Path $PSScriptRoot "init-metaloop-baseline.js"
Set-Content -Path $BaselinePath -Value $BaselineScript

Write-Host "[CREATED] Baseline initialization script: $BaselinePath"
Write-Host ""
Write-Host "Run to initialize baseline:"
Write-Host "  node '$BaselinePath'"
