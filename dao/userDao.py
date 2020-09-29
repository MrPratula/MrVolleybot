import json

import mysql.connector

from beans.User import User


def connect():
    with open("files/dbAccessData.json") as dbFile:
        db_dict = json.load(dbFile)

    try:
        return mysql.connector.connect(
            host=db_dict["host"],
            user=db_dict["user"],
            password=db_dict["password"],
            database=db_dict["database"]
        )

    except mysql.connector.Error:
        print("Can not connect to database")
        return None


# return a user with that id
def getUser(user_id):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT * FROM members WHERE chat_id = ?"

    cursor.execute(query, (str(user_id),))

    result = cursor.fetchall()

    try:

        person = result[0]

        chat_id = person[0]
        name = person[0]
        surname = person[0]
        nickname = person[0]
        number = person[0]
        bday = person[0]
        delays = person[0]
        absences = person[0]
        fines0 = person[0]
        fines1 = person[0]
        active = person[0]

    except IndexError:
        print("error")
        return

    return User(chat_id, name, surname, nickname, number, bday, delays, absences, fines0, fines1, active)


# return all people that are born in today's day and month
def getUserBday():
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT surname, nickname, bday " \
            "FROM members " \
            "WHERE DATE_FORMAT(bday, '%m-%d') = DATE_FORMAT(NOW(), '%m-%d')"

    cursor.execute(query)

    result = cursor.fetchall()

    people = []
    for person in result:

        people.append(User(surname=person[0], nickname=person[1], bday=person[2]))

    return people
