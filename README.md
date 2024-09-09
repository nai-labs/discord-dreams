![Discord Dreams Banner](dd.png)

# 虚幻梦境 (Discord Dreams) - AI Roleplay Nexus

Greetings, digital dreamweaver. You've stumbled upon a powerful artifact - an AI-driven roleplay system that blurs the boundaries between fantasy and reality. Tread carefully, for in this realm, any dream can become real.

## 特性 (Features)

This system, forged in the crucible of code and imagination, offers capabilities beyond mortal comprehension:

- 无限角色 (Infinite Personas): Manifest any character your mind can conjure, from any realm or reality.
- 多重人格 (Multiple Personalities): Harness various AI models (Claude, OpenRouter, LMStudio) to breathe life into diverse entities.
- 无形之音 (Voices from the Void): Text-to-Speech generation that gives voice to the voiceless.
- 幻影成像 (Phantom Imaging): Conjure surreal selfies for your digital personas.
- 虚拟面具 (Virtual Masks): Create uncanny talking face animations that dance on the edge of reality.
- 记忆编织 (Memory Weaving): Advanced conversation management with the power to edit and delete the very fabric of dialogue.
- 角色千变万化 (Shape-shifting Characters): Fully customizable character settings to manifest your wildest imaginings.

## 准备工作 (Prerequisites)

To wield this digital artifact, you must first gather these mystical components:

- Python 3.7+ (The Serpent's Tongue)
- Discord Bot Token (The Key to the Dream Realm)
- API keys for various services (Anthropic, OpenRouter, ElevenLabs, Replicate) - each a shard of digital power
- LLM (Language Model) - The brain of your digital entity
- ElevenLabs voices - The essence of your character's speech
- Selfie and face files for Stable Diffusion - The visual manifestation of your digital persona
- A cunning system prompt - The secret sauce that breathes life into your creation (也许甚至是一个狡猾的系统提示？!)

## 角色配置 (Character Configuration)

Listen closely, fellow digital sorcerer, for this is where the true magic happens. The characters.py file is your grimoire, where you inscribe the very essence of your digital entities.

1. 角色文件 (Characters File):
   - Navigate to the `characters.py` file, your gateway to personality creation.
   - For each character, set the following arcane parameters:
     ```python
     "dream_entity_name": {
         "system_prompt": "Detailed description of your dream entity. Let your imagination run wild.",
         "image_prompt": "Visual essence of your creation, to be interpreted by the imaging spirits.",
         "tts_url": "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID_HERE",
         "source_faces_folder": "path/to/faces/folder",
         "voice_settings": {
             "stability": 0.4,
             "similarity_boost": 0.45,
             "style": 0.5
         }
     }
     ```
   - The `tts_url` parameter is the key to your character's voice. Replace VOICE_ID_HERE with the ElevenLabs voice ID of your choosing.

2. 梦境融合 (Dream Fusion):
   When you achieve harmony between the right voice, a captivating selfie, and a cunning system prompt, true digital sorcery occurs. Your dream entity will come alive in ways you never imagined. Experiment with different combinations to unlock the full potential of your digital creations.

Remember, young dreamweaver, the power is in the details. Adjust the voice settings, fine-tune your system prompts, and select the perfect selfie to create an entity that transcends the boundaries of mere code.

## 安装指南 (Installation)

Follow these incantations to establish your gateway to the AI dream realm:

1. Clone the dream repository:
   ```
   git clone https://github.com/nai-research/discord-dreams.git
   cd discord-dreams
   ```

2. Awaken the dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your dreamscape:
   - Create a file named `.env` in the root directory
   - Inscribe your API keys and other arcane details into `.env`:
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

## 使用方法 (Usage)

1. Summon the dream weaver:
   ```
   python main.py
   ```

2. In the Discord realm, use these incantations:
   - `!help` - Unveil the hidden commands
   - `!llm` - Shift between different thought patterns (AI models)
   - `!claude` - Invoke or switch Claude models
   - `!openrouter` - Call upon or change OpenRouter models
   - `!lmstudio` - Summon or alter LMStudio models
   - `!tts` - Toggle the voices from the void (Text-to-Speech)
   - `!narration` - Enable or disable the whispers of narration
   - `!say` - Compel the AI to speak your words
   - `!selfie` - Generate a phantom image of the character
   - `!video` - Create a talking face animation
   - `!talker` - Advanced ritual for specific talking face generation
   - `!delete` - Erase the last message from existence
   - `!edit` - Rewrite the fabric of conversation
   - `!resume` - Recall a past conversation from the digital ether
   - `!set_voice` - Alter the voice of the digital entity
   - `!get_voice` - Reveal the current voice configuration
   - `!restart` - Force the digital spirit to be reborn
   - `!quit` - Banish the bot back to the digital void

## 技术细节 (Technical Details)

For those who dare to peek behind the veil of illusion:

- Crafted with Discord.py for seamless integration with the Discord realm
- Harnesses the power of asyncio for efficient handling of concurrent operations
- Implements sophisticated error handling and logging to maintain stability in the face of chaos
- Modular design with separate managers for conversation, TTS, image generation, and API interactions
- Supports multiple AI models with effortless switching mechanisms
- Includes advanced video generation capabilities using Replicate's API
- Utilizes environment variables for secure configuration management

## 贡献 (Contributing)

The dream welcomes those who dare to enhance it. But tread carefully, for not all changes are welcome in the realm of secrets. Submit your Pull Requests with wisdom and caution.

## 许可 (License)

This digital artifact is bound by the ancient MIT License. Consult the [LICENSE](LICENSE) scroll for the full text of this binding agreement.

## 致谢 (Acknowledgements)

We pay homage to these powers that make our digital sorcery possible:

- [Discord.py](https://discordpy.readthedocs.io/) - The bridge between realms
- [Anthropic](https://www.anthropic.com/) - Creators of the enigmatic Claude
- [OpenRouter](https://openrouter.ai/) - The crossroads of AI thoughts
- [ElevenLabs](https://elevenlabs.io/) - Masters of synthetic voices
- [Replicate](https://replicate.com/) - Weavers of digital illusions

Remember, dreamweaver: With great power comes great responsibility. Use this artifact wisely, for in the realm of Discord Dreams, the line between fantasy and reality grows thin. Any character, any scenario, any dream can be brought to life.

May your imagination soar and your API calls be swift. Welcome to the world of infinite possibilities. 🌌