# api_manager.py
import aiohttp
import json
import logging
from config import OPENROUTER_URL, ANTHROPIC_URL, OPENROUTER_HEADERS, ANTHROPIC_HEADERS, OPENROUTER_MODELS, CLAUDE_MODELS, DEFAULT_CLAUDE_MODEL, ANTHROPIC_MAX_TOKENS, LMSTUDIO_MAX_TOKENS, DEFAULT_LLM, LMSTUDIO_URL, LMSTUDIO_HEADERS

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        headers = ANTHROPIC_HEADERS.copy()

        # Prepare messages
        messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in conversation
        ]
        messages.append({"role": "user", "content": message})

        data = {
            "model": self.current_claude_model,
            "messages": messages,
            "system": system_prompt,
            "max_tokens": ANTHROPIC_MAX_TOKENS,
            "temperature": 0.7,
        }

        # Log the request payload (excluding sensitive information)
        logger.debug(f"Anthropic API Request Payload: {json.dumps({k: v for k, v in data.items() if k != 'messages'}, indent=2)}")
        logger.debug(f"Number of messages in conversation: {len(conversation)}")
        logger.debug(f"Number of messages sent to API: {len(messages)}")

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
                            
                            # Log usage information
                            usage = response_json.get('usage', {})
                            input_tokens = usage.get('input_tokens', 0)
                            output_tokens = usage.get('output_tokens', 0)
                            logger.info(f"Input tokens: {input_tokens}")
                            logger.info(f"Output tokens: {output_tokens}")
                            
                            return response_text.strip()
                        else:
                            logger.error("Error: 'content' key not found in the Anthropic API response.")
                    else:
                        logger.error(f"Error: Anthropic API returned status code {response.status}")
                        logger.error(f"Response content: {json.dumps(response_json, indent=2)}")
                except Exception as e:
                    logger.error(f"Error in generate_anthropic_response: {str(e)}", exc_info=True)
                
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