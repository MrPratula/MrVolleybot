import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from bot.menu import menu
from bot.start import start
from bot.paste import paste_show_c, paste_show_b, paste_add_c, paste_members_b, paste_add_b, paste_remove_b
from bot.games import update_avis_games, avis_games
from bot.workout import workout_c, workout_b, delay_button, absent_button, terminate_button, person_absent_button, \
                        person_delay_button

from utils.get_from_config import get_key


if __name__ == '__main__':

    key = get_key()

    updater = Updater(token=key, use_context=True)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher = updater.dispatcher

    #   COMMANDS
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('menu', menu))
    dispatcher.add_handler(CommandHandler('paste', paste_show_c))
    dispatcher.add_handler(CommandHandler('add', paste_add_c))
    dispatcher.add_handler(CommandHandler('up_avis', update_avis_games))
    dispatcher.add_handler(CommandHandler('game', avis_games))
    dispatcher.add_handler(CommandHandler('late', workout_c))

    #   BUTTONS
    dispatcher.add_handler(CallbackQueryHandler(paste_show_b, pattern="paste_show"))
    dispatcher.add_handler(CallbackQueryHandler(paste_members_b, pattern="^paste_members_.*$"))
    dispatcher.add_handler(CallbackQueryHandler(paste_add_b, pattern="^paste_add_.*$"))
    dispatcher.add_handler(CallbackQueryHandler(paste_remove_b, pattern="^paste_remove_.*$"))

    dispatcher.add_handler(CallbackQueryHandler(avis_games, pattern="game"))

    dispatcher.add_handler(CallbackQueryHandler(workout_b, pattern="workout_start"))
    dispatcher.add_handler(CallbackQueryHandler(delay_button, pattern="workout_delay"))
    dispatcher.add_handler(CallbackQueryHandler(absent_button, pattern="workout_absent"))
    dispatcher.add_handler(CallbackQueryHandler(person_absent_button, pattern="^workout_abs_.*$"))
    dispatcher.add_handler(CallbackQueryHandler(person_delay_button, pattern="^workout_del_.*$"))
    dispatcher.add_handler(CallbackQueryHandler(terminate_button, pattern="workout_end"))

    updater.start_polling()

    print("bot online")
