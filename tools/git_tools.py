"""
Ferramentas para operações Git.
"""

import subprocess
import os
from typing import Dict, Any
from .base import Tool, ToolResult


class GitStatusTool(Tool):
    """Ferramenta para verificar status do Git."""
    
    @property
    def name(self) -> str:
        return "git_status"
    
    @property
    def description(self) -> str:
        return "Mostra o status do repositório Git"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho do repositório (opcional)",
                    "default": "."
                }
            }
        }
    
    def execute(self, path: str = ".") -> ToolResult:
        try:
            if not os.path.exists(os.path.join(path, '.git')):
                return ToolResult(
                    success=False,
                    content=None,
                    error="Não é um repositório Git"
                )
            
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Erro Git: {result.stderr}"
                )
            
            return ToolResult(
                success=True,
                content=result.stdout,
                metadata={"path": path}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao verificar status Git: {str(e)}"
            )


class GitDiffTool(Tool):
    """Ferramenta para mostrar diff do Git."""
    
    @property
    def name(self) -> str:
        return "git_diff"
    
    @property
    def description(self) -> str:
        return "Mostra as diferenças no repositório Git"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Caminho do repositório (opcional)",
                    "default": "."
                },
                "staged": {
                    "type": "boolean",
                    "description": "Mostrar apenas arquivos staged",
                    "default": False
                }
            }
        }
    
    def execute(self, path: str = ".", staged: bool = False) -> ToolResult:
        try:
            cmd = ['git', 'diff']
            if staged:
                cmd.append('--staged')
            
            result = subprocess.run(
                cmd,
                cwd=path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Erro Git: {result.stderr}"
                )
            
            return ToolResult(
                success=True,
                content=result.stdout,
                metadata={"path": path, "staged": staged}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao executar git diff: {str(e)}"
            )


class GitCommitTool(Tool):
    """Ferramenta para fazer commits no Git."""
    
    @property
    def name(self) -> str:
        return "git_commit"
    
    @property
    def description(self) -> str:
        return "Faz commit das mudanças no Git"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Mensagem do commit"
                },
                "path": {
                    "type": "string",
                    "description": "Caminho do repositório (opcional)",
                    "default": "."
                },
                "add_all": {
                    "type": "boolean",
                    "description": "Adicionar todos os arquivos modificados",
                    "default": False
                }
            },
            "required": ["message"]
        }
    
    def execute(self, message: str, path: str = ".", add_all: bool = False) -> ToolResult:
        try:
            if add_all:
                # Adicionar arquivos
                result = subprocess.run(
                    ['git', 'add', '.'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    return ToolResult(
                        success=False,
                        content=None,
                        error=f"Erro ao adicionar arquivos: {result.stderr}"
                    )
            
            # Fazer commit
            result = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Erro ao fazer commit: {result.stderr}"
                )
            
            return ToolResult(
                success=True,
                content=result.stdout,
                metadata={"message": message, "path": path, "add_all": add_all}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao fazer commit: {str(e)}"
            )