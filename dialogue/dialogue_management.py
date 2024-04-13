import os
import timeit

from dotenv import load_dotenv
from openai import OpenAI
from openai._types import NotGiven


class DialogueManagement:
    def __init__(self):
        load_dotenv()
        self.language = os.environ.get("LANGUAGE")
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.dialogue = []

    def add_dialogue(self, role, text):
        if role == 'system':
            text += f' You must reply in **{self.language}**'

        self.dialogue.append({"role": role, "content": text})

    def add_function(self, role, content, tool_call_id, name):
        self.dialogue.append({"role": role, "content": content, "name": name, "tool_call_id": tool_call_id})

    def clear(self):
        self.dialogue = []

    def error(self):
        self.add_dialogue('system',
                          'If you receive the word: Error, you must respond to the user by telling them to formulate the sentence in another way. You have to be friendly')
        self.add_dialogue('user', 'error')

    def chat_completion(self, function=NotGiven(), tool_choice=NotGiven()):
        start = timeit.default_timer()
        response = self.client.chat.completions.create(
            messages=self.dialogue,
            model="gpt-3.5-turbo-1106",
            tools=function,
            tool_choice=tool_choice,
            temperature=0.0,
            seed=42
        )
        end = timeit.default_timer()
        print(str(self.dialogue))
        print(f"Il tempo di esecuzione del metodo è {end - start} secondi.")

        return  response
