import requests
from bs4 import BeautifulSoup
import urllib.parse

from core.providers.base import MusicProvider

G_LISTEN_URL_TEMPLATE = 'https://play.google.com/music/m/{song_id}?t={title}'
G_STORE_SEARCH_PAGE_TEMPLATE = 'https://play.google.com/store/search?c=music&q={query}'


class NotFoundError(Exception):
    pass

class GoogleMusic(MusicProvider):
    NAME = 'Google Music'

    @classmethod
    def is_music_url(self, url):
        if 'play.google.com/music' in url:
            return True

        return False

    def get_music_url(self, name):
        encoded_name = urllib.parse.quote_plus(name)
        search_url = G_STORE_SEARCH_PAGE_TEMPLATE.format(query=encoded_name)
        store_page = requests.get(search_url)
        if store_page.ok:
            soup = BeautifulSoup(store_page.content, 'html.parser')
            page_divs = soup.find_all('div', class_='details')
            for div in page_divs:
                try:
                    if div.find('a', class_='subtitle')['title'] in name:
                        song_title = div.find('a', class_='title')['title']
                        if song_title in name:
                            song_id = div.find('a', class_='title')['href'].split('tid=song-')[-1]
                            return G_LISTEN_URL_TEMPLATE.format(song_id=song_id, title=encoded_name)
                except (KeyError, ValueError):
                    pass

        raise NotFoundError


    def get_music_name(self, url):
        g_music_page = requests.get(url)
        soup = BeautifulSoup(g_music_page.content, 'html.parser')
        title_and_artist_tag = soup.find('meta', property='og:title')

        if title_and_artist_tag:
            return title_and_artist_tag.get('content')
