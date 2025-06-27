@echo off
setlocal enabledelayedexpansion
cls

echo =============================================================
echo           DEPLOY RAPIDO DO SISTEMA
echo =============================================================
echo.

echo Escolha o metodo de deploy:
echo.
echo [1] Railway (Mais facil - Recomendado)
echo [2] Heroku (Gratis com limitacoes)
echo [3] VPS com Docker
echo [4] VPS Tradicional
echo [5] Vercel (Frontend apenas)
echo [6] Preparar arquivos para deploy manual
echo [0] Sair
echo.

set /p opcao="Digite sua opcao: "

if "%opcao%"=="1" goto railway
if "%opcao%"=="2" goto heroku
if "%opcao%"=="3" goto docker
if "%opcao%"=="4" goto tradicional
if "%opcao%"=="5" goto vercel
if "%opcao%"=="6" goto preparar
if "%opcao%"=="0" goto fim

:railway
cls
echo =============================================================
echo           DEPLOY NO RAILWAY
echo =============================================================
echo.
echo PASSOS:
echo.
echo 1. Crie uma conta em: https://railway.app/
echo.
echo 2. Instale o Railway CLI:
echo    npm install -g @railway/cli
echo.
echo 3. Faca login:
echo    railway login
echo.
echo 4. Inicie o projeto:
echo    railway init
echo.
echo 5. Configure as variaveis de ambiente no painel Railway:
echo    - GEMINI_API_KEY
echo    - FLASK_SECRET_KEY
echo    - DATABASE_URL (sera criado automaticamente)
echo.
echo 6. Deploy:
echo    railway up
echo.
echo PRESSIONE QUALQUER TECLA PARA ABRIR O SITE DO RAILWAY...
pause >nul
start https://railway.app/
goto menu

:heroku
cls
echo =============================================================
echo           DEPLOY NO HEROKU
echo =============================================================
echo.
echo Verificando se Heroku CLI esta instalado...
where heroku >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Heroku CLI nao encontrado!
    echo.
    echo Baixe em: https://devcenter.heroku.com/articles/heroku-cli
    echo.
    pause
    goto menu
)

echo.
echo [OK] Heroku CLI encontrado!
echo.
echo Verificando se voce esta logado...
heroku auth:whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Fazendo login no Heroku...
    heroku login
)

echo.
echo Digite o nome do seu app (deixe vazio para gerar automatico):
set /p appname="Nome do app: "

if "%appname%"=="" (
    echo Criando app com nome automatico...
    heroku create
) else (
    echo Criando app: %appname%
    heroku create %appname%
)

echo.
echo Adicionando banco de dados PostgreSQL...
heroku addons:create heroku-postgresql:mini

echo.
echo Adicionando Redis...
heroku addons:create heroku-redis:mini

echo.
echo Configurando variaveis de ambiente...
set /p apikey="Digite sua GEMINI_API_KEY: "
heroku config:set GEMINI_API_KEY=%apikey%

echo.
echo Gerando SECRET_KEY...
heroku config:set FLASK_SECRET_KEY=%random%%random%%random%%random%

echo.
echo Fazendo deploy...
git add .
git commit -m "Deploy to Heroku"
git push heroku main

echo.
echo [CONCLUIDO] Abrindo app...
heroku open

pause
goto menu

:docker
cls
echo =============================================================
echo           DEPLOY COM DOCKER
echo =============================================================
echo.
echo COMANDOS PARA EXECUTAR NO SERVIDOR:
echo.
echo # 1. Instalar Docker:
echo curl -fsSL https://get.docker.com -o get-docker.sh
echo sudo sh get-docker.sh
echo.
echo # 2. Instalar Docker Compose:
echo sudo apt-get update
echo sudo apt-get install docker-compose-plugin
echo.
echo # 3. Clonar projeto:
echo git clone [SEU_REPOSITORIO]
echo cd sistema_verificacao_final
echo.
echo # 4. Configurar .env:
echo cp env.example .env
echo nano .env
echo.
echo # 5. Iniciar:
echo sudo docker-compose up -d
echo.
echo PRESSIONE QUALQUER TECLA PARA COPIAR COMANDOS...
pause >nul

echo curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh; sudo apt-get update; sudo apt-get install docker-compose-plugin | clip
echo.
echo [COPIADO] Comandos de instalacao copiados!
echo.
pause
goto menu

:tradicional
cls
echo =============================================================
echo           DEPLOY TRADICIONAL (VPS)
echo =============================================================
echo.
echo Gerando script de instalacao...

