<#
.SYNOPSIS
    Single-command RC runner for onto-tools-prp on Windows.

.DESCRIPTION
    Activates the 'onto-tools-artigo' conda environment, installs the package in
    editable mode, and runs the full canonical RC pipeline via run_rc.py.
    Propagates the exit code from run_rc.py.

.EXAMPLE
    .\scripts\rc.ps1
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot

# ── Locate conda ────────────────────────────────────────────────
$CondaExe = $null
foreach ($candidate in @(
    "$env:CONDA_EXE",
    "$env:USERPROFILE\miniconda3\Scripts\conda.exe",
    "$env:USERPROFILE\anaconda3\Scripts\conda.exe",
    "C:\ProgramData\miniconda3\Scripts\conda.exe",
    "C:\ProgramData\anaconda3\Scripts\conda.exe"
)) {
    if ($candidate -and (Test-Path $candidate)) {
        $CondaExe = $candidate
        break
    }
}

if (-not $CondaExe) {
    # Try conda on PATH
    $CondaExe = (Get-Command conda -ErrorAction SilentlyContinue)?.Source
}

if (-not $CondaExe) {
    Write-Error "conda not found. Install Miniconda/Anaconda or set CONDA_EXE."
    exit 1
}

Write-Host "Using conda: $CondaExe"

# ── Install package in editable mode ────────────────────────────
Write-Host "`n[1/2] Installing package (editable)..."
& $CondaExe run -n onto-tools-artigo --no-capture-output `
    python -m pip install --quiet -e $RepoRoot
if ($LASTEXITCODE -ne 0) {
    Write-Error "pip install -e . failed (exit $LASTEXITCODE)"
    exit $LASTEXITCODE
}

# ── Run the canonical RC pipeline ───────────────────────────────
Write-Host "`n[2/2] Running run_rc.py..."
& $CondaExe run -n onto-tools-artigo --no-capture-output `
    python "$RepoRoot\scripts\run_rc.py"
$rc = $LASTEXITCODE

Write-Host "`nrun_rc.py exited with code $rc"
exit $rc
