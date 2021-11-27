import datetime
import traceback

import telegram

from dao.user_dao import user_exist, is_admin
from utils.db import connect
from utils.lang import text
from utils.notify import notify_registration


def new(update, context):

    user_id = update.message.from_user.id

    if not user_exist(update.message.from_user.id):
        message = text("unauthorized")
        update.message.reply_text(message)
        return

    if not is_admin(user_id):
        message = text("unauthorized_2")
        update.message.reply_text(message)
        return

    data = context.args

    try:

        if not data:
            message = text("new_example")
        else:

            user_id = int(data[0])
            name = data[1].lower()
            surname = data[2].lower()
            nickname = data[3]
            date_s = data[4]

            if data[5] == "si":
                active = True
            else:
                active = False

            if data[6] == "si":
                avis = True
            else:
                avis = False

            if data[7] == "si":
                monza = True
            else:
                monza = False

            date_array = date_s.split("-")
            day = int(date_array[0])
            month = int(date_array[1])
            year = int(date_array[2])

            bday = datetime.date(year, month, day)

            db = connect()
            cursor = db.cursor(prepared=True)

            query = "INSERT INTO users (chat_id, name, surname, nickname, bday,  " \
                    "                   active, avis_sub, monza_sub) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            val = (user_id, name, surname, nickname, bday, active, avis, monza)

            try:
                cursor.execute(query, val)
                db.commit()
                message = text("new_ok").format(f"{name} {surname}".title())
            except Exception:
                print("new() had a problem")
                error = traceback.format_exc()
                print(error)
                message = text("new_error").format(error)
                update.message.reply_text(message, parse_mode=telegram.ParseMode.HTML)
                return

        notify_registration(user_id, context.bot)
        update.message.reply_text(message, parse_mode=telegram.ParseMode.HTML)

    except Exception:
        print("new() had a problem")
        error = traceback.format_exc()
        print(error)
        message = text("new_error").format(error)
        update.message.reply_text(message, parse_mode=telegram.ParseMode.HTML)


def my_id(update, context):

    chat_id = update.message.from_user.id
    print(chat_id)
    update.message.reply_text(f"il tuo id è <code>{chat_id}</code>", parse_mode=telegram.ParseMode.HTML)
