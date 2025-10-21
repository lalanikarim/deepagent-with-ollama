"""Core modules for Deep Agent with Ollama example implementation."""

from agent import DeepAgent
from tools import web_search, get_current_time, calculate
from config import Config

__version__ = "0.1.0"
__all__ = ["DeepAgent", "web_search", "get_current_time", "calculate"]
