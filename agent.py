"""Main AI Agent with MCP integration."""
import asyncio
from typing import List, Dict, Any, Optional
from anthropic import Anthropic
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from config import Config
from mcp_client import MCPClient
from logger import PromptLogger


class MCPAgent:
    """AI Agent with MCP (Model Context Protocol) integration."""
    
    def __init__(self, config: Config):
        """
        Initialize the MCP Agent.
        
        Args:
            config: Configuration object
        """
        self.config = config
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.mcp_client = MCPClient(config.MCP_SERVERS)
        self.console = Console()
        self.conversation_history: List[Dict[str, Any]] = []
        self.available_tools: List[Dict[str, Any]] = []
        self.logger = PromptLogger()  # Initialize prompt logger
        
    async def initialize(self):
        """Initialize the agent by connecting to MCP servers."""
        self.console.print("[bold cyan]🤖 Initializing MCP AI Agent...[/bold cyan]")
        
        # Show log location
        self.console.print(f"[cyan]📝 Log dosyaları: {self.logger.get_log_location()}[/cyan]")
        
        # Connect to MCP servers
        await self.mcp_client.connect()
        
        # Load available tools
        self.available_tools = await self.mcp_client.list_tools()
        
        if self.available_tools:
            self.console.print(f"[green]✓ Loaded {len(self.available_tools)} tools from MCP servers[/green]")
            for tool in self.available_tools:
                self.console.print(f"  • {tool['server']}.{tool['name']}: {tool['description']}")
        else:
            self.console.print("[yellow]⚠ No MCP tools available[/yellow]")
            
    async def shutdown(self):
        """Shutdown the agent and disconnect from MCP servers."""
        await self.mcp_client.disconnect()
        self.console.print("[cyan]👋 Agent shutdown complete[/cyan]")
        
    def _convert_tools_to_anthropic_format(self) -> List[Dict[str, Any]]:
        """Convert MCP tools to Anthropic API format."""
        anthropic_tools = []
        
        for tool in self.available_tools:
            anthropic_tool = {
                "name": f"{tool['server']}_{tool['name']}",
                "description": tool['description'] or "No description available",
                "input_schema": tool['inputSchema']
            }
            anthropic_tools.append(anthropic_tool)
            
        return anthropic_tools
    
    async def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Execute a tool call.
        
        Args:
            tool_name: Full tool name (server_toolname)
            tool_input: Tool arguments
            
        Returns:
            Tool execution result
        """
        # Parse server and tool name
        parts = tool_name.split('_', 1)
        if len(parts) != 2:
            error_result = {"error": f"Invalid tool name format: {tool_name}"}
            self.logger.log_tool_execution(tool_name, tool_input, error_result, success=False)
            return error_result
            
        server_name, actual_tool_name = parts
        
        try:
            result = await self.mcp_client.call_tool(server_name, actual_tool_name, tool_input)
            self.logger.log_tool_execution(tool_name, tool_input, result, success=True)
            return result
        except Exception as e:
            error_result = {"error": str(e)}
            self.logger.log_tool_execution(tool_name, tool_input, error_result, success=False)
            return error_result
    
    async def chat(self, user_message: str) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            user_message: User's input message
            
        Returns:
            Agent's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare system message
        system_message = """You are a helpful AI assistant with access to various tools through the Model Context Protocol (MCP).
You can use these tools to help users accomplish their tasks. When a user asks for something that requires tool usage,
analyze the request and use the appropriate tools to fulfill it.

Always explain what you're doing and provide clear, helpful responses."""
        
        # Convert MCP tools to Anthropic format
        anthropic_tools = self._convert_tools_to_anthropic_format()
        
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Create API request parameters
            api_params = {
                "model": self.config.MODEL_NAME,
                "max_tokens": self.config.MAX_TOKENS,
                "temperature": self.config.TEMPERATURE,
                "system": system_message,
                "messages": self.conversation_history
            }
            
            # Add tools if available
            if anthropic_tools:
                api_params["tools"] = anthropic_tools
            
            # Log the prompt being sent
            self.logger.log_prompt(
                system_message=system_message,
                messages=self.conversation_history,
                model=self.config.MODEL_NAME,
                temperature=self.config.TEMPERATURE,
                max_tokens=self.config.MAX_TOKENS,
                tools=anthropic_tools
            )
            
            # Get response from Claude
            response = self.client.messages.create(**api_params)
            
            # Log the response received
            usage_info = {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
            self.logger.log_response(
                response=response,
                stop_reason=response.stop_reason,
                usage=usage_info
            )
            
            # Check if we need to process tool calls
            if response.stop_reason == "tool_use":
                # Add assistant's response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Process each tool use
                tool_results = []
                for content_block in response.content:
                    if content_block.type == "tool_use":
                        self.console.print(f"[yellow]🔧 Using tool: {content_block.name}[/yellow]")
                        
                        # Execute the tool
                        result = await self._execute_tool(content_block.name, content_block.input)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": content_block.id,
                            "content": str(result)
                        })
                
                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                
            elif response.stop_reason == "end_turn":
                # Extract final text response
                final_response = ""
                for content_block in response.content:
                    if hasattr(content_block, "text"):
                        final_response += content_block.text
                
                # Add to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                return final_response
            else:
                # Handle other stop reasons
                final_response = f"Unexpected stop reason: {response.stop_reason}"
                self.conversation_history.append({
                    "role": "assistant",
                    "content": final_response
                })
                return final_response
        
        return "Maximum iterations reached. Please try rephrasing your request."
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
        self.console.print("[cyan]🗑️  Conversation history cleared[/cyan]")


