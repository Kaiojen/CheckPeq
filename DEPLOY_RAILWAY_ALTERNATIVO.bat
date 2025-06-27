@echo off
echo ================================================================
echo          SOLUCAO ALTERNATIVA PARA RAILWAY
echo ================================================================
echo.

echo Este script oferece 2 solucoes para o erro de deploy:
echo.
echo [1] Usar requirements.txt atualizado
echo [2] Usar requirements-railway.txt (minimo)
echo.

set /p opcao="Escolha uma opcao (1 ou 2): "

if "%opcao%"=="1" goto atualizado
if "%opcao%"=="2" goto minimo

:atualizado
echo.
echo Usando requirements.txt atualizado...
echo.
echo Fazendo commit...
git add requirements.txt
git commit -m "Fix: Atualizar todas as dependencias para compatibilidade"
git push
echo.
echo PRONTO! O Railway deve fazer o deploy automaticamente.
goto fim

:minimo
echo.
echo Alternando para requirements minimo...
echo.

REM Renomear requirements atual
if exist requirements-full.txt del requirements-full.txt
rename requirements.txt requirements-full.txt

REM Usar o minimo
copy requirements-railway.txt requirements.txt

echo.
echo Fazendo commit...
git add requirements.txt requirements-railway.txt requirements-full.txt
git commit -m "Fix: Usar requirements minimo para Railway"
git push

echo.
echo PRONTO! Usando configuracao minima.
echo.
echo Para voltar ao completo depois:
echo   rename requirements-full.txt requirements.txt
goto fim

:fim
echo.
echo ================================================================
echo Se ainda houver erro, tente:
echo.
echo 1. No Railway, adicione a variavel:
echo    PYTHON_VERSION = 3.11.5
echo.
echo 2. Ou mude o Procfile para:
echo    web: pip install streamlit==1.32.2 && streamlit run src/app.py --server.port $PORT
echo ================================================================
echo.
pause 