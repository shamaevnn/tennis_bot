

from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from base.models import Player
from parent_bot.registration.utils import check_status_decor


@check_status_decor
def player_main_info(update: Update, context: CallbackContext):

    player, _ = Player.get_player_and_created(update, context)
    should_pay_info = 'Привет'

    text = should_pay_info

    update.message.reply_text(
        text=text,
        parse_mode='HTML'
    )

    return ConversationHandler.END
