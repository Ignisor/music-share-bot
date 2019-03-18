import os

from botocore.vendored import requests
from core.providers.base import MusicProvider

SPOTIFY_API_TOKEN = os.environ.get('SPOTIFY_API_TOKEN')


class Spotify(MusicProvider):
    NAME = 'Spotify'
    _MUSIC_URL = 'https://open.spotify.com/track/{}'

    def get_music_name(self, url):
        api_url = 'https://api.spotify.com/v1/tracks/{}'

        resp = requests.get(url=api_url.format(self.__id_from_url(url)), headers=self.get_headers())
        resp.raise_for_status()

        data = resp.json()
        return f'{data["artists"][0]["name"]} - {data["name"]}'

    def get_music_url(self, name):
        api_url = 'https://api.spotify.com/v1/search'
        params = {
            'q': name,
            'type': "track",
        }

        resp = requests.get(url=api_url, params=params, headers=self.get_headers())
        resp.raise_for_status()

        data = resp.json()
        track_id = data['tracks']["items"][0]['id']
        url = self._MUSIC_URL.format(track_id)
        return url

    def __id_from_url(self, url):
        id_search = url.split('/')[-1]
        return id_search

    @staticmethod
    def get_headers():
        return {
            "Authorization": "Bearer {}".format(SPOTIFY_API_TOKEN)
        }

    @classmethod
    def is_music_url(self, url):
        if 'open.spotify' in url:
            return True

        return False
