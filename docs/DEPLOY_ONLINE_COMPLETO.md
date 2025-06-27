# 🚀 GUIA COMPLETO DE DEPLOY ONLINE

## ⚠️ IMPORTANTE: VOCÊ PRECISA INSTALAR ALGUMAS COISAS!

### 📋 O QUE PRECISA SER INSTALADO/CONFIGURADO:

## 🔴 MÉTODO 1: DEPLOY COM DOCKER (MAIS FÁCIL)

### No Servidor, você precisa instalar:

1. **Docker** e **Docker Compose**
2. **Git** (para clonar o projeto)
3. **Nginx** (para proxy reverso)
4. **Certbot** (para SSL/HTTPS)

### Passo a Passo:

```bash
# 1. Acessar o servidor (SSH)
ssh seu_usuario@seu_servidor.com

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# 4. Clonar seu projeto
git clone https://github.com/seu-usuario/sistema_verificacao_final.git
cd sistema_verificacao_final

# 5. Configurar variáveis de ambiente
cp env.example .env
nano .env  # Editar com suas configurações

# 6. Iniciar o sistema
sudo docker-compose up -d
```

## 🟡 MÉTODO 2: DEPLOY TRADICIONAL (VPS/Servidor)

### No Servidor, você precisa instalar:

1. **Python 3.11+**
2. **pip** e **virtualenv**
3. **PostgreSQL** ou **MySQL**
4. **Redis** (para cache)
5. **Nginx** (servidor web)
6. **Gunicorn** (servidor WSGI)
7. **Supervisor** (gerenciador de processos)
8. **Certbot** (para SSL)

### Passo a Passo:

```bash
# 1. Instalar Python e dependências do sistema
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install redis-server
sudo apt-get install nginx supervisor

# 2. Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# 3. Instalar dependências Python
pip install -r requirements.txt
pip install gunicorn

# 4. Configurar banco de dados
sudo -u postgres createdb sistema_verificacao
sudo -u postgres createuser -P seu_usuario

# 5. Configurar Nginx
sudo nano /etc/nginx/sites-available/sistema_verificacao
# (adicionar configuração)

# 6. Configurar Supervisor
sudo nano /etc/supervisor/conf.d/sistema_verificacao.conf
# (adicionar configuração)

# 7. Iniciar serviços
sudo systemctl restart nginx
sudo supervisorctl reread
sudo supervisorctl update
```

## 🟢 MÉTODO 3: DEPLOY EM PLATAFORMA CLOUD

### Opção A: Heroku (Grátis limitado)

```bash
# 1. Instalar Heroku CLI localmente
# Download em: https://devcenter.heroku.com/articles/heroku-cli

# 2. Criar conta no Heroku
# https://signup.heroku.com/

# 3. Preparar o projeto
heroku create nome-do-seu-app
heroku addons:create heroku-postgresql:hobby-dev
heroku addons:create heroku-redis:hobby-dev

# 4. Configurar variáveis
heroku config:set GEMINI_API_KEY=sua_chave_aqui
heroku config:set FLASK_SECRET_KEY=sua_chave_secreta

# 5. Deploy
git push heroku main
```

### Opção B: Railway (Mais simples)

1. Criar conta em https://railway.app/
2. Conectar GitHub
3. Selecionar repositório
4. Adicionar variáveis de ambiente
5. Deploy automático!

### Opção C: AWS/Google Cloud/Azure

**Requisitos mais complexos:**

- Configurar VPC, Security Groups
- Configurar Load Balancer
- Configurar Auto Scaling
- Configurar RDS para banco
- Configurar S3 para arquivos

## 📁 ARQUIVOS NECESSÁRIOS PARA DEPLOY

### 1. Procfile (para Heroku)

```
web: gunicorn src.app:app
```

### 2. runtime.txt (para Heroku)

```
python-3.11.5
```

### 3. .env (configurações)

```
GEMINI_API_KEY=sua_chave_api
DATABASE_URL=postgresql://usuario:senha@localhost/db
REDIS_URL=redis://localhost:6379
FLASK_SECRET_KEY=chave_secreta_segura
```

## 🔒 CONFIGURAÇÕES DE SEGURANÇA OBRIGATÓRIAS

1. **SSL/HTTPS** - Certificado SSL (Let's Encrypt grátis)
2. **Firewall** - Configurar portas
3. **Variáveis de Ambiente** - Nunca commitar senhas
4. **Backup** - Configurar backup automático
5. **Monitoramento** - Configurar alertas

## 💰 CUSTOS ESTIMADOS

### Opções Gratuitas (com limitações):

- **Heroku Free** - 550 horas/mês
- **Railway Starter** - $5 créditos/mês
- **Oracle Cloud Free** - VM sempre grátis

### Opções Pagas:

- **VPS Básico** - $5-20/mês (DigitalOcean, Linode)
- **Heroku Hobby** - $7/mês
- **AWS/GCP** - Pay as you go

## 🚨 CHECKLIST PRÉ-DEPLOY

- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados criado
- [ ] Dependências instaladas
- [ ] Domínio configurado (opcional)
- [ ] SSL configurado
- [ ] Backup configurado
- [ ] Logs configurados
- [ ] Testes executados

## 📱 MONITORAMENTO PÓS-DEPLOY

### Ferramentas Recomendadas:

- **UptimeRobot** - Monitoramento grátis
- **Sentry** - Logs de erro
- **New Relic** - Performance (tem plano grátis)

## ⚡ COMANDOS RÁPIDOS

### Docker:

```bash
# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Parar
docker-compose down
```

### Tradicional:

```bash
# Ver logs
tail -f /var/log/nginx/error.log

# Reiniciar app
sudo supervisorctl restart sistema_verificacao

# Status
sudo supervisorctl status
```

## 🆘 PROBLEMAS COMUNS

1. **"502 Bad Gateway"** - App não está rodando
2. **"Connection refused"** - Firewall bloqueando
3. **"Module not found"** - Dependências não instaladas
4. **"Permission denied"** - Permissões de arquivo

## 📞 SUPORTE

Se precisar de ajuda:

1. Verifique os logs
2. Teste localmente primeiro
3. Verifique as variáveis de ambiente
4. Confirme que todas as dependências estão instaladas

---

**RESUMO: SIM, VOCÊ PRECISA INSTALAR VÁRIAS COISAS NO SERVIDOR!**

O mais fácil é usar:

1. **Railway/Heroku** para teste rápido
2. **Docker** para produção
3. **VPS tradicional** se quiser controle total
