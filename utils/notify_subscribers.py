
from dao.user_dao import get_avis_subscribers


def notify_game_change_avis(message, bot):

    subscribers = get_avis_subscribers()

    for subscriber in subscribers:
        bot.send_message(chat_id=subscriber, text=message)
