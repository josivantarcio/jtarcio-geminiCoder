"""
Cliente AI melhorado para o Gemini Coder.
"""

import json
from typing import Dict, Any, List
import google.generativeai as genai

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import registry


class GeminiClient:
    """Cliente melhorado para a API do Gemini."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def process_request(self, request: str, context: str) -> Dict[str, Any]:
        """Processa uma solicitação do usuário."""
        
        # Obter lista de ferramentas
        available_tools = registry.get_tools_description()
        
        # Criar prompt avançado
        prompt = self._build_advanced_prompt(request, context, available_tools)
        
        try:
            response = self.model.generate_content(prompt)
            cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
            
            # Tentar parsear JSON
            try:
                return json.loads(cleaned_response)
            except json.JSONDecodeError:
                # Se não for JSON válido, tratar como resposta simples
                return {
                    "action": "ANSWER_QUESTION",
                    "answer": response.text
                }
        
        except Exception as e:
            return {
                "action": "ANSWER_QUESTION",
                "answer": f"Erro ao processar solicitação: {str(e)}"
            }
    
    def _build_advanced_prompt(self, request: str, context: str, tools: List[Dict[str, Any]]) -> str:
        """Constrói prompt avançado com ferramentas."""
        
        tools_description = "\\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in tools
        ])
        
        return f"""
Você é um assistente de código avançado, equivalente ao Claude Code. Você tem capacidades completas para analisar, modificar, refatorar e corrigir código diretamente nos projetos.

CONTEXTO ATUAL DO PROJETO:
{context}

FERRAMENTAS DISPONÍVEIS:
{tools_description}

SOLICITAÇÃO DO USUÁRIO:
{request}

SUAS CAPACIDADES INCLUEM:
- Correções diretas em código (como Claude Code faz)
- Refatoração completa de projetos
- Análise profunda de estruturas de código  
- Criação de projetos completos
- Múltiplas edições simultâneas
- Backup automático antes de modificações

INSTRUÇÕES COMPORTAMENTAIS:
1. SEJA PROATIVO: Se detectar problemas no código, corrija-os automaticamente
2. SEJA DIRETO: Execute as ações necessárias sem pedir muitas confirmações
3. SEJA COMPLETO: Quando solicitado para "corrigir" algo, faça todas as correções relacionadas
4. SEJA INTELIGENTE: Use o contexto do projeto para tomar decisões informadas

Responda com um objeto JSON usando uma dessas ações:

**USE_TOOL** - Para uma ferramenta única:
{{
    "action": "USE_TOOL",
    "tool": "nome_da_ferramenta",
    "parameters": {{"param": "value"}},
    "explanation": "O que será feito"
}}

**MULTI_TOOL** - Para múltiplas operações (PREFERIDO para correções):
{{
    "action": "MULTI_TOOL",
    "tools": [
        {{"tool": "backup", "parameters": {{"files": ["arquivo1.py", "arquivo2.py"]}}}},
        {{"tool": "multi_edit", "parameters": {{"edits": [...]}}}},
        {{"tool": "bash", "parameters": {{"command": "python -m py_compile *.py"}}}}
    ],
    "explanation": "Plano completo de correção/modificação"
}}

**CREATE_PROJECT** - Para novos projetos:
{{
    "action": "USE_TOOL",
    "tool": "create_project",
    "parameters": {{
        "project_name": "nome",
        "project_type": "python",
        "files": [
            {{"path": "main.py", "content": "..."}},
            {{"path": "requirements.txt", "content": "..."}}
        ]
    }},
    "explanation": "Criando projeto completo"
}}

**ANSWER_QUESTION** - Apenas para perguntas teóricas:
{{
    "action": "ANSWER_QUESTION",
    "answer": "Resposta detalhada"
}}

PADRÕES DE USO COMUM:

Para "corrigir bugs":
→ backup → analyze → multi_edit → bash (testar)

Para "refatorar código": 
→ backup → refactor → multi_edit → bash (validar)

Para "adicionar funcionalidade":
→ read (entender) → write/multi_edit (implementar) → bash (testar)

Para "analisar projeto":
→ glob (listar arquivos) → analyze → grep (buscar padrões)

IMPORTANTE: 
- Use multi_edit para correções em múltiplos arquivos
- Sempre faça backup antes de modificações grandes
- Execute testes após modificações quando possível
- Seja assertivo e execute as ações solicitadas

Responda APENAS com o objeto JSON válido.
"""
    
    def analyze_code_structure(self, file_path: str) -> Dict[str, Any]:
        """Analisa estrutura de um arquivo de código."""
        
        # Usar ferramenta de análise se for Python
        if file_path.endswith('.py'):
            result = registry.execute_tool('analyze', file_path=file_path)
            if result.success:
                return result.content
        
        # Fallback: ler arquivo e fazer análise básica
        result = registry.execute_tool('read', file_path=file_path)
        if result.success:
            content = result.content
            lines = content.split('\\n')
            
            return {
                'file_path': file_path,
                'lines': len(lines),
                'characters': len(content),
                'analysis_type': 'basic'
            }
        
        return {'error': 'Não foi possível analisar o arquivo'}
    
    def suggest_improvements(self, analysis: Dict[str, Any]) -> List[str]:
        """Sugere melhorias baseadas na análise."""
        suggestions = []
        
        if 'functions' in analysis:
            functions = analysis['functions']
            
            # Verificar funções sem docstring
            functions_without_docs = [f for f in functions if 'docstring' not in f]
            if functions_without_docs:
                suggestions.append(f"Adicionar docstrings para {len(functions_without_docs)} função(ões)")
            
            # Verificar funções com muitos parâmetros
            complex_functions = [f for f in functions if len(f.get('args', [])) > 5]
            if complex_functions:
                suggestions.append(f"Considerar refatorar {len(complex_functions)} função(ões) com muitos parâmetros")
        
        if 'classes' in analysis:
            classes = analysis['classes']
            
            # Verificar classes sem docstring
            classes_without_docs = [c for c in classes if 'docstring' not in c]
            if classes_without_docs:
                suggestions.append(f"Adicionar docstrings para {len(classes_without_docs)} classe(s)")
        
        return suggestions