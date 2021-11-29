
from telegram import InlineKeyboardButton


def keyboard_menu():

    keyboard = [[InlineKeyboardButton("Paste 🍖", callback_data="paste_show"),
                 InlineKeyboardButton("Allenamento 💪", callback_data="workout_start")],

                [InlineKeyboardButton("Rimuovi Paste 📤", callback_data="paste_members_remove"),
                 InlineKeyboardButton("Aggiungi Paste 📥", callback_data="paste_members_add")],

                [InlineKeyboardButton("Punti 🥇", callback_data="score_view"),
                 InlineKeyboardButton("Mod Punti 📝", callback_data="score_edit")],

                [InlineKeyboardButton("Partita 🆚", callback_data="game"),
                 InlineKeyboardButton("Modifica ⚙", callback_data="edit_main")],

                [InlineKeyboardButton("Multe 💰", callback_data="workout_fines")]

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

    keyboard = [[InlineKeyboardButton("Ritardo ⏱", callback_data="workout_delay"),
                 InlineKeyboardButton("Assente ❌", callback_data="workout_absent")],

                [InlineKeyboardButton("🟢 Termina 🟢", callback_data="workout_end")]]

    return keyboard


# arg = abs | del
# people = [[mario, true], [rossi, false]]
def keyboard_active(people, arg):

    keyboard = []

    for person in people:

        data = f"workout_{arg}_{person[0]}"

        if keyboard == [] or len(keyboard[len(keyboard) - 1]) == 2:

            if person[1]:
                keyboard.append([InlineKeyboardButton(person[0] + "   🔴", callback_data=data)])
            else:
                keyboard.append([InlineKeyboardButton(person[0] + "   🟢", callback_data=data)])

        else:

            if person[1]:
                keyboard[len(keyboard) - 1].append(InlineKeyboardButton(person[0] + "   🔴", callback_data=data))
            else:
                keyboard[len(keyboard) - 1].append(InlineKeyboardButton(person[0] + "   🟢", callback_data=data))

    keyboard.append([InlineKeyboardButton("🔙   INDIETRO   🔙", callback_data="workout_start")])

    return keyboard


def keyboard_edit():

    keyboard = [[InlineKeyboardButton("Numero #️⃣", callback_data="edit_number"),
                 InlineKeyboardButton("Attivo ☑", callback_data="edit_bool_active")],

                [InlineKeyboardButton("AVIS sub 🏆", callback_data="edit_bool_avis_sub"),
                 InlineKeyboardButton("Monza sub 🏅", callback_data="edit_bool_monza_sub")]]

    return keyboard


def keyboard_bool():

    keyboard = [[InlineKeyboardButton("SI 🟢", callback_data="edit_ans_true"),
                 InlineKeyboardButton("NO 🔴", callback_data="edit_ans_false")]]

    return keyboard


def keyboard_numbers():

    keyboard = []

    for n in range(31):

        if n == 0:
            continue

        data = f"edit_set_num_{n}"

        if keyboard == [] or len(keyboard[len(keyboard) - 1]) == 5:
            keyboard.append([InlineKeyboardButton(f"{n}", callback_data=data)])
        else:
            keyboard[len(keyboard) - 1].append(InlineKeyboardButton(f"{n}", callback_data=data))

    return keyboard


def keyboard_scores(people):

    keyboard = []

    for person in people:

        name = person[0]
        score = person[1]
        data = f"score_press_[key]_{name}"

        keyboard.append([InlineKeyboardButton("➖", callback_data=data.replace("[key]", "sub1")),
                         InlineKeyboardButton(f"{name} = {score}", callback_data=data.replace("[key]", "none")),
                         InlineKeyboardButton("➕", callback_data=data.replace("[key]", "add1"))])

    keyboard.append([InlineKeyboardButton("🟢   FINE   🟢", callback_data="score_press_end")])

    return keyboard
