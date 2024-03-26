import time
import gtts
import vlc

from functions import handle_function
from utils import fetch_function
from voice_recognition import VoiceRecognition
from dialogue_management import DialogueManagement


class VoiceAssistant:
    def __init__(self):
        self.voice_recognition = VoiceRecognition()
        self.dialogue_management = DialogueManagement()

    def play_audio_from_text(self, text):
        tts = gtts.gTTS(text, lang="it")
        tts.save("audio.mp3")
        v = vlc.MediaPlayer("audio.mp3")
        v.play()
        time.sleep(1)
        while v.is_playing():
            time.sleep(1)

    def run(self):
        functions = fetch_function(name="functions.json")
        while True:
            try:
                audio = self.voice_recognition.listen()
                text = self.voice_recognition.decode_speech(audio)
                if text:
                    print("You say:", text)
                    self.dialogue_management.add_dialogue('user', text)
                    chat_completion = self.dialogue_management.chat_completion(function=functions)
                    response_chat_gpt, function_response, function_name, tool_call_id = handle_function(
                        chat_completion.choices[0].message)

                    response_text = response_chat_gpt or str(function_response)

                    if response_text is not None:
                        self.dialogue_management.add_dialogue('assistant', response_text)

                    self.play_audio_from_text(response_text)

            except KeyboardInterrupt:
                break
