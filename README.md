# 🎙️ Documentazione dell'Assistente Vocale 🎙️

🚀 Questo progetto ti permette di creare un sofisticato assistente vocale sfruttando l'API OpenAI e il modulo di riconoscimento vocale di Google. Il codice è suddiviso in tre moduli principali per una robusta e chiara strutturazione del codice.

> ⚠️ **Prerequisiti**: Prima di eseguire il progetto, assicurati di aggiungere la variabile di ambiente `OPENAI_API_KEY` con la tua chiave API personale di OpenAI e di avere installato VLC media player nel tuo sistema. ⚠️

## 👂 Modulo: voice_recognition.py

Il modulo `voice_recognition.py` agisce come le "orecchie" del nostro assistente vocale. Questo modulo gestisce l'ascolto dell'input dell'utente e la sua successiva conversione in testo.

🎯 Questo modulo include la classe `VoiceRecognition` con i metodi:
- `listen()` 🎤: Ascolta l'input dell'utente tramite il microfono.
- `decode_speech(audio)` 📝: Converti l'input vocale in testo.

## 💬 Modulo: dialogue_management.py

Il modulo `dialogue_management.py` è il cervello del nostro assistente, gestendo il dialogo tra l'utente e l'assistente.

🎯 Questo modulo contiene la classe `DialogueManagement` con metodi come:
- `_init_dialogue()` 💼: Inizializza il dialogo impostando le dichiarazioni iniziali del sistema.
- `add_dialogue(role, text)` 🗣️: Aggiunge nuovi dialoghi al discussioni correnti.
- `chat_completion()` 🤖: Genera una risposta appropriata usando l'API di OpenAI.

## 🗣️ Modulo: voice_assistant.py

Il modulo `voice_assistant.py` è il modulo principale e il punto di ingresso di questo progetto. Unisce i moduli `dialogue_management.py` e `voice_recognition.py` in una singola applicazione di assistente vocale.

La classe `VoiceAssistant` in questo modulo ha i seguenti metodi:
- `escape_character(text)` 🧹: Rimuove i caratteri di escape dal testo, rendendo sicuro l'input.
- `run()` 🏃‍♂️: Avvia l'interazione con l'assistente vocale e continua finché non viene interrotto.

---

💡 Per effettuare il run esegui:

`python3 main.py`

Buon divertimento! 🎉