
import datetime

from telegram import InlineKeyboardMarkup

from dao.user_dao import user_exist, get_user_nick, how_many
from dao.workout_dao import add_delay, add_absence, get_today_delay, get_today_absences
from utils.keyboard import keyboard_late
from utils.lang import text


def workout_c(update, context):

    if not user_exist(update.message.from_user.id):
        update.message.reply_text("unauthorized")
        return

    keyboard = keyboard_late()

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = text("workout_start").format(datetime.date.today())

    update.message.reply_text(message, reply_markup=reply_markup)


def workout_b(update, context):

    query = update.callback_query
    keyboard = keyboard_late()

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = text("workout_start").format(datetime.date.today())

    query.edit_message_text(message, reply_markup=reply_markup)


def delay_button(update, context):

    query = update.callback_query
    add_delay(query.from_user.id)

    message = generate_workout_text(False)

    keyboard = keyboard_late()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)


def absent_button(update, context):

    query = update.callback_query
    add_absence(query.from_user.id)

    message = generate_workout_text(False)

    keyboard = keyboard_late()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)


def terminate_button(update, context):

    query = update.callback_query
    message = generate_workout_text(True)
    query.edit_message_text(message)


def generate_workout_text(finish):

    delays_id = get_today_delay()
    delays_names = []
    absences_id = get_today_absences()
    absences_names = []

    try:
        for user_id in delays_id:
            delays_names.append(get_user_nick(user_id))
        delay_people = "\n".join(delays_names)
    except:
        delay_people = "Nessuno"

    try:
        for user_id in absences_id:
            absences_names.append(get_user_nick(user_id))
        absent_people = "\n".join(absences_names)

    except:
        absent_people = "Nessuno"

    if not finish:
        message = text("workout_progress").format(datetime.date.today(), delay_people, absent_people)
    else:
        message = text("workout_end").format(datetime.date.today(), how_many()-len(absences_names),
                                             ", ".join(delays_names), ", ".join(absences_names))

    return message


def workout_count(update, context):

    query = update.callback_query
    query.edit_message_text("devo ancora farla")
