import paste.paste
import manage.start

from telegram.ext import CommandHandler

from day.checkDay import auto_checkBday
from utils import times


def init_command_handler(updater):
    dispatcher = updater.dispatcher

    # Intro

    dispatcher.add_handler(CommandHandler('start', manage.start.start))
    dispatcher.add_handler(CommandHandler('help', manage.start.help))
    dispatcher.add_handler(CommandHandler('test', manage.start.test))

    # Food stuff

    dispatcher.add_handler(CommandHandler('paste', paste.paste.showList))
    dispatcher.add_handler(CommandHandler('add', paste.paste.addPerson))
    dispatcher.add_handler(CommandHandler('pop', paste.paste.pop))
    dispatcher.add_handler(CommandHandler('remove', paste.paste.remove))


def init_job_queue(updater):
    job_queue = updater.job_queue

    # Bday stuff
    job_queue.run_daily(auto_checkBday, times.test_time)
