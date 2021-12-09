from telegram import InlineKeyboardMarkup

from dao.user_dao import user_exist, get_actives_nick
from utils.db import connect

from utils.lang import text
from utils.keyboard import array_to_keyboard


def paste_show_c(update, context):

    if not user_exist(update.message.from_user.id):
        update.message.reply_text("unauthorized")
        return

    paste_list = get_paste_list()

    message = text("paste_show").format("\n".join(paste_list))

    update.message.reply_text(message)


def paste_show_b(update, context):

    paste_list = get_paste_list()

    message = text("paste_show").format("\n".join(paste_list).title())

    update.callback_query.edit_message_text(message)


def paste_add_c(update, context):

    if not user_exist(update.message.from_user.id):
        update.message.reply_text("unauthorized")
        return

    try:
        name = context.args[0]
    except IndexError:
        message = text("paste_no_name")
        update.message.reply_text(message)
        return

    add_paste(name)
    message = text("paste_add").format(name.capitalize())
    update.message.reply_text(message)


def paste_members_b(update, context):

    c_query = update.callback_query
    choice = c_query.data[14:]

    if choice == "add":
        members = get_actives_nick()
        members.append("Annulla  ❌")
        keyboard = array_to_keyboard(members, "paste_add")
        message = text("paste_add_choice")

    else:
        members = get_paste_list()
        members.append("Annulla  ❌")
        keyboard = array_to_keyboard(members, "paste_remove")
        message = text("paste_remove_choice")

    reply_markup = InlineKeyboardMarkup(keyboard)

    c_query.edit_message_text(message, reply_markup=reply_markup)


def paste_add_b(update, context):

    c_query = update.callback_query
    choice = c_query.data[10:]

    if choice == "Annulla  ❌":
        message = text("paste_none")

    else:

        add_paste(choice)
        message = text("paste_add").format(choice.capitalize())

    c_query.edit_message_text(message)


def paste_remove_b(update, context):

    c_query = update.callback_query
    choice = c_query.data[13:]

    if choice == "Annulla  ❌":
        message = text("paste_none")

    else:

        remove_paste(choice)
        message = text("paste_remove").format(choice.capitalize())

    c_query.edit_message_text(message)


#   DAO


def get_paste_list():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT name FROM paste"

    try:

        cursor.execute(query, ())
        result = cursor.fetchall()

    except:
        print("can not get paste list")
        return None

    paste = []
    for person in result:
        paste.append(person[0])

    return paste


def add_paste(name):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "INSERT INTO paste (name) VALUES (%s)"

    try:
        cursor.execute(query, (name,))
        db.commit()
    except:
        print("can not add person into paste")


def remove_paste(name):

    db = connect()
    cursor = db.cursor(prepared=True)
    query = "DELETE FROM paste WHERE name = %s LIMIT 1"

    try:
        cursor.execute(query, (name,))
        db.commit()
    except:
        print("can not delete person from lista paste")
