from base.utils.telegram import extract_user_data_from_update
from telegram import Update
from typing import Tuple
from base.models import Player


def create_child(update: Update) -> Tuple[Player, bool]:
    """ python-telegram-bot's Update, Context --> User instance """
    data = extract_user_data_from_update(update)
    parent = Player.from_update(update)
    u = Player.objects.сreate(
        tg_id=None,
        parent=parent
    )
    return u
