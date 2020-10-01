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

    try:
        cursor.execute(query, (str(user_id),))
    except:
        print("query failed")
        return

    result = cursor.fetchall()

    try:
        person = result[0]

        chat_id = person[0]
        name = person[1]
        surname = person[2]
        nickname = person[3]
        number = person[4]
        bday = person[5]
        delays = person[6]
        absences = person[7]
        fines0 = person[8]
        fines1 = person[9]
        active = person[10]

    except IndexError:
        print("can not create user bean")
        return

    return User(chat_id, name, surname, nickname, number, bday, delays, absences, fines0, fines1, active)


# return all people that are born in today's day and month
def getUserBday():
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT surname, nickname, bday, active " \
            "FROM members " \
            "WHERE DATE_FORMAT(bday, '%m-%d') = DATE_FORMAT(NOW(), '%m-%d')"

    cursor.execute(query)

    result = cursor.fetchall()

    people = []
    for person in result:
        people.append(User(surname=person[0], nickname=person[1], bday=person[2], active=person[3]))

    return people


# return a user with provided name and surname
def getUserByFullName(name, surname):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT * FROM members WHERE name = ? && surname = ?"

    try:
        cursor.execute(query, (str(name), str(surname)))
    except:
        print("query failed")
        return

    result = cursor.fetchall()

    people = []
    for person in result:
        try:
            chat_id = person[0]
            name = person[1]
            surname = person[2]
            nickname = person[3]
            number = person[4]
            bday = person[5]
            delays = person[6]
            absences = person[7]
            fines0 = person[8]
            fines1 = person[9]
            active = person[10]

            user = User(chat_id, name, surname, nickname, number, bday, delays, absences, fines0, fines1, active)
            people.append(user)

        except IndexError:
            print("can not create user bean")

    return people


# get a user with chat, name, surname, bday and insert it into db
def create_new_user(user):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "INSERT INTO members (chat_id, name, surname, bday) VALUES (%s, %s, %s, %s)"

    data = (user.chat_id, user.name, user.surname, user.bday)

    try:
        cursor.execute(query, data)
        db.commit()
        return 0
    except mysql.connector.errors.IntegrityError:
        return 1


# edit user nickname
def edit_user_nickname(name, surname, new_nickname):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "UPDATE members SET nickname = %s WHERE name = %s && surname = %s"
    data = (new_nickname, name, surname)

    try:
        cursor.execute(query, data)
        db.commit()
        return 0
    except:
        return 1


# edit user number
def edit_user_number(name, surname, new_number):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "UPDATE members SET number = %s WHERE name = %s && surname = %s"
    data = (new_number, name, surname)

    try:
        cursor.execute(query, data)
        db.commit()
        return 0
    except:
        return 1


# edit user active
def edit_user_active(name, surname):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "UPDATE members SET active = NOT active WHERE name = %s && surname = %s"
    data = (name, surname)

    cursor.execute(query, data)
    db.commit()


# get all members
def get_all():
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT * FROM members"

    try:
        cursor.execute(query)
    except:
        print("query failed")
        return

    result = cursor.fetchall()

    people = []
    for person in result:
        try:
            chat_id = person[0]
            name = person[1]
            surname = person[2]
            nickname = person[3]
            number = person[4]
            bday = person[5]
            delays = person[6]
            absences = person[7]
            fines0 = person[8]
            fines1 = person[9]
            active = person[10]

            user = User(chat_id, name, surname, nickname, number, bday, delays, absences, fines0, fines1, active)
            people.append(user)

        except IndexError:
            print("can not create user bean")

    return people


# return all id and all active for check permissions
def get_id_active():
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT chat_id, active FROM members"

    try:
        cursor.execute(query)
    except:
        print("query failed")
        return

    result = cursor.fetchall()

    people = []
    for person in result:
        try:
            chat_id = person[0]
            active = person[1]

            user = User(chat_id=chat_id, active=active)
            people.append(user)

        except IndexError:
            print("can not create user bean")

    return people
