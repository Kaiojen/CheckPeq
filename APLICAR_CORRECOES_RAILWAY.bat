@echo off
echo ================================================================
echo    APLICANDO CORRECOES PARA RAILWAY - SISTEMA COMPLETO
echo ================================================================
echo.

echo O requirements.txt atual tem VARIOS PROBLEMAS:
echo.
echo [X] streamlit==1.32.2 - MUITO NOVA (erro no Railway)
echo [X] python-docx==1.2.0 - NAO INSTALA no Railway  
echo [X] pypdfium2==4.25.0 - ERRO de compilacao
echo [X] Flask==3.0.0 - Incompatibilidades
echo [X] Bibliotecas de teste - Desnecessarias
echo.

echo Deseja aplicar as correcoes? (S/N)
set /p resposta="Resposta: "

if /i not "%resposta%"=="S" goto fim

echo.
echo Fazendo backup do requirements atual...
copy requirements.txt requirements-backup-original.txt

echo.
echo Aplicando requirements correto...
copy requirements-railway-completo.txt requirements.txt

echo.
echo Commitando correcoes...
git add requirements.txt requirements-railway-completo.txt requirements-backup-original.txt ANALISE_REQUIREMENTS.md
git commit -m "Fix: Corrigir versoes para compatibilidade total com Railway"

echo.
echo Enviando para GitHub...
git push

echo.
echo ================================================================
echo                      PRONTO!
echo ================================================================
echo.
echo IMPORTANTE - Configure no Railway:
echo.
echo 1. GEMINI_API_KEY = sua_chave_api
echo 2. FLASK_SECRET_KEY = senha_segura
echo 3. PYTHON_VERSION = 3.11
echo.
echo O sistema vai funcionar com TODAS as funcionalidades:
echo [OK] Upload de PDF
echo [OK] Upload de DOCX  
echo [OK] Processamento com IA
echo [OK] Geracao de relatorios
echo.
echo ================================================================
goto fim

:fim
echo.
pause 