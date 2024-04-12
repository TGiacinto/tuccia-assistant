from abc import ABC

from home_assistant.abstract_device import AbstractDevice


class Alarm(AbstractDevice, ABC):
    def __init__(self, home_assistant):
        self.home_assistant = home_assistant
        self.__get_client()

    def activate(self, entity_id):
        self.__get_client().get_domain(entity_id.split('.')[0]).alarm_arm_home(entity_id=entity_id)

    def deactivate(self, entity_id):
        self.__get_client().get_domain(entity_id.split('.')[0]).alarm_disarm(entity_id=entity_id)

    def status(self, entity_id):
        client = self.home_assistant.client.get_domain(entity_id.split('.')[0])
        return client.get_state(entity_id=entity_id.split('.')[1])

    def __get_client(self):
        return self.home_assistant.client
