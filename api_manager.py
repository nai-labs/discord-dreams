# api_manager.py
import aiohttp
from config import OPENROUTER_URL, ANTHROPIC_URL, OPENROUTER_HEADERS, ANTHROPIC_HEADERS, OPENROUTER_MODELS, CLAUDE_MODELS, DEFAULT_CLAUDE_MODEL, ANTHROPIC_MAX_TOKENS, LMSTUDIO_MAX_TOKENS, DEFAULT_LLM, LMSTUDIO_URL, LMSTUDIO_HEADERS

class APIManager:
    def __init__(self):
        self.current_llm = DEFAULT_LLM
        self.current_claude_model = DEFAULT_CLAUDE_MODEL
        self.current_openrouter_model = list(OPENROUTER_MODELS.keys())[0]
        self.current_lmstudio_model = None

    async def generate_response(self, message, conversation, system_prompt):
        if self.current_llm == "anthropic":
            response_text = await self.generate_anthropic_response(message, conversation, system_prompt)
        elif self.current_llm == "openrouter":
            response_text = await self.generate_openrouter_response(message, conversation, system_prompt)
        elif self.current_llm == "lmstudio":
            response_text = await self.generate_lmstudio_response(message, conversation, system_prompt)
        else:
            response_text = "Invalid LLM selected."
        return response_text

    async def generate_anthropic_response(self, message, conversation, system_prompt):
        # Add the prompt caching beta header
        headers = ANTHROPIC_HEADERS.copy()
        headers['anthropic-beta'] = 'prompt-caching-2024-07-31'

        data = {
            "model": self.current_claude_model,
            "system": [
                {
                    "type": "text",
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            "messages": [
                *[{
                    "role": msg["role"],
                    "content": [
                        {
                            "type": "text",
                            "text": msg["content"],
                            "cache_control": {"type": "ephemeral"}
                        }
                    ]
                } for msg in conversation if msg["role"] != "system"],
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        }
                    ]
                }
            ],
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
                            
                            # Log cache-related information
                            usage = response_json.get('usage', {})
                            cache_created = usage.get('cache_creation_input_tokens', 0)
                            cache_read = usage.get('cache_read_input_tokens', 0)
                            print(f"Cache created: {cache_created} tokens")
                            print(f"Cache read: {cache_read} tokens")
                            
                            return response_text.strip()
                        else:
                            print("Error: 'content' key not found in the Anthropic API response.")
                    else:
                        print(f"Error: Anthropic API returned status code {response.status}")
                except Exception as e:
                    print(f"Error: {str(e)}")
                
                return "I apologize, but I encountered an error while processing your request."
            
    def get_current_llm(self):
        return self.current_llm

    async def generate_openrouter_response(self, message, conversation, system_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": msg["role"], "content": msg["content"]} for msg in conversation],
            {"role": "user", "content": message}
        ]

        async with aiohttp.ClientSession() as session:
            async with session.post(OPENROUTER_URL, json={
                "model": self.current_openrouter_model,
                "messages": messages
            }, headers=OPENROUTER_HEADERS) as response:
                response_json = await response.json()
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    response_text = response_json['choices'][0]['message']['content']
                    return response_text
                else:
                    return "No response generated."

    async def generate_lmstudio_response(self, message, conversation, system_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": msg["role"], "content": msg["content"]} for msg in conversation],
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

    def switch_llm(self, llm_name):
        if llm_name in ["anthropic", "openrouter", "lmstudio"]:
            self.current_llm = llm_name
            return True
        return False

    def set_lmstudio_model(self, model_name):
        self.current_lmstudio_model = model_name
        self.current_llm = "lmstudio"
        return True

    def get_current_model(self):
        if self.current_llm == "anthropic":
            return self.current_claude_model
        elif self.current_llm == "openrouter":
            return self.current_openrouter_model
        else:
            return self.current_lmstudio_model


    def switch_claude_model(self, model_code):
        for full_name, short_code in CLAUDE_MODELS.items():
            if model_code.lower() == short_code.lower():
                self.current_claude_model = full_name
                self.current_llm = "anthropic"
                return True
        return False

    def switch_openrouter_model(self, model_code):
        for full_name, short_code in OPENROUTER_MODELS.items():
            if model_code.lower() == short_code.lower():
                self.current_openrouter_model = full_name
                self.current_llm = "openrouter"
                return True
        return False

    def get_current_model(self):
        if self.current_llm == "anthropic":
            return self.current_claude_model
        else:
            return self.current_openrouter_model