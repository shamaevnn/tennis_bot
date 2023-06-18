from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from base.common_for_bots.player_info import get_player_info
from base.models import Player
from player_bot.menu_and_commands.keyboards import construct_main_menu

from player_bot.registration.utils import check_status_decor


@check_status_decor
def player_main_info(update: Update, context: CallbackContext):
    """посмотреть, основную инфу:
    статус
    группа, если есть
    отыгрыши
    сколько должен заплатить
    """

    player, _ = Player.get_player_and_created(update, context)
    text = get_player_info(player=player)

    update.message.reply_text(
        text=text, parse_mode="HTML", reply_markup=construct_main_menu(player)
    )
    return ConversationHandler.END
