#!/usr/bin/env python3
"""
Script de teste para verificar se todas as dependências estão instaladas corretamente
"""

import sys
import importlib
from pathlib import Path

print("=" * 60)
print("Sistema de Verificação IN SEGES 65/2021")
print("Teste de Instalação de Dependências")
print("=" * 60)
print()

# Lista de módulos necessários
required_modules = [
    ("streamlit", "Streamlit - Interface Web"),
    ("flask", "Flask - Servidor Web Alternativo"),
    ("pandas", "Pandas - Manipulação de Dados"),
    ("pdfplumber", "PDFPlumber - Extração de PDF"),
    ("fitz", "PyMuPDF - Processamento de PDF"),
    ("pdf2image", "PDF2Image - Conversão PDF para Imagem"),
    ("pytesseract", "Pytesseract - OCR"),
    ("docx", "Python-DOCX - Processamento de DOCX"),
    ("reportlab", "ReportLab - Geração de PDF"),
    ("PIL", "Pillow - Processamento de Imagens"),
    ("openpyxl", "OpenPyXL - Exportação Excel"),
    ("google.generativeai", "Google Generative AI - IA"),
    ("sqlite3", "SQLite3 - Banco de Dados"),
]

# Verificar Python
print(f"✓ Python {sys.version.split()[0]} instalado")
print()

# Verificar módulos
errors = []
warnings = []

for module_name, description in required_modules:
    try:
        if module_name == "google.generativeai":
            import google.generativeai as genai
        else:
            importlib.import_module(module_name)
        print(f"✓ {description:<40} OK")
    except ImportError as e:
        print(f"✗ {description:<40} ERRO")
        errors.append(f"{module_name}: {str(e)}")

print()

# Verificar Tesseract OCR
print("Verificando Tesseract OCR...")
try:
    import subprocess
    result = subprocess.run(['tesseract', '--version'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        version = result.stdout.split('\n')[0]
        print(f"✓ Tesseract OCR instalado: {version}")
    else:
        warnings.append("Tesseract OCR não encontrado (necessário apenas para PDFs digitalizados)")
except:
    warnings.append("Tesseract OCR não encontrado (necessário apenas para PDFs digitalizados)")

print()

# Verificar diretórios
print("Verificando estrutura de diretórios...")
directories = ['uploads', 'reports', 'database', 'src']
for dir_name in directories:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"✓ Diretório '{dir_name}' existe")
    else:
        print(f"✗ Diretório '{dir_name}' não encontrado")
        warnings.append(f"Diretório '{dir_name}' será criado automaticamente")

print()

# Verificar arquivos importantes
print("Verificando arquivos essenciais...")
files = [
    'requirements.txt',
    'src/app_streamlit.py',
    'src/main.py',
    'src/checklist_items.json',
    'src/config.py'
]
for file_name in files:
    file_path = Path(file_name)
    if file_path.exists():
        print(f"✓ Arquivo '{file_name}' existe")
    else:
        print(f"✗ Arquivo '{file_name}' não encontrado")
        errors.append(f"Arquivo essencial '{file_name}' não encontrado")

print()
print("=" * 60)

# Resumo
if not errors and not warnings:
    print("✅ SUCESSO: Todas as dependências estão instaladas corretamente!")
    print()
    print("Para executar o sistema:")
    print("  - Windows: run_streamlit.bat")
    print("  - Linux/Mac: streamlit run src/app_streamlit.py")
else:
    if errors:
        print("❌ ERROS ENCONTRADOS:")
        for error in errors:
            print(f"   - {error}")
        print()
        print("Para corrigir:")
        print("  pip install -r requirements.txt")
    
    if warnings:
        print()
        print("⚠️  AVISOS:")
        for warning in warnings:
            print(f"   - {warning}")

print()
print("=" * 60)

# Testar conexão com API (opcional)
try:
    print("\nTestando conexão com Google AI...")
    from src.config import GOOGLE_API_KEY
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Responda apenas: OK")
    if "OK" in response.text.upper():
        print("✓ Conexão com Google AI funcionando!")
    else:
        print("⚠️  API configurada mas resposta inesperada")
except Exception as e:
    print(f"⚠️  Erro ao testar API: {str(e)[:50]}...")
    print("   Verifique sua chave API e conexão com internet")

print()
input("Pressione ENTER para sair...") 