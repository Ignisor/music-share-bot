import re

from core.providers import INPUT_PROVIDERS


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
        for provider_cls in INPUT_PROVIDERS:
            if provider_cls.is_music_url(self.url):
                return provider_cls()

        raise ValueError(f'Unable to find provider for {self.url}')

    def get_name(self):
        return self.provider.get_music_name(self.url)


class UrlsExtractor(object):
    URL_REGEX = re.compile(r'(https?://[^\s]+)')

    @classmethod
    def get_urls(cls, message):
        for match in cls.URL_REGEX.finditer(message):
            yield match.group(1)

    @classmethod
    def get_music_urls(cls, message):
        urls = cls.get_urls(message)
        unique_urls = set()
        for url in urls:
            if url not in unique_urls:
                unique_urls.add(url)
                music_url = cls.__to_music_url(url)
                if music_url:
                    yield music_url

    @classmethod
    def __to_music_url(cls, url):
        """
        Returns instance of MusicUrl with provider if possible
        :param url: url to parse
        :return: MusicUrl
        """
        for provider in INPUT_PROVIDERS:
            if provider.is_music_url(url):
                return MusicUrl(url, provider())
