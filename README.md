# Gemini Coder

**Assistente de código inteligente** inspirado no Claude Code, mas usando Google Gemini API.

Uma ferramenta poderosa de análise e manipulação de código via linha de comando com sistema de ferramentas robusto, modo interativo contínuo e gerenciamento de contexto avançado.

## Características Principais

- **Sistema de Ferramentas Robusto**: 10+ ferramentas especializadas (read, write, edit, glob, grep, bash, git, etc.)
- **Modo Interativo Contínuo**: Interface rica com histórico e comandos especiais
- **Gerenciamento de Contexto/Memória**: Contexto persistente e análise de projetos
- **Sistema de Configuração**: Configuração flexível via arquivo ou variáveis de ambiente
- **Interface Rica**: Powered by Rich e Textual
- **Logging e Debugging**: Sistema de logs avançado com rotação
- **Análise de Código**: Parser AST para análise estrutural de Python
- **Detecção de Projetos**: Auto-detecta tipo de projeto (Python, Node.js, Java, etc.)

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/gemini-coder.git
   cd gemini-coder
   ```

2. **Instale as dependências:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Configure sua API key:**
   
   **Opção 1: Variável de ambiente**
   ```bash
   export GEMINI_API_KEY="sua_api_key_aqui"
   ```
   
   **Opção 2: Arquivo de configuração**
   ```bash
   python gemini_coder.py --create-config
   # Edite o arquivo .gemini_config.json criado
   ```

## Uso

### Modo Interativo (Recomendado)
```bash
python gemini_coder.py --interactive
```

### Comando Único
```bash
python gemini_coder.py "Crie um arquivo main.py com uma função hello world"
python gemini_coder.py "Analise o código do projeto" --path ./src
python gemini_coder.py "Procure por todas as funções def no projeto"
```

### Outras Opções
```bash
# Listar ferramentas disponíveis
python gemini_coder.py --tools

# Criar configuração de exemplo
python gemini_coder.py --create-config

# Usar arquivo de configuração específico
python gemini_coder.py --config custom_config.json --interactive
```

## Ferramentas Disponíveis

| Ferramenta | Descrição |
|------------|-----------|
| `read` | Lê conteúdo de arquivos |
| `write` | Escreve/cria arquivos |
| `edit` | Edita arquivos existentes |
| `glob` | Busca arquivos por padrão |
| `grep` | Busca texto/regex em arquivos |
| `bash` | Executa comandos shell |
| `git_status` | Mostra status do Git |
| `git_diff` | Mostra diferenças do Git |
| `git_commit` | Faz commits no Git |
| `analyze` | Analisa código Python (AST) |

## Modo Interativo - Comandos Especiais

No modo interativo, você pode usar comandos especiais:

```bash
gemini> help              # Mostra ajuda
gemini> tools             # Lista ferramentas
gemini> context           # Mostra contexto atual  
gemini> history           # Mostra histórico
gemini> load /path        # Carrega contexto de caminho
gemini> clear             # Limpa tela
gemini> clear history     # Limpa histórico
gemini> exit              # Sai do programa
```

## Configuração

### Arquivo de Configuração (.gemini_config.json)
```json
{
  "gemini_api_key": "sua_chave_aqui",
  "gemini_model": "gemini-1.5-flash",
  "use_rich_interface": true,
  "auto_confirm": false,
  "memory_file": ".gemini_memory.json",
  "max_history_entries": 100,
  "enable_dangerous_commands": false,
  "command_timeout": 30
}
```

### Variáveis de Ambiente
- `GEMINI_API_KEY`: Chave da API do Gemini
- `GEMINI_MODEL`: Modelo a usar (padrão: gemini-1.5-flash)
- `GEMINI_DEBUG`: Habilitar debug (true/false)
- `GEMINI_AUTO_CONFIRM`: Confirmar automaticamente (true/false)

## Contexto e Memória

O Gemini Coder mantém contexto inteligente:

- **Análise de Projeto**: Detecta tipo de projeto, estrutura de arquivos
- **Informações Git**: Branch atual, status, últimos commits
- **Histórico Persistente**: Conversas são salvas em `.gemini_memory.json`
- **Cache de Arquivos**: Arquivos importantes ficam em cache
- **Contexto Automático**: Carrega contexto relevante automaticamente

## Debugging

Habilite debug para diagnósticos avançados:

```bash
export GEMINI_DEBUG=true
python gemini_coder.py --interactive
```

Isso cria:
- Logs detalhados em `/logs/`
- Snapshots de debug em `/debug/`
- Métricas de performance
- Rastreamento de erros

## Exemplos de Uso

### Análise de Código
```bash
gemini> Analise o arquivo main.py e sugira melhorias
```

### Criação de Arquivos
```bash
gemini> Crie um arquivo de teste para a classe User com pytest
```

### Busca e Refatoração
```bash
gemini> Encontre todas as funções que usam print() e substitua por logging
```

### Operações Git
```bash
gemini> Faça commit das mudanças com mensagem apropriada
```

### Análise de Projeto
```bash
gemini> Analise a estrutura do projeto e crie um README detalhado
```

## Migração do Projeto Antigo

Se você tem o `main.py` antigo, o novo `gemini_coder.py` é totalmente compatível:

```bash
# Antigo
python main.py "solicitação"

# Novo (equivalente)
python gemini_coder.py "solicitação"
```

## Comparação com Claude Code

| Funcionalidade | Claude Code | Gemini Coder |
|----------------|-------------|--------------|
| Sistema de Ferramentas | Sim | Sim |
| Modo Interativo | Sim | Sim |
| Gerenciamento de Contexto | Sim | Sim |
| Interface Rica | Sim | Sim |
| Debugging Avançado | Sim | Sim |
| Open Source | Não | Sim |
| API Gratuita | Não | Sim (Gemini) |

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contribuição

Contribuições são muito bem-vindas! 

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Áreas para Contribuição
- Novas ferramentas especializadas
- Melhorias na interface
- Suporte a mais linguagens de programação
- Otimizações de performance
- Documentação e exemplos

## Reportar Issues

Encontrou um bug ou tem uma sugestão? [Abra uma issue](https://github.com/seu-usuario/gemini-coder/issues)

---

**Se você gostou do projeto, não esqueça de dar uma estrela!**
