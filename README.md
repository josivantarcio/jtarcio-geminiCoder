# Gemini Coder

Assistente de programação via linha de comando usando Google Gemini.

## Instalação

1. Instale o Python 3:
   ```bash
   sudo apt update && sudo apt install -y python3 python-is-python3
   ```
2. Instale as dependências:
   ```bash
   pip3 install --user --break-system-packages google-generativeai python-dotenv rich gitignore_parser
   ```
3. Configure o alias global (adicione ao final do seu `~/.bashrc`):
   ```bash
   echo 'alias gemini="python3 /home/josivan/ws/gemini-coder/main.py --path /home/josivan/ws/gemini-coder"' >> ~/.bashrc && source ~/.bashrc
   ```
4. Adicione sua chave Gemini API ao arquivo `.env`:
   ```env
   GEMINI_API_KEY="SUA_CHAVE_AQUI"
   ```

## Uso

De qualquer pasta do terminal:
```bash
gemini "sua pergunta ou solicitação aqui"
```
Exemplo:
```bash
gemini "Crie um arquivo de teste para a função 'somar' no exemplo.py"
```

## Funcionalidades
- Perguntas sobre código
- Criação e edição de arquivos
- Sugestão e execução de comandos
- Respeita .gitignore
- Confirmação antes de qualquer alteração

## Repositório
https://github.com/josivantarcio/jtarcio-geminiCoder.git
