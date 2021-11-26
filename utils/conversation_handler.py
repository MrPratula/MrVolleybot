
from telegram.ext import ConversationHandler, Filters, CommandHandler, MessageHandler

from bot.register import register, cancel, name, surname, nickname, bday, active, sub_a, sub_avis


NAME, SURNAME, NICKNAME, BDAY, ACTIVE, SUB_AVIS, SUB_A = range(7)


register_handler = ConversationHandler(

        entry_points=[CommandHandler("register", register)],

        states={

            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            SURNAME: [MessageHandler(Filters.text & ~Filters.command, surname)],
            NICKNAME: [MessageHandler(Filters.text & ~Filters.command, nickname)],
            BDAY: [MessageHandler(Filters.text & ~Filters.command, bday)],
            ACTIVE: [MessageHandler(Filters.text & ~Filters.command, active)],
            SUB_AVIS: [MessageHandler(Filters.text & ~Filters.command, sub_avis)],
            SUB_A: [MessageHandler(Filters.text & ~Filters.command, sub_a)]

        },

        fallbacks=[CommandHandler("cancel", cancel)]
    )
