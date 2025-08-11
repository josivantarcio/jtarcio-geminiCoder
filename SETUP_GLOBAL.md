# Setup Global do Gemini Coder

Este guia mostra como configurar o Gemini Coder para funcionar exatamente como o Claude Code - executando `gemini "mensagem"` de qualquer lugar no terminal.

## Instalação Rápida

```bash
# 1. Instalar dependências e configurar
bash install.sh

# 2. Configurar comando global
bash setup_global.sh

# 3. Testar
gemini "Olá mundo!"
```

## Passo a Passo Detalhado

### 1. Configuração Básica

```bash
# Clone e entre no diretório
git clone <seu-repo>
cd gemini-coder

# Instale dependências
pip3 install -r requirements.txt

# Configure API key
export GEMINI_API_KEY="sua_chave_aqui"
# OU
python3 gemini_coder.py --create-config
```

### 2. Setup Global

```bash
# Execute o script de setup global
bash setup_global.sh
```

O script irá:
- Criar comando `/usr/local/bin/gemini` 
- Configurar PATH automaticamente
- Verificar permissões e dependências
- Criar configuração global se necessário

### 3. Verificação

```bash
# Teste de qualquer diretório
cd /tmp
gemini --tools
gemini "Analise este diretório"
```

##  Como Usar (Igual ao Claude Code)

### Comandos Básicos
```bash
# De qualquer diretório
gemini "Crie um arquivo Python com hello world"
gemini "Analise este projeto"
gemini "Corrija o bug na função main()"

# Modo interativo
gemini --interactive
gemini -i

# Ver ferramentas disponíveis  
gemini --tools
```

### Exemplos Práticos

```bash
# Análise de projeto
cd ~/meu-projeto
gemini "Analise a estrutura deste projeto e sugira melhorias"

# Correções diretas (como Claude)
gemini "Corrija todos os erros de sintaxe nos arquivos Python"
gemini "Refatore a função calculate() para ser mais eficiente"
gemini "Adicione docstrings em todas as funções do projeto"

# Criação de projetos
cd ~/
gemini "Crie um projeto Flask básico chamado 'minha-api'"
gemini "Gere testes unitários para todas as funções"
```

##  Funcionalidades Avançadas

O Gemini agora pode fazer **correções diretas** como o Claude Code:

### Multi-Edit (Correções em Múltiplos Arquivos)
```bash
gemini "Substitua todas as ocorrências de 'print()' por 'logging.info()' em todos os arquivos Python"
```

### Refatoração
```bash
gemini "Renomeie a função 'calcular' para 'calculate' em todo o projeto"
gemini "Mova todas as funções de utilidade para um arquivo utils.py"
```

### Backup Automático
```bash
gemini "Faça backup dos arquivos antes de refatorar"
```

### Criação de Projetos Completos
```bash
gemini "Crie um projeto Django completo com models, views e templates"
```

##  Estrutura de Funcionamento

```
Sistema Global:
/usr/local/bin/gemini              # Comando global
~/.gemini_config.json              # Configuração global
~/seu-projeto/.gemini_memory.json  # Memória por projeto

Quando você executa 'gemini':
1. Comando global detecta diretório atual
2. Carrega contexto do projeto atual
3. Usa configuração global + memória local
4. Executa com todas as ferramentas disponíveis
```

##  Comparação com Claude Code

| Funcionalidade | Claude Code | Gemini Coder |
|---------------|-------------|--------------|
| `claude "msg"` | Sim | Sim `gemini "msg"` |
| Correções diretas | Sim | Sim |
| Modo interativo | Sim | Sim |
| Multi-edit | Sim | Sim |
| Análise de projeto | Sim | Sim |
| Memória de contexto | Sim | Sim |
| **Open Source** | Não | Sim |
| **API Gratuita** | Não | Sim |

##  Troubleshooting

### Comando 'gemini' não encontrado
```bash
# Verificar PATH
echo $PATH | grep -q "/usr/local/bin" && echo "PATH OK" || echo "Adicione /usr/local/bin ao PATH"

# Adicionar ao PATH permanentemente
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Erro de permissão
```bash
# Dar permissão ao comando
sudo chmod +x /usr/local/bin/gemini

# Verificar proprietário
ls -la /usr/local/bin/gemini
```

### API Key não encontrada
```bash
# Configurar globalmente
export GEMINI_API_KEY="sua_chave"
echo 'export GEMINI_API_KEY="sua_chave"' >> ~/.bashrc

# OU configurar por projeto
gemini --create-config
```

##  Desinstalação

```bash
# Remover comando global
sudo rm /usr/local/bin/gemini

# Remover configurações (opcional)
rm ~/.gemini_config.json
rm -rf ~/.gemini_coder_history
```

##  Atualizações

```bash
# Para atualizar o Gemini Coder
cd /caminho/para/gemini-coder
git pull
bash setup_global.sh  # Reconfigurar se necessário
```

---

 **Agora você tem o seu próprio Claude Code, mas melhor!** 

-  **Open Source** 
-  **API Gratuita**
-  **Totalmente customizável**
-  **Funcionalidades idênticas**