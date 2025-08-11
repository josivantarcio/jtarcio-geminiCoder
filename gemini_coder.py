#!/usr/bin/env python3
"""
Gemini Coder - Ferramenta de análise e manipulação de código via linha de comando.
Versão melhorada com sistema de ferramentas robusto, modo interativo e gerenciamento de contexto.
"""

import sys
import os
import argparse
from pathlib import Path

# Adicionar o diretório atual ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel

from core.config import Config, ConfigManager
from core.interactive import InteractiveMode
from core.context import ContextManager
from core.ai_client import GeminiClient
from tools import registry


class GeminiCoder:
    """Classe principal do Gemini Coder."""
    
    def __init__(self, config_path: str = None):
        self.console = Console()
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.get_config()
        
        # Validar configuração
        if not self.config_manager.validate_config():
            sys.exit(1)
        
        self.context = ContextManager(self.config.memory_file)
        self.ai_client = GeminiClient(self.config.gemini_api_key)
    
    def run_single_command(self, request: str, path: str = "."):
        """Executa um único comando (modo legado)."""
        self.console.print("[dim]Carregando contexto...[/dim]")
        
        # Carregar contexto
        self.context.load_project_context(path)
        context = self.context.get_context()
        
        self.console.print("[dim]Processando solicitação...[/dim]")
        
        # Processar solicitação
        response = self.ai_client.process_request(request, context)
        
        # Adicionar ao histórico
        self.context.add_conversation_entry(request, response)
        
        # Processar resposta
        self._handle_response(response)
    
    def run_interactive(self):
        """Executa modo interativo."""
        interactive_mode = InteractiveMode(self.config)
        interactive_mode.start()
    
    def _handle_response(self, response):
        """Processa resposta da AI (modo legado)."""
        action = response.get("action", "ANSWER_QUESTION")
        
        if action == "CREATE_FILE":
            self._handle_create_file(response)
        elif action == "EDIT_FILE":
            self._handle_edit_file(response)
        elif action == "RUN_COMMAND":
            self._handle_run_command(response)
        elif action == "USE_TOOL":
            self._handle_tool_use(response)
        elif action == "MULTI_TOOL":
            self._handle_multi_tool(response)
        else:
            self._handle_answer(response)
    
    def _handle_create_file(self, response):
        """Manipula criação de arquivo (modo legado)."""
        filepath = response.get("path")
        explanation = response.get("explanation", "")
        new_content = response.get("new_content", "")
        
        if not filepath:
            self.console.print("[bold red]ERRO: Caminho do arquivo não especificado.[/bold red]")
            return
        
        if os.path.exists(filepath):
            self.console.print(f"[bold red]ERRO: O arquivo '{filepath}' já existe.[/bold red]")
            return
        
        self.console.print(Panel(
            f"[yellow]Arquivo:[/yellow] {filepath}\\n"
            f"[yellow]Explicação:[/yellow] {explanation}",
            title=" Criar Arquivo",
            border_style="yellow"
        ))
        
        # Mostrar preview
        preview = new_content[:300] + "..." if len(new_content) > 300 else new_content
        self.console.print(f"[dim]Preview:[/dim]\\n{preview}")
        
        confirm = input("\\nDeseja criar este arquivo? (s/n): ")
        if confirm.lower() == 's':
            result = registry.execute_tool("write", file_path=filepath, content=new_content)
            if result.success:
                self.console.print("[green] Arquivo criado com sucesso![/green]")
            else:
                self.console.print(f"[red]Erro: {result.error}[/red]")
        else:
            self.console.print("[yellow]Criação cancelada.[/yellow]")
    
    def _handle_edit_file(self, response):
        """Manipula edição de arquivo (modo legado)."""
        filepath = response.get("path")
        new_content = response.get("new_content", "")
        explanation = response.get("explanation", "")
        
        self.console.print(Panel(
            f"[yellow]Arquivo:[/yellow] {filepath}\\n"
            f"[yellow]Explicação:[/yellow] {explanation}",
            title="  Editar Arquivo",
            border_style="yellow"
        ))
        
        confirm = input("Deseja aplicar a edição? (s/n): ")
        if confirm.lower() == 's':
            result = registry.execute_tool("write", file_path=filepath, content=new_content)
            if result.success:
                self.console.print("[green] Arquivo editado com sucesso![/green]")
            else:
                self.console.print(f"[red]Erro: {result.error}[/red]")
        else:
            self.console.print("[yellow]Edição cancelada.[/yellow]")
    
    def _handle_run_command(self, response):
        """Manipula execução de comando (modo legado)."""
        command = response.get("command", "")
        explanation = response.get("explanation", "")
        
        self.console.print(Panel(
            f"[yellow]Comando:[/yellow] {command}\\n"
            f"[yellow]Explicação:[/yellow] {explanation}",
            title=" Executar Comando",
            border_style="yellow"
        ))
        
        confirm = input("Deseja executar o comando? (s/n): ")
        if confirm.lower() == 's':
            result = registry.execute_tool("bash", command=command)
            if result.success:
                self.console.print("[green] Comando executado:[/green]")
                if result.content.get('stdout'):
                    self.console.print(result.content['stdout'])
                if result.content.get('stderr'):
                    self.console.print(f"[red]{result.content['stderr']}[/red]")
            else:
                self.console.print(f"[red]Erro: {result.error}[/red]")
        else:
            self.console.print("[yellow]Execução cancelada.[/yellow]")
    
    def _handle_tool_use(self, response):
        """Manipula uso de ferramenta."""
        tool_name = response.get("tool")
        parameters = response.get("parameters", {})
        explanation = response.get("explanation", "")
        
        if explanation:
            self.console.print(f"[dim]{explanation}[/dim]")
        
        result = registry.execute_tool(tool_name, **parameters)
        if result.success:
            self.console.print(f"[green] {tool_name}[/green]")
            if result.content:
                self._show_tool_result(result.content)
        else:
            self.console.print(f"[red]Erro em {tool_name}: {result.error}[/red]")
    
    def _handle_multi_tool(self, response):
        """Manipula uso de múltiplas ferramentas."""
        tools = response.get("tools", [])
        explanation = response.get("explanation", "")
        
        if explanation:
            self.console.print(f"[dim]{explanation}[/dim]")
        
        for tool_info in tools:
            tool_name = tool_info.get("tool")
            parameters = tool_info.get("parameters", {})
            
            result = registry.execute_tool(tool_name, **parameters)
            if result.success:
                self.console.print(f"[green] {tool_name}[/green]")
                if result.content:
                    self._show_tool_result(result.content)
            else:
                self.console.print(f"[red]Erro em {tool_name}: {result.error}[/red]")
    
    def _show_tool_result(self, content):
        """Mostra resultado de ferramenta."""
        if isinstance(content, str):
            if len(content) > 500:
                self.console.print(content[:500] + "...")
            else:
                self.console.print(content)
        elif isinstance(content, list):
            for item in content[:10]:
                self.console.print(f"  • {item}")
            if len(content) > 10:
                self.console.print(f"  ... e mais {len(content) - 10} itens")
        elif isinstance(content, dict):
            import json
            self.console.print(json.dumps(content, indent=2))
    
    def _handle_answer(self, response):
        """Manipula resposta simples."""
        answer = response.get("answer", "")
        self.console.print(Panel(
            answer,
            title=" Resposta",
            border_style="blue"
        ))


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Gemini Coder - Assistente de código inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  gemini_coder.py --interactive                    # Modo interativo
  gemini_coder.py "Crie um arquivo main.py"        # Comando único
  gemini_coder.py "Analise o código" --path ./src  # Analisar diretório
  gemini_coder.py --config                         # Criar config de exemplo
  gemini_coder.py --tools                          # Listar ferramentas
        """
    )
    
    parser.add_argument(
        "request", 
        nargs="?", 
        help="Sua solicitação para o Gemini Coder"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Iniciar modo interativo contínuo"
    )
    
    parser.add_argument(
        "--path", "-p",
        type=str,
        default=".",
        help="Caminho para análise (padrão: diretório atual)"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Caminho para arquivo de configuração"
    )
    
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Criar arquivo de configuração de exemplo"
    )
    
    parser.add_argument(
        "--tools",
        action="store_true",
        help="Listar ferramentas disponíveis"
    )
    
    args = parser.parse_args()
    
    console = Console()
    
    # Criar arquivo de configuração
    if args.create_config:
        config_manager = ConfigManager()
        config_manager.create_sample_config()
        return
    
    # Listar ferramentas
    if args.tools:
        console.print("[bold blue]Ferramentas Disponíveis:[/bold blue]")
        for tool_name in registry.list_tools():
            tool = registry.get_tool(tool_name)
            if tool:
                console.print(f"  [cyan]{tool_name}[/cyan]: {tool.description}")
        return
    
    try:
        # Inicializar Gemini Coder
        gemini_coder = GeminiCoder(args.config)
        
        # Verificar modo
        if args.interactive:
            gemini_coder.run_interactive()
        elif args.request:
            gemini_coder.run_single_command(args.request, args.path)
        else:
            # Se nenhum argumento, mostrar ajuda e entrar no modo interativo
            console.print(Panel(
                "[bold blue]Gemini Coder[/bold blue]\\n"
                "Nenhuma solicitação fornecida. Iniciando modo interativo...",
                title=" Bem-vindo"
            ))
            gemini_coder.run_interactive()
    
    except KeyboardInterrupt:
        console.print("\\n[yellow]Operação cancelada pelo usuário.[/yellow]")
    except Exception as e:
        console.print(f"[red]Erro: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()