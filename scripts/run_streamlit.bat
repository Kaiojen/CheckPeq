@echo off
echo ===================================================
echo Sistema de Verificacao IN SEGES 65/2021 - STREAMLIT
echo ===================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado! Por favor, instale o Python 3.8 ou superior.
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Instalar dependencias se necessario
echo Verificando dependencias...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
)

REM Criar pastas necessarias
if not exist "uploads" mkdir uploads
if not exist "reports" mkdir reports
if not exist "database" mkdir database

REM Iniciar aplicacao Streamlit
echo.
echo Iniciando aplicacao Streamlit...
echo.
echo O sistema sera aberto em seu navegador automaticamente.
echo Se nao abrir, acesse: http://localhost:8501
echo.
echo Para parar o servidor, pressione Ctrl+C
echo.
echo ===================================================

streamlit run src/app_streamlit.py

pause 