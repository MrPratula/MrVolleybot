import json


def text(word):

    try:
        with open("files/config.json", "r") as fLang:
            fDict = json.load(fLang)

            lang = fDict["language"]
    except FileNotFoundError:
        lang = "eng"

    message = ""

    if lang == "it":
        with open("lang/it.json", "r", encoding="utf-8") as f_it:
            fDict = json.load(f_it)
            message = fDict[word]

    elif lang == "es":
        with open("lang/es.json", "r", encoding="utf-8") as f_es:
            fDict = json.load(f_es)
            message = fDict[word]

    if message == "":
        with open("lang/en.json", "r", encoding="utf-8") as f_en:
            fDict = json.load(f_en)
            message = fDict[word]

    return str(message)
