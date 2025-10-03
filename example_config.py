"""Example MCP server configurations."""

# Example MCP server configurations
# Copy these to config.py and modify as needed

EXAMPLE_MCP_SERVERS = {
    # Filesystem server - access local files
    "filesystem": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/abdullahö/Desktop"]
    },
    
    # GitHub server - access GitHub repositories
    # "github": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-github"],
    #     "env": {
    #         "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
    #     }
    # },
    
    # PostgreSQL server - interact with PostgreSQL databases
    # "postgres": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:password@localhost/dbname"]
    # },
    
    # Puppeteer server - web scraping and browser automation
    # "puppeteer": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    # },
    
    # SQLite server - interact with SQLite databases
    # "sqlite": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "./database.db"]
    # },
    
    # Memory server - persistent memory for the agent
    # "memory": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-memory"]
    # },
    
    # Brave Search server - web search capabilities
    # "brave-search": {
    #     "command": "npx",
    #     "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    #     "env": {
    #         "BRAVE_API_KEY": "your_api_key_here"
    #     }
    # }
}


