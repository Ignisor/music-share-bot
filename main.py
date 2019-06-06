# Entrypoint for Google Cloud Functions

from interfaces.telegram import TelegramInterface
from flask import escape


def telegram_gc_function_handler(request):
    message_data = request.get_json()
    interface = TelegramInterface()

    try:
        interface.process_message(message_data)
    except Exception as e:
        msg = f'error: {escape(repr(e))}'
        print(msg)

        return msg

    return 'success'
