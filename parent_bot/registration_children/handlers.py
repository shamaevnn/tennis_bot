from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from base.models import Player
from parent_bot.registration.handlers import get_children_first_last_name
from parent_bot.registration.utils import check_status_decor


@check_status_decor
def get_children_reg(update: Update, context: CallbackContext):
    #player, _ = Player.get_player_and_created(update, context)
    print("Хоть что-то работает")
    return get_children_first_last_name
