from botocore.vendored import requests
from bs4 import BeautifulSoup


from core.providers.base import MusicProvider

class GoogleMusic(MusicProvider):
    NAME = 'Google Music'

    @classmethod
    def is_music_url(self, url):
        if 'play.google.com/music' in url:
            return True

        return False

    def get_music_url(self, name):
        raise NotImplementedError


    def get_music_name(self, url):
        g_music_page = requests.get(url)
        soup = BeautifulSoup(g_music_page.content, 'html.parser')
        title = soup.find('div', class_='title fade-out')
        artist = soup.find('div', class_='album-artist fade-out')
        if title and artist:
            return f'{artist.text} - {title.text}'

        return soup.find('meta', property='og:title').get('content')
