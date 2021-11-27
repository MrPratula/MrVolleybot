import traceback

from telegram import InlineKeyboardMarkup

from dao.user_dao import get_user_nick
from utils.db import connect
from utils.keyboard import keyboard_edit, keyboard_bool, keyboard_numbers
from utils.lang import text


def edit_b(update, context):

    user_id = update.callback_query.from_user.id
    context.user_data.update({"id": user_id})

    nickname = get_user_nick(user_id)
    keyboard = keyboard_edit()
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = text("edit_main").format(nickname)
    update.callback_query.edit_message_text(message, reply_markup=reply_markup)


def edit_number(update, context):

    query = update.callback_query
    keyboard = keyboard_numbers()
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = text("edit_number")

    query.edit_message_text(message, reply_markup=reply_markup)


def edit_bool(update, context):

    query = update.callback_query

    # what = active | avis_sub | monza_sub
    what = query.data[10:]
    context.user_data.update({"what": what})

    message = text(f"edit_{what}")

    keyboard = keyboard_bool()
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(message, reply_markup=reply_markup)


def edit_answer_bool(update, context):

    query = update.callback_query
    answer = query.data[9:]

    if answer == "true":
        state = True
    else:
        state = False

    what = context.user_data["what"]
    user_id = context.user_data["id"]

    change_activity(user_id, what, state)

    message = text(f"edit_{what}_end_{answer}")
    query.edit_message_text(message)


def edit_answer_number(update, context):

    query = update.callback_query
    number = query.data[13:]
    user_id = context.user_data["id"]

    change_user_number(user_id, number)

    message = text("edit_number_end").format(number)
    query.edit_message_text(message)


# DAO

def change_activity(chat_id, what, state):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "UPDATE users SET {} = %s WHERE chat_id = %s ".format(what)

    try:
        cursor.execute(query, (state, chat_id))
        db.commit()
    except Exception:
        print("change_activity() had a problem")
        print(traceback.format_exc())


def change_user_number(user_id, number):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "UPDATE users SET number = %s WHERE chat_id = %s "

    try:
        cursor.execute(query, (number, user_id))
        db.commit()
    except Exception:
        print("change_user_number() had a problem")
        print(traceback.format_exc())


