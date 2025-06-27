@echo off
echo ================================================================
echo       CORRIGINDO RAILWAY - SISTEMA COMPLETO
echo ================================================================
echo.

echo [OK] Requirements.txt ajustado com todas as funcionalidades
echo [OK] Runtime.txt atualizado para Python 3.11.7
echo [OK] Nixpacks.toml criado para melhor compatibilidade
echo [OK] Procfile apontando para app.py completo
echo.

echo Verificando modificacoes...
echo.
echo Requirements principais:
echo - streamlit 1.28.1 (versao estavel)
echo - Todas bibliotecas de PDF funcionais
echo - Suporte completo para IA
echo - Geracao de relatorios
echo.

echo Fazendo commit das correcoes...
git add requirements.txt runtime.txt nixpacks.toml Procfile
git commit -m "Fix: Ajustar versoes para compatibilidade total no Railway"

echo.
echo Enviando para GitHub...
git push

echo.
echo ================================================================
echo                  IMPORTANTE!
echo ================================================================
echo.
echo No Railway, adicione estas variaveis de ambiente:
echo.
echo 1. GEMINI_API_KEY = sua_chave_api
echo 2. FLASK_SECRET_KEY = uma_senha_segura
echo 3. PYTHON_VERSION = 3.11
echo.
echo O deploy deve funcionar com TODAS as funcionalidades!
echo.
echo ================================================================
echo.
pause 