import json


def get_key():

    try:
        with open("files/config.json", "r") as f_config:
            config_dict = json.load(f_config)
    except FileNotFoundError:
        print("can't open config.json file")
        exit(1)

    key = config_dict["key"]

    if key is None:
        print("no key in config.json")
        exit(1)

    else:
        return key


def get_avis_link():

    try:
        with open("files/config.json", "r") as f_config:
            config_dict = json.load(f_config)
    except FileNotFoundError:
        print("can not open config.json")
        return None

    return config_dict["avis_link"]


def get_team_name():

    try:
        with open("files/config.json", "r") as f_config:
            config_dict = json.load(f_config)
    except FileNotFoundError:
        print("can not open config.json")
        return None

    return config_dict["avis_name"]
