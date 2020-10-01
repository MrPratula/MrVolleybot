import datetime

from dao.userDao import *
from utils.text import happyBday
from paste.paste import addPerson
from utils.fastChat import getAVIS


def checkBday(update, context):
    users = getUserBday()

    if users is not None:

        for user in users:

            if user.nickname is not None:
                name = user.nickname
            else:
                name = user.surname

            age = datetime.date.today().year - user.bday.year

            context.bot.send_message(chat_id=getAVIS(), text=happyBday.format(name, age))

            if user.active == 1:
                addPerson(update, context, name=name)
                

def auto_checkBday(context):
    checkBday(None, context)
