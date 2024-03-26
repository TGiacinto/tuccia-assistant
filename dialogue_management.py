from openai import OpenAI
import os
from dotenv import load_dotenv


class DialogueManagement:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.dialogue = self._init_dialogue()

    @staticmethod
    def _init_dialogue():
        role = "system"
        content = ("Tu sei il Tuccia Assistant e sei un assistente vocale.")
        return [{"role": role, "content": content}]

    def add_dialogue(self, role, text):
        self.dialogue.append({"role": role, "content": text})

    def chat_completion(self):
        return self.client.chat.completions.create(
            messages=self.dialogue,
            model="gpt-3.5-turbo"
        )
