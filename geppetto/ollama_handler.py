import os
from typing import Callable
import logging

import ollama

from geppetto.llm_api_handler import LLMHandler
from geppetto.utils import convert_openai_markdown_to_slack

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")


class OllamaHandler(LLMHandler):

    def __init__(
            self,
            personality
    ):
        super().__init__("Ollama", OLLAMA_MODEL, client=None)
        self.personality = personality
        self.system_role = "system"
        self.assistant_role = "assistant"
        self.user_role = "user"

    def llm_generate_content(self, prompt: str, callback: Callable, *callback_args):
        logging.info("Sending msg to ollama: %s", prompt)
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": self.system_role,
                    "content": self.personality,
                },
                *prompt,
            ])
        content = response['message']['content']
        content_md = convert_openai_markdown_to_slack(content, model=self.model)
        if len(content_md) > 4000:
            # Split the message if it's too long
            response_parts = self.split_message(content_md)
            return response_parts
        else:
            return content_md
