#!/usr/bin/env pwsh
# Script PowerShell de setup do ambiente OntoTools
# Uso: .\scripts\setup.ps1

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  🔧 SETUP - OntoTools Environment" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Verificar se Conda está instalado
$condaCmd = Get-Command conda -ErrorAction SilentlyContinue
$mambaCmd = Get-Command mamba -ErrorAction SilentlyContinue

if (-not $condaCmd -and -not $mambaCmd) {
    Write-Host "❌ Conda/Mamba não encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instale Anaconda ou Miniconda:" -ForegroundColor Yellow
    Write-Host "  https://docs.anaconda.com/anaconda/install/" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

$pm = if ($mambaCmd) { "mamba" } else { "conda" }
Write-Host "✅ Package manager: $pm" -ForegroundColor Green

# Verificar se environment.yml existe
$envFile = Join-Path $PSScriptRoot "..\environment.yml"
if (-not (Test-Path $envFile)) {
    Write-Host "❌ Arquivo environment.yml não encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Arquivo: environment.yml" -ForegroundColor Green
Write-Host ""

# Criar/Atualizar ambiente
Write-Host "📦 Criando/Atualizando ambiente onto-tools-artigo..." -ForegroundColor Cyan
& $pm env create -f $envFile --force

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  ✅ AMBIENTE CRIADO COM SUCESSO!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "Para ativar:" -ForegroundColor Yellow
    Write-Host "  conda activate onto-tools-artigo" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Para instalar o pacote em modo desenvolvimento:" -ForegroundColor Yellow
    Write-Host "  pip install -e ." -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Erro ao criar ambiente!" -ForegroundColor Red
    exit 1
}
