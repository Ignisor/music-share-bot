import os

import requests
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
            song_info = title_and_artist_tag.text.split('|')[0]
            artist_and_title = song_info.split(' by ')[0]

            # it is my observation, could be just some garbage in the name
            if len(artist_and_title) > 40:
                title = artist_and_title.split(' - ')[1]
                return f'{title}'
            return f'{artist_and_title}'

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
