# 🚀 Deploy Rápido em 15 Minutos - Streamlit Cloud

## Passo 1: Criar Conta no GitHub (5 min)

1. Acesse https://github.com
2. Clique em "Sign up"
3. Crie sua conta gratuita

## Passo 2: Subir o Projeto (5 min)

1. No GitHub, clique em "New repository" (botão verde)
2. Nome: `sistema-verificacao-seges`
3. Deixe como "Public"
4. Clique em "Create repository"
5. Clique em "Upload files"
6. Arraste toda a pasta do projeto
7. Clique em "Commit changes"

## Passo 3: Deploy no Streamlit (5 min)

1. Acesse https://share.streamlit.io
2. Clique em "Sign up" → "Continue with GitHub"
3. Autorize o Streamlit
4. Clique em "New app"
5. Preencha:
   - Repository: `seu-usuario/sistema-verificacao-seges`
   - Branch: `main`
   - Main file path: `src/app_streamlit.py`
6. Clique em "Deploy"

## 🔐 Configurar a Chave da API

1. No Streamlit Cloud, clique no seu app
2. Clique em "⚙️ Settings" → "Secrets"
3. Cole este texto:

```
GOOGLE_API_KEY = "AIzaSyBV2_ME3XuWbKhJ-zSURhqm2RKDW5hl9Y0"
```

4. Clique em "Save"

## ✅ PRONTO!

Seu sistema estará disponível em:
`https://[seu-usuario]-sistema-verificacao-seges.streamlit.app`

## 📱 Compartilhe o Link

- Envie o link por email
- Coloque na intranet
- Adicione aos favoritos
- Funciona em celular!

## 💡 Dicas Importantes

- O sistema "dorme" após 7 dias sem uso (acorde acessando o link)
- Limite de 1GB RAM (suficiente para PDFs até 10MB)
- 100% gratuito para sempre
- Atualizações automáticas quando você atualizar o GitHub

---

**Precisa de ajuda?** O Streamlit tem chat de suporte ao vivo!
