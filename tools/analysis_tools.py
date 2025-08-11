"""
Ferramentas para análise de código.
"""

import os
import ast
from typing import Dict, Any, List
from .base import Tool, ToolResult


class AnalyzeTool(Tool):
    """Ferramenta para análise de código Python."""
    
    @property
    def name(self) -> str:
        return "analyze"
    
    @property
    def description(self) -> str:
        return "Analisa código Python para extrair informações estruturais"
    
    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Caminho do arquivo Python a ser analisado"
                },
                "include_docstrings": {
                    "type": "boolean",
                    "description": "Incluir docstrings na análise",
                    "default": True
                }
            },
            "required": ["file_path"]
        }
    
    def execute(self, file_path: str = None, files: List[str] = None, include_docstrings: bool = True) -> ToolResult:
        # Compatibilidade: aceitar tanto 'files' quanto 'file_path'
        if files and not file_path:
            file_path = files[0] if files else None
        
        if not file_path:
            return ToolResult(
                success=False,
                content=None,
                error="Parâmetro 'file_path' é obrigatório"
            )
        try:
            if not os.path.exists(file_path):
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Arquivo '{file_path}' não encontrado"
                )
            
            if not file_path.endswith('.py'):
                return ToolResult(
                    success=False,
                    content=None,
                    error="Esta ferramenta só analisa arquivos Python (.py)"
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            try:
                tree = ast.parse(source_code)
            except SyntaxError as e:
                return ToolResult(
                    success=False,
                    content=None,
                    error=f"Erro de sintaxe no arquivo: {str(e)}"
                )
            
            analysis = {
                "file_path": file_path,
                "classes": [],
                "functions": [],
                "imports": [],
                "variables": [],
                "constants": []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_info = {
                        "name": node.name,
                        "line": node.lineno,
                        "bases": [self._get_name(base) for base in node.bases],
                        "methods": []
                    }
                    
                    if include_docstrings and ast.get_docstring(node):
                        class_info["docstring"] = ast.get_docstring(node)
                    
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                "name": item.name,
                                "line": item.lineno,
                                "args": [arg.arg for arg in item.args.args]
                            }
                            if include_docstrings and ast.get_docstring(item):
                                method_info["docstring"] = ast.get_docstring(item)
                            class_info["methods"].append(method_info)
                    
                    analysis["classes"].append(class_info)
                
                elif isinstance(node, ast.FunctionDef):
                    # Só adicionar se não for método de classe
                    if not any(isinstance(parent, ast.ClassDef) 
                              for parent in ast.walk(tree) 
                              if hasattr(parent, 'body') and node in getattr(parent, 'body', [])):
                        func_info = {
                            "name": node.name,
                            "line": node.lineno,
                            "args": [arg.arg for arg in node.args.args]
                        }
                        if include_docstrings and ast.get_docstring(node):
                            func_info["docstring"] = ast.get_docstring(node)
                        analysis["functions"].append(func_info)
                
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            analysis["imports"].append({
                                "type": "import",
                                "module": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno
                            })
                    else:  # ImportFrom
                        for alias in node.names:
                            analysis["imports"].append({
                                "type": "from_import",
                                "module": node.module,
                                "name": alias.name,
                                "alias": alias.asname,
                                "line": node.lineno
                            })
                
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_info = {
                                "name": target.id,
                                "line": node.lineno
                            }
                            
                            # Detectar constantes (UPPER_CASE)
                            if target.id.isupper():
                                analysis["constants"].append(var_info)
                            else:
                                analysis["variables"].append(var_info)
            
            return ToolResult(
                success=True,
                content=analysis,
                metadata={
                    "file_path": file_path,
                    "classes_count": len(analysis["classes"]),
                    "functions_count": len(analysis["functions"]),
                    "imports_count": len(analysis["imports"])
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao analisar arquivo: {str(e)}"
            )
    
    def _get_name(self, node):
        """Extrai nome de um nó AST."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        else:
            return str(node)