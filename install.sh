#!/bin/bash

# Install script for Gemini Coder
# Instala dependências e configura alias global

set -e

echo " Gemini Coder - Instalador"
echo "=============================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo " Python 3 não encontrado. Por favor instale Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo " Python $PYTHON_VERSION encontrado"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo " pip3 não encontrado. Por favor instale pip"
    exit 1
fi

echo " pip encontrado"

# Instalar dependências
echo ""
echo " Instalando dependências..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo " Dependências instaladas com sucesso"
else
    echo " Erro ao instalar dependências"
    exit 1
fi

# Verificar API key
echo ""
if [ -z "$GEMINI_API_KEY" ]; then
    echo "  GEMINI_API_KEY não configurado"
    echo "   Por favor configure sua API key:"
    echo "   export GEMINI_API_KEY='sua_chave_aqui'"
    echo "   ou use: python3 gemini_coder.py --create-config"
else
    echo " GEMINI_API_KEY configurado"
fi

# Criar alias global (opcional)
echo ""
read -p " Deseja criar um alias global 'gemini' para facilitar o uso? (s/N): " create_alias

if [[ $create_alias =~ ^[Ss]$ ]]; then
    SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
    ALIAS_COMMAND="alias gemini='python3 $SCRIPT_DIR/gemini_coder.py'"
    
    # Detectar shell e arquivo de configuração
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
    
    # Verificar se alias já existe
    if grep -q "alias gemini=" "$SHELL_RC" 2>/dev/null; then
        echo "  Alias 'gemini' já existe em $SHELL_RC"
        read -p "   Deseja sobrescrever? (s/N): " overwrite
        if [[ $overwrite =~ ^[Ss]$ ]]; then
            sed -i "/alias gemini=/d" "$SHELL_RC"
            echo "$ALIAS_COMMAND" >> "$SHELL_RC"
            echo " Alias atualizado em $SHELL_RC"
        fi
    else
        echo "$ALIAS_COMMAND" >> "$SHELL_RC"
        echo " Alias criado em $SHELL_RC"
    fi
    
    echo ""
    echo "   Para usar o alias imediatamente:"
    echo "   source $SHELL_RC"
    echo ""
    echo "   Ou abra um novo terminal e use:"
    echo "   gemini --interactive"
    echo "   gemini 'sua solicitação'"
fi

# Teste básico
echo ""
echo " Testando instalação..."

if python3 gemini_coder.py --tools > /dev/null 2>&1; then
    echo " Instalação bem-sucedida!"
else
    echo " Erro no teste. Verifique a configuração."
    exit 1
fi

echo ""
echo " Instalação concluída!"
echo ""
echo " Próximos passos:"
echo "1. Configure sua GEMINI_API_KEY se ainda não fez"
echo "2. Execute: python3 gemini_coder.py --interactive"
echo "3. Ou se criou o alias: gemini --interactive"
echo ""
echo "Documentação: README.md"
echo " Issues: https://github.com/seu-usuario/gemini-coder/issues"
echo ""
echo "Feliz coding! "