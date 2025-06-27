@echo off
chcp 65001 > nul
title Diagnóstico do Sistema v2.0

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         🔍 DIAGNÓSTICO COMPLETO DO SISTEMA                       ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1] Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python não encontrado!
    pause
    exit /b
)
echo.

echo [2] Verificando ambiente virtual...
if exist venv\Scripts\activate.bat (
    echo ✅ Ambiente virtual existe
    call venv\Scripts\activate.bat
) else (
    echo ❌ Ambiente virtual não encontrado!
    pause
    exit /b
)
echo.

echo [3] Testando importações críticas...
echo.
echo Testando Streamlit...
python -c "import streamlit; print('✅ Streamlit OK')" 2>&1

echo.
echo Testando outras dependências...
python -c "import pandas; print('✅ Pandas OK')" 2>&1
python -c "import pdfplumber; print('✅ PDFPlumber OK')" 2>&1
python -c "import docx; print('✅ Python-docx OK')" 2>&1
python -c "import google.generativeai; print('✅ Google AI OK')" 2>&1

echo.
echo [4] Verificando módulos do sistema...
python -c "import sys; sys.path.insert(0, 'src'); from config import *; print('✅ Config OK')" 2>&1
python -c "import sys; sys.path.insert(0, 'src'); from security import *; print('✅ Security OK')" 2>&1
python -c "import sys; sys.path.insert(0, 'src'); from utils import *; print('✅ Utils OK')" 2>&1

echo.
echo [5] Verificando arquivo .env...
if exist .env (
    echo ✅ Arquivo .env existe
    python -c "from dotenv import load_dotenv; import os; load_dotenv(); key=os.getenv('GOOGLE_API_KEY'); print(f'API Key configurada: {"Sim" if key else "Não"}')"
) else (
    echo ❌ Arquivo .env não encontrado!
)

echo.
echo [6] Testando importação do app.py...
python -c "import sys; sys.path.insert(0, 'src'); import app; print('✅ App.py importado com sucesso')" 2>&1

echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
pause 