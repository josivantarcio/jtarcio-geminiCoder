"""
Modo interativo contínuo para o Gemini Coder.
"""

import os
import json
import readline
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import registry
from core.context import ContextManager
from core.ai_client import GeminiClient
from core.config import Config


class InteractiveMode:
    """Modo interativo contínuo."""
    
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.context = ContextManager()
        self.ai_client = GeminiClient(config.gemini_api_key)
        self.running = True
        self.history: List[Dict[str, Any]] = []
        
        # Configurar readline para histórico
        self._setup_readline()
    
    def _setup_readline(self):
        """Configura readline para histórico de comandos."""
        try:
            history_file = os.path.expanduser("~/.gemini_coder_history")
            if os.path.exists(history_file):
                readline.read_history_file(history_file)
            readline.set_history_length(1000)
            
            # Salvar histórico ao sair
            import atexit
            atexit.register(readline.write_history_file, history_file)
        except ImportError:
            pass  # readline não disponível em alguns sistemas
    
    def start(self):
        """Inicia o modo interativo."""
        self.console.print(Panel(
            "[bold blue]Gemini Coder - Modo Interativo[/bold blue]\n"
            "Digite 'help' para ver comandos disponíveis\n"
            "Digite 'exit' ou Ctrl+C para sair",
            title=" Bem-vindo",
            border_style="blue"
        ))
        
        # Carregar contexto inicial
        self.context.load_project_context(".")
        
        while self.running:
            try:
                user_input = Prompt.ask(
                    "[bold green]gemini>[/bold green]",
                    console=self.console
                ).strip()
                
                if not user_input:
                    continue
                
                # Processar comandos especiais
                if self._handle_special_commands(user_input):
                    continue
                
                # Processar solicitação normal
                self._process_request(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use 'exit' para sair ou continue digitando...[/yellow]")
            except EOFError:
                break
        
        self.console.print("[blue]Até logo! [/blue]")
    
    def _handle_special_commands(self, command: str) -> bool:
        """Processa comandos especiais. Retorna True se foi um comando especial."""
        command = command.lower()
        
        if command in ['exit', 'quit', 'bye']:
            self.running = False
            return True
        
        elif command == 'help':
            self._show_help()
            return True
        
        elif command == 'tools':
            self._show_tools()
            return True
        
        elif command == 'context':
            self._show_context()
            return True
        
        elif command == 'history':
            self._show_history()
            return True
        
        elif command.startswith('clear'):
            if 'history' in command:
                self.history.clear()
                self.console.print("[green]Histórico limpo![/green]")
            else:
                os.system('clear' if os.name == 'posix' else 'cls')
            return True
        
        elif command.startswith('load'):
            parts = command.split()
            if len(parts) > 1:
                self._load_context(parts[1])
            else:
                self.console.print("[red]Uso: load <caminho>[/red]")
            return True
        
        return False
    
    def _show_help(self):
        """Mostra ajuda."""
        help_table = Table(title="Comandos Disponíveis")
        help_table.add_column("Comando", style="cyan")
        help_table.add_column("Descrição", style="white")
        
        commands = [
            ("help", "Mostra esta ajuda"),
            ("tools", "Lista ferramentas disponíveis"),
            ("context", "Mostra contexto atual"),
            ("history", "Mostra histórico de conversas"),
            ("load <caminho>", "Carrega contexto de um caminho"),
            ("clear", "Limpa a tela"),
            ("clear history", "Limpa o histórico"),
            ("exit/quit/bye", "Sai do modo interativo")
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        self.console.print(help_table)
        
        self.console.print("\n[bold]Exemplos de uso:[/bold]")
        self.console.print("• Criar um arquivo: 'Crie um arquivo main.py com uma função hello world'")
        self.console.print("• Analisar código: 'Analise o arquivo exemplo.py'")
        self.console.print("• Buscar texto: 'Procure por todas as funções def no projeto'")
        self.console.print("• Executar comando: 'Execute pytest para rodar os testes'")
    
    def _show_tools(self):
        """Mostra ferramentas disponíveis."""
        tools_table = Table(title="Ferramentas Disponíveis")
        tools_table.add_column("Nome", style="cyan")
        tools_table.add_column("Descrição", style="white")
        
        for tool_name in registry.list_tools():
            tool = registry.get_tool(tool_name)
            if tool:
                tools_table.add_row(tool_name, tool.description)
        
        self.console.print(tools_table)
    
    def _show_context(self):
        """Mostra contexto atual."""
        context_info = self.context.get_context_info()
        
        context_table = Table(title="Contexto Atual")
        context_table.add_column("Propriedade", style="cyan")
        context_table.add_column("Valor", style="white")
        
        for key, value in context_info.items():
            if isinstance(value, (list, dict)):
                value = json.dumps(value, indent=2)[:100] + "..." if len(str(value)) > 100 else json.dumps(value, indent=2)
            context_table.add_row(key, str(value))
        
        self.console.print(context_table)
    
    def _show_history(self):
        """Mostra histórico de conversas."""
        if not self.history:
            self.console.print("[yellow]Nenhum histórico disponível[/yellow]")
            return
        
        for i, entry in enumerate(self.history[-5:], 1):  # Últimas 5 entradas
            self.console.print(f"\n[bold blue]#{i}[/bold blue]")
            self.console.print(f"[green]User:[/green] {entry['request']}")
            self.console.print(f"[cyan]AI:[/cyan] {entry['response'].get('explanation', 'N/A')}")
    
    def _load_context(self, path: str):
        """Carrega contexto de um caminho."""
        try:
            self.context.load_project_context(path)
            self.console.print(f"[green]Contexto carregado de: {path}[/green]")
        except Exception as e:
            self.console.print(f"[red]Erro ao carregar contexto: {e}[/red]")
    
    def _process_request(self, request: str):
        """Processa uma solicitação do usuário."""
        self.console.print("[dim]Processando...[/dim]")
        
        try:
            # Obter contexto atual
            context = self.context.get_context()
            
            # Chamar AI
            response = self.ai_client.process_request(request, context)
            
            # Adicionar ao histórico
            self.history.append({
                'request': request,
                'response': response,
                'timestamp': self.context.get_current_timestamp()
            })
            
            # Processar resposta
            self._handle_ai_response(response)
            
        except Exception as e:
            self.console.print(f"[red]Erro ao processar solicitação: {e}[/red]")
    
    def _handle_ai_response(self, response: Dict[str, Any]):
        """Processa a resposta da AI."""
        action = response.get("action", "ANSWER_QUESTION")
        
        if action == "USE_TOOL":
            self._execute_tool_action(response)
        elif action == "MULTI_TOOL":
            self._execute_multi_tool_action(response)
        elif action == "CREATE_FILE":
            self._handle_create_file(response)
        elif action == "EDIT_FILE":
            self._handle_edit_file(response)
        elif action == "RUN_COMMAND":
            self._handle_run_command(response)
        else:  # ANSWER_QUESTION
            self._show_answer(response)
    
    def _execute_tool_action(self, response: Dict[str, Any]):
        """Executa uma ação de ferramenta."""
        tool_name = response.get("tool")
        tool_params = response.get("parameters", {})
        explanation = response.get("explanation", "")
        
        if explanation:
            self.console.print(f"[yellow]{explanation}[/yellow]")
        
        # Executar ferramenta
        result = registry.execute_tool(tool_name, **tool_params)
        
        if result.success:
            self._show_tool_result(tool_name, result)
        else:
            self.console.print(f"[red]Erro na ferramenta {tool_name}: {result.error}[/red]")
    
    def _execute_multi_tool_action(self, response: Dict[str, Any]):
        """Executa múltiplas ferramentas."""
        tools = response.get("tools", [])
        explanation = response.get("explanation", "")
        
        if explanation:
            self.console.print(f"[yellow]{explanation}[/yellow]")
        
        for tool_info in tools:
            tool_name = tool_info.get("tool")
            tool_params = tool_info.get("parameters", {})
            
            self.console.print(f"\n[dim]Executando {tool_name}...[/dim]")
            result = registry.execute_tool(tool_name, **tool_params)
            
            if result.success:
                self._show_tool_result(tool_name, result)
            else:
                self.console.print(f"[red]Erro na ferramenta {tool_name}: {result.error}[/red]")
    
    def _show_tool_result(self, tool_name: str, result):
        """Mostra resultado de uma ferramenta."""
        self.console.print(f"\n[bold green] {tool_name}[/bold green]")
        
        if isinstance(result.content, str):
            if len(result.content) > 500:
                self.console.print(Text(result.content[:500] + "..."))
            else:
                self.console.print(Text(result.content))
        elif isinstance(result.content, list):
            for item in result.content[:10]:  # Mostrar até 10 itens
                self.console.print(f"  • {item}")
            if len(result.content) > 10:
                self.console.print(f"  ... e mais {len(result.content) - 10} itens")
        elif isinstance(result.content, dict):
            self.console.print(json.dumps(result.content, indent=2))
    
    def _handle_create_file(self, response: Dict[str, Any]):
        """Manipula criação de arquivo."""
        filepath = response.get("path")
        content = response.get("new_content", "")
        explanation = response.get("explanation", "")
        
        self.console.print(Panel(
            f"[yellow]Arquivo:[/yellow] {filepath}\n"
            f"[yellow]Explicação:[/yellow] {explanation}",
            title=" Criar Arquivo",
            border_style="yellow"
        ))
        
        # Mostrar preview do código
        if content:
            self.console.print(Markdown(f"```python\n{content[:300]}{'...' if len(content) > 300 else ''}\n```"))
        
        if Prompt.ask("Criar arquivo?", choices=['s', 'n'], default='s') == 's':
            result = registry.execute_tool("write", file_path=filepath, content=content)
            if result.success:
                self.console.print("[green] Arquivo criado com sucesso![/green]")
            else:
                self.console.print(f"[red]Erro: {result.error}[/red]")
    
    def _handle_edit_file(self, response: Dict[str, Any]):
        """Manipula edição de arquivo."""
        filepath = response.get("path")
        new_content = response.get("new_content", "")
        explanation = response.get("explanation", "")
        
        self.console.print(Panel(
            f"[yellow]Arquivo:[/yellow] {filepath}\n"
            f"[yellow]Explicação:[/yellow] {explanation}",
            title="  Editar Arquivo",
            border_style="yellow"
        ))
        
        if Prompt.ask("Aplicar edição?", choices=['s', 'n'], default='s') == 's':
            result = registry.execute_tool("write", file_path=filepath, content=new_content)
            if result.success:
                self.console.print("[green] Arquivo editado com sucesso![/green]")
            else:
                self.console.print(f"[red]Erro: {result.error}[/red]")
    
    def _handle_run_command(self, response: Dict[str, Any]):
        """Manipula execução de comando."""
        command = response.get("command", "")
        explanation = response.get("explanation", "")
        
        self.console.print(Panel(
            f"[yellow]Comando:[/yellow] {command}\n"
            f"[yellow]Explicação:[/yellow] {explanation}",
            title=" Executar Comando",
            border_style="yellow"
        ))
        
        if Prompt.ask("Executar comando?", choices=['s', 'n'], default='s') == 's':
            result = registry.execute_tool("bash", command=command)
            if result.success:
                self.console.print("[green] Comando executado:[/green]")
                if result.content.get('stdout'):
                    self.console.print(Text(result.content['stdout']))
                if result.content.get('stderr'):
                    self.console.print(f"[red]{result.content['stderr']}[/red]")
            else:
                self.console.print(f"[red]Erro: {result.error}[/red]")
    
    def _show_answer(self, response: Dict[str, Any]):
        """Mostra resposta simples."""
        answer = response.get("answer", "")
        if answer:
            self.console.print(Panel(
                Markdown(answer),
                title=" Resposta",
                border_style="blue"
            ))