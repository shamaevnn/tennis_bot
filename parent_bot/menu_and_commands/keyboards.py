from telegram import ReplyKeyboardMarkup
from typing import Optional
from base.models import Player
from parent_bot.player_info.static_text import CHILDREN_REG_BUTTON


def construct_parent_main_menu(player: Optional[Player] = None):
    return ReplyKeyboardMarkup(
        [
            [CHILDREN_REG_BUTTON]
        ],
        resize_keyboard=True
    )
