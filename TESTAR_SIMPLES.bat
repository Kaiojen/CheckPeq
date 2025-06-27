@echo off
chcp 65001 > nul
title Teste Simples do Sistema

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         🧪 EXECUTANDO VERSÃO SIMPLIFICADA PARA TESTES           ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✅ Ambiente virtual ativado
) else (
    echo ⚠️  Executando sem ambiente virtual
)

echo.
echo Iniciando versão simplificada...
python -m streamlit run src/app_simple.py

pause 