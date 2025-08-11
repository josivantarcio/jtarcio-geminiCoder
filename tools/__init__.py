"""
Sistema de ferramentas para o Gemini Coder.
Inspirado no sistema de tools do Claude Code.
"""

from .base import Tool, ToolRegistry
from .file_tools import ReadTool, WriteTool, EditTool, GlobTool
from .shell_tools import BashTool
from .git_tools import GitStatusTool, GitDiffTool, GitCommitTool
from .search_tools import GrepTool
from .analysis_tools import AnalyzeTool
from .project_tools import MultiEditTool, CreateProjectTool, RefactorTool, BackupTool

# Registro global de ferramentas
registry = ToolRegistry()

# Registrar ferramentas padrão
registry.register(ReadTool())
registry.register(WriteTool())
registry.register(EditTool())
registry.register(GlobTool())
registry.register(BashTool())
registry.register(GitStatusTool())
registry.register(GitDiffTool())
registry.register(GitCommitTool())
registry.register(GrepTool())
registry.register(AnalyzeTool())

# Registrar ferramentas avançadas
registry.register(MultiEditTool())
registry.register(CreateProjectTool())
registry.register(RefactorTool())
registry.register(BackupTool())

__all__ = [
    'Tool', 'ToolRegistry', 'registry',
    'ReadTool', 'WriteTool', 'EditTool', 'GlobTool',
    'BashTool', 'GitStatusTool', 'GitDiffTool', 'GitCommitTool',
    'GrepTool', 'AnalyzeTool',
    'MultiEditTool', 'CreateProjectTool', 'RefactorTool', 'BackupTool'
]