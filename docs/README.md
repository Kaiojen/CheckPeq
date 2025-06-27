# Sistema de Verificação Automática - IN SEGES nº 65/2021

## 📋 Sobre o Sistema

Sistema web profissional para verificação automática de documentos de pesquisa de preços em processos licitatórios, baseado na Instrução Normativa SEGES nº 65/2021. O sistema utiliza **Inteligência Artificial (Google Gemini)** para analisar documentos PDF e DOCX, verificando automaticamente o cumprimento dos 16 itens obrigatórios do checklist oficial da CJU.

## ✨ Funcionalidades Principais

- **📄 Processamento Inteligente de Documentos**

  - Suporte para arquivos PDF e DOCX
  - Extração automática de texto
  - OCR integrado para documentos digitalizados
  - Análise com IA (Google Gemini API)

- **🔍 Verificação Automática**

  - Análise dos 16 itens da IN SEGES 65/2021
  - Identificação de páginas onde cada requisito foi encontrado
  - Justificativas detalhadas para cada item
  - Status: Cumprido (✅), Ausente (❌) ou Não Aplicável (⚪)

- **📊 Relatórios Profissionais**

  - Geração de relatório PDF com layout institucional
  - Exportação para Excel
  - Estatísticas visuais em tempo real
  - Histórico de verificações em banco de dados

- **🎨 Interface Moderna**
  - Design responsivo e intuitivo
  - Cards informativos e estatísticas visuais
  - Feedback em tempo real durante o processamento
  - Suporte a drag-and-drop para upload de arquivos

## 🚀 Como Executar

### Opção 1: Streamlit (Recomendado)

```bash
# Windows
run_streamlit.bat

# Linux/Mac
streamlit run src/app_streamlit.py
```

### Opção 2: Flask

```bash
# Windows
run_flask.bat

# Linux/Mac
cd src && python main.py
```

## 📦 Instalação Manual

1. **Clone o repositório:**

```bash
git clone [url-do-repositorio]
cd sistema_verificacao_final
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Configure o Tesseract OCR (para documentos digitalizados):**

   - Windows: Baixe e instale de https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
   - Mac: `brew install tesseract tesseract-lang`

4. **Execute o sistema:**

```bash
streamlit run src/app_streamlit.py
```

## 🔧 Configuração

### API do Google AI (Gemini)

O sistema já vem configurado com uma chave API, mas você pode usar sua própria:

1. Obtenha uma chave em: https://makersuite.google.com/app/apikey
2. Edite o arquivo `src/app_streamlit.py`
3. Substitua a chave na linha:

```python
GOOGLE_API_KEY = "sua-chave-aqui"
```

### Estrutura de Pastas

```
sistema_verificacao_final/
├── src/
│   ├── app_streamlit.py    # Aplicação principal Streamlit
│   ├── main.py             # Aplicação Flask (alternativa)
│   └── checklist_items.json # Configuração dos 16 itens
├── uploads/                 # Arquivos temporários
├── reports/                 # Relatórios gerados
├── database/               # Banco de dados SQLite
├── requirements.txt        # Dependências Python
├── run_streamlit.bat      # Script para Windows (Streamlit)
└── run_flask.bat          # Script para Windows (Flask)
```

## 📊 Os 16 Itens Verificados

1. **Orçamento Estimado**: Existência de orçamento com composições detalhadas
2. **Compatibilidade com Mercado**: Valores compatíveis com práticas de mercado
3. **Mínimo de Três Preços**: Base em pelo menos 3 preços ou justificativa
4. **Mediana em Sistemas Oficiais**: Comparação com mediana do Painel de Preços
5. **Elementos Obrigatórios**: Presença de 8 elementos mínimos na pesquisa
6. **Priorização de Fontes Oficiais**: Uso prioritário de sistemas governamentais
7. **Contratações Recentes**: Referências com menos de 1 ano
8. **Consulta a Fornecedores**: Mínimo de 3 fornecedores consultados
9. **Validade dos Orçamentos**: Máximo 6 meses de antecedência
10. **Prazo de Resposta**: Compatibilidade com complexidade do objeto
11. **Dados Completos**: CNPJ/CPF, endereços, contatos nos orçamentos
12. **Características Comerciais**: Informações conforme art. 4º da IN
13. **Fornecedores sem Resposta**: Relação dos consultados não respondentes
14. **Motivação da Divulgação**: Justificativa do momento de divulgação
15. **Atividades de Custeio**: Observância ao Decreto 10.193/19
16. **Impacto Orçamentário**: Estimativas para novas despesas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+
- **Frontend**: Streamlit / Flask
- **IA**: Google Generative AI (Gemini)
- **PDF**: PyMuPDF, pdfplumber
- **OCR**: Tesseract (pytesseract)
- **Relatórios**: ReportLab
- **Banco de Dados**: SQLite
- **Excel**: OpenPyXL

## 📝 Requisitos do Sistema

- Python 3.8 ou superior
- 4GB RAM mínimo (8GB recomendado)
- Conexão com internet (para API do Google AI)
- Navegador web moderno
- Tesseract OCR (opcional, para PDFs digitalizados)

## 🔒 Segurança e Privacidade

- Arquivos processados localmente
- Dados enviados apenas para API do Google AI para análise
- Banco de dados local (SQLite)
- Sem armazenamento em nuvem
- Arquivos temporários deletados após processamento

## 📞 Suporte

Para dúvidas ou problemas:

- Verifique se todas as dependências foram instaladas
- Certifique-se de ter conexão com internet
- Consulte os logs de erro no terminal
- Verifique se o arquivo está no formato correto (PDF/DOCX)

## 🎯 Casos de Uso

1. **Equipes de Licitação**: Verificação rápida de conformidade
2. **Pregoeiros**: Análise prévia de documentação
3. **Auditoria**: Conferência de processos licitatórios
4. **Consultoria**: Preparação de documentos conformes

## ⚡ Performance

- Processamento médio: 30-60 segundos por documento
- Suporte a arquivos até 16MB
- OCR limitado a 10 primeiras páginas (configurável)
- Análise de IA limitada a 5000 caracteres por item

## 🔄 Atualizações Futuras

- [ ] Integração com sistemas de gestão
- [ ] API REST para integração
- [ ] Suporte a mais formatos de arquivo
- [ ] Dashboard de análises históricas
- [ ] Exportação em mais formatos

---

**Desenvolvido para a Controladoria-Geral da União (CGU)**

Sistema de Verificação Automática - IN SEGES nº 65/2021 v1.0
