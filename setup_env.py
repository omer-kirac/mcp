"""Helper script to set up the environment."""
import os
from pathlib import Path


def create_env_file():
    """Create a .env file with example configuration."""
    env_content = """# Anthropic API Key
ANTHROPIC_API_KEY=sk-ant-api03-Gg4aCA3owakTlcPdp2F
Va9vfaPXelnaIVzzcEIgY9s24bmVx97FT
mkm4ueQVGtJWDgBYLcvq3ofC-7fod
nK2Hg-l3zPYwAA 

# Agent Settings
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.7
"""
    
    env_path = Path(".env")
    
    if env_path.exists():
        response = input(".env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env file creation.")
            return
    
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(env_content)
    
    print("✓ .env file created successfully!")
    print("\nPlease edit .env and add your Anthropic API key.")
    print("You can get an API key from: https://console.anthropic.com/")


def main():
    """Main setup function."""
    print("🤖 MCP AI Agent Setup\n")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        return
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Create .env file
    create_env_file()
    
    print("\n📋 Next steps:")
    print("1. Edit .env file and add your ANTHROPIC_API_KEY")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Edit config.py and add your MCP servers")
    print("4. Run the agent: python main.py")
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()


