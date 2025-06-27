"""
Módulo de segurança para o Sistema de Verificação IN SEGES 65/2021
Implementa validações, sanitização e proteções contra ataques
"""

import re
import os
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Tuple, List
from functools import wraps
from datetime import datetime, timedelta
import logging
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# =============================================================================
# VALIDAÇÃO DE ARQUIVOS
# =============================================================================

class FileValidator:
    """Classe para validação segura de arquivos"""
    
    def __init__(self):
        self.mime_types = {
            'pdf': ['application/pdf'],
            'docx': [
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword'
            ]
        }
        # Importar configurações aqui para evitar importação circular
        from config import (
            ALLOWED_EXTENSIONS, 
            MAX_FILE_SIZE, 
            FILENAME_REGEX,
            MAX_FILENAME_LENGTH
        )
        self.allowed_extensions = ALLOWED_EXTENSIONS
        self.max_file_size = MAX_FILE_SIZE
        self.filename_regex = FILENAME_REGEX
        self.max_filename_length = MAX_FILENAME_LENGTH
    
    def validate_file(self, file_content: bytes, filename: str) -> Tuple[bool, Optional[str]]:
        """
        Valida arquivo completamente
        
        Returns:
            Tuple[bool, Optional[str]]: (válido, mensagem_erro)
        """
        # Validar nome do arquivo
        is_valid, error = self.validate_filename(filename)
        if not is_valid:
            return False, error
        
        # Validar tamanho
        if len(file_content) > self.max_file_size:
            return False, f"Arquivo muito grande. Máximo: {self.max_file_size / 1024 / 1024}MB"
        
        # Validar extensão
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if extension not in self.allowed_extensions:
            return False, f"Extensão não permitida. Use: {', '.join(self.allowed_extensions)}"
        
        # Verificar assinatura do arquivo (magic numbers)
        if not self._check_file_signature(file_content, extension):
            return False, "Arquivo corrompido ou tipo incorreto"
        
        return True, None
    
    def validate_filename(self, filename: str) -> Tuple[bool, Optional[str]]:
        """Valida nome do arquivo contra injeções"""
        # Verificar comprimento
        if len(filename) > self.max_filename_length:
            return False, "Nome do arquivo muito longo"
        
        # Verificar caracteres permitidos
        if not re.match(self.filename_regex, filename):
            return False, "Nome do arquivo contém caracteres inválidos"
        
        # Verificar path traversal
        if any(danger in filename for danger in ['..', '/', '\\', '\x00']):
            return False, "Nome do arquivo contém caracteres perigosos"
        
        return True, None
    
    def _check_file_signature(self, content: bytes, extension: str) -> bool:
        """Verifica assinatura binária do arquivo"""
        signatures = {
            'pdf': b'%PDF',
            'docx': b'PK\x03\x04'  # ZIP signature (DOCX é um ZIP)
        }
        
        expected_sig = signatures.get(extension)
        if not expected_sig:
            return True  # Se não temos assinatura, assumir válido
        
        return content.startswith(expected_sig)
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitiza nome de arquivo mantendo extensão"""
        # Usar secure_filename do Werkzeug
        filename = secure_filename(filename)
        
        # Se filename ficou vazio, gerar um nome
        if not filename:
            filename = f"documento_{secrets.token_hex(8)}.pdf"
        
        return filename

# =============================================================================
# RATE LIMITING
# =============================================================================

class RateLimiter:
    """Implementa rate limiting simples em memória"""
    
    def __init__(self):
        self.requests = {}  # {ip: [(timestamp, count)]}
        self.cleanup_interval = 300  # 5 minutos
        self.last_cleanup = datetime.now()
        # Importar configuração aqui
        from config import RATE_LIMIT_PER_MINUTE
        self.rate_limit = RATE_LIMIT_PER_MINUTE
    
    def is_allowed(self, identifier: str) -> bool:
        """Verifica se requisição é permitida"""
        now = datetime.now()
        
        # Limpar dados antigos periodicamente
        if (now - self.last_cleanup).seconds > self.cleanup_interval:
            self._cleanup()
        
        # Obter requisições do último minuto
        minute_ago = now - timedelta(minutes=1)
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Filtrar requisições antigas
        self.requests[identifier] = [
            req for req in self.requests[identifier] 
            if req > minute_ago
        ]
        
        # Verificar limite
        if len(self.requests[identifier]) >= self.rate_limit:
            logger.warning(f"Rate limit excedido para: {identifier}")
            return False
        
        # Adicionar nova requisição
        self.requests[identifier].append(now)
        return True
    
    def _cleanup(self):
        """Remove dados antigos"""
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        
        for identifier in list(self.requests.keys()):
            self.requests[identifier] = [
                req for req in self.requests[identifier]
                if req > hour_ago
            ]
            if not self.requests[identifier]:
                del self.requests[identifier]
        
        self.last_cleanup = now

# =============================================================================
# CRIPTOGRAFIA E HASHING
# =============================================================================

class SecurityUtils:
    """Utilitários de segurança"""
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Gera token seguro"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def hash_file(content: bytes) -> str:
        """Gera hash SHA-256 do arquivo"""
        return hashlib.sha256(content).hexdigest()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash de senha usando SHA-256 com salt"""
        salt = secrets.token_hex(16)
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verifica senha (implementação simplificada)"""
        # Em produção, usar bcrypt ou similar
        return SecurityUtils.hash_password(password) == hashed

# =============================================================================
# SANITIZAÇÃO DE ENTRADA
# =============================================================================

class InputSanitizer:
    """Sanitiza entradas do usuário"""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 1000) -> str:
        """Sanitiza texto removendo caracteres perigosos"""
        # Remover caracteres de controle
        text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        # Limitar comprimento
        text = text[:max_length]
        
        # Remover múltiplos espaços
        text = ' '.join(text.split())
        
        return text.strip()
    
    @staticmethod
    def sanitize_sql(value: str) -> str:
        """Sanitiza valor para SQL (usar com cuidado, prefira prepared statements)"""
        # Remover caracteres perigosos para SQL
        dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
        for char in dangerous_chars:
            value = value.replace(char, '')
        return value
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Escapa HTML para prevenir XSS"""
        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            ">": "&gt;",
            "<": "&lt;",
        }
        return "".join(html_escape_table.get(c, c) for c in text)

