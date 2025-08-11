#!/bin/bash

# Setup global do Gemini Coder - Similar ao Claude Code
# Permite usar 'gemini "mensagem"' de qualquer lugar

set -e

echo " Gemini Coder - Setup Global"
echo "==============================="

# Obter diretório atual do projeto
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
GEMINI_PATH="$SCRIPT_DIR/gemini_coder.py"

# Verificar se o arquivo principal existe
if [ ! -f "$GEMINI_PATH" ]; then
    echo " Erro: gemini_coder.py não encontrado em $SCRIPT_DIR"
    exit 1
fi

# Criar wrapper script
WRAPPER_SCRIPT="/usr/local/bin/gemini"
TEMP_WRAPPER="/tmp/gemini_wrapper"

cat > "$TEMP_WRAPPER" << EOF
#!/bin/bash
# Gemini Coder Global Wrapper
# Permite usar 'gemini "mensagem"' de qualquer diretório

GEMINI_PROJECT_PATH="$SCRIPT_DIR"
GEMINI_SCRIPT="\$GEMINI_PROJECT_PATH/gemini_coder.py"

# Verificar se o script existe
if [ ! -f "\$GEMINI_SCRIPT" ]; then
    echo " Erro: Gemini Coder não encontrado em \$GEMINI_PROJECT_PATH"
    echo "Execute o setup novamente no diretório correto"
    exit 1
fi

# Executar o gemini_coder.py do diretório atual do usuário
cd "\$(pwd)"
export PYTHONPATH="\$GEMINI_PROJECT_PATH:\$PYTHONPATH"
python3 "\$GEMINI_SCRIPT" "\$@"
EOF

# Tornar executable
chmod +x "$TEMP_WRAPPER"

# Verificar permissões para /usr/local/bin
if [ -w "/usr/local/bin" ]; then
    mv "$TEMP_WRAPPER" "$WRAPPER_SCRIPT"
    echo " Comando global 'gemini' instalado em /usr/local/bin/gemini"
else
    echo " Permissões de administrador necessárias..."
    if command -v sudo &> /dev/null; then
        sudo mv "$TEMP_WRAPPER" "$WRAPPER_SCRIPT"
        echo " Comando global 'gemini' instalado em /usr/local/bin/gemini"
    else
        echo " sudo não disponível. Instalação manual necessária:"
        echo "   sudo cp $TEMP_WRAPPER /usr/local/bin/gemini"
        echo "   sudo chmod +x /usr/local/bin/gemini"
        exit 1
    fi
fi

# Verificar se /usr/local/bin está no PATH
if [[ ":$PATH:" != *":/usr/local/bin:"* ]]; then
    echo "  /usr/local/bin não está no PATH"
    echo "   Adicione ao seu ~/.bashrc ou ~/.zshrc:"
    echo "   export PATH=\"/usr/local/bin:\$PATH\""
fi

# Criar configuração global se não existir
GLOBAL_CONFIG="$HOME/.gemini_config.json"
if [ ! -f "$GLOBAL_CONFIG" ]; then
    echo ""
    read -p "Deseja criar configuração global? (S/n): " create_config
    if [[ ! $create_config =~ ^[Nn]$ ]]; then
        python3 "$GEMINI_PATH" --create-config
        if [ -f ".gemini_config.json" ]; then
            mv ".gemini_config.json" "$GLOBAL_CONFIG"
            echo " Configuração criada em $GLOBAL_CONFIG"
        fi
    fi
fi

# Teste
echo ""
echo " Testando instalação global..."
if command -v gemini &> /dev/null; then
    if gemini --tools > /dev/null 2>&1; then
        echo " Instalação global bem-sucedida!"
    else
        echo "  Comando encontrado mas com erro. Verifique a configuração."
    fi
else
    echo " Comando 'gemini' não encontrado no PATH"
    echo "   Você pode precisar reiniciar o terminal ou adicionar /usr/local/bin ao PATH"
fi

echo ""
echo " Setup concluído!"
echo ""
echo " Como usar (de qualquer diretório):"
echo "   gemini \"Crie um arquivo main.py\""
echo "   gemini --interactive"
echo "   gemini \"Analise este projeto\""
echo ""
echo "Para desinstalar:"
echo "   sudo rm /usr/local/bin/gemini"
echo ""
echo "Agora você pode usar 'gemini' como o 'claude'! "