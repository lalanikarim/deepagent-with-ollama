"""Configuration settings for Deep Agent with Ollama."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Deep Agent with Ollama settings."""
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
    
    # Validate required environment variables
    if not OLLAMA_BASE_URL:
        raise ValueError("OLLAMA_BASE_URL environment variable is required")
    if not OLLAMA_MODEL:
        raise ValueError("OLLAMA_MODEL environment variable is required")
    
    # Agent Configuration
    USE_LONGTERM_MEMORY = os.getenv("USE_LONGTERM_MEMORY", "false").lower() == "true"
    
    # Custom system prompt (optional)
    CUSTOM_SYSTEM_PROMPT = os.getenv("CUSTOM_SYSTEM_PROMPT", None)
    
    # Default tools configuration
    WEB_SEARCH_MAX_RESULTS = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "5"))
    WEB_SEARCH_REGION = os.getenv("WEB_SEARCH_REGION", "us-en")
    WEB_SEARCH_SAFESEARCH = os.getenv("WEB_SEARCH_SAFESEARCH", "moderate")
    
    @classmethod
    def validate(cls):
        """Validate configuration settings."""
        errors = []
        
        # Check if Ollama is accessible
        try:
            import requests
            response = requests.get(f"{cls.OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code != 200:
                errors.append(f"Ollama server not accessible at {cls.OLLAMA_BASE_URL}")
        except Exception as e:
            errors.append(f"Cannot connect to Ollama server: {e}")
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(errors))
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration."""
        print("Deep Agent with Ollama Configuration:")
        print("=" * 30)
        print(f"Ollama Base URL: {cls.OLLAMA_BASE_URL}")
        print(f"Ollama Model: {cls.OLLAMA_MODEL}")
        print(f"Use Long-term Memory: {cls.USE_LONGTERM_MEMORY}")
        print(f"Web Search Max Results: {cls.WEB_SEARCH_MAX_RESULTS}")
        print(f"Web Search Region: {cls.WEB_SEARCH_REGION}")
        print(f"Web Search SafeSearch: {cls.WEB_SEARCH_SAFESEARCH}")
        if cls.CUSTOM_SYSTEM_PROMPT:
            print(f"Custom System Prompt: {cls.CUSTOM_SYSTEM_PROMPT[:100]}...")
        print("=" * 30)
