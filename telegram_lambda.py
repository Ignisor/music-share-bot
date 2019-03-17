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
            'error': repr(e)
        }

    return {
        'statusCode': 200
    }


interface = TelegramInterface()


def main():
    new_offset = None
    while True:
        interface.get_updates(new_offset)
        last_update = interface.get_last_update()
        if last_update:
            last_update_id = last_update['update_id']

            interface.process_message(last_update)
            new_offset = last_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
