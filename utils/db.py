import json
import mysql.connector


def connect():

    with open("files/config.json") as f_config:
        config_dict = json.load(f_config)

        try:
            return mysql.connector.connect(
                host=config_dict["host"],
                user=config_dict["user"],
                password=config_dict["password"],
                database=config_dict["database"]
            )

        except mysql.connector.Error:
            print("Can not connect to database")
            return None
