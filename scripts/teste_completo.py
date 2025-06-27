#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Teste Completo do Sistema
Verifica todas as dependências e componentes
"""

import sys
import os
import json
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

print("=" * 60)
print("TESTE COMPLETO DO SISTEMA")
print("=" * 60)

# 1. Testar importações básicas
print("\n[1] Testando importações básicas...")
try:
    import streamlit as st
    print("✅ Streamlit importado")
except ImportError as e:
    print(f"❌ Erro ao importar Streamlit: {e}")

try:
    import pandas as pd
    print("✅ Pandas importado")
except ImportError as e:
    print(f"❌ Erro ao importar Pandas: {e}")

try:
    import pdfplumber
    print("✅ PDFPlumber importado")
except ImportError as e:
    print(f"❌ Erro ao importar PDFPlumber: {e}")

try:
    import docx
    print("✅ Python-docx importado")
except ImportError as e:
    print(f"❌ Erro ao importar Python-docx: {e}")

try:
    import google.generativeai as genai
    print("✅ Google AI importado")
except ImportError as e:
    print(f"❌ Erro ao importar Google AI: {e}")

# 2. Testar configurações
print("\n[2] Testando configurações...")
try:
    from config import GOOGLE_API_KEY, UPLOAD_FOLDER, REPORTS_FOLDER, DATABASE_FOLDER
    print("✅ Config importado")
    print(f"   - GOOGLE_API_KEY: {'Configurada' if GOOGLE_API_KEY else 'NÃO configurada'}")
    print(f"   - UPLOAD_FOLDER: {UPLOAD_FOLDER}")
    print(f"   - REPORTS_FOLDER: {REPORTS_FOLDER}")
    print(f"   - DATABASE_FOLDER: {DATABASE_FOLDER}")
except Exception as e:
    print(f"❌ Erro ao importar config: {e}")

# 3. Testar módulos de segurança
print("\n[3] Testando módulos de segurança...")
try:
    from security import file_validator, security_auditor, input_sanitizer
    print("✅ Módulo security importado")
except Exception as e:
    print(f"⚠️  Módulo security não disponível: {e}")

try:
    from utils import format_utils, document_analyzer
    print("✅ Módulo utils importado")
except Exception as e:
    print(f"⚠️  Módulo utils não disponível: {e}")

# 4. Verificar diretórios
print("\n[4] Verificando diretórios...")
base_dir = Path(__file__).parent.parent

dirs_to_check = {
    "src": base_dir / "src",
    "database": base_dir / "database",
    "reports": base_dir / "reports",
    "uploads": base_dir / "uploads",
    "temp": base_dir / "temp"
}

for name, path in dirs_to_check.items():
    if path.exists():
        print(f"✅ {name}: {path}")
    else:
        print(f"❌ {name}: {path} NÃO existe")
        # Criar diretório
        try:
            path.mkdir(exist_ok=True, parents=True)
            print(f"   ↳ Diretório criado")
        except Exception as e:
            print(f"   ↳ Erro ao criar: {e}")

# 5. Verificar checklist
print("\n[5] Verificando arquivo checklist...")
checklist_path = base_dir / "src" / "checklist_items.json"
if checklist_path.exists():
    try:
        with open(checklist_path, 'r', encoding='utf-8') as f:
            items = json.load(f)
        print(f"✅ Checklist carregado: {len(items)} itens")
    except Exception as e:
        print(f"❌ Erro ao carregar checklist: {e}")
else:
    print(f"❌ Arquivo checklist não encontrado em: {checklist_path}")

# 6. Testar conexão com Google AI
print("\n[6] Testando conexão com Google AI...")
try:
    from config import GOOGLE_API_KEY
    if GOOGLE_API_KEY:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Responda apenas: OK")
        print(f"✅ Google AI funcionando: {response.text.strip()}")
    else:
        print("⚠️  GOOGLE_API_KEY não configurada")
except Exception as e:
    print(f"❌ Erro ao conectar com Google AI: {e}")

# 7. Verificar arquivo .env
print("\n[7] Verificando arquivo .env...")
env_path = base_dir / ".env"
if env_path.exists():
    print(f"✅ Arquivo .env existe")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            print(f"   - GOOGLE_API_KEY carregada do .env: {api_key[:20]}...")
        else:
            print("   - GOOGLE_API_KEY não encontrada no .env")
    except Exception as e:
        print(f"   - Erro ao carregar .env: {e}")
else:
    print("❌ Arquivo .env não encontrado")
    print("   ↳ Crie um arquivo .env baseado no env.example")

# 8. Testar processamento de arquivo simples
print("\n[8] Testando processamento de arquivo...")
test_file = base_dir / "COMO_USAR.txt"
if test_file.exists():
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Leitura de arquivo OK: {len(content)} caracteres")
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
else:
    print("⚠️  Arquivo de teste não encontrado")

# Resumo final
print("\n" + "=" * 60)
print("RESUMO DO TESTE")
print("=" * 60)
print("\nSe houver erros acima, execute:")
print("1. INSTALAR.bat para reinstalar dependências")
print("2. CONFIGURAR_API.bat para configurar a API do Google")
print("3. Certifique-se de que o arquivo .env existe")
print("\nPressione ENTER para sair...")
input() 