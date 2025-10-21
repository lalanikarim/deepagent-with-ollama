"""Deep Agent with Ollama implementation using custom tools."""

import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage
from deepagents import create_deep_agent
from langgraph.store.memory import InMemoryStore

from tools import web_search, get_current_time, calculate
from config import Config


class DeepAgent:
    """A deep agent with Ollama implementation using custom tools."""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        tools: Optional[List] = None,
        system_prompt: Optional[str] = None,
        use_longterm_memory: Optional[bool] = None,
        show_tools: Optional[bool] = None,
    ):
        """
        Initialize the Deep Agent.
        
        Args:
            model_name: Name of the Ollama model to use (defaults to OLLAMA_MODEL env var)
            base_url: Base URL for Ollama API (defaults to OLLAMA_BASE_URL env var)
            tools: Custom tools to add to the agent
            system_prompt: Custom system prompt
            use_longterm_memory: Whether to use long-term memory (defaults to USE_LONGTERM_MEMORY env var)
            show_tools: Whether to show tool usage in streaming mode (defaults to False)
        """
        # Use provided values or config values (no defaults)
        self.model_name = model_name if model_name is not None else Config.OLLAMA_MODEL
        self.base_url = base_url if base_url is not None else Config.OLLAMA_BASE_URL
        self.use_longterm_memory = use_longterm_memory if use_longterm_memory is not None else Config.USE_LONGTERM_MEMORY
        self.show_tools = show_tools if show_tools is not None else False
        
        # Initialize the Ollama model
        self.llm = ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.1,
        )
        
        # Default tools
        default_tools = [web_search, get_current_time, calculate]
        
        # Combine default and custom tools
        self.tools = default_tools + (tools or [])
        
        # Default system prompt
        if not system_prompt:
            system_prompt = Config.CUSTOM_SYSTEM_PROMPT or self._get_default_system_prompt()
        
        # Create the deep agent
        agent_kwargs = {
            "model": self.llm,
            "tools": self.tools,
            "system_prompt": system_prompt,
        }
        
        # Add long-term memory if requested
        if self.use_longterm_memory:
            store = InMemoryStore()
            agent_kwargs["store"] = store
            agent_kwargs["use_longterm_memory"] = True
        
        self.agent = create_deep_agent(**agent_kwargs)
    
    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the agent."""
        return """You are a helpful AI assistant with access to web search, time information, calculation capabilities, and advanced planning tools.

Key capabilities:
- Web search: Use the web_search tool to find current information on any topic
- Time awareness: Use get_current_time to know the current date and time
- Calculations: Use calculate to perform mathematical operations
- Task planning: Use write_todos to create and manage structured task lists for complex work
- File operations: Use filesystem tools (ls, read_file, write_file, edit_file) to store and organize information
- Task delegation: Use task tool to launch sub-agents for complex, independent tasks

Planning and Task Management Guidelines:
1. For complex tasks (3+ steps), ALWAYS start by using write_todos to create a structured plan
2. Mark your first task as in_progress immediately when creating the todo list
3. Update task status in real-time as you work (pending → in_progress → completed)
4. Break down complex tasks into smaller, manageable steps
5. Use the task tool to delegate independent complex tasks to sub-agents
6. Use filesystem tools to store intermediate results and organize information

Research Guidelines:
1. Always use web search when you need current information or facts
2. Be thorough in your research - use multiple searches if needed
3. Cite your sources when providing information from web searches
4. Use filesystem tools to store and organize research findings

General Guidelines:
1. Be helpful, accurate, and transparent about your capabilities
2. Demonstrate thoroughness by planning complex tasks upfront
3. Show progress by updating task lists as you work
4. Use appropriate tools for each type of task

