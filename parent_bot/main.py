import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters, Dispatcher
)

import telegram

from tennis_bot.settings import PARENT_TELEGRAM_TOKEN
from parent_bot.registration.handlers import get_first_last_name, get_phone_number,get_children_first_last_name
from parent_bot.registration_children.handlers import get_children_reg
from parent_bot.menu_and_commands.handlers import start, cancel, INSERT_FIO, INSERT_PHONE_NUMBER
from parent_bot.player_info.static_text import CHILDREN_REG_BUTTON

registration_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],

    states={
        INSERT_FIO: [MessageHandler(Filters.regex(r'^\w+\s\w+$'), get_first_last_name)],
        INSERT_PHONE_NUMBER: [MessageHandler(Filters.regex(r'^\d+$'), get_phone_number)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]

)


def setup_dispatcher(dp: object):
    dp.add_handler(registration_handler)
    dp.add_handler(MessageHandler(Filters.regex(CHILDREN_REG_BUTTON), get_children_reg))

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
