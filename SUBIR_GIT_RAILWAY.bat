@echo off
setlocal enabledelayedexpansion
cls

echo ================================================================
echo           ASSISTENTE DE DEPLOY GITHUB + RAILWAY
echo ================================================================
echo.
echo Este script vai te ajudar a subir seu projeto pro GitHub
echo e fazer deploy no Railway!
echo.
pause

:menu
cls
echo ================================================================
echo                    MENU PRINCIPAL
echo ================================================================
echo.
echo [1] Verificar se Git esta instalado
echo [2] Configurar Git (primeira vez)
echo [3] Criar .gitignore (importante!)
echo [4] Subir projeto pro GitHub
echo [5] Abrir Railway para deploy
echo [6] Gerar comandos manuais
echo [7] Ver guia completo
echo [0] Sair
echo.
set /p opcao="Escolha uma opcao: "

if "%opcao%"=="1" goto verificar_git
if "%opcao%"=="2" goto configurar_git
if "%opcao%"=="3" goto criar_gitignore
if "%opcao%"=="4" goto subir_github
if "%opcao%"=="5" goto abrir_railway
if "%opcao%"=="6" goto gerar_comandos
if "%opcao%"=="7" goto ver_guia
if "%opcao%"=="0" goto fim

goto menu

:verificar_git
cls
echo ================================================================
echo                 VERIFICANDO GIT
echo ================================================================
echo.
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Git NAO esta instalado!
    echo.
    echo Baixe em: https://git-scm.com/download/windows
    echo.
    echo Deseja abrir o site de download? [S/N]
    set /p abrir="Resposta: "
    if /i "!abrir!"=="S" start https://git-scm.com/download/windows
) else (
    echo [OK] Git esta instalado!
    git --version
)
echo.
pause
goto menu

:configurar_git
cls
echo ================================================================
echo                 CONFIGURAR GIT
echo ================================================================
echo.
echo Digite seus dados do GitHub:
echo.
set /p nome="Seu nome completo: "
set /p email="Seu email: "

git config --global user.name "%nome%"
git config --global user.email "%email%"

echo.
echo [OK] Git configurado!
echo Nome: %nome%
echo Email: %email%
echo.
pause
goto menu

:criar_gitignore
cls
echo ================================================================
echo                 CRIAR .GITIGNORE
echo ================================================================
echo.
echo Criando arquivo .gitignore para proteger arquivos sensíveis...
echo.

(
echo # Ambiente virtual
echo venv/
echo env/
echo ENV/
echo.
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo.
echo # Arquivos de configuração
echo .env
echo .env.local
echo .env.production
echo config.ini
echo.
echo # Banco de dados
echo *.db
echo *.sqlite3
echo *.sqlite
echo.
echo # Logs
echo logs/
echo *.log
echo.
echo # Arquivos temporários
echo temp/
echo tmp/
echo *.tmp
echo.
echo # Uploads (se não quiser versionar)
echo uploads/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # OS
echo Thumbs.db
echo .DS_Store
echo desktop.ini
) > .gitignore

echo [OK] Arquivo .gitignore criado!
echo.
echo Arquivos que NAO serao enviados pro GitHub:
type .gitignore | findstr /v "^#" | findstr /v "^$"
echo.
pause
goto menu

:subir_github
cls
echo ================================================================
echo              SUBIR PROJETO PRO GITHUB
echo ================================================================
echo.
echo IMPORTANTE: Voce precisa primeiro criar um repositorio no GitHub!
echo.
echo Ja criou o repositorio no GitHub? [S/N]
set /p criou="Resposta: "

if /i not "!criou!"=="S" (
    echo.
    echo PASSOS PARA CRIAR:
    echo 1. Acesse https://github.com
    echo 2. Clique no + no canto superior direito
    echo 3. Clique em "New repository"
    echo 4. Nome: sistema-verificacao
    echo 5. Deixe Public marcado
    echo 6. NAO marque nenhuma outra opcao
    echo 7. Clique em "Create repository"
    echo.
    echo Deseja abrir o GitHub? [S/N]
    set /p abrir="Resposta: "
    if /i "!abrir!"=="S" start https://github.com/new
    pause
    goto menu
)

echo.
echo Digite seu nome de usuario do GitHub:
set /p usuario="Usuario: "

echo.
echo Iniciando processo de upload...
echo.

rem Verificar se já existe .git
if exist .git (
    echo [!] Repositorio Git ja existe. Continuando...
) else (
    echo [*] Inicializando Git...
    git init
)

echo.
echo [*] Adicionando arquivos...
git add .

echo.
echo [*] Criando commit...
git commit -m "Deploy inicial - Sistema de Verificacao" 2>nul
if %errorlevel% neq 0 (
    echo [!] Nada para commitar ou erro no commit
)

echo.
echo [*] Conectando ao GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/%usuario%/sistema-verificacao.git

echo.
echo [*] Enviando para o GitHub...
echo.
echo ATENCAO: Se pedir senha, use seu TOKEN do GitHub (nao a senha normal)!
echo.
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo              SUCESSO! PROJETO NO GITHUB!
    echo ================================================================
    echo.
    echo URL do seu repositorio:
    echo https://github.com/%usuario%/sistema-verificacao
    echo.
    echo Proximo passo: Deploy no Railway!
) else (
    echo.
    echo [ERRO] Falha ao enviar. Possiveis causas:
    echo 1. Usuario incorreto
    echo 2. Repositorio nao existe
    echo 3. Precisa criar um token
    echo.
    echo Para criar token:
    echo GitHub > Settings > Developer settings > Personal access tokens
)

echo.
pause
goto menu

:abrir_railway
cls
echo ================================================================
echo                    RAILWAY DEPLOY
echo ================================================================
echo.
echo Abrindo Railway no navegador...
echo.
echo PASSOS NO RAILWAY:
echo 1. Clique em "Start a New Project"
echo 2. Login com GitHub
echo 3. Clique em "New Project"
echo 4. Selecione "Deploy from GitHub repo"
echo 5. Escolha "sistema-verificacao"
echo 6. Configure as variaveis:
echo    - GEMINI_API_KEY
echo    - FLASK_SECRET_KEY
echo    - PORT = 5000
echo.
start https://railway.app
pause
goto menu

:gerar_comandos
cls
echo ================================================================
echo                 COMANDOS MANUAIS
echo ================================================================
echo.
echo Copie e cole estes comandos no CMD:
echo.
echo --- CONFIGURAR GIT ---
echo git config --global user.name "Seu Nome"
echo git config --global user.email "seuemail@example.com"
echo.
echo --- SUBIR PRO GITHUB ---
echo git init
echo git add .
echo git commit -m "Primeiro commit"
echo git remote add origin https://github.com/SEU-USUARIO/sistema-verificacao.git
echo git push -u origin main
echo.
echo --- ATUALIZAR MUDANCAS ---
echo git add .
echo git commit -m "Atualizacao"
echo git push
echo.
echo Deseja copiar os comandos? [S/N]
set /p copiar="Resposta: "
if /i "!copiar!"=="S" (
    echo git init; git add .; git commit -m "Deploy"; git push -u origin main | clip
    echo.
    echo [OK] Comandos copiados para a area de transferencia!
)
echo.
pause
goto menu

:ver_guia
cls
echo Abrindo guia completo...
start notepad GUIA_RAILWAY_COMPLETO.md
goto menu

:fim
echo.
echo Encerrando...
timeout /t 2 /nobreak >nul
exit 