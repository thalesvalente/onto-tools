#!/usr/bin/env pwsh
# Script PowerShell para executar o menu CLI do OntoTools
# Uso: .\menu.ps1

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ONTO-TOOLS - Menu Interativo" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Tentar conda onto-tools-artigo
if (Get-Command conda -ErrorAction SilentlyContinue) {
    Write-Host "Ativando ambiente conda onto-tools-artigo..." -ForegroundColor Green
    # Conda requer inicialização especial no PowerShell
    $condaHook = "$env:CONDA_EXE" -replace "condabin\\conda.bat", "shell\condabin\conda-hook.ps1"
    if (Test-Path $condaHook) {
        . $condaHook
    }
    conda activate onto-tools-artigo
    Write-Host ""
    Write-Host "Iniciando menu interativo..." -ForegroundColor Green
    Write-Host ""
    python -m onto_tools.cli_menu
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit
}

# 4. Nenhum ambiente encontrado
Write-Host ""
Write-Host "=========================================================" -ForegroundColor Yellow
Write-Host "AVISO: Ambiente conda onto-tools-artigo nao encontrado!" -ForegroundColor Yellow
Write-Host "=========================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Configure o ambiente primeiro:"
Write-Host ""
Write-Host \"  conda create -n onto-tools-artigo python=3.12\"
Write-Host "  conda activate onto-tools-artigo"
Write-Host "  conda run -n onto-tools-artigo pip install -e ."
Write-Host ""
Write-Host "Consulte GUIA-EXECUCAO.md para detalhes."
Write-Host "=========================================================" -ForegroundColor Yellow
Write-Host ""
Read-Host "Pressione Enter para sair"
