import json
import mysql.connector

from beans.Log import Log


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


def add_text_log(log):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "INSERT INTO log (date, user_id, first_name, last_name, username, lang_code, text) VALUES (%s, %s, %s, " \
            "%s, %s, %s, %s) "

    data = (log.date, log.user_id, log.first_name, log.last_name, log.username, log.lang_code, log.text)

    try:
        cursor.execute(query, data)
        db.commit()
        return 0
    except mysql.connector.errors.IntegrityError:
        return 1


def add_command_log(log):
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "INSERT INTO log (date, user_id, first_name, last_name, username, lang_code, command, text) VALUES (%s, " \
            "%s, %s, %s, %s, %s, %s, %s) "

    data = (log.date, log.user_id, log.first_name, log.last_name, log.username, log.lang_code, log.command, log.text)

    try:
        cursor.execute(query, data)
        db.commit()
        return 0
    except mysql.connector.errors.IntegrityError:
        return 1
