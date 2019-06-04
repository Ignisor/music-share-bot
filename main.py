# Entrypoint for Google Cloud Functions

from interfaces.telegram import TelegramInterface


def telegram_gc_function_handler(request):
    message_data = request.get_json()
    interface = TelegramInterface()

    try:
        interface.process_message(message_data)
    except Exception as e:
        return f'error: {repr(e)}'

    return 'success'
