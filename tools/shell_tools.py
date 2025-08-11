"""
Ferramentas para execução de comandos shell.
"""

import subprocess
import shlex
from typing import Dict, Any
from .base import Tool, ToolResult


class BashTool(Tool):
    """Ferramenta para executar comandos bash."""
    
    @property
    def name(self) -> str:
        return "bash"
    
    @property
    def description(self) -> str:
        return "Executa comandos no shell bash"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Comando a ser executado"
                },
                "cwd": {
                    "type": "string",
                    "description": "Diretório de trabalho (opcional)",
                    "default": "."
                },
                "timeout": {
                    "type": "number",
                    "description": "Timeout em segundos (opcional)",
                    "default": 30
                }
            },
            "required": ["command"]
        }
    
    def execute(self, command: str = None, cwd: str = ".", timeout: int = 30) -> ToolResult:
        if not command:
            return ToolResult(
                success=False,
                content=None,
                error="Parâmetro 'command' é obrigatório"
            )
        try:
            # Usar shell=True para comandos complexos, mas validar entrada
            if any(dangerous in command for dangerous in ['rm -rf /', 'rm -rf *', 'format', 'del /f /s /q']):
                return ToolResult(
                    success=False,
                    content=None,
                    error="Comando potencialmente perigoso bloqueado"
                )
            
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return ToolResult(
                success=result.returncode == 0,
                content={
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                },
                metadata={
                    "command": command,
                    "cwd": cwd,
                    "timeout": timeout
                }
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                success=False,
                content=None,
                error=f"Comando excedeu timeout de {timeout} segundos"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao executar comando: {str(e)}"
            )