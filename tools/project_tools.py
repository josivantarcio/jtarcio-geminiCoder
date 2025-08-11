"""
Ferramentas para manipulação direta de projetos.
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path
from .base import Tool, ToolResult


class MultiEditTool(Tool):
    """Ferramenta para múltiplas edições em sequência."""
    
    @property
    def name(self) -> str:
        return "multi_edit"
    
    @property
    def description(self) -> str:
        return "Realiza múltiplas edições em diferentes arquivos em sequência"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "edits": {
                    "type": "array",
                    "description": "Lista de edições a serem realizadas",
                    "items": {
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Caminho do arquivo"},
                            "old_text": {"type": "string", "description": "Texto a ser substituído"},
                            "new_text": {"type": "string", "description": "Novo texto"}
                        },
                        "required": ["file_path", "old_text", "new_text"]
                    }
                }
            },
            "required": ["edits"]
        }
    
    def execute(self, edits: List[Dict[str, str]]) -> ToolResult:
        results = []
        successful_edits = []
        
        for i, edit in enumerate(edits):
            file_path = edit["file_path"]
            old_text = edit["old_text"]
            new_text = edit["new_text"]
            
            try:
                if not os.path.exists(file_path):
                    results.append(f" Arquivo {file_path} não encontrado")
                    continue
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if old_text not in content:
                    results.append(f"  Texto não encontrado em {file_path}")
                    continue
                
                new_content = content.replace(old_text, new_text)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                results.append(f" {file_path} editado")
                successful_edits.append({
                    "file": file_path,
                    "replacements": content.count(old_text)
                })
            
            except Exception as e:
                results.append(f" Erro em {file_path}: {str(e)}")
        
        return ToolResult(
            success=len(successful_edits) > 0,
            content="\n".join(results),
            metadata={
                "total_edits": len(edits),
                "successful_edits": len(successful_edits),
                "details": successful_edits
            }
        )


class CreateProjectTool(Tool):
    """Ferramenta para criar estrutura de projetos."""
    
    @property
    def name(self) -> str:
        return "create_project"
    
    @property
    def description(self) -> str:
        return "Cria estrutura completa de projeto com múltiplos arquivos"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "Nome do projeto"},
                "project_type": {"type": "string", "description": "Tipo de projeto (python, nodejs, etc.)"},
                "files": {
                    "type": "array",
                    "description": "Arquivos a serem criados",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Caminho do arquivo"},
                            "content": {"type": "string", "description": "Conteúdo do arquivo"}
                        },
                        "required": ["path", "content"]
                    }
                }
            },
            "required": ["project_name", "files"]
        }
    
    def execute(self, project_name: str, files: List[Dict[str, str]], 
                project_type: str = "python") -> ToolResult:
        
        results = []
        created_files = []
        
        # Criar diretório do projeto
        project_path = Path(project_name)
        try:
            project_path.mkdir(exist_ok=True)
            results.append(f" Projeto '{project_name}' criado")
        except Exception as e:
            return ToolResult(
                success=False,
                content=f"Erro ao criar diretório do projeto: {e}",
                error=str(e)
            )
        
        # Criar arquivos
        for file_info in files:
            file_path = project_path / file_info["path"]
            content = file_info["content"]
            
            try:
                # Criar diretórios pais se necessário
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                results.append(f" {file_info['path']} criado")
                created_files.append(str(file_path))
                
            except Exception as e:
                results.append(f" Erro ao criar {file_info['path']}: {e}")
        
        return ToolResult(
            success=len(created_files) > 0,
            content="\n".join(results),
            metadata={
                "project_name": project_name,
                "project_type": project_type,
                "files_created": len(created_files),
                "files": created_files
            }
        )


class RefactorTool(Tool):
    """Ferramenta para refatoração de código."""
    
    @property
    def name(self) -> str:
        return "refactor"
    
    @property
    def description(self) -> str:
        return "Refatora código realizando múltiplas operações (renomear, mover, etc.)"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "operations": {
                    "type": "array",
                    "description": "Operações de refatoração",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "description": "Tipo: rename, move, extract"},
                            "file_path": {"type": "string", "description": "Arquivo alvo"},
                            "old_name": {"type": "string", "description": "Nome antigo"},
                            "new_name": {"type": "string", "description": "Nome novo"}
                        },
                        "required": ["type", "file_path"]
                    }
                }
            },
            "required": ["operations"]
        }
    
    def execute(self, operations: List[Dict[str, str]]) -> ToolResult:
        results = []
        successful_ops = 0
        
        for op in operations:
            op_type = op["type"]
            file_path = op["file_path"]
            
            try:
                if op_type == "rename" and "old_name" in op and "new_name" in op:
                    result = self._rename_in_file(file_path, op["old_name"], op["new_name"])
                    results.append(result)
                    if "" in result:
                        successful_ops += 1
                        
                elif op_type == "move":
                    # Implementar movimentação de arquivos
                    results.append(f"  Operação 'move' não implementada ainda")
                    
                else:
                    results.append(f"  Operação '{op_type}' desconhecida")
                    
            except Exception as e:
                results.append(f" Erro na operação {op_type}: {e}")
        
        return ToolResult(
            success=successful_ops > 0,
            content="\n".join(results),
            metadata={
                "total_operations": len(operations),
                "successful_operations": successful_ops
            }
        )
    
    def _rename_in_file(self, file_path: str, old_name: str, new_name: str) -> str:
        """Renomeia variável/função em arquivo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Busca por padrões de código (função, variável, classe)
            import re
            patterns = [
                rf'\bdef {re.escape(old_name)}\b',  # função
                rf'\bclass {re.escape(old_name)}\b',  # classe
                rf'\b{re.escape(old_name)}\s*=',  # variável
                rf'\b{re.escape(old_name)}\b',  # uso geral
            ]
            
            replacements = 0
            new_content = content
            
            for pattern in patterns:
                matches = re.findall(pattern, new_content)
                if matches:
                    new_content = re.sub(pattern, lambda m: m.group().replace(old_name, new_name), new_content)
                    replacements += len(matches)
            
            if replacements > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return f" {file_path}: {old_name} → {new_name} ({replacements} alterações)"
            else:
                return f"  {file_path}: '{old_name}' não encontrado"
                
        except Exception as e:
            return f" {file_path}: Erro - {e}"


