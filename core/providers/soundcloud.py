import os

from botocore.vendored import requests
from bs4 import BeautifulSoup

from core.providers.base import MusicProvider

SOUNDCLOUD_CLIENT_ID = os.environ.get('SOUNDCLOUD_CLIENT_ID')


class SoundCloud(MusicProvider):
    NAME = 'SoundCloud'
    _MUSIC_URL = 'https://soundcloud.com/{}/{}'

    def get_music_name(self, url):
        soundcloud_page = requests.get(url)
        soup = BeautifulSoup(soundcloud_page.content, 'html.parser')
        title_and_artist_tag = soup.find('title')

        if title_and_artist_tag:
            song_title = title_and_artist_tag.text.split('|')[0]
            song_title_split = song_title.split(' by ')
            return f'{song_title_split[0]}'

    def get_music_url(self, name):
        api_url = 'https://api-v2.soundcloud.com/search'
        params = {
            'q': name,
            'client_id': SOUNDCLOUD_CLIENT_ID,
            'limit': 1,
        }

        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        user = data['collection'][0]['user']['permalink']
        track_link = data['collection'][0]['permalink']
        url = self._MUSIC_URL.format(user, track_link)
        return url

    @classmethod
    def is_music_url(self, url):
        if 'soundcloud' in url:
            return True

        return False
