
from dao import userDao
from utils import fastChat


def check_permission(chat_id):

    if chat_id == fastChat.getPRADA():
        return 0

    people = userDao.get_id_active()

    for person in people:
        if chat_id == person.chat_id:
            if person.active is True:
                return 1
            else:
                return 2

    return 101
