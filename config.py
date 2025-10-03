"""Configuration settings for the MCP AI Agent."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration class for agent settings."""
    
    # Anthropic API settings
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20241022")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # MCP Server configurations
    MCP_SERVERS = {
        # Enuygun - Seyahat aramaları (uçak, otel, otobüs, araba)
        "enuygun": {
            "command": "npx",
            "args": ["-y", "mcp-remote", "https://mcp.enuygun.com/mcp"]
        }
        
        # İsterseniz diğer sunucuları da ekleyebilirsiniz:
        # "filesystem": {
        #     "command": "npx",
        #     "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/abdullahö/Desktop"]
        # }
    }
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )

