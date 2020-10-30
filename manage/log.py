from beans.Log import Log
from dao.logDao import add_text_log
from dao.logDao import add_command_log


def save_text(update, context):

    date = update.message.date
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    lang_code = update.message.from_user.language_code
    text = update.message.text

    log = Log(date=date, user_id=user_id, first_name=first_name, last_name=last_name, username=username,
              lang_code=lang_code, text=text)

    add_text_log(log)


def save_command(update, command):

    date = update.message.date
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name
    username = update.message.from_user.username
    lang_code = update.message.from_user.language_code
    command = command
    text = update.message.text

    log = Log(date=date, user_id=user_id, first_name=first_name, last_name=last_name, username=username,
              lang_code=lang_code, command=command, text=text)

    add_command_log(log)
