"""
Gerenciador de contexto e memória para o Gemini Coder.
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
from gitignore_parser import parse_gitignore


class ContextManager:
    """Gerencia o contexto e memória das conversas."""
    
    def __init__(self, memory_file: str = ".gemini_memory.json"):
        self.memory_file = memory_file
        self.current_context: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, Any]] = []
        self.project_files: Dict[str, str] = {}  # Cache de arquivos
        self.project_structure: Dict[str, Any] = {}
        self.load_memory()
    
    def load_memory(self):
        """Carrega memória persistente do disco."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('conversation_history', [])
                    self.current_context = data.get('current_context', {})
            except Exception as e:
                print(f"Erro ao carregar memória: {e}")
    
    def save_memory(self):
        """Salva memória no disco."""
        try:
            memory_data = {
                'conversation_history': self.conversation_history[-50:],  # Manter últimas 50
                'current_context': self.current_context,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar memória: {e}")
    
    def add_conversation_entry(self, request: str, response: Dict[str, Any]):
        """Adiciona entrada à conversa."""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'request': request,
            'response': response,
            'context_hash': self._get_context_hash()
        }
        self.conversation_history.append(entry)
        
        # Manter apenas últimas 100 entradas na memória
        if len(self.conversation_history) > 100:
            self.conversation_history = self.conversation_history[-100:]
        
        self.save_memory()
    
    def load_project_context(self, path: str = "."):
        """Carrega contexto do projeto."""
        project_info = {
            'path': os.path.abspath(path),
            'loaded_at': datetime.now().isoformat()
        }
        
        # Verificar se é repositório Git
        git_dir = os.path.join(path, '.git')
        if os.path.exists(git_dir):
            project_info['is_git_repo'] = True
            project_info['git_info'] = self._get_git_info(path)
        
        # Analisar estrutura do projeto
        project_info['structure'] = self._analyze_project_structure(path)
        
        # Detectar tipo de projeto
        project_info['project_type'] = self._detect_project_type(path)
        
        # Carregar arquivos importantes
        project_info['important_files'] = self._load_important_files(path)
        
        self.current_context.update(project_info)
        self.save_memory()
    
    def _get_git_info(self, path: str) -> Dict[str, Any]:
        """Obtém informações do Git."""
        import subprocess
        
        git_info = {}
        try:
            # Branch atual
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  cwd=path, capture_output=True, text=True)
            if result.returncode == 0:
                git_info['current_branch'] = result.stdout.strip()
            
            # Status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=path, capture_output=True, text=True)
            if result.returncode == 0:
                git_info['has_changes'] = bool(result.stdout.strip())
                git_info['status'] = result.stdout.strip()
            
            # Último commit
            result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                                  cwd=path, capture_output=True, text=True)
            if result.returncode == 0:
                git_info['last_commit'] = result.stdout.strip()
        
        except Exception:
            pass  # Git não disponível ou erro
        
        return git_info
    
    def _analyze_project_structure(self, path: str) -> Dict[str, Any]:
        """Analisa estrutura do projeto."""
        structure = {
            'directories': [],
            'files': [],
            'total_files': 0,
            'file_types': {}
        }
        
        # Configurar gitignore se existir
        gitignore_path = os.path.join(path, '.gitignore')
        matches = parse_gitignore(gitignore_path) if os.path.exists(gitignore_path) else lambda x: False
        
        for root, dirs, files in os.walk(path):
            # Filtrar diretórios ignorados
            dirs[:] = [d for d in dirs if not matches(os.path.join(root, d))]
            
            rel_root = os.path.relpath(root, path)
            if rel_root != '.':
                structure['directories'].append(rel_root)
            
            for file in files:
                filepath = os.path.join(root, file)
                if not matches(filepath):
                    rel_path = os.path.relpath(filepath, path)
                    structure['files'].append(rel_path)
                    structure['total_files'] += 1
                    
                    # Contar tipos de arquivo
                    ext = os.path.splitext(file)[1].lower()
                    structure['file_types'][ext] = structure['file_types'].get(ext, 0) + 1
        
        return structure
    
    def _detect_project_type(self, path: str) -> List[str]:
        """Detecta tipo de projeto baseado nos arquivos."""
        project_types = []
        
        files_in_root = os.listdir(path)
        
        # Python
        if any(f in files_in_root for f in ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile']):
            project_types.append('python')
        
        # Node.js
        if 'package.json' in files_in_root:
            project_types.append('nodejs')
        
        # Java
        if any(f in files_in_root for f in ['pom.xml', 'build.gradle']):
            project_types.append('java')
        
        # Rust
        if 'Cargo.toml' in files_in_root:
            project_types.append('rust')
        
        # Go
        if 'go.mod' in files_in_root:
            project_types.append('go')
        
        # Web
        if any(f in files_in_root for f in ['index.html', 'package.json']):
            project_types.append('web')
        
        # Docker
        if any(f in files_in_root for f in ['Dockerfile', 'docker-compose.yml']):
            project_types.append('docker')
        
        return project_types
    
    def _load_important_files(self, path: str) -> Dict[str, str]:
        """Carrega conteúdo de arquivos importantes."""
        important_files = {}
        
        # Lista de arquivos importantes para carregar
        important_filenames = [
            'README.md', 'README.txt', 'README',
            'requirements.txt', 'package.json', 'Cargo.toml', 'go.mod',
            'setup.py', 'pyproject.toml', 'pom.xml', 'build.gradle',
            'Dockerfile', 'docker-compose.yml',
            '.gitignore', 'LICENSE', 'Makefile'
        ]
        
        for filename in important_filenames:
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath) and os.path.getsize(filepath) < 50000:  # Max 50KB
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        important_files[filename] = f.read()
                except Exception:
                    pass  # Ignorar erros de leitura
        
        return important_files
    
    def get_context(self) -> str:
        """Obtém contexto formatado para a AI."""
        context_parts = []
        
        # Informações do projeto
        if 'path' in self.current_context:
            context_parts.append(f"=== CONTEXTO DO PROJETO ===")
            context_parts.append(f"Caminho: {self.current_context['path']}")
            
            if 'project_type' in self.current_context:
                context_parts.append(f"Tipos: {', '.join(self.current_context['project_type'])}")
            
            if 'git_info' in self.current_context:
                git_info = self.current_context['git_info']
                context_parts.append(f"Git Branch: {git_info.get('current_branch', 'N/A')}")
                context_parts.append(f"Status: {'Limpo' if not git_info.get('has_changes') else 'Com alterações'}")
        
        # Estrutura do projeto
        if 'structure' in self.current_context:
            structure = self.current_context['structure']
            context_parts.append(f"\\nArquivos: {structure['total_files']}")
            context_parts.append(f"Tipos principais: {dict(list(sorted(structure['file_types'].items(), key=lambda x: x[1], reverse=True))[:5])}")
        
        # Arquivos importantes
        if 'important_files' in self.current_context:
            context_parts.append(f"\\n=== ARQUIVOS IMPORTANTES ===")
            for filename, content in self.current_context['important_files'].items():
                context_parts.append(f"\\n--- {filename} ---")
                context_parts.append(content[:1000] + ("..." if len(content) > 1000 else ""))
        
        # Histórico recente
        if self.conversation_history:
            context_parts.append(f"\\n=== HISTÓRICO RECENTE ===")
            for entry in self.conversation_history[-3:]:  # Últimas 3 entradas
                context_parts.append(f"User: {entry['request'][:100]}...")
                response_text = entry['response'].get('explanation', entry['response'].get('answer', ''))
                context_parts.append(f"AI: {response_text[:100]}...")
        
        return "\\n".join(context_parts)
    
    def get_context_info(self) -> Dict[str, Any]:
        """Obtém informações do contexto para exibição."""
        info = {}
        
        if 'path' in self.current_context:
            info['Projeto'] = self.current_context['path']
        
        if 'project_type' in self.current_context:
            info['Tipos'] = ', '.join(self.current_context['project_type'])
        
        if 'structure' in self.current_context:
            structure = self.current_context['structure']
            info['Total de Arquivos'] = structure['total_files']
            info['Diretórios'] = len(structure['directories'])
        
        if 'git_info' in self.current_context:
            git_info = self.current_context['git_info']
            info['Git Branch'] = git_info.get('current_branch', 'N/A')
            info['Git Status'] = 'Limpo' if not git_info.get('has_changes') else 'Com alterações'
        
        info['Histórico'] = len(self.conversation_history)
        
        return info
    
    def _get_context_hash(self) -> str:
        """Gera hash do contexto atual."""
        context_str = json.dumps(self.current_context, sort_keys=True)
        return hashlib.md5(context_str.encode()).hexdigest()[:8]
    
    def get_current_timestamp(self) -> str:
        """Obtém timestamp atual."""
        return datetime.now().isoformat()
    
    def update_file_cache(self, filepath: str, content: str):
        """Atualiza cache de arquivo."""
        self.project_files[filepath] = content
    
    def get_file_from_cache(self, filepath: str) -> Optional[str]:
        """Obtém arquivo do cache."""
        return self.project_files.get(filepath)
    
    def clear_context(self):
        """Limpa contexto atual."""
        self.current_context.clear()
        self.project_files.clear()
        self.save_memory()