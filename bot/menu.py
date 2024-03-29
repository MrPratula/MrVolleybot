
from telegram import InlineKeyboardMarkup

from dao.user_dao import user_exist

from utils.keyboard import keyboard_menu
from utils.lang import text


def menu(update, context):

    try:

        if not user_exist(update.message.from_user.id):
            message = text("unauthorized")
            update.message.reply_text(message)
            return

        keyboard = keyboard_menu()

        reply_markup = InlineKeyboardMarkup(keyboard)
        message = text("menu_init").format(update.message.from_user.first_name)

        context.bot.send_message(update.message.chat_id, message, reply_markup=reply_markup)

    except:
        message = "Database offline"
        context.bot.send_message(update.message.chat_id, message)
