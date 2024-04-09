from abc import ABC, abstractmethod


class AbstractDevice(ABC):
    @abstractmethod
    def activate(self, entity_id):
        pass

    @abstractmethod
    def deactivate(self, entity_id):
        pass

    @abstractmethod
    def status(self, entity_id):
        pass
