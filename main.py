import argparse
import os
import json
import subprocess
import google.generativeai as genai
from dotenv import load_dotenv
from rich.console import Console
from rich.text import Text
from rich.markdown import Markdown
from gitignore_parser import parse_gitignore

def build_context_from_path(path):
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"ERRO: Não foi possível ler o arquivo '{path}': {e}"); exit(1)
    elif os.path.isdir(path):
        context_str = ""
        gitignore_path = os.path.join(path, '.gitignore')
        matches = parse_gitignore(gitignore_path) if os.path.exists(gitignore_path) else lambda x: False
        for root, _, files in os.walk(path):
            for file in files:
                filepath = os.path.join(root, file)
                if not matches(filepath):
                    try:
                        rel_path = os.path.relpath(filepath, path)
                        context_str += f"--- Início do arquivo: {rel_path} ---\n"
                        with open(filepath, 'r', encoding='utf-8') as f: context_str += f.read()
                        context_str += f"\n--- Fim do arquivo: {rel_path} ---\n\n"
                    except (IOError, UnicodeDecodeError): pass
        return context_str
    else:
        print(f"ERRO: O caminho '{path}' não é um arquivo ou diretório válido."); exit(1)

def ask_gemini(question, context, filename):
    """Envia a pergunta e o contexto para a API do Gemini."""
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("ERRO: A variável de ambiente GEMINI_API_KEY não foi definida."); exit(1)
        genai.configure(api_key=api_key)

        prompt = f"""
        Você é um sistema de análise de código. Sua tarefa é analisar um pedido do usuário, o histórico da conversa e o contexto de um projeto para propor a próxima ação.

        Analise o seguinte contexto:
        --- INÍCIO DO CONTEXTO ---
        {context}
        --- FIM DO CONTEXTO ---

        Com base neste contexto, responda à seguinte pergunta:
        Pergunta: "{question}"

        Responda OBRIGATORIAMENTE com um objeto JSON. As ações possíveis são:
        1.  `CREATE_FILE`: Se o usuário pedir para criar um novo arquivo.
            {{
                "action": "CREATE_FILE",
                "path": "caminho/sugerido/para/o/novo_arquivo.py",
                "explanation": "Explicação do porquê e para que este arquivo está sendo criado.",
                "new_content": "O CONTEÚDO COMPLETO DO NOVO ARQUIVO"
            }}
        2.  `EDIT_FILE`: Se o usuário pedir uma alteração em um arquivo específico.
            {{
                "action": "EDIT_FILE",
                "path": "caminho/do/arquivo/para/editar.py",
                "explanation": "Uma breve explicação da alteração.",
                "new_content": "O NOVO CONTEÚDO COMPLETO DO ARQUIVO"
            }}
        3.  `RUN_COMMAND`: Se o usuário pedir uma ação que requer um comando de terminal.
            {{
                "action": "RUN_COMMAND",
                "command": "o comando a ser executado",
                "explanation": "Uma breve explicação do porquê este comando é necessário."
            }}
        4.  `ANSWER_QUESTION`: Se o pedido for apenas uma pergunta.
            {{
                "action": "ANSWER_QUESTION",
                "answer": "A sua resposta para a pergunta."
            }}
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        import json
        cleaned = response.text.strip().replace('```json', '').replace('```', '')
        try:
            return json.loads(cleaned)
        except Exception:
            return {"action": "ANSWER_QUESTION", "answer": response.text}
    except Exception as e:
        return {"action": "ANSWER_QUESTION", "answer": f"ERRO: Ocorreu um problema ao chamar a API do Gemini: {e}"}

def main():
    parser = argparse.ArgumentParser(
        description="Gemini Coder: solicite ações ou perguntas sobre seu projeto."
    )
    parser.add_argument("solicitacao", nargs="?", type=str, help="Sua solicitação para o Gemini Coder.")
    parser.add_argument("--path", type=str, default=".", help="O caminho para o arquivo ou diretório a ser analisado.")
    args = parser.parse_args()

    if not args.solicitacao:
        print("Uso: python main.py [--path .] \"sua solicitação aqui\"")
        exit(2)

    context = build_context_from_path(args.path)
    print("Analisando o contexto e preparando a resposta...")
    ai_response = ask_gemini(args.solicitacao, context, os.path.basename(args.path))

    if ai_response.get("action") == "CREATE_FILE":
        filepath = ai_response.get("path")
        explanation = ai_response.get("explanation", "")
        new_content = ai_response.get("new_content", "")
        if not filepath:
            console.print("[bold red]ERRO: A IA sugeriu criar um arquivo sem um caminho.[/bold red]"); return
        if os.path.exists(filepath):
            console.print(f"[bold red]ERRO: O arquivo '{filepath}' já existe. A criação foi cancelada para evitar sobrescrever.[/bold red]"); return
        console.print(f"\n[bold yellow]Sugestão de criação de arquivo:[/bold yellow]")
        console.print(f"[yellow]Caminho do Arquivo:[/yellow] {filepath}")
        console.print(f"[yellow]Explicação:[/yellow] {explanation}\n")
        console.print(Markdown("```python\n" + new_content + "\n```"))
        confirm = input("\n> Deseja criar este arquivo? (s/n): ")
        if confirm.lower() == 's':
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            console.print(f"\n[bold green]Arquivo '{filepath}' criado com sucesso![/bold green]")
        else:
            console.print("\n[bold red]Criação de arquivo descartada.[/bold red]")
    elif ai_response.get("action") == "EDIT_FILE":
        filepath = ai_response.get("path", args.path)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_file_content = f.read()
        except Exception:
            original_file_content = ""
        new_content = ai_response.get("new_content", "")
        explanation = ai_response.get("explanation", "")
        print(f"\n--- Proposta de Edição ({filepath}) ---")
        print(f"Explicação: {explanation}")
        print("\n--- Código Original ---")
        console.print(Text(original_file_content))
        print("\n--- Código Proposto ---")
        console.print(Text(new_content))
        confirm = input("\nDeseja aplicar a alteração? (s/n): ")
        if confirm.lower() == 's':
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"\nArquivo '{filepath}' atualizado!")
        else:
            print("\nAlteração descartada.")
    elif ai_response.get("action") == "RUN_COMMAND":
        command = ai_response.get("command", "")
        explanation = ai_response.get("explanation", "")
        print(f"\n--- Proposta de Comando ---")
        print(f"Explicação: {explanation}")
        print(f"Comando: {command}")
        confirm = input("\nDeseja executar o comando? (s/n): ")
        if confirm.lower() == 's':
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"\nComando executado!")
            except Exception as e:
                print(f"\nErro ao executar comando: {e}")
        else:
            print("\nExecução descartada.")
    else:
        print("\n--- Resposta do Gemini Coder ---")
        print(ai_response.get("answer", ""))
        print("--------------------------------\n")

if __name__ == "__main__":
    main()
