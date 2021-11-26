import datetime

from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from utils.lang import text
from utils.notify import notify_admin

NAME, SURNAME, NICKNAME, BDAY, ACTIVE, SUB_AVIS, SUB_A = range(7)


def register(update, context):
    message = text("register_start")
    update.message.reply_text(message)

    return NAME


def cancel(update, context):
    message = text("register_cancel")
    update.message.reply_text(message)

    return ConversationHandler.END


def name(update, context):
    user_name = update.message.text
    chat_id = update.message.from_user.id

    context.user_data.update({"name": user_name})
    context.user_data.update({"id": chat_id})

    message = text("register_name")
    update.message.reply_text(message)

    return SURNAME


def surname(update, context):
    user_surname = update.message.text
    context.user_data.update({"surname": user_surname})

    message = text("register_surname")
    update.message.reply_text(message)

    return NICKNAME


def nickname(update, context):
    user_nickname = update.message.text
    context.user_data.update({"nickname": user_nickname})

    message = text("register_nickname")
    update.message.reply_text(message)

    return BDAY


def bday(update, context):
    user_bday = update.message.text

    try:
        bday_array = user_bday.split("-")

        if len(bday_array) == 1:
            bday_array = user_bday.split("/")

        day = int(bday_array[0])
        month = int(bday_array[1])
        year = int(bday_array[2])

        bday_date = datetime.date(year, month, day)

    except Exception:
        message = text("register_bad_bday")
        update.message.reply_text(message)
        return BDAY

    context.user_data.update({"bday": bday_date})

    message = text("register_bday")
    keyboard = [["SI", "NO"]]
    placeholder = text("register_placeholder")
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True,
                                       input_field_placeholder=placeholder)
    update.message.reply_text(message, reply_markup=reply_markup)

    return ACTIVE


def active(update, context):
    answer = update.message.text.upper()

    if answer != "SI" and answer != "NO":
        message = text("register_active_fail")
        keyboard = [["SI", "NO"]]
        placeholder = text("register_placeholder")
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True,
                                           input_field_placeholder=placeholder)
        update.message.reply_text(message, reply_markup=reply_markup)
        return ACTIVE

    elif answer == "SI":
        user_active = True
    else:
        user_active = False

    context.user_data.update({"active": user_active})

    message = text("register_active")
    keyboard = [["SI", "NO"]]
    placeholder = text("register_placeholder")
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True,
                                       input_field_placeholder=placeholder)
    update.message.reply_text(message, reply_markup=reply_markup)

    return SUB_AVIS


def sub_avis(update, context):
    answer = update.message.text.upper()

    if answer != "SI" and answer != "NO":
        message = text("register_sub_avis_fail")
        keyboard = [["SI", "NO"]]
        placeholder = text("register_placeholder")
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True,
                                           input_field_placeholder=placeholder)
        update.message.reply_text(message, reply_markup=reply_markup)
        return ACTIVE

    elif answer == "SI":
        user_sub_avis = True
    else:
        user_sub_avis = False

    context.user_data.update({"sub_avis": user_sub_avis})

    message = text("register_sub_avis")
    keyboard = [["SI", "NO"]]
    placeholder = text("register_placeholder")
    reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True,
                                       input_field_placeholder=placeholder)
    update.message.reply_text(message, reply_markup=reply_markup)

    return SUB_A


def sub_a(update, context):
    answer = update.message.text.upper()

    if answer != "SI" and answer != "NO":
        message = text("register_sub_a_fail")
        keyboard = [["SI", "NO"]]
        placeholder = text("register_placeholder")
        reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True, resize_keyboard=True,
                                           input_field_placeholder=placeholder)
        update.message.reply_text(message, reply_markup=reply_markup)
        return ACTIVE

    elif answer == "SI":
        user_sub_a = True
    else:
        user_sub_a = False

    u_id = context.user_data["id"]
    u_name = context.user_data["name"]
    u_surname = context.user_data["surname"]
    u_nick = context.user_data["nickname"]
    u_bday = context.user_data["bday"]
    u_active = context.user_data["active"]
    u_avis_sub = context.user_data["sub_avis"]

    message = text("register_sub_a")
    admin_message = text("register_admin").format(u_id, u_name, u_surname, u_nick, u_bday, u_active, u_avis_sub,
                                                  user_sub_a)

    notify_admin(admin_message, context.bot)
    update.message.reply_text(message)

    return ConversationHandler.END
