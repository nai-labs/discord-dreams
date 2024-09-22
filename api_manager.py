import aiohttp
import json
from config import OPENROUTER_URL, ANTHROPIC_URL, OPENROUTER_HEADERS, ANTHROPIC_HEADERS, OPENROUTER_MODELS, CLAUDE_MODELS, DEFAULT_CLAUDE_MODEL, ANTHROPIC_MAX_TOKENS, LMSTUDIO_MAX_TOKENS, DEFAULT_LLM, LMSTUDIO_URL, LMSTUDIO_HEADERS

class APIManager:
    def __init__(self):
        self.current_language_model = DEFAULT_LLM
        self.current_claude_model = DEFAULT_CLAUDE_MODEL
        self.current_openrouter_model = list(OPENROUTER_MODELS.keys())[0]
        self.current_lmstudio_model = None

    async def generate_response(self, message, conversation, system_prompt):
        if self.current_language_model == "anthropic":
            response_text = await self.generate_anthropic_response(message, conversation, system_prompt)
        elif self.current_language_model == "openrouter":
            response_text = await self.generate_openrouter_response(message, conversation, system_prompt)
        elif self.current_language_model == "lmstudio":
            response_text = await self.generate_lmstudio_response(message, conversation, system_prompt)
        else:
            response_text = "Invalid Language Model selected."
        return response_text

    async def generate_anthropic_response(self, message, conversation, system_prompt):
        headers = ANTHROPIC_HEADERS.copy()
        headers['anthropic-beta'] = 'prompt-caching-2024-07-31'

        messages = [
            *[{
                "role": message["role"],
                "content": message["content"]
            } for message in conversation if message["role"] != "system"],
            {
                "role": "user",
                "content": message
            }
        ]

        data = {
            "model": self.current_claude_model,
            "messages": messages,
            "system": system_prompt,
            "max_tokens": ANTHROPIC_MAX_TOKENS,
            "temperature": 0.7,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(ANTHROPIC_URL, json=data, headers=headers) as response:
                try:
                    response_json = await response.json()
                    if response.status == 200:
                        if 'content' in response_json:
                            content = response_json['content']
                            response_text = ""
                            for item in content:
                                if item['type'] == 'text':
                                    response_text += item['text']
                            return response_text.strip()
                        else:
                            print("Error: 'content' key not found in the Anthropic API response.")
                    else:
                        print(f"Error: Anthropic API returned status code {response.status}")
                except Exception as error:
                    print(f"Error: {str(error)}")
                
                return "I apologize, but I encountered an error while processing your request."

    async def generate_openrouter_response(self, message, conversation, system_prompt):
        print(f"OpenRouter - Conversation history length: {len(conversation)}")

        messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": msg["role"], "content": msg["content"]} for msg in conversation],
            {"role": "user", "content": message}
        ]

        print(f"OpenRouter Request - Model: {self.current_openrouter_model}")
        print(f"OpenRouter Request - Messages: {json.dumps(messages, indent=2)}")

        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, json={
                "model": self.current_openrouter_model,
                "messages": messages
            }, headers=OPENROUTER_HEADERS) as response:
                response_json = await response.json()
                print(f"OpenRouter Response Status: {response.status}")

                if 'choices' in response_json and len(response_json['choices']) > 0:
                    response_text = response_json['choices'][0]['message']['content']
                    return response_text
                else:
                    return "No response generated."

    async def generate_lmstudio_response(self, message, conversation, system_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": message["role"], "content": message["content"]} for message in conversation],
            {"role": "user", "content": message}
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(LMSTUDIO_URL, json={
                "model": self.current_lmstudio_model,
                "messages": messages,
                "max_tokens": LMSTUDIO_MAX_TOKENS,
                "temperature": 0.7,
            }, headers=LMSTUDIO_HEADERS) as response:
                response_json = await response.json()
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    response_text = response_json['choices'][0]['message']['content']
                    return response_text
                else:
                    return "No response generated from LMStudio."

    async def fetch_lmstudio_models(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(LMSTUDIO_URL.replace('chat/completions', 'models'), headers=LMSTUDIO_HEADERS) as response:
                if response.status == 200:
                    models_json = await response.json()
                    return [model['id'] for model in models_json.get('data', [])]
                else:
                    return []

    def switch_language_model(self, language_model_name):
        if language_model_name in ["anthropic", "openrouter", "lmstudio"]:
            self.current_language_model = language_model_name
            return True
        return False

    def set_lmstudio_model(self, model_name):
        self.current_lmstudio_model = model_name
        self.current_language_model = "lmstudio"
        return True

    def get_current_model(self):
        if self.current_language_model == "anthropic":
            return self.current_claude_model
        elif self.current_language_model == "openrouter":
            return self.current_openrouter_model
        else:
            return self.current_lmstudio_model

    def switch_claude_model(self, model_code):
        for full_name, short_code in CLAUDE_MODELS.items():
            if model_code.lower() == short_code.lower():
                self.current_claude_model = full_name
                self.current_language_model = "anthropic"
                return True
        return False

    def switch_openrouter_model(self, model_code):
        for full_name, short_code in OPENROUTER_MODELS.items():
            if model_code.lower() == short_code.lower():
                self.current_openrouter_model = full_name
                self.current_language_model = "openrouter"
                return True
        return False

    def get_current_language_model(self):
        return self.current_language_model