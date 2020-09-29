
import json


from utils import text
from utils.fastChat import getAVIS

filePath = "files/listaPaste.json"


def showList(update, context):
    with open(filePath, 'r') as f_paste:
        paste_dict = json.load(f_paste)

    message = '\n'.join(paste_dict)

    try:
        chat = update.message.chat_id
    except:
        chat = getAVIS()

    if message == '':
        message = text.emptyList

    context.bot.send_message(chat_id=chat, text=message)


def addPerson(update, context, name=None):
    if name is None:
        try:
            sent_name = context.args[0]
        except IndexError:
            context.bot.send_message(chat_id=update.message.chat_id,
                                     text=text.validName)
            return
    else:
        sent_name = name

    with open(filePath, 'r+') as f_paste:
        paste_dict = json.load(f_paste)
        paste_dict.append(sent_name)
        f_paste.seek(0)
        json.dump(paste_dict, f_paste, indent=4)
        f_paste.truncate()

    try:
        chat = update.message.chat_id
    except:
        chat = getAVIS()

    context.bot.send_message(chat_id=chat, text=text.personAdded.format(sent_name))

    showList(update, context)


def pop(update, context):
    with open(filePath, 'r+') as f_paste:
        paste_dict = json.load(f_paste)
        paste_dict.pop(0)
        f_paste.seek(0)
        json.dump(paste_dict, f_paste, indent=4)
        f_paste.truncate()

    context.bot.send_message(chat_id=update.message.chat_id, text=text.listUpdated)

    showList(update, context)


def remove(update, context):
    n = int(context.args[0])

    if n <= 1:
        context.bot.send_message(chat_id=update.message.chat_id, text=text.usePop)
        return

    with open(filePath, "r+") as f_paste:
        paste_dict = json.load(f_paste)
        if n > len(paste_dict):
            message = 'Out of index'
        else:
            name = paste_dict[n - 1]
            paste_dict.pop(n - 1)
            f_paste.seek(0)
            json.dump(paste_dict, f_paste, indent=4)
            f_paste.truncate()
            message = text.personRemoved.format(name)

    context.bot.send_message(chat_id=update.message.chat_id, text=message)

    showList(update, context)
