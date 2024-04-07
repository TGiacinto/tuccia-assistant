from dialogue_management import DialogueManagement
from functions import handle_function
from text_to_speech_service import TextToSpeechService, ServiceType
from utils import fetch_function
from voice_recognition import VoiceRecognition


class VoiceAssistant:
    def __init__(self):
        self.voice_recognition = VoiceRecognition()
        self.dialogue_management = DialogueManagement()
        self.text_to_speech_service = TextToSpeechService(service=ServiceType.GTTS)

    def __start(self):
        self.dialogue_management.add_dialogue('user',
                                              "Give me a welcome phrase, saying that your name is what you can do.")
        chat_completion = self.dialogue_management.chat_completion()
        message = chat_completion.choices[0].message.content
        self.text_to_speech_service.play_audio_from_text(message)

    def run(self):
        self.__start()
        functions = fetch_function(name="functions.json")
        while True:
            try:
                TextToSpeechService.play = True
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

                    self.text_to_speech_service.play_audio_from_text(response_text)

            except KeyboardInterrupt:
                break
