#!/usr/bin/env python3
"""Command-line interface for Deep Agent with Ollama."""

import argparse
import sys
import asyncio
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from deepagent import DeepAgent
from config import Config


def print_banner():
    """Print the application banner."""
    print("🤖 Deep Agent with Ollama CLI")
    print("=" * 50)


async def interactive_mode(agent: DeepAgent):
    """Interactive chat mode."""
    print("💬 Interactive Chat Mode")
    print("Type 'quit' to exit, 'help' for commands")
    print("-" * 30)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print("Available commands:")
                print("- quit/exit/q: Exit the chat")
                print("- help: Show this help message")
                print("- config: Show current configuration")
                print("- Any other text: Chat with the agent")
                continue
            elif user_input.lower() == 'config':
                Config.print_config()
                continue
            elif not user_input:
                continue
            
            print("🤖 Agent: ", end="", flush=True)
            
            # Stream the response
            async for chunk in agent.astream_chat(user_input):
                print(chunk, end="", flush=True)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")


async def single_query_mode(agent: DeepAgent, query: str, stream: bool = True):
    """Single query mode."""
    print(f"🔍 Query: {query}")
    print("-" * 30)
    
    try:
        if stream:
            print("🤖 Response: ", end="", flush=True)
            async for chunk in agent.astream_chat(query):
                print(chunk, end="", flush=True)
            print()
        else:
            response = await agent.achat(query)
            print(f"🤖 Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Deep Agent with Ollama CLI")
    parser.add_argument(
        "query", 
        nargs="?", 
        help="Query to ask the agent (if not provided, enters interactive mode)"
    )
    parser.add_argument(
        "--model", 
        default=Config.OLLAMA_MODEL,
        help=f"Ollama model to use (default: {Config.OLLAMA_MODEL})"
    )
    parser.add_argument(
        "--base-url", 
        default=Config.OLLAMA_BASE_URL,
        help=f"Ollama base URL (default: {Config.OLLAMA_BASE_URL})"
    )
    parser.add_argument(
        "--no-stream", 
        action="store_true", 
        help="Disable streaming responses"
    )
    parser.add_argument(
        "--show-tools", 
        action="store_true", 
        help="Show tool usage and planning steps in streaming mode"
    )
    parser.add_argument(
        "--config", 
        action="store_true",
        help="Show configuration and exit"
    )
    parser.add_argument(
        "--validate", 
        action="store_true",
        help="Validate configuration and exit"
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Handle special commands
    if args.config:
        Config.print_config()
        return
    
    if args.validate:
        try:
            Config.validate()
            print("✅ Configuration is valid")
        except ValueError as e:
            print(f"❌ Configuration validation failed: {e}")
            sys.exit(1)
        return
    
    # Create the agent
    try:
        print(f"🔄 Initializing agent with model: {args.model}")
        agent = DeepAgent(
            model_name=args.model,
            base_url=args.base_url,
            use_longterm_memory=Config.USE_LONGTERM_MEMORY,
            system_prompt=Config.CUSTOM_SYSTEM_PROMPT,
            show_tools=args.show_tools,
        )
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)
    
    # Run the appropriate mode
    if args.query:
        # Single query mode
        asyncio.run(single_query_mode(agent, args.query, not args.no_stream))
    else:
        # Interactive mode
        asyncio.run(interactive_mode(agent))


if __name__ == "__main__":
    main()
