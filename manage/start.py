import json
from utils import text


def start(update, context):
    context.bot.send_message(text=text.start, chat_id=update.message.chat_id)


def help(update, context):
    with open("manage/commands.json", "r") as f_command:
        command_dict = json.load(f_command)

    message = text.help + "\n/" + "\n/".join(command_dict)

    context.bot.send_message(text=message, chat_id=update.message.chat_id)


def test(update, context):

    print("test")

