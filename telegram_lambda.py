import json

from interfaces.telegram import TelegramInterface


def lambda_handler(event, context):
    message_data = json.loads(event['body'])
    interface = TelegramInterface()

    try:
        interface.process_message(message_data)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'error: {repr(e)}',
        }

    return {
        'statusCode': 200
    }
