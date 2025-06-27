import streamlit as st
import os
import json
import tempfile
from datetime import datetime
import pandas as pd
import sqlite3
from pathlib import Path
import uuid
import base64
from io import BytesIO

# Configurações da página
st.set_page_config(
    page_title="Sistema de Verificação IN SEGES 65/2021",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Importações para processamento de documentos
import pdfplumber
# import fitz  # PyMuPDF - REMOVIDO
# from pdf2image import convert_from_path - REMOVIDO
# import pytesseract - REMOVIDO
import docx
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas

# Importação do Google Generative AI
import google.generativeai as genai

# Importar configurações com tratamento de erro
try:
    from config import GOOGLE_API_KEY, UPLOAD_FOLDER, REPORTS_FOLDER, DATABASE_FOLDER
except Exception as e:
    st.error(f"❌ Erro ao carregar configurações: {e}")
    st.stop()

# Criar diretórios se não existirem
for folder in [UPLOAD_FOLDER, REPORTS_FOLDER, DATABASE_FOLDER]:
    folder.mkdir(exist_ok=True, parents=True)

# Importar módulos de segurança e utilidades
SECURITY_ENABLED = False
try:
    from security import file_validator, security_auditor, input_sanitizer
    from utils import format_utils, document_analyzer
    SECURITY_ENABLED = True
except ImportError as e:
    st.sidebar.warning("⚠️ Módulos de segurança não disponíveis. Executando em modo básico.")
    SECURITY_ENABLED = False

# Configurar API do Google AI apenas se disponível
model = None
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"❌ Erro ao configurar Google AI: {e}")
else:
    st.warning("⚠️ GOOGLE_API_KEY não configurada. Configure no arquivo .env")

# Criar diretórios necessários (já importados do config)
DB_FOLDER = DATABASE_FOLDER  # Manter compatibilidade com nome usado no código

