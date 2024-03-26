import time
import gtts
import vlc
from voice_recognition import VoiceRecognition
from dialogue_management import DialogueManagement


class VoiceAssistant:
    def __init__(self):
        self.voice_recognition = VoiceRecognition()
        self.dialogue_management = DialogueManagement()

    def run(self):
        while True:
            try:
                audio = self.voice_recognition.listen()
                text = self.voice_recognition.decode_speech(audio)
                if text:
                    print("You say:", text)
                    self.dialogue_management.add_dialogue('user', text)
                    chat_completion = self.dialogue_management.chat_completion()
                    answer = chat_completion.choices[0].message.content
                    self.dialogue_management.add_dialogue('assistant', answer)

                    tts = gtts.gTTS(answer, lang="it")
                    tts.save("audio.mp3")
                    v = vlc.MediaPlayer("audio.mp3")
                    v.play()
                    time.sleep(1)
                    while v.is_playing():
                        time.sleep(1)
            except KeyboardInterrupt:
                break
