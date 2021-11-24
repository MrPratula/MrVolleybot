
from telegram import InlineKeyboardButton


def keyboard_menu():

    keyboard = [[InlineKeyboardButton("Paste", callback_data="paste_show"),
                 InlineKeyboardButton("Allenamento", callback_data="workout_start")],

                [InlineKeyboardButton("Rimuovi Paste", callback_data="paste_members_remove"),
                 InlineKeyboardButton("Partita", callback_data="game")],

                [InlineKeyboardButton("Aggiungi Paste", callback_data="paste_members_add"),
                 InlineKeyboardButton("Multe", callback_data="workout_count")]
                ]

    return keyboard


def array_to_keyboard(array, callback_data):

    keyboard = []

    for name in array:

        data = "{}_{}".format(callback_data, name)

        if keyboard == [] or len(keyboard[len(keyboard) - 1]) == 2:
            keyboard.append([InlineKeyboardButton(name.capitalize(), callback_data=data)])
        else:
            keyboard[len(keyboard) - 1].append(InlineKeyboardButton(name.capitalize(), callback_data=data))

    return keyboard


def keyboard_late():

    keyboard = [[InlineKeyboardButton("Ritardo", callback_data="workout_delay"),
                 InlineKeyboardButton("Assente", callback_data="workout_absent")],

                [InlineKeyboardButton("Termina", callback_data="workout_end")]]

    return keyboard
