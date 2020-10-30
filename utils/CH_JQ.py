
from utils import times
from telegram.ext import CommandHandler, MessageHandler, Filters

from paste import paste
from manage import start, administration, db_interaction
from day.checkDay import auto_checkBday
from manage.log import save_text


def init_command_handler(updater):
    dispatcher = updater.dispatcher

    # Intro

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_text))
    dispatcher.add_handler(CommandHandler('start', start.start))
    dispatcher.add_handler(CommandHandler('help', start.help))
    dispatcher.add_handler(CommandHandler('man', start.man))
    dispatcher.add_handler(CommandHandler('test', start.test))

    # Management

    dispatcher.add_handler(CommandHandler('ban', administration.ban))
    dispatcher.add_handler(CommandHandler('kick', administration.kick))
    dispatcher.add_handler(CommandHandler('unban', administration.unban))

    # DB interactions

    dispatcher.add_handler(CommandHandler('register', db_interaction.register))
    dispatcher.add_handler(CommandHandler('nickname', db_interaction.edit_nickname))
    dispatcher.add_handler(CommandHandler('number', db_interaction.edit_number))
    dispatcher.add_handler(CommandHandler('active', db_interaction.change_active))
    dispatcher.add_handler(CommandHandler('members', db_interaction.members))

    # Food stuff

    dispatcher.add_handler(CommandHandler('paste', paste.showList))
    dispatcher.add_handler(CommandHandler('add', paste.addPerson))
    dispatcher.add_handler(CommandHandler('pop', paste.pop))
    dispatcher.add_handler(CommandHandler('remove', paste.remove))


def init_job_queue(updater):
    job_queue = updater.job_queue

    # Bday stuff
    job_queue.run_daily(auto_checkBday, times.every_day)