(
echo #!/bin/bash
echo # Script de instalacao automatica
echo.
echo echo "Atualizando sistema..."
echo sudo apt-get update -y
echo.
echo echo "Instalando Python 3.11..."
echo sudo apt-get install -y python3.11 python3.11-venv python3-pip
echo.
echo echo "Instalando PostgreSQL..."
echo sudo apt-get install -y postgresql postgresql-contrib
echo.
echo echo "Instalando Redis..."
echo sudo apt-get install -y redis-server
echo.
echo echo "Instalando Nginx..."
echo sudo apt-get install -y nginx
echo.
echo echo "Clonando projeto..."
echo git clone https://github.com/seu-usuario/sistema_verificacao_final.git
echo cd sistema_verificacao_final
echo.
echo echo "Criando ambiente virtual..."
echo python3.11 -m venv venv
echo source venv/bin/activate
echo.
echo echo "Instalando dependencias..."
echo pip install -r requirements.txt
echo pip install gunicorn
echo.
echo echo "Configurando banco de dados..."
echo sudo -u postgres createdb sistema_verificacao
echo.
echo echo "Deploy concluido!"
) > deploy_vps.sh

echo.
echo [OK] Script criado: deploy_vps.sh
echo.
echo Copie este arquivo para seu servidor e execute:
echo chmod +x deploy_vps.sh
echo ./deploy_vps.sh
echo.
pause
goto menu

:vercel
cls
echo =============================================================
echo           DEPLOY NO VERCEL (Frontend)
echo =============================================================
echo.
echo Instalando Vercel CLI...
npm install -g vercel

echo.
echo Fazendo deploy...
vercel

echo.
pause
goto menu

:preparar
cls
echo =============================================================
echo           PREPARANDO ARQUIVOS PARA DEPLOY
echo =============================================================
echo.

echo Verificando arquivos necessarios...
echo.

if exist Procfile (
    echo [OK] Procfile encontrado
) else (
    echo [!] Criando Procfile...
    echo web: gunicorn src.app:app > Procfile
)

if exist runtime.txt (
    echo [OK] runtime.txt encontrado
) else (
    echo [!] Criando runtime.txt...
    echo python-3.11.5 > runtime.txt
)

if exist requirements.txt (
    echo [OK] requirements.txt encontrado
) else (
    echo [ERRO] requirements.txt nao encontrado!
)

if exist .gitignore (
    echo [OK] .gitignore encontrado
) else (
    echo [!] Criando .gitignore...
    (
    echo venv/
    echo __pycache__/
    echo *.pyc
    echo .env
    echo *.db
    echo logs/
    echo uploads/
    echo temp/
    ) > .gitignore
)

echo.
echo Criando arquivo de variaveis de exemplo...
(
echo # Variaveis de Ambiente
echo GEMINI_API_KEY=sua_chave_aqui
echo FLASK_SECRET_KEY=gere_uma_chave_segura
echo DATABASE_URL=postgresql://user:pass@localhost/dbname
echo REDIS_URL=redis://localhost:6379
echo PORT=5000
echo ENVIRONMENT=production
) > .env.production

echo.
echo [OK] Arquivos preparados!
echo.
echo PROXIMOS PASSOS:
echo 1. Configure as variaveis em .env.production
echo 2. Faca commit das mudancas
echo 3. Escolha uma plataforma de deploy
echo.
pause
goto menu

:menu
cls
echo.
echo Deseja fazer mais alguma coisa?
echo [1] Voltar ao menu principal
echo [0] Sair
echo.
set /p cont="Opcao: "
if "%cont%"=="1" goto inicio
goto fim

:inicio
cls
echo =============================================================
echo           DEPLOY RAPIDO DO SISTEMA
echo =============================================================
echo.

echo Escolha o metodo de deploy:
echo.
echo [1] Railway (Mais facil - Recomendado)
echo [2] Heroku (Gratis com limitacoes)
echo [3] VPS com Docker
echo [4] VPS Tradicional
echo [5] Vercel (Frontend apenas)
echo [6] Preparar arquivos para deploy manual
echo [0] Sair
echo.

set /p opcao="Digite sua opcao: "

if "%opcao%"=="1" goto railway
if "%opcao%"=="2" goto heroku
if "%opcao%"=="3" goto docker
if "%opcao%"=="4" goto tradicional
if "%opcao%"=="5" goto vercel
if "%opcao%"=="6" goto preparar
if "%opcao%"=="0" goto fim

:fim
echo.
echo Encerrando...
timeout /t 2 /nobreak >nul
exit 