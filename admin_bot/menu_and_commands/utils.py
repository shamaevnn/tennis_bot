from telegram import Update
from telegram.ext import CallbackContext

from admin_bot.menu_and_commands.static_text import NO_PERMISSION
from base.models import Player


def check_coach_status_decor(func):
    def wrapper(update: Update, context: CallbackContext):
        res = None
        player, _ = Player.get_player_and_created(update, context)
        if player.is_coach:
            res = func(update, context)
        else:
            context.bot.send_message(player.tg_id, NO_PERMISSION, reply_markup=None)
        return res

    return wrapper
