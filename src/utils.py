"""
Módulo de utilidades para o Sistema de Verificação IN SEGES 65/2021
Contém funções auxiliares e helpers reutilizáveis
"""

import os
import hashlib
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
import json
import tempfile
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import functools
import time

logger = logging.getLogger(__name__)

# =============================================================================
# DECORADORES ÚTEIS
# =============================================================================

def timing_decorator(func):
    """Decorador para medir tempo de execução"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"{func.__name__} levou {elapsed_time:.2f}s para executar")
            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"{func.__name__} falhou após {elapsed_time:.2f}s: {e}")
            raise
    return wrapper

def retry_decorator(max_attempts: int = 3, delay: float = 1.0):
    """Decorador para retry automático"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt < max_attempts - 1:
                        logger.warning(f"Tentativa {attempt + 1} falhou: {e}. Tentando novamente...")
                        time.sleep(delay * (attempt + 1))  # Backoff exponencial
                    else:
                        logger.error(f"Todas as {max_attempts} tentativas falharam")
                        raise
            return None
        return wrapper
    return decorator

def cache_result(ttl_seconds: int = 3600):
    """Decorador simples de cache em memória"""
    cache = {}
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Criar chave de cache
            cache_key = hashlib.md5(
                f"{func.__name__}:{args}:{kwargs}".encode()
            ).hexdigest()
            
            # Verificar cache
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl_seconds:
                    logger.debug(f"Cache hit para {func.__name__}")
                    return result
            
            # Executar função e cachear
            result = func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            
            # Limpar cache antigo
            _cleanup_cache(cache, ttl_seconds)
            
            return result
        return wrapper
    return decorator

def _cleanup_cache(cache: dict, ttl_seconds: int):
    """Remove entradas expiradas do cache"""
    current_time = time.time()
    expired_keys = [
        key for key, (_, timestamp) in cache.items()
        if current_time - timestamp > ttl_seconds
    ]
    for key in expired_keys:
        del cache[key]

# =============================================================================
# PROCESSAMENTO ASSÍNCRONO
# =============================================================================

class AsyncProcessor:
    """Classe para processamento assíncrono de tarefas"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.thread_executor = ThreadPoolExecutor(max_workers=max_workers)
        self.process_executor = ProcessPoolExecutor(max_workers=max_workers)
    
    async def process_files_async(self, files: List[Path], processor_func) -> List[Any]:
        """Processa múltiplos arquivos de forma assíncrona"""
        loop = asyncio.get_event_loop()
        
        # Criar tarefas
        tasks = []
        for file in files:
            task = loop.run_in_executor(
                self.thread_executor,
                processor_func,
                file
            )
            tasks.append(task)
        
        # Aguardar conclusão
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar erros
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Erro ao processar {files[i]}: {result}")
            else:
                processed_results.append(result)
        
        return processed_results
    
    def cleanup(self):
        """Limpa recursos"""
        self.thread_executor.shutdown(wait=True)
        self.process_executor.shutdown(wait=True)

# =============================================================================
# MANIPULAÇÃO DE ARQUIVOS
# =============================================================================

class FileUtils:
    """Utilitários para manipulação de arquivos"""
    
    @staticmethod
    def get_file_hash(file_path: Path) -> str:
        """Calcula hash SHA-256 de um arquivo"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    @staticmethod
    def safe_file_write(file_path: Path, content: str, encoding: str = 'utf-8'):
        """Escreve arquivo de forma segura (atomic write)"""
        # Criar diretório se não existir
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Escrever em arquivo temporário primeiro
        with tempfile.NamedTemporaryFile(
            mode='w',
            encoding=encoding,
            delete=False,
            dir=file_path.parent
        ) as tmp_file:
            tmp_file.write(content)
            tmp_path = Path(tmp_file.name)
        
        # Mover arquivo temporário para destino final
        tmp_path.replace(file_path)
    
    @staticmethod
    def cleanup_old_files(directory: Path, days: int = 30) -> int:
        """Remove arquivos mais antigos que X dias"""
        if not directory.exists():
            return 0
        
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        removed_count = 0
        
        for file_path in directory.iterdir():
            if file_path.is_file():
                if file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        removed_count += 1
                        logger.info(f"Arquivo removido: {file_path}")
                    except Exception as e:
                        logger.error(f"Erro ao remover {file_path}: {e}")
        
        return removed_count

