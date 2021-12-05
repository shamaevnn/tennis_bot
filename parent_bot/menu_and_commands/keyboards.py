from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Optional
from base.models import Player
from parent_bot.player_info.static_text import CHILDREN_REG_BUTTON, CHILDREN
from parent_bot.registration_children.manage_data import CHILD_REG
def construct_parent_main_menu(player: Optional[Player] = None):
    return ReplyKeyboardMarkup(
        [
            [CHILDREN]
        ],
        resize_keyboard=True
    )


def reg_child_butten(player: Optional[Player] = None):
    buttons = []
    buttons.append([
        InlineKeyboardButton(
            text=CHILDREN_REG_BUTTON,
            callback_data=CHILD_REG
        )
    ])
    return InlineKeyboardMarkup(buttons)
