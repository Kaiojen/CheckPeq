# 🚀 GUIA COMPLETO RAILWAY - DO ZERO AO DEPLOY

## 📌 RAILWAY É GRÁTIS? SIM!

- ✅ **Plano Starter**: US$ 5 de créditos GRÁTIS por mês
- ✅ **Suficiente** para projetos pequenos/médios
- ✅ **Sem cartão de crédito** necessário

---

## 📝 PARTE 1: CRIAR CONTA NO GITHUB

### 1.1 - Acessar o GitHub

1. Abra seu navegador
2. Digite: **https://github.com**
3. Clique em **"Sign up"** (canto superior direito)

### 1.2 - Preencher dados

1. **Username**: escolha um nome único (ex: seu-nome123)
2. **Email**: use um email válido
3. **Password**: crie uma senha forte
4. Resolva o captcha
5. Clique em **"Create account"**

### 1.3 - Verificar email

1. Abra seu email
2. Procure por "GitHub"
3. Clique no link de verificação

---

## 💻 PARTE 2: INSTALAR O GIT NO WINDOWS

### 2.1 - Baixar o Git

1. Acesse: **https://git-scm.com/download/windows**
2. O download começará automaticamente
3. Se não, clique em **"64-bit Git for Windows Setup"**

### 2.2 - Instalar

1. Execute o arquivo baixado
2. Clique **"Next"** em todas as telas (configuração padrão está OK)
3. Na tela "Adjusting your PATH", deixe marcado **"Git from the command line"**
4. Clique **"Install"**
5. Clique **"Finish"**

### 2.3 - Verificar instalação

1. Abra o **Prompt de Comando** (CMD)
2. Digite: `git --version`
3. Deve aparecer algo como: `git version 2.xx.x`

---

## 📤 PARTE 3: SUBIR PROJETO PARA O GITHUB

### 3.1 - Configurar Git (PRIMEIRA VEZ APENAS)

Abra o CMD na pasta do projeto e digite:

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seuemail@gmail.com"
```

### 3.2 - Criar repositório no GitHub

1. Entre no GitHub (https://github.com)
2. Clique no **"+"** no canto superior direito
3. Clique em **"New repository"**
4. Preencha:
   - **Repository name**: `sistema-verificacao`
   - **Description**: `Sistema de Verificação de Documentos`
   - Deixe **Public** marcado
   - NÃO marque nenhuma outra opção
5. Clique em **"Create repository"**

### 3.3 - Subir arquivos (NO CMD, NA PASTA DO PROJETO)

```bash
# 1. Inicializar Git
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Criar primeiro commit
git commit -m "Primeiro commit - Sistema completo"

# 4. Conectar ao GitHub (SUBSTITUA 'seu-usuario' pelo seu username)
git remote add origin https://github.com/seu-usuario/sistema-verificacao.git

# 5. Enviar para o GitHub
git push -u origin main
```

**NOTA**: Se pedir senha, use seu TOKEN do GitHub (não a senha normal)

### 3.4 - Criar Token GitHub (se necessário)

1. No GitHub, clique na sua foto (canto superior direito)
2. Clique em **"Settings"**
3. Role até o final e clique em **"Developer settings"**
4. Clique em **"Personal access tokens"** > **"Tokens (classic)"**
5. Clique em **"Generate new token"** > **"Generate new token (classic)"**
6. Em **"Note"**: digite `Railway Deploy`
7. Em **"Expiration"**: escolha **"No expiration"**
8. Marque a caixa **"repo"** (marca todas as sub-opções)
9. Role até o final e clique **"Generate token"**
10. **COPIE O TOKEN** (só aparece uma vez!)
11. Use este token como senha quando o Git pedir

---

## 🚂 PARTE 4: DEPLOY NO RAILWAY

### 4.1 - Criar conta Railway

1. Acesse: **https://railway.app**
2. Clique em **"Start a New Project"**
3. Clique em **"Login with GitHub"**
4. Autorize o Railway a acessar sua conta

### 4.2 - Criar novo projeto

1. Na tela inicial do Railway, clique em **"New Project"**
2. Clique em **"Deploy from GitHub repo"**
3. Procure por **"sistema-verificacao"**
4. Clique no repositório quando aparecer

### 4.3 - Configurar variáveis de ambiente

1. Depois que o deploy começar, clique em **"Variables"**
2. Clique em **"Add Variable"**
3. Adicione estas variáveis:

```
GEMINI_API_KEY = sua_chave_api_aqui
FLASK_SECRET_KEY = uma_senha_segura_qualquer
PORT = 5000
```

**IMPORTANTE**: Para pegar sua GEMINI_API_KEY:

1. Acesse: https://aistudio.google.com/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada

### 4.4 - Adicionar banco de dados (GRÁTIS)

1. No painel do Railway, clique em **"New"**
2. Selecione **"Database"** > **"Add PostgreSQL"**
3. O Railway criará automaticamente e conectará ao seu app

### 4.5 - Ver o site funcionando

1. No painel do Railway, clique no seu projeto
2. Clique na aba **"Settings"**
3. Em **"Domains"**, clique em **"Generate Domain"**
4. Clique no link gerado (algo como: `sistema-verificacao.up.railway.app`)

---

## 🔧 PARTE 5: COMANDOS ÚTEIS

### Atualizar o sistema (após fazer mudanças)

```bash
# Na pasta do projeto
git add .
git commit -m "Descrição da mudança"
git push
```

**O Railway atualiza automaticamente!**

### Ver logs no Railway

1. Entre no projeto no Railway
2. Clique em **"View Logs"**

---

## ❓ PROBLEMAS COMUNS E SOLUÇÕES

### "Erro de permissão no Git"

- Use o token do GitHub como senha (não a senha da conta)

### "Site não abre"

1. Verifique se adicionou todas as variáveis
2. Veja os logs no Railway
3. Certifique-se que o Procfile existe

### "Erro 404"

- Aguarde 2-3 minutos após o deploy

### "Application Error"

- Faltou adicionar a GEMINI_API_KEY nas variáveis

---

## 🎯 CHECKLIST FINAL

- [ ] Conta GitHub criada e verificada
- [ ] Git instalado no computador
- [ ] Projeto enviado para o GitHub
- [ ] Conta Railway criada
- [ ] Projeto importado do GitHub
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados PostgreSQL adicionado
- [ ] Domínio gerado
- [ ] Site funcionando!

---

## 💡 DICAS EXTRAS

1. **Monitorar uso**: No Railway, veja quanto dos $5 você está usando
2. **Backup**: O GitHub já serve como backup do código
3. **Domínio próprio**: Pode conectar seu domínio depois (ex: seusite.com.br)

---

## 🆘 PRECISA DE AJUDA?

Execute o script `SUBIR_GIT_RAILWAY.bat` que criei para automatizar parte do processo!
