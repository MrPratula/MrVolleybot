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

    """
    update_monza_games(update, context)
    games = get_all_games()

    today = datetime.datetime.now()

    remaining_games = []
    for game in games:
        if game[0] >= today:
            remaining_games.append(game)

    date = remaining_games[0][0].strftime("%a %d-%m-%Y %H:%M")
    first_game = "{} - {}".format(date, remaining_games[0][1])
    remaining_games.pop(0)
    other_games = ""
    for game in remaining_games:
        date = game[0].strftime("%a %d-%m-%Y %H:%M")
        other_games = other_games + "{} - {}\n".format(date, game[1])

    message = text("game_remaining").format(first_game, other_games)
    update.callback_query.edit_message_text(message, parse_mode=telegram.ParseMode.HTML)
    """


def update_monza_games(update, context):
    games = get_monza_games_website()
    new_games = []
    for game in games:
        date = game[0][0].split("/")
        time = str(re.findall("[0-2][0-9].[0-5][0-9]", game[0][1])[0]).split(".")
        day = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0]), int(time[1]))
        opponent = game[1]
        new_games.append((day, opponent))

    old_games = get_all_games()

    new_games_copy = new_games.copy()
    old_games_copy = old_games.copy()

    for game in new_games:
        if game in old_games:
            old_games_copy.remove(game)
            new_games_copy.remove(game)

    old_games = old_games_copy
    new_games = new_games_copy

    message = text("game_changed")

    if old_games:
        for game in old_games:
            del_game(game[0], game[1])
            date = game[0].strftime("%a %d-%m-%Y %H:%M")
            msg = text("game_remove").format(date, game[1])
            message = message + "\n" + msg

    if new_games:
        for game in new_games:
            insert_game(game[0], game[1])
            date = game[0].strftime("%a %d-%m-%Y %H:%M")
            msg = text("game_add").format(date, game[1])
            message = message + "\n" + msg

    if old_games == [] and new_games == []:

        try:
            update.message.reply_text(text("game_not_changed"))
        except:
            return
    else:
        notify_game_change_avis(message, context.bot)


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
        finally:
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
