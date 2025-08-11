"""
Ferramentas para busca e análise de código.
"""

import os
import re
import subprocess
from typing import Dict, Any, List
from .base import Tool, ToolResult


class GrepTool(Tool):
    """Ferramenta para buscar texto em arquivos."""
    
    @property
    def name(self) -> str:
        return "grep"
    
    @property
    def description(self) -> str:
        return "Busca texto/padrões em arquivos usando regex"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Padrão regex a ser buscado"
                },
                "path": {
                    "type": "string",
                    "description": "Caminho onde buscar (arquivo ou diretório)",
                    "default": "."
                },
                "file_pattern": {
                    "type": "string",
                    "description": "Padrão de arquivos a incluir (ex: *.py)",
                    "default": "*"
                },
                "ignore_case": {
                    "type": "boolean",
                    "description": "Ignorar maiúsculas/minúsculas",
                    "default": False
                },
                "line_numbers": {
                    "type": "boolean",
                    "description": "Mostrar números das linhas",
                    "default": True
                }
            },
            "required": ["pattern"]
        }
    
    def execute(self, pattern: str = None, files: List[str] = None, path: str = ".", file_pattern: str = "*", 
                ignore_case: bool = False, line_numbers: bool = True) -> ToolResult:
        # Compatibilidade: aceitar tanto 'files' quanto 'pattern'
        if files and not pattern:
            pattern = files[0] if files else None
        
        if not pattern:
            return ToolResult(
                success=False,
                content=None,
                error="Parâmetro 'pattern' é obrigatório"
            )
        try:
            # Usar ripgrep se disponível, senão grep padrão
            cmd = []
            if subprocess.which('rg'):  # ripgrep
                cmd = ['rg', pattern, path]
                if ignore_case:
                    cmd.append('-i')
                if line_numbers:
                    cmd.append('-n')
                if file_pattern != "*":
                    cmd.extend(['-g', file_pattern])
            else:  # grep padrão
                cmd = ['grep', '-r', pattern, path]
                if ignore_case:
                    cmd.append('-i')
                if line_numbers:
                    cmd.append('-n')
                if file_pattern != "*":
                    cmd.extend(['--include', file_pattern])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )
            
            # grep retorna 1 quando não encontra matches, isso não é erro
            if result.returncode > 1:
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Erro na busca: {result.stderr}"
                )
            
            matches = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            return ToolResult(
                success=True,
                content=matches,
                metadata={
                    "pattern": pattern,
                    "path": path,
                    "file_pattern": file_pattern,
                    "matches_count": len(matches)
                }
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao buscar padrão: {str(e)}"
            )