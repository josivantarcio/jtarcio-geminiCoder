"""
Ferramentas para manipulação de arquivos.
"""

import os
import glob
from typing import Dict, Any
from .base import Tool, ToolResult


class ReadTool(Tool):
    """Ferramenta para ler arquivos."""
    
    @property
    def name(self) -> str:
        return "read"
    
    @property
    def description(self) -> str:
        return "Lê o conteúdo de um arquivo específico"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Caminho para o arquivo a ser lido"
                }
            },
            "required": ["file_path"]
        }
    
    def execute(self, file_path: str) -> ToolResult:
        try:
            if not os.path.exists(file_path):
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Arquivo '{file_path}' não encontrado"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return ToolResult(
                success=True,
                content=content,
                metadata={"file_path": file_path, "size": len(content)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao ler arquivo: {str(e)}"
            )


class WriteTool(Tool):
    """Ferramenta para escrever arquivos."""
    
    @property
    def name(self) -> str:
        return "write"
    
    @property
    def description(self) -> str:
        return "Escreve conteúdo em um arquivo (sobrescreve se existir)"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Caminho para o arquivo a ser criado/sobrescrito"
                },
                "content": {
                    "type": "string",
                    "description": "Conteúdo a ser escrito no arquivo"
                }
            },
            "required": ["file_path", "content"]
        }
    
    def execute(self, file_path: str, content: str) -> ToolResult:
        try:
            # Criar diretórios se necessário
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                content=f"Arquivo '{file_path}' criado/atualizado com sucesso",
                metadata={"file_path": file_path, "size": len(content)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao escrever arquivo: {str(e)}"
            )


class EditTool(Tool):
    """Ferramenta para editar arquivos existentes."""
    
    @property
    def name(self) -> str:
        return "edit"
    
    @property
    def description(self) -> str:
        return "Edita um arquivo existente substituindo texto específico"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Caminho para o arquivo a ser editado"
                },
                "old_text": {
                    "type": "string",
                    "description": "Texto a ser substituído"
                },
                "new_text": {
                    "type": "string",
                    "description": "Novo texto"
                }
            },
            "required": ["file_path", "old_text", "new_text"]
        }
    
    def execute(self, file_path: str, old_text: str, new_text: str) -> ToolResult:
        try:
            if not os.path.exists(file_path):
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Arquivo '{file_path}' não encontrado"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_text not in content:
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Texto '{old_text}' não encontrado no arquivo"
                )
            
            new_content = content.replace(old_text, new_text)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return ToolResult(
                success=True,
                content=f"Arquivo '{file_path}' editado com sucesso",
                metadata={
                    "file_path": file_path,
                    "replacements": content.count(old_text)
                }
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao editar arquivo: {str(e)}"
            )


class GlobTool(Tool):
    """Ferramenta para buscar arquivos por padrão."""
    
    @property
    def name(self) -> str:
        return "glob"
    
    @property
    def description(self) -> str:
        return "Busca arquivos usando padrões glob (ex: *.py, **/*.js)"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {
                    "type": "string",
                    "description": "Padrão glob para buscar arquivos"
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Se deve buscar recursivamente",
                    "default": True
                }
            },
            "required": ["pattern"]
        }
    
    def execute(self, pattern: str, recursive: bool = True) -> ToolResult:
        try:
            if recursive:
                files = glob.glob(pattern, recursive=True)
            else:
                files = glob.glob(pattern)
            
            files = [f for f in files if os.path.isfile(f)]
            files.sort()
            
            return ToolResult(
                success=True,
                content=files,
                metadata={
                    "pattern": pattern,
                    "count": len(files),
                    "recursive": recursive
                }
            )
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao buscar arquivos: {str(e)}"
            )