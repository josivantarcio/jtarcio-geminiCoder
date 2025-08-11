"""
Sistema de debugging para o Gemini Coder.
"""

import os
import json
import time
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from functools import wraps
from pathlib import Path

from .logger import get_logger


class DebugManager:
    """Gerenciador de debugging avançado."""
    
    def __init__(self, debug_dir: str = "debug"):
        self.debug_dir = Path(debug_dir)
        self.logger = get_logger()
        self.debug_enabled = os.getenv("GEMINI_DEBUG", "false").lower() in ("true", "1", "yes")
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.debug_enabled:
            self._setup_debug_environment()
    
    def _setup_debug_environment(self):
        """Configura ambiente de debug."""
        try:
            self.debug_dir.mkdir(exist_ok=True)
            
            # Arquivo de sessão atual
            self.session_file = self.debug_dir / f"session_{self.session_id}.json"
            
            # Log inicial
            self.logger.debug(f"Debug mode enabled. Session: {self.session_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to setup debug environment: {e}")
            self.debug_enabled = False
    
    def is_enabled(self) -> bool:
        """Verifica se debug está habilitado."""
        return self.debug_enabled
    
    def log_session_start(self, config: Dict[str, Any]):
        """Log início da sessão."""
        if not self.debug_enabled:
            return
        
        session_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "config": self._sanitize_config(config),
            "environment": {
                "python_version": os.sys.version,
                "platform": os.sys.platform,
                "cwd": os.getcwd(),
                "env_vars": {k: v for k, v in os.environ.items() if "GEMINI" in k}
            },
            "events": []
        }
        
        self._write_session_data(session_data)
    
    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log evento de debug."""
        if not self.debug_enabled:
            return
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }
        
        try:
            session_data = self._read_session_data()
            session_data["events"].append(event)
            self._write_session_data(session_data)
            
        except Exception as e:
            self.logger.error(f"Failed to log debug event: {e}")
    
    def log_tool_execution(self, tool_name: str, parameters: Dict[str, Any], result: Any, duration: float):
        """Log execução de ferramenta."""
        self.log_event("tool_execution", {
            "tool_name": tool_name,
            "parameters": parameters,
            "result_type": type(result).__name__,
            "success": getattr(result, 'success', None),
            "duration": duration,
            "error": getattr(result, 'error', None)
        })
    
    def log_ai_interaction(self, request: str, context_length: int, response: Dict[str, Any], duration: float):
        """Log interação com AI."""
        self.log_event("ai_interaction", {
            "request_length": len(request),
            "request_preview": request[:200] + "..." if len(request) > 200 else request,
            "context_length": context_length,
            "response_action": response.get("action"),
            "duration": duration
        })
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log erro com contexto."""
        error_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        
        self.log_event("error", error_data)
        self.logger.error(f"Error logged: {error_data['error_type']}: {error_data['error_message']}")
    
    def log_performance_metric(self, operation: str, duration: float, metadata: Dict[str, Any] = None):
        """Log métrica de performance."""
        self.log_event("performance", {
            "operation": operation,
            "duration": duration,
            "metadata": metadata or {}
        })
    
    def debug_decorator(self, operation_name: str):
        """Decorator para debug automático de funções."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.debug_enabled:
                    return func(*args, **kwargs)
                
                start_time = time.time()
                
                try:
                    # Log entrada
                    self.log_event("function_enter", {
                        "function": f"{func.__module__}.{func.__name__}",
                        "operation": operation_name,
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys())
                    })
                    
                    # Executar função
                    result = func(*args, **kwargs)
                    
                    # Log sucesso
                    duration = time.time() - start_time
                    self.log_event("function_exit", {
                        "function": f"{func.__module__}.{func.__name__}",
                        "operation": operation_name,
                        "duration": duration,
                        "success": True,
                        "result_type": type(result).__name__
                    })
                    
                    return result
                
                except Exception as e:
                    # Log erro
                    duration = time.time() - start_time
                    self.log_event("function_error", {
                        "function": f"{func.__module__}.{func.__name__}",
                        "operation": operation_name,
                        "duration": duration,
                        "error": str(e),
                        "error_type": type(e).__name__
                    })
                    raise
            
            return wrapper
        return decorator
    
    def create_debug_snapshot(self, name: str, data: Dict[str, Any]):
        """Cria snapshot de debug."""
        if not self.debug_enabled:
            return
        
        snapshot_file = self.debug_dir / f"snapshot_{name}_{int(time.time())}.json"
        
        try:
            with open(snapshot_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "session_id": self.session_id,
                    "name": name,
                    "data": data
                }, f, indent=2, default=str)
            
            self.logger.debug(f"Debug snapshot created: {snapshot_file}")
        
        except Exception as e:
            self.logger.error(f"Failed to create debug snapshot: {e}")
    
    def get_debug_summary(self) -> Dict[str, Any]:
        """Obtém resumo da sessão de debug."""
        if not self.debug_enabled:
            return {"debug_enabled": False}
        
        try:
            session_data = self._read_session_data()
            events = session_data.get("events", [])
            
            summary = {
                "debug_enabled": True,
                "session_id": self.session_id,
                "total_events": len(events),
                "event_types": {},
                "errors": [],
                "performance": {}
            }
            
            # Analisar eventos
            total_duration = 0
            for event in events:
                event_type = event["type"]
                summary["event_types"][event_type] = summary["event_types"].get(event_type, 0) + 1
                
                if event_type == "error":
                    summary["errors"].append({
                        "timestamp": event["timestamp"],
                        "error": event["data"]["error_message"]
                    })
                
                elif event_type == "performance":
                    duration = event["data"]["duration"]
                    operation = event["data"]["operation"]
                    
                    if operation not in summary["performance"]:
                        summary["performance"][operation] = {
                            "count": 0,
                            "total_duration": 0,
                            "avg_duration": 0
                        }
                    
                    summary["performance"][operation]["count"] += 1
                    summary["performance"][operation]["total_duration"] += duration
                    summary["performance"][operation]["avg_duration"] = (
                        summary["performance"][operation]["total_duration"] / 
                        summary["performance"][operation]["count"]
                    )
            
            return summary
        
        except Exception as e:
            self.logger.error(f"Failed to generate debug summary: {e}")
            return {"debug_enabled": True, "error": str(e)}
    
    def _sanitize_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Remove dados sensíveis da configuração."""
        sanitized = config.copy()
        
        # Mascarar API key
        if "gemini_api_key" in sanitized and sanitized["gemini_api_key"]:
            key = sanitized["gemini_api_key"]
            sanitized["gemini_api_key"] = key[:8] + "..." + key[-4:]
        
        return sanitized
    
    def _read_session_data(self) -> Dict[str, Any]:
        """Lê dados da sessão."""
        if not self.session_file.exists():
            return {"events": []}
        
        with open(self.session_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _write_session_data(self, data: Dict[str, Any]):
        """Escreve dados da sessão."""
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)


# Instância global do debug manager
_debug_manager: Optional[DebugManager] = None


def get_debug_manager() -> DebugManager:
    """Obtém o debug manager global."""
    global _debug_manager
    
    if _debug_manager is None:
        _debug_manager = DebugManager()
    
    return _debug_manager


def debug_function(operation_name: str):
    """Decorator para debug de função."""
    return get_debug_manager().debug_decorator(operation_name)