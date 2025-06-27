@echo off
chcp 65001 > nul
title Teste Completo do Sistema

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         🔧 EXECUTANDO TESTE COMPLETO DO SISTEMA                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

python scripts\teste_completo.py

pause 