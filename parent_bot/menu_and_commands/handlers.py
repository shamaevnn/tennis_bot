from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from base.common_for_bots.static_text import THIS_WAY_YEAH
from .static_text import HELP_MESSAGE


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=THIS_WAY_YEAH,
    )

    return ConversationHandler.END


def get_help(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=HELP_MESSAGE,
    )
