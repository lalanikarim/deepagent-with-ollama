"""Deep Agent with Ollama package for creating intelligent agents."""

from .agent import DeepAgent
from .tools import web_search, get_current_time, calculate

__version__ = "0.1.0"
__all__ = ["DeepAgent", "web_search", "get_current_time", "calculate"]
