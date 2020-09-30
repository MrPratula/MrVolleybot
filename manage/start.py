import json
from utils import text


help_file = "public_files/commands.json"


def start(update, context):
    your_id = update.message.chat_id
    context.bot.send_message(text=text.start.format(your_id), chat_id=update.message.chat_id)


def help(update, context):
    with open(help_file, "r") as f_command:
        command_dict = json.load(f_command)

    message = text.help + "\n/" + "\n/".join(command_dict)

    context.bot.send_message(text=message, chat_id=update.message.chat_id)


def test(update, context):

    print("test")

