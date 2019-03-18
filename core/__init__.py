from core.providers import ALL_PROVIDERS
from core.urls import UrlsExtractor

BOT_RESPONSE = '{music_urls}'
MUSIC_FROMAT = '{name}:\n{urls}'


def process_message(message):
    msg_urls = UrlsExtractor.get_music_urls(message)
    musics = {}
    for url in msg_urls:
        name = url.get_name()
        musics[name] = []

        for provider in ALL_PROVIDERS:
            if type(url.provider) == provider:
                alternative_url = f'[{provider.NAME}]({url.url})'
            else:
                alternative_url = f'[{provider.NAME}]({provider().get_music_url(name)})'
            musics[name].append(alternative_url)

    musics_texts = []
    for name, music_urls in musics.items():
        musics_texts.append(MUSIC_FROMAT.format(name=name, urls='\n'.join(music_urls)))
    response = BOT_RESPONSE.format(music_urls='\n'.join(musics_texts))

    return response
