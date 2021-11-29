from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from parent_bot.registration.static_text import CHILDREN_REG_FIO
from parent_bot.registration.utils import check_status_decor

INSERT_CHILD_FIO = range(1)


@check_status_decor
def get_children_reg(update: Update, context: CallbackContext):
    update.message.reply_text(
        CHILDREN_REG_FIO
    )
    print("Хоть что-то работает")
    return INSERT_CHILD_FIO
