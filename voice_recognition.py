import speech_recognition as sr


class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Dimmi qualcosa...")
            try:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=1)
                return audio
            except sr.WaitTimeoutError as e:
                return None

    def decode_speech(self, audio):
        try:
            if audio is None: return
            return self.recognizer.recognize_google(audio, language='it-IT')
        except sr.UnknownValueError:
            print("Non ho capito quello che hai detto")
        except sr.RequestError as e:
            print(f"Errore nella richiesta a Google Speech Recognition service; {e}")
