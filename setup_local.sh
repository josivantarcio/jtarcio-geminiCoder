#!/bin/bash

# Setup local do Gemini Coder - Sem necessidade de sudo
# Cria alias local no ~/.bashrc

set -e

echo " Gemini Coder - Setup Local"
echo "=============================="

# Obter diretório atual do projeto
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
GEMINI_PATH="$SCRIPT_DIR/gemini_coder.py"

# Verificar se o arquivo principal existe
if [ ! -f "$GEMINI_PATH" ]; then
    echo "Erro: gemini_coder.py não encontrado em $SCRIPT_DIR"
    exit 1
fi

# Detectar shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    SHELL_RC="$HOME/.bashrc"
    SHELL_NAME="bash"
fi

echo " Shell detectado: $SHELL_NAME"
echo " Arquivo de configuração: $SHELL_RC"

# Criar função gemini
GEMINI_FUNCTION="
# Gemini Coder - Função global
gemini() {
    local current_dir=\$(pwd)
    cd \"$SCRIPT_DIR\"
    python3 \"$GEMINI_PATH\" \"\$@\"
    cd \"\$current_dir\"
}
"

# Remover função antiga se existir
if grep -q "# Gemini Coder - Função global" "$SHELL_RC" 2>/dev/null; then
    echo "  Função 'gemini' já existe. Removendo versão antiga..."
    sed -i '/# Gemini Coder - Função global/,/^}$/d' "$SHELL_RC"
fi

# Adicionar nova função
echo "$GEMINI_FUNCTION" >> "$SHELL_RC"

echo " Função 'gemini' adicionada ao $SHELL_RC"

# Verificar se .local/bin está no PATH
LOCAL_BIN="$HOME/.local/bin"
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    echo " Adicionando ~/.local/bin ao PATH..."
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
fi

# Criar configuração global se não existir
GLOBAL_CONFIG="$HOME/.gemini_config.json"
if [ ! -f "$GLOBAL_CONFIG" ]; then
    echo ""
    read -p " Deseja criar configuração global? (S/n): " create_config
    if [[ ! $create_config =~ ^[Nn]$ ]]; then
        python3 "$GEMINI_PATH" --create-config
        if [ -f "$SCRIPT_DIR/.gemini_config.json" ]; then
            mv "$SCRIPT_DIR/.gemini_config.json" "$GLOBAL_CONFIG"
            echo " Configuração criada em $GLOBAL_CONFIG"
        fi
    fi
fi

echo ""
echo " Setup local concluído!"
echo ""
echo " Para usar agora:"
echo "   source $SHELL_RC"
echo "   gemini \"Olá mundo!\""
echo ""
echo " Ou abra um novo terminal e use:"
echo "   gemini --interactive"
echo "   gemini \"sua mensagem\""
echo ""
echo " Para testar imediatamente:"
echo "   bash -c 'source $SHELL_RC && gemini --tools'"
echo ""
echo "Agora você pode usar 'gemini' como o 'claude'! "