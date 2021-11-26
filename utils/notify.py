import telegram

from dao.user_dao import get_avis_subscribers, get_admin


def notify_game_change_avis(message, bot):

    subscribers = get_avis_subscribers()

    for subscriber in subscribers:
        bot.send_message(chat_id=subscriber, text=message)


def notify_admin(message, bot):

    admins = get_admin()

    for admin in admins:
        bot.send_message(chat_id=admin, text=message, parse_mode=telegram.ParseMode.HTML)
