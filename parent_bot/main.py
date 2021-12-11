import django
import os

from parent_bot.menu_and_commands.handlers import cancel, get_help
from parent_bot.menu_and_commands.static_text import HELP_BUTTON, CHILDREN_MENU_BUTTON

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters
)

import telegram

from tennis_bot.settings import PARENT_TELEGRAM_TOKEN
from .parent_registration.handlers import get_first_last_name, get_phone_number, start, \
    INSERT_FIO, INSERT_PHONE_NUMBER
from .child_registration.handlers import insert_child_first_last_name, INSERT_CHILD_FIO, get_child_first_last_name_and_create_child
from parent_bot.children_info.handlers import list_all_children
from .child_registration.manage_data import CHILD_REG

registration_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        INSERT_FIO: [MessageHandler(Filters.regex(r'^\w+\s\w+$'), get_first_last_name)],
        INSERT_PHONE_NUMBER: [MessageHandler(Filters.regex(r'^\d+$'), get_phone_number)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]

)
registration_child_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(insert_child_first_last_name, pattern=f'^{CHILD_REG}')],

    states={
        INSERT_CHILD_FIO: [MessageHandler(Filters.regex(r'^\w+\s\w+$'), get_child_first_last_name_and_create_child)],
    },

    fallbacks=[CommandHandler('cancel', cancel)]

)


def setup_dispatcher(dp):
    dp.add_handler(registration_handler)
    dp.add_handler(registration_child_handler)
    dp.add_handler(MessageHandler(Filters.regex(CHILDREN_MENU_BUTTON), list_all_children))

    dp.add_handler(MessageHandler(Filters.regex(HELP_BUTTON), get_help))

    return dp


def main():
    updater = Updater(PARENT_TELEGRAM_TOKEN)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = telegram.Bot(PARENT_TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()


bot = telegram.Bot(PARENT_TELEGRAM_TOKEN)

if __name__ == '__main__':
    main()
