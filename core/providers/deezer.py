from botocore.vendored import requests

from core.providers.base import MusicProvider


class Deezer(MusicProvider):
    NAME = 'Deezer'
    _MUSIC_URL = 'http://www.deezer.com/track/{}'

    def get_music_name(self, url):
        api_url = 'http://api.deezer.com/track/{}'

        resp = requests.get(url=api_url.format(self.__id_from_url(url)))
        resp.raise_for_status()

        data = resp.json()
        return f'{data["artist"]["name"]} - {data["title"]}'

    def get_music_url(self, name):
        api_url = 'http://api.deezer.com/search/track'
        params = {
            'q': name,
            'index': 0,
            'limit': 1,
            'output': 'json'
        }

        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        track_id = data['data'][0]['id']
        url = self._MUSIC_URL.format(track_id)
        return url

    @staticmethod
    def __id_from_url(url):
        id_search = url.split('/')[-1]
        return id_search

    @classmethod
    def is_music_url(self, url):
        if 'deezer' in url:
            return True

        return False
