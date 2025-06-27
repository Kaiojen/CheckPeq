@echo off
chcp 65001 > nul
title Sistema de Verificação v2.0

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         🚀 EXECUTANDO SISTEMA DE VERIFICAÇÃO v2.0              ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

:: Mover para o diretório do script
cd /d "%~dp0"

:: Verificar se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo ⚠️  Ambiente virtual 'venv' não encontrado.
    echo    Por favor, execute o arquivo 'INSTALAR.bat' primeiro.
    echo.
    pause
    exit /b
)

:: Ativar ambiente virtual
echo 🔐 Ativando ambiente virtual seguro...
call venv\Scripts\activate.bat
echo.

:: Iniciar a aplicação
echo 🌐 Iniciando aplicação Streamlit...
echo    Acesse a URL no seu navegador. Pressione Ctrl+C para fechar.
echo.
python -m streamlit run src/app.py

pause 