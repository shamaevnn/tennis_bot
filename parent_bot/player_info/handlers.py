from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from base.models import Player
from parent_bot.registration.utils import check_status_decor
from parent_bot.menu_and_commands.keyboards import construct_parent_main_menu


@check_status_decor
def player_main_info(update: Update, context: CallbackContext):
    player, _ = Player.get_player_and_created(update, context)
    text = 'Привет, {first_name} {last_name}!'
    update.message.reply_text(
        text=text.format(first_name=player.first_name, last_name=player.last_name),
        reply_markup=construct_parent_main_menu(),
        parse_mode='HTML'
    )
    return ConversationHandler.END
