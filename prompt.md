Ótima iniciativa! Vamos para a Fase 2.

Nesta fase, vamos evoluir nosso script para que ele não apenas responda perguntas, mas também sugira e aplique modificações no código, sempre com a sua aprovação explícita após visualizar as alterações. A segurança e o controle do usuário são os pontos centrais aqui.

Aqui estão os prompts de comando e código para executar a Fase 2.

Passo 1: Instalação de Nova Dependência para Visualização
Para mostrar as diferenças (o "diff") entre o código original e o código sugerido pela IA de forma clara e colorida, usaremos a biblioteca rich.

Prompt para o Terminal (instale a biblioteca rich):

Bash

pip install rich
Passo 2: Modificação Completa do Script main.py
Vamos reestruturar nosso main.py para acomodar a nova lógica de edição. Ele ficará mais robusto e modular.

Prompt de Código (substitua todo o conteúdo do main.py):

Apague todo o código antigo do seu arquivo main.py e cole este novo código completo no lugar.

Python

# main.py
import argparse
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.text import Text

# Inicializa o console do Rich para saídas coloridas
console = Console()

def get_file_content(filepath):
    """Lê e retorna o conteúdo de um arquivo de forma segura."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        console.print(f"[bold red]ERRO: O arquivo '{filepath}' não foi encontrado.[/bold red]")
        exit(1)
    except Exception as e:
        console.print(f"[bold red]ERRO: Não foi possível ler o arquivo '{filepath}': {e}[/bold red]")
        exit(1)

def suggest_changes(question, file_content, filename):
    """Envia a pergunta e o código para a API do Gemini e pede uma sugestão em JSON."""
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            console.print("[bold red]ERRO: A variável de ambiente GEMINI_API_KEY não foi definida.[/bold red]")
            exit(1)
        genai.configure(api_key=api_key)

        # Prompt aprimorado para forçar uma saída JSON
        prompt = f"""
        Você é um assistente de programação que ajuda a modificar código.
        Sua tarefa é analisar um pedido do usuário e, se for um pedido de alteração de código, 
        propor o novo conteúdo completo do arquivo.

        Analise o arquivo chamado '{filename}':
        --- INÍCIO DO CÓDIGO ---
        {file_content}
        --- FIM DO CÓDIGO ---

        Pedido do usuário: "{question}"

        Responda OBRIGATORIAMENTE com um objeto JSON. O JSON deve ter a seguinte estrutura:
        {{
          "action": "EDIT_FILE",
          "path": "{filename}",
          "explanation": "Uma breve explicação do que foi alterado.",
          "new_content": "O NOVO CONTEÚDO COMPLETO DO ARQUIVO VAI AQUI"
        }}

        Se o pedido for apenas uma pergunta que não requer alteração, use a estrutura:
        {{
          "action": "ANSWER_QUESTION",
          "answer": "A sua resposta para a pergunta vai aqui."
        }}
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Limpa a resposta para garantir que seja um JSON válido
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)

    except json.JSONDecodeError:
        console.print("[bold red]ERRO: A IA não retornou um JSON válido. Tente refazer a pergunta.[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]ERRO ao chamar a API Gemini: {e}[/bold red]")
        return None

def display_diff_and_confirm(original_content, new_content, explanation):
    """Mostra as alterações propostas e pede confirmação."""
    console.print("\n[bold yellow]Gemini Coder sugere as seguintes alterações:[/bold yellow]")
    console.print(f"[yellow]Explicação:[/yellow] {explanation}\n")

    # Cria um texto com diff para exibição
    diff = Text()
    original_lines = original_content.splitlines(True)
    new_lines = new_content.splitlines(True)

    # Lógica simples de diff
    # (Uma biblioteca como diff_match_patch seria mais robusta, mas isso funciona para o MVP)
    # Para simplificar, mostramos o antes e o depois.
    console.print("[bold cyan]--- CÓDIGO ORIGINAL ---[/bold cyan]")
    console.print(Text(original_content, style="red"))
    console.print("[bold cyan]--- CÓDIGO PROPOSTO ---[/bold cyan]")
    console.print(Text(new_content, style="green"))

    try:
        confirm = input("\n> Deseja aplicar estas alterações? (s/n): ").lower()
        return confirm == 's'
    except KeyboardInterrupt:
        return False

