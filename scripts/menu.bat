@echo off
setlocal
echo.
echo ========================================
echo   ONTO-TOOLS - Menu Interativo
echo ========================================
echo.

REM Delegar para o script PowerShell
powershell -ExecutionPolicy Bypass -File "%~dp0menu.ps1"

