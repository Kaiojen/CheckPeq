@echo off
echo ===================================================
echo Sistema de Verificacao IN SEGES 65/2021 - FLASK
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
if not exist "src\uploads" mkdir src\uploads
if not exist "src\temp" mkdir src\temp

REM Iniciar aplicacao Flask
echo.
echo Iniciando aplicacao Flask...
echo.
echo Acesse o sistema em: http://localhost:5000
echo.
echo Para parar o servidor, pressione Ctrl+C
echo.
echo ===================================================

cd src
python main.py

pause 