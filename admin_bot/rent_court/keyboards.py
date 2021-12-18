from typing import Union

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .static_text import YES, NO
from . import manage_data


def permission4rent_keyboard(
    tg_id: Union[str, int], tr_day_id: Union[str, int]
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=YES,
                callback_data=f"{manage_data.PERMISSION_FOR_RENT_COURT}{manage_data.PERMISSION_YES}|{tg_id}|{tr_day_id}",
            ),
            InlineKeyboardButton(
                text=NO,
                callback_data=f"{manage_data.PERMISSION_FOR_RENT_COURT}{manage_data.PERMISSION_NO}|{tg_id}|{tr_day_id}",
            ),
        ]
    ]

    return InlineKeyboardMarkup(buttons)