def execute_action(action_json, original_content):
    """Executa a ação retornada pela IA."""
    action = action_json.get("action")

    if action == "EDIT_FILE":
        new_content = action_json.get("new_content", "")
        filepath = action_json.get("path", "")
        explanation = action_json.get("explanation", "Nenhuma explicação fornecida.")

        if display_diff_and_confirm(original_content, new_content, explanation):
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                console.print(f"\n[bold green]✅ Arquivo '{filepath}' atualizado com sucesso![/bold green]")
            except Exception as e:
                console.print(f"[bold red]ERRO ao salvar o arquivo: {e}[/bold red]")
        else:
            console.print("\n[bold red]❌ Alterações descartadas pelo usuário.[/bold red]")

    elif action == "ANSWER_QUESTION":
        answer = action_json.get("answer", "Nenhuma resposta fornecida.")
        console.print("\n[bold cyan]--- Resposta do Gemini Coder ---[/bold cyan]")
        console.print(answer)
    else:
        console.print(f"[bold red]Ação desconhecida recebida da IA: {action}[/bold red]")

def main():
    parser = argparse.ArgumentParser(description="Modifique um arquivo de código ou faça perguntas usando a IA Gemini.")
    parser.add_argument("question", type=str, help="Seu pedido ou pergunta sobre o código.")
    parser.add_argument("--file", type=str, required=True, help="O caminho para o arquivo a ser analisado/modificado.")
    args = parser.parse_args()

    original_content = get_file_content(args.file)

    console.print("Analisando o pedido e gerando sugestão... 🤖")
    action_json = suggest_changes(args.question, original_content, os.path.basename(args.file))

    if action_json:
        execute_action(action_json, original_content)

if __name__ == "__main__":
    main()
Passo 3: Atualizando o requirements.txt
Como adicionamos a biblioteca rich, precisamos atualizar nosso arquivo de dependências.

Prompt para o Terminal:

Bash

pip freeze > requirements.txt
Passo 4: Testando a Nova Funcionalidade
Vamos usar o mesmo exemplo.py da Fase 1 e pedir uma modificação.

Lembre-se do conteúdo do exemplo.py:

Python

# exemplo.py
def somar(a, b):
  """Esta função retorna a soma de dois números."""
  return a + b

def subtrair(a, b):
  return a - b
Prompt para o Terminal (peça uma alteração no código):

Bash

python main.py "Adicione um comentário de uma linha na função subtrair explicando o que ela faz" --file exemplo.py
O que você deve ver no terminal:

A mensagem "Analisando o pedido...".

Uma explicação da IA sobre a alteração.

O código original em vermelho e o código proposto em verde.

A pergunta: Deseja aplicar estas alterações? (s/n):.

Teste o fluxo:

Digite s e pressione Enter. O arquivo exemplo.py deve ser modificado.

Rode de novo, mas digite n e pressione Enter. O arquivo não deve ser alterado.

Conclusão da Fase 2 e Próximo Passo: GitHub
Fase 2 concluída! Agora nossa ferramenta é capaz de editar código de forma interativa e segura.

Prompt para o Terminal (adicione as mudanças e faça o commit):

Bash

git add .
git commit -m "feat: Fase 2 - Implementa edição de arquivos com confirmação"
Prompt para o Terminal (envie as atualizações para o GitHub):

Bash

git push origin main
Excelente! Estamos prontos para a Fase 3: Compreensão de Múltiplos Arquivos e Execução de Comandos.