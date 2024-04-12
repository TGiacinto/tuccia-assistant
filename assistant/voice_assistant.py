from dialogue.dialogue_management import DialogueManagement
from functions.functions import handle_function
from home_assistant.home_assistant import HomeAssistant
from recognition.voice_recognition import VoiceRecognition
from text_to_speech.text_to_speech_service import TextToSpeechService, ServiceType
from utils.utils import fetch_function


class VoiceAssistant:
    def __init__(self):
        self.voice_recognition = VoiceRecognition()
        self.dialogue_management = DialogueManagement()
        self.text_to_speech_service = TextToSpeechService(service=ServiceType.PYTTSX3)
        self.home_assistant = HomeAssistant()

    def __start(self):
        ha_is_active = self.home_assistant.is_active()

        prompt = f'You are Tuccia Assistant, a voice assistant. Understand and answer your questions. You should invoke the search_online function only if the user requests it. You can interact with Home Assistant. Any device-related requests invoke the "home_assistant" function. So you need to carefully understand user intent. I can call functions! I reply with a maximum of 20 words! You must use friendly language.' if ha_is_active else f'You are Tuccia Assistant, a voice assistant. You understand and answer your questions. You should only search online if the user requests it. You must activate the fun_voice function only if the user requests it. I can call functions! You cannot interact with Home Assistant because the user has not configured it.  You reply with a maximum of 20 words! You must use friendly language. '

        self.dialogue = self.dialogue_management.add_dialogue(role='system', text=prompt)
        sentence = "Hi, what's your name? What can you do? You can control home devices." if ha_is_active else "Hi, what's your name? What can you do? . You need to tell the user that they need to configure home assistant for a better home automation experience"

        self.dialogue_management.add_dialogue(role='user', text=sentence)
        chat_completion = self.dialogue_management.chat_completion()
        message = chat_completion.choices[0].message.content
        self.text_to_speech_service.play_audio_from_text(message)

    def run(self):
        self.__start()
        function_name = "functions_home_assistant.json" if self.home_assistant.is_active() else "functions.json"
        functions = fetch_function(name=function_name)
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

            except Exception as e:
                error = DialogueManagement()
                error.error()
                chat_completion = error.chat_completion()
                message = chat_completion.choices[0].message.content
                self.text_to_speech_service.play_audio_from_text(message)
