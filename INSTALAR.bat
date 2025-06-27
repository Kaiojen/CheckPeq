@echo off
chcp 65001 > nul
title Sistema de Verificação v2.0 - Instalador Detalhado

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         📦 INSTALADOR DO SISTEMA DE VERIFICAÇÃO v2.0             ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Este script irá configurar o ambiente e instalar as dependências.
echo Por favor, observe a saída para qualquer mensagem de erro.
echo.

:: Mover para o diretório do script
cd /d "%~dp0"

:: 1. Verificar Python
echo [1/5] Verificando instalação do Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Por favor, instale o Python 3.8+
    echo    Visite: https://www.python.org/downloads/
    pause
    exit /b
)
echo  + Python encontrado!
echo.

:: 2. Criar ou recriar Ambiente Virtual
echo [2/5] Criando/Limpando ambiente virtual na pasta 'venv'...
if exist venv (
    echo  + Removendo venv antigo para uma instalação limpa...
    rmdir /s /q venv
)
python -m venv venv
echo  + Ambiente virtual 'venv' criado.
echo.

:: 3. Ativar e Instalar Dependências
echo [3/5] Ativando ambiente e instalando dependências de 'requirements.txt'...
call venv\Scripts\activate.bat
echo.
echo [3.1] Atualizando pip...
python.exe -m pip install --upgrade pip
echo.
echo [3.2] Instalando pacotes... (Isso pode levar alguns minutos)
python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências. Verifique as mensagens acima.
    pause
    exit /b
)
echo  + Dependências instaladas com sucesso.
echo.

:: 4. Verificar Instalação
echo [4/5] Verificando se o Streamlit foi instalado corretamente...
python.exe -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO CRÍTICO: O Streamlit não foi encontrado no ambiente virtual.
    echo    A instalação falhou. Por favor, verifique os erros acima.
    pause
    exit /b
)
echo  + Streamlit verificado com sucesso!
echo.


:: 5. Configurar Arquivo de Ambiente
echo [5/5] Configurando arquivo de ambiente '.env'...
if not exist .env (
    echo  + Criando arquivo '.env' a partir do exemplo...
    copy env.example .env > nul
    echo.
    echo ----------------- IMPORTANTE -----------------
    echo.
    echo  Um arquivo chamado '.env' foi criado.
    echo  Abra este arquivo e adicione sua GOOGLE_API_KEY.
    echo.
    echo ----------------------------------------------
) else (
    echo  + Arquivo '.env' já existe. Nenhuma alteração foi feita.
)
echo.

echo.
echo ✅ **Instalação e verificação concluídas com sucesso!**
echo.
echo Para iniciar o sistema, execute o arquivo:
echo    EXECUTAR.bat
echo.
pause 