from utils import fastChat
from utils import text
from dao.userDao import getUserByFullName
from manage.security import check_permission
from manage.log import save_command


# kicked people can rejoin the group
def kick(update, context):
    save_command(update, "kick")
    if check_permission(update.message.from_user.id) > 0:
        context.bot.send_message(text=text.unauthorized, chat_id=update.message.chat_id)
        return

    try:
        people = getUserByFullName(context.args[0], context.args[1])
    except:
        message = text.args_not_given
        context.bot.send_message(text=message, chat_id=update.message.chat_id)
        return

    if not people:
        message = text.person_not_found.format(context.args[0], context.args[1])
        context.bot.send_message(text=message, chat_id=update.message.chat_id)
        return

    chat = fastChat.getAVIS()

    for person in people:
        try:
            context.bot.kick_chat_member(chat_id=chat, user_id=person.chat_id)
            context.bot.unban_chat_member(chat_id=chat, user_id=person.chat_id)
        except:
            message = text.can_not_kick.format(person.name + ' ' + person.surname, chat)
            context.bot.send_message(text=message, chat_id=update.message.chat_id)


# banned people can not join group
def ban(update, context):
    save_command(update, "ban")
    if check_permission(update.message.from_user.id) > 0:
        context.bot.send_message(text=text.unauthorized, chat_id=update.message.chat_id)
        return

    try:
        people = getUserByFullName(context.args[0], context.args[1])
    except:
        message = text.args_not_given
        context.bot.send_message(text=message, chat_id=update.message.chat_id)
        return

    if not people:
        message = text.person_not_found.format(context.args[0], context.args[1])
        context.bot.send_message(text=message, chat_id=update.message.chat_id)
        return

    chat = fastChat.getAVIS()

    for person in people:

        try:
            context.bot.kick_chat_member(chat_id=chat, user_id=person.chat_id)
        except:
            message = text.can_not_ban.format(person.name + ' ' + person.surname, chat)
            context.bot.send_message(text=message, chat_id=update.message.chat_id)


# unban people to let them rejoin group
def unban(update, context):
    save_command(update, "unban")
    if check_permission(update.message.from_user.id) > 0:
        context.bot.send_message(text=text.unauthorized, chat_id=update.message.chat_id)
        return

    try:
        people = getUserByFullName(context.args[0], context.args[1])
    except:
        message = text.args_not_given
        context.bot.send_message(text=message, chat_id=update.message.chat_id)
        return

    if not people:
        message = text.person_not_found.format(context.args[0], context.args[1])
        context.bot.send_message(text=message, chat_id=update.message.chat_id)
        return

    chat = fastChat.getAVIS()

    for person in people:

        try:
            context.bot.unban_chat_member(chat_id=chat, user_id=person.chat_id)
        except:
            message = text.can_not_unban.format(person.name + ' ' + person.surname, chat)
            context.bot.send_message(text=message, chat_id=update.message.chat_id)
