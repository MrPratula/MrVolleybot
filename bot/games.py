import re

import requests
import datetime

import telegram
from bs4 import BeautifulSoup

from utils.get_from_config import get_avis_link, get_team_name
from dao.game_dao import insert_game, del_game, get_all_games
from utils.notify import notify_game_change_avis
from utils.lang import text


def update_avis_games(update, context):

    games = get_avis_games_federvolley()
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


def avis_games(update, context):

    update_avis_games(update, context)
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


def get_avis_games_federvolley():

    link = get_avis_link()

    html_text = requests.get(link).text

    soup = BeautifulSoup(html_text, 'html.parser')

    my_team = get_team_name()
    games = []

    for table in soup.find_all("table", class_="GridView"):
        for row in table.find_all("tr", class_="RowGridView"):
            if my_team in row.text:
                columns = row.find_all("td")
                date = columns[1].find("b").find("span").contents[0::2]
                opponent = list(filter(lambda e: e != my_team, columns[2].find("b").find("span").contents[0::2]))[0]
                games.append((date, opponent))

    return games
