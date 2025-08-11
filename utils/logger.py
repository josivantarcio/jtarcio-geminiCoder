"""
Sistema de logging para o Gemini Coder.
"""

import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """Formatter com cores para logs no terminal."""
    
    # Códigos de cor ANSI
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        # Adicionar cor baseada no nível
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
        
        return super().format(record)


class GeminiLogger:
    """Logger personalizado para o Gemini Coder."""
    
    def __init__(self, name: str = "gemini_coder", log_dir: str = "logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura o logger."""
        self.logger.setLevel(logging.DEBUG)
        
        # Limpar handlers existentes
        self.logger.handlers.clear()
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Handler para arquivo
        if self._create_log_directory():
            file_handler = self._create_file_handler()
            if file_handler:
                self.logger.addHandler(file_handler)
    
    def _create_log_directory(self) -> bool:
        """Cria diretório de logs."""
        try:
            self.log_dir.mkdir(exist_ok=True)
            return True
        except Exception as e:
            print(f"Erro ao criar diretório de logs: {e}")
            return False
    
    def _create_file_handler(self) -> Optional[logging.Handler]:
        """Cria handler para arquivo com rotação."""
        try:
            log_file = self.log_dir / f"{self.name}.log"
            
            # Handler com rotação (máximo 10MB, manter 5 arquivos)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            
            return file_handler
        
        except Exception as e:
            print(f"Erro ao configurar log de arquivo: {e}")
            return None
    
    def set_level(self, level: str):
        """Define nível de log."""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        if level.upper() in level_map:
            self.logger.setLevel(level_map[level.upper()])
            # Atualizar nível do console handler
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                    handler.setLevel(level_map[level.upper()])
    
    def debug(self, message: str, **kwargs):
        """Log debug."""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info."""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning."""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error."""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical."""
        self.logger.critical(message, extra=kwargs)
    
    def log_tool_execution(self, tool_name: str, parameters: dict, result: dict):
        """Log específico para execução de ferramentas."""
        self.info(
            f"Tool executed: {tool_name}",
            tool=tool_name,
            params=parameters,
            success=result.get('success', False)
        )
        
        if not result.get('success', False):
            self.error(f"Tool failed: {tool_name} - {result.get('error', 'Unknown error')}")
    
    def log_ai_request(self, request: str, response: dict):
        """Log específico para requisições AI."""
        self.info(
            f"AI request processed",
            request_length=len(request),
            action=response.get('action', 'unknown')
        )
        
        self.debug(f"Request: {request[:200]}...")
        self.debug(f"Response: {str(response)[:500]}...")
    
    def log_context_update(self, context_info: dict):
        """Log específico para atualizações de contexto."""
        self.info(
            f"Context updated",
            project_path=context_info.get('path'),
            files_count=context_info.get('structure', {}).get('total_files', 0)
        )
    
    def log_performance(self, operation: str, duration: float):
        """Log de performance."""
        self.debug(f"Performance: {operation} took {duration:.3f}s")


# Instância global do logger
_logger: Optional[GeminiLogger] = None


def setup_logger(
    name: str = "gemini_coder", 
    log_dir: str = "logs", 
    level: str = "INFO"
) -> GeminiLogger:
    """Configura e retorna o logger global."""
    global _logger
    
    if _logger is None:
        _logger = GeminiLogger(name, log_dir)
    
    _logger.set_level(level)
    return _logger


def get_logger() -> GeminiLogger:
    """Obtém o logger global."""
    global _logger
    
    if _logger is None:
        _logger = setup_logger()
    
    return _logger