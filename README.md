# 🤖 Deep Agent with Ollama

A powerful AI agent implementation using [Deep Agents](https://github.com/langchain-ai/deepagents) framework with [Ollama](https://ollama.ai/) for local LLM processing and DuckDuckGo for web search capabilities.

## 🌟 Features

- **Local LLM Processing**: Uses Ollama for privacy-focused AI processing
- **Web Search**: DuckDuckGo integration for real-time information
- **Deep Planning**: Advanced task planning and execution with structured todo lists
- **File System Access**: Store and retrieve information locally
- **Sub-agent Support**: Delegate tasks to specialized sub-agents
- **Memory Management**: Short-term and long-term memory capabilities
- **Streaming Support**: Real-time response streaming with progress indication
- **Async Support**: Full async/await support for modern Python applications
- **Task Management**: Built-in todo list creation and management
- **Progress Tracking**: Real-time task status updates and progress indication
- **Command-Line Interface**: Unified interface for all agent interactions

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **uv** package manager (recommended) or pip

### Installation

1. **Clone and setup the project:**
   ```bash
   git clone <your-repo-url>
   cd deepagent
   uv sync  # or pip install -e .
   ```

2. **Install and start Ollama:**
   ```bash
   # Install Ollama (visit https://ollama.ai/download for your OS)
   # Start Ollama server
   ollama serve
   ```

3. **Pull a model:**
   ```bash
   ollama pull llama3.2:3b
   ```

4. **Run setup script:**
   ```bash
   uv run python setup.py
   ```

### Basic Usage

```python
from deepagent import DeepAgent

# Create the agent
agent = DeepAgent(
    model_name="llama3.2:3b",
    base_url="http://localhost:11434"
)

# Chat with the agent
response = agent.chat("What's the latest news about AI?")
print(response)
```

## 🎯 Usage

### **CLI Mode** (Recommended for all users)

```bash
# Single query (streaming - default)
uv run python cli.py "What is the latest news about AI?"

# Single query (non-streaming)
uv run python cli.py "Calculate 15 * 23" --no-stream

# Multi-step planning task
uv run python cli.py "Research Python 3.13 features, write a summary, and create a presentation outline"

# Task delegation example
uv run python cli.py "I need to: 1) Search for AI news, 2) Calculate 15 * 23, 3) Get current time. Please plan and execute these tasks."

# Interactive mode
uv run python cli.py

# Show configuration
uv run python cli.py --config

# Validate setup
uv run python cli.py --validate

# Use different model
uv run python cli.py "Hello" --model llama3.2:latest

# Use different Ollama server
uv run python cli.py "Hello" --base-url http://localhost:11434

# Show tool usage and planning steps (verbose mode)
uv run python cli.py "Research AI news and calculate metrics" --show-tools

# Example of enhanced tool visibility:
# 🔧 Using web_search(max_results=5, query=AI news, region=us-en, safesearch=moderate)
# 📤 web_search output: [{"title": "Latest AI news...", "body": "...", "href": "..."}]
# 🔧 Using calculate(expression=15 * 23)
# 📤 calculate output: Result: 345
```

### **Programmatic Usage**

```python
from deepagent import DeepAgent

# Create agent
agent = DeepAgent()

# Simple chat
response = agent.chat("What is 5 * 8?")
print(response)

# Streaming chat
for chunk in agent.stream_chat("Search for Python news"):
    print(chunk, end="", flush=True)

# Async usage
import asyncio
async def main():
    response = await agent.achat("What's the weather like?")
    print(response)

asyncio.run(main())
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional):

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
USE_LONGTERM_MEMORY=false
WEB_SEARCH_MAX_RESULTS=5
WEB_SEARCH_REGION=us-en
WEB_SEARCH_SAFESEARCH=moderate
```

### Custom Configuration

```python
from deepagent import DeepAgent

agent = DeepAgent(
    model_name="llama3.2:3b",
    base_url="http://localhost:11434",
    use_longterm_memory=True,
    system_prompt="You are a specialized research assistant..."
)
```

## 🛠️ Available Tools

### Built-in Deep Agents Tools

#### Task Planning
- **Function**: `write_todos(todos)`
- **Purpose**: Create and manage structured task lists for complex work
- **Example**: Automatically used for multi-step tasks to track progress

#### File System Operations
- **Function**: `ls(path)`, `read_file(path)`, `write_file(path, content)`, `edit_file(path, old_string, new_string)`
- **Purpose**: Store and organize information locally
- **Example**: Save research results, create reports, organize files

#### Task Delegation
- **Function**: `task(subagent_type, task_description)`
- **Purpose**: Launch sub-agents for complex, independent tasks
- **Example**: Delegate research tasks to specialized agents

### Custom Tools

#### Web Search
- **Function**: `web_search(query, max_results=5, region="us-en", safesearch="moderate")`
- **Purpose**: Search the web using DuckDuckGo
- **Example**: `web_search("latest AI developments", max_results=3)`

#### Time Information
- **Function**: `get_current_time()`
- **Purpose**: Get current date and time
- **Example**: `get_current_time()`

#### Calculator
- **Function**: `calculate(expression)`
- **Purpose**: Perform mathematical calculations
- **Example**: `calculate("15 * 23 + 45")`

## 🧠 Advanced Features

### Deep Planning and Task Management

The agent automatically uses structured planning for complex tasks:

```bash
# Multi-step task with automatic planning
uv run python cli.py "Research the latest Python 3.13 features, write a summary report, and create a presentation outline"

# Explicit planning request
uv run python cli.py "Create a plan to organize my daily tasks and help me implement it"

# Task delegation example
uv run python cli.py "I need to research AI developments, calculate some metrics, and get current time. Please plan and execute these tasks."
```

The agent will:
1. **Create a structured todo list** using `write_todos` for complex tasks
2. **Track progress** by updating task status (pending → in_progress → completed)
3. **Use filesystem tools** to store intermediate results and reports
4. **Delegate tasks** to sub-agents when appropriate
5. **Show real-time progress** through streaming output
6. **Display tool usage** with `--show-tools` flag for detailed planning visibility
7. **Show tool inputs and outputs** for complete transparency in verbose mode

### Streaming Responses

```python
# Synchronous streaming
for chunk in agent.stream_chat("Tell me about quantum computing"):
    print(chunk, end="", flush=True)

# Asynchronous streaming
async for chunk in agent.astream_chat("Explain machine learning"):
    print(chunk, end="", flush=True)
```

### Long-term Memory

```python
from deepagent import DeepAgent

agent = DeepAgent(
    model_name="llama3.2:3b",
    use_longterm_memory=True  # Enables persistent memory
)
```

### Custom Tools

```python
from langchain_core.tools import tool

@tool
def custom_tool(input_text: str) -> str:
    """Custom tool description."""
    return f"Processed: {input_text}"

agent = DeepAgent(
    model_name="llama3.2:3b",
    tools=[custom_tool]
)
```

## 📁 Project Structure

```
deepagent/
├── src/
│   └── deepagent/
│       ├── __init__.py       # Package initialization
│       ├── agent.py          # Main agent implementation
│       └── tools.py          # Custom tools (web search, calculator, etc.)
├── config.py                 # Configuration settings and environment variables
├── cli.py                    # Command-line interface (main entry point)
├── setup.py                  # Setup and validation script
├── pyproject.toml            # Project dependencies
├── .env                      # Environment variables (create this)
└── README.md                 # This file
```

## 🔍 Troubleshooting

### Common Issues

1. **Ollama not running:**
   ```bash
   ollama serve
   ```

2. **Model not found:**
   ```bash
   ollama pull llama3.2:3b  # or your configured model
   ```

3. **Connection refused:**
   - Check if Ollama is running on the correct port
   - Verify the `OLLAMA_BASE_URL` in your `.env` file

4. **Web search not working:**
   - Check your internet connection
   - Verify DuckDuckGo is accessible

5. **Agent seems stuck/hanging:**
   - Use streaming mode to see progress: `uv run python cli.py "your query"`
   - Try non-streaming mode: `uv run python cli.py "your query" --no-stream`

### Debug Mode

For programmatic debugging, enable logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = DeepAgent()
```

Or use the CLI's interactive mode for step-by-step debugging:

```bash
uv run python cli.py
# Then use the interactive mode to test queries step by step
```

### Performance Tips

1. **Use streaming mode** for long operations to see progress
2. **Start with simple queries** before complex web searches
3. **Use the CLI mode** for interactive usage
4. **Check configuration** with `uv run python cli.py --config`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Deep Agents](https://github.com/langchain-ai/deepagents) - The core framework
- [Ollama](https://ollama.ai/) - Local LLM processing
- [DuckDuckGo](https://duckduckgo.com/) - Web search capabilities
- [LangChain](https://langchain.com/) - LLM framework

## 📚 Resources

- [Deep Agents Documentation](https://github.com/langchain-ai/deepagents)
- [Ollama Documentation](https://ollama.ai/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [DuckDuckGo Search API](https://pypi.org/project/duckduckgo-search/)
