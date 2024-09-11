# Discord Dreams - AI Roleplay Bot

So, you want to make an AI roleplay bot for Discord? Here's one. It's called Discord Dreams. It does stuff.

## Features

- **Multiple Characters**: Create as many AI characters as you want. Go nuts.
- **AI Model Switching**: Use Claude, OpenRouter, or LMStudio. Choose your poison.
- **Text-to-Speech**: Make your AI talk. Revolutionary, I know.
- **Image Generation**: Your AI can send selfies. Because apparently that's a thing now.
- **Conversation Management**: Edit or delete conversation history. Useful for when your AI says something stupid.
- **Character Customization**: Adjust your AI's personality. Make it as annoying as you want.  Or.. whatever.

## Prerequisites

Here's what you need. Don't blame me if you can't figure it out:

- Python 3.7+
- Discord Bot Token
- API keys for Anthropic, OpenRouter, ElevenLabs, and Replicate
- A Language Model (LLM)
- ElevenLabs voices
- Selfie and face files for Stable Diffusion
- A system prompt

## Character Setup

1. Find `characters.py`. Edit it.
2. Set up characters like this:

   ```python
   "character_name": {
       "system_prompt": "Character description goes here.",
       "image_prompt": "How the character looks, I guess.",
       "tts_url": "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID_HERE",
       "source_faces_folder": "path/to/faces/folder",
       "voice_settings": {
           "stability": 0.4,
           "similarity_boost": 0.45,
           "style": 0.5
       }
   }
   ```

3. Replace VOICE_ID_HERE with an ElevenLabs voice ID. Try not to pick something too annoying.

## Installation

1. Clone the repo:
   ```
   git clone https://github.com/nai-research/discord-dreams.git
   cd discord-dreams
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your config:
   - Make a `.env` file in the root directory
   - Put your API keys and stuff in it:
     ```
     DISCORD_BOT_TOKEN=your_discord_bot_token
     DISCORD_USER_ID=your_discord_user_id
     OPENROUTER_KEY=your_openrouter_api_key
     OPENROUTER_HTTP_REFERER=your_openrouter_http_referer
     ANTHROPIC_API_KEY=your_anthropic_api_key
     ELEVENLABS_API_KEY=your_elevenlabs_api_key
     REPLICATE_API_TOKEN=your_replicate_api_token
     DEFAULT_LLM=anthropic
     ```

## Usage

1. Start the bot:
   ```
   python main.py
   ```

2. Commands:
   - `!help` - Shows commands. You'll probably need this.
   - `!llm` - Switch AI models
   - `!claude`, `!openrouter`, `!lmstudio` - Switch to specific models
   - `!tts` - Toggle text-to-speech
   - `!narration` - Toggle narration
   - `!say` - Make the AI say something
   - `!selfie` - Generate a profile pic
   - `!video` - Make a talking animation
   - `!talker` - More advanced video generation
   - `!delete` - Delete the last message
   - `!edit` - Edit a message
   - `!resume` - Continue a previous conversation
   - `!set_voice`, `!get_voice` - Manage AI voice
   - `!restart` - Restart the bot
   - `!quit` - Stop the bot

## Technical Details

- Uses Discord.py
- Asyncio for concurrent operations
- Error handling and logging
- Modular design
- Multiple AI model support
- Video generation with Replicate's API
- Environment variables for configuration

## Contributing

If you want to contribute, go ahead. Just don't break anything.



That's it. Have fun with your AI roleplay bot, I guess.