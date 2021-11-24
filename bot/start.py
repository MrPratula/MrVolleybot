
from utils.lang import text
from dao.user_dao import user_exist


def start(update, context):

    if user_exist(update.message.from_user.id):
        name = update.message.from_user.first_name
        message = text("start_yes").format(name)

    else:
        message = text("unauthorized")
    update.message.reply_text(message)
