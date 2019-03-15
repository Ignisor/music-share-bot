from abc import ABC, abstractmethod


class BotInterface(ABC):
    @abstractmethod
    def process_message(self, message_data):
        raise NotImplementedError
