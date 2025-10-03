"""Main entry point for the MCP AI Agent."""
import asyncio
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

from agent import MCPAgent
from config import Config


console = Console()


def print_welcome():
    """Print welcome message."""
    welcome_text = """
# 🤖 MCP AI Agent

Hoş geldiniz! Bu AI agent, Model Context Protocol (MCP) ile entegre edilmiştir.

**Komutlar:**
- Herhangi bir soru sorun veya görev verin
- `clear` - Konuşma geçmişini temizle
- `tools` - Mevcut araçları listele
- `help` - Yardım menüsü
- `exit` veya `quit` - Çıkış

Agent şu anda bağlı MCP sunucularındaki araçları kullanabilir.
    """
    console.print(Panel(Markdown(welcome_text), border_style="cyan"))


async def main():
    """Main application loop."""
    try:
        # Validate configuration
        Config.validate()
    except ValueError as e:
        console.print(f"[bold red]❌ Configuration Error:[/bold red] {e}")
        console.print("\n[yellow]Lütfen .env dosyanızı oluşturun ve ANTHROPIC_API_KEY değişkenini ayarlayın.[/yellow]")
        console.print("[yellow]Örnek için .env.example dosyasına bakın.[/yellow]")
        return
    
    # Initialize agent
    agent = MCPAgent(Config)
    
    try:
        await agent.initialize()
        print_welcome()
        
        # Main interaction loop
        while True:
            try:
                user_input = Prompt.ask("\n[bold cyan]Siz[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.lower() in ["exit", "quit", "çıkış"]:
                    console.print("[yellow]Görüşmek üzere! 👋[/yellow]")
                    break
                    
                elif user_input.lower() == "clear":
                    agent.clear_history()
                    continue
                    
                elif user_input.lower() == "tools":
                    if agent.available_tools:
                        console.print("\n[bold]Mevcut Araçlar:[/bold]")
                        for tool in agent.available_tools:
                            console.print(f"  • [cyan]{tool['server']}.{tool['name']}[/cyan]: {tool['description']}")
                    else:
                        console.print("[yellow]Henüz bağlı MCP sunucusu yok.[/yellow]")
                    continue
                    
                elif user_input.lower() == "help":
                    print_welcome()
                    continue
                
                # Get agent response
                console.print("\n[bold green]Agent[/bold green]:")
                response = await agent.chat(user_input)
                
                # Display response
                console.print(Panel(Markdown(response), border_style="green"))
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Kesintiye uğradı. Çıkmak için 'exit' yazın.[/yellow]")
                continue
                
            except Exception as e:
                console.print(f"[bold red]Hata:[/bold red] {e}")
                
    finally:
        await agent.shutdown()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program sonlandırıldı.[/yellow]")


