@echo off
echo ==========================================
echo   CONFIGURADOR DE API KEY - GOOGLE GEMINI
echo ==========================================
echo.
echo Este assistente vai ajudar voce a configurar
echo a chave da API necessaria para o sistema.
echo.
echo PRIMEIRO, OBTENHA SUA CHAVE GRATUITA:
echo --------------------------------------
echo 1. Acesse: https://makersuite.google.com/app/apikey
echo 2. Faca login com Google
echo 3. Clique em "Create API Key"
echo 4. Copie a chave (comeca com AIza...)
echo.
echo Pressione qualquer tecla quando tiver a chave...
pause > nul
echo.
echo ==========================================
echo.
set /p API_KEY="AIzaSyBV2_ME3XuWbKhJ-zSURhqm2RKDW5hl9Y0 "
echo.

if "%API_KEY%"=="" (
    echo [ERRO] Chave nao pode estar vazia!
    pause
    exit /b 1
)

echo Configurando a chave...
echo.

REM Criar pasta se nao existir
if not exist ".streamlit" mkdir .streamlit

REM Salvar no arquivo secrets.toml
echo GOOGLE_API_KEY = "%API_KEY%" > .streamlit\secrets.toml

REM Tambem configurar como variavel de ambiente
setx GOOGLE_API_KEY "%API_KEY%" > nul 2>&1

echo ==========================================
echo   CONFIGURACAO CONCLUIDA COM SUCESSO!
echo ==========================================
echo.
echo A chave foi salva em:
echo - Arquivo: .streamlit\secrets.toml
echo - Variavel de ambiente: GOOGLE_API_KEY
echo.
echo Agora voce pode executar o sistema!
echo.
pause 