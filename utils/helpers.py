"""
Funções auxiliares para o Gemini Coder.
"""

import os
import time
import hashlib
from typing import Optional, List, Dict, Any
from pathlib import Path


def format_file_size(size_bytes: int) -> str:
    """Formata tamanho de arquivo em formato legível."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def safe_read_file(file_path: str, max_size: int = 1024 * 1024) -> Optional[str]:
    """Lê arquivo de forma segura com limite de tamanho."""
    try:
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        if path.stat().st_size > max_size:
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    except Exception:
        return None


def validate_file_path(file_path: str, must_exist: bool = True) -> bool:
    """Valida caminho de arquivo."""
    try:
        path = Path(file_path)
        
        if must_exist and not path.exists():
            return False
        
        # Verificar se é um caminho válido
        if not path.parent.exists():
            return False
        
        # Verificar se não é um diretório quando esperamos arquivo
        if must_exist and path.is_dir():
            return False
        
        return True
    
    except Exception:
        return False


def calculate_file_hash(file_path: str) -> Optional[str]:
    """Calcula hash MD5 de um arquivo."""
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    except Exception:
        return None


def get_file_info(file_path: str) -> Dict[str, Any]:
    """Obtém informações detalhadas de um arquivo."""
    try:
        path = Path(file_path)
        
        if not path.exists():
            return {"exists": False}
        
        stat = path.stat()
        
        info = {
            "exists": True,
            "path": str(path.absolute()),
            "name": path.name,
            "extension": path.suffix,
            "size": stat.st_size,
            "size_formatted": format_file_size(stat.st_size),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:]
        }
        
        # Hash apenas para arquivos pequenos
        if path.is_file() and stat.st_size < 10 * 1024 * 1024:  # < 10MB
            info["hash"] = calculate_file_hash(file_path)
        
        return info
    
    except Exception as e:
        return {"exists": False, "error": str(e)}


def find_files_by_extension(directory: str, extensions: List[str], recursive: bool = True) -> List[str]:
    """Encontra arquivos por extensão."""
    try:
        path = Path(directory)
        
        if not path.exists() or not path.is_dir():
            return []
        
        files = []
        extensions = [ext.lower() for ext in extensions]
        
        if recursive:
            pattern = "**/*"
        else:
            pattern = "*"
        
        for file_path in path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                files.append(str(file_path))
        
        return sorted(files)
    
    except Exception:
        return []


def create_backup_path(original_path: str) -> str:
    """Cria caminho para backup de arquivo."""
    path = Path(original_path)
    timestamp = int(time.time())
    
    return str(path.with_suffix(f".backup_{timestamp}{path.suffix}"))


def is_text_file(file_path: str) -> bool:
    """Verifica se arquivo é texto."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
        
        # Verificar se contém bytes nulos (indicativo de arquivo binário)
        if b'\x00' in chunk:
            return False
        
        # Tentar decodificar como UTF-8
        try:
            chunk.decode('utf-8')
            return True
        except UnicodeDecodeError:
            return False
    
    except Exception:
        return False


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Trunca string se for muito longa."""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def normalize_path(path: str) -> str:
    """Normaliza caminho de arquivo."""
    return str(Path(path).resolve())


def get_relative_path(file_path: str, base_path: str = ".") -> str:
    """Obtém caminho relativo."""
    try:
        return str(Path(file_path).relative_to(Path(base_path).resolve()))
    except ValueError:
        return file_path


def ensure_directory(directory: str) -> bool:
    """Garante que diretório existe."""
    try:
        Path(directory).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def count_lines_in_file(file_path: str) -> int:
    """Conta linhas em arquivo."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def get_file_language(file_path: str) -> Optional[str]:
    """Detecta linguagem de programação baseada na extensão."""
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.c': 'c',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.php': 'php',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'zsh',
        '.fish': 'fish',
        '.ps1': 'powershell',
        '.sql': 'sql',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.xml': 'xml',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.conf': 'conf',
        '.md': 'markdown',
        '.markdown': 'markdown',
        '.rst': 'restructuredtext',
        '.tex': 'latex',
        '.r': 'r',
        '.R': 'r',
        '.m': 'matlab',
        '.pl': 'perl',
        '.lua': 'lua',
        '.vim': 'vim',
        '.dockerfile': 'dockerfile',
        '.Dockerfile': 'dockerfile'
    }
    
    extension = Path(file_path).suffix.lower()
    return language_map.get(extension)