# Inicializar banco de dados
def init_database():
    conn = sqlite3.connect(DB_FOLDER / "verificacoes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verificacoes (
            id TEXT PRIMARY KEY,
            data_hora TIMESTAMP,
            conferente TEXT,
            arquivo TEXT,
            resultado_json TEXT,
            relatorio_path TEXT
        )
    """)
    conn.commit()
    conn.close()

init_database()

# Carregar itens do checklist
def load_checklist_items():
    json_path = Path("src/checklist_items.json")
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error("Arquivo checklist_items.json não encontrado!")
        return {}

# CSS personalizado
def load_css():
    st.markdown("""
    <style>
    /* Tema principal */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header estilizado */
    .header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        text-align: center;
    }
    
    /* Cards estilizados */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }
    
    /* Resultados */
    .result-sim {
        background: #d1fae5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .result-nao {
        background: #fee2e2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .result-na {
        background: #e5e7eb;
        border-left: 4px solid #6b7280;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    /* Estatísticas */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
    }
    
    /* Botões customizados */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(59,130,246,0.3);
    }
    
    /* Upload area */
    .uploadedFile {
        background: #f8fafc;
        border: 2px dashed #d1d5db;
        border-radius: 10px;
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Função para extrair texto com indicação de páginas
def extract_text_from_pdf_with_pages(file_path):
    pages_text = {}
    full_text = ""
    
    # Tentar extração direta de texto
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    pages_text[i+1] = page_text
                    full_text += f"\n--- Página {i+1} ---\n{page_text}\n"
    except Exception as e:
        st.warning(f"Erro com pdfplumber: {e}")
    
    # PyMuPDF removido - apenas usar pdfplumber
    
    # OCR removido temporariamente
    if not full_text.strip():
        st.warning("⚠️ Não foi possível extrair texto do PDF. O arquivo pode estar digitalizado como imagem.")
    
    return full_text, pages_text

# Função para extrair texto de DOCX com páginas
def extract_text_from_docx_with_pages(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = ""
        pages_text = {1: ""}  # DOCX não tem páginas definidas
        
        for paragraph in doc.paragraphs:
            full_text += paragraph.text + "\n"
            pages_text[1] += paragraph.text + "\n"
            
        return full_text, pages_text
    except Exception as e:
        st.error(f"Erro ao extrair texto do DOCX: {e}")
        return "", {}

# Função para analisar com IA
def analyze_with_ai(item_num, item_text, document_text):
    if not model:
        # Se não há modelo, usar análise por palavras-chave
        return analyze_by_keywords(item_num, document_text)
    
    prompt = f"""
    Você é um especialista em análise de documentos de licitação e pesquisa de preços.
    
    Analise o seguinte texto de um documento de pesquisa de preços e verifique se ele atende ao seguinte requisito da IN SEGES 65/2021:
    
    REQUISITO (Item {item_num}): {item_text}
    
    DOCUMENTO A ANALISAR:
    {document_text[:5000]}  # Limitar para não exceder o contexto
    
    Responda APENAS com uma das seguintes opções:
    - "Sim" - se o documento claramente atende ao requisito
    - "Não" - se o documento não atende ou não há evidências claras
    - "N/A" - se o requisito não se aplica a este tipo de documento
    
    Além da resposta, forneça uma breve justificativa (máximo 2 linhas) e indique se encontrou alguma página específica onde o requisito é mencionado.
    
    Formato da resposta:
    STATUS: [Sim/Não/N/A]
    JUSTIFICATIVA: [breve explicação]
    PÁGINA: [número da página ou "Não identificada"]
    """
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Extrair informações da resposta
        lines = result_text.split('\n')
        status = "Não"
        justificativa = ""
        pagina = "Não identificada"
        
        for line in lines:
            if line.startswith("STATUS:"):
                status_raw = line.replace("STATUS:", "").strip()
                if "Sim" in status_raw:
                    status = "Sim"
                elif "N/A" in status_raw or "Não se aplica" in status_raw:
                    status = "N/A"
                else:
                    status = "Não"
            elif line.startswith("JUSTIFICATIVA:"):
                justificativa = line.replace("JUSTIFICATIVA:", "").strip()
            elif line.startswith("PÁGINA:"):
                pagina = line.replace("PÁGINA:", "").strip()
        
        return status, justificativa, pagina
        
    except Exception as e:
        st.warning(f"Erro na análise AI do item {item_num}: {e}")
        # Fallback para análise por palavras-chave
        return analyze_by_keywords(item_num, document_text)

# Análise por palavras-chave (fallback)
def analyze_by_keywords(item_num, document_text):
    keywords_map = {
        1: ["orçamento estimado", "composições detalhadas", "preços", "formação"],
        2: ["valor previamente estimado", "compatível", "mercado", "bancos de dados"],
        3: ["três preços", "3 preços", "justificativa", "número mínimo"],
        4: ["sistemas oficiais", "Painel de Preços", "mediana", "banco de preços"],
        5: ["descrição do objeto", "agente responsável", "fontes consultadas", "método estatístico"],
        6: ["sistemas oficiais", "priorizados", "Painel de Preços", "contratações similares"],
        7: ["contratações similares", "1 ano", "um ano", "prazo inferior"],
        8: ["pesquisa direta", "três fornecedores", "3 fornecedores", "consulta"],
        9: ["6 meses", "seis meses", "orçamentos", "validade"],
        10: ["prazo de resposta", "complexidade", "compatível"],
        11: ["CPF", "CNPJ", "endereços", "data de emissão", "orçamentos"],
        12: ["art. 4º", "características da contratação", "IN 65/2021"],
        13: ["fornecedores consultados", "não enviaram", "sem resposta"],
        14: ["motivação", "divulgação do orçamento", "momento"],
        15: ["custeio", "Decreto 10.193/19", "art. 3º"],
        16: ["impacto orçamentário", "adequação orçamentária", "estimativa"]
    }
    
    keywords = keywords_map.get(item_num, [])
    document_lower = document_text.lower()
    
    found_keywords = sum(1 for keyword in keywords if keyword.lower() in document_lower)
    
    if found_keywords >= 2:
        return "Sim", f"Encontradas {found_keywords} palavras-chave relevantes", "Múltiplas páginas"
    elif found_keywords == 1:
        return "Não", f"Apenas {found_keywords} palavra-chave encontrada", "Não identificada"
    else:
        return "Não", "Nenhuma evidência encontrada", "Não identificada"

# Gerar relatório PDF profissional
def generate_pdf_report(conferente, arquivo, resultados, verificacao_id):
    try:
        report_path = REPORTS_FOLDER / f"relatorio_{verificacao_id}.pdf"
        
        # Criar documento
        doc = SimpleDocTemplate(
            str(report_path),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Container para elementos
        elements = []
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Estilo para subtítulo
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Estilo para texto normal
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#374151'),
            alignment=TA_JUSTIFY,
            spaceAfter=12
        )
        
        # Cabeçalho
        elements.append(Paragraph("RELATÓRIO DE VERIFICAÇÃO", title_style))
        elements.append(Paragraph("Pesquisa de Preços - IN SEGES nº 65/2021", subtitle_style))
        elements.append(Spacer(1, 20))
        
        # Informações gerais
        info_data = [
            ['Conferente:', conferente],
            ['Data e Hora:', datetime.now().strftime('%d/%m/%Y - %H:%M')],
            ['Arquivo Analisado:', arquivo],
            ['Código de Verificação:', verificacao_id]
        ]
        
        info_table = Table(info_data, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDINGRIGHT', (0, 0), (-1, -1), 12),
            ('PADDINGLEFT', (0, 0), (-1, -1), 12),
            ('PADDINGBOTTOM', (0, 0), (-1, -1), 8),
            ('PADDINGTOP', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db'))
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 30))
        
        # Resumo estatístico
        total = len(resultados)
        cumpridos = sum(1 for r in resultados.values() if r['status'] == 'Sim')
        ausentes = sum(1 for r in resultados.values() if r['status'] == 'Não')
        nao_aplicaveis = sum(1 for r in resultados.values() if r['status'] == 'N/A')
        
        elements.append(Paragraph("RESUMO DA VERIFICAÇÃO", ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )))
        
        summary_data = [
            ['Total de Itens', 'Cumpridos', 'Ausentes', 'Não Aplicáveis'],
            [str(total), f'{cumpridos} ({cumpridos/total*100:.1f}%)', 
             f'{ausentes} ({ausentes/total*100:.1f}%)', 
             f'{nao_aplicaveis} ({nao_aplicaveis/total*100:.1f}%)']
        ]
        
        summary_table = Table(summary_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('PADDINGBOTTOM', (0, 0), (-1, -1), 12),
            ('PADDINGTOP', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 30))
        
        # Detalhamento dos resultados
        elements.append(Paragraph("DETALHAMENTO DOS RESULTADOS", ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )))
        
        # Tabela de resultados
        results_data = [['Item', 'Descrição', 'Status', 'Página']]
        
        for item_key, resultado in resultados.items():
            item_num = item_key.replace("Item ", "")
            status_symbol = {
                'Sim': '✓',
                'Não': '✗',
                'N/A': '○'
            }.get(resultado['status'], '?')
            
            # Truncar descrição se muito longa
            descricao = resultado['descricao']
            if len(descricao) > 80:
                descricao = descricao[:77] + "..."
            
            pagina = resultado.get('pagina', 'N/I')
            if pagina == "Não identificada":
                pagina = "N/I"
            
            results_data.append([
                f"{item_num}",
                descricao,
                f"{status_symbol} {resultado['status']}",
                pagina
            ])
        
        # Criar tabela com larguras de coluna ajustadas
        results_table = Table(results_data, colWidths=[1.5*cm, 10*cm, 2.5*cm, 2*cm])
        
        # Estilizar tabela
        table_style = TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Corpo da tabela
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (3, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('PADDINGRIGHT', (0, 0), (-1, -1), 8),
            ('PADDINGLEFT', (0, 0), (-1, -1), 8),
            ('PADDINGBOTTOM', (0, 0), (-1, -1), 8),
            ('PADDINGTOP', (0, 0), (-1, -1), 8),
        ])
        
        # Colorir linhas baseado no status
        for i, (item_key, resultado) in enumerate(resultados.items(), 1):
            if resultado['status'] == 'Sim':
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#d1fae5'))
            elif resultado['status'] == 'Não':
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fee2e2'))
            else:  # N/A
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f3f4f6'))
        
        results_table.setStyle(table_style)
        elements.append(results_table)
        
        # Adicionar observações se houver justificativas
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("OBSERVAÇÕES", ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e3a8a'),
            spaceAfter=15,
            fontName='Helvetica-Bold'
        )))
        
        obs_text = []
        for item_key, resultado in resultados.items():
            if resultado.get('justificativa'):
                item_num = item_key.replace("Item ", "")
                obs_text.append(f"<b>Item {item_num}:</b> {resultado['justificativa']}")
        
        if obs_text:
            for obs in obs_text:
                elements.append(Paragraph(obs, normal_style))
        else:
            elements.append(Paragraph("Nenhuma observação adicional.", normal_style))
        
        # Assinatura digital
        elements.append(Spacer(1, 50))
        
        signature_style = ParagraphStyle(
            'Signature',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            alignment=TA_CENTER,
            spaceAfter=5
        )
        
        elements.append(Paragraph("_" * 60, signature_style))
        elements.append(Paragraph("Sistema de Verificação Automática", signature_style))
        elements.append(Paragraph("IN SEGES nº 65/2021 - CJU", signature_style))
        elements.append(Paragraph(f"Documento gerado eletronicamente em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}", signature_style))
        
        # Gerar PDF
        doc.build(elements)
        
        return str(report_path)
        
    except Exception as e:
        st.error(f"Erro ao gerar relatório PDF: {e}")
        return None

