import traceback

from utils.db import connect


def user_exist(user_id):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT EXISTS(SELECT * FROM users WHERE chat_id = %s)"

    try:

        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

    except:
        print("can not check if user exist")
        return False

    if result[0][0] == 1:
        return True
    else:
        return False


def get_members_nick():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT nickname FROM users WHERE active = %s"

    try:

        cursor.execute(query, (True,))
        result = cursor.fetchall()

    except:
        print("can not get users nickname")
        return None

    names = []
    for nickname in result:
        names.append(nickname[0])

    return names


def get_avis_subscribers():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT chat_id FROM users WHERE avis_sub = %s"

    try:

        cursor.execute(query, (True,))
        result = cursor.fetchall()

    except:
        print("can not get avis subscribers id")
        return None

    if result:
        return result[0]
    else:
        return []


def get_user_nick(person_id):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT nickname FROM users WHERE chat_id = %s"

    try:

        cursor.execute(query, (person_id,))
        result = cursor.fetchall()

    except Exception:
        print("get_user_nick() had a problem")
        print(traceback.format_exc())
        return "NO NAME"

    return str(result[0][0])


def how_many():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT COUNT(*) FROM users WHERE active = %s"

    try:

        cursor.execute(query, (True,))
        result = cursor.fetchall()

    except:
        print("can not get how many active users")
        return None

    return int(result[0][0])


def get_admin():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT chat_id FROM users WHERE admin = %s"

    try:
        cursor.execute(query, (True,))
        result = cursor.fetchall()
    except Exception:
        print("get_admin() had a problem")
        print(traceback.format_exc())
        return []

    return result[0]
