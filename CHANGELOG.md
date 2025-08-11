# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

## [2.0.0] - 2025-01-11 - MAJOR REWRITE 

###  Novas Funcionalidades
- **Sistema de Ferramentas Robusto**: 10+ ferramentas especializadas (read, write, edit, glob, grep, bash, git, analyze)
- **Modo Interativo Contínuo**: Interface rica com Rich, comandos especiais e histórico
- **Gerenciamento de Contexto/Memória**: Contexto persistente e análise inteligente de projetos
- **Sistema de Configuração**: Configuração flexível via JSON ou variáveis de ambiente
- **Logging e Debugging**: Sistema de logs com rotação e debugging avançado
- **Análise de Código**: Parser AST para análise estrutural de código Python
- **Detecção de Projetos**: Auto-detecta Python, Node.js, Java, Rust, Go, etc.
- **Interface Rica**: Powered by Rich com panels, tabelas e syntax highlighting

###  Ferramentas Implementadas
- `read`: Lê arquivos com validação de tamanho
- `write`: Cria/sobrescreve arquivos com criação de diretórios
- `edit`: Edita arquivos com busca e substituição
- `glob`: Busca arquivos por padrão com suporte recursivo
- `grep`: Busca texto/regex em arquivos (ripgrep quando disponível)
- `bash`: Executa comandos shell com timeout e validação
- `git_status`: Status do repositório Git
- `git_diff`: Diferenças do Git (staged/unstaged)
- `git_commit`: Commits automáticos
- `analyze`: Análise AST de código Python

###  Modo Interativo
- Comandos especiais: `help`, `tools`, `context`, `history`, `load`, `clear`, `exit`
- Histórico persistente com readline
- Preview de código com syntax highlighting
- Confirmações interativas para operações destrutivas

###  Contexto e Memória
- Análise automática de estrutura de projeto
- Detecção de tipo de projeto
- Informações Git (branch, status, commits)
- Cache de arquivos importantes
- Histórico de conversas persistente
- Context-aware para melhores respostas

### Configuração
- Arquivo `.gemini_config.json` com todas as opções
- Suporte a variáveis de ambiente
- Configuração de timeouts, limites e comportamentos
- Validação de configuração com mensagens de erro claras

###  Debugging e Logs
- Sistema de logs com rotação automática
- Debug mode com `GEMINI_DEBUG=true`
- Snapshots de debug para diagnósticos
- Métricas de performance
- Rastreamento de erros detalhado

###  Melhorias na AI
- Prompt system redesenhado para usar ferramentas
- Suporte a múltiplas ferramentas em sequência
- Better context awareness
- Improved error handling

###  Arquitetura
- Código completamente reestruturado em módulos
- Separação clara entre core, tools, utils
- Design patterns aplicados (Registry, Manager, etc.)
- Extensibilidade para novas ferramentas
- Type hints em todo o código

###  Documentação
- README completamente reescrito
- Documentação detalhada de todas as funcionalidades
- Exemplos de uso práticos
- Guia de configuração e troubleshooting
- Changelog detalhado

## [1.0.0] - 2024-XX-XX - Versão Original

### Funcionalidades Básicas
- Script simples `main.py`
- 4 ações básicas: CREATE_FILE, EDIT_FILE, RUN_COMMAND, ANSWER_QUESTION
- Integração com Google Gemini API
- Respeito ao .gitignore
- Confirmação antes de alterações

### Limitações da Versão Original
- Sem modo interativo
- Sem gerenciamento de contexto
- Sem sistema de ferramentas
- Sem logging
- Interface simples
- Sem configuração flexível

---

## Tipos de Mudanças
-  **Novas Funcionalidades**: Novas features
-  **Melhorias**: Melhorias em features existentes
- **Correções**: Bug fixes
-  **Documentação**: Mudanças na documentação
-  **Refatoração**: Mudanças de código sem alterar funcionalidade
-  **Performance**: Melhorias de performance
-  **Segurança**: Correções de segurança