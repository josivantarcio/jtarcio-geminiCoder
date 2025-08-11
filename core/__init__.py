"""
Módulo core do Gemini Coder.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from core.interactive import InteractiveMode
    from core.context import ContextManager
    from core.ai_client import GeminiClient
    from core.config import Config
except ImportError:
    # Fallback para imports relativos
    from .interactive import InteractiveMode
    from .context import ContextManager
    from .ai_client import GeminiClient
    from .config import Config

__all__ = ['InteractiveMode', 'ContextManager', 'GeminiClient', 'Config']