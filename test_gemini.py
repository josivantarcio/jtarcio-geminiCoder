#!/usr/bin/env python3
"""
Teste rápido do Gemini Coder para verificar se tudo está funcionando.
"""

import sys
import os

# Adicionar o diretório atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tools
from core.config import Config
registry = tools.registry
from rich.console import Console

def test_tools():
    """Testa se todas as ferramentas estão carregando corretamente."""
    console = Console()
    
    console.print(" [bold blue]Testando Ferramentas do Gemini Coder[/bold blue]")
    console.print("=" * 50)
    
    tools = registry.list_tools()
    console.print(f" [green]{len(tools)} ferramentas carregadas:[/green]")
    
    for tool_name in tools:
        tool = registry.get_tool(tool_name)
        if tool:
            console.print(f"  • [cyan]{tool_name}[/cyan]: {tool.description}")
    
    console.print()
    
    # Testar execução básica
    console.print(" [bold yellow]Testando execução básica...[/bold yellow]")
    
    # Teste glob
    result = registry.execute_tool("glob", pattern="*.py")
    if result.success:
        console.print(f" [green]glob: {len(result.content)} arquivos Python encontrados[/green]")
    else:
        console.print(f" [red]glob: {result.error}[/red]")
    
    # Teste read (este arquivo)
    result = registry.execute_tool("read", file_path=__file__)
    if result.success:
        console.print(f" [green]read: {result.metadata['size']} bytes lidos[/green]")
    else:
        console.print(f" [red]read: {result.error}[/red]")
    
    console.print()
    console.print(" [bold green]Teste concluído![/bold green]")

def test_config():
    """Testa carregamento de configuração."""
    console = Console()
    
    console.print(" [bold blue]Testando Configuração[/bold blue]")
    console.print("=" * 30)
    
    try:
        config = Config.load()
        console.print(" [green]Configuração carregada[/green]")
        
        if config.gemini_api_key:
            key_preview = config.gemini_api_key[:8] + "..." + config.gemini_api_key[-4:]
            console.print(f" [green]API Key: {key_preview}[/green]")
        else:
            console.print("[yellow]API Key não configurada[/yellow]")
            console.print("   Configure com: export GEMINI_API_KEY='sua_chave'")
            console.print("   Ou: python gemini_coder.py --create-config")
        
    except Exception as e:
        console.print(f" [red]Erro na configuração: {e}[/red]")

if __name__ == "__main__":
    console = Console()
    
    console.print()
    console.print(" [bold cyan]GEMINI CODER - TESTE DE SISTEMA[/bold cyan]")
    console.print("=" * 60)
    console.print()
    
    test_config()
    console.print()
    test_tools()
    console.print()
    
    console.print(" [bold]Próximos passos:[/bold]")
    console.print("1. Configure GEMINI_API_KEY se ainda não fez")
    console.print("2. Execute: [cyan]python gemini_coder.py --interactive[/cyan]")  
    console.print("3. Ou instale globalmente: [cyan]bash setup_global.sh[/cyan]")
    console.print()
    console.print(" Documentação completa: README.md")
    console.print(" Setup global: SETUP_GLOBAL.md")
    console.print()