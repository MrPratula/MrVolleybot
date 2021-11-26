
import datetime
import traceback

from telegram import InlineKeyboardMarkup

from dao.user_dao import user_exist
from utils.db import connect
from utils.keyboard import keyboard_late, keyboard_active
from utils.lang import text


def workout_c(update, context):

    if not user_exist(update.message.from_user.id):
        update.message.reply_text("unauthorized")
        return

    keyboard = keyboard_late()

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = generate_workout_text()

    update.message.reply_text(message, reply_markup=reply_markup)


def workout_b(update, context):

    query = update.callback_query
    keyboard = keyboard_late()

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = generate_workout_text()

    query.edit_message_text(message, reply_markup=reply_markup)


def delay_button(update, context):

    query = update.callback_query

    actives = get_actives_delay()
    keyboard = keyboard_active(actives, "del")

    message = generate_workout_text()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)


def absent_button(update, context):

    query = update.callback_query

    actives = get_actives_absence()
    keyboard = keyboard_active(actives, "abs")

    message = generate_workout_text()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)


def terminate_button(update, context):

    query = update.callback_query
    message = generate_workout_text()
    query.edit_message_text(message)


def person_absent_button(update, context):

    query = update.callback_query
    name = query.data[12:]

    abs_id = name_to_id(name)
    add_absent(abs_id)

    actives = get_actives_absence()
    keyboard = keyboard_active(actives, "abs")

    message = generate_workout_text()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)


def person_delay_button(update, context):

    query = update.callback_query
    name = query.data[12:]

    del_id = name_to_id(name)
    add_delay(del_id)

    actives = get_actives_delay()
    keyboard = keyboard_active(actives, "del")

    message = generate_workout_text()
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(message, reply_markup=reply_markup)


def generate_workout_text():

    delays = get_actives_delay()
    absences = get_actives_absence()

    today = datetime.date.today()

    total = how_many()
    present = total
    names_abs = []

    for person in absences:
        if person[1]:
            present -= 1
            names_abs.append(person[0])

    if present == total:
        abs_text = ""
    else:
        abs_text = text("workout_absent") + "\n".join(names_abs)

    names_del = []
    for person in delays:
        if person[1]:
            names_del.append(person[0])

    if not names_del:
        del_text = ""
    else:
        del_text = text("workout_delay") + "\n".join(names_del)

    message = text("workout_main").format(today, present) + abs_text + del_text

    return message


# DAO

def get_actives_delay():

    actives = []

    db = connect()
    cursor = db.cursor(prepared=True)

    query1 = "SELECT nickname FROM users WHERE active = TRUE ORDER BY nickname"

    try:
        cursor.execute(query1, ())
        result_actives = cursor.fetchall()
    except Exception:
        print("get_actives_delay() had a problem")
        print(traceback.format_exc())
        return []

    if not result_actives:
        return []

    query2 = "SELECT nickname FROM users, workouts_2021_2022 WHERE date = %s AND chat_id = person AND delay = TRUE"

    today = datetime.date.today()
    try:
        cursor.execute(query2, (today,))
        result_delay = cursor.fetchall()
    except Exception:
        print("get_actives_delay() had a problem")
        print(traceback.format_exc())
        return []

    for person in result_actives:

        if person in result_delay:
            actives.append([list(person)[0], True])
        else:
            actives.append([list(person)[0], False])

    return actives


def get_actives_absence():

    absences = []

    db = connect()
    cursor = db.cursor(prepared=True)

    query1 = "SELECT nickname FROM users WHERE active = TRUE ORDER BY nickname"

    try:
        cursor.execute(query1, ())
        result_actives = cursor.fetchall()
    except Exception:
        print("get_actives_absence() had a problem")
        print(traceback.format_exc())
        return []

    if not result_actives:
        return []

    query2 = "SELECT nickname FROM users, workouts_2021_2022 WHERE date = %s AND chat_id = person AND absent = TRUE"

    today = datetime.date.today()
    try:
        cursor.execute(query2, (today,))
        result_delay = cursor.fetchall()
    except Exception:
        print("get_actives_delay() had a problem")
        print(traceback.format_exc())
        return []

    for person in result_actives:

        if person in result_delay:
            absences.append([list(person)[0], True])
        else:
            absences.append([list(person)[0], False])

    return absences


def add_delay(person_id):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "INSERT INTO workouts_2021_2022 (date, person, delay) VALUES (%s, %s, NOT delay)"
    val = (datetime.date.today(), person_id)

    try:
        cursor.execute(query, val)
        db.commit()
    except:

        query = "UPDATE workouts_2021_2022 SET delay = not delay WHERE date = %s AND person = %s"

        try:
            cursor.execute(query, val)
            db.commit()
        except Exception:
            print("add_delay() had a problem")
            print(traceback.format_exc())


def add_absent(person_id):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "INSERT INTO workouts_2021_2022 (date, person, absent) VALUES (%s, %s, NOT absent)"
    val = (datetime.date.today(), person_id)

    try:
        cursor.execute(query, val)
        db.commit()
    except:

        query = "UPDATE workouts_2021_2022 SET absent = not absent WHERE date = %s AND person = %s"

        try:
            cursor.execute(query, val)
            db.commit()
        except Exception:
            print("add_absent() had a problem")
            print(traceback.format_exc())


def how_many():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT COUNT(*) FROM users WHERE active = %s"

    try:
        cursor.execute(query, (True,))
        result = cursor.fetchall()
    except Exception:
        print("how_many() had a problem")
        print(traceback.format_exc())
        return 100

    return int(result[0][0])


def name_to_id(name):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT chat_id FROM users WHERE nickname = %s"

    try:
        cursor.execute(query, (name,))
        result = cursor.fetchall()
    except Exception:
        print("name_to_id() had a problem")
        print(traceback.format_exc())
        return 0

    return int(result[0][0])
