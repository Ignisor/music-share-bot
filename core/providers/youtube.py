import os
import re

from botocore.vendored import requests

from core.providers.base import MusicProvider

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')


class YouTube(MusicProvider):
    NAME = 'YouTube'
    _ID_REGEX = re.compile(r'\?.*v=([\w]+)')
    _MUSIC_URL = 'https://youtube.com/watch?v={}'

    def get_music_name(self, url):
        api_url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'part': 'snippet',
            'id': self.__id_from_url(url),
            'fields': 'items/snippet/title,items/snippet/description,items/snippet/tags',
            'key': YOUTUBE_API_KEY,
        }
        resp = requests.get(url=api_url, params=params)
        resp.raise_for_status()

        data = resp.json()
        description = data['items'][0]['snippet']['description']
        lines = [line for line in description.split('\n') if line]

        # Temporary terrible solution due to youtube inconsistent descriptions
        try:
            title, performer = lines[1].split(' · ')
            name = f'{performer} - {title}'
        except ValueError:

            # Check for title
            title = data['items'][0]['snippet']['title']

            # It is an assumption that the very first tag is an performer itself
            performer = data['items'][0]['snippet']['tags'][0]

            if performer.lower() in title.lower():

                # Remove strings like "(Official video)" or "feat" from title, not to mess with other providers search
                name = re.sub(r"[\(\[].*?[\)\]]", "", title)
                for dirt in ["ft.", "feat", "vs."]:
                    if dirt in name:
                        name = name.replace(dirt, "")
            else:

                # This is the case of auto generated videos without performer in title
                name = f'{performer} - {title}'
        return name

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
        url = self._MUSIC_URL.format(video_id)

        return url

    def __id_from_url(self, url):
        id_search = self._ID_REGEX.search(url)
        return id_search.group(1)

    @classmethod
    def is_music_url(cls, url):
        if 'youtube.com' in url and 'music.youtube' not in url:
            return True
        
        return False
