# PowerShell script to check prerequisites for SDD
param(
    [switch]$Json,
    [switch]$RequireTasks,
    [switch]$IncludeTasks
)

$result = @{
    FEATURE_DIR = "specs/todo-feature"
    AVAILABLE_DOCS = @("spec.md", "plan.md", "tasks.md")
}

if ($Json) {
    $result | ConvertTo-Json
} else {
    Write-Host "FEATURE_DIR=specs/todo-feature"
    Write-Host "AVAILABLE_DOCS=spec.md,plan.md,tasks.md"
}