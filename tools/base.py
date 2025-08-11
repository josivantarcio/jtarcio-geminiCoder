"""
Classes base para o sistema de ferramentas.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ToolResult:
    """Resultado da execução de uma ferramenta."""
    success: bool
    content: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Tool(ABC):
    """Classe base para todas as ferramentas."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome da ferramenta."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição da ferramenta."""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """Schema dos parâmetros da ferramenta."""
        pass
    
    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Executa a ferramenta com os parâmetros fornecidos."""
        pass
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a ferramenta para dicionário (para serialização)."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }


class ToolRegistry:
    """Registro central de ferramentas disponíveis."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Registra uma nova ferramenta."""
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Obtém uma ferramenta pelo nome."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """Lista nomes de todas as ferramentas registradas."""
        return list(self._tools.keys())
    
    def get_tools_description(self) -> List[Dict[str, Any]]:
        """Obtém descrição de todas as ferramentas para o AI."""
        return [tool.to_dict() for tool in self._tools.values()]
    
    def execute_tool(self, name: str, **kwargs) -> ToolResult:
        """Executa uma ferramenta pelo nome."""
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(
                success=False,
                content=None,
                error=f"Ferramenta '{name}' não encontrada"
            )
        
        try:
            return tool.execute(**kwargs)
        except Exception as e:
            return ToolResult(
                success=False,
                content=None,
                error=f"Erro ao executar ferramenta '{name}': {str(e)}"
            )