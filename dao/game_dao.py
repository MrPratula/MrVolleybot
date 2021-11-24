

from utils.db import connect



def insert_game(day, opponent):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "INSERT INTO avis_games_2021_2022 (date, opponent) VALUES (%s, %s)"

    try:
        cursor.execute(query, (day, opponent))
        db.commit()
    except:
        print("can not insert game into db")


def del_game(day, opponent):

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "DELETE FROM avis_games_2021_2022 WHERE date = %s AND opponent = %s"

    try:
        cursor.execute(query, (day, opponent))
        db.commit()
    except:
        print("can not delete game from db")


def get_all_games():

    db = connect()
    cursor = db.cursor(prepared=True)

    query = "SELECT * FROM avis_games_2021_2022"

    try:
        cursor.execute(query, ())
    except:
        print("can not get all games")
        return None

    return cursor.fetchall()
