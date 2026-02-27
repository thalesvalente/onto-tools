Param([string]$YamlPath = "")

# 1) Auto-descoberta do YAML (.yml ou .yaml)
# Procura primeiro na raiz do projeto (um nível acima de scripts/)
$projectRoot = Split-Path -Parent $PSScriptRoot
$cwd = $projectRoot
$candidates = @()
if ($YamlPath -ne "") { $candidates += $YamlPath }
$candidates += @(
    (Join-Path $projectRoot "environment.yml"),
    (Join-Path $projectRoot "environment.yaml")
)
$YamlFile = $null
foreach ($c in $candidates) {
  if (Test-Path $c) { $YamlFile = $c; break }
}
if (-not $YamlFile) { throw "Nenhum arquivo environment.yml/.yaml encontrado. Use -YamlPath <caminho>." }
Write-Host ">> YAML detectado: $YamlFile" -ForegroundColor Cyan

# 2) Pré-validação **permissiva** do YAML (formato/estrutura)
$txt = Get-Content -Raw -Path $YamlFile -EA Stop
if ($txt -match "`t") { Write-Warning "Arquivo contém TABs (não recomendado em YAML)." }
$hasName = $txt -match '(?im)^\s*name\s*:'
$hasChannels = $txt -match '(?im)^\s*channels\s*:'
$hasDeps = $txt -match '(?im)^\s*dependencies\s*:'
if (-not ($hasName -and $hasChannels -and $hasDeps)) {
  throw "Spec inválida: YAML precisa ter chaves 'name:', 'channels:' e 'dependencies:' (inline ou multilinha)."
}

# 3) PM (mamba/conda) + localizar CONDA_EXE
$condaCmd = (Get-Command conda -EA SilentlyContinue)
$mambaCmd = (Get-Command mamba -EA SilentlyContinue)
if (-not $condaCmd -and -not $mambaCmd) {
  throw "Conda/Mamba não encontrados no PATH. Rode 'conda init powershell' e abra nova sessão."
}
$pm = if ($mambaCmd) { "mamba" } else { "conda" }
$condaExe = $Env:CONDA_EXE
if (-not $condaExe -or -not (Test-Path $condaExe)) {
  $condaExe = (Get-Command conda.exe -EA SilentlyContinue)?.Source
}
if (-not $condaExe -or -not (Test-Path $condaExe)) {
  $condaExe = (Get-Command conda -EA SilentlyContinue)?.Source
}

# 4) Inicializar hook do conda na própria sessão (se possível)
try {
  if ($condaExe) {
    $hook = & $condaExe "shell.powershell" "hook" 2>$null
    if ($hook) { Invoke-Expression $hook }
  }
} catch {}

# 5) Nome do ambiente
$envName = [regex]::Match($txt, '(?im)^\s*name\s*:\s*(.+)$').Groups[1].Value.Trim()
if (-not $envName) { $envName = "onto-tools" }
Write-Host ">> Ambiente alvo: $envName" -ForegroundColor Cyan

# 6) Criar/Atualizar
$exists = & $pm env list | Select-String -Pattern ("^\s*{0}\s" -f [regex]::Escape($envName)) | Measure-Object | Select-Object -ExpandProperty Count
if ($exists -gt 0) {
  Write-Host ">> Ambiente existe. Atualizando a partir do YAML..." -ForegroundColor Green
  & $pm env update -n $envName -f $YamlFile --prune
} else {
  Write-Host ">> Criando ambiente a partir do YAML..." -ForegroundColor Green
  & $pm env create -f $YamlFile
}

# 7) Ativar (melhor esforço) + verificação sem ativar
$activated = $false
try {
  if (Get-Command conda -EA SilentlyContinue) {
    conda activate $envName
    $activated = $true
  }
} catch {}
if (-not $activated) {
  Write-Warning ("Não foi possível ativar automaticamente. Para ativar, rode: & {0} shell.powershell hook | Out-String | Invoke-Expression; conda activate {1}" -f $condaExe, $envName)
}

# 8) Versões (sem depender de activate)
Write-Host ">> Versões (sanity check sem 'activate'):" -ForegroundColor Cyan
& $pm --version
if ($condaExe) { & $condaExe "--version" }
& $pm run -n $envName --no-capture-output python --version
& $pm run -n $envName --no-capture-output pip --version