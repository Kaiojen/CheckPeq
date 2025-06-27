"""
Configurações centralizadas do Sistema de Verificação IN SEGES 65/2021
Versão 2.0 - Segurança aprimorada com variáveis de ambiente
"""

import os
import sys
from pathlib import Path
from typing import Optional
import logging
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Diretório base
BASE_DIR = Path(__file__).parent.parent

# =============================================================================
# CONFIGURAÇÕES DE SEGURANÇA
# =============================================================================

# API Keys - NUNCA hardcode em produção!
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Validar se a API key está configurada
if not GOOGLE_API_KEY:
    logger.warning(
        "⚠️ GOOGLE_API_KEY não configurada! "
        "Configure a variável de ambiente ou crie um arquivo .env"
    )
    # Em desenvolvimento, pode usar uma key temporária (remover em produção)
    if os.environ.get("FLASK_ENV") == "development":
        logger.warning("Modo desenvolvimento - usando configuração padrão temporária")
    else:
        logger.error("❌ GOOGLE_API_KEY é obrigatória em produção!")
        sys.exit(1)

# Secret Keys
SECRET_KEY = os.environ.get("SECRET_KEY", os.urandom(32).hex())
DATABASE_ENCRYPTION_KEY = os.environ.get("DATABASE_ENCRYPTION_KEY", os.urandom(32).hex())

# =============================================================================
# CONFIGURAÇÕES DE DIRETÓRIOS
# =============================================================================

UPLOAD_FOLDER = BASE_DIR / "uploads"
REPORTS_FOLDER = BASE_DIR / "reports"
DATABASE_FOLDER = BASE_DIR / "database"
TEMP_FOLDER = BASE_DIR / "temp"
LOGS_FOLDER = BASE_DIR / "logs"

# Criar diretórios se não existirem
for folder in [UPLOAD_FOLDER, REPORTS_FOLDER, DATABASE_FOLDER, TEMP_FOLDER, LOGS_FOLDER]:
    folder.mkdir(exist_ok=True, parents=True)

# =============================================================================
# CONFIGURAÇÕES DE UPLOAD E SEGURANÇA
# =============================================================================

MAX_FILE_SIZE = int(os.environ.get("MAX_UPLOAD_SIZE_MB", "16")) * 1024 * 1024  # MB para bytes
ALLOWED_EXTENSIONS = set(os.environ.get("ALLOWED_EXTENSIONS", "pdf,docx").split(","))

# Validação de nome de arquivo
FILENAME_REGEX = r'^[a-zA-Z0-9_\-\.]+$'
MAX_FILENAME_LENGTH = 255

# Rate limiting
RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "30"))

# =============================================================================
# CONFIGURAÇÕES DE PROCESSAMENTO
# =============================================================================

# OCR
OCR_MAX_PAGES = int(os.environ.get("OCR_MAX_PAGES", "10"))
OCR_LANGUAGE = os.environ.get("OCR_LANGUAGE", "por")
OCR_TIMEOUT = int(os.environ.get("OCR_TIMEOUT", "30"))  # segundos

# Análise com IA
MAX_TEXT_LENGTH_FOR_AI = int(os.environ.get("MAX_TEXT_LENGTH_FOR_AI", "5000"))
ANALYSIS_TIMEOUT = int(os.environ.get("ANALYSIS_TIMEOUT", "60"))  # segundos
AI_RETRY_ATTEMPTS = int(os.environ.get("AI_RETRY_ATTEMPTS", "3"))
AI_RETRY_DELAY = int(os.environ.get("AI_RETRY_DELAY", "2"))  # segundos

# =============================================================================
# CONFIGURAÇÕES DO BANCO DE DADOS
# =============================================================================

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATABASE_FOLDER}/verificacoes.db")
DATABASE_POOL_SIZE = int(os.environ.get("DATABASE_POOL_SIZE", "10"))
DATABASE_POOL_RECYCLE = int(os.environ.get("DATABASE_POOL_RECYCLE", "3600"))

# =============================================================================
# CONFIGURAÇÕES DE CACHE
# =============================================================================

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", "3600"))  # 1 hora
CACHE_KEY_PREFIX = os.environ.get("CACHE_KEY_PREFIX", "inseges:")

# =============================================================================
# CONFIGURAÇÕES DO SERVIDOR
# =============================================================================

# Flask
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("FLASK_PORT", "5000"))
FLASK_DEBUG = os.environ.get("FLASK_ENV") == "development"

# Streamlit
STREAMLIT_HOST = os.environ.get("STREAMLIT_HOST", "localhost")
STREAMLIT_PORT = int(os.environ.get("STREAMLIT_PORT", "8501"))

# =============================================================================
# CONFIGURAÇÕES DE RELATÓRIO
# =============================================================================

REPORT_PAGE_SIZE = 'A4'
REPORT_MARGINS = {
    'rightMargin': 2,  # cm
    'leftMargin': 2,   # cm
    'topMargin': 2,    # cm
    'bottomMargin': 2  # cm
}

# Assinatura digital
ENABLE_DIGITAL_SIGNATURE = os.environ.get("ENABLE_DIGITAL_SIGNATURE", "false").lower() == "true"
SIGNATURE_CERTIFICATE_PATH = os.environ.get("SIGNATURE_CERTIFICATE_PATH")

# =============================================================================
# CONFIGURAÇÕES DE LOG
# =============================================================================

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOGS_FOLDER / os.environ.get("LOG_FILE", "sistema.log")
LOG_MAX_BYTES = int(os.environ.get("LOG_MAX_BYTES", "10485760"))  # 10MB
LOG_BACKUP_COUNT = int(os.environ.get("LOG_BACKUP_COUNT", "5"))

# =============================================================================
# MENSAGENS DO SISTEMA
# =============================================================================

MESSAGES = {
    'no_file': 'Nenhum arquivo enviado',
    'no_text': 'Não foi possível extrair texto do documento',
    'processing_error': 'Erro ao processar o documento',
    'ai_error': 'Erro na análise com IA',
    'report_error': 'Erro ao gerar relatório',
    'success': 'Documento analisado com sucesso',
    'rate_limit': 'Limite de requisições excedido. Tente novamente em alguns minutos.',
    'invalid_file': 'Arquivo inválido ou formato não suportado',
    'file_too_large': f'Arquivo muito grande. Tamanho máximo: {MAX_FILE_SIZE / 1024 / 1024}MB'
}

# =============================================================================
# VALIDAÇÃO DE CONFIGURAÇÕES
# =============================================================================

def validate_config() -> bool:
    """Valida se todas as configurações críticas estão definidas"""
    errors = []
    
    if not GOOGLE_API_KEY and FLASK_DEBUG is False:
        errors.append("GOOGLE_API_KEY não configurada")
    
    if not SECRET_KEY:
        errors.append("SECRET_KEY não configurada")
    
    if not all([UPLOAD_FOLDER.exists(), REPORTS_FOLDER.exists(), DATABASE_FOLDER.exists()]):
        errors.append("Diretórios necessários não existem")
    
    if errors:
        for error in errors:
            logger.error(f"❌ Erro de configuração: {error}")
        return False
    
    logger.info("✅ Todas as configurações validadas com sucesso")
    return True

# Executar validação ao importar
if __name__ != "__main__":
    validate_config() 