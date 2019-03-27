from core.providers import OUTPUT_PROVIDERS
from core.urls import UrlsExtractor

BOT_RESPONSE = '{music_urls}'
MUSIC_FROMAT = '{name}:\n{urls}'


def process_message(message):
    msg_urls = UrlsExtractor.get_music_urls(message)
    if not msg_urls:
        return None

    musics = {}
    for url in msg_urls:
        name = url.get_name()
        if not name:
            return None

        # if user sent two links to one song we skip 2nd..n
        if musics.get(name):
            continue

        musics[name] = []

        for provider in OUTPUT_PROVIDERS:
            if type(url.provider) == provider:
                alternative_url = f'[{provider.NAME}]({url.url})'
            else:
                try:
                    alternative_url = f'[{provider.NAME}]({provider().get_music_url(name)})'
                except Exception:
                    alternative_url = None

            if alternative_url:
                musics[name].append(alternative_url)

    musics_texts = []
    for name, music_urls in musics.items():
        musics_texts.append(MUSIC_FROMAT.format(name=name, urls='\n'.join(music_urls)))

    if musics_texts:
        response = BOT_RESPONSE.format(music_urls='\n'.join(musics_texts))
    else:
        response = None

    return response
