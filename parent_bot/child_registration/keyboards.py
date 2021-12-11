from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .manage_data import CHILD_REG
from .static_text import CHILDREN_REG_BUTTON


def reg_child_button():
    buttons = [[
        InlineKeyboardButton(
            text=CHILDREN_REG_BUTTON,
            callback_data=CHILD_REG
        )
    ]]
    return InlineKeyboardMarkup(buttons)