
import ast
import json
from collections import deque
from typing import List, Dict, Tuple, Deque, Union

from openai import OpenAI

client = OpenAI(api_key='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')

MAX_RETRIES = 3

class ChatMemory:
    def __init__(self, max_length: int = 10):
        self.messages: Deque[Dict] = deque(maxlen=max_length)

    def add_message(self, role: str = None, content: str = None, messages: List[Dict] = None):
        if messages:
            for message in messages:
                if not message.get("content") or not message.get("role"):
                    raise ValueError("Both 'role' and 'content' fields must be provided in the message.")
                self.messages.append(message)
        else:
            if not role or not content:
                raise ValueError("Both 'role' and 'content' fields must be provided.")
            self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Dict]:
        return list(self.messages)

chat_memory = ChatMemory()

def send_gpt_message(
    messages: List[Dict] = None,
    content: str = None,
    add_history: bool = True,
    model: str = "gpt-4",
) -> str:
    chat_history = chat_memory.get_messages()
    gpt_message = chat_history

    if add_history:
        chat_memory.add_message(messages=messages, content=content, role="user")

    if content:
        gpt_message += [{"role": "user", "content": content}]
    elif messages:
        gpt_message += messages
    else:
        raise Exception("No gpt message was given, failed to send gpt message.")

    print(f"Sending gpt_message: {gpt_message}")

    retry_counter = 0
    while retry_counter < MAX_RETRIES:
        try:
            response = client.Completion.create(engine=model,
                                                prompt=gpt_message,
                                                max_tokens=150)
            user_response = response['choices'][0]['text']

            if add_history:
                chat_memory.add_message(role="assistant", content=user_response)

            return user_response
        except Exception as exc:
            retry_counter += 1
            print(f"""
                  Failed to send request to gpt api: {gpt_message}. \n 
                  The reason is: {exc}. \n
                  Retrying #{retry_counter}...
                  """)

# The updated usage of OpenAI GPT-3 API methods and response handling based on library updates.
