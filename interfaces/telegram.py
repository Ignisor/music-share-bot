from core import process_message
from interfaces.base import BotInterface

from botocore.vendored import requests


class TelegramInterface(BotInterface):
    API_TOKEN = '826840330:AAFxyiXEr3fAFCYdc-CdLch0AIFNodOXqi0'
    API_URL = f'https://api.telegram.org/bot{API_TOKEN}/'

    def process_message(self, message_data):
        message = message_data['message']
        response = process_message(message['text'])

        self._send_message(response, message['chat']['id'])

    def _send_message(self, message, chat_id):
        url = self.API_URL + 'sendMessage'
        params = {
            'text': message,
            'chat_id': chat_id,
        }
        requests.get(url, params=params)
