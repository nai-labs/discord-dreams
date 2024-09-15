#!/bin/bash

echo "Discord Dreams Installer for macOS"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Prompt for API keys
echo "Please enter the following API keys:"
read -p "Discord Bot Token: " discord_token
read -p "Discord User ID: " discord_user_id
read -p "OpenRouter API Key: " openrouter_key
read -p "OpenRouter HTTP Referer (https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=YOUR_PERMISSIONS&scope=bot): " openrouter_referer
read -p "Anthropic API Key: " anthropic_key
read -p "ElevenLabs API Key: " elevenlabs_key
read -p "Replicate API Token: " replicate_token

# Create .env file
cat > .env << EOL
DISCORD_BOT_TOKEN=${discord_token}
DISCORD_USER_ID=${discord_user_id}
OPENROUTER_KEY=${openrouter_key}
OPENROUTER_HTTP_REFERER=${openrouter_referer}
ANTHROPIC_API_KEY=${anthropic_key}
ELEVENLABS_API_KEY=${elevenlabs_key}
REPLICATE_API_TOKEN=${replicate_token}
DEFAULT_LLM=anthropic
EOL

echo ""
echo "Installation complete! To run Discord Dreams, follow these steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the bot: python main.py"
echo ""
echo "Open Discord, and enjoy using Discord Dreams!"