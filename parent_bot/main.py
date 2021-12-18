import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennis_bot.settings")
django.setup()
from telegram.ext import Updater

import telegram

from tennis_bot.settings import PARENT_TELEGRAM_TOKEN


def main():
    updater = Updater(PARENT_TELEGRAM_TOKEN)

    dp = updater.dispatcher

    bot_info = telegram.Bot(PARENT_TELEGRAM_TOKEN).get_me()
    bot_link = f"https://t.me/" + bot_info["username"]

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()


bot = telegram.Bot(PARENT_TELEGRAM_TOKEN)

if __name__ == "__main__":
    main()
