import logging

from interfaces.telegram import TelegramUpdaterInterface

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
interface = TelegramUpdaterInterface()


def main():
    interface.run_updater()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
