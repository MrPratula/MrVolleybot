import datetime

from beans.User import User
from utils import text
from dao import userDao
from manage.security import check_permission


def register(update, context):
    if check_permission(update.message.chat_id) > 0:
        return

    try:
        chat_id = context.args[0]
        name = context.args[1]
        surname = context.args[2]
        bday = context.args[3]

        bday_array = bday.split("-")
        bday_year = int(bday_array[0])
        bday_month = int(bday_array[1])
        bday_day = int(bday_array[2])
    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.wrong_args_new_user)
        return

    try:
        bday_date = datetime.date(year=bday_year, month=bday_month, day=bday_day)
    except:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.wrong_data_format)
        return

    result = userDao.create_new_user(User(chat_id=chat_id, name=name, surname=surname, bday=bday_date))

    if result == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.insert_success)
    elif result == 1:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.chat_id_already_exist)


def edit_nickname(update, context):
    if check_permission(update.message.chat_id) > 1:
        return
    try:
        name = context.args[0]
        surname = context.args[1]
        nickname = context.args[2]

    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.wrong_args_nickname)
        return

    result = userDao.edit_user_nickname(name, surname, nickname)

    if result == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.nickname_updated)
    elif result == 1:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.nickname_update_failed)


def edit_number(update, context):
    if check_permission(update.message.chat_id) > 1:
        return

    try:
        name = context.args[0]
        surname = context.args[1]
        number = int(context.args[2])

    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.wrong_args_number)
        return

    if number < 0 or number > 99:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.wrong_range_number)
        return
    elif number == 0:
        result = userDao.edit_user_number(name, surname, None)
    else:
        result = userDao.edit_user_number(name, surname, number)

    if result == 0:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.number_updated)
    elif result == 1:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.number_update_failed)


def change_active(update, context):
    if check_permission(update.message.chat_id) > 0:
        return

    try:
        name = context.args[0]
        surname = context.args[1]

    except IndexError:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.wrong_args_active)
        return

    userDao.edit_user_active(name, surname)
    context.bot.send_message(chat_id=update.message.chat_id, text=text.active_updated)


def members(update, context):
    if check_permission(update.message.chat_id) > 2:
        return

    people = userDao.get_all()
    message = ""

    for person in people:
        message = message \
                  + str(person.chat_id) + " " \
                  + person.name + " " \
                  + person.surname + " " \
                  + str(person.nickname) + " " \
                  + str(person.number) + " " \
                  + str(person.bday) + " "\
                  + str(person.delays) + " "\
                  + str(person.absence) + " "\
                  + str(person.fines0) + " "\
                  + str(person.fines1) + " " \
                  + str(person.active) + "\n"

    context.bot.send_message(chat_id=update.message.chat_id, text=message)
