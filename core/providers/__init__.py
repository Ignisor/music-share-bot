from core.providers.apple_music import AppleMusic
from core.providers.deezer import Deezer
from core.providers.spotify import Spotify
from core.providers.youtube import YouTube
from core.providers.youtube_music import YouTubeMusic
from core.providers.google_music import GoogleMusic


INPUT_PROVIDERS = (YouTubeMusic, AppleMusic, Deezer, Spotify, GoogleMusic)
OUTPUT_PROVIDERS = (YouTube, YouTubeMusic, AppleMusic, Deezer, Spotify)
