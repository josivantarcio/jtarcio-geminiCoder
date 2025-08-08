import argparse
import os
import google.generativeai as genai
from dotenv import load_dotenv

def get_file_content(filepath):
    """Lê e retorna o conteúdo de um arquivo de forma segura."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{filepath}' não foi encontrado.")
        exit(1)
    except Exception as e:
        print(f"ERRO: Não foi possível ler o arquivo '{filepath}': {e}")
        exit(1)

def ask_gemini(question, file_content, filename):
    """Envia a pergunta e o conteúdo do arquivo para a API do Gemini."""
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("ERRO: A variável de ambiente GEMINI_API_KEY não foi definida.")
            exit(1)
        genai.configure(api_key=api_key)

        prompt = f"""
        Você é um assistente de programação sênior. Sua tarefa é responder a uma pergunta sobre um trecho de código.

        Analise o seguinte arquivo chamado '{filename}':
        --- INÍCIO DO CÓDIGO ---
        {file_content}
        --- FIM DO CÓDIGO ---

        Com base neste código, responda à seguinte pergunta:
        Pergunta: "{question}"
        """

        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"ERRO: Ocorreu um problema ao chamar a API do Gemini: {e}"

def main():
    """Função principal para orquestrar o script."""
    parser = argparse.ArgumentParser(
        description="Faça uma pergunta sobre um arquivo de código usando a IA Gemini."
    )
    parser.add_argument("question", type=str, help="A pergunta que você quer fazer sobre o código.")
    parser.add_argument("--file", type=str, required=True, help="O caminho para o arquivo de código a ser analisado.")

    args = parser.parse_args()

    file_content = get_file_content(args.file)

    print("Analisando o código e preparando a resposta... 🤖")
    ai_response = ask_gemini(args.question, file_content, os.path.basename(args.file))

    print("\n--- Resposta do Gemini Coder ---")
    print(ai_response)
    print("--------------------------------\n")

if __name__ == "__main__":
    main()
