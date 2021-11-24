

from utils.db import connect


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
    query = "DELETE FROM paste WHERE name = %s "

    try:
        cursor.execute(query, (name,))
        db.commit()
    except:
        print("can not delete person from lista paste")
