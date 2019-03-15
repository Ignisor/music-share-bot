from abc import ABC, abstractmethod


class MusicProvider(ABC):
    NAME = None

    @abstractmethod
    def get_music_name(self, url):
        raise NotImplementedError
    
    @abstractmethod
    def get_music_url(self, name):
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def is_music_url(self, url):
        raise NotImplementedError
