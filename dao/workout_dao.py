import datetime

from utils.db import connect





def add_absence(person_id):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "INSERT INTO workouts_2021_2022 (date, person, asbent) VALUES (%s, %s, NOT asbent)"
    val = (datetime.date.today(), person_id)

    try:
        cursor.execute(query, val)
        db.commit()
    except:

        query = "UPDATE workouts_2021_2022 SET asbent = not asbent WHERE date = %s AND person = %s"

        try:
            cursor.execute(query, val)
            db.commit()
        except:
            print("can not change person delay")


def get_today_delay():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT person FROM workouts_2021_2022 WHERE date = %s and delay = %s"

    today = datetime.date.today()
    try:
        cursor.execute(query, (today, True))
    except:
        print("can not get today delays")
        return None

    try:
        return cursor.fetchall()[0]
    except IndexError:
        return None


def get_today_absences():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT person FROM workouts_2021_2022 WHERE date = %s and asbent = %s"

    today = datetime.date.today()
    try:
        cursor.execute(query, (today, True))
    except:
        print("can not get today absence")
        return None

    try:
        return cursor.fetchall()[0]
    except IndexError:
        return None
