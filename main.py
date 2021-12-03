import datetime
import logging

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from bot.menu import menu
from bot.start import start
from bot.paste import paste_show_c, paste_show_b, paste_add_c, paste_members_b, paste_add_b, paste_remove_b
from bot.games_avis import update_avis_games, avis_games
from bot.workout import workout_c, workout_b, delay_button, absent_button, terminate_button, person_absent_button, \
                        person_delay_button, show_fines
from bot.edit import edit_b, edit_bool, edit_number, edit_answer_bool, edit_answer_number
from bot.new_user import new, my_id
from bot.day import check_bday
from bot.score import score_edit, score_edit_press, score_view_b, score_view_c

from utils.conversation_handler import register_handler

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
    dispatcher.add_handler(CommandHandler('new', new))
    dispatcher.add_handler(CommandHandler('id', my_id))
    dispatcher.add_handler(CommandHandler('day', check_bday))
    dispatcher.add_handler(CommandHandler('score', score_view_c))


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
    dispatcher.add_handler(CallbackQueryHandler(show_fines, pattern="workout_fines"))

    dispatcher.add_handler(CallbackQueryHandler(edit_b, pattern="edit_main"))
    dispatcher.add_handler(CallbackQueryHandler(edit_bool, pattern="^edit_bool_.*$"))
    dispatcher.add_handler(CallbackQueryHandler(edit_answer_bool, pattern="^edit_ans_.*$"))
    dispatcher.add_handler(CallbackQueryHandler(edit_number, pattern="edit_number"))
    dispatcher.add_handler(CallbackQueryHandler(edit_answer_number, pattern="edit_set_num_.*$"))

    dispatcher.add_handler(CallbackQueryHandler(score_view_b, pattern="score_view"))
    dispatcher.add_handler(CallbackQueryHandler(score_edit, pattern="score_edit"))
    dispatcher.add_handler(CallbackQueryHandler(score_edit_press, pattern="score_press_.*$"))

    # register
    dispatcher.add_handler(register_handler)

    # JOB QUEUE

    job_queue = updater.job_queue
    # job_queue.run_daily(check_bday, time=datetime.time(15, 30, 0), context=None)

    updater.start_polling()

    print("bot online")
