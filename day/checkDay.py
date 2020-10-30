import datetime

from dao.userDao import *
from utils.text import happyBday
from paste.paste import addPerson
from utils.fastChat import getAVIS
from utils.fastChat import getPRADA


def checkBday(update, context):
    users = getUserBday()

    if not users:

        context.bot.send_message(chat_id=getPRADA(), text="someone is happy")

        for user in users:

            if user.nickname is not None:
                name = user.nickname
            else:
                name = user.surname

            age = datetime.date.today().year - user.bday.year

            context.bot.send_message(chat_id=getAVIS(), text=happyBday.format(name, age))

            if user.active == 1:
                addPerson(update, context, name=name)
                
    else:
        context.bot.send_message(chat_id=getPRADA(), text="nobody is happy")


def auto_checkBday(context):
    checkBday(None, context)
