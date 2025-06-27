@echo off
echo ========================================
echo TESTADOR DO SISTEMA - IN SEGES 65/2021
echo ========================================
echo.

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

echo.
echo Verificando instalacao...
echo.
python test_install.py
echo.
echo ========================================
echo.

echo Escolha qual versao testar:
echo.
echo 1 - Versao 2.0 (NOVA - Otimizada para Web)
echo 2 - Versao 1.0 (Original)
echo 3 - Sair
echo.

set /p opcao="Digite o numero da opcao: "

if "%opcao%"=="1" (
    echo.
    echo Iniciando Sistema v2.0...
    echo O navegador abrira automaticamente em alguns segundos.
    echo.
    echo Para parar o servidor, pressione Ctrl+C
    echo.
    streamlit run src/app_v2.py
) else if "%opcao%"=="2" (
    echo.
    echo Iniciando Sistema v1.0...
    echo O navegador abrira automaticamente em alguns segundos.
    echo.
    echo Para parar o servidor, pressione Ctrl+C
    echo.
    streamlit run src/app_streamlit.py
) else (
    echo Saindo...
)

pause 