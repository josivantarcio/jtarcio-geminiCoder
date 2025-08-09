# Code Analyzer CLI

Ferramenta de análise e manipulação de código via linha de comando usando Google Gemini API.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/code-analyzer-cli.git
   cd code-analyzer-cli
   ```

2. Instale as dependências:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Configure sua API key no arquivo `.env`:
   ```env
   GEMINI_API_KEY="SUA_CHAVE_AQUI"
   ```

## Uso

Execute o script:
```bash
python main.py "sua solicitação aqui"
```
Exemplo:
```bash
python main.py "Crie um arquivo de teste para a função 'somar' no exemplo.py"
```

## Funcionalidades

- Análise de código e projetos
- Criação e edição de arquivos
- Sugestão e execução de comandos
- Respeita arquivos .gitignore
- Confirmação antes de qualquer alteração
- Interface de linha de comando simples

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
