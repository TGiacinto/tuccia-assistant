from abc import ABC

from home_assistant.abstract_device import AbstractDevice


class Light(AbstractDevice, ABC):
    def __init__(self, home_assistant, color):
        self.home_assistant = home_assistant
        self.__get_client()
        self.color = color

    def activate(self, entity_id):
        self.__turn_on_with_color(entity_id) if self.color is not None and self.color != '' else self.__turn_on(entity_id)

    def deactivate(self, entity_id):
        self.__get_client().get_domain(entity_id.split('.')[0]).turn_off(entity_id=entity_id)

    def status(self, entity_id):
        client = self.home_assistant.client.get_domain(entity_id.split('.')[0])
        return client.get_state(entity_id=entity_id.split('.')[1])

    def __turn_on(self, entity_id):
        self.__get_client().get_domain(entity_id.split('.')[0]).turn_on(entity_id=entity_id)

    def __turn_on_with_color(self, entity_id):
        self.__get_client().get_domain(entity_id.split('.')[0]).turn_on(entity_id=entity_id, color_name=self.color)

    def __get_client(self):
        return self.home_assistant.client