When you don't know something or need current information, use web search to find it."""
    
    def chat(self, message: str) -> str:
        """
        Chat with the agent.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        try:
            # Create the input for the agent
            inputs = {
                "messages": [{"role": "user", "content": message}]
            }
            
            # Get response from the agent
            response = self.agent.invoke(inputs)
            
            # Extract the final message
            if "messages" in response and response["messages"]:
                final_message = response["messages"][-1]
                if isinstance(final_message, AIMessage):
                    return final_message.content
            
            return "I apologize, but I couldn't generate a proper response."
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def achat(self, message: str) -> str:
        """
        Async chat with the agent.
        
        Args:
            message: User message
            
        Returns:
            Agent response
        """
        try:
            # Create the input for the agent
            inputs = {
                "messages": [{"role": "user", "content": message}]
            }
            
            # Get response from the agent
            response = await self.agent.ainvoke(inputs)
            
            # Extract the final message
            if "messages" in response and response["messages"]:
                final_message = response["messages"][-1]
                if isinstance(final_message, AIMessage):
                    return final_message.content
            
            return "I apologize, but I couldn't generate a proper response."
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def stream_chat(self, message: str):
        """
        Stream chat responses from the agent.
        
        Args:
            message: User message
            
        Yields:
            Chunks of the agent response
        """
        try:
            # Create the input for the agent
            inputs = {
                "messages": [{"role": "user", "content": message}]
            }
            
            # Stream response from the agent with values mode (reliable)
            for chunk in self.agent.stream(inputs, stream_mode="values"):
                if "messages" in chunk and chunk["messages"]:
                    final_message = chunk["messages"][-1]
                    if isinstance(final_message, AIMessage):
                        # Check if this message has tool calls to show planning steps
                        if self.show_tools and hasattr(final_message, 'tool_calls') and final_message.tool_calls:
                            for tool_call in final_message.tool_calls:
                                # Show tool name and inputs
                                tool_name = tool_call['name']
                                tool_args = tool_call.get('args', {})
                                args_str = ", ".join([f"{k}={v}" for k, v in tool_args.items()])
                                yield f"\n🔧 Using {tool_name}({args_str})\n"
                        
                        # Check for tool results in the message history
                        if self.show_tools and "messages" in chunk:
                            for msg in chunk["messages"]:
                                if hasattr(msg, 'name') and hasattr(msg, 'content') and msg.name:
                                    # This is a tool result message
                                    tool_output = msg.content
                                    if tool_output and len(tool_output) > 100:
                                        tool_output = tool_output[:100] + "..."
                                    yield f"📤 {msg.name} output: {tool_output}\n"
                        
                        # Yield the content
                        if final_message.content:
                            yield final_message.content
                        
        except Exception as e:
            yield f"Error: {str(e)}"
    
    async def astream_chat(self, message: str):
        """
        Async stream chat responses from the agent.
        
        Args:
            message: User message
            
        Yields:
            Chunks of the agent response
        """
        try:
            # Create the input for the agent
            inputs = {
                "messages": [{"role": "user", "content": message}]
            }
            
            # Stream response from the agent with values mode (reliable)
            async for chunk in self.agent.astream(inputs, stream_mode="values"):
                if "messages" in chunk and chunk["messages"]:
                    final_message = chunk["messages"][-1]
                    if isinstance(final_message, AIMessage):
                        # Check if this message has tool calls to show planning steps
                        if self.show_tools and hasattr(final_message, 'tool_calls') and final_message.tool_calls:
                            for tool_call in final_message.tool_calls:
                                # Show tool name and inputs
                                tool_name = tool_call['name']
                                tool_args = tool_call.get('args', {})
                                args_str = ", ".join([f"{k}={v}" for k, v in tool_args.items()])
                                yield f"\n🔧 Using {tool_name}({args_str})\n"
                        
                        # Check for tool results in the message history
                        if self.show_tools and "messages" in chunk:
                            for msg in chunk["messages"]:
                                if hasattr(msg, 'name') and hasattr(msg, 'content') and msg.name:
                                    # This is a tool result message
                                    tool_output = msg.content
                                    if tool_output and len(tool_output) > 100:
                                        tool_output = tool_output[:100] + "..."
                                    yield f"📤 {msg.name} output: {tool_output}\n"
                        
                        # Yield the content
                        if final_message.content:
                            yield final_message.content
                        
        except Exception as e:
            yield f"Error: {str(e)}"
