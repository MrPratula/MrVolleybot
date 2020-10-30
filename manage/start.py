from utils import text
from dao.commandDao import getCommands
from dao.commandDao import getCommandsFull
from manage.security import check_permission
from manage.log import save_command


def start(update, context):
    save_command(update, "start")
    your_id = update.message.chat_id
    context.bot.send_message(text=text.start.format(your_id), chat_id=update.message.chat_id)


def help(update, context):
    save_command(update, "help")
    if check_permission(update.message.from_user.id) > 2:
        context.bot.send_message(text=text.unauthorized, chat_id=update.message.chat_id)
        return

    commands = getCommands()
    message = text.help + '\n'
    for command in commands:
        message = message + '\n/' + command.command

    context.bot.send_message(text=message, chat_id=update.message.chat_id)


def man(update, context):
    save_command(update, "man")
    if check_permission(update.message.from_user.id) > 2:
        context.bot.send_message(text=text.unauthorized, chat_id=update.message.chat_id)
        return

    commands = getCommandsFull()
    message = text.man + '\n'

    for command in commands:
        message = message + '\n\n/' + \
                  command.command + ' ' + command.args + '\n' + \
                  command.description.capitalize() + ';'

    context.bot.send_message(text=message, chat_id=update.message.chat_id)


def test(update, context):
    save_command(update, "test")
    print("test")
