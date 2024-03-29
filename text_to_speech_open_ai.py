import os
from dotenv import load_dotenv

from openai import OpenAI


class TextToSpeechOpenAi:

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def convert_to_speech(self, text):
        return self.client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )
