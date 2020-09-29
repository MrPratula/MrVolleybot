import logging

from utils import text, fastChat, CH_JQ

from utils.messageUtils import send_text

from telegram.ext import Updater

if __name__ == '__main__':

    try:
        with open("files/key.txt", "r") as fKey:
            key = fKey.readline()
    except FileNotFoundError:
        print(text.keyError)
        exit(1)

    updater = Updater(token=key, use_context=True)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    CH_JQ.init_command_handler(updater)
    CH_JQ.init_job_queue(updater)

    send_text(fastChat.getPRADA(), 'Service ON')

    updater.start_polling()
