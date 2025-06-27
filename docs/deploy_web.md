# 🌐 Guia de Deploy Web - Sistema IN SEGES 65/2021

## Opções de Hospedagem Gratuita

### 1. Streamlit Cloud (RECOMENDADO) ⭐

**100% Gratuito | Mais Fácil | Oficial do Streamlit**

#### Passo a Passo:

1. **Crie conta no GitHub**

   - https://github.com
   - Faça upload do projeto

2. **Crie conta no Streamlit Cloud**

   - https://share.streamlit.io
   - Conecte com seu GitHub

3. **Deploy em 3 cliques**

   - New app → Selecione repositório
   - Main file: `src/app_streamlit.py`
   - Deploy!

4. **URL pública gerada**
   - Exemplo: `https://seu-app.streamlit.app`

### 2. Render.com

**Gratuito com limites | Fácil**

```yaml
# render.yaml
services:
  - type: web
    name: sistema-in-seges
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run src/app_streamlit.py --server.port $PORT"
```

### 3. Railway.app

**$5 créditos grátis/mês**

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### 4. Google Cloud Run

**Generoso tier gratuito**

```dockerfile
# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD streamlit run src/app_streamlit.py \
    --server.port 8080 \
    --server.address 0.0.0.0
```

```bash
# Deploy
gcloud run deploy sistema-seges \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## 🔐 Configurações de Segurança para Web

### 1. Variáveis de Ambiente

```python
# src/app_streamlit.py - Modificar início do arquivo
import os
import streamlit as st

# Configuração segura da API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    st.error("⚠️ Configure a variável GOOGLE_API_KEY no servidor")
    st.stop()
```

### 2. Limites de Upload

```python
# Adicionar no config.py
MAX_FILE_SIZE_MB = 10  # Reduzir para web
MAX_DAILY_REQUESTS = 100  # Limitar uso
```

### 3. Autenticação (Opcional)

```python
# Adicionar autenticação simples
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Senha", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Senha", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Senha incorreta")
        return False
    else:
        return True

# No início do main()
if not check_password():
    st.stop()
```

## 📊 Comparação de Plataformas

| Plataforma      | Gratuito   | Facilidade | Performance | Limites          |
| --------------- | ---------- | ---------- | ----------- | ---------------- |
| Streamlit Cloud | ✅ Sim     | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐    | 1GB RAM          |
| Render          | ✅ Sim\*   | ⭐⭐⭐⭐   | ⭐⭐⭐      | Sleep após 15min |
| Railway         | 💰 $5/mês  | ⭐⭐⭐⭐   | ⭐⭐⭐⭐    | 500MB RAM        |
| Google Cloud    | ✅ Sim\*\* | ⭐⭐⭐     | ⭐⭐⭐⭐⭐  | 2M requests/mês  |
| Heroku          | 💰 $7/mês  | ⭐⭐⭐     | ⭐⭐⭐⭐    | Não recomendado  |

\*Com limitações / \*\*Tier gratuito generoso

## 🚀 Deploy Rápido - Streamlit Cloud

### 1. Preparar Repositório

```bash
# Estrutura necessária
/
├── src/
│   ├── app_streamlit.py
│   ├── config.py
│   └── checklist_items.json
├── requirements.txt
└── .streamlit/
    └── secrets.toml  # Para API keys
```

### 2. Arquivo secrets.toml

```toml
# .streamlit/secrets.toml (NÃO commitar!)
GOOGLE_API_KEY = "sua-chave-aqui"
```

### 3. Configurar no Streamlit Cloud

- Settings → Secrets → Colar conteúdo do secrets.toml

## ⚡ Otimizações para Web

### 1. Cache de Resultados

```python
@st.cache_data(ttl=3600)  # Cache por 1 hora
def analyze_document_cached(file_content, file_name):
    return analyze_document(file_content, file_name)
```

### 2. Limite de Processamento

```python
# Adicionar timeouts
import signal
from contextlib import contextmanager

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutError("Processamento excedeu o tempo limite")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

# Usar no processamento
with time_limit(60):
    results = analyze_document(...)
```

### 3. Compressão de Arquivos

```python
# Limitar tamanho de upload
if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
    st.error("Arquivo muito grande para versão web. Máximo: 10MB")
    st.stop()
```

## 📱 URL Amigável

### Configurar domínio personalizado:

1. Compre domínio (ex: verificacao-seges.com.br)
2. Configure CNAME para seu-app.streamlit.app
3. Adicione no Streamlit Cloud Settings

## 🔍 Monitoramento

### Google Analytics (Opcional)

```python
# Adicionar ao início do app
GA_TRACKING_CODE = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
"""
st.markdown(GA_TRACKING_CODE, unsafe_allow_html=True)
```

## 📋 Checklist para Deploy

- [ ] Remover API keys do código
- [ ] Configurar variáveis de ambiente
- [ ] Testar localmente com vars de ambiente
- [ ] Criar repositório no GitHub
- [ ] Fazer deploy no Streamlit Cloud
- [ ] Configurar secrets no dashboard
- [ ] Testar funcionalidades online
- [ ] Configurar domínio (opcional)
- [ ] Adicionar analytics (opcional)

## 🎯 Recomendação Final

**Para seu caso, recomendo Streamlit Cloud porque:**

1. 100% gratuito
2. Integração perfeita com Streamlit
3. Deploy em minutos
4. Suporta secrets para API keys
5. URL pública compartilhável
6. Atualizações automáticas via GitHub

---

**Tempo estimado para colocar no ar: 15 minutos**
