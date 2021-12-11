from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.models import Player
from parent_bot.child_registration.manage_data import CHILD_REG
from parent_bot.child_registration.static_text import CHILDREN_REG_BUTTON
from .manage_data import GET_CHILD_INFO


def list_all_children_with_add_one_more_button(parent: Player) -> InlineKeyboardMarkup:
    children_values = parent.children.all().values('first_name', 'last_name', 'id')

    buttons = []
    for value in children_values:
        child_first_last_name = f"{value['first_name']} {value['last_name']}"
        buttons.append([
            InlineKeyboardButton(
                text=child_first_last_name,
                callback_data=f"{GET_CHILD_INFO}{value['id']}"
            )
        ])
    buttons.append([
        InlineKeyboardButton(
            text=CHILDREN_REG_BUTTON,
            callback_data=CHILD_REG
        )
    ])
    return InlineKeyboardMarkup(buttons)
