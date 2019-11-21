import requests
from bs4 import BeautifulSoup
import urllib.parse
from lxml import html

from core.providers.base import MusicProvider

G_LISTEN_URL_TEMPLATE = 'https://play.google.com/music/m/{song_id}'
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

    @staticmethod
    def get_search_res_divs(songs__div):
        return [i.getchildren() for i in songs__div][0]

    def get_music_url(self, name):
        encoded_name = urllib.parse.quote_plus(name)
        search_url = G_STORE_SEARCH_PAGE_TEMPLATE.format(query=encoded_name)
        store_page = requests.get(search_url)
        if store_page.ok:
            tree = html.fromstring(store_page.content)
            main_div = tree.xpath("/html/body/div[1]/div[4]/c-wiz/div")
            h2_songs_tag = [h for h in main_div[0].xpath('.//h2[text()="Songs"]')]
            search_res_divs = self.get_search_res_divs(h2_songs_tag[0].getparent().getparent().getnext())
            if not search_res_divs:
                search_res_divs = self.get_search_res_divs(h2_songs_tag[0].getparent().getparent().getparent().getnext())

            for div in search_res_divs:
                song_divs = div.getchildren()

                for song_div in song_divs:
                    title_divs = song_div.findall('.//div[@title]')
                    song_as = song_div.findall('.//a')

                    artist = song_as[-1].getchildren()[0].text
                    title = title_divs[0].attrib['title']
                    full_song_name = f'{artist} {title}'

                    if any(x in name for x in full_song_name):
                        link = song_as[0].attrib['href']
                        if 'tid=song-' in link:
                            song_id = link.split('tid=song-')[-1]
                        else:
                            song_id = link.split('id=')[-1]

                        link = G_LISTEN_URL_TEMPLATE.format(song_id=song_id)
                        return link
        raise NotFoundError

    def get_music_name(self, url):
        g_music_page = requests.get(url)
        soup = BeautifulSoup(g_music_page.content, 'html.parser')
        title_and_artist_tag = soup.find('meta', property='og:title')

        if title_and_artist_tag:
            return title_and_artist_tag.get('content')
