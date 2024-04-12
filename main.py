from assistant.voice_assistant import VoiceAssistant
from home_assistant.home_assistant import HomeAssistant

if __name__ == "__main__":
    ha = HomeAssistant()
    states = ha.get_my_states()
    print(states)
    domain = ha.client.get_domain('climate')
    print(domain)
    assistant = VoiceAssistant()
    assistant.run()
