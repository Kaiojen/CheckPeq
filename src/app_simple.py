"""
Versão simplificada do Sistema para testes
Remove todas as dependências complexas para identificar o problema
"""

import streamlit as st
import os
from pathlib import Path
import json

# Configurações básicas da página
st.set_page_config(
    page_title="Sistema de Verificação - Teste Simples",
    page_icon="🧪",
    layout="wide"
)

# Título
st.title("🧪 Sistema de Verificação - Modo de Teste Simples")
st.write("Esta é uma versão simplificada para diagnóstico")

# Teste 1: Verificar se Streamlit está funcionando
st.header("1. Teste do Streamlit")
st.success("✅ Streamlit está funcionando corretamente!")

# Teste 2: Upload de arquivo básico
st.header("2. Teste de Upload de Arquivo")
uploaded_file = st.file_uploader("Escolha um arquivo", type=['pdf', 'docx', 'txt'])

if uploaded_file:
    st.write(f"✅ Arquivo recebido: {uploaded_file.name}")
    st.write(f"Tamanho: {uploaded_file.size} bytes")
    
    # Tentar ler o conteúdo (apenas para txt)
    if uploaded_file.name.endswith('.txt'):
        content = uploaded_file.read().decode('utf-8')
        st.text_area("Conteúdo do arquivo:", content[:500], height=200)

# Teste 3: Verificar diretórios
st.header("3. Verificação de Diretórios")
base_dir = Path(__file__).parent.parent

directories = {
    "Base": base_dir,
    "Src": base_dir / "src",
    "Database": base_dir / "database",
    "Reports": base_dir / "reports"
}

for name, path in directories.items():
    if path.exists():
        st.write(f"✅ {name}: {path} existe")
    else:
        st.write(f"❌ {name}: {path} NÃO existe")

# Teste 4: Verificar checklist
st.header("4. Verificação do Checklist")
checklist_path = Path("src/checklist_items.json")
if checklist_path.exists():
    with open(checklist_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
    st.write(f"✅ Checklist carregado: {len(items)} itens")
else:
    st.write("❌ Arquivo checklist_items.json não encontrado")

# Botão de teste
if st.button("🔄 Recarregar Página"):
    st.rerun()

st.markdown("---")
st.info("Se você consegue ver esta página, o Streamlit está funcionando. O problema está em outro lugar.") 