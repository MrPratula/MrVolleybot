
from utils import times
from telegram.ext import CommandHandler


from paste import paste
from manage import start, administration
from day.checkDay import auto_checkBday


def init_command_handler(updater):
    dispatcher = updater.dispatcher

    # Intro

    dispatcher.add_handler(CommandHandler('start', start.start))
    dispatcher.add_handler(CommandHandler('help', start.help))
    dispatcher.add_handler(CommandHandler('test', start.test))

    # Management

    dispatcher.add_handler(CommandHandler('ban', administration.ban))
    dispatcher.add_handler(CommandHandler('kick', administration.kick))
    dispatcher.add_handler(CommandHandler('unban', administration.unban))

    # Food stuff

    dispatcher.add_handler(CommandHandler('paste', paste.showList))
    dispatcher.add_handler(CommandHandler('add', paste.addPerson))
    dispatcher.add_handler(CommandHandler('pop', paste.pop))
    dispatcher.add_handler(CommandHandler('remove', paste.remove))


def init_job_queue(updater):
    job_queue = updater.job_queue

    # Bday stuff
    job_queue.run_daily(auto_checkBday, times.test_time)
