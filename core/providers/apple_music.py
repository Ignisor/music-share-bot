import re

from botocore.vendored import requests

from core.providers.base import MusicProvider


class AppleMusic(MusicProvider):
    NAME = 'Apple Music'
    _ID_REGEX = re.compile(r'\?.*i=([\w]+)')
    _MUSIC_URL = 'https://itunes.apple.com/us/album/{}/{}?i={}'

    def get_music_name(self, url):
        api_url = 'https://itunes.apple.com/lookup'

        params = {
            'id': self.__id_from_url(url),
            'entity': 'song'
        }
        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        if data['resultCount']:
            performer = data['results'][0]['artistName']
            title = data['results'][0]['trackName']
            return f'{performer} - {title}'
        return None

    def get_music_url(self, name):
        api_url = 'https://itunes.apple.com/search?'
        params = {
            'term': name,
            'entity': 'song'
        }

        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        track_name = re.sub(r"[\(\[].*?[\)\]]", "", data['results'][0]['trackName'])
        collection_id = data['results'][0]['collectionId']
        track_id = data['results'][0]['trackId']
        url = self._MUSIC_URL.format(track_name, collection_id, track_id)
        return url

    def __id_from_url(self, url):
        id_search = self._ID_REGEX.search(url)
        return id_search.group(1)

    @classmethod
    def is_music_url(self, url):
        if 'itunes.apple' in url:
            return True

        return False
