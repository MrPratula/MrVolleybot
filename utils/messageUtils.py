import requests


def send_text(chat_id, message):

    with open("files/key.txt", "r") as fKey:
        key = fKey.readline()

    data = [('chat_id', str(chat_id)), ('text', message)]

    url = 'https://api.telegram.org/bot{}/sendMessage'.format(key)
    requests.post(url, data=data)
