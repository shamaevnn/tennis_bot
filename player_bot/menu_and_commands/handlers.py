from telegram.ext import ConversationHandler

from base.common_for_bots.static_text import THIS_WAY_YEAH
from base.models import User
from player_bot.menu_and_commands.keyboard_utils import construct_main_menu
from player_bot.menu_and_commands.static_text import HELP_MESSAGE
from player_bot.registration.static_text import FIRST_TIME_GREETING, FIRST_TIME_INSERT_FIRST_LAST_MAME, \
    FIRST_TIME_INSERT_PHONE_NUMBER
from player_bot.user_info.handlers import user_main_info


INSERT_FIO, INSERT_PHONE_NUMBER = range(2)


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


def get_help(update, context):
    user, _ = User.get_user_and_created(update, context)
    update.message.reply_text(
        text=HELP_MESSAGE,
        reply_markup=construct_main_menu(user)
    )