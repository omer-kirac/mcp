"""FastAPI application for MCP AI Agent."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
import uvicorn
import signal
import sys

from agent import MCPAgent
from config import Config

# Global agent instance
agent = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    global agent
    
    # Startup
    try:
        Config.validate()
        agent = MCPAgent(Config)
        await agent.initialize()
        print("✓ Agent initialized successfully")
    except ValueError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Startup Error: {e}")
        sys.exit(1)
    
    yield
    
    # Shutdown
    try:
        if agent:
            await agent.shutdown()
            print("✓ Agent shutdown successfully")
    except Exception as e:
        print(f"Shutdown Error: {e}")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="MCP AI Agent API",
    description="API for interacting with MCP AI Agent",
    version="1.0.0",
    lifespan=lifespan
)

class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    clear_history: Optional[bool] = False

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the AI agent.
    
    Args:
        request: ChatRequest object containing the message and clear_history flag
        
    Returns:
        ChatResponse object containing the agent's response
    """
    try:
        if request.clear_history:
            agent.clear_history()
            
        response = await agent.chat(request.message)
        return ChatResponse(response=response)
        
    except Exception as e:
        import traceback
        error_detail = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(f"Chat endpoint error: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools")
async def list_tools():
    """
    List available MCP tools.
    
    Returns:
        List of available tools
    """
    return {"tools": agent.available_tools}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent_ready": agent is not None}

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\nShutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")


