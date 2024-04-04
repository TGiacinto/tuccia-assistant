# 🎙️ Voice Assistant Documentation 🎙️

🚀 This project allows you to create a sophisticated voice assistant using the OpenAI API and the Google speech recognition module. The code is divided into three main modules for a robust and clear code structure.

> ⚠️ **Prerequisites**: Before running the project, make sure to add the `OPENAI_API_KEY` environment variable with your personal OpenAI API key and to have VLC media player installed on your system. Also, make sure you have Python and pip installed in your environment.⚠️

## 🛠️ Local Installation

To install the project locally, follow these steps:

1. Create a virtual environment using `venv`:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

    - On Windows:

   ```bash
   venv\Scripts\activate
   ```

    - On Unix or MacOS:

   ```bash
   source venv/bin/activate
   ```

3. Install project dependencies using `pip`:

```bash
pip3 install -r requirements.txt
```

## 👂 Module: voice_recognition.py

The `voice_recognition.py` module acts as the "ears" of our voice assistant. This module handles listening to user input and its subsequent conversion to text.

🎯 This module includes the `VoiceRecognition` class with methods:
- `listen()` 🎤: Listen to user input via the microphone.
- `decode_speech(audio)` 📝: Convert voice input to text.

## 💬 Module: dialogue_management.py

The `dialogue_management.py` module is the brain of our assistant, managing the dialogue between the user and the assistant.

🎯 This module contains the `DialogueManagement` class with methods like:
- `_init_dialogue()` 💼: Initialize dialogue by setting up initial system statements.
- `add_dialogue(role, text)` 🗣️: Add new dialogues to ongoing discussions.
- `chat_completion()` 🤖: Generate an appropriate response using the OpenAI API.

## 🗣️ Module: voice_assistant.py

The `voice_assistant.py` module is the main module and entry point of this project. It combines the `dialogue_management.py` and `voice_recognition.py` modules into a single voice assistant application.

The `VoiceAssistant` class in this module has the following methods:
- `escape_character(text)` 🧹: Remove escape characters from text, making input safe.
- `run()` 🏃‍♂️: Start the interaction with the voice assistant and continue until interrupted.

---

💡 **Available Text-to-Speech Services**:
- `PYTTSX3`: Pyttsx3
- `OPENAI`: OpenAI
- `GTTS`: gTTS
- `FUN_VOICE`: Fun Voice
- `ELEVENLABS`: ElevenLabs *(requires key configuration)*

ℹ️ **Next Implementation**: Integration with Home Assistant will soon be added for enhanced automation and home control.

💡 To run, execute:

```bash
python3 main.py
```

💡 To change the Text-to-Speech service, modify the value of the `service` variable in the `__init__` method of the `VoiceAssistant` module.
- `TextToSpeechService(service=ServiceType.GTTS)` 🗣️

Have fun! 🎉

---
