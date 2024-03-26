import speech_recognition as sr


class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Dimmi qualcosa...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, phrase_time_limit=5)
            return audio

    def decode_speech(self, audio):
        try:
            return self.recognizer.recognize_google(audio, language='it-IT')
        except sr.UnknownValueError:
            print("Non ho capito quello che hai detto")
        except sr.RequestError as e:
            print(f"Errore nella richiesta a Google Speech Recognition service; {e}")
