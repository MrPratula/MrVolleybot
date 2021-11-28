import datetime
import traceback

from telegram import InlineKeyboardMarkup

from utils.db import connect
from utils.keyboard import keyboard_scores
from dao.user_dao import get_user_id, user_exist
from utils.lang import text


def score_edit(update, context):

    query = update.callback_query

    people = get_scores()
    keyboard = keyboard_scores(people)

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = text("score_edit")

    query.edit_message_text(message, reply_markup=reply_markup)


def score_edit_press(update, context):

    query = update.callback_query

    name = query.data[17:]
    what = query.data[12:16]

    if what == "none":
        return

    if what == "end":
        message = text("score_edit_end")
        query.edit_message_text(message)
        return

    user_id = get_user_id(name)
    update_score(user_id, what)

    score_edit(update, context)


def score_view_b(update, context):

    scores = get_scores()
    message = text("score_order").format(datetime.date.today().year, get_message_score(scores))
    update.callback_query.edit_message_text(message)


def score_view_c(update, context):

    if not user_exist(update.message.from_user.id):
        message = text("unauthorized")
        update.message.reply_text(message)
        return

    scores = get_scores()
    message = text("score_order").format(datetime.date.today().year, get_message_score(scores))
    update.message.reply_text(message)


def get_message_score(scores):

    message = ""
    count = 0
    scores.sort(key=lambda i: i[1], reverse=True)

    for score in scores:

        count += 1

        if count == 1:
            message = message + f"🥇 {score[0]} = {score[1]}\n"
        elif count == 2:
            message = message + f"🥈 {score[0]} = {score[1]}\n"
        elif count == 3:
            message = message + f"🥉 {score[0]} = {score[1]}\n"
        else:
            message = message + f"💩 {score[0]} = {score[1]}\n"

    return message


# DAO

def get_scores():

    db = connect()
    cursor = db.cursor(prepared=True)

    query1 = "SELECT nickname FROM users WHERE active = TRUE ORDER BY nickname"

    try:
        cursor.execute(query1, ())
        result_actives = cursor.fetchall()
    except Exception:
        print("get_scores() had a problem")
        print(traceback.format_exc())
        return []

    if not result_actives:
        return []

    query2 = "SELECT nickname, score FROM users, score_2021_2022 WHERE chat_id = user_id"

    try:
        cursor.execute(query2, ())
        result_scores = cursor.fetchall()
    except Exception:
        print("get_scores() had a problem")
        print(traceback.format_exc())
        return []

    scores = []
    copy = []

    for x in result_scores:
        copy.append((x[0],))

    for person_1 in result_actives:
        name_1 = person_1[0]
        if person_1 in copy:
            for person_2 in result_scores:
                name_2 = person_2[0]
                score_2 = person_2[1]
                if name_1 == name_2:
                    scores.append((name_2, score_2))
        else:
            scores.append((name_1, 0))

    return scores


def update_score(user_id, what):

    db = connect()
    cursor = db.cursor(prepared=True)

    if what == "sub1":
        query = "INSERT INTO score_2021_2022 (user_id, score) VALUE (%s, %s)"
        data = (user_id, -1)
    else:
        query = "INSERT INTO score_2021_2022 (user_id, score) VALUE (%s, %s) "
        data = (user_id, 1)

    try:
        cursor.execute(query, data)
        db.commit()
    except Exception:

        if what == "sub1":
            query = "UPDATE score_2021_2022 SET score = score - 1 WHERE user_id = %s"
        else:
            query = "UPDATE score_2021_2022 SET score = score + 1 WHERE user_id = %s"

        try:
            cursor.execute(query, (user_id,))
            db.commit()
        except Exception:
            print("update_score() had a problem")
            print(traceback.format_exc())
