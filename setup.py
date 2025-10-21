#!/usr/bin/env python3
"""Setup script for Deep Agent with Ollama."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False


def check_ollama_installed() -> bool:
    """Check if Ollama is installed and running."""
    print("🔍 Checking Ollama installation...")
    
    try:
        # Check if ollama command exists
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama command not found")
            return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False


def check_ollama_server() -> bool:
    """Check if Ollama server is running."""
    print("🔍 Checking Ollama server...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is running")
            return True
        else:
            print("❌ Ollama server not responding")
            return False
    except Exception as e:
        print(f"❌ Ollama server not accessible: {e}")
        return False


def check_model_available(model_name: str) -> bool:
    """Check if the specified model is available."""
    print(f"🔍 Checking if model '{model_name}' is available...")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            if model_name in model_names:
                print(f"✅ Model '{model_name}' is available")
                return True
            else:
                print(f"❌ Model '{model_name}' not found")
                print(f"Available models: {', '.join(model_names)}")
                return False
        else:
            print("❌ Could not fetch model list")
            return False
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False


def pull_model(model_name: str) -> bool:
    """Pull a model from Ollama."""
    print(f"📥 Pulling model '{model_name}'...")
    return run_command(f"ollama pull {model_name}", f"Pulling model {model_name}")


def main():
    """Main setup function."""
    print("🚀 Deep Agent with Ollama Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not run_command("uv sync", "Installing Python dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check Ollama installation
    print("\n🔧 Checking Ollama setup...")
    if not check_ollama_installed():
        print("\n❌ Ollama is not installed. Please install it first:")
        print("Visit: https://ollama.ai/download")
        sys.exit(1)
    
    # Check Ollama server
    if not check_ollama_server():
        print("\n⚠️  Ollama server is not running. Please start it:")
        print("Run: ollama serve")
        sys.exit(1)
    
    # Check for configured model
    # Add core directory to path
    sys.path.insert(0, str(Path(__file__).parent / "core"))
    from config import Config
    configured_model = Config.OLLAMA_MODEL
    if not check_model_available(configured_model):
        print(f"\n📥 Model '{configured_model}' not found. Pulling it...")
        if not pull_model(configured_model):
            print("❌ Failed to pull model")
            sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\n🎉 You can now run the Deep Agent with Ollama examples:")
    print("  uv run python examples/cli.py")
    print("\n📚 Available modes:")
    print("  - cli: Command-line interface example")
    print("  - interactive: Interactive chat mode")


if __name__ == "__main__":
    main()
