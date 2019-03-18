import os

from core import process_message
from interfaces.base import BotInterface

from botocore.vendored import requests


class TelegramInterface(BotInterface):
    API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

    def process_message(self, message_data):
        message = message_data['message']
        response = process_message(message['text'])

        if response:
            self._send_message(response, message['chat']['id'], message['message_id'])

    def _send_message(self, message, chat_id, message_id):
        url = self.API_URL + 'sendMessage'
        params = {
            'text': message,
            'chat_id': chat_id,
            'parse_mode': 'Markdown',
            'reply_to_message_id': message_id,
            'disable_web_page_preview': True
        }
        requests.get(url, params=params)

    def get_updates(self, offset=None, timeout=30):
        url = self.API_URL + 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(url, params=params)
        return resp.json()['result']

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[-1]
            return last_update
        return

    def get_chat_id(self, update):
        chat_id = update['message']['chat']['id']
        return chat_id
