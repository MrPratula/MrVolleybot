import json
import mysql.connector

from beans.Command import Command


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


def getCommands():
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT number, command FROM commands"

    try:
        cursor.execute(query)
    except:
        print("query failed")
        return

    result = cursor.fetchall()

    commands = []
    for command in result:

        try:
            commands.append(Command(command[0], command[1]))
        except:
            print("can not create command bean")

    print(commands)
    commands.sort(key=lambda f: f.number)
    return commands


def getCommandsFull():
    db = connect()
    cursor = db.cursor(prepared=True)
    query = "SELECT * FROM commands"

    try:
        cursor.execute(query)
    except:
        print("query failed")
        return

    result = cursor.fetchall()

    commands = []
    for command in result:

        try:

            num = command[0]
            com = command[1]
            args = ''
            description = ''

            if command[2] is not None:
                args = command[2]

            if command[3] is not None:
                description = command[3]

            commands.append(Command(num, com, args, description))
        except:
            print("can not create command bean")

    print(commands)
    return commands
