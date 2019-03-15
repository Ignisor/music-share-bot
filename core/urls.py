from core.providers import ALL_PROVIDERS


class MusicUrl(object):
    def __init__(self, url, provider=None):
        self.url = url

        self.__provider = provider

    @property
    def provider(self):
        if self.__provider is None:
            self.__provider = self.__get_provider()
        
        return self.__provider

    def __get_provider(self):
        for provider_cls in ALL_PROVIDERS:
            provider_cls.is_music_url(self.url)
        
        return provider_cls()

    def get_name(self):
        return self.provider.get_music_name(self.url)
