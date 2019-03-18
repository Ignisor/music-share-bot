import base64
import os

import requests
from core.providers.base import MusicProvider

SPOTIFY_API_TOKEN = None

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

class Spotify(MusicProvider):
    NAME = 'Spotify'
    _MUSIC_URL = 'https://open.spotify.com/track/{}'


    def get_access_token(self):
        api_url = 'https://accounts.spotify.com/api/token'

        auth_str = bytes('{}:{}'.format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET), 'utf-8')
        b64_auth_str = base64.b64encode(auth_str).decode('utf-8')
        headers = {
                'Authorization': f'Basic {b64_auth_str}',
            }

        resp = requests.post(
            url=api_url,
            headers=headers,
            data={"grant_type": "client_credentials"}
        )
        SPOTIFY_API_TOKEN = resp.json()['access_token']
        return SPOTIFY_API_TOKEN

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
        track_id = data['tracks']['items'][0]['id']
        url = self._MUSIC_URL.format(track_id)
        return url

    def __id_from_url(self, url):
        id_search = url.split('/')[-1]
        return id_search

    def get_headers(self):

        if not SPOTIFY_API_TOKEN:
            return {
                "Authorization": f'Bearer {self.get_access_token()}'
            }

        return {
                "Authorization": f'Bearer {SPOTIFY_API_TOKEN}'
            }


    @classmethod
    def is_music_url(self, url):
        if 'open.spotify' in url:
            return True

        return False