# =============================================================================
# DECORADORES DE SEGURANÇA
# =============================================================================

def require_auth(f):
    """Decorador para exigir autenticação (exemplo)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Implementar lógica de autenticação aqui
        # Por enquanto, apenas passa
        return f(*args, **kwargs)
    return decorated_function

def validate_input(param_name: str, validator_func):
    """Decorador para validar parâmetros de entrada"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if param_name in kwargs:
                value = kwargs[param_name]
                is_valid, error = validator_func(value)
                if not is_valid:
                    raise ValueError(f"Parâmetro inválido {param_name}: {error}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =============================================================================
# AUDITORIA
# =============================================================================

class SecurityAuditor:
    """Registra eventos de segurança"""
    
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or Path("logs/security.log")
        self.log_file.parent.mkdir(exist_ok=True, parents=True)
    
    def log_event(self, event_type: str, details: dict, severity: str = "INFO"):
        """Registra evento de segurança"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "type": event_type,
            "severity": severity,
            "details": details
        }
        
        # Log para arquivo
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} [{severity}] {event_type}: {details}\n")
        except Exception as e:
            logger.error(f"Erro ao gravar log de segurança: {e}")
        
        # Log para sistema
        log_func = getattr(logger, severity.lower(), logger.info)
        log_func(f"Security event: {event_type} - {details}")
    
    def log_access(self, user: str, resource: str, action: str, success: bool):
        """Registra tentativa de acesso"""
        self.log_event(
            "ACCESS_ATTEMPT",
            {
                "user": user,
                "resource": resource,
                "action": action,
                "success": success
            },
            severity="WARNING" if not success else "INFO"
        )
    
    def log_file_upload(self, filename: str, size: int, user: str, valid: bool):
        """Registra upload de arquivo"""
        self.log_event(
            "FILE_UPLOAD",
            {
                "filename": filename,
                "size": size,
                "user": user,
                "valid": valid
            },
            severity="WARNING" if not valid else "INFO"
        )

# Instâncias globais
file_validator = FileValidator()
rate_limiter = RateLimiter()
security_utils = SecurityUtils()
input_sanitizer = InputSanitizer()
security_auditor = SecurityAuditor()
 