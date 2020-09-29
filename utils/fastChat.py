import json


def getAVIS():
    with open("files/defaultChatId.json", "r") as f_chat:
        chat_dict = json.load(f_chat)

    return chat_dict["AVIS"]


def getPRADA():
    with open("files/defaultChatId.json", "r") as f_chat:
        chat_dict = json.load(f_chat)

    return chat_dict["PRADA"]
