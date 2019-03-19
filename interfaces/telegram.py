import os

from telegram import Bot, Update, MessageEntity
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater

from core import process_message
from interfaces.base import BotInterface


class TelegramInterface(BotInterface):
    API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

    def __init__(self):
        self.bot = Bot(self.API_TOKEN)
        self.dispatcher = Dispatcher(self.bot, None, workers=0)
        self._init_handlers()

    def _init_handlers(self):
        handlers = [
            MessageHandler(
                Filters.text & (Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK)),
                self._handle_message
            )
        ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def _handle_message(self, update, context):
        text = update.message.text
        response = process_message(text)

        if response:
            update.message.reply_markdown(
                response,
                quote=True,
                disable_web_page_preview=True,
                disable_notification=True,
            )

    def process_message(self, message_data):
        update = Update.de_json(message_data, self.bot)
        self.dispatcher.process_update(update)


class TelegramUpdaterInterface(TelegramInterface):
    def __init__(self):
        self.updater = Updater(token=self.API_TOKEN, use_context=True)
        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher
        self._init_handlers()

    def run_updater(self):
        self.updater.start_polling()
        self.updater.idle()
        self.updater.stop()
