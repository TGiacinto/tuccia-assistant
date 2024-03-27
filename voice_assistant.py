import time
import gtts
import vlc

from functions import handle_function
from text_to_speech import TextToSpeech
from utils import fetch_function
from voice_recognition import VoiceRecognition
from dialogue_management import DialogueManagement


def play_audio_from_text(text, use_open_ai=False):
    path = "audio.mp3"

    if use_open_ai is False:
        tts = gtts.gTTS(text, lang="it")
        tts.save(path)
    else:
        open_ai_text_to_speech = TextToSpeech()
        response = open_ai_text_to_speech.convert_to_speech(text)
        response.stream_to_file(path)

    v = vlc.MediaPlayer(path)
    v.play()
    time.sleep(1)
    while v.is_playing():
        time.sleep(1)


class VoiceAssistant:
    def __init__(self):
        self.voice_recognition = VoiceRecognition()
        self.dialogue_management = DialogueManagement()

    def run(self):
        play_audio_from_text("Ciao sono Tuccia Assistant. Come posso aiutarti oggi?", use_open_ai=False)
        functions = fetch_function(name="functions.json")
        while True:
            try:
                audio = self.voice_recognition.listen()
                text = self.voice_recognition.decode_speech(audio)
                if text:
                    print("You say:", text)
                    self.dialogue_management.add_dialogue('user', text)
                    chat_completion = self.dialogue_management.chat_completion(function=functions, tool_choice="auto")
                    response_chat_gpt, function_response, function_name, tool_call_id = handle_function(
                        chat_completion.choices[0].message)

                    response_text = response_chat_gpt or str(function_response)

                    if response_text is not None:
                        self.dialogue_management.add_dialogue('assistant', response_text)

                    play_audio_from_text(response_text, use_open_ai=False)

            except KeyboardInterrupt:
                break
