"""MCP Client for connecting to MCP servers."""
import asyncio
from typing import Any, Dict, List, Optional
from contextlib import AsyncExitStack

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
except ImportError:
    print("Warning: MCP library not installed. Install with: pip install mcp")
    ClientSession = None
    StdioServerParameters = None
    stdio_client = None


class MCPClient:
    """Client for interacting with MCP servers."""
    
    def __init__(self, server_configs: Dict[str, Dict[str, Any]]):
        """
        Initialize MCP client with server configurations.
        
        Args:
            server_configs: Dictionary of server name -> server config
        """
        self.server_configs = server_configs
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        
    async def connect(self):
        """Connect to all configured MCP servers."""
        if not self.server_configs:
            print("No MCP servers configured.")
            return
            
        for server_name, config in self.server_configs.items():
            try:
                server_params = StdioServerParameters(
                    command=config["command"],
                    args=config.get("args", []),
                    env=config.get("env")
                )
                
                stdio_transport = await self.exit_stack.enter_async_context(
                    stdio_client(server_params)
                )
                read, write = stdio_transport
                session = await self.exit_stack.enter_async_context(
                    ClientSession(read, write)
                )
                
                await session.initialize()
                self.sessions[server_name] = session
                print(f"✓ Connected to MCP server: {server_name}")
                
            except Exception as e:
                print(f"✗ Failed to connect to {server_name}: {e}")
    
    async def disconnect(self):
        """Disconnect from all MCP servers."""
        await self.exit_stack.aclose()
        self.sessions.clear()
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools from connected servers."""
        all_tools = []
        
        for server_name, session in self.sessions.items():
            try:
                response = await session.list_tools()
                for tool in response.tools:
                    tool_info = {
                        "server": server_name,
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.inputSchema
                    }
                    all_tools.append(tool_info)
            except Exception as e:
                print(f"Error listing tools from {server_name}: {e}")
                
        return all_tools
    
    async def call_tool(self, server_name: str, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on a specific MCP server.
        
        Args:
            server_name: Name of the server
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")
            
        session = self.sessions[server_name]
        try:
            result = await session.call_tool(tool_name, arguments)
            return result
        except Exception as e:
            raise Exception(f"Error calling tool {tool_name}: {e}")
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """List all available resources from connected servers."""
        all_resources = []
        
        for server_name, session in self.sessions.items():
            try:
                response = await session.list_resources()
                for resource in response.resources:
                    resource_info = {
                        "server": server_name,
                        "uri": resource.uri,
                        "name": resource.name,
                        "description": resource.description,
                        "mimeType": resource.mimeType
                    }
                    all_resources.append(resource_info)
            except Exception as e:
                print(f"Error listing resources from {server_name}: {e}")
                
        return all_resources
    
    async def read_resource(self, server_name: str, uri: str) -> Any:
        """
        Read a resource from a specific MCP server.
        
        Args:
            server_name: Name of the server
            uri: Resource URI
            
        Returns:
            Resource contents
        """
        if server_name not in self.sessions:
            raise ValueError(f"Server {server_name} not connected")
            
        session = self.sessions[server_name]
        try:
            result = await session.read_resource(uri)
            return result
        except Exception as e:
            raise Exception(f"Error reading resource {uri}: {e}")


