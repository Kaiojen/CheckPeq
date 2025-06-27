# 🚀 Guia Completo: Instalar e Testar o Sistema Localmente

## 📋 Verificação do Sistema

### Problemas Detectados:

- ❌ Streamlit não instalado
- ❌ Bibliotecas de PDF não instaladas
- ❌ OCR (Tesseract) não configurado

### Solução: Vamos instalar tudo do zero!

---

## 🔧 PASSO A PASSO COMPLETO

### PASSO 1: Abrir o Terminal Correto

1. Pressione `Windows + R`
2. Digite `cmd` e pressione Enter
3. Cole este comando para ir até a pasta do projeto:

```cmd
cd /d "C:\Users\gabri\OneDrive\Desktop\sistema_verificacao_final"
```

### PASSO 2: Criar Ambiente Virtual (Recomendado)

Isso evita conflitos com outras instalações Python:

```cmd
python -m venv venv
```

Ative o ambiente virtual:

```cmd
venv\Scripts\activate
```

> Você verá `(venv)` no início da linha quando estiver ativo

### PASSO 3: Instalar TODAS as Dependências

Execute estes comandos **um por vez**:

```cmd
pip install --upgrade pip
```

```cmd
pip install streamlit==1.46.1
```

```cmd
pip install pdfplumber==0.11.7
```

```cmd
pip install PyMuPDF==1.26.1
```

```cmd
pip install pdf2image==1.17.0
```

```cmd
pip install pytesseract==0.3.13
```

```cmd
pip install google-generativeai==0.8.1
```

```cmd
pip install -r requirements.txt
```

### PASSO 4: Instalar Tesseract OCR (Para PDFs Digitalizados)

1. **Baixe o instalador:**

   - Acesse: https://github.com/UB-Mannheim/tesseract/wiki
   - Baixe: tesseract-ocr-w64-setup-5.3.3.20231005.exe (ou versão mais recente)

2. **Instale o Tesseract:**

   - Execute o instalador
   - **IMPORTANTE:** Durante a instalação, marque a opção "Add to PATH"
   - Instale em: `C:\Program Files\Tesseract-OCR`

3. **Baixe o idioma Português:**
   - Durante a instalação, na tela "Choose Components"
   - Expanda "Additional Language Data"
   - Marque "Portuguese"

### PASSO 5: Instalar Poppler (Para PDF2Image)

1. **Baixe o Poppler:**

   - Acesse: https://github.com/oschwartz10612/poppler-windows/releases/
   - Baixe: Release-xx.xx.x-x.zip

2. **Extraia e Configure:**
   - Extraia para: `C:\poppler`
   - Adicione ao PATH: `C:\poppler\Library\bin`

**Como adicionar ao PATH:**

1. Pesquise "Variáveis de ambiente" no menu Iniciar
2. Clique em "Variáveis de Ambiente"
3. Em "Variáveis do Sistema", encontre "Path"
4. Clique "Editar" → "Novo"
5. Adicione: `C:\poppler\Library\bin`
6. OK em todas as janelas

### PASSO 6: Verificar Instalação

Feche e abra um novo CMD, vá até a pasta do projeto e execute:

```cmd
python test_install.py
```

Todos os itens devem aparecer com ✓

---

## 🎮 TESTANDO O SISTEMA

### Opção 1: Testar a Versão 2.0 (Melhorada)

```cmd
streamlit run src/app_v2.py
```

### Opção 2: Testar a Versão Original

```cmd
streamlit run src/app_streamlit.py
```

### O que vai acontecer:

1. O navegador abrirá automaticamente
2. Você verá a interface do sistema
3. A URL será algo como: http://localhost:8501

---

## 🧪 ROTEIRO DE TESTES

### Teste 1: Upload Básico

1. Digite seu nome
2. Faça upload do arquivo `Check List - Pesquisa de Preços.md` (está na pasta do projeto)
3. Clique em "Iniciar Conferência"
4. Aguarde a análise (30-60 segundos)
5. Verifique os resultados

### Teste 2: Gerar Relatório

1. Após a análise, clique em "Baixar Relatório PDF"
2. O PDF deve ser baixado com sucesso
3. Abra o PDF e verifique o conteúdo

### Teste 3: Nova Verificação

1. Clique em "Nova Verificação"
2. O sistema deve voltar à tela inicial

### Teste 4: PDF Real (Opcional)

1. Use um PDF real de pesquisa de preços
2. O sistema deve processar normalmente

---

## 🐛 SOLUÇÃO DE PROBLEMAS

### Erro: "streamlit: comando não reconhecido"

```cmd
python -m streamlit run src/app_v2.py
```

### Erro: "No module named 'xxx'"

```cmd
pip install xxx --upgrade
```

(substitua xxx pelo nome do módulo)

### Erro: "Tesseract not found"

- Verifique se instalou o Tesseract
- Reinicie o computador após adicionar ao PATH

### Erro com Poppler/PDF2Image

- Certifique-se que o Poppler está no PATH
- Teste com: `where pdftoppm` (deve mostrar o caminho)

---

## ✅ CHECKLIST FINAL

Antes de subir para web, verifique:

- [ ] Sistema roda sem erros localmente
- [ ] Upload de PDF funciona
- [ ] Upload de DOCX funciona
- [ ] Geração de relatório PDF funciona
- [ ] Interface está bonita e responsiva
- [ ] Análise com IA retorna resultados coerentes
- [ ] Botão "Nova Verificação" funciona

---

## 🌐 PRÓXIMO PASSO: DEPLOY WEB

Quando tudo estiver funcionando localmente:

1. Suba o código para o GitHub
2. Use o arquivo `src/app_v2.py` (versão otimizada)
3. Configure a API key no Streamlit Cloud
4. Deploy em minutos!

---

**DICA:** Se tiver qualquer problema, o erro geralmente aparece no terminal onde você executou o comando. Copie o erro e podemos resolver juntos!
