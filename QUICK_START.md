#  Quick Start - Gemini Coder

##  Instalação em 30 segundos

```bash
# 1. Clone e entre no diretório
git clone <seu-repo>
cd gemini-coder

# 2. Instale tudo automaticamente
bash install.sh

# 3. Configure API Key
export GEMINI_API_KEY="sua_chave_aqui"

# 4. Setup global (funcionar como 'claude')
bash setup_global.sh

# 5. Teste
gemini "Olá mundo!"
```

##  Como usar (idêntico ao Claude Code)

```bash
# Análise de projeto
gemini "Analise este projeto"

# Correções diretas
gemini "Corrija todos os bugs no arquivo main.py"

# Criação de código
gemini "Crie um servidor Flask básico"

# Refatoração
gemini "Refatore o código para usar classes"

# Modo interativo
gemini --interactive
```

##  Sem instalação global

```bash
# Uso local
python gemini_coder.py "sua solicitação"
python gemini_coder.py --interactive
```

##  Configuração Rápida

**Opção 1: Variável de ambiente**
```bash
export GEMINI_API_KEY="sua_api_key"
```

**Opção 2: Arquivo de config**
```bash
python gemini_coder.py --create-config
# Edite o .gemini_config.json criado
```

##  Exemplos Práticos

### Análise de Projeto
```bash
gemini "Analise a estrutura deste projeto Python e sugira melhorias"
```

### Correções Automáticas
```bash
gemini "Corrija todos os erros de sintaxe e adicione type hints"
```

### Criação de Projetos
```bash
gemini "Crie um projeto Django completo com authentication"
```

### Refatoração
```bash
gemini "Refatore este código para usar padrões de design"
```

##  14 Ferramentas Disponíveis

- **read/write/edit**: Manipulação de arquivos
- **glob/grep**: Busca de arquivos e texto  
- **bash**: Execução de comandos
- **git_***: Operações Git automatizadas
- **analyze**: Análise de código Python
- **multi_edit**: Edições em múltiplos arquivos
- **create_project**: Criação de projetos completos
- **refactor**: Refatoração automatizada
- **backup**: Backup antes de modificações

##  vs Claude Code

| Funcionalidade | Claude Code | Gemini Coder |
|----------------|-------------|--------------|
| `claude "msg"` | Sim | Sim `gemini "msg"` |
| Correções diretas | Sim | Sim |
| Análise de projetos | Sim | Sim |
| **Open Source** | Não | Sim |
| **API Gratuita** | Não | Sim |
| **Extensível** | Não | Sim |

##  Problemas?

```bash
# Teste do sistema
python test_gemini.py

# Ver ferramentas
gemini --tools

# Reconfigurar global
bash setup_global.sh
```

##  Documentação

- **README.md**: Documentação completa
- **SETUP_GLOBAL.md**: Setup detalhado do comando global
- **CHANGELOG.md**: Histórico de mudanças

---

** Agora você tem seu próprio Claude Code!**

-  **Grátis** (API Gemini)
-  **Open Source**  
-  **Funcionalidades idênticas**
-  **Totalmente customizável**