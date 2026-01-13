from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class ChatGroqWrapper:
    def __init__(
        self,
        model="openai/gpt-oss-120b",
        system_prompt=None,
        **defaults
    ):
        self.client = Groq()
        self.model = model
        self.system_prompt = system_prompt
        self.defaults = defaults

    def _normalize_messages(self, message):
        messages = []

        # Inject system prompt once per call
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })

        # Case 1: string → user
        if isinstance(message, str):
            messages.append({
                "role": "user",
                "content": message
            })

        # Case 2: dict → default role=user if missing
        elif isinstance(message, dict):
            messages.append({
                "role": message.get("role", "user"),
                "content": message["content"]
            })

        # Case 3: list of messages
        elif isinstance(message, list):
            for msg in message:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg["content"]
                })

        else:
            raise TypeError("Message must be str, dict, or list")

        return messages

    def invoke(self, message, stream=False):
        messages = self._normalize_messages(message)
        return self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream,
            **self.defaults
        )


