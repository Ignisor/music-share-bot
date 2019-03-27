import os

from telegram import Bot, Update, MessageEntity, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater, CallbackQueryHandler

from core import process_message
from interfaces.base import BotInterface


class TelegramInterface(BotInterface):
    API_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    ADMINS_CHAT = os.environ.get('BOT_ADMINS_CHAT')

    def __init__(self):
        self.bot = Bot(self.API_TOKEN)
        self.dispatcher = Dispatcher(self.bot, None, workers=0)
        self._init_handlers()

    def _init_handlers(self):
        handlers = [
            MessageHandler(
                Filters.text & (Filters.entity(MessageEntity.URL) | Filters.entity(MessageEntity.TEXT_LINK)),
                self._handle_message
            ),

            CallbackQueryHandler(
                self._handle_mismatch_button
            )
        ]

        for handler in handlers:
            self.dispatcher.add_handler(handler)

    def _handle_message(self, bot, update):
        text = update.message.text
        response = process_message(text)

        response_keyboard = TelegramInterface.get_keyboard(update.message)

        if response:
            update.message.reply_markdown(
                response,
                quote=True,
                disable_web_page_preview=True,
                disable_notification=True,
                reply_markup=response_keyboard
            )

    def _handle_mismatch_button(self, bot, update):
        if TelegramInterface.ADMINS_CHAT:
            user_message_id = update.callback_query.message.reply_to_message.message_id
            bad_response_message_id = update.callback_query.message.message_id
            message_chat_id = update.callback_query.message.chat.id

            bot.forwardMessage(chat_id=TelegramInterface.ADMINS_CHAT, from_chat_id=message_chat_id,
                               message_id=user_message_id)
            bot.forwardMessage(chat_id=TelegramInterface.ADMINS_CHAT, from_chat_id=message_chat_id,
                               message_id=bad_response_message_id)

            bot.edit_message_reply_markup(chat_id=message_chat_id,
                                  message_id=bad_response_message_id,
                                  reply_markup=None)


    def process_message(self, message_data):
        update = Update.de_json(message_data, self.bot)
        self.dispatcher.process_update(update)

    @staticmethod
    def get_keyboard(message):
        if TelegramInterface.ADMINS_CHAT:
            message_id = message.message_id
            feedback_button = InlineKeyboardButton(text="report mismatch",
                                                   callback_data='/bad_response {}'.format(message_id))
            buttons = [[feedback_button]]
            return InlineKeyboardMarkup(inline_keyboard=buttons)



class TelegramUpdaterInterface(TelegramInterface):
    def __init__(self):
        self.updater = Updater(token=self.API_TOKEN, use_context=False)
        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher
        self._init_handlers()

    def run_updater(self):
        self.updater.start_polling()
        self.updater.idle()
        self.updater.stop()
