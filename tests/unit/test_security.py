"""
Testes unitários para o módulo de segurança
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from security import (
    FileValidator,
    RateLimiter,
    SecurityUtils,
    InputSanitizer,
    SecurityAuditor
)

class TestFileValidator:
    """Testes para FileValidator"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.validator = FileValidator()
    
    def test_valid_pdf_file(self):
        """Testa arquivo PDF válido"""
        # PDF header
        content = b'%PDF-1.4\n%\xc7\xec\x8f\xa2\n'
        filename = "documento.pdf"
        
        is_valid, error = self.validator.validate_file(content, filename)
        assert is_valid is True
        assert error is None
    
    def test_valid_docx_file(self):
        """Testa arquivo DOCX válido"""
        # DOCX/ZIP header
        content = b'PK\x03\x04\x14\x00\x00\x00'
        filename = "documento.docx"
        
        is_valid, error = self.validator.validate_file(content, filename)
        assert is_valid is True
        assert error is None
    
    def test_invalid_extension(self):
        """Testa arquivo com extensão inválida"""
        content = b'test content'
        filename = "arquivo.exe"
        
        is_valid, error = self.validator.validate_file(content, filename)
        assert is_valid is False
        assert error is not None
        assert "Extensão não permitida" in error
    
    def test_file_too_large(self):
        """Testa arquivo muito grande"""
        # Criar conteúdo maior que o limite
        content = b'x' * (17 * 1024 * 1024)  # 17MB
        filename = "grande.pdf"
        
        is_valid, error = self.validator.validate_file(content, filename)
        assert is_valid is False
        assert error is not None
        assert "muito grande" in error
    
    def test_invalid_filename_characters(self):
        """Testa nome de arquivo com caracteres inválidos"""
        content = b'%PDF-1.4'
        filename = "../../etc/passwd"
        
        is_valid, error = self.validator.validate_filename(filename)
        assert is_valid is False
        assert error is not None
        assert "caracteres perigosos" in error
    
    def test_sanitize_filename(self):
        """Testa sanitização de nome de arquivo"""
        dangerous_name = "../../../etc/passwd.pdf"
        safe_name = self.validator.sanitize_filename(dangerous_name)
        
        assert ".." not in safe_name
        assert "/" not in safe_name
        assert "\\" not in safe_name


class TestRateLimiter:
    """Testes para RateLimiter"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.limiter = RateLimiter()
        self.limiter.rate_limit = 3  # Limite baixo para testes
    
    def test_allow_initial_requests(self):
        """Testa que requisições iniciais são permitidas"""
        identifier = "test_user"
        
        assert self.limiter.is_allowed(identifier) is True
        assert self.limiter.is_allowed(identifier) is True
        assert self.limiter.is_allowed(identifier) is True
    
    def test_block_after_limit(self):
        """Testa bloqueio após exceder limite"""
        identifier = "test_user"
        
        # Fazer 3 requisições (limite)
        for _ in range(3):
            self.limiter.is_allowed(identifier)
        
        # 4ª requisição deve ser bloqueada
        assert self.limiter.is_allowed(identifier) is False
    
    def test_cleanup_old_requests(self):
        """Testa limpeza de requisições antigas"""
        identifier = "test_user"
        
        # Adicionar requisições antigas manualmente
        old_time = datetime.now() - timedelta(hours=2)
        self.limiter.requests[identifier] = [old_time]
        
        # Forçar cleanup
        self.limiter._cleanup()
        
        # Verificar que foi removido
        assert identifier not in self.limiter.requests


class TestSecurityUtils:
    """Testes para SecurityUtils"""
    
    def test_generate_secure_token(self):
        """Testa geração de token seguro"""
        token1 = SecurityUtils.generate_secure_token()
        token2 = SecurityUtils.generate_secure_token()
        
        # Tokens devem ser diferentes
        assert token1 != token2
        
        # Tokens devem ter comprimento adequado
        assert len(token1) > 20
    
    def test_hash_file(self):
        """Testa hash de arquivo"""
        content = b"test content"
        hash1 = SecurityUtils.hash_file(content)
        hash2 = SecurityUtils.hash_file(content)
        
        # Mesmo conteúdo deve gerar mesmo hash
        assert hash1 == hash2
        
        # Hash deve ser SHA-256 (64 caracteres hex)
        assert len(hash1) == 64
        
        # Conteúdo diferente deve gerar hash diferente
        hash3 = SecurityUtils.hash_file(b"different content")
        assert hash1 != hash3


class TestInputSanitizer:
    """Testes para InputSanitizer"""
    
    def test_sanitize_text_removes_control_chars(self):
        """Testa remoção de caracteres de controle"""
        text = "Hello\x00World\x01\x02"
        sanitized = InputSanitizer.sanitize_text(text)
        
        assert sanitized == "HelloWorld"
    
    def test_sanitize_text_limits_length(self):
        """Testa limite de comprimento"""
        text = "x" * 2000
        sanitized = InputSanitizer.sanitize_text(text, max_length=100)
        
        assert len(sanitized) == 100
    
    def test_sanitize_sql(self):
        """Testa sanitização SQL"""
        dangerous = "'; DROP TABLE users; --"
        sanitized = InputSanitizer.sanitize_sql(dangerous)
        
        assert "'" not in sanitized
        assert ";" not in sanitized
        assert "--" not in sanitized
    
    def test_sanitize_html(self):
        """Testa escape de HTML"""
        html = '<script>alert("XSS")</script>'
        sanitized = InputSanitizer.sanitize_html(html)
        
        assert "<script>" not in sanitized
        assert "&lt;script&gt;" in sanitized


class TestSecurityAuditor:
    """Testes para SecurityAuditor"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.temp_log = Path("test_security.log")
        self.auditor = SecurityAuditor(self.temp_log)
    
    def teardown_method(self):
        """Cleanup após cada teste"""
        if self.temp_log.exists():
            self.temp_log.unlink()
    
    def test_log_event(self):
        """Testa log de evento"""
        self.auditor.log_event(
            "TEST_EVENT",
            {"action": "test", "user": "test_user"},
            "INFO"
        )
        
        # Verificar que arquivo foi criado
        assert self.temp_log.exists()
        
        # Verificar conteúdo
        content = self.temp_log.read_text()
        assert "TEST_EVENT" in content
        assert "test_user" in content
    
    def test_log_file_upload(self):
        """Testa log de upload de arquivo"""
        self.auditor.log_file_upload(
            filename="test.pdf",
            size=1024,
            user="test_user",
            valid=True
        )
        
        content = self.temp_log.read_text()
        assert "FILE_UPLOAD" in content
        assert "test.pdf" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
