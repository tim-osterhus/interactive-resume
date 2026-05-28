param(
  [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Invoke-Native {
  param(
    [string]$Command,
    [string[]]$Arguments
  )
  & $Command @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "Command failed with exit code ${LASTEXITCODE}: $Command $($Arguments -join ' ')"
  }
}

function Invoke-Step($Name, [scriptblock]$Script) {
  Write-Host "`n== $Name =="
  & $Script
}

Invoke-Step "Backend install" {
  if (-not $SkipInstall) {
    Push-Location (Join-Path $RepoRoot "backend")
    try {
      Invoke-Native python @("-m", "pip", "install", "-e", ".[dev]")
    } finally {
      Pop-Location
    }
  }
}

Invoke-Step "Example ingest" {
  Push-Location (Join-Path $RepoRoot "backend")
  try {
    Invoke-Native python @("-m", "app.ingest", "--corpus", "../examples/raw-corpus")
  } finally {
    Pop-Location
  }
}

Invoke-Step "Backend tests" {
  Push-Location (Join-Path $RepoRoot "backend")
  try {
    Invoke-Native python @("-m", "pytest")
  } finally {
    Pop-Location
  }
}

Invoke-Step "Smoke eval" {
  Push-Location (Join-Path $RepoRoot "backend")
  try {
    Invoke-Native python @("-m", "app.evaluate", "--questions", "../examples/evals/smoke-questions.jsonl")
  } finally {
    Pop-Location
  }
}

Invoke-Step "Frontend install and tests" {
  Push-Location (Join-Path $RepoRoot "frontend")
  try {
    if (-not $SkipInstall) {
      Invoke-Native npm @("install")
    }
    Invoke-Native npm @("test")
    Invoke-Native npm @("run", "build")
  } finally {
    Pop-Location
  }
}

Invoke-Step "Public hygiene scan" {
  $secretHits = rg -n --hidden -g '!/.git/**' -g '!frontend/dist/**' -g '!backend/data/**' '(\bsk-[A-Za-z0-9_]{16,}\b|BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY|password\s*=|api[_-]?key\s*=)' $RepoRoot
  if ($LASTEXITCODE -eq 0) {
    throw "Secret-shaped strings found:`n$secretHits"
  }
  if ($LASTEXITCODE -gt 1) {
    throw "rg failed during secret scan"
  }

  $privateCorpus = git -C $RepoRoot status --short -- raw-corpus private-corpus backend/data/index
  if ($privateCorpus) {
    throw "Private/generated corpus or index files appear in git status:`n$privateCorpus"
  }
}

Write-Host "`nTemplate verification completed."
