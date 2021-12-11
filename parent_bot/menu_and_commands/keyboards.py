from telegram import ReplyKeyboardMarkup

from .static_text import HELP_BUTTON, CHILDREN_MENU_BUTTON


def construct_parent_main_menu():
    return ReplyKeyboardMarkup(
        [
            [CHILDREN_MENU_BUTTON, HELP_BUTTON]
        ],
        resize_keyboard=True
    )
