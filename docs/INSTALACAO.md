# Guia de Instalação e Configuração

## 📋 Pré-requisitos

### Sistema Operacional

- Windows 10/11
- Linux (Ubuntu 20.04 ou superior)
- macOS 10.15 ou superior

### Software Necessário

1. **Python 3.8 ou superior**

   - Download: https://www.python.org/downloads/
   - Verificar instalação: `python --version`

2. **Git** (opcional, para clonar o repositório)

   - Download: https://git-scm.com/downloads

3. **Tesseract OCR** (para documentos digitalizados)
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
   - macOS: `brew install tesseract tesseract-lang`

## 🚀 Instalação Rápida

### Windows

1. **Baixar o sistema:**

   - Extraia o arquivo ZIP em uma pasta de sua preferência

2. **Executar o instalador:**
   ```cmd
   run_streamlit.bat
   ```
   - O script instalará automaticamente todas as dependências
   - O navegador abrirá com o sistema

### Linux/macOS

1. **Clonar o repositório:**

   ```bash
   git clone [URL_DO_REPOSITORIO]
   cd sistema_verificacao_final
   ```

2. **Criar ambiente virtual (recomendado):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Instalar dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o sistema:**
   ```bash
   streamlit run src/app_streamlit.py
   ```

## 🔧 Configuração Avançada

### 1. Configurar API do Google AI

#### Opção A: Variável de Ambiente

```bash
# Linux/macOS
export GOOGLE_API_KEY="sua-chave-aqui"

# Windows
set GOOGLE_API_KEY=sua-chave-aqui
```

#### Opção B: Arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```
GOOGLE_API_KEY=sua-chave-aqui
```

#### Opção C: Editar config.py

Edite o arquivo `src/config.py`:

```python
GOOGLE_API_KEY = "sua-chave-aqui"
```

### 2. Configurar Tesseract OCR

#### Windows

1. Instale o Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Adicione ao PATH do sistema:

   - Painel de Controle → Sistema → Configurações Avançadas
   - Variáveis de Ambiente → PATH
   - Adicionar: `C:\Program Files\Tesseract-OCR`

3. Verificar instalação:
   ```cmd
   tesseract --version
   ```

#### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-por

# Verificar instalação
tesseract --version
```

### 3. Configurar Proxy (se necessário)

Para ambientes corporativos com proxy:

```python
# Adicionar ao início de app_streamlit.py
import os
os.environ['HTTP_PROXY'] = 'http://seu-proxy:porta'
os.environ['HTTPS_PROXY'] = 'http://seu-proxy:porta'
```

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"

- Instale Python 3.8 ou superior
- Adicione Python ao PATH do sistema
- Reinicie o terminal/prompt

### Erro: "Módulo não encontrado"

```bash
pip install -r requirements.txt --upgrade
```

### Erro: "Tesseract não encontrado"

- Instale o Tesseract OCR
- Verifique se está no PATH
- Reinicie o sistema

### Erro: "Conexão com API falhou"

- Verifique sua conexão com internet
- Verifique se a chave API está correta
- Verifique configurações de proxy/firewall

### Erro: "Porta já em uso"

```bash
# Streamlit em outra porta
streamlit run src/app_streamlit.py --server.port 8502

# Flask em outra porta
python src/main.py --port 5001
```

## 📦 Dependências Principais

| Biblioteca          | Versão | Função               |
| ------------------- | ------ | -------------------- |
| streamlit           | 1.46.1 | Interface web        |
| google-generativeai | 0.8.1  | IA para análise      |
| pdfplumber          | 0.11.7 | Extração de PDF      |
| PyMuPDF             | 1.26.1 | Processamento PDF    |
| pytesseract         | 0.3.13 | OCR                  |
| reportlab           | 4.4.2  | Geração de PDF       |
| pandas              | 2.3.0  | Manipulação de dados |
| openpyxl            | 3.1.2  | Exportação Excel     |

## 🔒 Considerações de Segurança

1. **API Key**

   - Nunca compartilhe sua chave API
   - Use variáveis de ambiente em produção
   - Rotacione chaves periodicamente

2. **Arquivos**

   - Arquivos são processados localmente
   - Deletados após processamento
   - Não são armazenados em nuvem

3. **Banco de Dados**
   - SQLite local
   - Sem acesso externo
   - Backup regular recomendado

## 📱 Acesso Mobile

O sistema é responsivo e pode ser acessado via dispositivos móveis:

1. Execute o sistema com IP público:

   ```bash
   streamlit run src/app_streamlit.py --server.address 0.0.0.0
   ```

2. Acesse no dispositivo móvel:
   ```
   http://[IP_DO_SERVIDOR]:8501
   ```

## 🚀 Deploy em Produção

### Opção 1: Servidor Local

1. Configure como serviço do Windows/systemd
2. Use nginx como proxy reverso
3. Configure HTTPS com certificado SSL

### Opção 2: Docker

```dockerfile
FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "src/app_streamlit.py"]
```

### Opção 3: Cloud

- Heroku
- Google Cloud Run
- AWS EC2
- Azure App Service

## 📞 Suporte

Em caso de dúvidas:

1. Consulte a documentação
2. Verifique os logs do sistema
3. Abra uma issue no repositório
4. Contate o administrador do sistema

---

**Sistema de Verificação IN SEGES 65/2021** - Versão 1.0
