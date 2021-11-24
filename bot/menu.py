
from telegram import InlineKeyboardMarkup

from dao.user_dao import user_exist

from utils.keyboard import keyboard_menu
from utils.lang import text


def menu(update, context):

    if not user_exist(update.message.from_user.id):
        update.message.reply_text("unauthorized")
        return

    keyboard = keyboard_menu()

    reply_markup = InlineKeyboardMarkup(keyboard)
    message = text("menu_init").format(update.message.from_user.first_name)

    update.message.reply_text(message, reply_markup=reply_markup)