class BackupTool(Tool):
    """Ferramenta para criar backups antes de modificações."""
    
    @property
    def name(self) -> str:
        return "backup"
    
    @property
    def description(self) -> str:
        return "Cria backup de arquivos antes de modificações"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "files": {
                    "type": "array",
                    "description": "Arquivos para backup",
                    "items": {"type": "string"}
                },
                "backup_dir": {
                    "type": "string", 
                    "description": "Diretório para backups",
                    "default": ".backups"
                }
            },
            "required": ["files"]
        }
    
    def execute(self, files: List[str] = None, backup_dir: str = ".backups") -> ToolResult:
        if not files:
            return ToolResult(
                success=False,
                content=None,
                error="Parâmetro 'files' é obrigatório"
            )
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(backup_dir) / timestamp
        
        try:
            backup_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return ToolResult(
                success=False,
                content=f"Erro ao criar diretório de backup: {e}",
                error=str(e)
            )
        
        backed_up = []
        results = []
        
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    src = Path(file_path)
                    dst = backup_path / src.name
                    shutil.copy2(src, dst)
                    backed_up.append(file_path)
                    results.append(f" {file_path} → {dst}")
                else:
                    results.append(f"  {file_path} não encontrado")
                    
            except Exception as e:
                results.append(f" Erro ao fazer backup de {file_path}: {e}")
        
        return ToolResult(
            success=len(backed_up) > 0,
            content="\n".join(results),
            metadata={
                "backup_dir": str(backup_path),
                "files_backed_up": len(backed_up),
                "timestamp": timestamp
            }
        )