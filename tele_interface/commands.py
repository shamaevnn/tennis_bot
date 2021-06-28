from telegram.ext import ConversationHandler

from admin_bot.static_text import THIS_WAY_YEAH
from base.models import User
from base.utils import construct_main_menu
from tele_interface.handlers import INSERT_FIO, INSERT_PHONE_NUMBER
from tele_interface.user_info.handlers import user_main_info
from tele_interface.static_text import FIRST_TIME_GREETING, FIRST_TIME_INSERT_FIRST_LAST_MAME, \
    FIRST_TIME_INSERT_PHONE_NUMBER


def start(update, context):
    user, created = User.get_user_and_created(update, context)

    if created:
        update.message.reply_text(
            text=FIRST_TIME_GREETING,
        )
        if user.last_name and user.first_name:
            update.message.reply_text(
                text=FIRST_TIME_INSERT_PHONE_NUMBER,
            )
            return INSERT_PHONE_NUMBER
        else:
            update.message.reply_text(
                text=FIRST_TIME_INSERT_FIRST_LAST_MAME,
            )
            return INSERT_FIO
    else:
        user_main_info(update, context)
        return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text(
        text=THIS_WAY_YEAH,
        reply_markup=construct_main_menu()
    )

    return ConversationHandler.END