# =============================================================================
# FORMATAÇÃO E CONVERSÃO
# =============================================================================

class FormatUtils:
    """Utilitários de formatação"""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Formata tamanho de arquivo para exibição"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def format_duration(seconds: float) -> str:
        """Formata duração em formato legível"""
        if seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes}min"
        else:
            hours = int(seconds / 3600)
            return f"{hours}h"
    
    @staticmethod
    def sanitize_for_filename(text: str, max_length: int = 50) -> str:
        """Sanitiza texto para uso em nome de arquivo"""
        # Remover caracteres inválidos
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            text = text.replace(char, '')
        
        # Limitar comprimento
        if len(text) > max_length:
            text = text[:max_length]
        
        # Remover espaços extras
        text = ' '.join(text.split())
        
        return text.strip()

# =============================================================================
# ANÁLISE DE DOCUMENTOS
# =============================================================================

class DocumentAnalyzer:
    """Utilitários para análise de documentos"""
    
    @staticmethod
    def extract_metadata(file_path: Path) -> Dict[str, Any]:
        """Extrai metadados de um arquivo"""
        stat = file_path.stat()
        
        metadata = {
            'filename': file_path.name,
            'size': stat.st_size,
            'size_formatted': FormatUtils.format_file_size(stat.st_size),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'extension': file_path.suffix.lower(),
            'hash': FileUtils.get_file_hash(file_path)
        }
        
        return metadata
    
    @staticmethod
    def chunk_text(text: str, chunk_size: int = 5000, overlap: int = 500) -> List[str]:
        """Divide texto em chunks com overlap"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            
            # Tentar quebrar em fim de sentença
            if end < text_length:
                # Procurar pontos de quebra naturais
                for delimiter in ['. ', '.\n', '! ', '? ', '\n\n']:
                    last_delimiter = text.rfind(delimiter, start, end)
                    if last_delimiter != -1:
                        end = last_delimiter + len(delimiter)
                        break
            
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Próximo chunk com overlap
            start = end - overlap if end < text_length else text_length
        
        return chunks
    
    @staticmethod
    def count_words(text: str) -> int:
        """Conta palavras em um texto"""
        return len(text.split())
    
    @staticmethod
    def estimate_reading_time(text: str, wpm: int = 200) -> float:
        """Estima tempo de leitura em minutos"""
        word_count = DocumentAnalyzer.count_words(text)
        return word_count / wpm

# =============================================================================
# VALIDAÇÃO DE DADOS
# =============================================================================

class ValidationUtils:
    """Utilitários de validação"""
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Valida CPF brasileiro"""
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        for i in range(9, 11):
            value = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != int(cpf[i]):
                return False
        
        return True
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Valida CNPJ brasileiro"""
        # Remove caracteres não numéricos
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj) != 14:
            return False
        
        # Validação simplificada
        # Em produção, implementar validação completa
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

# =============================================================================
# HELPERS DE CONFIGURAÇÃO
# =============================================================================

class ConfigHelper:
    """Helpers para configuração"""
    
    @staticmethod
    def get_env_bool(key: str, default: bool = False) -> bool:
        """Obtém variável de ambiente booleana"""
        value = os.environ.get(key, '').lower()
        if value in ('true', '1', 'yes', 'on'):
            return True
        elif value in ('false', '0', 'no', 'off'):
            return False
        return default
    
    @staticmethod
    def get_env_list(key: str, delimiter: str = ',') -> List[str]:
        """Obtém lista de valores de variável de ambiente"""
        value = os.environ.get(key, '')
        if not value:
            return []
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    
    @staticmethod
    def generate_secret_key(length: int = 32) -> str:
        """Gera chave secreta segura"""
        import secrets
        return secrets.token_hex(length)

# Instâncias globais para uso conveniente
file_utils = FileUtils()
format_utils = FormatUtils()
document_analyzer = DocumentAnalyzer()
validation_utils = ValidationUtils()
config_helper = ConfigHelper()