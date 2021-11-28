from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from base.common_for_bots.static_text import THIS_WAY_YEAH
from base.models import Player
from parent_bot.menu_and_commands.static_text import HELP_MESSAGE
from parent_bot.registration.static_text import FIRST_TIME_GREETING, FIRST_TIME_INSERT_FIRST_LAST_MAME, \
    FIRST_TIME_INSERT_PHONE_NUMBER
from parent_bot.player_info.handlers import player_main_info

INSERT_FIO, INSERT_PHONE_NUMBER = range(2)

def start(update: Update, context: CallbackContext):
    player, created = Player.get_player_and_created(update, context)

    if created:
        update.message.reply_text(
            text=FIRST_TIME_GREETING,
        )
        if player.last_name and player.first_name:
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
        player_main_info(update, context)
        return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=THIS_WAY_YEAH,
    )

    return ConversationHandler.END


def get_help(update: Update, context: CallbackContext):
    player, _ = Player.get_player_and_created(update, context)
    update.message.reply_text(
        text=HELP_MESSAGE,
    )
