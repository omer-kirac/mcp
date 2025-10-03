"""Logging utilities for LLM prompts and responses."""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax


class PromptLogger:
    """Logger for LLM prompts and responses."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize the prompt logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.console = Console()
        
        # Create session log file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_file = self.log_dir / f"session_{timestamp}.jsonl"
        self.text_log_file = self.log_dir / f"session_{timestamp}.txt"
        
    def _serialize_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert messages to JSON-serializable format."""
        serialized = []
        for msg in messages:
            serialized_msg = {
                "role": msg.get("role", ""),
                "content": self._serialize_content(msg.get("content"))
            }
            serialized.append(serialized_msg)
        return serialized
    
    def _serialize_content(self, content: Any) -> Any:
        """Convert content to JSON-serializable format."""
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            return [self._serialize_content(item) for item in content]
        elif isinstance(content, dict):
            return {k: self._serialize_content(v) for k, v in content.items()}
        elif hasattr(content, 'text'):
            # Handle TextBlock objects
            return content.text
        elif hasattr(content, 'model_dump'):
            # Handle Pydantic models
            return content.model_dump()
        elif hasattr(content, '__dict__'):
            # Handle other objects with __dict__
            return str(content)
        else:
            return str(content)
    
    def log_prompt(
        self, 
        system_message: str,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float,
        max_tokens: int,
        tools: List[Dict[str, Any]] = None
    ):
        """
        Log the prompt sent to LLM.
        
        Args:
            system_message: System message
            messages: Conversation messages
            model: Model name
            temperature: Temperature setting
            max_tokens: Max tokens setting
            tools: Available tools (optional)
        """
        timestamp = datetime.now().isoformat()
        
        # Serialize messages to JSON-compatible format
        serialized_messages = self._serialize_messages(messages)
        
        log_entry = {
            "timestamp": timestamp,
            "type": "prompt",
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_message": system_message,
            "messages": serialized_messages,
            "tools_count": len(tools) if tools else 0
        }
        
        # Write to JSONL file
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        # Write to text log file
        with open(self.text_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"PROMPT - {timestamp}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Model: {model}\n")
            f.write(f"Temperature: {temperature}\n")
            f.write(f"Max Tokens: {max_tokens}\n")
            f.write(f"Tools Available: {len(tools) if tools else 0}\n\n")
            f.write(f"System Message:\n{system_message}\n\n")
            f.write(f"Conversation History:\n")
            for i, msg in enumerate(serialized_messages):
                f.write(f"  [{i+1}] {msg['role'].upper()}:\n")
                if isinstance(msg['content'], str):
                    f.write(f"    {msg['content']}\n")
                else:
                    f.write(f"    {json.dumps(msg['content'], ensure_ascii=False, indent=2)}\n")
            f.write("\n")
        
        # Console output
        self.console.print(Panel(
            f"[bold cyan]📤 PROMPT GÖNDERİLDİ[/bold cyan]\n\n"
            f"[yellow]Model:[/yellow] {model}\n"
            f"[yellow]Sıcaklık:[/yellow] {temperature}\n"
            f"[yellow]Maksimum Token:[/yellow] {max_tokens}\n"
            f"[yellow]Araç Sayısı:[/yellow] {len(tools) if tools else 0}\n"
            f"[yellow]Mesaj Sayısı:[/yellow] {len(messages)}",
            title="🤖 LLM İsteği",
            border_style="cyan"
        ))
        
    def log_response(
        self,
        response: Any,
        stop_reason: str,
        usage: Dict[str, int] = None
    ):
        """
        Log the response received from LLM.
        
        Args:
            response: LLM response object
            stop_reason: Why the response stopped
            usage: Token usage information
        """
        timestamp = datetime.now().isoformat()
        
        # Extract content from response
        content_blocks = []
        text_content = ""
        tool_uses = []
        
        for block in response.content:
            if hasattr(block, 'text'):
                text_content += block.text
                content_blocks.append({
                    "type": "text",
                    "text": block.text
                })
            elif hasattr(block, 'type') and block.type == "tool_use":
                tool_uses.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
                content_blocks.append({
                    "type": "tool_use",
                    "name": block.name,
                    "id": block.id,
                    "input": block.input
                })
        
        log_entry = {
            "timestamp": timestamp,
            "type": "response",
            "stop_reason": stop_reason,
            "content": content_blocks,
            "usage": usage if usage else {}
        }
        
        # Write to JSONL file
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        # Write to text log file
        with open(self.text_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'-'*80}\n")
            f.write(f"RESPONSE - {timestamp}\n")
            f.write(f"{'-'*80}\n")
            f.write(f"Stop Reason: {stop_reason}\n")
            if usage:
                f.write(f"Usage: {json.dumps(usage, ensure_ascii=False)}\n")
            f.write(f"\nContent:\n")
            
            if text_content:
                f.write(f"\nMetin:\n{text_content}\n")
            
            if tool_uses:
                f.write(f"\nAraç Kullanımları:\n")
                for tool in tool_uses:
                    f.write(f"  - {tool['name']}\n")
                    f.write(f"    Input: {json.dumps(tool['input'], ensure_ascii=False, indent=4)}\n")
            f.write("\n")
        
        # Console output
        usage_text = ""
        if usage:
            usage_text = (
                f"\n[yellow]Token Kullanımı:[/yellow]\n"
                f"  • Giriş: {usage.get('input_tokens', 0)}\n"
                f"  • Çıkış: {usage.get('output_tokens', 0)}\n"
                f"  • Toplam: {usage.get('input_tokens', 0) + usage.get('output_tokens', 0)}"
            )
        
        tool_text = ""
        if tool_uses:
            tool_text = f"\n[yellow]Kullanılan Araçlar:[/yellow] {', '.join([t['name'] for t in tool_uses])}"
        
        self.console.print(Panel(
            f"[bold green]📥 YANIT ALINDI[/bold green]\n\n"
            f"[yellow]Duruş Nedeni:[/yellow] {stop_reason}"
            f"{tool_text}"
            f"{usage_text}",
            title="🤖 LLM Yanıtı",
            border_style="green"
        ))
        
        if text_content and len(text_content) > 0:
            self.console.print(Panel(
                text_content,
                title="💬 Yanıt Metni",
                border_style="blue"
            ))
    
    def log_tool_execution(
        self,
        tool_name: str,
        tool_input: Dict[str, Any],
        result: Any,
        success: bool = True
    ):
        """
        Log tool execution.
        
        Args:
            tool_name: Name of the tool
            tool_input: Tool input parameters
            result: Tool execution result
            success: Whether execution was successful
        """
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "type": "tool_execution",
            "tool_name": tool_name,
            "tool_input": tool_input,
            "result": str(result),
            "success": success
        }
        
        # Write to JSONL file
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        
        # Write to text log file
        with open(self.text_log_file, "a", encoding="utf-8") as f:
            f.write(f"\n{'~'*80}\n")
            f.write(f"TOOL EXECUTION - {timestamp}\n")
            f.write(f"{'~'*80}\n")
            f.write(f"Tool: {tool_name}\n")
            f.write(f"Success: {success}\n")
            f.write(f"Input: {json.dumps(tool_input, ensure_ascii=False, indent=2)}\n")
            f.write(f"Result: {str(result)[:500]}...\n\n")  # Limit result length
        
        # Console output
        status = "✓" if success else "✗"
        color = "green" if success else "red"
        self.console.print(f"[{color}]{status} Araç Çalıştırıldı: {tool_name}[/{color}]")
    
    def get_log_location(self) -> str:
        """Get the location of log files."""
        return str(self.log_dir.absolute())

