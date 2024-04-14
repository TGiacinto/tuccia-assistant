import os

from dotenv import load_dotenv
from homeassistant_api import Client

from utils import utils


class HomeAssistant:
    def __init__(self):
        load_dotenv()
        try:
            self.client = Client(os.environ.get("HOME_ASSISTANT_URL"), os.environ.get("HOME_ASSISTANT_TOKEN"))
            self.client.get_states()
            self.active = True
        except Exception:
            self.active = False

    def is_active(self):
        return self.active

    def get_my_states(self):
        if self.active:
            states = self.client.get_states()
            result = []
            for state in states:
                result.append({'entity_id': state.entity_id, 'name': state.attributes['friendly_name'],'state':state.state})
            exclude_keywords = ['sun', 'person', 'home', 'person', 'tts', 'todo','forecast_casa']
            return utils.filter_entities_and_exclude_key(result, exclude_keywords, 'entity_id')

        else:
            print("Home assistant not configured!")
