
import datetime
import traceback

from utils.db import connect
from utils.lang import text
from utils.notify import notify_group

from dao.paste_dao import add_paste


def check_bday(update, context):

    people = get_bdays()

    # person = [name, bday, active]
    for person in people:

        age = datetime.date.today().year - person[1].year
        message = text("check_bday_true").format(person[0], age)
        notify_group(message, context.bot)

        # active = \x01 | \x00
        if person[2] == '\x01':
            add_paste(person[0])
            message = text("check_bday_add").format(person[0])
            notify_group(message, context.bot)


# DAO

def get_bdays():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT nickname, bday, active " \
            "FROM users " \
            "WHERE DATE_FORMAT(bday, '%m-%d') = DATE_FORMAT(NOW(), '%m-%d')"

    try:
        cursor.execute(query, ())
        result = cursor.fetchall()
    except Exception:
        print("get_bdays() had a problem")
        print(traceback.format_exc())
        return []

    return result








