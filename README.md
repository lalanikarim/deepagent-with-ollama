# 🤖 Deep Agent with Ollama - Example Implementation

This is an **example implementation** demonstrating how to use the [Deep Agents](https://github.com/langchain-ai/deepagents) framework with [Ollama](https://ollama.ai/) for local LLM processing. It showcases advanced AI agent capabilities including planning, tool usage, and web search integration.

## 🎯 What This Example Demonstrates

- **Deep Agents Framework Integration** - How to use `create_deep_agent` with custom tools
- **Local LLM Processing** - Ollama integration for privacy-focused AI processing
- **Planning Capabilities** - Built-in `write_todos` tool for task management
- **Web Search Integration** - DuckDuckGo as an alternative to Tavily
- **Streaming with Tool Visibility** - Real-time feedback showing tool usage and outputs
- **File System Operations** - Built-in filesystem tools for data persistence
- **Sub-agent Delegation** - Task delegation to specialized agents

## 🏗️ Project Structure

```
deepagent/
├── core/                    # Core implementation modules
│   ├── agent.py            # DeepAgent class implementation
│   ├── tools.py            # Custom tools (web search, calculator, etc.)
│   ├── config.py           # Configuration management
│   └── __init__.py         # Core module exports
├── examples/               # Example usage and CLI
│   └── cli.py             # Command-line interface example
├── setup.py               # Setup and validation script
├── pyproject.toml         # Project dependencies
├── env.example            # Environment configuration template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** (recommended: 3.13) installed
2. **Ollama** installed and running
3. **uv** package manager (recommended) or pip

### Setup

1. **Clone and install:**
   ```bash
   git clone <your-repo-url>
   cd deepagent
   uv sync  # or pip install -e .
   ```

2. **Start Ollama:**
   ```bash
   ollama serve
   ```

3. **Pull a model:**
   ```bash
   ollama pull llama3.2:3b
   ```

4. **Configure environment:**
   ```bash
   cp env.example .env
   # Edit .env with your Ollama configuration
   ```

5. **Run setup validation:**
   ```bash
   uv run python setup.py
   ```

## 🎮 Example Usage

### Command-Line Interface

```bash
# Simple query
uv run python examples/cli.py "What is the latest news about AI?"

# Multi-step planning task
uv run python examples/cli.py "Research Python 3.13 features, write a summary, and create a presentation outline"

# Show tool usage and planning steps (verbose mode)
uv run python examples/cli.py "Research AI news and calculate metrics" --show-tools

# Interactive mode
uv run python examples/cli.py
```

## 🔧 Configuration

Create a `.env` file based on `env.example`:

```env
# Ollama Configuration (REQUIRED)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest

# Agent Configuration
USE_LONGTERM_MEMORY=false

# Web Search Configuration
WEB_SEARCH_MAX_RESULTS=5
WEB_SEARCH_REGION=us-en
WEB_SEARCH_SAFESEARCH=moderate
```

## 🛠️ Implementation Details

### Deep Agents Framework Integration

This example demonstrates how to integrate with the Deep Agents framework using:
- `create_deep_agent()` function for agent creation
- Custom tools integration
- Built-in planning capabilities
- Streaming with tool visibility

### Available Tools

**Built-in Deep Agents Tools:**
- **`write_todos`** - Task planning and management
- **`ls`, `read_file`, `write_file`, `edit_file`** - File system operations
- **`task`** - Sub-agent delegation

**Custom Tools in This Example:**
- **`web_search`** - DuckDuckGo web search
- **`get_current_time`** - Current time information
- **`calculate`** - Mathematical calculations

## 🧠 Planning and Task Management

The example demonstrates the Deep Agents planning capabilities with real-time tool visibility. When using the `--show-tools` flag, you can see:

- Tool calls with input parameters
- Tool outputs (truncated for readability)
- Planning steps using `write_todos`
- Task delegation and file operations

This provides transparency into how the agent breaks down complex tasks and executes them step by step.

## 📚 Learning Resources

- [Deep Agents Documentation](https://github.com/langchain-ai/deepagents)
- [Ollama Documentation](https://ollama.ai/docs)
- [LangChain Documentation](https://python.langchain.com/)

## 🤝 Contributing

This is an example implementation. Feel free to:
- Fork and modify for your own use cases
- Submit issues or suggestions
- Create your own examples based on this structure

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Deep Agents](https://github.com/langchain-ai/deepagents) - The core framework
- [Ollama](https://ollama.ai/) - Local LLM processing
- [DuckDuckGo](https://duckduckgo.com/) - Web search capabilities
- [LangChain](https://langchain.com/) - LLM framework