import json

from interfaces.telegram import TelegramInterface


def aws_lambda_handler(event, context):
    message_data = json.loads(event['body'])
    interface = TelegramInterface()

    try:
        interface.process_message(message_data)
    except Exception as e:
        return {
            'statusCode': 200,
            'body': f'error: {repr(e)}',
        }

    return {
        'statusCode': 200
    }
