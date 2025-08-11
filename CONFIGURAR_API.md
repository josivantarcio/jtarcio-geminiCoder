#  Configurar API Key do Gemini

##  **Comando `gemini` já está funcionando!**

Você já pode usar `gemini "mensagem"` de qualquer lugar. Só falta configurar a API key.

##  Como obter a API Key

1. **Acesse**: https://makersuite.google.com/app/apikey
2. **Faça login** com sua conta Google
3. **Clique em "Create API Key"**
4. **Copie a chave** gerada

##  Configurar API Key

### Opção 1: Variável de Ambiente (Recomendado)

```bash
# Adicionar ao ~/.bashrc (permanente)
echo 'export GEMINI_API_KEY="sua_api_key_aqui"' >> ~/.bashrc
source ~/.bashrc

# Ou apenas para esta sessão (temporário)  
export GEMINI_API_KEY="sua_api_key_aqui"
```

### Opção 2: Arquivo de Configuração

```bash
# Criar config global
gemini --create-config

# Editar o arquivo criado
nano ~/.gemini_config.json
```

No arquivo, substitua `"your_api_key_here"` pela sua chave real.

##  Testar Configuração

```bash
# Testar se está funcionando
gemini "olá mundo"

# Modo interativo
gemini --interactive
```

##  Exemplo de Uso

```bash
# Análise
gemini "analise este diretório"

# Criação de código
gemini "crie um arquivo hello.py"

# Correções
gemini "corrija os erros neste código"
```

##  Se der erro

```bash
# Ver onde está o erro
gemini --tools

# Verificar se PATH está correto
echo $PATH | grep ".local/bin"

# Re-executar setup se necessário
cd ~/ws/gemini-coder
bash setup_local.sh
```

---

** Assim que configurar a API key, você terá seu próprio "Claude Code" funcionando!**