import re

import requests

from core.providers.base import MusicProvider

YOUTUBE_API_KEY = 'AIzaSyDVjLd6MAuJsDXJhbxjVmOAaoduoO4K1Bs'


class YouTube(MusicProvider):
    NAME = 'YouTube'
    _ID_REGEX = re.compile(r'\?.*v=([\w]+)')
    __MUSIC_URL = 'https://youtube.com/watch?v={}'

    def get_music_name(self, url):
        api_url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part': 'snippet',
            'id': self.__id_from_url(url),
            'fields': 'items/snippet/title,items/snippet/description',
            'key': YOUTUBE_API_KEY,
        }

        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        description = data['items'][0]['snippet']['description']
        lines = [line for line in description.split('\n') if line]
        title, performer = lines[1].split(' · ')

        return f'{performer} - {title}'

    def get_music_url(self, name):
        api_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet', 
            'maxResults': 1, 
            'q': name,
            'key': YOUTUBE_API_KEY,
        }

        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        video_id = data['items'][0]['id']['videoId']
        url = self.__MUSIC_URL.format(video_id)

        return url

    def __id_from_url(self, url):
        id_search = self._ID_REGEX.search(url)
        return id_search.group(1)

    @classmethod
    def is_music_url(cls, url):
        if 'youtube.com' in url and 'music.youtube' not in url:
            return True
        
        return False
