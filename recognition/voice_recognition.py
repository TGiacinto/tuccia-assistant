import speech_recognition as sr

from text_to_speech.text_to_speech_service import TextToSpeechService


class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.text_to_speech_service = TextToSpeechService()

    def listen(self):
        with sr.Microphone() as source:
            print("Say me...")
            try:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, phrase_time_limit=30, timeout=5)
                return audio
            except sr.WaitTimeoutError as e:
                return None

    def decode_speech(self, audio):
        try:
            if audio is None and audio != '': return
            return self.recognizer.recognize_google(audio, language='it-IT')
        except sr.UnknownValueError:
            print("I dont understand!")
            self.text_to_speech_service.play_audio_from_text("Non capito, puoi ripetere?")
        except sr.RequestError as e:
            print(f"Error Google Speech Recognition service; {e}")
