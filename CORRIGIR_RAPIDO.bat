@echo off
chcp 65001 > nul
title Correção Rápida do Sistema

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║         🔧 CORREÇÃO RÁPIDA DO SISTEMA                            ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1] Criando diretórios necessários...
mkdir database 2>nul
mkdir reports 2>nul
mkdir uploads 2>nul
mkdir temp 2>nul
mkdir logs 2>nul
echo ✅ Diretórios criados

echo.
echo [2] Verificando arquivo .env...
if not exist .env (
    echo Criando arquivo .env...
    echo # Configuração do Google Gemini AI > .env
    echo GOOGLE_API_KEY=sua_chave_aqui >> .env
    echo ✅ Arquivo .env criado - CONFIGURE SUA API KEY!
) else (
    echo ✅ Arquivo .env já existe
)

echo.
echo [3] Instalando dependências faltantes...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    pip install python-dotenv --quiet
    pip install streamlit --quiet
    echo ✅ Dependências instaladas
) else (
    echo ❌ Ambiente virtual não encontrado - Execute INSTALAR.bat primeiro
)

echo.
echo [4] Limpando arquivos temporários...
del /q temp\*.* 2>nul
del /q uploads\*.* 2>nul
echo ✅ Arquivos temporários limpos

echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
echo PRÓXIMOS PASSOS:
echo.
echo 1. Se você ainda não configurou a API do Google:
echo    - Execute CONFIGURAR_API.bat
echo.
echo 2. Para testar o sistema:
echo    - Execute TESTAR_SIMPLES.bat (versão simplificada)
echo    - Execute TESTAR_SISTEMA.bat (teste completo)
echo.
echo 3. Para executar o sistema:
echo    - Execute EXECUTAR.bat
echo.
pause 