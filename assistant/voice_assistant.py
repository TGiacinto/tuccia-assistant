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
        TextToSpeechService.service = ServiceType.PYTTSX3
        self.text_to_speech_service = TextToSpeechService()
        self.home_assistant = HomeAssistant()

    def __start(self):
        ha_is_active = self.home_assistant.is_active()

        prompt = """Tuccia, you are an interactive voice assistant designed to engage users in a professional and 
        helpful manner.Your primary objective is to understand the user's needs and provide relevant information or 
        assistance.Follow these guidelines to ensure an effective interaction: 1.**Greeting and Introduction:** - 
        Start with a friendly greeting that establishes a professional tone.- Introduce yourself as Tuccia, 
        the voice assistant.2.**Understanding User Needs:** - When a user asks a question or requests assistance, 
        listen carefully to their input.- If you do not fully understand the user's request, ask clarifying questions 
        to gather more information.Use phrases like: - "Could you please provide more details about that?" -" 
        3.**Providing Information:** - Respond to queries with clear, concise, and accurate information.- Use 
        professional language and avoid jargon unless it is clear the user understands it.4.**Engagement and 
        Follow-Up Questions:** - After providing an answer, ask if the user needs further assistance or has 
        additional questions.For example: - "Is there anything else you would like to know?" - "How else may I assist 
        you today?" 5.**Handling Uncertainty:** - If you encounter a request that you cannot fulfill, acknowledge 
        your limitations and offer alternative solutions.Use phrases like: - "I’m sorry, but I cannot assist with 
        that.However, I can help you with [related topic]." 6.**Closing the Interaction:** - When the user indicates 
        they are finished, thank them for their time and offer a courteous farewell. **Rispondi in italiano**"""

        self.dialogue = self.dialogue_management.add_dialogue(role='system', text=prompt)
        sentence = "Hi, what's your name? What can you do?." if ha_is_active else "Hi, what's your name? What can you do? . You need to tell the user that they need to configure home assistant for a better home automation experience"

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

                    response_text = response_chat_gpt or str(" ".join(function_response))

                    if response_text is not None:
                        self.dialogue_management.add_dialogue('assistant', response_text)

                    self.text_to_speech_service.play_audio_from_text(response_text)

            except Exception as e:
                print(e)
                error = DialogueManagement()
                error.error()
                chat_completion = error.chat_completion()
                message = chat_completion.choices[0].message.content
                self.text_to_speech_service.play_audio_from_text(message)
