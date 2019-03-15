import re

import requests

from core.providers.youtube import YouTube

YOUTUBE_API_KEY = 'AIzaSyDVjLd6MAuJsDXJhbxjVmOAaoduoO4K1Bs'


class YouTubeMusic(YouTube):
    NAME = 'YouTube Music'
    _MUSIC_URL = 'https://music.youtube.com/watch?v={}'

    @classmethod
    def is_music_url(self, url):
        if 'music.youtube' in url:
            return True
        
        return False
