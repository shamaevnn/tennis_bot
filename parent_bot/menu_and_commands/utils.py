from telegram import Update
from telegram.ext import CallbackContext

from base.models import Player
from parent_bot.menu_and_commands.static_text import COACH_HAVE_NOT_CONFIRMED_YET


def check_status_decor(func):
    """декоратор, который дает доступ к родительскому боту если есть галочка is_parent"""
    def wrapper(update: Update, context: CallbackContext):
        res = None
        player, _ = Player.get_player_and_created(update, context)
        if player.is_parent:
            res = func(update, context)
        else:
            context.bot.send_message(player.tg_id, COACH_HAVE_NOT_CONFIRMED_YET)
        return res

    return wrapper
