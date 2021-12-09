import re
import datetime
import requests
import unicodedata

from bs4 import BeautifulSoup

from utils.get_from_config import get_monza_link, get_monza_place
from utils.lang import text


def monza_games(update, context):

    games = get_monza_games_website()

    for game in games:
        print(game)


def update_monza_games(update, context):
    print("toDO")


def get_monza_games_website():
    link = get_monza_link()

    html_text = requests.get(link).text

    soup = BeautifulSoup(html_text, 'html.parser')

    my_place = get_monza_place()
    games = []

    for row in soup.find_all("tr"):

        giornata = row.find("td", class_="giornata")
        data = row.find("td", class_="data")
        casa = row.find("td", class_="casa")
        trasferta = row.find("td", class_="trasferta")
        orario = row.find("td", class_="orario")
        impianto = row.find("td", class_="impianto")
        # risultato = row.find("td", class_="risultato")

        try:
            date = to_date(data.text, orario.text)
            if impianto.text == my_place and date > datetime.datetime.now():
                giornata_u = unicodedata.normalize("NFKD", giornata.text).replace("Â°", "°")
                games.append((giornata_u, date, casa.text, trasferta.text))
        except Exception:
            continue

    return games


def to_date(date_string, hour_string):
    date_array = date_string.split("/")
    hour_array = hour_string.split(":")

    date = datetime.datetime(year=2000 + int(date_array[2]),
                             month=int(date_array[1]),
                             day=int(date_array[0]),
                             hour=int(hour_array[0]),
                             minute=int(hour_array[1]))
    return date