# Interface principal
def main():
    load_css()
    
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">📋 Sistema de Verificação Automática</h1>
        <p class="header-subtitle">Conferência de Pesquisa de Preços - IN SEGES nº 65/2021</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar se há resultados salvos na sessão
    if 'verification_complete' not in st.session_state:
        st.session_state.verification_complete = False
    
    # Formulário principal
    if not st.session_state.verification_complete:
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                
                # Alerta informativo
                st.success("✅ **Sistema em Produção:** Processamento completo com IA, OCR e geração de relatórios profissionais")
                
                # Nome do conferente
                conferente = st.text_input(
                    "👤 Nome do servidor responsável pela conferência:",
                    placeholder="Digite seu nome completo",
                    key="conferente",
                    max_chars=100
                )
                
                # Sanitizar entrada se módulo de segurança disponível
                if SECURITY_ENABLED and conferente:
                    conferente = input_sanitizer.sanitize_text(conferente, max_length=100)
                
                # Upload de arquivo
                uploaded_file = st.file_uploader(
                    "📄 Selecione o documento para análise:",
                    type=['pdf', 'docx'],
                    help="Arquivos PDF ou DOCX até 16MB. Suporte a OCR para documentos digitalizados."
                )
                
                if uploaded_file:
                    # Validação de segurança
                    if SECURITY_ENABLED:
                        # Verificar tamanho
                        if uploaded_file.size > 16 * 1024 * 1024:  # 16MB
                            st.error("❌ Arquivo muito grande. Tamanho máximo: 16MB")
                            uploaded_file = None
                        else:
                            file_size_formatted = format_utils.format_file_size(uploaded_file.size)
                            st.info(f"📎 Arquivo selecionado: **{uploaded_file.name}** ({file_size_formatted})")
                    else:
                        st.info(f"📎 Arquivo selecionado: **{uploaded_file.name}** ({uploaded_file.size / 1024 / 1024:.2f} MB)")
                
                # Botão de análise
                if st.button("🚀 Iniciar Conferência", type="primary", disabled=not (conferente and uploaded_file)):
                    if conferente and uploaded_file:
                        # Salvar arquivo temporariamente
                        temp_path = UPLOAD_FOLDER / f"{uuid.uuid4()}_{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Processar documento
                        with st.spinner("🔍 Analisando documento..."):
                            # Extrair texto
                            if uploaded_file.name.lower().endswith('.pdf'):
                                full_text, pages_text = extract_text_from_pdf_with_pages(str(temp_path))
                            else:
                                full_text, pages_text = extract_text_from_docx_with_pages(str(temp_path))
                            
                            if not full_text.strip():
                                st.error("❌ Não foi possível extrair texto do documento.")
                                temp_path.unlink()
                                st.stop()
                            
                            # Carregar checklist
                            checklist_items = load_checklist_items()
                            
                            # Analisar cada item
                            progress_bar = st.progress(0)
                            resultados = {}
                            
                            for idx, (item_key, item_desc) in enumerate(checklist_items.items()):
                                progress_bar.progress((idx + 1) / len(checklist_items))
                                
                                # Analisar item - usar IA se disponível, senão usar análise básica
                                if model:
                                    status, justificativa, pagina = analyze_with_ai(
                                        int(item_key.replace("Item ", "")), 
                                        item_desc, 
                                        full_text
                                    )
                                else:
                                    # Análise básica por palavras-chave
                                    status, justificativa, pagina = analyze_by_keywords(
                                        int(item_key.replace("Item ", "")), 
                                        full_text
                                    )

                                
                                resultados[item_key] = {
                                    'status': status,
                                    'descricao': item_desc,
                                    'justificativa': justificativa,
                                    'pagina': pagina
                                }
                            
                            # Gerar ID único para verificação
                            verificacao_id = str(uuid.uuid4())[:8]
                            
                            # Salvar resultados na sessão
                            st.session_state.resultados = resultados
                            st.session_state.conferente = conferente
                            st.session_state.arquivo = uploaded_file.name
                            st.session_state.verificacao_id = verificacao_id
                            st.session_state.verification_complete = True
                            
                            # Salvar no banco de dados
                            conn = sqlite3.connect(DB_FOLDER / "verificacoes.db")
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO verificacoes (id, data_hora, conferente, arquivo, resultado_json, relatorio_path)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (
                                verificacao_id,
                                datetime.now(),
                                conferente,
                                uploaded_file.name,
                                json.dumps(resultados, ensure_ascii=False),
                                None
                            ))
                            conn.commit()
                            conn.close()
                            
                            # Limpar arquivo temporário
                            temp_path.unlink()
                            
                            # Recarregar página para mostrar resultados
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Exibir resultados
    else:
        # Estatísticas
        resultados = st.session_state.resultados
        total = len(resultados)
        cumpridos = sum(1 for r in resultados.values() if r['status'] == 'Sim')
        ausentes = sum(1 for r in resultados.values() if r['status'] == 'Não')
        nao_aplicaveis = sum(1 for r in resultados.values() if r['status'] == 'N/A')
        
        # Cards de estatísticas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{total}</div>
                <div class="stat-label">Total de Itens</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: #10b981;">{cumpridos}</div>
                <div class="stat-label">Cumpridos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: #ef4444;">{ausentes}</div>
                <div class="stat-label">Ausentes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number" style="color: #6b7280;">{nao_aplicaveis}</div>
                <div class="stat-label">Não Aplicáveis</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Detalhamento dos resultados
        st.markdown("### 📊 Detalhamento da Verificação")
        
        # Organizar resultados por status
        for status in ['Sim', 'Não', 'N/A']:
            items_status = [(k, v) for k, v in resultados.items() if v['status'] == status]
            
            if items_status:
                if status == 'Sim':
                    st.markdown("#### ✅ Itens Cumpridos")
                elif status == 'Não':
                    st.markdown("#### ❌ Itens Ausentes")
                else:
                    st.markdown("#### ⚪ Itens Não Aplicáveis")
                
                for item_key, resultado in items_status:
                    item_num = item_key.replace("Item ", "")
                    
                    with st.expander(f"**{item_key}** - {resultado['descricao'][:60]}..."):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Descrição completa:** {resultado['descricao']}")
                            if resultado.get('justificativa'):
                                st.write(f"**Justificativa:** {resultado['justificativa']}")
                        
                        with col2:
                            st.write(f"**Status:** {resultado['status']}")
                            st.write(f"**Página:** {resultado.get('pagina', 'N/I')}")
        
        # Botões de ação
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📥 Gerar Relatório PDF", type="primary"):
                with st.spinner("Gerando relatório..."):
                    report_path = generate_pdf_report(
                        st.session_state.conferente,
                        st.session_state.arquivo,
                        st.session_state.resultados,
                        st.session_state.verificacao_id
                    )
                    
                    if report_path and Path(report_path).exists():
                        # Atualizar banco de dados
                        conn = sqlite3.connect(DB_FOLDER / "verificacoes.db")
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE verificacoes SET relatorio_path = ? WHERE id = ?
                        """, (report_path, st.session_state.verificacao_id))
                        conn.commit()
                        conn.close()
                        
                        # Disponibilizar download
                        with open(report_path, "rb") as f:
                            pdf_bytes = f.read()
                        
                        st.download_button(
                            label="⬇️ Baixar Relatório PDF",
                            data=pdf_bytes,
                            file_name=f"relatorio_verificacao_{st.session_state.verificacao_id}.pdf",
                            mime="application/pdf"
                        )
        
        with col2:
            if st.button("📊 Exportar para Excel"):
                # Criar DataFrame
                df_data = []
                for item_key, resultado in resultados.items():
                    df_data.append({
                        'Item': item_key,
                        'Descrição': resultado['descricao'],
                        'Status': resultado['status'],
                        'Página': resultado.get('pagina', 'N/I'),
                        'Justificativa': resultado.get('justificativa', '')
                    })
                
                df = pd.DataFrame(df_data)
                
                # Converter para Excel
                output = BytesIO()
                # BytesIO funciona com pandas, ignorar warning do linter
                with pd.ExcelWriter(output, engine='openpyxl') as writer:  # type: ignore
                    df.to_excel(writer, index=False, sheet_name='Verificação')
                
                excel_data = output.getvalue()
                
                st.download_button(
                    label="⬇️ Baixar Excel",
                    data=excel_data,
                    file_name=f"verificacao_{st.session_state.verificacao_id}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col3:
            if st.button("🔄 Nova Verificação"):
                # Limpar sessão
                for key in ['resultados', 'conferente', 'arquivo', 'verificacao_id', 'verification_complete']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()

# Executar aplicação
if __name__ == "__main__":
    main() 