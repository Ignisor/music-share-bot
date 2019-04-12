# Bot for better music sharing
This is a bot which purpose is to simplify music sharing for users of different music streaming services.

## Using
Python 3.7

## Currently supported providers and interfaces
### Providers (music services)
-   [YouTube Music](https://music.youtube.com/)
-   [YouTube](https://www.youtube.com/) (Output only)
-   [Spotify](https://www.spotify.com/)
-   [Apple Music](https://www.apple.com/ru/apple-music/)
-   [Deezer](https://www.deezer.com)
-   [Google Play Music](https://play.google.com/music)
-   [SoundCloud](https://soundcloud.com/)

### Interfaces (apps and bots)
-   [Telegram](https://telegram.org/)

## Installation
-   Clone the project:
    ```bash
    git clone git@github.com:Ignisor/music-share-bot.git
    ```

-   Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

-   Required environment variables:
	-   SPOTIFY_CLIENT_ID - client ID for Spotify API
	-   SPOTIFY_CLIENT_SECRET - client secret key for Spotify API
	-   YOUTUBE_API_KEY - API key for youtube API

-   Optional environment variables:
    	-   BOT_ADMINS_CHAT - if you set admins chat (eg @our_chat) bot messages will have 'report button'. if click - bot forwards messages to admins chat

### For development
-   Install local requirements:
    ```bash
    pip install -r local_requirements.txt
    ```

### Amazon Lambda
Deployment to the Amazon Lambda is currently handled by CD using [Buddy](https://app.buddy.works/).

#### [Telegram](https://telegram.org/)
The [telegram_lambda.py](telegram_lambda.py) used as entrypoint for Telegram BOT interface. 

That interface uses [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library. To handle dependencies in lambda recommended way is to install them using `--target` attribure of `pip install` command. E.g. `pip install -r requirements.txt --target package/`. And then add the target folder to `PYTHONPATH` environment variable.

Bot token must be specified in `TELEGRAM_BOT_TOKEN` environment variable.

## Contributing
Pull requests are welcome. `dev` - is the main branch. For major changes, please open an issue first to discuss what you would like to change.

Don't forget to update **README.md** and **requirements.txt** if needed.

## License
[MIT](https://choosealicense.com/licenses/mit/)
